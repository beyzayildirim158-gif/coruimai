# Instagram AI Agent Orchestrator
# Python FastAPI with NEW PIPELINE ARCHITECTURE
"""
NEW PIPELINE AKIŞI:
1. START: Apify Scrape - Ham veri çekimi
2. DELTA SYNC: PostgreSQL'den önceki raporu getir
3. STAGE 1: DOMAIN MASTER - Sektör ve benchmark belirleme (Foundation)
4. STAGE 2: PHD AGENT TEAM - Growth, Sales, Visual, Technical, Community paralel çalışır
5. STAGE 3: GOVERNOR AUDIT - Veto Gate, çelişki kontrolü
6. STAGE 4: ELI5 & HOOK AUDIT - Formatları düzenleme, hook yazma
7. FINAL: JSON & PDF Output
"""

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uvicorn
import asyncio
import httpx
import redis.asyncio as redis
import json
import os
import logging
from datetime import datetime
from contextlib import asynccontextmanager

# Import both old orchestrator (for backward compatibility) and new pipeline
from agents.orchestrator import AgentOrchestrator
from agents.new_pipeline import NewPipelineOrchestrator, create_pipeline_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
redis_client: Optional[redis.Redis] = None
orchestrator: Optional[AgentOrchestrator] = None
pipeline: Optional[NewPipelineOrchestrator] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global redis_client, orchestrator, pipeline
    
    # Startup
    logger.info("Starting Agent Orchestrator with NEW PIPELINE...")
    
    # Connect to Redis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url, decode_responses=True)
    
    # Initialize old orchestrator (for backward compatibility)
    orchestrator = AgentOrchestrator(redis_client)
    
    # Initialize NEW PIPELINE
    pipeline = create_pipeline_orchestrator(redis_client)
    
    logger.info("Agent Orchestrator with NEW PIPELINE started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agent Orchestrator...")
    if redis_client:
        await redis_client.close()


# Create FastAPI app
app = FastAPI(
    title="Instagram AI Agent Orchestrator",
    description="7-agent AI system for Instagram account analysis",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
_allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
_extra_origins = [o.strip() for o in _allowed_origins_env.split(",") if o.strip()]

ALLOWED_ORIGINS: list[str] = [
    # Cloudflare Tunnel public domain
    "https://coriumai-local.com",
    # Vercel production (all preview & custom domains)
    "https://*.vercel.app",
    # Local development
    "http://localhost:3000",
    "http://localhost:3001",
    # In-network frontend container
    "http://frontend:3000",
    *_extra_origins,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class AccountData(BaseModel):
    username: str
    followers: int
    following: int
    posts: int
    bio: Optional[str] = None
    verified: bool = False
    isPrivate: bool = False
    isBusiness: bool = False
    engagementRate: Optional[float] = 0.0
    avgLikes: Optional[float] = None  # NULL = veri çekilemedi (HAYALET VERİ durumu)
    avgComments: Optional[float] = None  # NULL = veri çekilemedi
    botScore: Optional[float] = 0.0
    isBot: bool = False
    suspiciousPatterns: List[str] = []
    niche: str = "General"
    recentPosts: List[Dict[str, Any]] = []
    rawData: Dict[str, Any] = {}


class OwnAccountCredentials(BaseModel):
    """Credentials for own account analysis"""
    username: str
    password: Optional[str] = None
    fetch_private: bool = False
    two_fa_code: Optional[str] = None


class CompetitorTarget(BaseModel):
    """Target for competitor analysis"""
    username: str


class DataAcquisitionRequest(BaseModel):
    """Request for Instagram data acquisition"""
    analysis_type: str  # "own_account" | "competitor"
    own_account: Optional[OwnAccountCredentials] = None
    competitor: Optional[CompetitorTarget] = None


class StartAnalysisRequest(BaseModel):
    analysisId: str
    accountData: AccountData
    agents: List[str]
    # Optional data acquisition request
    acquisition: Optional[DataAcquisitionRequest] = None
    # Direct own_account for authenticated mode (from backend)
    own_account: Optional[OwnAccountCredentials] = None
    # Analysis mode: 'public' or 'authenticated'
    mode: str = 'public'


class AnalysisProgress(BaseModel):
    analysisId: str
    status: str
    progress: int
    currentAgent: Optional[str] = None
    completedAgents: List[str] = []
    agentResults: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        await redis_client.ping()
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "redis": "connected",
                "gemini": "configured" if os.getenv("GEMINI_API_KEY") else "not configured",
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
        }


# Start analysis
@app.post("/analyze/start")
async def start_analysis(
    request: StartAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a new analysis with the specified agents.
    
    Optionally includes data acquisition request for Instagram scraping.
    """
    try:
        logger.info(f"Starting analysis {request.analysisId} for @{request.accountData.username}")
        
        # Prepare acquisition request if provided
        acquisition_request = None
        if request.acquisition:
            acquisition_request = request.acquisition.model_dump()
            logger.info(f"Data acquisition requested: {acquisition_request.get('analysis_type')}")
        
        # Store initial state in Redis
        await redis_client.hset(
            f"analysis:{request.analysisId}",
            mapping={
                "status": "PROCESSING",
                "progress": "0",
                "currentAgent": "instagramDataAcquisition" if acquisition_request else (request.agents[0] if request.agents else ""),
                "completedAgents": json.dumps([]),
                "startedAt": datetime.utcnow().isoformat(),
                "hasDataAcquisition": "true" if acquisition_request else "false",
            }
        )
        
        # Run analysis in background with acquisition request
        background_tasks.add_task(
            run_analysis,
            request.analysisId,
            request.accountData.model_dump(),
            request.agents,
            acquisition_request
        )
        
        return {
            "success": True,
            "analysisId": request.analysisId,
            "status": "PROCESSING",
            "message": "Analysis started",
            "hasDataAcquisition": acquisition_request is not None,
        }
    except Exception as e:
        logger.error(f"Failed to start analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =================================================================
# DATA ACQUISITION ENDPOINTS
# =================================================================

@app.post("/acquire/instagram")
async def acquire_instagram_data(request: DataAcquisitionRequest):
    """
    Standalone Instagram data acquisition.
    
    Use this endpoint to acquire data without running full analysis.
    Useful for:
    - Pre-fetching data before analysis
    - Competitor research
    - Data validation
    
    Modes:
    - own_account: Full access with login credentials (100% coverage)
    - competitor: Public data only via Apify (30% coverage)
    """
    try:
        logger.info(f"Data acquisition request: {request.analysis_type}")
        
        result = await orchestrator.acquire_instagram_data(request.model_dump())
        
        return {
            "success": result.get("success", False),
            "mode": result.get("mode"),
            "target": result.get("target_account"),
            "data": result.get("data"),
            "metadata": result.get("metadata"),
            "limitations": result.get("limitations"),
        }
        
    except Exception as e:
        logger.error(f"Data acquisition failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/acquire/availability")
async def get_data_availability():
    """
    Get data availability matrix for different analysis modes.
    
    Shows which data is available for each agent in:
    - full_access mode (own account with login)
    - public_only mode (competitor analysis)
    """
    return {
        "modes": {
            "full_access": {
                "description": "Kendi hesabınız (login ile)",
                "coverage": "100%",
                "sources": ["login_scrape", "apify"],
                "available_data": [
                    "reach", "impressions", "demographics", "saves",
                    "shares", "profile_visits", "follower_growth",
                    "story_insights", "website_clicks", "discovery_sources",
                    "posts", "likes", "comments", "follower_count",
                    "following_count", "bio", "post_captions", "hashtags"
                ],
                "agent_availability": orchestrator.agent_data_availability.get("full_access", {}),
            },
            "public_only": {
                "description": "Rakip analizi (sadece herkese açık veriler)",
                "coverage": "30%",
                "sources": ["apify"],
                "available_data": [
                    "posts", "likes", "comments", "follower_count",
                    "following_count", "bio", "post_frequency",
                    "post_captions", "hashtags", "engagement_rate_estimated"
                ],
                "unavailable_data": [
                    "reach", "impressions", "demographics", "saves",
                    "shares", "profile_visits", "follower_growth",
                    "story_insights", "website_clicks", "discovery_sources"
                ],
                "agent_availability": orchestrator.agent_data_availability.get("public_only", {}),
            },
        },
        "disclaimer": "public_only modunda özel metrikler tahmini değerlerdir ve %70 güven oranına sahiptir.",
    }


# Get analysis status
@app.get("/analyze/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Get the current status of an analysis"""
    try:
        data = await redis_client.hgetall(f"analysis:{analysis_id}")
        
        if not data:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {
            "analysisId": analysis_id,
            "status": data.get("status", "UNKNOWN"),
            "progress": int(data.get("progress", 0)),
            "currentAgent": data.get("currentAgent"),
            "completedAgents": json.loads(data.get("completedAgents", "[]")),
            "error": data.get("error"),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analysis status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =================================================================
# CONTENT PLAN GENERATION ENDPOINTS
# =================================================================

class ContentPlanRequest(BaseModel):
    """Request model for content plan generation"""
    analysisId: str
    accountData: Optional[AccountData] = None
    useExistingResults: bool = True


class ContentPlanFromAnalysisRequest(BaseModel):
    """Request to generate content plan from existing analysis"""
    analysisId: str


@app.post("/content-plan/generate")
async def generate_content_plan(request: ContentPlanRequest):
    """
    Generate a 7-day content plan from analysis results.
    
    If useExistingResults is True, will use cached analysis results.
    Otherwise, will run a fresh analysis first.
    """
    try:
        logger.info(f"Content plan request for analysis {request.analysisId}")
        
        agent_results = None
        account_data = None
        
        # Try to get existing results
        if request.useExistingResults:
            results_key = f"analysis:{request.analysisId}:results"
            cached_results = await redis_client.get(results_key)
            
            if cached_results:
                full_results = json.loads(cached_results)
                # Extract agentResults from full results
                if "agentResults" in full_results:
                    agent_results = full_results["agentResults"]
                elif "agent_details" in full_results:
                    agent_results = full_results["agent_details"]
                else:
                    agent_results = full_results
                logger.info(f"Using cached results for analysis {request.analysisId}")
            
            # Get account data from Redis if available
            account_data_key = f"analysis:{request.analysisId}:accountData"
            cached_account = await redis_client.get(account_data_key)
            if cached_account:
                account_data = json.loads(cached_account)
        
        # Use provided account data if no cached data
        if account_data is None and request.accountData:
            account_data = request.accountData.model_dump()
        
        if account_data is None:
            raise HTTPException(
                status_code=400,
                detail="No account data available. Provide accountData or use an existing analysis."
            )
        
        # Generate content plan
        content_plan = await orchestrator.generate_content_plan(
            account_data=account_data,
            agent_results=agent_results,
            run_analysis_if_needed=not request.useExistingResults
        )
        
        if content_plan.get("error"):
            raise HTTPException(status_code=400, detail=content_plan)
        
        # Cache the content plan
        await redis_client.set(
            f"analysis:{request.analysisId}:contentPlan",
            json.dumps(content_plan),
            ex=86400 * 7  # 7 days TTL
        )
        
        return {
            "success": True,
            "analysisId": request.analysisId,
            "contentPlan": content_plan
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate content plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/content-plan/from-analysis/{analysis_id}")
async def generate_content_plan_from_analysis(analysis_id: str):
    """
    Generate a 7-day content plan from a completed analysis.
    Uses only the existing analysis results - no new API calls for analysis.
    """
    try:
        logger.info(f"Generating content plan from analysis {analysis_id}")
        
        # Check analysis status
        status_data = await redis_client.hgetall(f"analysis:{analysis_id}")
        
        if not status_data:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        if status_data.get("status") != "COMPLETED":
            raise HTTPException(
                status_code=400,
                detail=f"Analysis must be completed first. Current status: {status_data.get('status', 'UNKNOWN')}"
            )
        
        # Get analysis results
        results_key = f"analysis:{analysis_id}:results"
        cached_results = await redis_client.get(results_key)
        
        if not cached_results:
            raise HTTPException(
                status_code=404,
                detail="Analysis results not found. They may have expired."
            )
        
        full_results = json.loads(cached_results)
        
        # Extract agentResults from full results
        # New pipeline stores results as: {finalScore, agentResults, eli5Report, ...}
        if "agentResults" in full_results:
            agent_results = full_results["agentResults"]
        elif "agent_details" in full_results:
            # Old pipeline format
            agent_results = full_results["agent_details"]
        else:
            # Assume full_results is already agent_results (legacy format)
            agent_results = full_results
        
        logger.info(f"Content plan: Extracted agent results with keys: {list(agent_results.keys())}")
        
        # Get account data
        account_data_key = f"analysis:{analysis_id}:accountData"
        cached_account = await redis_client.get(account_data_key)
        
        if not cached_account:
            # Try to extract from agent results
            account_data = {
                "username": agent_results.get("contentStrategist", {}).get("account_profile", {}).get("username", "unknown"),
                "followers": agent_results.get("audienceDynamics", {}).get("audience_profile", {}).get("total_followers", 0),
                "following": 0,
                "posts": 0,
                "niche": agent_results.get("domainMaster", {}).get("niche_identification", {}).get("primary_niche", "General"),
                "analysisId": analysis_id
            }
        else:
            account_data = json.loads(cached_account)
        
        account_data["analysisId"] = analysis_id
        
        # Generate content plan
        content_plan = await orchestrator.generate_content_plan(
            account_data=account_data,
            agent_results=agent_results,
            run_analysis_if_needed=False
        )
        
        if content_plan.get("error"):
            return {
                "success": False,
                "analysisId": analysis_id,
                "error": content_plan.get("error"),
                "validation": content_plan.get("validation"),
                "recommendation": content_plan.get("recommendation")
            }
        
        # Cache the content plan
        await redis_client.set(
            f"analysis:{analysis_id}:contentPlan",
            json.dumps(content_plan),
            ex=86400 * 7  # 7 days TTL
        )
        
        return {
            "success": True,
            "analysisId": analysis_id,
            "contentPlan": content_plan,
            "metadata": {
                "generatedAt": datetime.utcnow().isoformat(),
                "dataSource": "cached_analysis"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate content plan from analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/content-plan/{analysis_id}")
async def get_content_plan(analysis_id: str):
    """Get a previously generated content plan"""
    try:
        content_plan_key = f"analysis:{analysis_id}:contentPlan"
        cached_plan = await redis_client.get(content_plan_key)
        
        if not cached_plan:
            raise HTTPException(
                status_code=404,
                detail="Content plan not found. Generate one first using /content-plan/from-analysis/{analysis_id}"
            )
        
        return {
            "success": True,
            "analysisId": analysis_id,
            "contentPlan": json.loads(cached_plan)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get content plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/content-plan/{analysis_id}")
async def delete_content_plan(analysis_id: str):
    """Delete a generated content plan"""
    try:
        content_plan_key = f"analysis:{analysis_id}:contentPlan"
        deleted = await redis_client.delete(content_plan_key)
        
        return {
            "success": deleted > 0,
            "message": "Content plan deleted" if deleted > 0 else "Content plan not found"
        }
        
    except Exception as e:
        logger.error(f"Failed to delete content plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/content-plan/validate-data/{analysis_id}")
async def validate_content_plan_data(analysis_id: str):
    """
    Validate if an analysis has sufficient data for content plan generation.
    Returns validation status and missing fields.
    """
    try:
        # Get analysis results
        results_key = f"analysis:{analysis_id}:results"
        cached_results = await redis_client.get(results_key)
        
        if not cached_results:
            raise HTTPException(
                status_code=404,
                detail="Analysis results not found"
            )
        
        full_results = json.loads(cached_results)
        
        # Extract agentResults from full results
        if "agentResults" in full_results:
            agent_results = full_results["agentResults"]
        elif "agent_details" in full_results:
            agent_results = full_results["agent_details"]
        else:
            agent_results = full_results
        
        # Use the content plan generator's validation
        validation = orchestrator.content_plan_generator.validate_required_data(agent_results)
        
        return {
            "analysisId": analysis_id,
            "validation": validation,
            "canGeneratePlan": validation.get("can_generate", False)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to validate content plan data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =================================================================
# END CONTENT PLAN GENERATION ENDPOINTS
# =================================================================


# Get analysis result
@app.get("/analyze/result/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    """Get the full results of a completed analysis"""
    try:
        data = await redis_client.hgetall(f"analysis:{analysis_id}")
        
        if not data:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        if data.get("status") != "COMPLETED":
            raise HTTPException(
                status_code=400, 
                detail=f"Analysis is {data.get('status', 'UNKNOWN').lower()}"
            )
        
        results_key = f"analysis:{analysis_id}:results"
        results = await redis_client.get(results_key)
        
        return {
            "analysisId": analysis_id,
            "status": "COMPLETED",
            "agentResults": json.loads(results) if results else {},
            "completedAt": data.get("completedAt"),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analysis result: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Cancel analysis
@app.post("/analyze/cancel/{analysis_id}")
async def cancel_analysis(analysis_id: str):
    """Cancel a running analysis"""
    try:
        # Update status in Redis
        await redis_client.hset(
            f"analysis:{analysis_id}",
            mapping={
                "status": "CANCELLED",
                "cancelledAt": datetime.utcnow().isoformat(),
            }
        )
        
        return {
            "success": True,
            "message": "Analysis cancellation requested",
        }
    except Exception as e:
        logger.error(f"Failed to cancel analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Background task to run analysis with NEW PIPELINE
async def run_analysis(
    analysis_id: str,
    account_data: Dict[str, Any],
    agents: List[str],
    acquisition_request: Optional[Dict[str, Any]] = None
):
    """
    Run the full analysis pipeline with NEW PIPELINE ARCHITECTURE.
    
    AKIŞ:
    1. Data Acquisition (Apify Scrape)
    2. Delta Sync (PostgreSQL'den önceki rapor)
    3. STAGE 1: Domain Master (sektör benchmarkları)
    4. STAGE 2: PhD Agent Team (parallel)
    5. STAGE 3: Governor Audit (veto gate)
    6. STAGE 4: ELI5 & Hook Audit
    7. FINAL: Store results
    """
    try:
        logger.info(f"=" * 60)
        logger.info(f"NEW PIPELINE: Starting analysis {analysis_id}")
        logger.info(f"=" * 60)
        
        # Store account data for later content plan generation
        await redis_client.set(
            f"analysis:{analysis_id}:accountData",
            json.dumps(account_data),
            ex=86400 * 7  # 7 days TTL
        )
        
        # Webhook URL for backend updates
        webhook_url = os.getenv("BACKEND_WEBHOOK_URL", "http://localhost:3001/api/webhooks/analysis-update")
        
        # ===========================================================
        # PHASE 0: DATA ACQUISITION (Apify Scrape)
        # ===========================================================
        enriched_account_data = account_data
        acquisition_result = None
        data_mode = None
        
        if acquisition_request:
            logger.info(f"PHASE 0: Data Acquisition for {analysis_id}")
            
            await redis_client.hset(
                f"analysis:{analysis_id}",
                mapping={
                    "currentAgent": "instagramDataAcquisition",
                    "progress": "5",
                    "stage": "DATA_ACQUISITION",
                }
            )
            
            await send_webhook_update(webhook_url, {
                "analysisId": analysis_id,
                "status": "PROCESSING",
                "progress": 5,
                "stage": "DATA_ACQUISITION",
                "currentAgent": "instagramDataAcquisition",
                "message": "Instagram veri toplama başlatıldı",
            })
            
            try:
                acquisition_result = await orchestrator.acquire_instagram_data(acquisition_request)
                
                if acquisition_result.get("success"):
                    enriched_account_data = orchestrator.enrich_account_data_with_acquisition(
                        account_data,
                        acquisition_result
                    )
                    data_mode = acquisition_result.get("mode")
                    
                    # Store enriched data
                    await redis_client.set(
                        f"analysis:{analysis_id}:accountData",
                        json.dumps(enriched_account_data),
                        ex=86400 * 7
                    )
                    
                    logger.info(f"Data acquisition completed, mode: {data_mode}")
                else:
                    logger.warning(f"Data acquisition failed: {acquisition_result.get('error')}")
            except Exception as acq_error:
                logger.error(f"Data acquisition error: {acq_error}")
        
        # ===========================================================
        # DELTA SYNC: Get Previous Analysis from PostgreSQL (via Backend)
        # ===========================================================
        previous_analysis = None
        
        await redis_client.hset(
            f"analysis:{analysis_id}",
            mapping={
                "stage": "DELTA_SYNC",
                "progress": "8",
            }
        )
        
        await send_webhook_update(webhook_url, {
            "analysisId": analysis_id,
            "status": "PROCESSING",
            "progress": 8,
            "stage": "DELTA_SYNC",
            "message": "Önceki analiz verileri kontrol ediliyor...",
        })
        
        try:
            # Try to fetch previous analysis from backend
            username = enriched_account_data.get("username", "")
            if username:
                async with httpx.AsyncClient() as client:
                    backend_url = os.getenv("BACKEND_URL", "http://backend-api:3001")
                    response = await client.get(
                        f"{backend_url}/api/analyze/previous/{username}",
                        timeout=10.0
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success") and data.get("analysis"):
                            previous_analysis = data["analysis"]
                            logger.info(f"Found previous analysis from {previous_analysis.get('analysisCompletedAt', 'unknown')}")
                    else:
                        logger.info(f"No previous analysis found for {username}")
        except Exception as delta_error:
            logger.warning(f"Delta sync failed: {delta_error}")
        
        # ===========================================================
        # RUN NEW PIPELINE (Stages 1-4)
        # ===========================================================
        logger.info("Starting NEW PIPELINE analysis...")
        
        async def progress_callback(progress_data: Dict[str, Any]):
            """Callback for pipeline progress updates"""
            # Filter out None values for Redis (Redis doesn't accept None)
            redis_mapping = {
                "stage": str(progress_data.get("stage") or "PROCESSING"),
                "progress": str(progress_data.get("progress") or 0),
                "currentAgent": str(progress_data.get("currentAgent") or ""),
            }
            
            await redis_client.hset(
                f"analysis:{analysis_id}",
                mapping=redis_mapping
            )
            
            # Also filter None for webhook
            webhook_data = {
                "analysisId": analysis_id,
                "status": "PROCESSING",
            }
            for key, value in progress_data.items():
                if value is not None:
                    webhook_data[key] = value
            
            await send_webhook_update(webhook_url, webhook_data)
        
        # Run the new pipeline
        results = await pipeline.run_full_analysis(
            account_data=enriched_account_data,
            previous_analysis=previous_analysis,
            progress_callback=progress_callback,
        )
        
        # Add acquisition metadata to results
        if acquisition_result:
            results["_dataAcquisition"] = {
                "mode": acquisition_result.get("mode"),
                "coverage": acquisition_result.get("metadata", {}).get("data_coverage"),
                "sources": acquisition_result.get("metadata", {}).get("sources_used", []),
                "limitations": acquisition_result.get("limitations"),
            }
        
        # ===========================================================
        # FINAL: Store Results and Complete
        # ===========================================================
        
        # Check for errors
        if results.get("error"):
            raise Exception(results.get("error"))
        
        # Get final score and grade
        final_score = results.get("finalScore", 0)
        final_grade = results.get("finalGrade", "F")
        
        logger.info(f"Analysis completed: Score={final_score}, Grade={final_grade}")
        
        # Analysis complete
        await redis_client.hset(
            f"analysis:{analysis_id}",
            mapping={
                "status": "COMPLETED",
                "progress": "100",
                "stage": "COMPLETED",
                "currentAgent": "",
                "completedAt": datetime.utcnow().isoformat(),
                "finalScore": str(final_score),
                "finalGrade": final_grade,
            }
        )
        
        # Store full results
        await redis_client.set(
            f"analysis:{analysis_id}:results",
            json.dumps(results),
            ex=86400 * 7  # 7 days TTL
        )
        
        # Send final update
        await send_webhook_update(webhook_url, {
            "analysisId": analysis_id,
            "status": "COMPLETED",
            "progress": 100,
            "stage": "COMPLETED",
            "finalScore": final_score,
            "finalGrade": final_grade,
            "agentResults": results.get("agentResults", {}),
            "eli5Report": results.get("eli5Report", {}),
        })
        
        logger.info(f"=" * 60)
        logger.info(f"NEW PIPELINE: Analysis {analysis_id} completed successfully")
        logger.info(f"Final Score: {final_score}, Grade: {final_grade}")
        logger.info(f"=" * 60)
        
    except Exception as e:
        logger.error(f"Analysis {analysis_id} failed: {e}")
        
        # Update status to failed
        await redis_client.hset(
            f"analysis:{analysis_id}",
            mapping={
                "status": "FAILED",
                "error": str(e),
            }
        )
        
        # Send failure update
        webhook_url = os.getenv("BACKEND_WEBHOOK_URL", "http://localhost:3001/api/webhooks/analysis-update")
        await send_webhook_update(webhook_url, {
            "analysisId": analysis_id,
            "status": "FAILED",
            "error": str(e),
        })


async def send_webhook_update(url: str, data: Dict[str, Any]):
    """Send update to backend webhook"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=data,
                timeout=10.0
            )
            if response.status_code != 200:
                logger.warning(f"Webhook returned {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to send webhook update: {e}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=os.getenv("NODE_ENV") == "development"
    )
