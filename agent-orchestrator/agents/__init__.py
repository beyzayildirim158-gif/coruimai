# =============================================================================
# Agents Package Init - Version 2.0
# Instagram AI Agent System
# =============================================================================

# Core Agents
from .base_agent import BaseAgent
from .orchestrator import AgentOrchestrator
from .system_governor import SystemGovernorAgent
from .growth_virality import GrowthViralityAgent
from .attention_architect import AttentionArchitectAgent
from .sales_conversion import SalesConversionAgent
from .community_loyalty import CommunityLoyaltyAgent
from .visual_brand import VisualBrandAgent
from .domain_master import DomainMasterAgent
from .content_strategist import ContentStrategistAgent
from .audience_dynamics import AudienceDynamicsAgent
from .content_plan_generator import ContentPlanGenerator

# Validation and Quality
from .metric_sanity_gates import MetricSanityGates, get_sanity_gates

# Pipeline and Orchestration
from .eli5_formatter import ELI5FormatterAgent
from .new_pipeline import NewPipelineOrchestrator, create_pipeline_orchestrator
from .deepseek_final_analyst import DeepSeekFinalAnalyst, create_deepseek_analyst
from .deepseek_fallback import DeepSeekFallback, get_deepseek_fallback, is_fallback_available
from .advanced_analysis_engine import AdvancedAnalysisEngine, run_advanced_analysis

# New v2.0 Modules
from .models import (
    AccountData,
    PostData,
    AgentFinding,
    AgentRecommendation,
    AgentResult,
    AnalysisResult,
    ELI5Report,
)
from .cot_prompting import (
    COT_ANALYSIS_TEMPLATE,
    OUTPUT_SCHEMA,
    validate_output_quality,
    SelfCorrectionEngine,
    calculate_viral_potential,
    predict_growth_trajectory,
)
from .llm_manager import (
    LLMManager,
    ModelType,
    ModelProvider,
    get_model_for_agent,
)
from .output_serializer import (
    OutputSerializer,
    serialize_analysis,
    score_to_grade,
)
from .structured_logger import (
    get_logger,
    LogContext,
    track_execution,
    log_agent_result,
    AgentError,
    LLMError,
    ValidationError,
    RateLimitError,
    ScrapingError,
    metrics,
)

# Instagram Data Acquisition
from .instagram_scraper import (
    InstagramDataAcquisitionAgent,
    ApifyClient,
    LoginScraper,
    AnalysisMode,
    DataSource,
    AcquisitionError,
    adjust_analysis_depth,
    create_agent_data_package,
    calculate_engagement_metrics,
    CompetitorConfig,
)

__all__ = [
    # Core Agents
    "BaseAgent",
    "AgentOrchestrator",
    "SystemGovernorAgent",
    "GrowthViralityAgent",
    "AttentionArchitectAgent",
    "SalesConversionAgent",
    "CommunityLoyaltyAgent",
    "VisualBrandAgent",
    "DomainMasterAgent",
    "ContentStrategistAgent",
    "AudienceDynamicsAgent",
    "ContentPlanGenerator",
    
    # Validation and Quality
    "MetricSanityGates",
    "get_sanity_gates",
    
    # Pipeline and Orchestration
    "ELI5FormatterAgent",
    "NewPipelineOrchestrator",
    "create_pipeline_orchestrator",
    "DeepSeekFinalAnalyst",
    "create_deepseek_analyst",
    "DeepSeekFallback",
    "get_deepseek_fallback",
    "is_fallback_available",
    "AdvancedAnalysisEngine",
    "run_advanced_analysis",
    
    # New v2.0 Modules - Data Models
    "AccountData",
    "PostData",
    "AgentFinding",
    "AgentRecommendation",
    "AgentResult",
    "AnalysisResult",
    "ELI5Report",
    
    # New v2.0 Modules - CoT Prompting
    "COT_ANALYSIS_TEMPLATE",
    "OUTPUT_SCHEMA",
    "validate_output_quality",
    "SelfCorrectionEngine",
    "calculate_viral_potential",
    "predict_growth_trajectory",
    
    # New v2.0 Modules - Multi-LLM
    "LLMManager",
    "ModelType",
    "ModelProvider",
    "get_model_for_agent",
    
    # New v2.0 Modules - Output Serializer
    "OutputSerializer",
    "serialize_analysis",
    "score_to_grade",
    
    # New v2.0 Modules - Structured Logger
    "get_logger",
    "LogContext",
    "track_execution",
    "log_agent_result",
    "AgentError",
    "LLMError",
    "ValidationError",
    "RateLimitError",
    "ScrapingError",
    "metrics",
    
    # Instagram Data Acquisition
    "InstagramDataAcquisitionAgent",
    "ApifyClient",
    "LoginScraper",
    "AnalysisMode",
    "DataSource",
    "AcquisitionError",
    "adjust_analysis_depth",
    "create_agent_data_package",
    "calculate_engagement_metrics",
    "CompetitorConfig",
]
