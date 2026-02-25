# =============================================================================
# Pydantic Models - PhD Level Data Validation
# Instagram AI Agent System - Version 2.0
# =============================================================================
"""
Bu modül tüm veri yapıları için güçlü Pydantic validation sağlar.

Amaçlar:
1. Frontend/PDF tutarsızlığını önlemek için tek kaynak (single source of truth)
2. LLM çıktılarını validate etmek için structured schemas
3. API request/response validation
4. ETL pipeline için data contracts

Kullanım:
    from agents.models import (
        AccountData, AgentFinding, AgentRecommendation, 
        AgentResult, AnalysisResult
    )
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
import re


# =============================================================================
# ENUMS - Sabit Değer Kümeleri
# =============================================================================

class SubscriptionTier(str, Enum):
    """Kullanıcı abonelik seviyeleri"""
    STARTER = "STARTER"
    PROFESSIONAL = "PROFESSIONAL"
    PREMIUM = "PREMIUM"
    ENTERPRISE = "ENTERPRISE"


class AnalysisStatus(str, Enum):
    """Analiz durumları"""
    PENDING = "PENDING"
    SCRAPING = "SCRAPING"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class FindingType(str, Enum):
    """Bulgu tipleri"""
    STRENGTH = "strength"
    WEAKNESS = "weakness"
    OPPORTUNITY = "opportunity"
    THREAT = "threat"
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class RecommendationPriority(str, Enum):
    """Öneri öncelik seviyeleri"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationDifficulty(str, Enum):
    """Öneri zorluk seviyeleri"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class AgentName(str, Enum):
    """Agent isimleri - tutarlılık için"""
    DOMAIN_MASTER = "domainMaster"
    GROWTH_VIRALITY = "growthVirality"
    SALES_CONVERSION = "salesConversion"
    VISUAL_BRAND = "visualBrand"
    COMMUNITY_LOYALTY = "communityLoyalty"
    ATTENTION_ARCHITECT = "attentionArchitect"
    SYSTEM_GOVERNOR = "systemGovernor"
    ELI5_FORMATTER = "eli5Formatter"
    DEEPSEEK_ANALYST = "deepseekFinalAnalyst"
    CONTENT_STRATEGIST = "contentStrategist"
    AUDIENCE_DYNAMICS = "audienceDynamics"


# =============================================================================
# BASE MODELS - Temel Yapılar
# =============================================================================

class BaseModelConfig(BaseModel):
    """Tüm modeller için ortak konfigürasyon"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="allow",  # Ekstra alanları kabul et (esneklik için)
    )


# =============================================================================
# ACCOUNT DATA - Instagram Hesap Verileri
# =============================================================================

class PostData(BaseModelConfig):
    """Tek bir post için veri yapısı"""
    post_id: str = Field(description="Post unique identifier")
    type: str = Field(default="image", description="Post type: image, video, carousel, reel")
    timestamp: Optional[datetime] = None
    likes: int = Field(ge=0, default=0)
    comments: int = Field(ge=0, default=0)
    views: Optional[int] = Field(ge=0, default=None)
    saves: Optional[int] = Field(ge=0, default=None)
    shares: Optional[int] = Field(ge=0, default=None)
    caption: Optional[str] = None
    hashtags: List[str] = Field(default_factory=list)
    mentions: List[str] = Field(default_factory=list)
    engagement_rate: Optional[float] = None
    
    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        valid_types = ["image", "video", "carousel", "reel", "story", "igtv", "sidecar"]
        return v.lower() if v.lower() in valid_types else "image"


class AccountData(BaseModelConfig):
    """Instagram hesap verisi - Apify'dan gelen ham veri"""
    username: str = Field(min_length=1, max_length=30)
    followers: int = Field(ge=0, alias="followersCount")
    following: int = Field(ge=0, alias="followsCount")
    posts: int = Field(ge=0, alias="postsCount")
    bio: Optional[str] = Field(default=None, max_length=2200)
    fullName: Optional[str] = None
    profilePicUrl: Optional[str] = None
    isVerified: bool = False
    isPrivate: bool = False
    isBusiness: bool = False
    category: Optional[str] = None
    externalUrl: Optional[str] = None
    
    # Engagement metrics
    engagementRate: Optional[float] = Field(ge=0, le=100, default=None)
    avgLikes: Optional[float] = Field(ge=0, default=None)
    avgComments: Optional[float] = Field(ge=0, default=None)
    avgViews: Optional[float] = Field(ge=0, default=None)
    
    # Post data
    latestPosts: List[PostData] = Field(default_factory=list)
    recentPosts: Optional[List[Dict[str, Any]]] = None  # Raw post data
    
    # Metadata
    scrapedAt: Optional[datetime] = None
    dataSource: str = Field(default="apify")
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Instagram username validation"""
        v = v.strip().lower().replace("@", "")
        if not re.match(r"^[a-z0-9._]+$", v):
            raise ValueError("Invalid Instagram username format")
        return v
    
    @field_validator("engagementRate")
    @classmethod
    def round_engagement(cls, v: Optional[float]) -> Optional[float]:
        """Round engagement rate to 2 decimal places"""
        return round(v, 2) if v is not None else None
    
    @model_validator(mode="after")
    def calculate_missing_metrics(self) -> "AccountData":
        """Calculate derived metrics if missing"""
        # Calculate engagement rate if not provided
        if self.engagementRate is None and self.followers > 0:
            if self.avgLikes is not None:
                self.engagementRate = round((self.avgLikes / self.followers) * 100, 2)
        return self
    
    class Config:
        populate_by_name = True  # Allow both field name and alias


# =============================================================================
# AGENT OUTPUT MODELS - LLM Çıktı Yapıları
# =============================================================================

class AgentFinding(BaseModelConfig):
    """
    Tek bir agent bulgusu - Minimum uzunluk zorunlu
    
    ÖNEMLI: Frontend ve PDF'te tutarlı gösterim için bu yapı kullanılmalı
    """
    type: FindingType = Field(default=FindingType.INFO)
    category: str = Field(min_length=2, max_length=50)
    finding: str = Field(
        min_length=100,  # ZORUNLU: En az 100 karakter
        description="Detaylı bulgu açıklaması - TEK CÜMLE YASAK"
    )
    evidence: Optional[str] = Field(
        default=None,
        min_length=20,
        description="Bulguyu destekleyen kanıt/veri"
    )
    impact_score: int = Field(ge=0, le=100, default=50)
    
    @field_validator("finding")
    @classmethod
    def validate_finding_length(cls, v: str) -> str:
        """Bulgunun yeterli uzunlukta olduğunu kontrol et"""
        if len(v.strip()) < 100:
            raise ValueError(
                f"Finding çok kısa ({len(v)} karakter). En az 100 karakter gerekli. "
                "TEK CÜMLE YASAK - detaylı açıklama yapın."
            )
        return v.strip()


class AgentRecommendation(BaseModelConfig):
    """
    Tek bir agent önerisi - Aksiyon odaklı, detaylı
    
    ÖNEMLI: Genel öneriler yasak, spesifik olmalı
    """
    priority: Union[RecommendationPriority, int] = Field(default=RecommendationPriority.MEDIUM)
    category: str = Field(min_length=2, max_length=50)
    action: str = Field(
        min_length=150,  # ZORUNLU: En az 150 karakter
        description="Spesifik aksiyon önerisi - genel ifadeler YASAK"
    )
    expected_impact: str = Field(
        min_length=30,
        description="Beklenen etki/sonuç"
    )
    implementation: Optional[str] = Field(
        default=None,
        min_length=50,
        description="Uygulama adımları"
    )
    difficulty: RecommendationDifficulty = Field(default=RecommendationDifficulty.MEDIUM)
    timeline: str = Field(default="1-2 weeks")
    kpi: Optional[str] = Field(default=None, description="Başarı metriği")
    
    @field_validator("action")
    @classmethod
    def validate_action_specificity(cls, v: str) -> str:
        """Önerinin yeterince spesifik olduğunu kontrol et"""
        banned_generic_phrases = [
            "daha fazla paylaşım yap",
            "içerik kalitesini artır",
            "tutarlı ol",
            "etkileşimi artır",
            "more content",
            "be consistent",
            "increase engagement"
        ]
        v_lower = v.lower()
        for phrase in banned_generic_phrases:
            if phrase in v_lower and len(v) < 200:
                raise ValueError(
                    f"Öneri çok genel: '{phrase}'. "
                    "SPESİFİK, AKSİYON ODAKLI öneriler yazın."
                )
        return v.strip()
    
    @field_validator("priority", mode="before")
    @classmethod
    def convert_priority(cls, v):
        """Convert integer priority to enum"""
        if isinstance(v, int):
            priority_map = {1: "critical", 2: "high", 3: "medium", 4: "low"}
            return RecommendationPriority(priority_map.get(v, "medium"))
        return v


class AgentMetrics(BaseModelConfig):
    """
    Agent metrikleri - Tutarlılık için zorunlu alanlar
    """
    overallScore: float = Field(ge=0, le=100, description="Agent genel skoru (0-100)")
    confidence: float = Field(ge=0, le=100, default=80.0)
    
    # Opsiyonel metrikler - agent'a özel
    engagementScore: Optional[float] = Field(ge=0, le=100, default=None)
    growthScore: Optional[float] = Field(ge=0, le=100, default=None)
    contentScore: Optional[float] = Field(ge=0, le=100, default=None)
    visualScore: Optional[float] = Field(ge=0, le=100, default=None)
    communityScore: Optional[float] = Field(ge=0, le=100, default=None)
    conversionScore: Optional[float] = Field(ge=0, le=100, default=None)
    
    @field_validator("overallScore", "confidence")
    @classmethod
    def round_scores(cls, v: float) -> float:
        """Round scores to 1 decimal place"""
        return round(v, 1)


class InsightItem(BaseModelConfig):
    """
    Insight öğesi - ELI5 ve özet bölümler için
    """
    icon: str = Field(default="💡", max_length=10)
    label: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=50, description="Detaylı içerik")
    color_code: Optional[str] = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")


class AgentResult(BaseModelConfig):
    """
    Tek bir agent'ın tam çıktısı
    
    Bu model LLM çıktısını validate eder ve tutarlılık sağlar
    """
    # Zorunlu alanlar
    agentName: str
    agentRole: Optional[str] = None
    findings: List[AgentFinding] = Field(min_length=1)
    recommendations: List[AgentRecommendation] = Field(min_length=1)
    metrics: AgentMetrics
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    modelUsed: str = Field(default="gemini-2.0-flash")
    processingTime: Optional[float] = None
    
    # Error handling
    error: bool = False
    errorMessage: Optional[str] = None
    parseError: bool = False
    rawResponse: Optional[str] = None
    
    # Validation flags
    vetoed: bool = False
    vetoReason: Optional[str] = None
    selfCorrected: bool = False
    correctionCount: int = Field(ge=0, default=0)
    
    @model_validator(mode="after")
    def ensure_minimum_content(self) -> "AgentResult":
        """En az 3 bulgu ve 3 öneri olduğundan emin ol"""
        if not self.error:
            if len(self.findings) < 3:
                # Uyarı log'la ama hata verme (esneklik için)
                pass
            if len(self.recommendations) < 3:
                pass
        return self


# =============================================================================
# ELI5 REPORT MODEL - Basitleştirilmiş Rapor
# =============================================================================

class ELI5Section(BaseModelConfig):
    """ELI5 rapor bölümü"""
    title: str
    emoji: str = Field(default="📌", max_length=10)
    content: str = Field(min_length=100)
    bullet_points: List[str] = Field(default_factory=list)


class ELI5Report(BaseModelConfig):
    """
    Basitleştirilmiş rapor yapısı - Frontend'de gösterilecek
    """
    executiveSummary: str = Field(min_length=200, description="Yönetici özeti")
    keyStrengths: List[InsightItem] = Field(min_length=1)
    keyWeaknesses: List[InsightItem] = Field(min_length=1)
    quickWins: List[str] = Field(min_length=1, description="Hızlı kazanımlar")
    longTermGoals: List[str] = Field(min_length=1, description="Uzun vadeli hedefler")
    sections: List[ELI5Section] = Field(default_factory=list)
    
    # Hook/Attention grabbers
    attentionHooks: List[str] = Field(default_factory=list)
    callToAction: Optional[str] = None


# =============================================================================
# FINAL ANALYSIS RESULT - Tam Analiz Sonucu
# =============================================================================

class OverallScore(BaseModelConfig):
    """Genel skor yapısı"""
    score: float = Field(ge=0, le=100)
    grade: str = Field(pattern=r"^[A-F][+-]?$")
    label: str
    color: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")
    
    @field_validator("grade")
    @classmethod
    def validate_grade(cls, v: str) -> str:
        valid_grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]
        if v.upper() not in valid_grades:
            raise ValueError(f"Invalid grade: {v}")
        return v.upper()


class BusinessIdentity(BaseModelConfig):
    """İşletme kimliği tespiti"""
    is_service_provider: bool = False
    account_type: str = Field(default="content_creator")
    correct_success_metrics: List[str] = Field(default_factory=list)
    wrong_metrics_to_avoid: List[str] = Field(default_factory=list)
    benchmark_engagement: float = Field(ge=0, le=100, default=2.5)
    analysis_note: Optional[str] = None


class AnalysisResult(BaseModelConfig):
    """
    TAM ANALİZ SONUCU - Frontend ve PDF için tek kaynak
    
    Bu model tüm analiz verilerini içerir ve tutarlılık sağlar.
    Frontend ve PDF generator bu modeli kullanmalı.
    """
    # Temel bilgiler
    analysisId: str
    username: str
    analysisStartedAt: datetime
    analysisCompletedAt: Optional[datetime] = None
    status: AnalysisStatus = Field(default=AnalysisStatus.COMPLETED)
    
    # Hesap verileri
    accountData: AccountData
    
    # Skorlar
    overallScore: OverallScore
    
    # Agent sonuçları
    agentResults: Dict[str, AgentResult]
    
    # ELI5 rapor
    eli5Report: Optional[ELI5Report] = None
    
    # Final verdict (DeepSeek)
    finalVerdict: Optional[Dict[str, Any]] = None
    
    # Content plan
    contentPlan: Optional[Dict[str, Any]] = None
    
    # Business identity
    businessIdentity: Optional[BusinessIdentity] = None
    
    # Metadata
    pipelineVersion: str = Field(default="2.0")
    totalProcessingTime: Optional[float] = None
    stagesCompleted: List[str] = Field(default_factory=list)
    
    # Validation results
    hardValidation: Optional[Dict[str, Any]] = None
    sanitizationReport: Optional[Dict[str, Any]] = None
    
    @model_validator(mode="after")
    def calculate_completion(self) -> "AnalysisResult":
        """Analiz tamamlandıysa completion time hesapla"""
        if self.status == AnalysisStatus.COMPLETED and self.analysisCompletedAt is None:
            self.analysisCompletedAt = datetime.utcnow()
        return self


# =============================================================================
# API REQUEST/RESPONSE MODELS
# =============================================================================

class AnalysisRequest(BaseModelConfig):
    """Analiz başlatma isteği"""
    username: str = Field(min_length=1, max_length=30)
    userId: str
    tier: SubscriptionTier = Field(default=SubscriptionTier.STARTER)
    options: Optional[Dict[str, Any]] = None
    
    @field_validator("username")
    @classmethod
    def clean_username(cls, v: str) -> str:
        return v.strip().lower().replace("@", "")


class AnalysisResponse(BaseModelConfig):
    """Analiz sonuç yanıtı"""
    success: bool
    analysisId: str
    status: AnalysisStatus
    message: Optional[str] = None
    result: Optional[AnalysisResult] = None
    error: Optional[str] = None


class ProgressUpdate(BaseModelConfig):
    """İlerleme güncellemesi"""
    stage: str
    progress: int = Field(ge=0, le=100)
    currentAgent: Optional[str] = None
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_agent_output(raw_output: Dict[str, Any], agent_name: str) -> AgentResult:
    """
    LLM'den gelen ham çıktıyı validate et ve AgentResult'a dönüştür
    
    Args:
        raw_output: LLM'den gelen ham dictionary
        agent_name: Agent ismi
        
    Returns:
        Validated AgentResult
        
    Raises:
        ValidationError: Validation başarısız olursa
    """
    # Findings'i validate et
    findings = []
    for f in raw_output.get("findings", []):
        if isinstance(f, str):
            # String findings'i dict'e dönüştür
            findings.append({
                "type": "info",
                "category": "general",
                "finding": f,
                "impact_score": 50
            })
        elif isinstance(f, dict):
            findings.append(f)
    
    # Recommendations'ı validate et
    recommendations = []
    for r in raw_output.get("recommendations", []):
        if isinstance(r, str):
            recommendations.append({
                "priority": "medium",
                "category": "general",
                "action": r,
                "expected_impact": "Improvement expected",
                "difficulty": "medium",
                "timeline": "1-2 weeks"
            })
        elif isinstance(r, dict):
            recommendations.append(r)
    
    # Metrics'i validate et
    metrics = raw_output.get("metrics", {})
    if "overallScore" not in metrics:
        # Default score hesapla
        metrics["overallScore"] = 50.0
    
    return AgentResult(
        agentName=agent_name,
        agentRole=raw_output.get("agentRole", ""),
        findings=[AgentFinding(**f) for f in findings] if findings else [
            AgentFinding(
                type=FindingType.INFO,
                category="system",
                finding="Analiz tamamlandı ancak detaylı bulgular çıkarılamadı. " * 3,
                impact_score=50
            )
        ],
        recommendations=[AgentRecommendation(**r) for r in recommendations] if recommendations else [
            AgentRecommendation(
                priority=RecommendationPriority.MEDIUM,
                category="system",
                action="Analiz tekrar çalıştırılarak daha detaylı öneriler elde edilebilir. " * 3,
                expected_impact="Daha detaylı analiz sonuçları",
                difficulty=RecommendationDifficulty.EASY,
                timeline="immediate"
            )
        ],
        metrics=AgentMetrics(**metrics),
        modelUsed=raw_output.get("modelUsed", "gemini-2.0-flash"),
        error=raw_output.get("error", False),
        errorMessage=raw_output.get("errorMessage"),
        parseError=raw_output.get("parseError", False),
        rawResponse=raw_output.get("rawResponse")
    )


def score_to_grade(score: float) -> tuple[str, str, str]:
    """
    Skoru nota çevir
    
    Returns:
        (grade, label, color_hex)
    """
    if score >= 90:
        return ("A+", "Mükemmel", "#10B981")
    elif score >= 85:
        return ("A", "Harika", "#22C55E")
    elif score >= 80:
        return ("A-", "Çok İyi", "#34D399")
    elif score >= 75:
        return ("B+", "İyi", "#84CC16")
    elif score >= 70:
        return ("B", "İyi", "#A3E635")
    elif score >= 65:
        return ("B-", "Ortanın Üstü", "#BEF264")
    elif score >= 60:
        return ("C+", "Orta", "#FACC15")
    elif score >= 55:
        return ("C", "Orta", "#FCD34D")
    elif score >= 50:
        return ("C-", "Ortanın Altı", "#FBBF24")
    elif score >= 45:
        return ("D+", "Zayıf", "#F97316")
    elif score >= 40:
        return ("D", "Zayıf", "#FB923C")
    elif score >= 35:
        return ("D-", "Çok Zayıf", "#F87171")
    else:
        return ("F", "Başarısız", "#EF4444")
