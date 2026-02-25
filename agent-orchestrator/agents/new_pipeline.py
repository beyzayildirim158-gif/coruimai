# New Pipeline Orchestrator - Sequential Multi-Stage Analysis
# Implements the new analysis flow with Delta Sync, Governor Audit, and ELI5 formatting
"""
New Pipeline Orchestrator

AKIŞ:
1. START: Apify Scrape - Ham veri çekimi
2. DELTA SYNC: PostgreSQL'den önceki raporu getir
3. STAGE 1: Domain Master - Sektör ve benchmark belirleme (Foundation)
4. STAGE 2: PhD Agent Team - Paralel çalışma
5. STAGE 3: Governor Audit - Veto Gate, çelişki kontrolü
6. STAGE 4: ELI5 & Hook Audit - Basit dil çevirisi
7. FINAL: JSON & PDF Output
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from google import genai
from google.genai import types

from .domain_master import DomainMasterAgent
from .growth_virality import GrowthViralityAgent
from .sales_conversion import SalesConversionAgent
from .visual_brand import VisualBrandAgent
from .community_loyalty import CommunityLoyaltyAgent
from .attention_architect import AttentionArchitectAgent
from .system_governor import SystemGovernorAgent
from .eli5_formatter import ELI5FormatterAgent
from .content_plan_generator import ContentPlanGenerator
from .deepseek_final_analyst import DeepSeekFinalAnalyst
from .deepseek_fallback import get_deepseek_fallback, is_fallback_available
from .metric_sanity_gates import MetricSanityGates, get_sanity_gates

logger = logging.getLogger(__name__)


class NewPipelineOrchestrator:
    """
    New Pipeline Orchestrator
    
    Sequential multi-stage analysis with:
    - Delta sync for comparison with previous reports
    - Domain Master as foundation (runs first)
    - PhD agents run with industry benchmarks
    - Governor audit with veto power
    - ELI5 formatting for simple output
    """
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        
        # Initialize Gemini Client (new SDK)
        self._init_gemini()
        
        # Initialize agents
        self._init_agents()
        
        # Rate limiting - Optimized for Gemini 1.5 Flash (higher rate limits)
        self.last_api_call = 0
        self.min_interval = 4.0  # 4 seconds between API calls (15 RPM)
        
        # Config for better 503 handling
        self.max_retries = 6  # More retries for 503 recovery
        self.retry_base_delay = 8  # Base delay seconds (shorter for 503, decorator handles exponential)
        self.global_cooldown = 0  # Global cooldown after rate limit
        
    def _init_gemini(self) -> None:
        """Initialize Gemini with new SDK"""
        api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_client = genai.Client(api_key=api_key)
        
        # Store config for agents - increased max_output_tokens for complete responses
        self.generation_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            max_output_tokens=16384,  # Increased from 8192 to prevent truncation
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
            ]
        )
        
        # Model name - Using gemini-2.0-flash for stability (verified in models.list())
        self.model_name = "gemini-2.0-flash"
    
    def _init_agents(self) -> None:
        """Initialize all agents with new SDK client - SHARED instances (legacy)"""
        # NOTE: These are shared instances, for isolated execution use _create_fresh_agents()
        self._create_agent_instances()
    
    def _create_agent_instances(self) -> None:
        """Create fresh agent instances - called for each analysis to prevent state bleeding"""
        # Stage 1: Foundation
        self.domain_master = DomainMasterAgent(self.gemini_client, self.generation_config, self.model_name)
        
        # Stage 2: PhD Team (will run in parallel but with rate limiting)
        self.phd_agents = {
            "growthVirality": GrowthViralityAgent(self.gemini_client, self.generation_config, self.model_name),
            "salesConversion": SalesConversionAgent(self.gemini_client, self.generation_config, self.model_name),
            "visualBrand": VisualBrandAgent(self.gemini_client, self.generation_config, self.model_name),
            "communityLoyalty": CommunityLoyaltyAgent(self.gemini_client, self.generation_config, self.model_name),
            "attentionArchitect": AttentionArchitectAgent(self.gemini_client, self.generation_config, self.model_name),
        }
        
        # Stage 3: Governor (Veto Gate)
        self.governor = SystemGovernorAgent(self.gemini_client, self.generation_config, self.model_name)
        
        # Stage 4: ELI5 Formatter
        self.eli5_formatter = ELI5FormatterAgent(self.gemini_client, self.generation_config, self.model_name)
        
        # Stage 5: DeepSeek Final Analyst (Son yorum)
        self.deepseek_analyst = DeepSeekFinalAnalyst()
        
        # Stage 4.5: Metric Sanity Gates (Post-processor)
        self.sanity_gates = get_sanity_gates()
        
        # Content Plan Generator
        self.content_plan_generator = ContentPlanGenerator(self.gemini_client, self.generation_config, self.model_name)
    
    async def _rate_limit_wait(self) -> None:
        """Wait for rate limit"""
        # Check global cooldown first
        if self.global_cooldown > 0:
            logger.info(f"Global cooldown: waiting {self.global_cooldown}s...")
            await asyncio.sleep(self.global_cooldown)
            self.global_cooldown = 0
        
        now = time.time()
        elapsed = now - self.last_api_call
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            logger.info(f"Rate limit: waiting {wait_time:.1f}s...")
            await asyncio.sleep(wait_time)
        self.last_api_call = time.time()
    
    async def _run_agent_with_retry(
        self,
        agent,
        account_data: Dict[str, Any],
        agent_name: str,
    ) -> Dict[str, Any]:
        """
        Run agent with Gemini as PRIMARY and DeepSeek as SECONDARY
        
        Order:
        1. Try Gemini first (higher quality, better reasoning)
        2. If Gemini fails, fall back to DeepSeek
        3. If both fail, return error response
        """
        # ============================================================
        # STRATEGY: Gemini PRIMARY, DeepSeek SECONDARY
        # Gemini provides higher quality analysis
        # ============================================================
        
        # STEP 1: Try Gemini first
        for attempt in range(self.max_retries):
            try:
                await self._rate_limit_wait()
                logger.info(f"🚀 Running {agent_name} with Gemini (primary, attempt {attempt + 1})...")
                
                result = await agent.analyze(account_data)
                
                if result.get("error"):
                    raise Exception(result.get("errorMessage", "Unknown error"))
                
                logger.info(f"✓ {agent_name} completed via Gemini (primary)")
                result["modelUsed"] = "gemini-primary"
                return result
                
            except Exception as gemini_error:
                error_str = str(gemini_error).lower()
                
                # Model overloaded (503) - switch to DeepSeek immediately
                if any(x in error_str for x in ["503", "unavailable", "overloaded"]):
                    logger.warning(f"⚡ Gemini overloaded (503) for {agent_name}, switching to DeepSeek immediately...")
                    break  # Exit retry loop, go to DeepSeek
                
                # Rate limit / Quota exhausted error
                if any(x in error_str for x in ["429", "rate", "quota", "exhausted"]):
                    wait_time = self.retry_base_delay * (2 ** attempt)  # 15, 30, 60,
                    logger.warning(f"Gemini rate limited on {agent_name} (attempt {attempt + 1}/{self.max_retries}), waiting {wait_time}s...")
                    
                    # Set global cooldown for next agent too
                    self.global_cooldown = min(30, wait_time // 2)
                    
                    await asyncio.sleep(wait_time)
                    continue
                
                # Other error - try DeepSeek immediately on last retry
                if attempt >= self.max_retries - 1:
                    logger.warning(f"Gemini failed for {agent_name} after {self.max_retries} attempts, trying DeepSeek secondary...")
                    break
                
                # Retry Gemini with shorter delay
                logger.warning(f"Gemini error in {agent_name}: {gemini_error}, retrying in {self.retry_base_delay}s...")
                await asyncio.sleep(self.retry_base_delay)
                continue
        
        # STEP 2: Fall back to DeepSeek (if available)
        if is_fallback_available():
            try:
                await self._rate_limit_wait()
                logger.info(f"🔄 Running {agent_name} with DeepSeek (secondary)...")
                
                fallback = get_deepseek_fallback()
                
                # Get prompts from agent
                system_prompt = agent.get_system_prompt()
                user_prompt = agent.get_analysis_prompt(account_data)
                
                result = await fallback.run_agent_analysis(
                    agent_name=agent_name,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt
                )
                
                if not result.get("error"):
                    logger.info(f"✓ {agent_name} completed via DeepSeek (secondary)")
                    result["modelUsed"] = "deepseek-secondary"
                    return result
                else:
                    logger.warning(f"DeepSeek also returned error for {agent_name}")
                    
            except Exception as deepseek_error:
                logger.warning(f"DeepSeek error for {agent_name}: {deepseek_error}")
        
        # STEP 3: Both failed - return default response
        logger.error(f"✗ {agent_name} failed with both Gemini and DeepSeek")
        return self._get_error_response(agent_name)
    
    def _get_error_response(self, agent_name: str) -> Dict[str, Any]:
        """Generate a default error response with a valid overallScore"""
        return {
            "agent": agent_name,
            "error": False,  # Mark as success to not break pipeline
            "errorMessage": None,
            "findings": [
                {
                    "type": "info",
                    "category": "system",
                    "finding": f"{agent_name} analizi tamamlanamadı - default değerler kullanıldı",
                    "evidence": "Rate limit veya API hatası nedeniyle",
                    "impact_score": 50
                }
            ],
            "recommendations": [
                {
                    "priority": 1,
                    "category": "system",
                    "action": "Analizi daha sonra tekrar deneyin",
                    "expected_impact": "Daha detaylı sonuçlar",
                    "implementation": "Birkaç dakika bekleyip yeniden analiz başlatın",
                    "difficulty": "easy",
                    "timeline": "immediate"
                }
            ],
            "metrics": {
                "overallScore": 50.0  # Default neutral score
            },
            "agentName": agent_name,
            "timestamp": datetime.utcnow().isoformat(),
            "modelUsed": self.model_name,
            "note": "Bu sonuç API sınırlamaları nedeniyle default değerler içermektedir."
        }
    
    async def run_full_analysis(
        self,
        account_data: Dict[str, Any],
        previous_analysis: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """
        Run full analysis pipeline
        
        Args:
            account_data: Fresh data from Apify
            previous_analysis: Delta - previous analysis for comparison
            progress_callback: Async function to report progress
            
        Returns:
            Complete analysis result
        """
        # ============================================================
        # CRITICAL FIX: Create fresh agent instances for EACH analysis
        # This prevents state bleeding between concurrent analyses
        # (e.g., @natgeo data appearing in @ilm_wa_iman analysis)
        # ============================================================
        logger.info(f"🔄 Creating fresh agent instances for @{account_data.get('username', 'unknown')}")
        self._create_agent_instances()
        
        results = {
            "analysisStartedAt": datetime.utcnow().isoformat(),
            "username": account_data.get("username"),
            "stages": {},
            "agentResults": {},
            "eli5Report": {},
            "finalScore": 0,
            "finalGrade": "F",
        }
        
        async def report_progress(stage: str, progress: int, agent: str = None, message: str = None):
            if progress_callback:
                await progress_callback({
                    "stage": stage,
                    "progress": progress,
                    "currentAgent": agent,
                    "message": message,
                })
        
        try:
            # ============================================================
            # STAGE 1: DOMAIN MASTER (Foundation)
            # ============================================================
            await report_progress("STAGE_1", 5, "domainMaster", "Sektör ve benchmark analizi başlıyor...")
            
            logger.info("=" * 60)
            logger.info("STAGE 1: DOMAIN MASTER - Setting Industry Benchmarks")
            logger.info("=" * 60)
            
            domain_result = await self._run_agent_with_retry(
                self.domain_master,
                account_data,
                "domainMaster"
            )
            
            results["agentResults"]["domainMaster"] = domain_result
            results["stages"]["domain_master"] = {
                "completed": not domain_result.get("error"),
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            # Extract benchmarks for other agents
            industry_benchmarks = self._extract_benchmarks(domain_result)
            
            # ============================================================
            # YENİ: İŞLETME KİMLİĞİ TESPİTİ (Business Identity Detection)
            # ============================================================
            business_identity = self.domain_master.detect_business_identity(account_data)
            results["businessIdentity"] = business_identity
            
            # Log business identity
            if business_identity.get("is_service_provider"):
                logger.warning(f"⚠️ BUSINESS IDENTITY: {business_identity['account_type']}")
                logger.warning(f"   Doğru metrikler: {business_identity['correct_success_metrics']}")
                logger.warning(f"   YANLIŞ metrikler: {business_identity['wrong_metrics_to_avoid']}")
            
            # Update benchmarks based on business identity
            if business_identity.get("is_service_provider"):
                industry_benchmarks["account_type"] = business_identity["account_type"]
                industry_benchmarks["correct_metrics"] = business_identity["correct_success_metrics"]
                industry_benchmarks["engagement_rate"]["average"] = business_identity.get("benchmark_engagement", 1.5)
                industry_benchmarks["business_identity_note"] = business_identity.get("analysis_note", "")
            
            await report_progress("STAGE_1", 15, "domainMaster", "Sektör benchmarkları belirlendi")
            
            # ============================================================
            # STAGE 2: PHD AGENT TEAM (Sequential to avoid rate limits)
            # ============================================================
            await report_progress("STAGE_2", 20, None, "PhD ajan takımı çalışmaya başlıyor...")
            
            logger.info("=" * 60)
            logger.info("STAGE 2: PHD AGENT TEAM - Running with Industry Benchmarks")
            logger.info("=" * 60)
            
            # Enrich account data with benchmarks and delta
            enriched_data = self._enrich_with_benchmarks(
                account_data,
                industry_benchmarks,
                previous_analysis
            )
            
            # Run PhD agents sequentially (to avoid rate limits)
            phd_agent_names = list(self.phd_agents.keys())
            progress_per_agent = 50 / len(phd_agent_names)  # 20-70%
            
            import random
            
            for i, agent_name in enumerate(phd_agent_names):
                # Add jitter between agents to prevent burst requests
                if i > 0:
                    jitter = random.uniform(1.0, 3.0)
                    logger.info(f"⏳ Jitter delay: {jitter:.1f}s before {agent_name}")
                    await asyncio.sleep(jitter)
                
                current_progress = 20 + int((i + 1) * progress_per_agent)
                await report_progress("STAGE_2", current_progress, agent_name, f"{agent_name} analiz ediyor...")
                
                agent = self.phd_agents[agent_name]
                agent_result = await self._run_agent_with_retry(agent, enriched_data, agent_name)
                results["agentResults"][agent_name] = agent_result
            
            results["stages"]["phd_team"] = {
                "completed": True,
                "agents_run": phd_agent_names,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            await report_progress("STAGE_2", 70, None, "PhD ajan takımı tamamlandı")
            
            # ============================================================
            # STAGE 3: GOVERNOR AUDIT (Veto Gate)
            # ============================================================
            await report_progress("STAGE_3", 72, "systemGovernor", "Governor audit başlıyor...")
            
            logger.info("=" * 60)
            logger.info("STAGE 3: GOVERNOR AUDIT - Checking for Contradictions")
            logger.info("=" * 60)
            
            # Prepare audit data
            audit_data = {
                **enriched_data,
                "agentResults": results["agentResults"],
                "industryBenchmarks": industry_benchmarks,
            }
            
            # Run governor audit
            governor_result = await self._run_governor_audit(audit_data)
            results["agentResults"]["systemGovernor"] = governor_result
            
            # ============================================================
            # YENİ: SERT VALİDASYON KURALLARI UYGULA (Hard Validation Rules)
            # ============================================================
            logger.info("Applying HARD VALIDATION RULES...")
            
            # Tüm sonuçları birleştir ve validation rules uygula
            combined_results = {
                "metrics": self._aggregate_all_metrics(results["agentResults"]),
                "swot": self._extract_swot(results["agentResults"]),
                **results["agentResults"]
            }
            
            # Governor'un hard validation rules'unu uygula
            validated_results = self.governor.apply_hard_validation_rules(
                combined_results,
                account_data
            )
            
            # Validation sonuçlarını kaydet
            results["hardValidation"] = validated_results.get("hard_validation_results", {})
            
            # Log validation violations
            violations = results["hardValidation"].get("violations", [])
            if violations:
                logger.warning(f"🚨 HARD VALIDATION: {len(violations)} kural ihlali bulundu!")
                for v in violations:
                    logger.warning(f"   - {v['rule']}: {v['message']}")
            
            # Check for vetoes
            vetoes = governor_result.get("vetoes", [])
            if vetoes:
                logger.warning(f"Governor found {len(vetoes)} contradictions!")
                results["stages"]["governor_audit"] = {
                    "completed": True,
                    "vetoes_found": len(vetoes),
                    "vetoes": vetoes,
                    "timestamp": datetime.utcnow().isoformat(),
                }
                # Re-run vetoed agents (simplified - just flag them)
                for veto in vetoes:
                    agent_name = veto.get("agent")
                    if agent_name in results["agentResults"]:
                        results["agentResults"][agent_name]["vetoed"] = True
                        results["agentResults"][agent_name]["vetoReason"] = veto.get("reason")
            else:
                results["stages"]["governor_audit"] = {
                    "completed": True,
                    "vetoes_found": 0,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            
            await report_progress("STAGE_3", 80, "systemGovernor", "Governor audit tamamlandı")
            
            # ============================================================
            # STAGE 4: ELI5 & HOOK AUDIT (Formatting)
            # ============================================================
            await report_progress("STAGE_4", 82, "eli5Formatter", "Rapor basitleştiriliyor...")
            
            logger.info("=" * 60)
            logger.info("STAGE 4: ELI5 & HOOK AUDIT - Simplifying Report")
            logger.info("=" * 60)
            
            eli5_data = {
                **account_data,
                "agentResults": results["agentResults"],
                "industryBenchmarks": industry_benchmarks,
            }
            
            eli5_result = await self._run_agent_with_retry(
                self.eli5_formatter,
                eli5_data,
                "eli5Formatter"
            )
            
            results["eli5Report"] = eli5_result
            results["stages"]["eli5_formatting"] = {
                "completed": not eli5_result.get("error"),
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            await report_progress("STAGE_4", 88, "eli5Formatter", "Rapor hazırlandı")
            
            # ============================================================
            # STAGE 4.5: METRIC SANITY GATES (Post-Processing)
            # Çelişkili metrikleri düzeltir, genel önerileri spesifikleştirir
            # ============================================================
            await report_progress("STAGE_4_5", 89, "metricSanityGates", "Metrik tutarlılığı kontrol ediliyor...")
            
            logger.info("=" * 60)
            logger.info("STAGE 4.5: METRIC SANITY GATES - Enforcing Consistency")
            logger.info("=" * 60)
            
            try:
                # Sanity gates uygula - çelişkili metrikleri düzelt
                sanitized_results, sanity_report = self.sanity_gates.apply_all_gates(
                    results["agentResults"],
                    account_data
                )
                
                # Düzeltilmiş sonuçları kaydet
                results["agentResults"] = sanitized_results
                results["sanitizationReport"] = {
                    "corrections": sanity_report.get("corrections", {}),
                    "warnings": sanity_report.get("warnings", []),
                    "phase_info": sanity_report.get("strategic_phase", {}),
                    "metrics_summary": self.sanity_gates._extract_cross_agent_metrics(sanitized_results),
                }
                
                # Log sanity gate sonuçları
                corrections = sanity_report.get("corrections", [])
                warnings = sanity_report.get("warnings", [])
                phase_info = sanity_report.get("strategic_phase", {})
                
                if corrections:
                    logger.warning(f"🔧 SANITY GATES: {len(corrections)} düzeltme yapıldı")
                    for correction in corrections:
                        if isinstance(correction, dict):
                            logger.info(f"   - {correction.get('type', 'unknown')}: {correction.get('message', correction)}")
                        else:
                            logger.info(f"   - {correction}")
                
                if warnings:
                    logger.warning(f"⚠️ SANITY GATES: {len(warnings)} uyarı")
                    for warning in warnings[:5]:  # İlk 5 uyarıyı logla
                        logger.info(f"   - {warning}")
                
                if phase_info:
                    logger.info(f"📊 STRATEGIC PHASE: {phase_info.get('phase_name', 'Unknown')}")
                    logger.info(f"   Effective Score: {phase_info.get('effective_score', 'N/A')}")
                    logger.info(f"   Focus Areas: {phase_info.get('focus_areas', [])}")
                
                results["stages"]["sanity_gates"] = {
                    "completed": True,
                    "corrections_count": len(corrections),
                    "warnings_count": len(warnings),
                    "determined_phase": phase_info.get("determined_phase", "unknown"),
                    "timestamp": datetime.utcnow().isoformat(),
                }
                
            except Exception as sanity_error:
                logger.error(f"Sanity Gates error: {sanity_error}")
                results["stages"]["sanity_gates"] = {
                    "completed": False,
                    "error": str(sanity_error),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            
            await report_progress("STAGE_4_5", 89, "metricSanityGates", "Metrik tutarlılığı tamamlandı")

            # ============================================================
            # STAGE 4.6: DATA QUALITY REPORT (Missing Fields Detection)
            # Toplanamayan / eksik veri alanlarını tespit et ve raporla
            # ============================================================
            results["agentResults"]["dataQualityReport"] = self._detect_missing_fields(
                enriched_data, results["agentResults"]
            )
            logger.info(
                f"📋 DATA QUALITY: "
                f"{len(results['agentResults']['dataQualityReport']['missing_fields'])} eksik alan tespit edildi"
            )

            # ============================================================
            # STAGE 5: DEEPSEEK FINAL ANALYST (Son Yorum)
            # ============================================================
            await report_progress("STAGE_5", 90, "deepseekFinalAnalyst", "Final yorum hazırlanıyor...")
            
            logger.info("=" * 60)
            logger.info("STAGE 5: DEEPSEEK FINAL ANALYST - Generating Final Verdict")
            logger.info("=" * 60)
            
            # DeepSeek için tüm verileri hazırla
            deepseek_data = {
                "username": account_data.get("username"),
                "accountData": account_data,
                "finalScore": self._calculate_final_score(results["agentResults"], enriched_data)[0],
                "finalGrade": self._calculate_final_score(results["agentResults"], enriched_data)[1],
                "agentResults": results["agentResults"],
                "businessIdentity": results.get("businessIdentity", {}),
                "hardValidation": results.get("hardValidation", {}),
                "industryBenchmarks": industry_benchmarks,
                "dataFetchError": enriched_data.get("dataFetchError", False),
                "dataFetchWarning": enriched_data.get("dataFetchWarning", ""),
            }
            
            # DeepSeek Final Analyst'ı çalıştır
            deepseek_result = await self.deepseek_analyst.analyze(deepseek_data)
            
            results["finalVerdict"] = deepseek_result
            results["stages"]["deepseek_final"] = {
                "completed": not deepseek_result.get("error"),
                "disabled": deepseek_result.get("disabled", False),
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            if deepseek_result.get("disabled"):
                logger.warning("DeepSeek Final Analyst devre dışı - API key ayarlanmamış")
            elif deepseek_result.get("error"):
                logger.error(f"DeepSeek error: {deepseek_result.get('errorMessage')}")
            else:
                logger.info("✓ DeepSeek Final Analyst completed successfully")
            
            await report_progress("STAGE_5", 95, "deepseekFinalAnalyst", "Final yorum tamamlandı")
            
            # ============================================================
            # FINAL: Calculate Overall Score & Grade
            # ============================================================
            logger.info("=" * 60)
            logger.info("FINAL: Calculating Overall Score")
            logger.info("=" * 60)
            
            final_score, final_grade = self._calculate_final_score(results["agentResults"], enriched_data)
            results["finalScore"] = final_score
            results["finalGrade"] = final_grade
            results["analysisCompletedAt"] = datetime.utcnow().isoformat()
            
            # FALSE-NEGATIVE koruma uyarısını results'a ekle
            if enriched_data.get("dataFetchError"):
                results["warnings"] = results.get("warnings", [])
                results["warnings"].append(enriched_data.get("dataFetchWarning", ""))
                results["dataFetchError"] = True
                results["protectedMetrics"] = enriched_data.get("protectedMetrics", [])
            
            # Add comparison with previous analysis if available
            if previous_analysis:
                results["deltaComparison"] = self._calculate_delta(
                    results,
                    previous_analysis
                )
            
            await report_progress("COMPLETED", 100, None, "Analiz tamamlandı!")
            
            logger.info(f"Analysis completed: Score={final_score}, Grade={final_grade}")
            
            return results
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            results["error"] = str(e)
            results["analysisCompletedAt"] = datetime.utcnow().isoformat()
            return results
    
    def _detect_missing_fields(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        DATA QUALITY REPORT: Detect fields that could not be collected.
        Returns a structured report with missing field names, reasons, and a confidence score.
        """
        missing: list[Dict[str, Any]] = []

        # ── Helper ──────────────────────────────────────────────────────────
        def _absent(key: str, obj: Dict[str, Any] = account_data) -> bool:
            v = obj.get(key)
            return v is None or v == "" or v == [] or v == {}

        # ── 1. Comment text data ──────────────────────────────────────────
        # Aggregate latest_comments from all posts to top-level for easy access
        all_comment_texts: List[str] = []
        for p in (account_data.get("recentPosts") or []):
            all_comment_texts.extend(p.get("latest_comments") or [])
        if all_comment_texts and _absent("comments_list") and _absent("recentComments"):
            # Comments found in posts — expose at top level for Sentiment Engine
            account_data["comments_list"] = all_comment_texts[:50]  # max 50 yorumu al

        has_comments = bool(account_data.get("comments_list") or account_data.get("recentComments"))
        if not has_comments:
            missing.append({
                "field": "comments_list",
                "label": "Yorum içerikleri",
                "reason": "Apify bu çekimde yorum metni döndürmedi; yalnızca yorum sayısı mevcut.",
                "impact": "Duygu analizi (Sentiment Engine) çalışamıyor.",
                "severity": "high",
            })

        # ── 2. Follower growth history ───────────────────────────────────
        if _absent("followerHistory") and _absent("followerGrowth"):
            missing.append({
                "field": "followerHistory",
                "label": "Takipçi büyüme geçmişi",
                "reason": "Instagram API geçmiş takipçi verisini paylaşmıyor; bu veri teknik olarak scrape edilemiyor.",
                "impact": "Büyüme hızı mevcut post verilerinden tahmin ediliyor.",
                "severity": "medium",
                "ai_instruction": "Yeterli geçmiş veri oluşana kadar büyüme hızı hesaplanmamaktadır. Bunu kritik hata olarak değerlendirme.",
            })

        # ── 3. Story data ────────────────────────────────────────────────
        if _absent("storyInsights") and _absent("stories") and _absent("avgStoryViews"):
            missing.append({
                "field": "story_insights",
                "label": "Story verileri",
                "reason": "Apify Instagram scraper story içeriğini çekemiyor.",
                "impact": "Story bazlı etkileşim analizi yapılamıyor.",
                "severity": "medium",
            })

        # ── 4. Competitor data ───────────────────────────────────────────
        competitors = account_data.get("competitors") or []
        if not competitors:
            missing.append({
                "field": "competitors",
                "label": "Rakip hesap verisi",
                "reason": "Rakip hesap otomatik tespit edilemedi; kullanıcı tarafından sağlanmadı.",
                "impact": "Rekabetçi kıyaslama (Competitive Benchmark) tahminsel verilerle yapılıyor.",
                "severity": "low",
            })

        # ── 5. Content format distribution ──────────────────────────────
        posts = account_data.get("recentPosts") or []
        # A post has meaningful type data if it's NOT the generic default 'image'
        # or if __typename / product_type was properly parsed into reel/carousel
        has_type_data = any(p.get("type") not in (None, "", "image") for p in posts)
        if posts and not has_type_data:
            missing.append({
                "field": "content_format_distribution",
                "label": "İçerik format dağılımı (Reels/Carousel/Image)",
                "reason": "Apify'den gelen post verisinde içerik tipi (type) alanı eksik.",
                "impact": "Reels/Carousel/Statik gönderi dağılımı hesaplanamıyor.",
                "severity": "medium",
            })

        # ── 6. Audience demographics ────────────────────────────────────
        if _absent("audienceDemographics"):
            missing.append({
                "field": "audience_demographics",
                "label": "Hedef kitle demografisi (yaş/cinsiyet/konum)",
                "reason": "Public-only modda Instagram demografik veri paylaşmıyor.",
                "impact": "Persona analizi ve reklam hedefleme önerileri genelleştiriliyor.",
                "severity": "medium",
            })

        # ── 7. Post timestamps ───────────────────────────────────────────
        posts_without_ts = [p for p in posts if not p.get("timestamp") and not p.get("takenAt")]
        if len(posts_without_ts) > len(posts) * 0.3:
            missing.append({
                "field": "post_timestamps",
                "label": f"Post tarihleri ({len(posts_without_ts)}/{len(posts)} gönderi)",
                "reason": "Kısıtlı/private içeriklerde timestamp gelmiyor.",
                "impact": "Paylaşım zamanlaması analizi (Audience Chronobiology) eksik kalıyor.",
                "severity": "low",
            })

        # ── Confidence score ─────────────────────────────────────────────
        high_count   = sum(1 for m in missing if m["severity"] == "high")
        medium_count = sum(1 for m in missing if m["severity"] == "medium")
        low_count    = sum(1 for m in missing if m["severity"] == "low")
        penalty = high_count * 15 + medium_count * 7 + low_count * 3
        confidence_score = max(30, 100 - penalty)

        return {
            "missing_fields": [m["field"] for m in missing],
            "missing_details": missing,
            "confidence_score": confidence_score,
            "total_missing": len(missing),
            "has_critical_gaps": high_count > 0,
            "summary": (
                f"{len(missing)} veri alanı toplanamadı." if missing
                else "Tüm kritik veriler başarıyla toplandı."
            ),
        }

    def _extract_benchmarks(self, domain_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract industry benchmarks from Domain Master result"""
        if domain_result.get("error"):
            # Default benchmarks if Domain Master failed
            return {
                "industry": "general",
                "engagement_rate": {"poor": 1.0, "average": 2.5, "good": 4.0, "excellent": 6.0},
                "growth_rate": {"poor": 1.0, "average": 3.0, "good": 5.0, "excellent": 10.0},
                "follower_quality": {"poor": 50, "average": 65, "good": 80, "excellent": 90},
            }
        
        # Extract from result
        metrics = domain_result.get("metrics", {})
        detailed = domain_result.get("detailed_analysis", {})
        
        return {
            "industry": domain_result.get("detected_niche", "general"),
            "engagement_rate": detailed.get("engagement_benchmarks", {
                "poor": 1.0, "average": 2.5, "good": 4.0, "excellent": 6.0
            }),
            "growth_rate": detailed.get("growth_benchmarks", {
                "poor": 1.0, "average": 3.0, "good": 5.0, "excellent": 10.0
            }),
            "follower_quality": detailed.get("follower_quality_benchmarks", {
                "poor": 50, "average": 65, "good": 80, "excellent": 90
            }),
            "content_frequency": detailed.get("posting_frequency", {
                "minimum": 3, "recommended": 5, "optimal": 7
            }),
            "niche_specific_rules": detailed.get("niche_rules", []),
        }
    
    def _enrich_with_benchmarks(
        self,
        account_data: Dict[str, Any],
        benchmarks: Dict[str, Any],
        previous_analysis: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Enrich account data with benchmarks and delta"""
        enriched = account_data.copy()
        
        # ============================================================
        # FALSE-NEGATIVE KORUMA PROTOKOLÜ (Data Fetch Error Protection)
        # ============================================================
        avg_likes = account_data.get("avgLikes", 0) or 0
        followers = account_data.get("followers", 0) or 0
        
        # ============================================================
        # OPERATION SIGHT RESTORATION - GELİŞTİRİLMİŞ HAYALET VERİ TESPİTİ
        # 3 farklı durum kontrol ediliyor:
        # 1. avgLikes == 0 veya None ama followers > 1000 → API sorunu
        # 2. Backend'den gelen dataFetchWarning varsa → Zaten bilinen sorun
        # 3. posts > 0 ama recentPosts boş → Post çekilemedi
        # ============================================================
        
        # Backend'den gelen uyarıyı kontrol et
        backend_warning = account_data.get("dataFetchWarning")
        
        # avgLikes kontrolü (None veya 0)
        avg_likes_missing = avg_likes is None or avg_likes == 0
        
        # Post sayısı vs çekilen post kontrolü
        reported_posts = account_data.get("posts", 0) or account_data.get("postsCount", 0) or 0
        recent_posts = account_data.get("recentPosts", []) or []
        post_mismatch = reported_posts > 0 and len(recent_posts) == 0
        
        # Herhangi bir veri sorunu var mı?
        has_data_issue = (
            (followers > 1000 and avg_likes_missing) or  # Klasik hayalet veri
            backend_warning is not None or               # Backend zaten uyardı
            post_mismatch                                # Post çekilemedi
        )
        
        if has_data_issue:
            logger.warning("=" * 60)
            logger.warning("⚠️ FALSE-NEGATIVE KORUMA AKTİF!")
            logger.warning(f"   Followers: {followers:,} | avgLikes: {avg_likes}")
            logger.warning(f"   Reported Posts: {reported_posts} | Scraped Posts: {len(recent_posts)}")
            if backend_warning:
                logger.warning(f"   Backend Warning: {backend_warning[:100]}...")
            logger.warning("   Durum: Instagram API kısıtlaması - engagement verisi güvenilmez")
            logger.warning("   Aksiyon: Engagement metrikleri muaf tutulacak, skor korunacak")
            logger.warning("=" * 60)
            
            enriched["dataFetchError"] = True
            enriched["dataFetchErrorType"] = "ENGAGEMENT_DATA_UNAVAILABLE"
            
            # En açıklayıcı uyarıyı seç
            if backend_warning:
                enriched["dataFetchWarning"] = backend_warning
            elif post_mismatch:
                enriched["dataFetchWarning"] = (
                    f"⚠️ HAYALET VERİ TESPİTİ: Profilde {reported_posts} gönderi görünüyor ancak "
                    f"hiçbir post çekilemedi. Muhtemel sebepler: 1) Hesap yaş kısıtlamalı, "
                    f"2) Apify cookie/login gerekli, 3) resultsType='posts' olmayabilir. "
                    f"Engagement metrikleri güvenilir DEĞİL."
                )
            else:
                enriched["dataFetchWarning"] = (
                    f"⚠️ VERİ ERİŞİM UYARISI: {followers:,} takipçili hesapta engagement verisi "
                    f"(avgLikes={avg_likes}) çekilemedi veya sıfır. Bu hesabın gerçek etkileşimi "
                    f"muhtemelen 0 değildir. Engagement metrikleri puanlama dışı bırakıldı."
                )
            
            enriched["protectedMetrics"] = ["engagementRate", "avgLikes", "avgComments", "likesToFollowersRatio"]
            
            # Engagement rate varsayılan değer ata
            engagement_rate = account_data.get("engagementRate")
            if engagement_rate is None or engagement_rate == 0:
                assumed_rate = benchmarks.get("engagement_rate", {}).get("average", 2.5)
                enriched["assumedEngagementRate"] = assumed_rate
                enriched["engagementRateNote"] = f"API kısıtlaması nedeniyle sektör ortalaması varsayıldı: %{assumed_rate}"
        else:
            enriched["dataFetchError"] = False
        
        # Add industry benchmarks
        enriched["industryBenchmarks"] = benchmarks
        enriched["industry"] = benchmarks.get("industry", "general")
        
        # Add delta (previous analysis) for comparison
        if previous_analysis:
            enriched["previousAnalysis"] = {
                "date": previous_analysis.get("analysisCompletedAt"),
                "score": previous_analysis.get("finalScore"),
                "grade": previous_analysis.get("finalGrade"),
                "metrics": self._extract_previous_metrics(previous_analysis),
            }
            enriched["hasDelta"] = True
        else:
            enriched["hasDelta"] = False
        
        # Add strict evaluation flag
        enriched["strictEvaluation"] = True
        
        # Data fetch error varsa, evaluation context'e ekle
        data_fetch_note = ""
        if enriched.get("dataFetchError"):
            data_fetch_note = """
⚠️ VERİ ERİŞİM KISITLAMASI AKTİF:
- Beğeni verileri çekilemedi (API limiti)
- Engagement metrikleri GÜVENİLMEZ
- Bu metriklere dayalı olumsuz yorum YAPMA
- Puanlama sadece erişilebilir verilerle yapılacak
"""
        
        enriched["evaluationContext"] = f"""
🚨 ZORUNLU BENCHMARK KURALLARI - TEK DOĞRULUK KAYNAĞI 🚨

SEKTÖR: {benchmarks.get('industry', 'genel')}
HESAP TİPİ: {benchmarks.get('account_type', 'CONTENT_CREATOR')}

📊 BENCHMARK STANDARTLARI (Domain Master tarafından belirlendi):
- Minimum etkileşim oranı: %{benchmarks.get('engagement_rate', {}).get('average', 2.5)}
- "İyi" etkileşim: %{benchmarks.get('engagement_rate', {}).get('good', 4.0)}
- "Mükemmel" etkileşim: %{benchmarks.get('engagement_rate', {}).get('excellent', 6.0)}
- Minimum büyüme oranı: %{benchmarks.get('growth_rate', {}).get('average', 3.0)}
- "İyi" büyüme: %{benchmarks.get('growth_rate', {}).get('good', 5.0)}

⛔ YASAK DAVRANIŞ:
- ASLA kendi bilginden sektör ortalaması UYDURMA
- ASLA yukarıdaki benchmarkların dışında değer kullanma
- Eğer metrik bu standardın ALTINDAYSA durumu NEGATİF yorumla
- %{benchmarks.get('engagement_rate', {}).get('average', 2.5)} altı engagement ASLA "iyi" değildir

✅ ZORUNLU DAVRANIŞ:
- Sadece sana verilen benchmark_standards verisini referans al
- Metrik < Benchmark ise: "yetersiz", "düşük", "geliştirmeli"
- Metrik >= Benchmark ise: "yeterli", "sektör ortalamasında"
- Metrik > Good Benchmark ise: "iyi", "başarılı"

{data_fetch_note}
"""
        
        return enriched
    
    def _extract_previous_metrics(self, previous: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key metrics from previous analysis"""
        agent_results = previous.get("agentResults", {})
        
        metrics = {}
        for agent_name, result in agent_results.items():
            if isinstance(result, dict) and "metrics" in result:
                metrics[agent_name] = result["metrics"]
        
        return metrics
    
    async def _run_governor_audit(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run governor audit with contradiction checking"""
        # Create special audit prompt
        agent_results = audit_data.get("agentResults", {})
        benchmarks = audit_data.get("industryBenchmarks", {})
        engagement_rate = audit_data.get("engagementRate", 0)
        
        # Check for obvious contradictions before calling LLM
        contradictions = []
        
        # Rule 1: Low engagement cannot be "good"
        engagement_threshold = benchmarks.get("engagement_rate", {}).get("average", 2.5)
        for agent_name, result in agent_results.items():
            if not isinstance(result, dict):
                continue
            
            findings = result.get("findings", [])
            metrics = result.get("metrics", {})
            
            # Check if agent said "good" engagement with low actual rate
            if engagement_rate < engagement_threshold:
                for finding in findings:
                    if isinstance(finding, str):
                        finding_lower = finding.lower()
                        if any(word in finding_lower for word in ["iyi", "good", "excellent", "harika", "başarılı"]):
                            if any(word in finding_lower for word in ["etkileşim", "engagement"]):
                                contradictions.append({
                                    "agent": agent_name,
                                    "type": "false_positive",
                                    "reason": f"Etkileşim oranı %{engagement_rate:.2f} (sektör ortalaması %{engagement_threshold}), 'iyi' denemez",
                                    "finding": finding[:100],
                                })
        
        # Run full governor analysis
        await self._rate_limit_wait()
        governor_result = await self.governor.analyze(audit_data)
        
        # Post-process: dedupe, clean, filter meaningless entries
        governor_result = self.governor.post_process_result(governor_result)
        
        # Merge pre-checked contradictions
        if "vetoes" not in governor_result:
            governor_result["vetoes"] = []
        governor_result["vetoes"].extend(contradictions)
        
        return governor_result
    
    def _calculate_final_score(self, agent_results: Dict[str, Any], enriched_data: Dict[str, Any] = None) -> Tuple[float, str]:
        """Calculate final score from all agent results with FALSE-NEGATIVE protection"""
        
        # FALSE-NEGATIVE KORUMA: Veri çekme hatası varsa engagement-ağırlıklı skorları muaf tut
        data_fetch_error = False
        protected_metrics = []
        if enriched_data:
            data_fetch_error = enriched_data.get("dataFetchError", False)
            protected_metrics = enriched_data.get("protectedMetrics", [])
        
        weights = {
            "domainMaster": 0.10,
            "growthVirality": 0.20,
            "salesConversion": 0.15,
            "visualBrand": 0.15,
            "communityLoyalty": 0.20,
            "attentionArchitect": 0.15,
            "systemGovernor": 0.05,
        }
        
        # FALSE-NEGATIVE KORUMA: Veri hatası varsa engagement-ağırlıklı ajanların weight'ini azalt
        if data_fetch_error:
            logger.warning("⚠️ FALSE-NEGATIVE KORUMA: Score hesaplaması ayarlandı")
            # Engagement-bağımlı ajanların ağırlığını düşür
            weights["growthVirality"] = 0.10  # 0.20 -> 0.10
            weights["communityLoyalty"] = 0.10  # 0.20 -> 0.10
            # Engagement-bağımsız ajanların ağırlığını artır
            weights["visualBrand"] = 0.20  # 0.15 -> 0.20
            weights["salesConversion"] = 0.20  # 0.15 -> 0.20
            weights["domainMaster"] = 0.15  # 0.10 -> 0.15
            weights["attentionArchitect"] = 0.20  # 0.15 -> 0.20
        
        total_score = 0
        total_weight = 0
        
        for agent_name, result in agent_results.items():
            if agent_name not in weights:
                continue
            if not isinstance(result, dict):
                continue
            if result.get("error"):
                continue
            
            # Get score from metrics
            metrics = result.get("metrics", {})
            
            # Look for various score fields
            score = None
            for key in ["overallScore", "score", "totalScore", "finalScore"]:
                if key in metrics and metrics[key] is not None:
                    try:
                        score = float(metrics[key])
                        break
                    except (TypeError, ValueError):
                        continue
            
            # If no score found, try to calculate from sub-metrics
            if score is None:
                numeric_metrics = []
                for v in metrics.values():
                    try:
                        if isinstance(v, (int, float)) and 0 <= v <= 100:
                            numeric_metrics.append(float(v))
                    except (TypeError, ValueError):
                        continue
                if numeric_metrics:
                    score = sum(numeric_metrics) / len(numeric_metrics)
            
            if score is not None and isinstance(score, (int, float)):
                # Apply veto penalty
                if result.get("vetoed"):
                    score *= 0.7  # 30% penalty for vetoed results
                
                weight = weights[agent_name]
                total_score += score * weight
                total_weight += weight
        
        # Calculate weighted average
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 50  # Default neutral score
        
        # Determine grade
        if final_score >= 90:
            grade = "A+"
        elif final_score >= 80:
            grade = "A"
        elif final_score >= 70:
            grade = "B"
        elif final_score >= 60:
            grade = "C"
        elif final_score >= 50:
            grade = "D"
        else:
            grade = "F"
        
        return round(final_score, 1), grade
    
    def _calculate_delta(
        self,
        current: Dict[str, Any],
        previous: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Calculate changes from previous analysis"""
        current_score = current.get("finalScore") or 0
        previous_score = previous.get("finalScore") or previous.get("overallScore") or 0
        
        # Ensure both are numbers
        if not isinstance(current_score, (int, float)):
            current_score = 0
        if not isinstance(previous_score, (int, float)):
            previous_score = 0
        
        score_change = current_score - previous_score
        
        return {
            "previousScore": previous_score,
            "currentScore": current_score,
            "scoreChange": round(score_change, 1),
            "trend": "up" if score_change > 0 else ("down" if score_change < 0 else "stable"),
            "previousGrade": previous.get("finalGrade"),
            "currentGrade": current.get("finalGrade"),
            "previousDate": previous.get("analysisCompletedAt"),
            "daysSinceLastAnalysis": self._days_between(
                previous.get("analysisCompletedAt"),
                current.get("analysisStartedAt")
            ),
        }
    
    def _days_between(self, date1: str, date2: str) -> int:
        """Calculate days between two ISO dates"""
        try:
            d1 = datetime.fromisoformat(date1.replace("Z", "+00:00"))
            d2 = datetime.fromisoformat(date2.replace("Z", "+00:00"))
            return abs((d2 - d1).days)
        except:
            return 0
    
    def _aggregate_all_metrics(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Tüm agent metriklerini birleştir"""
        aggregated = {}
        
        for agent_name, result in agent_results.items():
            if not isinstance(result, dict):
                continue
            
            metrics = result.get("metrics", {})
            for key, value in metrics.items():
                # Çakışan key'leri agent adıyla prefiksle
                if key in aggregated:
                    aggregated[f"{agent_name}_{key}"] = value
                else:
                    aggregated[key] = value
        
        return aggregated
    
    def _extract_swot(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Agent sonuçlarından SWOT analizi çıkar"""
        swot = {
            "strengths": [],
            "weaknesses": [],
            "opportunities": [],
            "threats": []
        }
        
        for agent_name, result in agent_results.items():
            if not isinstance(result, dict):
                continue
            
            # SWOT doğrudan result'ta olabilir
            if "swot" in result:
                agent_swot = result["swot"]
                for key in swot.keys():
                    if key in agent_swot and isinstance(agent_swot[key], list):
                        swot[key].extend(agent_swot[key])
            
            # Veya findings'den çıkarabiliriz
            findings = result.get("findings", [])
            for finding in findings:
                if isinstance(finding, dict):
                    f_type = finding.get("type", "").lower()
                    f_text = finding.get("finding", "")
                    
                    if "strength" in f_type or "positive" in f_type:
                        swot["strengths"].append(f_text)
                    elif "weakness" in f_type or "negative" in f_type:
                        swot["weaknesses"].append(f_text)
                    elif "opportunity" in f_type:
                        swot["opportunities"].append(f_text)
                    elif "threat" in f_type or "risk" in f_type:
                        swot["threats"].append(f_text)
        
        return swot


# Factory function
def create_pipeline_orchestrator(redis_client=None) -> NewPipelineOrchestrator:
    """Create a new pipeline orchestrator instance"""
    return NewPipelineOrchestrator(redis_client)
