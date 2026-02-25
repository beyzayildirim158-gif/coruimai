# Agent Orchestrator - PhD Level Implementation
# Central Controller for Multi-Agent Instagram Analysis System
"""
Agent Orchestrator - PhD Level

Bu modül multi-agent sistemin merkezi kontrolcüsüdür. Agent başlatma,
yürütme sıralaması, veri dağıtımı, sonuç toplama, hata yönetimi,
doğrulama koordinasyonu ve final rapor üretimini yönetir.

Now includes Content Plan Generator for 7-day dynamic content planning.
"""

import asyncio
import gc
import json
import logging
import os
import statistics
import time
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from google import genai
from google.genai import types

from .audience_dynamics import AudienceDynamicsAgent
from .attention_architect import AttentionArchitectAgent
from .base_agent import BaseAgent
from .community_loyalty import CommunityLoyaltyAgent
from .content_plan_generator import ContentPlanGenerator
from .content_strategist import ContentStrategistAgent
from .domain_master import DomainMasterAgent
from .growth_virality import GrowthViralityAgent
from .metric_sanity_gates import MetricSanityGates, get_sanity_gates
from .sales_conversion import SalesConversionAgent
from .system_governor import SystemGovernorAgent
from .visual_brand import VisualBrandAgent
from .instagram_scraper import (
    InstagramDataAcquisitionAgent,
    AnalysisMode,
    adjust_analysis_depth,
    create_agent_data_package,
)
from .advanced_analysis_engine import AdvancedAnalysisEngine, run_advanced_analysis

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Performance metrics collector"""

    def __init__(self):
        self.metrics: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def record(self, metric_name: str, value: float, tags: Optional[Dict[str, Any]] = None) -> None:
        """Record a metric value"""
        self.metrics[metric_name].append({
            "value": value,
            "timestamp": time.time(),
            "tags": tags or {},
        })

    def get_summary(self, metric_name: str) -> Dict[str, Any]:
        """Get statistical summary of a metric"""
        values = [m["value"] for m in self.metrics[metric_name]]
        if not values:
            return {"count": 0, "mean": 0, "median": 0, "min": 0, "max": 0}
        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
        }

    def clear(self) -> None:
        """Clear all metrics"""
        self.metrics.clear()


class RateLimiter:
    """Token bucket rate limiter for API calls - Gemini optimized"""

    def __init__(self, rpm: int = 15):
        """Initialize with conservative RPM (Gemini free tier: 15 RPM)"""
        self.rpm = rpm
        self.tokens = float(rpm)
        self.last_update = time.time()
        self.min_interval = 60.0 / rpm  # Minimum seconds between requests
        self.last_request = 0

    async def acquire(self) -> None:
        """Acquire a token, waiting if necessary with minimum interval enforcement"""
        # Enforce minimum interval between requests
        now = time.time()
        time_since_last = now - self.last_request
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            await asyncio.sleep(wait_time)
        
        # Token bucket logic
        while self.tokens < 1:
            await asyncio.sleep(0.5)
            self._refill()
        
        self.tokens -= 1
        self.last_request = time.time()

    def _refill(self) -> None:
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.rpm, self.tokens + elapsed * (self.rpm / 60))
        self.last_update = now


class CacheManager:
    """Multi-layer cache manager"""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.local_cache: Dict[str, Any] = {}

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache (local first, then Redis)"""
        if key in self.local_cache:
            return self.local_cache[key]
        if self.redis:
            try:
                cached = await self.redis.get(key)
                if cached:
                    return json.loads(cached)
            except Exception:
                pass
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache"""
        self.local_cache[key] = value
        if self.redis:
            try:
                await self.redis.setex(key, ttl, json.dumps(value))
            except Exception:
                pass

    async def get_or_compute(
        self,
        key: str,
        compute_fn,
        ttl: int = 3600,
    ) -> Any:
        """Get from cache or compute and cache"""
        cached = await self.get(key)
        if cached is not None:
            return cached
        result = await compute_fn()
        await self.set(key, result, ttl)
        return result

    def clear_local(self) -> None:
        """Clear local cache"""
        self.local_cache.clear()


class AgentOrchestrator:
    """
    Agent Orchestrator - PhD Level

    Central controller for multi-agent Instagram analysis system.

    Responsibilities:
    - Agent initialization
    - Execution sequencing (parallel/sequential/dependency-aware)
    - Data distribution to agents
    - Result aggregation
    - Error handling with graceful degradation
    - Validation coordination
    - Final report generation

    Agent Roles:
    1. Content Strategist: İçerik analizi, algoritma uyumu
    2. Audience Dynamics: Kitle analizi, demografik
    3. Engagement Optimizer (Attention Architect): Etkileşim optimizasyonu
    4. Visual Brand: Görsel kimlik analizi
    5. Growth Architect (Growth Virality): Büyüme stratejisi
    6. Domain Master: Niche uzmanlığı
    7. Community Loyalty: Topluluk ve sadakat
    8. Sales Conversion: Satış ve monetizasyon
    9. System Governor: Doğrulama, bot tespiti
    
    Data Acquisition Layer:
    - Instagram Data Acquisition Agent: Veri toplama (Login Scrape + Apify)
    """

    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.analysis_id = str(uuid.uuid4())

        # Initialize infrastructure
        self._init_gemini()
        self._init_agents()
        self._init_data_acquisition()
        self._init_execution_config()
        self._init_aggregation_config()
        self._init_error_handling()
        self._init_quality_assurance()

        # Support systems
        self.metrics_collector = MetricsCollector()
        self.rate_limiter = RateLimiter(rpm=60)
        self.cache_manager = CacheManager(redis_client)
        
        # Metric Sanity Gates - Post-processing for consistency
        self.sanity_gates = get_sanity_gates()

    # ---------------------- Initialization ----------------------
    def _init_gemini(self) -> None:
        """Initialize Gemini API with new google.genai SDK"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        
        # Create client with new SDK
        self.gemini_client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
        # Generation config for consistent, high-quality outputs
        self.generation_config = types.GenerateContentConfig(
            temperature=0.7,  # Balanced creativity/consistency
            top_p=0.9,
            top_k=40,
            max_output_tokens=8192,  # Allow detailed responses
            response_mime_type="application/json",  # Force JSON output
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_NONE"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_NONE"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_NONE"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_NONE"
                ),
            ]
        )

    def _init_data_acquisition(self) -> None:
        """Initialize Instagram Data Acquisition Agent"""
        self.data_acquisition_agent = InstagramDataAcquisitionAgent()
        
        # Data availability tracking
        self.data_mode: Optional[str] = None
        self.data_limitations: Optional[Dict[str, Any]] = None
        
        # Agent data availability matrix
        self.agent_data_availability = {
            # Full Access Mode (own account with login)
            AnalysisMode.FULL_ACCESS.value: {
                "contentStrategist": "full",
                "audienceDynamics": "full",
                "attentionArchitect": "full",
                "visualBrand": "full",
                "growthVirality": "full",
                "domainMaster": "full",
                "communityLoyalty": "full",
                "salesConversion": "full",
                "systemGovernor": "full",
            },
            # Public Only Mode (competitor analysis)
            AnalysisMode.PUBLIC_ONLY.value: {
                "contentStrategist": "limited",
                "audienceDynamics": "estimated",
                "attentionArchitect": "limited",
                "visualBrand": "full",
                "growthVirality": "limited",
                "domainMaster": "full",
                "communityLoyalty": "limited",
                "salesConversion": "limited",
                "systemGovernor": "limited",
            },
        }

    def _init_agents(self) -> None:
        """Initialize all agents including Content Plan Generator with new SDK"""
        self.agents: Dict[str, BaseAgent] = {
            "contentStrategist": ContentStrategistAgent(self.gemini_client, self.generation_config, self.model_name),
            "audienceDynamics": AudienceDynamicsAgent(self.gemini_client, self.generation_config, self.model_name),
            "visualBrand": VisualBrandAgent(self.gemini_client, self.generation_config, self.model_name),
            "attentionArchitect": AttentionArchitectAgent(self.gemini_client, self.generation_config, self.model_name),
            "growthVirality": GrowthViralityAgent(self.gemini_client, self.generation_config, self.model_name),
            "domainMaster": DomainMasterAgent(self.gemini_client, self.generation_config, self.model_name),
            "communityLoyalty": CommunityLoyaltyAgent(self.gemini_client, self.generation_config, self.model_name),
            "salesConversion": SalesConversionAgent(self.gemini_client, self.generation_config, self.model_name),
            "systemGovernor": SystemGovernorAgent(self.gemini_client, self.generation_config, self.model_name),
        }
        
        # Content Plan Generator - separate from main analysis flow
        self.content_plan_generator = ContentPlanGenerator(self.gemini_client, self.generation_config, self.model_name)

        # Agent dependency graph (Data Acquisition runs first, before all)
        self.dependency_graph = {
            # Level -1 - Data Acquisition (runs first)
            "level_data": ["instagramDataAcquisition"],
            # Level 0 - No dependencies (can run in parallel)
            # DomainMaster Level 0'da çünkü niş bilgisi tüm ajanlar için kritik
            "level_0": ["contentStrategist", "audienceDynamics", "visualBrand", "domainMaster"],
            # Level 1 - Depends on Level 0 (niş bilgisi ve kitle bilgisi kullanır)
            "level_1": ["attentionArchitect", "growthVirality", "communityLoyalty", "salesConversion"],
            # Level 2 - Depends on all (validation)
            "level_2": ["systemGovernor"],
            # Level 3 - Content Plan (depends on all agents, optional)
            "level_3": ["contentPlanGenerator"],
        }

        # Data requirements per agent
        self.agent_data_requirements = {
            "contentStrategist": ["posts", "recentPosts", "contentTypes", "hashtagUsage", "engagementRate"],
            "audienceDynamics": ["followers", "audienceDemographics", "topLocations", "activeHours"],
            "visualBrand": ["recentPosts", "bio", "profilePicture"],
            "attentionArchitect": ["engagementRate", "avgLikes", "avgComments", "recentPosts"],
            "growthVirality": ["followers", "growthRate", "following", "engagementRate"],
            "domainMaster": ["category", "bio", "hashtagUsage", "contentTypes"],
            "communityLoyalty": ["followers", "engagementRate", "avgComments", "recentPosts"],
            "salesConversion": ["followers", "engagementRate", "category", "isBusiness"],
            "systemGovernor": ["ALL"],  # Needs everything + agent results
            "contentPlanGenerator": ["ALL_AGENT_RESULTS"],  # Needs all agent outputs
        }

    def _init_execution_config(self) -> None:
        """Initialize execution configuration"""
        self.execution_config = {
            "strategy": "sequential",  # sequential to avoid rate limits, was: dependency_aware
            "max_concurrent": 2,  # Reduced from 5 to avoid rate limits
            "timeouts": {
                "single_agent": 120,  # Increased for retries
                "all_agents": 600,  # 10 minutes for all agents
                "validation": 60,
                "report_generation": 30,
                "total_analysis": 900,  # 15 minutes total
            },
            "retry": {
                "max_retries": 5,
                "backoff_base": 5,  # seconds - increased from 1
                "backoff_multiplier": 3,  # More aggressive backoff
            },
            "agent_delay": 5,  # Seconds to wait between agents
        }

        # Semaphore for concurrent API calls
        self.semaphore = asyncio.Semaphore(self.execution_config["max_concurrent"])

    def _init_aggregation_config(self) -> None:
        """Initialize result aggregation configuration"""
        # Agent weights for composite score
        self.agent_weights = {
            "contentStrategist": 0.14,
            "audienceDynamics": 0.12,
            "attentionArchitect": 0.14,
            "visualBrand": 0.10,
            "growthVirality": 0.12,
            "domainMaster": 0.08,
            "communityLoyalty": 0.10,
            "salesConversion": 0.10,
            "systemGovernor": 0.10,
        }

        # Validation multipliers
        self.validation_multipliers = {
            "high_confidence": 1.0,  # >0.85
            "medium_confidence": 0.95,  # 0.70-0.85
            "low_confidence": 0.90,  # <0.70
            "critical_issues": 0.85,
        }

        # Health grade mapping
        self.health_grades = {
            "A": (90, 100),
            "B": (80, 89),
            "C": (70, 79),
            "D": (60, 69),
            "F": (0, 59),
        }

        # Finding categories
        self.finding_categories = [
            "Content & Strategy",
            "Audience & Growth",
            "Engagement & Community",
            "Visual & Brand",
            "Technical & Compliance",
            "Monetization & Business",
        ]

        # Recommendation priority weights
        self.recommendation_weights = {
            "impact": 0.30,
            "ease": 0.25,
            "time_to_result": 0.20,
            "resource_requirement": 0.15,
            "confidence": 0.10,
        }

    def _init_error_handling(self) -> None:
        """Initialize error handling configuration"""
        self.error_types = {
            "AGENT_ERROR": {"severity": "medium", "recovery": "use_defaults"},
            "DATA_ERROR": {"severity": "high", "recovery": "request_new_data"},
            "TIMEOUT_ERROR": {"severity": "medium", "recovery": "retry_or_skip"},
            "VALIDATION_ERROR": {"severity": "high", "recovery": "rerun_or_flag"},
            "SYSTEM_ERROR": {"severity": "critical", "recovery": "retry_entire"},
        }

        self.circuit_breaker = {
            "failure_threshold": 5,
            "reset_timeout": 30,
            "half_open_requests": 3,
            "state": "closed",
            "failures": 0,
            "last_failure": None,
        }

    def _init_quality_assurance(self) -> None:
        """Initialize QA configuration"""
        self.qa_weights = {
            "completeness": 0.30,
            "consistency": 0.30,
            "quality": 0.25,
            "format": 0.15,
        }

        self.qa_thresholds = {
            "release_ready": (90, 100),
            "minor_fixes": (75, 89),
            "review_required": (60, 74),
            "regenerate": (0, 59),
        }

    # ---------------------- Agent Execution ----------------------
    async def run_agent(
        self,
        agent_name: str,
        account_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run a single agent with error handling"""
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_name}")

        start_time = time.time()

        try:
            logger.info(f"Running agent: {agent_name}")
            result = await agent.analyze(account_data)
            duration_ms = (time.time() - start_time) * 1000

            self.metrics_collector.record(
                "agent_duration_ms",
                duration_ms,
                tags={"agent": agent_name, "success": True},
            )

            logger.info(f"Agent {agent_name} completed in {duration_ms:.0f}ms")
            return result

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(f"Agent {agent_name} failed after {duration_ms:.0f}ms: {e}")

            self.metrics_collector.record(
                "agent_duration_ms",
                duration_ms,
                tags={"agent": agent_name, "success": False, "error": str(e)},
            )

            return self._get_default_result(agent_name, str(e))

    async def run_agent_safe(
        self,
        agent_name: str,
        account_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run agent with timeout and retry"""
        timeout = self.execution_config["timeouts"]["single_agent"]
        retry_config = self.execution_config["retry"]

        for attempt in range(retry_config["max_retries"]):
            try:
                async with self.semaphore:
                    await self.rate_limiter.acquire()
                    result = await asyncio.wait_for(
                        self.run_agent(agent_name, account_data),
                        timeout=timeout,
                    )
                    return result

            except asyncio.TimeoutError:
                logger.warning(f"Agent {agent_name} timed out (attempt {attempt + 1})")
                if attempt < retry_config["max_retries"] - 1:
                    backoff = retry_config["backoff_base"] * (retry_config["backoff_multiplier"] ** attempt)
                    await asyncio.sleep(backoff)
                else:
                    return self._get_default_result(agent_name, "Timeout")

            except Exception as e:
                logger.error(f"Agent {agent_name} error (attempt {attempt + 1}): {e}")
                if attempt < retry_config["max_retries"] - 1:
                    backoff = retry_config["backoff_base"] * (retry_config["backoff_multiplier"] ** attempt)
                    await asyncio.sleep(backoff)
                else:
                    return self._get_default_result(agent_name, str(e))

        return self._get_default_result(agent_name, "Max retries exceeded")

    def _get_default_result(self, agent_name: str, error: str) -> Dict[str, Any]:
        """Get default result when agent fails"""
        return {
            "agent": agent_name,
            "status": "error",
            "error": error,
            "score": 50,  # Neutral score
            "findings": [
                f"{agent_name} analizi mevcut değil",
                "Tahmini değerler kullanılıyor",
            ],
            "recommendations": [
                "Tam sonuçlar için analizi tekrar çalıştırın",
            ],
            "metrics": {},
            "confidence": 0.30,
            "error_flag": True,
        }

    # ---------------------- Execution Strategies ----------------------
    async def run_sequential(
        self,
        account_data: Dict[str, Any],
        agent_names: List[str],
    ) -> Dict[str, Any]:
        """Run agents sequentially with delay between each to avoid rate limits"""
        results = {}
        agent_delay = self.execution_config.get("agent_delay", 5)
        
        for i, agent_name in enumerate(agent_names):
            # Add delay between agents (not before first)
            if i > 0:
                logger.info(f"Waiting {agent_delay}s before next agent to avoid rate limits...")
                await asyncio.sleep(agent_delay)
            
            result = await self.run_agent_safe(agent_name, account_data)
            results[agent_name] = result
        return results

    async def run_parallel(
        self,
        account_data: Dict[str, Any],
        agent_names: List[str],
    ) -> Dict[str, Any]:
        """Run agents in parallel"""
        tasks = [
            self.run_agent_safe(agent_name, account_data)
            for agent_name in agent_names
        ]
        results_list = await asyncio.gather(*tasks, return_exceptions=True)

        results = {}
        for agent_name, result in zip(agent_names, results_list):
            if isinstance(result, Exception):
                results[agent_name] = self._get_default_result(agent_name, str(result))
            else:
                results[agent_name] = result

        return results

    async def run_dependency_aware(
        self,
        account_data: Dict[str, Any],
        agent_names: List[str],
    ) -> Dict[str, Any]:
        """Run agents respecting dependency levels with cross-agent data sharing"""
        results = {}

        # Filter requested agents by level
        level_0_agents = [a for a in self.dependency_graph["level_0"] if a in agent_names]
        level_1_agents = [a for a in self.dependency_graph["level_1"] if a in agent_names]
        level_2_agents = [a for a in self.dependency_graph["level_2"] if a in agent_names]

        # Level 0 - Parallel (no dependencies)
        if level_0_agents:
            logger.info(f"Running Level 0 agents: {level_0_agents}")
            level_0_results = await self.run_parallel(account_data, level_0_agents)
            results.update(level_0_results)

        # Level 1 - Parallel (depends on Level 0)
        # Enrich account_data with Level 0 results for cross-agent insights
        if level_1_agents:
            logger.info(f"Running Level 1 agents: {level_1_agents}")
            enriched_data = self._enrich_with_level0_results(account_data, results)
            level_1_results = await self.run_parallel(enriched_data, level_1_agents)
            results.update(level_1_results)

        # Level 2 - Sequential (depends on all - validation)
        # Pass all previous results for comprehensive validation
        if level_2_agents:
            logger.info(f"Running Level 2 agents: {level_2_agents}")
            # System Governor needs all previous agent results for validation
            validation_data = self._prepare_validation_data(account_data, results)
            level_2_results = await self.run_sequential(validation_data, level_2_agents)
            results.update(level_2_results)

        return results

    def _enrich_with_level0_results(
        self,
        account_data: Dict[str, Any],
        level0_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Enrich account data with Level 0 agent insights for Level 1 agents.
        This enables cross-agent data sharing for richer analysis.
        """
        enriched = account_data.copy()
        
        # Add cross-agent insights section
        enriched["crossAgentInsights"] = {}
        
        # Extract key insights from Content Strategist
        if "contentStrategist" in level0_results:
            cs_result = level0_results["contentStrategist"]
            enriched["crossAgentInsights"]["contentStrategist"] = {
                "contentEffectivenessScore": self._safe_extract(cs_result, "metrics.contentEffectivenessScore", 0),
                "hashtagEffectiveness": self._safe_extract(cs_result, "metrics.hashtagEffectiveness", 0),
                "captionQuality": self._safe_extract(cs_result, "metrics.captionQuality", 0),
                "postingConsistency": self._safe_extract(cs_result, "metrics.postingConsistency", "medium"),
                "algorithmAlignment": self._safe_extract(cs_result, "metrics.algorithmAlignmentScore", 0),
                "contentPillars": self._safe_extract(cs_result, "detailed_scores.content_diversity.topic_variety.pillars_identified", []),
                "hookAnalysis": self._safe_extract(cs_result, "hookAnalysis", {}),
                "hashtagAnalysis": self._safe_extract(cs_result, "hashtagAnalysis", {}),
            }
        
        # Extract key insights from Audience Dynamics
        if "audienceDynamics" in level0_results:
            ad_result = level0_results["audienceDynamics"]
            enriched["crossAgentInsights"]["audienceDynamics"] = {
                "audienceQuality": self._safe_extract(ad_result, "metrics.audienceQuality", 0),
                "demographicFit": self._safe_extract(ad_result, "metrics.demographicFit", 0),
                "engagementPotential": self._safe_extract(ad_result, "metrics.engagementPotential", 0),
                "followerSegmentation": self._safe_extract(ad_result, "followerSegmentation", {}),
                "botDetectionScore": self._safe_extract(ad_result, "botDetectionScore", {}),
                "topPersonas": self._safe_extract(ad_result, "personas", [])[:3],
                "audienceSize": self._safe_extract(ad_result, "audience_profile.total_followers", 0),
                "audienceGrowthTrend": self._safe_extract(ad_result, "audience_analysis.growth_trend", "stable"),
            }
        
        # Extract key insights from Visual Brand
        if "visualBrand" in level0_results:
            vb_result = level0_results["visualBrand"]
            enriched["crossAgentInsights"]["visualBrand"] = {
                "visualConsistency": self._safe_extract(vb_result, "metrics.visualConsistency", 0),
                "brandRecognition": self._safe_extract(vb_result, "metrics.brandRecognition", 0),
                "colorConsistencyScore": self._safe_extract(vb_result, "colorConsistencyScore", {}),
                "gridProfessionalism": self._safe_extract(vb_result, "gridProfessionalism", {}),
                "visualArchetype": self._safe_extract(vb_result, "visualArchetypeAnalysis.archetype", "unknown"),
                "dominantColors": self._safe_extract(vb_result, "dominantColors", []),
                "thumbnailAnalysis": self._safe_extract(vb_result, "thumbnailAnalysis", {}),
            }
        
        # Extract key insights from Domain Master - NİŞ BİLGİSİ KRİTİK!
        if "domainMaster" in level0_results:
            dm_result = level0_results["domainMaster"]
            niche_info = self._safe_extract(dm_result, "niche_identification", {})
            business_identity = self._safe_extract(dm_result, "business_identity", {})
            
            enriched["crossAgentInsights"]["domainMaster"] = {
                "detectedNiche": self._safe_extract(niche_info, "primary_niche", 
                    self._safe_extract(niche_info, "detected_niche", "general")),
                "nicheCategory": self._safe_extract(niche_info, "category", "Genel"),
                "nicheConfidence": self._safe_extract(niche_info, "confidence", 0),
                "subNiches": self._safe_extract(niche_info, "sub_niches", []),
                "nicheAuthority": self._safe_extract(dm_result, "metrics.nicheAuthorityScore", 50),
                "trendAlignment": self._safe_extract(dm_result, "metrics.trendAlignmentScore", 50),
            }
            
            # Business Identity bilgisini de enriched'a ekle (SalesConversion için kritik)
            enriched["businessIdentity"] = {
                "account_type": self._safe_extract(business_identity, "account_type", "CONTENT_CREATOR"),
                "is_service_provider": self._safe_extract(business_identity, "is_service_provider", False),
                "correct_success_metrics": self._safe_extract(business_identity, "correct_success_metrics", []),
                "wrong_metrics_to_avoid": self._safe_extract(business_identity, "wrong_metrics_to_avoid", []),
                "benchmark_engagement": self._safe_extract(business_identity, "benchmark_engagement", 2.5),
            }
            
            # Ayrıca doğrudan niş bilgisini de ekle (kolay erişim için)
            enriched["detectedNiche"] = enriched["crossAgentInsights"]["domainMaster"]["detectedNiche"]
            enriched["nicheCategory"] = enriched["crossAgentInsights"]["domainMaster"]["nicheCategory"]
        
        # Add summary metrics for quick reference
        enriched["level0Summary"] = {
            "avgContentScore": self._calculate_avg_score(level0_results, "contentStrategist"),
            "avgAudienceScore": self._calculate_avg_score(level0_results, "audienceDynamics"),
            "avgVisualScore": self._calculate_avg_score(level0_results, "visualBrand"),
            "overallLevel0Score": self._calculate_overall_level0_score(level0_results),
            "criticalIssues": self._extract_critical_issues(level0_results),
            "topStrengths": self._extract_top_strengths(level0_results),
        }
        
        logger.info(f"Enriched account data with Level 0 insights: {list(enriched['crossAgentInsights'].keys())}")
        return enriched
    
    def _safe_extract(self, data: Dict[str, Any], path: str, default: Any) -> Any:
        """Safely extract nested value from dict using dot notation"""
        try:
            keys = path.split(".")
            value = data
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key)
                else:
                    return default
                if value is None:
                    return default
            return value
        except Exception:
            return default
    
    def _calculate_avg_score(self, results: Dict[str, Any], agent_name: str) -> float:
        """Calculate average score from agent result"""
        if agent_name not in results:
            return 0.0
        result = results[agent_name]
        return self._extract_score(result)
    
    def _calculate_overall_level0_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall Level 0 score"""
        scores = []
        weights = {"contentStrategist": 0.4, "audienceDynamics": 0.35, "visualBrand": 0.25}
        
        for agent, weight in weights.items():
            if agent in results:
                score = self._extract_score(results[agent])
                scores.append(score * weight)
        
        return sum(scores) / sum(weights.values()) if scores else 0.0
    
    def _extract_critical_issues(self, results: Dict[str, Any]) -> List[str]:
        """Extract critical issues from Level 0 results"""
        issues = []
        for agent_name, result in results.items():
            findings = self._extract_findings(result)
            for finding in findings:
                if isinstance(finding, dict):
                    if finding.get("severity") == "high" or finding.get("type") == "weakness":
                        issues.append(f"[{agent_name}] {finding.get('finding', finding.get('text', str(finding)))}")
                elif isinstance(finding, str) and any(kw in finding.lower() for kw in ["kritik", "düşük", "zayıf", "risk", "eksik"]):
                    issues.append(f"[{agent_name}] {finding}")
        return issues[:5]  # Top 5 critical issues
    
    def _extract_top_strengths(self, results: Dict[str, Any]) -> List[str]:
        """Extract top strengths from Level 0 results"""
        strengths = []
        for agent_name, result in results.items():
            findings = self._extract_findings(result)
            for finding in findings:
                if isinstance(finding, dict):
                    if finding.get("type") == "strength":
                        strengths.append(f"[{agent_name}] {finding.get('finding', finding.get('text', str(finding)))}")
                elif isinstance(finding, str) and any(kw in finding.lower() for kw in ["güçlü", "iyi", "yüksek", "başarılı", "excellent"]):
                    strengths.append(f"[{agent_name}] {finding}")
        return strengths[:5]  # Top 5 strengths
    
    def _prepare_validation_data(
        self,
        account_data: Dict[str, Any],
        all_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Prepare comprehensive data for System Governor validation"""
        validation_data = account_data.copy()
        validation_data["agentResults"] = all_results
        validation_data["resultsSummary"] = {
            "totalAgentsRun": len(all_results),
            "successfulAgents": sum(1 for r in all_results.values() if not r.get("error_flag")),
            "failedAgents": sum(1 for r in all_results.values() if r.get("error_flag")),
            "overallConsistency": self._calculate_result_consistency(all_results),
        }
        return validation_data
    
    def _calculate_result_consistency(self, results: Dict[str, Any]) -> float:
        """Calculate consistency score across agent results"""
        scores = [self._extract_score(r) for r in results.values() if not r.get("error_flag")]
        if len(scores) < 2:
            return 1.0
        
        # Calculate coefficient of variation (lower = more consistent)
        mean_score = sum(scores) / len(scores)
        if mean_score == 0:
            return 0.5
        
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5
        cv = std_dev / mean_score
        
        # Convert to consistency score (0-1, higher = more consistent)
        consistency = max(0, 1 - cv)
        return round(consistency, 2)

    async def run_all_agents(
        self,
        account_data: Dict[str, Any],
        agent_names: List[str],
    ) -> Dict[str, Any]:
        """Run all specified agents using configured strategy"""
        strategy = self.execution_config["strategy"]

        if strategy == "sequential":
            return await self.run_sequential(account_data, agent_names)
        elif strategy == "parallel":
            return await self.run_parallel(account_data, agent_names)
        else:  # dependency_aware
            return await self.run_dependency_aware(account_data, agent_names)

    # ---------------------- Validation ----------------------
    async def validate_results(
        self,
        results: Dict[str, Any],
        account_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Use System Governor to validate all agent results"""
        system_governor = self.agents["systemGovernor"]

        try:
            validation = await asyncio.wait_for(
                system_governor.validate_all(results, account_data),
                timeout=self.execution_config["timeouts"]["validation"],
            )
            return validation
        except asyncio.TimeoutError:
            logger.warning("Validation timed out")
            return {
                "validated": False,
                "confidence": 0.50,
                "issues": [{"type": "timeout", "description": "Validation timed out"}],
                "adjustments": [],
            }
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return {
                "validated": False,
                "confidence": 0.50,
                "issues": [{"type": "error", "description": str(e)}],
                "adjustments": [],
            }

    # ---------------------- Result Aggregation ----------------------
    def calculate_overall_score(
        self,
        results: Dict[str, Any],
        validation: Dict[str, Any],
    ) -> float:
        """Calculate weighted overall score"""
        total_weight = 0.0
        weighted_sum = 0.0

        for agent_name, result in results.items():
            if agent_name in self.agent_weights and not result.get("error_flag"):
                weight = self.agent_weights[agent_name]
                score = self._extract_score(result)
                weighted_sum += score * weight
                total_weight += weight

        if total_weight == 0:
            return 50.0  # Default neutral score

        base_score = weighted_sum / total_weight

        # Apply validation multiplier
        confidence = validation.get("confidence", 0.70)
        if confidence > 0.85:
            multiplier = self.validation_multipliers["high_confidence"]
        elif confidence >= 0.70:
            multiplier = self.validation_multipliers["medium_confidence"]
        else:
            multiplier = self.validation_multipliers["low_confidence"]

        # Check for critical issues
        if validation.get("issues") and any(
            i.get("severity") == "high" for i in validation.get("issues", [])
        ):
            multiplier = min(multiplier, self.validation_multipliers["critical_issues"])

        return base_score * multiplier

    def _extract_score(self, result: Dict[str, Any]) -> float:
        """Extract score from agent result"""
        if "score" in result:
            return float(result["score"])
        if "analysis" in result and isinstance(result["analysis"], dict):
            analysis = result["analysis"]
            if "score" in analysis:
                return float(analysis["score"])
            if "metrics" in analysis:
                metrics = analysis["metrics"]
                # Try various score field names
                for field in ["overallScore", "overall_score", "score"]:
                    if field in metrics:
                        return float(metrics[field])
        return 50.0  # Default

    def get_health_grade(self, score: float) -> str:
        """Map score to health grade"""
        for grade, (low, high) in self.health_grades.items():
            if low <= score <= high:
                return grade
        return "F"

    def consolidate_findings(
        self,
        results: Dict[str, Any],
        max_findings: int = 15,
    ) -> List[Dict[str, Any]]:
        """Consolidate and prioritize findings from all agents"""
        all_findings = []

        for agent_name, result in results.items():
            findings = self._extract_findings(result)
            for finding in findings:
                all_findings.append({
                    "text": finding,
                    "source_agent": agent_name,
                    "category": self._categorize_finding(finding, agent_name),
                    "importance": self._assess_importance(finding),
                    "confidence": result.get("confidence", 0.70),
                })

        # Sort by importance and confidence
        all_findings.sort(
            key=lambda x: (
                {"high": 3, "medium": 2, "low": 1}.get(x["importance"], 1),
                x["confidence"],
            ),
            reverse=True,
        )

        # Deduplicate similar findings
        consolidated = self._deduplicate_findings(all_findings)

        return consolidated[:max_findings]

    def _extract_findings(self, result: Dict[str, Any]) -> List[str]:
        """Extract findings from agent result"""
        if "findings" in result:
            return result["findings"]
        if "analysis" in result and isinstance(result["analysis"], dict):
            return result["analysis"].get("findings", [])
        return []

    def _categorize_finding(self, finding: str, agent_name: str) -> str:
        """Categorize finding based on content and source agent"""
        agent_category_map = {
            "contentStrategist": "Content & Strategy",
            "audienceDynamics": "Audience & Growth",
            "attentionArchitect": "Engagement & Community",
            "visualBrand": "Visual & Brand",
            "growthVirality": "Audience & Growth",
            "domainMaster": "Content & Strategy",
            "communityLoyalty": "Engagement & Community",
            "salesConversion": "Monetization & Business",
            "systemGovernor": "Technical & Compliance",
        }
        return agent_category_map.get(agent_name, "Content & Strategy")

    def _assess_importance(self, finding: str) -> str:
        """Assess importance of finding"""
        high_keywords = ["kritik", "önemli", "acil", "risk", "düşük", "yüksek", "critical", "urgent"]
        medium_keywords = ["orta", "geliştirilmeli", "optimize", "moderate"]

        finding_lower = finding.lower()
        if any(kw in finding_lower for kw in high_keywords):
            return "high"
        if any(kw in finding_lower for kw in medium_keywords):
            return "medium"
        return "low"

    def _deduplicate_findings(
        self,
        findings: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Remove duplicate/similar findings"""
        seen_texts = set()
        deduplicated = []

        for finding in findings:
            text = finding["text"].lower()[:100]  # First 100 chars for comparison
            if text not in seen_texts:
                seen_texts.add(text)
                deduplicated.append(finding)

        return deduplicated

    def prioritize_recommendations(
        self,
        results: Dict[str, Any],
        max_recommendations: int = 10,
    ) -> List[Dict[str, Any]]:
        """Prioritize recommendations from all agents"""
        all_recommendations = []

        for agent_name, result in results.items():
            recommendations = self._extract_recommendations(result)
            for rec in recommendations:
                all_recommendations.append({
                    "text": rec,
                    "source_agent": agent_name,
                    "impact": self._assess_impact(rec),
                    "difficulty": self._assess_difficulty(rec),
                    "timeframe": self._assess_timeframe(rec),
                    "confidence": result.get("confidence", 0.70),
                })

        # Calculate priority score
        for rec in all_recommendations:
            rec["priority_score"] = self._calculate_priority_score(rec)

        # Sort by priority
        all_recommendations.sort(key=lambda x: x["priority_score"], reverse=True)

        # Deduplicate
        deduplicated = self._deduplicate_recommendations(all_recommendations)

        return deduplicated[:max_recommendations]

    def _extract_recommendations(self, result: Dict[str, Any]) -> List[str]:
        """Extract recommendations from agent result"""
        if "recommendations" in result:
            return result["recommendations"]
        if "analysis" in result and isinstance(result["analysis"], dict):
            return result["analysis"].get("recommendations", [])
        return []

    def _assess_impact(self, recommendation: str) -> int:
        """Assess impact of recommendation (0-100)"""
        high_impact = ["viral", "büyüme", "growth", "artış", "revenue", "gelir"]
        medium_impact = ["optimize", "geliştir", "improve", "enhance"]

        rec_lower = recommendation.lower()
        if any(kw in rec_lower for kw in high_impact):
            return 85
        if any(kw in rec_lower for kw in medium_impact):
            return 65
        return 45

    def _assess_difficulty(self, recommendation: str) -> str:
        """Assess implementation difficulty"""
        easy_keywords = ["hemen", "basit", "kolay", "immediately", "simple", "easy"]
        hard_keywords = ["karmaşık", "uzun", "complex", "difficult", "major"]

        rec_lower = recommendation.lower()
        if any(kw in rec_lower for kw in easy_keywords):
            return "easy"
        if any(kw in rec_lower for kw in hard_keywords):
            return "hard"
        return "medium"

    def _assess_timeframe(self, recommendation: str) -> str:
        """Assess timeframe for implementation"""
        immediate_kw = ["hemen", "bugün", "immediately", "today", "now"]
        long_term_kw = ["uzun vadeli", "long-term", "months", "ay"]

        rec_lower = recommendation.lower()
        if any(kw in rec_lower for kw in immediate_kw):
            return "immediate"
        if any(kw in rec_lower for kw in long_term_kw):
            return "long-term"
        return "short-term"

    def _calculate_priority_score(self, recommendation: Dict[str, Any]) -> float:
        """Calculate priority score for recommendation"""
        w = self.recommendation_weights

        impact_score = recommendation["impact"] / 100
        ease_score = {"easy": 1.0, "medium": 0.6, "hard": 0.3}.get(
            recommendation["difficulty"], 0.6
        )
        time_score = {"immediate": 1.0, "short-term": 0.7, "long-term": 0.4}.get(
            recommendation["timeframe"], 0.7
        )
        resource_score = ease_score  # Simplified
        confidence_score = recommendation["confidence"]

        return (
            impact_score * w["impact"]
            + ease_score * w["ease"]
            + time_score * w["time_to_result"]
            + resource_score * w["resource_requirement"]
            + confidence_score * w["confidence"]
        ) * 100

    def _deduplicate_recommendations(
        self,
        recommendations: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Remove duplicate recommendations"""
        seen_texts = set()
        deduplicated = []

        for rec in recommendations:
            text = rec["text"].lower()[:80]
            if text not in seen_texts:
                seen_texts.add(text)
                deduplicated.append(rec)

        return deduplicated

    def select_key_strengths(
        self,
        results: Dict[str, Any],
        max_count: int = 3,
    ) -> List[str]:
        """Select top strengths from findings"""
        positive_keywords = ["güçlü", "iyi", "yüksek", "başarılı", "excellent", "strong", "good"]
        strengths = []

        for agent_name, result in results.items():
            findings = self._extract_findings(result)
            for finding in findings:
                if any(kw in finding.lower() for kw in positive_keywords):
                    score = self._extract_score(result)
                    strengths.append({"text": finding, "score": score})

        strengths.sort(key=lambda x: x["score"], reverse=True)
        return [s["text"] for s in strengths[:max_count]]

    def select_critical_issues(
        self,
        results: Dict[str, Any],
        validation: Dict[str, Any],
        max_count: int = 3,
    ) -> List[str]:
        """Select critical issues"""
        negative_keywords = ["düşük", "risk", "sorun", "eksik", "low", "poor", "issue", "problem"]
        issues = []

        for agent_name, result in results.items():
            findings = self._extract_findings(result)
            for finding in findings:
                if any(kw in finding.lower() for kw in negative_keywords):
                    issues.append(finding)

        # Add validation alerts
        for issue in validation.get("issues", []):
            if isinstance(issue, dict):
                issues.append(issue.get("description", str(issue)))
            else:
                issues.append(str(issue))

        return issues[:max_count]

    def select_immediate_actions(
        self,
        recommendations: List[Dict[str, Any]],
        max_count: int = 3,
    ) -> List[str]:
        """Select immediate action items"""
        immediate = [
            r for r in recommendations
            if r.get("timeframe") == "immediate" and r.get("difficulty") == "easy"
        ]
        immediate.sort(key=lambda x: x.get("impact", 0), reverse=True)
        return [r["text"] for r in immediate[:max_count]]

    # ---------------------- Report Generation ----------------------
    def calculate_composite_metrics(
        self,
        results: Dict[str, Any],
    ) -> Dict[str, float]:
        """Calculate composite metrics from all agents"""
        metrics = {
            "content_score": self._extract_score(results.get("contentStrategist", {})),
            "audience_score": self._extract_score(results.get("audienceDynamics", {})),
            "engagement_score": self._extract_score(results.get("attentionArchitect", {})),
            "visual_score": self._extract_score(results.get("visualBrand", {})),
            "growth_score": self._extract_score(results.get("growthVirality", {})),
            "niche_score": self._extract_score(results.get("domainMaster", {})),
            "community_score": self._extract_score(results.get("communityLoyalty", {})),
            "monetization_score": self._extract_score(results.get("salesConversion", {})),
            "authenticity_score": self._extract_score(results.get("systemGovernor", {})),
        }
        return metrics

    def calculate_qa_score(
        self,
        results: Dict[str, Any],
        validation: Dict[str, Any],
    ) -> Tuple[float, str]:
        """Calculate QA score and status"""
        # Completeness
        agents_with_results = sum(1 for r in results.values() if not r.get("error_flag"))
        completeness = (agents_with_results / len(results)) * 100 if results else 0

        # Consistency
        consistency = 100 if validation.get("validated", False) else 70

        # Quality
        avg_confidence = statistics.mean([
            r.get("confidence", 0.70) for r in results.values()
        ]) if results else 0.70
        quality = avg_confidence * 100

        # Format (assume valid if we got this far)
        format_score = 100

        qa_score = (
            completeness * self.qa_weights["completeness"]
            + consistency * self.qa_weights["consistency"]
            + quality * self.qa_weights["quality"]
            + format_score * self.qa_weights["format"]
        )

        # Determine status
        for status, (low, high) in self.qa_thresholds.items():
            if low <= qa_score <= high:
                return qa_score, status

        return qa_score, "regenerate"

    async def generate_report(
        self,
        account_data: Dict[str, Any],
        results: Dict[str, Any],
        validation: Dict[str, Any],
        execution_metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate final comprehensive report"""
        start_time = time.time()

        # Calculate scores
        overall_score = self.calculate_overall_score(results, validation)
        health_grade = self.get_health_grade(overall_score)
        composite_metrics = self.calculate_composite_metrics(results)

        # Consolidate findings and recommendations
        consolidated_findings = self.consolidate_findings(results)
        prioritized_recommendations = self.prioritize_recommendations(results)

        # Select highlights
        key_strengths = self.select_key_strengths(results)
        critical_issues = self.select_critical_issues(results, validation)
        immediate_actions = self.select_immediate_actions(prioritized_recommendations)

        # QA
        qa_score, qa_status = self.calculate_qa_score(results, validation)

        report_duration = time.time() - start_time

        return {
            "report_metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "analysis_duration": execution_metadata.get("total_duration", 0),
                "report_generation_duration": report_duration,
                "agents_run": list(results.keys()),
                "data_freshness": datetime.utcnow().isoformat(),
                "overall_confidence": validation.get("confidence", 0.70),
            },
            "executive_summary": {
                "overall_score": round(overall_score, 1),
                "health_grade": health_grade,
                "key_strengths": key_strengths,
                "critical_issues": critical_issues,
                "immediate_actions": immediate_actions,
            },
            "detailed_scores": composite_metrics,
            "comprehensive_findings": [
                {
                    "rank": i + 1,
                    "category": f["category"],
                    "finding": f["text"],
                    "importance": f["importance"],
                    "source_agents": [f["source_agent"]],
                    "confidence": f["confidence"],
                }
                for i, f in enumerate(consolidated_findings)
            ],
            "prioritized_recommendations": [
                {
                    "rank": i + 1,
                    "recommendation": r["text"],
                    "priority": "high" if r["priority_score"] > 70 else "medium" if r["priority_score"] > 40 else "low",
                    "impact": r["impact"],
                    "difficulty": r["difficulty"],
                    "timeframe": r["timeframe"],
                    "expected_outcome": f"Bu öneri uygulandığında {r['impact']}% etkisi bekleniyor",
                    "source_agents": [r["source_agent"]],
                    "confidence": r["confidence"],
                }
                for i, r in enumerate(prioritized_recommendations)
            ],
            "agent_details": results,
            "validation": {
                "status": "validated" if validation.get("validated") else "warnings",
                "confidence": validation.get("confidence", 0.70),
                "data_quality": "good" if validation.get("validated") else "acceptable",
                "alerts": [
                    i.get("description", str(i)) if isinstance(i, dict) else str(i)
                    for i in validation.get("issues", [])
                ],
            },
            "quality_assurance": {
                "qa_score": round(qa_score, 1),
                "status": qa_status,
                "ready_for_delivery": qa_status in ["release_ready", "minor_fixes"],
            },
            "appendix": {
                "methodology": "Multi-agent AI analysis using specialized domain experts",
                "data_sources": ["Instagram API", "Profile scraping", "Engagement analysis"],
                "limitations": [
                    "Analysis based on available public data",
                    "Engagement metrics may have ±5% variance",
                    "Bot detection has ~80% accuracy",
                ],
            },
        }

    # ---------------------- Data Acquisition ----------------------
    async def acquire_instagram_data(
        self,
        request: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Acquire Instagram data using the Data Acquisition Agent.
        
        This is the first step in the analysis pipeline. It determines
        the analysis mode (full_access vs public_only) and fetches data
        from the appropriate sources.
        
        Args:
            request: Analysis request with type and optional credentials
                - analysis_type: "own_account" | "competitor"
                - own_account: { username, password?, fetch_private? }
                - competitor: { username }
                
        Returns:
            Acquisition result with data, mode, and limitations
        """
        logger.info(f"Starting Instagram data acquisition")
        start_time = time.time()
        
        try:
            # Run data acquisition
            result = await self.data_acquisition_agent.acquire_data(request)
            
            # Store mode and limitations for downstream agents
            self.data_mode = result.get("mode")
            self.data_limitations = result.get("limitations")
            
            duration_ms = (time.time() - start_time) * 1000
            logger.info(f"Data acquisition completed in {duration_ms:.0f}ms, mode: {self.data_mode}")
            
            self.metrics_collector.record(
                "data_acquisition_duration_ms",
                duration_ms,
                tags={"mode": self.data_mode, "success": result.get("success", False)},
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Data acquisition failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "mode": AnalysisMode.PUBLIC_ONLY.value,
                "data": None,
            }

    def enrich_account_data_with_acquisition(
        self,
        account_data: Dict[str, Any],
        acquisition_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Enrich account data with data from acquisition.
        
        Merges acquisition results into the account data format
        expected by analysis agents.
        """
        if not acquisition_result.get("success") or not acquisition_result.get("data"):
            logger.warning("No acquisition data to enrich, using original account data")
            return account_data
        
        enriched = account_data.copy()
        acq_data = acquisition_result.get("data", {})
        
        # Add acquisition metadata
        enriched["_acquisition"] = {
            "mode": acquisition_result.get("mode"),
            "sources": acquisition_result.get("metadata", {}).get("sources_used", []),
            "coverage": acquisition_result.get("metadata", {}).get("data_coverage"),
            "timestamp": acquisition_result.get("metadata", {}).get("scrape_timestamp"),
            "limitations": acquisition_result.get("limitations"),
        }
        
        # Merge profile data
        profile = acq_data.get("profile", {})
        if profile:
            enriched["username"] = profile.get("username", enriched.get("username"))
            enriched["followers"] = profile.get("follower_count", enriched.get("followers", 0))
            enriched["following"] = profile.get("following_count", enriched.get("following", 0))
            enriched["posts"] = profile.get("post_count", enriched.get("posts", 0))
            enriched["bio"] = profile.get("bio", enriched.get("bio", ""))
            enriched["verified"] = profile.get("is_verified", enriched.get("verified", False))
            enriched["isBusiness"] = profile.get("is_business", enriched.get("isBusiness", False))
            enriched["profilePicUrl"] = profile.get("profile_pic_url", enriched.get("profilePicUrl", ""))
            enriched["externalUrl"] = profile.get("external_url", enriched.get("externalUrl"))
        
        # Merge posts data
        posts = acq_data.get("posts", [])
        if posts:
            enriched["recentPosts"] = posts
            
            # Calculate engagement metrics from posts
            if len(posts) > 0:
                avg_likes = sum(p.get("likes", 0) for p in posts) / len(posts)
                avg_comments = sum(p.get("comments", 0) for p in posts) / len(posts)
                followers = enriched.get("followers", 1) or 1
                engagement_rate = ((avg_likes + avg_comments) / followers) * 100
                
                enriched["avgLikes"] = avg_likes
                enriched["avgComments"] = avg_comments
                enriched["engagementRate"] = round(engagement_rate, 2)
        
        # Merge private data if available (full_access mode)
        if acquisition_result.get("mode") == AnalysisMode.FULL_ACCESS.value:
            audience = acq_data.get("audience")
            if audience:
                enriched["audienceDemographics"] = audience
            
            insights = acq_data.get("insights_timeline")
            if insights:
                enriched["insightsTimeline"] = insights
            
            stories = acq_data.get("stories")
            if stories:
                enriched["storyInsights"] = stories
        
        # Add estimated metrics if public_only mode
        estimated = acq_data.get("estimated")
        if estimated:
            enriched["estimatedMetrics"] = estimated
        
        # Calculate analysis depth adjustments
        enriched["_analysisAdjustments"] = adjust_analysis_depth(
            acquisition_result.get("mode", AnalysisMode.PUBLIC_ONLY.value)
        )
        
        logger.info(f"Enriched account data with {len(posts)} posts, mode: {acquisition_result.get('mode')}")
        return enriched

    def get_agent_data_availability_for_mode(self) -> Dict[str, str]:
        """Get data availability for each agent based on current mode"""
        if self.data_mode and self.data_mode in self.agent_data_availability:
            return self.agent_data_availability[self.data_mode]
        return self.agent_data_availability.get(AnalysisMode.PUBLIC_ONLY.value, {})

    # ---------------------- Main Analysis Entry Point ----------------------
    async def analyze_account(
        self,
        account_data: Dict[str, Any],
        agent_names: Optional[List[str]] = None,
        acquisition_request: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Main entry point for account analysis.
        
        Analysis Pipeline:
        1. Data Acquisition (if request provided) - Instagram scraping
        2. Run all analysis agents (parallel/dependency-aware)
        3. System Governor validation
        4. Report generation
        
        Args:
            account_data: Base account data
            agent_names: List of agents to run (default: all)
            acquisition_request: Optional data acquisition request
                - analysis_type: "own_account" | "competitor"
                - own_account: { username, password?, fetch_private? }
                - competitor: { username }
        
        Returns:
            Complete analysis report with all agent results
        """
        self.analysis_id = str(uuid.uuid4())
        start_time = time.time()

        # Default to all agents except systemGovernor (run separately for validation)
        if agent_names is None:
            agent_names = [
                "contentStrategist",
                "audienceDynamics",
                "visualBrand",
                "attentionArchitect",
                "growthVirality",
                "domainMaster",
                "communityLoyalty",
                "salesConversion",
            ]

        execution_metadata = {
            "analysis_id": self.analysis_id,
            "started_at": datetime.utcnow().isoformat(),
            "agents_requested": agent_names,
            "cache_hits": 0,
            "retries": 0,
            "data_mode": None,
            "data_sources": [],
        }

        try:
            logger.info(f"Starting analysis for @{account_data.get('username', 'unknown')}")
            
            # Phase 0: Data Acquisition (if request provided)
            enriched_account_data = account_data
            acquisition_result = None
            
            if acquisition_request:
                logger.info("Phase 0: Running Instagram data acquisition")
                acquisition_result = await self.acquire_instagram_data(acquisition_request)
                
                if acquisition_result.get("success"):
                    enriched_account_data = self.enrich_account_data_with_acquisition(
                        account_data,
                        acquisition_result
                    )
                    execution_metadata["data_mode"] = acquisition_result.get("mode")
                    execution_metadata["data_sources"] = acquisition_result.get("metadata", {}).get("sources_used", [])
                    execution_metadata["data_coverage"] = acquisition_result.get("metadata", {}).get("data_coverage")
                else:
                    logger.warning(f"Data acquisition failed: {acquisition_result.get('error')}")
                    execution_metadata["data_acquisition_error"] = acquisition_result.get("error")
            
            # Phase 1: Validate input data
            logger.info("Phase 1: Validating input data")

            # Phase 2: Run all agents with enriched data
            logger.info("Phase 2: Running agents")
            results = await self.run_all_agents(enriched_account_data, agent_names)

            # Track completed agents
            agents_completed = [
                name for name, result in results.items()
                if not result.get("error_flag")
            ]
            agents_failed = [
                name for name, result in results.items()
                if result.get("error_flag")
            ]

            # Phase 3: Validation
            logger.info("Phase 3: Running validation")
            validation = await self.validate_results(results, enriched_account_data)

            # Phase 3.5: Apply Metric Sanity Gates (consistency enforcement)
            logger.info("Phase 3.5: Applying metric sanity gates")
            results, sanity_gate_report = self.sanity_gates.apply_all_gates(
                results, enriched_account_data
            )

            # Phase 4: Generate report
            logger.info("Phase 4: Generating report")
            total_duration = time.time() - start_time
            execution_metadata.update({
                "completed_at": datetime.utcnow().isoformat(),
                "total_duration": total_duration,
                "agents_completed": agents_completed,
                "agents_failed": agents_failed,
            })

            report = await self.generate_report(
                enriched_account_data, results, validation, execution_metadata
            )

            # Add orchestration metadata
            report["orchestration_metadata"] = execution_metadata
            
            # Add sanity gate report
            report["sanity_gates"] = sanity_gate_report
            
            # Add strategic phase to executive summary
            if sanity_gate_report.get("strategic_phase"):
                phase = sanity_gate_report["strategic_phase"]
                report["executive_summary"]["strategic_phase"] = phase["phase_name"]
                report["executive_summary"]["phase_focus"] = phase["focus_areas"]
                report["executive_summary"]["blocked_strategies"] = phase["blocked_strategies"]
            
            # Add data acquisition info to report
            if acquisition_result:
                report["data_acquisition"] = {
                    "mode": acquisition_result.get("mode"),
                    "coverage": acquisition_result.get("metadata", {}).get("data_coverage"),
                    "sources": acquisition_result.get("metadata", {}).get("sources_used", []),
                    "limitations": acquisition_result.get("limitations"),
                    "agent_data_availability": self.get_agent_data_availability_for_mode(),
                }
                
                # Add disclaimer if public_only mode
                if acquisition_result.get("mode") == AnalysisMode.PUBLIC_ONLY.value:
                    report["data_disclaimer"] = {
                        "message": "Bu analiz sadece herkese açık veriler kullanılarak yapılmıştır. Özel metrikler (reach, impressions, demographics vb.) tahmini değerlerdir.",
                        "confidence_adjustment": 0.7,
                        "unavailable_metrics": acquisition_result.get("limitations", {}).get("unavailable_metrics", []),
                    }

            # Cleanup
            self._cleanup()

            logger.info(f"Analysis completed in {total_duration:.1f}s")
            return report

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            total_duration = time.time() - start_time
            return {
                "orchestration_metadata": {
                    "analysis_id": self.analysis_id,
                    "status": "failed",
                    "error": str(e),
                    "duration": total_duration,
                    "data_mode": self.data_mode,
                },
                "executive_summary": {
                    "overall_score": 0,
                    "health_grade": "F",
                    "key_strengths": [],
                    "critical_issues": [f"Analysis failed: {e}"],
                    "immediate_actions": ["Retry analysis"],
                },
                "agent_details": {},
                "validation": {"status": "failed", "confidence": 0},
            }

    # ---------------------- Advanced Analysis Report Generation ----------------------
    async def generate_advanced_analysis(
        self,
        account_data: Dict[str, Any],
        agent_results: Optional[Dict[str, Any]] = None,
        analysis_id: Optional[str] = None,
        run_analysis_if_needed: bool = True
    ) -> Dict[str, Any]:
        """
        Generate comprehensive advanced analysis report using the Advanced Analysis Engine.
        
        This implements all 11 analysis modules:
        1. Bot ve Fake Follower Tespiti
        2. Engagement Rate Benchmarking
        3. Bio, Profil ve İçerik Tutarlılık Kontrolü
        4. Hashtag Stratejisi Analizi
        5. İçerik Formatı ve Büyüme Kanalı Kullanımı
        6. İçerik Kalitesi ve Dağılımı
        7. Shadowban ve Algoritma Risk Göstergeleri
        8. Öncelikli Eylem Önerileri
        9. Viral Potansiyel ve Büyüme İzleme
        10. Açıklama ve Gerekçe
        11. Veri Kalitesi ve Güven Skoru
        
        Args:
            account_data: Base account data with statistics
            agent_results: Pre-computed agent results (optional)
            analysis_id: Analysis ID for tracking
            run_analysis_if_needed: If True and no results provided, run full analysis first
            
        Returns:
            Complete advanced analysis report with all findings, recommendations, and strategies
        """
        logger.info(f"Starting advanced analysis for @{account_data.get('username', 'unknown')}")
        start_time = time.time()
        
        try:
            # Use provided analysis_id or generate new one
            analysis_id = analysis_id or str(uuid.uuid4())
            
            # Step 1: Get or run agent analysis
            if agent_results is None and run_analysis_if_needed:
                logger.info("No agent results provided, running full analysis first...")
                analysis_result = await self.analyze_account(account_data)
                agent_results = analysis_result.get('agent_details', {})
            elif agent_results is None:
                return {
                    "error": "No agent results provided",
                    "recommendation": "Run analysis first or set run_analysis_if_needed=True"
                }
            
            # Extract agentResults if full results object is passed
            if "agentResults" in agent_results:
                logger.info("Extracting agentResults from full results object")
                agent_results = agent_results["agentResults"]
            elif "agent_details" in agent_results:
                logger.info("Extracting agent_details from results object")
                agent_results = agent_results["agent_details"]
            
            logger.info(f"Agent results available: {list(agent_results.keys())}")
            
            # Step 2: Prepare account data with all metrics
            enriched_account_data = self._prepare_advanced_analysis_data(account_data)
            
            # Step 3: Run Advanced Analysis Engine
            logger.info("Running Advanced Analysis Engine...")
            advanced_engine = AdvancedAnalysisEngine()
            advanced_report = advanced_engine.analyze(
                enriched_account_data,
                agent_results,
                analysis_id
            )
            
            duration_ms = (time.time() - start_time) * 1000
            logger.info(f"Advanced analysis completed in {duration_ms:.0f}ms")
            
            # Step 4: Add generation metadata
            advanced_report['_generation_metadata'] = {
                'duration_ms': duration_ms,
                'timestamp': datetime.now().isoformat(),
                'account': account_data.get('username', 'unknown'),
                'engine_version': 'AdvancedAnalysisEngine v1.0',
                'agents_analyzed': list(agent_results.keys())
            }
            
            return advanced_report
            
        except Exception as e:
            import traceback
            logger.error(f"Advanced analysis failed: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                "error": str(e),
                "status": "failed",
                "recommendation": "Check agent results and retry"
            }
    
    def _prepare_advanced_analysis_data(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare account data for advanced analysis"""
        enriched = account_data.copy()
        
        # Ensure all required fields exist
        defaults = {
            'username': 'unknown',
            'followers': 0,
            'following': 0,
            'posts': 0,
            'engagementRate': 0,
            'avgLikes': 0,
            'avgComments': 0,
            'bio': '',
            'category': 'unknown',
            'isBusiness': False,
            'isVerified': False
        }
        
        for key, default_value in defaults.items():
            if key not in enriched or enriched[key] is None:
                enriched[key] = default_value
        
        return enriched

    # ---------------------- Content Plan Generation ----------------------
    async def generate_content_plan(
        self,
        account_data: Dict[str, Any],
        agent_results: Optional[Dict[str, Any]] = None,
        run_analysis_if_needed: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a 7-day content plan using all agent analysis results.
        
        Args:
            account_data: Base account data
            agent_results: Pre-computed agent results (optional)
            run_analysis_if_needed: If True and no results provided, run full analysis first
            
        Returns:
            Complete 7-day content plan with validation
        """
        logger.info(f"Starting content plan generation for @{account_data.get('username', 'unknown')}")
        start_time = time.time()
        
        try:
            # Step 1: Get or run agent analysis
            if agent_results is None and run_analysis_if_needed:
                logger.info("No agent results provided, running full analysis first...")
                analysis_result = await self.run_full_analysis(account_data)
                agent_results = analysis_result.get('agent_details', {})
            elif agent_results is None:
                return {
                    "error": "No agent results provided",
                    "recommendation": "Run analysis first or set run_analysis_if_needed=True"
                }
            
            # Extract agentResults if full results object is passed
            if "agentResults" in agent_results:
                logger.info("Extracting agentResults from full results object")
                agent_results = agent_results["agentResults"]
            elif "agent_details" in agent_results:
                logger.info("Extracting agent_details from results object")
                agent_results = agent_results["agent_details"]
            
            logger.info(f"Agent results keys: {list(agent_results.keys())}")
            
            # Step 2: Validate data completeness
            validation = self.content_plan_generator.validate_required_data(agent_results)
            
            if not validation['can_generate']:
                logger.warning(f"Insufficient data for content plan: {validation['missing_agents']}")
                return {
                    "error": "Insufficient analysis data",
                    "validation": validation,
                    "recommendation": "Run full analysis to gather required data"
                }
            
            # Step 3: Prepare enriched data
            enriched_data = self._prepare_content_plan_data(account_data, agent_results)
            
            # Step 4: Generate content plan
            logger.info("Generating 7-day content plan...")
            content_plan = await self.content_plan_generator.generate_content_plan(
                enriched_data,
                agent_results
            )
            
            duration_ms = (time.time() - start_time) * 1000
            logger.info(f"Content plan generated in {duration_ms:.0f}ms")
            
            # Step 5: Add metadata
            content_plan['_generation_metadata'] = {
                'duration_ms': duration_ms,
                'data_validation': validation,
                'timestamp': datetime.now().isoformat(),
                'account': account_data.get('username', 'unknown')
            }
            
            return content_plan
            
        except Exception as e:
            import traceback
            logger.error(f"Content plan generation failed: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                "error": str(e),
                "status": "failed",
                "recommendation": "Check agent results and retry"
            }
    
    def _prepare_content_plan_data(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare comprehensive data for content plan generation"""
        enriched = account_data.copy()
        
        # Handle case where full results object is passed instead of just agentResults
        if "agentResults" in agent_results:
            agent_results = agent_results["agentResults"]
        elif "agent_details" in agent_results:
            agent_results = agent_results["agent_details"]
        
        enriched['agentResults'] = agent_results
        
        # Add cross-agent insights summary
        enriched['crossAgentInsights'] = {}
        
        # Extract key data from each agent
        for agent_name, result in agent_results.items():
            # Skip non-dict results
            if not isinstance(result, dict):
                logger.warning(f"Skipping non-dict result for agent {agent_name}: {type(result)}")
                continue
            if result and not result.get('error_flag'):
                enriched['crossAgentInsights'][agent_name] = self._extract_key_insights(
                    agent_name, result
                )
        
        # Calculate summary metrics
        enriched['level0Summary'] = {
            'avgContentScore': self._calculate_avg_score(agent_results, 'contentStrategist'),
            'avgAudienceScore': self._calculate_avg_score(agent_results, 'audienceDynamics'),
            'avgVisualScore': self._calculate_avg_score(agent_results, 'visualBrand'),
            'overallScore': self._calculate_overall_level0_score(agent_results),
            'criticalIssues': self._extract_critical_issues(agent_results),
            'topStrengths': self._extract_top_strengths(agent_results),
        }
        
        return enriched
    
    def _extract_key_insights(self, agent_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key insights from agent result for content planning"""
        insights = {}
        
        if agent_name == 'contentStrategist':
            insights = {
                'contentEffectivenessScore': self._safe_extract(result, 'metrics.contentEffectivenessScore', 0),
                'hashtagEffectiveness': self._safe_extract(result, 'metrics.hashtagEffectiveness', 0),
                'captionQuality': self._safe_extract(result, 'metrics.captionQuality', 0),
                'contentPillars': self._safe_extract(result, 'detailed_scores.content_diversity.topic_variety.pillars_identified', []),
                'hookAnalysis': self._safe_extract(result, 'hookAnalysis', {}),
                'hashtagAnalysis': self._safe_extract(result, 'hashtagAnalysis', {}),
                'abTestRecommendations': self._safe_extract(result, 'abTestRecommendations', {}),
            }
        elif agent_name == 'audienceDynamics':
            insights = {
                'audienceQuality': self._safe_extract(result, 'metrics.audienceQuality', 0),
                'followerSegmentation': self._safe_extract(result, 'followerSegmentation', {}),
                'botDetectionScore': self._safe_extract(result, 'botDetectionScore', {}),
                'personas': self._safe_extract(result, 'personas', []),
                'languagePatterns': self._safe_extract(result, 'audience_analysis.language_patterns', {}),
            }
        elif agent_name == 'visualBrand':
            insights = {
                'visualConsistency': self._safe_extract(result, 'metrics.visualConsistency', 0),
                'colorConsistencyScore': self._safe_extract(result, 'colorConsistencyScore', {}),
                'dominantColors': self._safe_extract(result, 'dominantColors', []),
                'visualArchetype': self._safe_extract(result, 'visualArchetypeAnalysis.archetype', 'unknown'),
                'gridProfessionalism': self._safe_extract(result, 'gridProfessionalism', {}),
            }
        elif agent_name == 'attentionArchitect':
            insights = {
                'retentionPrediction': self._safe_extract(result, 'retentionPrediction', {}),
                'emotionalTriggers': self._safe_extract(result, 'emotionalTriggers', []),
                'hookAnalysis': self._safe_extract(result, 'hook_analysis', {}),
                'postLevelAnalysis': self._safe_extract(result, 'postLevelAnalysis', []),
            }
        elif agent_name == 'growthVirality':
            insights = {
                'growthProjection': self._safe_extract(result, 'growthProjection', {}),
                'competitorGapAnalysis': self._safe_extract(result, 'competitorGapAnalysis', {}),
                'viralLoopStrategy': self._safe_extract(result, 'viralLoopStrategy', {}),
                'funnelAnalysis': self._safe_extract(result, 'funnelAnalysis', {}),
            }
        elif agent_name == 'domainMaster':
            insights = {
                'nicheIdentification': self._safe_extract(result, 'niche_identification', {}),
                'nicheBenchmarks': self._safe_extract(result, 'nicheBenchmarks', {}),
                'sectorBestPractices': self._safe_extract(result, 'sectorBestPractices', {}),
                'seasonalConsiderations': self._safe_extract(result, 'seasonalConsiderations', {}),
                'trendAnalysis': self._safe_extract(result, 'trend_analysis', {}),
            }
        elif agent_name == 'communityLoyalty':
            insights = {
                'communityHealth': self._safe_extract(result, 'community_health', {}),
                'loyaltyIndicators': self._safe_extract(result, 'loyalty_analysis', {}),
            }
        elif agent_name == 'salesConversion':
            insights = {
                'monetizationReadiness': self._safe_extract(result, 'monetization_readiness', {}),
                'conversionPotential': self._safe_extract(result, 'conversion_analysis', {}),
            }
        
        return insights

    def _cleanup(self) -> None:
        """Cleanup after analysis"""
        self.metrics_collector.clear()
        self.cache_manager.clear_local()
        gc.collect()

    # ---------------------- Health Check ----------------------
    async def health_check(self) -> Dict[str, Any]:
        """Check orchestrator health"""
        checks = {
            "gemini_api": await self._check_gemini(),
            "agents": self._check_agents(),
            "redis": await self._check_redis(),
        }

        all_healthy = all(checks.values())

        return {
            "status": "healthy" if all_healthy else "unhealthy",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def _check_gemini(self) -> bool:
        """Check Gemini API availability"""
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    self.gemini_model.generate_content,
                    "test",
                ),
                timeout=5.0,
            )
            return response is not None
        except Exception:
            return False

    def _check_agents(self) -> bool:
        """Check all agents initialized"""
        return len(self.agents) == 9 and self.content_plan_generator is not None

    async def _check_redis(self) -> bool:
        """Check Redis availability"""
        if not self.redis:
            return True  # Redis is optional
        try:
            await self.redis.ping()
            return True
        except Exception:
            return False


__all__ = ["AgentOrchestrator", "MetricsCollector", "RateLimiter", "CacheManager"]
