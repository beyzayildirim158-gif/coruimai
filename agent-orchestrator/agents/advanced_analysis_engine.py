# Advanced Analysis Engine - Comprehensive Instagram Account Analysis
# Implements all 11 analysis modules from the system enhancement prompt
"""
Advanced Analysis Engine

Bu modül Instagram hesap analizinde gelişmiş tespit ve öneri sistemlerini uygular:
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
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Timeframe(Enum):
    IMMEDIATE = "immediate"
    SHORT_TERM = "1-2 weeks"
    MEDIUM_TERM = "1-3 months"
    LONG_TERM = "3-6 months"


@dataclass
class Finding:
    """Tek bir bulgu"""
    id: str
    category: str
    severity: RiskLevel
    title: str
    description: str
    evidence: List[str]
    metrics: Dict[str, Any]
    impact_score: int  # 0-100
    confidence: float  # 0-1
    rationale: str


@dataclass
class Recommendation:
    """Tek bir öneri"""
    id: str
    priority: int  # 1 = highest
    category: str
    action: str
    description: str
    expected_impact: str
    impact_score: int  # 0-100
    difficulty: Difficulty
    timeframe: Timeframe
    implementation_steps: List[str]
    rationale: str
    quick_win: bool = False


@dataclass
class AnalysisReport:
    """Tam analiz raporu"""
    report_id: str
    analysis_id: str
    generated_at: str
    account_username: str
    
    # Özet
    executive_summary: Dict[str, Any] = field(default_factory=dict)
    key_issues: List[str] = field(default_factory=list)
    overall_health_score: int = 0
    overall_grade: str = "F"
    
    # Detaylı bulgular
    findings: List[Finding] = field(default_factory=list)
    
    # Risk değerlendirmeleri
    risk_assessments: Dict[str, Any] = field(default_factory=dict)
    
    # Öncelikli öneriler
    recommendations: List[Recommendation] = field(default_factory=list)
    
    # Strateji önerileri
    content_strategy: Dict[str, Any] = field(default_factory=dict)
    growth_strategy: Dict[str, Any] = field(default_factory=dict)
    
    # İzleme ve takip
    monitoring_actions: List[Dict[str, Any]] = field(default_factory=list)
    
    # Veri kalitesi
    data_quality: Dict[str, Any] = field(default_factory=dict)


class AdvancedAnalysisEngine:
    """
    Gelişmiş Instagram Hesap Analiz Motoru
    
    Tüm agent sonuçlarını alır ve kapsamlı, yapılandırılmış bir analiz raporu üretir.
    """
    
    # Niche bazlı benchmark değerleri
    NICHE_BENCHMARKS = {
        "default": {
            "engagement_rate": {"avg": 2.5, "top_25": 4.0, "top_10": 6.0},
            "growth_rate": {"avg": 4.0, "top_25": 8.0, "top_10": 15.0},
            "save_rate": {"avg": 2.0, "top_25": 4.0},
            "comment_rate": {"avg": 0.05, "top_25": 0.10},
        },
        "shopping_deals": {
            "engagement_rate": {"avg": 2.5, "top_25": 3.5, "top_10": 5.0},
            "growth_rate": {"avg": 4.0, "top_25": 6.0, "top_10": 10.0},
            "save_rate": {"avg": 3.0, "top_25": 5.0},
            "comment_rate": {"avg": 0.03, "top_25": 0.06},
        },
        "lifestyle": {
            "engagement_rate": {"avg": 3.0, "top_25": 5.0, "top_10": 8.0},
            "growth_rate": {"avg": 5.0, "top_25": 10.0, "top_10": 20.0},
            "save_rate": {"avg": 2.5, "top_25": 4.5},
            "comment_rate": {"avg": 0.04, "top_25": 0.08},
        },
    }
    
    # Optimal içerik dağılımı
    OPTIMAL_CONTENT_MIX = {
        "educational": 40,
        "inspirational": 20,
        "entertaining": 15,
        "promotional": 10,
        "community": 15,
    }
    
    # Optimal format dağılımı
    OPTIMAL_FORMAT_MIX = {
        "reels": 45,
        "carousel": 30,
        "single_post": 15,
        "stories": 10,  # daily average
    }
    
    # Hashtag stratejisi
    OPTIMAL_HASHTAG_DISTRIBUTION = {
        "total": 25,
        "mega": 2,      # >10M posts
        "large": 4,     # 1M-10M posts
        "medium": 10,   # 100K-1M posts
        "small": 6,     # 10K-100K posts
        "micro": 3,     # <10K posts (niche specific)
    }
    
    def __init__(self):
        self.findings: List[Finding] = []
        self.recommendations: List[Recommendation] = []
        self.finding_counter = 0
        self.rec_counter = 0
    
    def analyze(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any],
        analysis_id: str,
    ) -> Dict[str, Any]:
        """
        Ana analiz fonksiyonu - tüm modülleri çalıştırır ve rapor üretir
        """
        self.findings = []
        self.recommendations = []
        self.finding_counter = 0
        self.rec_counter = 0
        
        username = account_data.get("username", "unknown")
        
        logger.info(f"Advanced analysis starting for @{username}")
        
        # 1. Bot ve Fake Follower Tespiti
        bot_analysis = self._analyze_bot_activity(account_data, agent_results)
        
        # 2. Engagement Rate Benchmarking
        engagement_analysis = self._analyze_engagement_benchmarks(account_data, agent_results)
        
        # 3. Bio ve İçerik Tutarlılık
        consistency_analysis = self._analyze_profile_consistency(account_data, agent_results)
        
        # 4. Hashtag Stratejisi
        hashtag_analysis = self._analyze_hashtag_strategy(account_data, agent_results)
        
        # 5. İçerik Formatı ve Büyüme Kanalları
        format_analysis = self._analyze_content_formats(account_data, agent_results)
        
        # 6. İçerik Kalitesi ve Dağılımı
        content_analysis = self._analyze_content_distribution(account_data, agent_results)
        
        # 7. Shadowban ve Algoritma Riski
        shadowban_analysis = self._analyze_shadowban_risk(account_data, agent_results)
        
        # 9. Viral Potansiyel
        viral_analysis = self._analyze_viral_potential(account_data, agent_results)
        
        # 11. Veri Kalitesi
        data_quality = self._assess_data_quality(account_data, agent_results)
        
        # Genel skor hesapla
        overall_score, overall_grade = self._calculate_overall_score(
            bot_analysis, engagement_analysis, consistency_analysis,
            hashtag_analysis, format_analysis, content_analysis,
            shadowban_analysis, viral_analysis
        )
        
        # Önerileri önceliklendir
        prioritized_recommendations = self._prioritize_recommendations()
        
        # Strateji önerileri oluştur
        content_strategy = self._generate_content_strategy(agent_results)
        growth_strategy = self._generate_growth_strategy(agent_results)
        
        # İzleme aksiyonları
        monitoring_actions = self._generate_monitoring_actions()
        
        # Yönetici özeti
        executive_summary = self._generate_executive_summary(
            username, overall_score, overall_grade,
            bot_analysis, engagement_analysis, shadowban_analysis
        )
        
        # Final rapor
        report = {
            "reportMetadata": {
                "reportId": f"advanced_analysis_{analysis_id[:8]}",
                "analysisId": analysis_id,
                "generatedAt": datetime.now().isoformat(),
                "version": "3.0",
                "reportType": "ADVANCED_COMPREHENSIVE_ANALYSIS",
                "engineVersion": "AdvancedAnalysisEngine v1.0"
            },
            
            "executiveSummary": executive_summary,
            
            "keyIssues": self._extract_key_issues(),
            
            "overallAssessment": {
                "healthScore": overall_score,
                "grade": overall_grade,
                "verdict": self._get_verdict(overall_grade),
                "confidenceLevel": data_quality.get("overall_confidence", 0.75)
            },
            
            "detailedFindings": {
                "botAndAuthenticity": bot_analysis,
                "engagementBenchmarks": engagement_analysis,
                "profileConsistency": consistency_analysis,
                "hashtagStrategy": hashtag_analysis,
                "contentFormats": format_analysis,
                "contentDistribution": content_analysis,
                "shadowbanRisk": shadowban_analysis,
                "viralPotential": viral_analysis
            },
            
            "riskAssessments": {
                "overallRiskLevel": self._calculate_overall_risk(),
                "botRisk": bot_analysis.get("risk_level", "unknown"),
                "shadowbanRisk": shadowban_analysis.get("risk_level", "unknown"),
                "algorithmPenaltyRisk": engagement_analysis.get("algorithm_penalty_risk", "unknown"),
                "accountSuspensionRisk": bot_analysis.get("suspension_risk", "low"),
                "riskFactors": self._compile_risk_factors()
            },
            
            "prioritizedRecommendations": {
                "quickWins": [r for r in prioritized_recommendations if r.get("quick_win")],
                "shortTerm": [r for r in prioritized_recommendations if r.get("timeframe") == "1-2 weeks"],
                "mediumTerm": [r for r in prioritized_recommendations if r.get("timeframe") == "1-3 months"],
                "longTerm": [r for r in prioritized_recommendations if r.get("timeframe") == "3-6 months"],
                "allRecommendations": prioritized_recommendations
            },
            
            "strategies": {
                "content": content_strategy,
                "growth": growth_strategy,
                "engagement": self._generate_engagement_strategy(agent_results),
                "community": self._generate_community_strategy(agent_results)
            },
            
            "monitoringAndFollowUp": {
                "keyMetricsToTrack": monitoring_actions,
                "reviewSchedule": self._generate_review_schedule(),
                "alertThresholds": self._generate_alert_thresholds()
            },
            
            "dataQuality": data_quality,
            
            "findings": [self._finding_to_dict(f) for f in self.findings],
            
            "actionPlan": self._generate_action_plan(prioritized_recommendations)
        }
        
        logger.info(f"Advanced analysis completed for @{username} - Score: {overall_score}/100 ({overall_grade})")
        
        return report
    
    # ==================== 1. Bot ve Fake Follower Tespiti ====================
    
    def _analyze_bot_activity(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Bot ve fake follower aktivitesi analizi"""
        
        system_gov = agent_results.get("systemGovernor", {})
        metrics = system_gov.get("metrics", {})
        detailed = system_gov.get("detailed_analysis", {})
        
        # Temel metrikler
        bot_score = detailed.get("bot_detection", {}).get("overall_bot_score", 50)
        authenticity_score = metrics.get("authenticityScore", 50)
        follower_quality = metrics.get("followerQualityScore", 50)
        engagement_auth = metrics.get("engagementAuthenticityScore", 50)
        
        # Takipçi analizi
        follower_analysis = detailed.get("follower_analysis", {})
        ghost_followers = follower_analysis.get("estimated_ghost_followers", "50")
        bot_followers = follower_analysis.get("estimated_bot_followers", "15")
        real_followers = follower_analysis.get("estimated_real_followers", "35")
        
        # Risk seviyesi belirleme
        risk_level = self._determine_bot_risk_level(bot_score, authenticity_score)
        
        # Şüpheli sinyaller
        suspicious_signals = detailed.get("bot_detection", {}).get("suspicious_signals", [])
        
        # Bulgular oluştur
        if bot_score > 50:
            self._add_finding(
                category="bot_detection",
                severity=RiskLevel.HIGH if bot_score > 70 else RiskLevel.MEDIUM,
                title="Yüksek Bot/Fake Takipçi Aktivitesi Tespit Edildi",
                description=f"Bot skoru {bot_score}/100 ile endişe verici seviyede. Tahmini bot takipçi oranı: {bot_followers}%, ghost takipçi oranı: {ghost_followers}%.",
                evidence=[
                    f"Bot skoru: {bot_score}/100",
                    f"Authenticity skoru: {authenticity_score}/100",
                    f"Tahmini gerçek takipçi: {real_followers}%",
                    *[s.get("signal", "") for s in suspicious_signals[:3]]
                ],
                metrics={
                    "bot_score": bot_score,
                    "authenticity_score": authenticity_score,
                    "ghost_percentage": ghost_followers,
                    "bot_percentage": bot_followers
                },
                impact_score=85 if bot_score > 70 else 70,
                confidence=0.85,
                rationale="Yüksek bot oranı algoritma cezasına, düşük erişime ve potansiyel hesap askıya alma riskine yol açar."
            )
            
            # Öneri ekle
            self._add_recommendation(
                priority=1,
                category="bot_cleanup",
                action="Acil Bot ve Ghost Takipçi Temizliği",
                description="Sahte ve etkileşimsiz takipçileri kaldırarak hesap sağlığını iyileştirin.",
                expected_impact="Engagement rate +50-100% artış, algoritma görünürlüğü iyileşmesi",
                impact_score=90,
                difficulty=Difficulty.MEDIUM,
                timeframe=Timeframe.IMMEDIATE,
                implementation_steps=[
                    "Takipçi listesini manuel veya araç ile inceleyin",
                    "Profil resmi olmayan, 0 gönderi olan hesapları engelleyin",
                    "Son 6 ayda hiç etkileşim yapmayan takipçileri kaldırın",
                    "Günde max 100-200 hesap temizliği yapın (spam algılanmasını önlemek için)",
                    "Bu işlemi 2-4 hafta boyunca sürdürün"
                ],
                rationale="Ghost ve bot takipçiler engagement rate'i düşürür, algoritma hesabınızı 'düşük kaliteli' olarak işaretler.",
                quick_win=False
            )
        
        # Engagement pod tespiti
        pod_detection = detailed.get("bot_detection", {}).get("pod_detection", {})
        pod_probability = pod_detection.get("probability", 0)
        
        if pod_probability > 0.3:
            self._add_finding(
                category="engagement_pod",
                severity=RiskLevel.MEDIUM,
                title="Engagement Pod Aktivitesi Şüphesi",
                description="Yorum ve beğeni zamanlamalarında şüpheli örüntüler tespit edildi.",
                evidence=[
                    f"Pod olasılığı: {pod_probability * 100:.0f}%",
                    f"Zamanlama korelasyonu: {pod_detection.get('timing_correlation', 'N/A')}",
                ],
                metrics={"pod_probability": pod_probability},
                impact_score=60,
                confidence=0.70,
                rationale="Engagement pod'ları kısa vadede engagement artırsa da algoritma tarafından tespit edilebilir."
            )
        
        return {
            "bot_score": bot_score,
            "authenticity_score": authenticity_score,
            "follower_quality_score": follower_quality,
            "engagement_authenticity_score": engagement_auth,
            "risk_level": risk_level.value,
            "follower_breakdown": {
                "real": real_followers,
                "ghost": ghost_followers,
                "bot": bot_followers
            },
            "suspicious_signals": suspicious_signals,
            "pod_detection": pod_detection,
            "suspension_risk": "high" if bot_score > 75 else ("medium" if bot_score > 50 else "low"),
            "cleanup_urgency": "immediate" if bot_score > 70 else ("soon" if bot_score > 50 else "optional")
        }
    
    def _determine_bot_risk_level(self, bot_score: float, authenticity_score: float) -> RiskLevel:
        """Bot risk seviyesi belirleme"""
        combined = (bot_score + (100 - authenticity_score)) / 2
        if combined > 70:
            return RiskLevel.HIGH
        elif combined > 50:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    # ==================== 2. Engagement Rate Benchmarking ====================
    
    def _analyze_engagement_benchmarks(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Engagement rate benchmark analizi"""
        
        # Hesap metrikleri
        followers = account_data.get("followers", 0)
        engagement_rate = float(account_data.get("engagementRate", 0) or 0)
        avg_likes = float(account_data.get("avgLikes", 0) or 0)
        avg_comments = float(account_data.get("avgComments", 0) or 0)
        
        # Niche belirleme
        domain_master = agent_results.get("domainMaster", {})
        niche = "default"
        if domain_master.get("rawResponse"):
            # Niche'i raw response'dan çıkarmaya çalış
            raw = domain_master.get("rawResponse", "")
            if "shopping" in raw.lower() or "deals" in raw.lower():
                niche = "shopping_deals"
            elif "lifestyle" in raw.lower():
                niche = "lifestyle"
        
        benchmarks = self.NICHE_BENCHMARKS.get(niche, self.NICHE_BENCHMARKS["default"])
        
        # Benchmark karşılaştırması
        er_benchmark = benchmarks["engagement_rate"]
        er_avg = er_benchmark["avg"]
        er_top_25 = er_benchmark["top_25"]
        
        # Performans hesaplama
        er_vs_avg = (engagement_rate / er_avg * 100) if er_avg > 0 else 0
        percentile = self._calculate_percentile(engagement_rate, er_benchmark)
        
        # Kritik düşük performans kontrolü
        is_critical = er_vs_avg < 10  # Benchmark'ın %10'undan az
        is_below_avg = engagement_rate < er_avg
        
        algorithm_penalty_risk = "low"
        if is_critical:
            algorithm_penalty_risk = "critical"
        elif er_vs_avg < 30:
            algorithm_penalty_risk = "high"
        elif er_vs_avg < 50:
            algorithm_penalty_risk = "medium"
        
        # Bulgu oluştur
        if is_critical:
            self._add_finding(
                category="engagement",
                severity=RiskLevel.CRITICAL,
                title="Kritik Düşük Engagement Rate",
                description=f"Engagement rate ({engagement_rate:.2f}%) niche ortalamasının ({er_avg}%) sadece %{er_vs_avg:.1f}'i. Bu kritik seviyede düşük.",
                evidence=[
                    f"Mevcut ER: {engagement_rate:.2f}%",
                    f"Niche ortalaması: {er_avg}%",
                    f"Top %25 eşiği: {er_top_25}%",
                    f"Performans: Benchmark'ın %{er_vs_avg:.1f}'i",
                    f"Percentile: Alt %{100 - percentile:.0f}"
                ],
                metrics={
                    "engagement_rate": engagement_rate,
                    "niche_average": er_avg,
                    "vs_benchmark_pct": er_vs_avg,
                    "percentile": percentile
                },
                impact_score=95,
                confidence=0.90,
                rationale="Bu kadar düşük engagement, algoritmanın içeriğinizi neredeyse hiç göstermediği anlamına gelir. Organik erişim pratik olarak sıfırdır."
            )
            
            self._add_recommendation(
                priority=1,
                category="engagement",
                action="Acil Engagement Kurtarma Planı",
                description="Engagement rate'i artırmak için kapsamlı strateji değişikliği gerekli.",
                expected_impact="ER %0.05'ten en az %0.5'e çıkarma (10x artış)",
                impact_score=95,
                difficulty=Difficulty.HARD,
                timeframe=Timeframe.MEDIUM_TERM,
                implementation_steps=[
                    "İçerik stratejisini tamamen gözden geçirin",
                    "Hook'ları güçlendirin - ilk 1 saniyede dikkat çekin",
                    "Soru sorarak etkileşimi teşvik edin",
                    "CTA'ları netleştirin",
                    "Posting zamanlarını optimize edin",
                    "Reels formatına ağırlık verin"
                ],
                rationale="Mevcut ER ile organik büyüme imkansız. Önce engagement düzeltilmeli.",
                quick_win=False
            )
        elif is_below_avg:
            self._add_finding(
                category="engagement",
                severity=RiskLevel.MEDIUM,
                title="Ortalamanın Altında Engagement Rate",
                description=f"Engagement rate ({engagement_rate:.2f}%) niche ortalamasının ({er_avg}%) altında.",
                evidence=[
                    f"Mevcut ER: {engagement_rate:.2f}%",
                    f"Niche ortalaması: {er_avg}%",
                    f"Fark: {er_avg - engagement_rate:.2f} puan"
                ],
                metrics={
                    "engagement_rate": engagement_rate,
                    "niche_average": er_avg,
                    "gap": er_avg - engagement_rate
                },
                impact_score=70,
                confidence=0.85,
                rationale="Ortalama altı engagement, içerik kalitesi veya kitle uyumsuzluğuna işaret eder."
            )
        
        return {
            "current_engagement_rate": engagement_rate,
            "niche": niche,
            "benchmarks": er_benchmark,
            "vs_average_pct": er_vs_avg,
            "percentile": percentile,
            "is_critical": is_critical,
            "is_below_average": is_below_avg,
            "algorithm_penalty_risk": algorithm_penalty_risk,
            "gap_to_average": max(0, er_avg - engagement_rate),
            "gap_to_top_25": max(0, er_top_25 - engagement_rate),
            "followers": followers,
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
            "like_to_follower_ratio": (avg_likes / followers * 100) if followers > 0 else 0
        }
    
    def _calculate_percentile(self, value: float, benchmarks: Dict[str, float]) -> float:
        """Değerin percentile'ını hesapla"""
        avg = benchmarks.get("avg", 2.5)
        top_25 = benchmarks.get("top_25", 4.0)
        top_10 = benchmarks.get("top_10", 6.0)
        
        if value >= top_10:
            return 95
        elif value >= top_25:
            return 75 + (value - top_25) / (top_10 - top_25) * 20
        elif value >= avg:
            return 50 + (value - avg) / (top_25 - avg) * 25
        else:
            return max(1, (value / avg) * 50)
    
    # ==================== 3. Bio ve İçerik Tutarlılık ====================
    
    def _analyze_profile_consistency(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Bio, profil ve içerik tutarlılık analizi"""
        
        bio = account_data.get("bio", "")
        username = account_data.get("username", "")
        
        # Domain Master'dan niche bilgisi
        domain_master = agent_results.get("domainMaster", {})
        raw_response = domain_master.get("rawResponse", "")
        
        # Tutarlılık sorunları tespit et
        consistency_issues = []
        consistency_score = 100
        
        # Bio anahtar kelimeleri
        bio_keywords = self._extract_keywords(bio.lower())
        
        # İçerik niche'i (domain master'dan)
        content_niche = "unknown"
        if "shopping" in raw_response.lower() or "deals" in raw_response.lower():
            content_niche = "shopping_deals"
        elif "art" in raw_response.lower():
            content_niche = "art"
        elif "lifestyle" in raw_response.lower():
            content_niche = "lifestyle"
        
        # Bio-İçerik uyumsuzluğu kontrolü
        bio_niche = "unknown"
        if any(kw in bio_keywords for kw in ["fiyat", "ucuz", "indirim", "karşılaştır"]):
            bio_niche = "shopping_deals"
        elif any(kw in bio_keywords for kw in ["sanat", "art", "çizim"]):
            bio_niche = "art"
        
        # Uyumsuzluk tespiti
        if bio_niche != "unknown" and content_niche != "unknown" and bio_niche != content_niche:
            consistency_issues.append({
                "type": "niche_mismatch",
                "bio_niche": bio_niche,
                "content_niche": content_niche,
                "severity": "high"
            })
            consistency_score -= 30
            
            self._add_finding(
                category="consistency",
                severity=RiskLevel.HIGH,
                title="Bio ve İçerik Niche Uyumsuzluğu",
                description=f"Bio '{bio_niche}' niche'ini işaret ederken içerik '{content_niche}' kategorisinde. Bu algoritma karışıklığına neden olur.",
                evidence=[
                    f"Bio anahtar kelimeleri: {', '.join(list(bio_keywords)[:5])}",
                    f"Tespit edilen bio niche: {bio_niche}",
                    f"Tespit edilen içerik niche: {content_niche}"
                ],
                metrics={
                    "consistency_score": consistency_score,
                    "bio_niche": bio_niche,
                    "content_niche": content_niche
                },
                impact_score=80,
                confidence=0.85,
                rationale="Algoritma, bio ve içerik arasındaki tutarsızlık nedeniyle hesabınızı doğru kategorize edemez ve keşif sayfasında göstermez."
            )
            
            self._add_recommendation(
                priority=2,
                category="profile_optimization",
                action="Bio ve Profil Tutarlılığını Sağlayın",
                description="Bio'yu içerik stratejinizle uyumlu hale getirin.",
                expected_impact="Keşif sayfası görünürlüğü +30-50%, doğru kitle çekimi",
                impact_score=80,
                difficulty=Difficulty.EASY,
                timeframe=Timeframe.IMMEDIATE,
                implementation_steps=[
                    "Bio'yu içerik niche'inizi net yansıtacak şekilde güncelleyin",
                    "Anahtar kelimeleri bio'ya ekleyin",
                    "Profil adını optimize edin (aranabilir kelimeler ekleyin)",
                    "Highlight'ları niche'e uygun düzenleyin"
                ],
                rationale="Net ve tutarlı bir profil, hem algoritmaya hem de ziyaretçilere hesabınızın ne hakkında olduğunu anlatır.",
                quick_win=True
            )
        
        # CTA eksikliği kontrolü
        has_cta = any(kw in bio.lower() for kw in ["link", "tıkla", "göz at", "profil", "dm", "ulaş"])
        if not has_cta:
            consistency_issues.append({
                "type": "missing_cta",
                "severity": "medium"
            })
            consistency_score -= 15
        
        return {
            "consistency_score": consistency_score,
            "issues": consistency_issues,
            "bio_analysis": {
                "length": len(bio),
                "has_emoji": any(ord(c) > 127 for c in bio),
                "has_cta": has_cta,
                "keywords": list(bio_keywords)[:10]
            },
            "niche_alignment": {
                "bio_niche": bio_niche,
                "content_niche": content_niche,
                "aligned": bio_niche == content_niche or bio_niche == "unknown" or content_niche == "unknown"
            }
        }
    
    def _extract_keywords(self, text: str) -> set:
        """Metinden anahtar kelimeler çıkar"""
        # Basit tokenizasyon
        words = text.replace(".", " ").replace(",", " ").replace("!", " ").split()
        # 3 karakterden uzun kelimeleri al
        return {w for w in words if len(w) > 3}
    
    # ==================== 4. Hashtag Stratejisi ====================
    
    def _analyze_hashtag_strategy(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Hashtag stratejisi analizi"""
        
        domain_master = agent_results.get("domainMaster", {})
        raw_response = domain_master.get("rawResponse", "")
        
        # Varsayılan değerler (gerçek veriden çekilemezse)
        current_strategy = {
            "avg_hashtags": 15,
            "distribution": {
                "mega": 5,
                "large": 5,
                "medium": 3,
                "small": 2,
                "micro": 0
            },
            "effectiveness_score": 40
        }
        
        # Raw response'dan hashtag bilgisi çıkarmaya çalış
        if "hashtag_analysis" in raw_response:
            try:
                import re
                hashtag_section = raw_response[raw_response.find("hashtag_analysis"):]
                # Basit parsing - gerçek implementasyonda daha gelişmiş olmalı
                if "avg_hashtags_per_post" in hashtag_section:
                    match = re.search(r'"avg_hashtags_per_post":\s*(\d+)', hashtag_section)
                    if match:
                        current_strategy["avg_hashtags"] = int(match.group(1))
            except:
                pass
        
        optimal = self.OPTIMAL_HASHTAG_DISTRIBUTION
        
        # Dağılım analizi
        distribution_issues = []
        
        # Mikro-niche hashtag eksikliği
        if current_strategy["distribution"]["micro"] == 0:
            distribution_issues.append({
                "issue": "missing_micro_niche",
                "impact": "high",
                "recommendation": "Mikro-niche hashtag'ler ekleyin (#ucuzurunara, #fiyatkarsilastirma gibi)"
            })
        
        # Mega hashtag fazlalığı
        if current_strategy["distribution"]["mega"] > 3:
            distribution_issues.append({
                "issue": "too_many_mega",
                "impact": "medium",
                "recommendation": "Mega hashtag sayısını 2-3'e düşürün, orta boy hashtag'lere ağırlık verin"
            })
        
        # Toplam hashtag sayısı
        total_hashtags = current_strategy["avg_hashtags"]
        if total_hashtags < 20:
            distribution_issues.append({
                "issue": "insufficient_hashtags",
                "impact": "medium",
                "recommendation": f"Hashtag sayısını {total_hashtags}'den 25'e çıkarın"
            })
        
        effectiveness_score = current_strategy["effectiveness_score"]
        
        if effectiveness_score < 50 or len(distribution_issues) > 1:
            self._add_finding(
                category="hashtag",
                severity=RiskLevel.MEDIUM,
                title="Etkisiz Hashtag Stratejisi",
                description=f"Hashtag etkinlik skoru {effectiveness_score}/100. Dağılım dengesiz ve mikro-niche hashtag'ler eksik.",
                evidence=[
                    f"Ortalama hashtag sayısı: {total_hashtags}",
                    f"Mega hashtag: {current_strategy['distribution']['mega']} (optimal: 2)",
                    f"Mikro-niche hashtag: {current_strategy['distribution']['micro']} (optimal: 3)",
                    *[d["recommendation"] for d in distribution_issues]
                ],
                metrics={
                    "effectiveness_score": effectiveness_score,
                    "current_distribution": current_strategy["distribution"],
                    "optimal_distribution": optimal
                },
                impact_score=65,
                confidence=0.80,
                rationale="Doğru hashtag stratejisi, içeriğinizi hedef kitlenize ulaştırmanın en önemli organik yollarından biridir."
            )
            
            self._add_recommendation(
                priority=4,
                category="hashtag",
                action="Hashtag Stratejisini Optimize Edin",
                description="Dengeli ve niche-odaklı hashtag dağılımı oluşturun.",
                expected_impact="Keşif erişimi +20-40%, hedef kitle ulaşımı iyileşmesi",
                impact_score=65,
                difficulty=Difficulty.EASY,
                timeframe=Timeframe.IMMEDIATE,
                implementation_steps=[
                    f"Toplam hashtag sayısını {optimal['total']}'e çıkarın",
                    f"Dağılım: Mega {optimal['mega']}, Large {optimal['large']}, Medium {optimal['medium']}, Small {optimal['small']}, Micro {optimal['micro']}",
                    "5 farklı hashtag seti oluşturun ve dönüşümlü kullanın",
                    "Niche-specific mikro hashtag'ler araştırın ve ekleyin",
                    "Her post için en alakalı seti seçin"
                ],
                rationale="Mikro-niche hashtag'ler daha az rekabet, daha hedefli kitle demektir.",
                quick_win=True
            )
        
        return {
            "current_strategy": current_strategy,
            "optimal_strategy": optimal,
            "effectiveness_score": effectiveness_score,
            "issues": distribution_issues,
            "recommendations": {
                "increase_to": optimal["total"],
                "add_micro_niche": True,
                "reduce_mega": current_strategy["distribution"]["mega"] > 3,
                "suggested_sets": self._generate_hashtag_sets(account_data)
            }
        }
    
    def _generate_hashtag_sets(self, account_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Örnek hashtag setleri oluştur"""
        return [
            {
                "name": "Fiyat Karşılaştırma Seti",
                "hashtags": ["#indirim", "#ucuz", "#fiyatkarsilastirma", "#akillalisveris", "#tasarruf",
                            "#kampanya", "#firsatlar", "#ucuzluk", "#alışveriş", "#evdekor",
                            "#mutfak", "#evurunleri", "#pratikurunler", "#enucuz", "#indirimlihayat"],
                "use_for": "Fiyat karşılaştırma içerikleri"
            },
            {
                "name": "Ürün İnceleme Seti",
                "hashtags": ["#uruninceme", "#alisveristavsiye", "#nerdenalınır", "#kaliteli",
                            "#fiyatperformans", "#test", "#karsilastirma", "#detayliinceleme",
                            "#kullanıcıyorumu", "#onerilenurunler"],
                "use_for": "Ürün inceleme ve değerlendirme içerikleri"
            }
        ]
    
    # ==================== 5. İçerik Formatı ve Büyüme Kanalları ====================
    
    def _analyze_content_formats(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """İçerik formatı ve büyüme kanalı analizi"""
        
        visual_brand = agent_results.get("visualBrand", {})
        format_analysis = visual_brand.get("format_analysis", {})
        
        current_mix = format_analysis.get("current_mix", {
            "reels": 0,
            "carousel": 0,
            "single_post": 100
        })
        
        optimal_mix = self.OPTIMAL_FORMAT_MIX
        
        # Format boşlukları tespit et
        format_gaps = []
        
        # Reels eksikliği
        reels_pct = current_mix.get("reels", 0)
        if reels_pct < 30:
            format_gaps.append({
                "format": "reels",
                "current": reels_pct,
                "optimal": optimal_mix["reels"],
                "gap": optimal_mix["reels"] - reels_pct,
                "priority": "critical" if reels_pct == 0 else "high"
            })
        
        # Carousel eksikliği
        carousel_pct = current_mix.get("carousel", 0)
        if carousel_pct < 20:
            format_gaps.append({
                "format": "carousel",
                "current": carousel_pct,
                "optimal": optimal_mix["carousel"],
                "gap": optimal_mix["carousel"] - carousel_pct,
                "priority": "high" if carousel_pct == 0 else "medium"
            })
        
        # Tek post fazlalığı
        single_pct = current_mix.get("single_post", 0)
        if single_pct > 30:
            format_gaps.append({
                "format": "single_post",
                "current": single_pct,
                "optimal": optimal_mix["single_post"],
                "excess": single_pct - optimal_mix["single_post"],
                "priority": "medium"
            })
        
        # Kritik format eksikliği bulgusu
        if reels_pct == 0:
            self._add_finding(
                category="content_format",
                severity=RiskLevel.HIGH,
                title="Kritik: Reels Formatı Hiç Kullanılmıyor",
                description="Hesapta hiç Reels içeriği yok. Reels, Instagram'ın en çok desteklediği ve en yüksek organik erişim sağlayan format.",
                evidence=[
                    f"Mevcut Reels oranı: {reels_pct}%",
                    f"Optimal Reels oranı: {optimal_mix['reels']}%",
                    "Reels, statik postlara göre 2-3x daha fazla erişim sağlar",
                    "Algoritma Reels'i keşif sayfasında öncelikli gösterir"
                ],
                metrics={
                    "current_reels_pct": reels_pct,
                    "optimal_reels_pct": optimal_mix["reels"],
                    "reach_multiplier": "2-3x"
                },
                impact_score=85,
                confidence=0.90,
                rationale="Reels olmadan organik büyüme çok zor. Algoritma video içeriği önceliklendirir."
            )
            
            self._add_recommendation(
                priority=2,
                category="content_format",
                action="Haftada 3-4 Reels Üretmeye Başlayın",
                description="Reels formatı ile organik erişimi ve büyümeyi artırın.",
                expected_impact="Organik erişim +100-300%, yeni takipçi kazanımı hızlanması",
                impact_score=90,
                difficulty=Difficulty.MEDIUM,
                timeframe=Timeframe.SHORT_TERM,
                implementation_steps=[
                    "Haftada minimum 3-4 Reels hedefleyin",
                    "İlk 1 saniyede dikkat çeken hook kullanın",
                    "Trend ses/müzikleri kullanın",
                    "15-30 saniye optimal uzunluk",
                    "Fiyat karşılaştırma, before/after, hızlı ipuçları formatları deneyin",
                    "Tutarlı posting saatleri belirleyin (akşam 19:00-22:00)"
                ],
                rationale="Reels, Instagram'ın en çok desteklediği format. Algoritma Reels'i keşifte önceliklendirir.",
                quick_win=False
            )
        
        # Interactive story eksikliği
        growth_virality = agent_results.get("growthVirality", {})
        channel_analysis = growth_virality.get("channel_analysis", {})
        
        return {
            "current_mix": current_mix,
            "optimal_mix": optimal_mix,
            "format_gaps": format_gaps,
            "deviation_score": format_analysis.get("deviation_score", 80),
            "recommendations": {
                "increase_reels": reels_pct < optimal_mix["reels"],
                "increase_carousel": carousel_pct < optimal_mix["carousel"],
                "reduce_single_post": single_pct > optimal_mix["single_post"],
                "weekly_targets": {
                    "reels": 4,
                    "carousel": 2,
                    "single_post": 1
                }
            },
            "growth_channels": {
                "reels": {"status": "unused" if reels_pct == 0 else "underutilized", "potential": 95},
                "explore": {"status": "underutilized", "potential": 90},
                "collaborations": {"status": "unused", "potential": 85},
                "hashtags": {"status": "suboptimal", "potential": 80}
            }
        }
    
    # ==================== 6. İçerik Kalitesi ve Dağılımı ====================
    
    def _analyze_content_distribution(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """İçerik kalitesi ve dağılım analizi"""
        
        domain_master = agent_results.get("domainMaster", {})
        raw_response = domain_master.get("rawResponse", "")
        
        # Varsayılan mevcut dağılım (gerçek veriden çekilemezse)
        current_distribution = {
            "educational": 10,
            "inspirational": 5,
            "entertaining": 70,
            "promotional": 10,
            "community": 5
        }
        
        # Raw response'dan içerik dağılımı çıkarmaya çalış
        if "content_pillar_analysis" in raw_response:
            try:
                import re
                # Basit regex ile değerleri çek
                for pillar in ["educational", "inspirational", "entertaining", "promotional", "community"]:
                    match = re.search(rf'"{pillar}":\s*(\d+)', raw_response)
                    if match:
                        current_distribution[pillar] = int(match.group(1))
            except:
                pass
        
        optimal = self.OPTIMAL_CONTENT_MIX
        
        # Dağılım analizi
        imbalances = []
        balance_score = 100
        
        for pillar, optimal_pct in optimal.items():
            current_pct = current_distribution.get(pillar, 0)
            diff = abs(current_pct - optimal_pct)
            
            if diff > 20:
                direction = "fazla" if current_pct > optimal_pct else "eksik"
                imbalances.append({
                    "pillar": pillar,
                    "current": current_pct,
                    "optimal": optimal_pct,
                    "diff": diff,
                    "direction": direction
                })
                balance_score -= diff // 2
        
        balance_score = max(0, balance_score)
        
        # Kritik dengesizlik bulgusu
        if balance_score < 50:
            self._add_finding(
                category="content_distribution",
                severity=RiskLevel.MEDIUM,
                title="İçerik Dağılımı Dengesiz",
                description=f"İçerik ayakları dengesi {balance_score}/100. Eğitici içerik %{current_distribution['educational']} (optimal %{optimal['educational']}), eğlence %{current_distribution['entertaining']} (optimal %{optimal['entertaining']}).",
                evidence=[
                    f"Eğitici içerik: {current_distribution['educational']}% (optimal: {optimal['educational']}%)",
                    f"Eğlence içerik: {current_distribution['entertaining']}% (optimal: {optimal['entertaining']}%)",
                    f"Topluluk içerik: {current_distribution['community']}% (optimal: {optimal['community']}%)",
                    *[f"{i['pillar']}: {i['diff']}% {i['direction']}" for i in imbalances]
                ],
                metrics={
                    "balance_score": balance_score,
                    "current_distribution": current_distribution,
                    "optimal_distribution": optimal
                },
                impact_score=70,
                confidence=0.80,
                rationale="Değer odaklı eğitici içerik, save rate ve uzun vadeli sadakat için kritiktir."
            )
            
            self._add_recommendation(
                priority=3,
                category="content_strategy",
                action="İçerik Dağılımını Yeniden Dengeleyin",
                description="Eğitici ve topluluk içeriğini artırın, aşırı eğlence/promosyonu azaltın.",
                expected_impact="Save rate +50%, topluluk bağlılığı artışı, algoritma favorisi olma",
                impact_score=75,
                difficulty=Difficulty.MEDIUM,
                timeframe=Timeframe.SHORT_TERM,
                implementation_steps=[
                    f"Eğitici içeriği {current_distribution['educational']}%'den {optimal['educational']}%'e çıkarın",
                    f"Eğlence içeriği {current_distribution['entertaining']}%'den {optimal['entertaining']}%'e düşürün",
                    "Her hafta en az 2 'nasıl yapılır' veya 'ipuçları' içeriği paylaşın",
                    "Topluluk etkileşimli içerikler ekleyin (soru-cevap, anket)",
                    "İçerik takvimi oluşturun ve ayak dağılımını takip edin"
                ],
                rationale="Eğitici içerik save edilir ve algoritma tarafından değerli kabul edilir.",
                quick_win=False
            )
        
        return {
            "current_distribution": current_distribution,
            "optimal_distribution": optimal,
            "balance_score": balance_score,
            "imbalances": imbalances,
            "recommendations": {
                "increase": [i["pillar"] for i in imbalances if i["direction"] == "eksik"],
                "decrease": [i["pillar"] for i in imbalances if i["direction"] == "fazla"],
                "weekly_content_mix": {
                    "educational": 3,
                    "inspirational": 1,
                    "entertaining": 1,
                    "promotional": 1,
                    "community": 1
                }
            }
        }
    
    # ==================== 7. Shadowban ve Algoritma Riski ====================
    
    def _analyze_shadowban_risk(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Shadowban ve algoritma risk analizi"""
        
        # 🚨 GUARD CLAUSE: Veri yoksa shadowban analizi yapma
        recent_posts = account_data.get("recentPosts", [])
        if not recent_posts or len(recent_posts) == 0:
            return {
                "risk_score": None,  # 0 veya 100 DEĞİL, None
                "risk_level": "UNKNOWN",
                "indicators": [],
                "description": "⚠️ Veri çekilemediği için Shadowban analizi yapılamadı. Bu bir hesap cezası değil, teknik bir veri erişim sorunudur.",
                "mitigation_strategies": [],
                "data_availability": False,
                "warning": "Post verisi alınamadı - Shadowban skorlaması mümkün değil"
            }
        
        system_gov = agent_results.get("systemGovernor", {})
        risk_assessment = system_gov.get("risk_assessment", {})
        shadowban_risk = risk_assessment.get("shadowban_risk", {})
        
        risk_score = shadowban_risk.get("score", 50)
        risk_level = shadowban_risk.get("level", "medium")
        indicators = shadowban_risk.get("indicators", [])
        
        # Ek risk faktörleri hesapla
        engagement_rate = float(account_data.get("engagementRate", 0) or 0)
        followers = account_data.get("followers", 0)
        
        additional_indicators = []
        
        # Çok düşük engagement
        if engagement_rate < 0.1:
            additional_indicators.append("Kritik düşük engagement rate")
            risk_score = min(100, risk_score + 20)
        
        # Bot aktivitesi
        bot_score = system_gov.get("detailed_analysis", {}).get("bot_detection", {}).get("overall_bot_score", 0)
        if bot_score > 60:
            additional_indicators.append("Yüksek bot aktivitesi")
            risk_score = min(100, risk_score + 15)
        
        all_indicators = indicators + additional_indicators
        
        # Risk seviyesi güncelle
        if risk_score > 75:
            final_risk_level = "high"
        elif risk_score > 50:
            final_risk_level = "medium"
        else:
            final_risk_level = "low"
        
        if final_risk_level == "high":
            self._add_finding(
                category="shadowban",
                severity=RiskLevel.HIGH,
                title="Yüksek Shadowban/Algoritma Cezası Riski",
                description=f"Shadowban risk skoru {risk_score}/100. Hesap algoritma tarafından cezalandırılıyor olabilir.",
                evidence=[
                    f"Risk skoru: {risk_score}/100",
                    *all_indicators[:5]
                ],
                metrics={
                    "risk_score": risk_score,
                    "risk_level": final_risk_level,
                    "indicators_count": len(all_indicators)
                },
                impact_score=85,
                confidence=0.75,
                rationale="Shadowban durumunda içerikleriniz keşifte görünmez, hashtag'lerden erişilmez olur."
            )
            
            self._add_recommendation(
                priority=1,
                category="shadowban_prevention",
                action="Shadowban Risk Azaltma Planı",
                description="Algoritma cezasını kaldırmak veya önlemek için acil adımlar.",
                expected_impact="Organik erişimin normale dönmesi, keşif görünürlüğü",
                impact_score=90,
                difficulty=Difficulty.MEDIUM,
                timeframe=Timeframe.IMMEDIATE,
                implementation_steps=[
                    "24-48 saat paylaşım yapmayın (hesap dinlendirme)",
                    "Bot/automation araçlarını devre dışı bırakın",
                    "Yasaklı veya spam hashtag'leri kullanmayı bırakın",
                    "Günlük like/yorum/takip limitlerini aşmayın",
                    "Düşük kaliteli/spam içerik paylaşmayın",
                    "Hesap güvenlik ayarlarını kontrol edin"
                ],
                rationale="Shadowban genellikle spam davranış veya TOS ihlalinden kaynaklanır.",
                quick_win=False
            )
        
        return {
            "risk_score": risk_score,
            "risk_level": final_risk_level,
            "indicators": all_indicators,
            "platform_risk": risk_assessment.get("platform_risk", {}),
            "account_standing": risk_assessment.get("account_standing", {}),
            "mitigation_strategies": [
                "Bot ve automation kullanımını durdurun",
                "Hashtag stratejisini gözden geçirin",
                "Posting sıklığını normalize edin",
                "Yüksek kaliteli, değer odaklı içerik üretin"
            ]
        }
    
    # ==================== 9. Viral Potansiyel ====================
    
    def _analyze_viral_potential(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Viral potansiyel analizi"""
        
        growth_virality = agent_results.get("growthVirality", {})
        viral_analysis = growth_virality.get("viral_analysis", {})
        attention_arch = agent_results.get("attentionArchitect", {})
        
        viral_coefficient = viral_analysis.get("viral_coefficient", 0)
        content_shareability = viral_analysis.get("content_shareability", 10)
        hook_effectiveness = attention_arch.get("metrics", {}).get("hookEffectivenessScore", 40)
        
        # Viral hazırlık skoru
        viral_readiness = (content_shareability + hook_effectiveness) / 2
        
        viral_opportunities = viral_analysis.get("viral_content_opportunities", [])
        
        if viral_readiness < 40:
            self._add_finding(
                category="viral_potential",
                severity=RiskLevel.MEDIUM,
                title="Düşük Viral Potansiyel",
                description=f"İçerik paylaşılabilirlik skoru {content_shareability}/100, hook etkinliği {hook_effectiveness}/100. Viral olma şansı düşük.",
                evidence=[
                    f"Viral katsayı: {viral_coefficient}",
                    f"Paylaşılabilirlik: {content_shareability}/100",
                    f"Hook etkinliği: {hook_effectiveness}/100"
                ],
                metrics={
                    "viral_coefficient": viral_coefficient,
                    "shareability": content_shareability,
                    "hook_effectiveness": hook_effectiveness,
                    "viral_readiness": viral_readiness
                },
                impact_score=60,
                confidence=0.70,
                rationale="Viral içerik, organik büyümenin en güçlü motorudur."
            )
            
            self._add_recommendation(
                priority=5,
                category="viral_strategy",
                action="Viral Potansiyeli Artırın",
                description="Hook'ları güçlendirin, paylaşılabilir içerik üretin.",
                expected_impact="Viral olma şansı +200-500%, organik erişim patlaması potansiyeli",
                impact_score=70,
                difficulty=Difficulty.HARD,
                timeframe=Timeframe.MEDIUM_TERM,
                implementation_steps=[
                    "İlk 0.5-1 saniyede güçlü hook kullanın",
                    "Merak uyandıran, şaşırtıcı bilgilerle başlayın",
                    "Trend ses ve formatları kullanın",
                    "Kaydetmeye değer, pratik değer sunun",
                    "Paylaşmayı teşvik eden CTA'lar ekleyin",
                    "'Arkadaşını etiketle' gibi paylaşım mekanizmaları kullanın"
                ],
                rationale="Viral içerik tek bir postla binlerce yeni takipçi getirebilir.",
                quick_win=False
            )
        
        return {
            "viral_coefficient": viral_coefficient,
            "content_shareability": content_shareability,
            "hook_effectiveness": hook_effectiveness,
            "viral_readiness_score": viral_readiness,
            "opportunities": viral_opportunities,
            "blueprints": growth_virality.get("viralLoopStrategy", {}).get("viralContentBlueprints", [])
        }
    
    # ==================== 11. Veri Kalitesi ====================
    
    def _assess_data_quality(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Veri kalitesi değerlendirmesi"""
        
        system_gov = agent_results.get("systemGovernor", {})
        validation = system_gov.get("validation", {})
        qa = system_gov.get("quality_assurance", {})
        
        # Veri tamlığı kontrolü
        required_fields = ["username", "followers", "following", "posts", "engagementRate"]
        present_fields = sum(1 for f in required_fields if account_data.get(f) is not None)
        completeness = present_fields / len(required_fields)
        
        # Agent sonuç kalitesi
        agent_count = len([k for k, v in agent_results.items() if v and not v.get("error")])
        total_agents = 8  # Beklenen agent sayısı
        agent_coverage = agent_count / total_agents
        
        # Genel güven skoru
        overall_confidence = (completeness * 0.4 + agent_coverage * 0.4 + 0.2)  # Base 0.2
        
        return {
            "overall_confidence": round(overall_confidence, 2),
            "data_completeness": round(completeness, 2),
            "agent_coverage": round(agent_coverage, 2),
            "data_freshness": validation.get("dataFreshness", "unknown"),
            "data_consistency": validation.get("dataConsistent", True),
            "anomalies_detected": validation.get("anomaliesDetected", False),
            "quality_checks": {
                "completeness": completeness >= 0.8,
                "consistency": validation.get("dataConsistent", True),
                "freshness": validation.get("dataFreshness") == "fresh",
                "accuracy": qa.get("checks", {}).get("accuracy") == "accurate"
            },
            "confidence_factors": [
                "Engagement rate hesaplama doğruluğu",
                "Takipçi kalite tahmini güvenilirliği",
                "Bot tespit algoritması kesinliği"
            ]
        }
    
    # ==================== Yardımcı Fonksiyonlar ====================
    
    def _add_finding(self, **kwargs) -> None:
        """Bulgu ekle"""
        self.finding_counter += 1
        finding = Finding(
            id=f"F{self.finding_counter:03d}",
            category=kwargs["category"],
            severity=kwargs["severity"],
            title=kwargs["title"],
            description=kwargs["description"],
            evidence=kwargs["evidence"],
            metrics=kwargs["metrics"],
            impact_score=kwargs["impact_score"],
            confidence=kwargs["confidence"],
            rationale=kwargs["rationale"]
        )
        self.findings.append(finding)
    
    def _add_recommendation(self, **kwargs) -> None:
        """Öneri ekle"""
        self.rec_counter += 1
        rec = Recommendation(
            id=f"R{self.rec_counter:03d}",
            priority=kwargs["priority"],
            category=kwargs["category"],
            action=kwargs["action"],
            description=kwargs["description"],
            expected_impact=kwargs["expected_impact"],
            impact_score=kwargs["impact_score"],
            difficulty=kwargs["difficulty"],
            timeframe=kwargs["timeframe"],
            implementation_steps=kwargs["implementation_steps"],
            rationale=kwargs["rationale"],
            quick_win=kwargs.get("quick_win", False)
        )
        self.recommendations.append(rec)
    
    def _finding_to_dict(self, finding: Finding) -> Dict[str, Any]:
        """Finding'i dictionary'e çevir"""
        return {
            "id": finding.id,
            "category": finding.category,
            "severity": finding.severity.value,
            "title": finding.title,
            "description": finding.description,
            "evidence": finding.evidence,
            "metrics": finding.metrics,
            "impactScore": finding.impact_score,
            "confidence": finding.confidence,
            "rationale": finding.rationale
        }
    
    def _recommendation_to_dict(self, rec: Recommendation) -> Dict[str, Any]:
        """Recommendation'ı dictionary'e çevir"""
        return {
            "id": rec.id,
            "priority": rec.priority,
            "category": rec.category,
            "action": rec.action,
            "description": rec.description,
            "expectedImpact": rec.expected_impact,
            "impactScore": rec.impact_score,
            "difficulty": rec.difficulty.value,
            "timeframe": rec.timeframe.value,
            "implementationSteps": rec.implementation_steps,
            "rationale": rec.rationale,
            "quick_win": rec.quick_win
        }
    
    def _calculate_overall_score(self, *analyses) -> Tuple[int, str]:
        """Genel skor ve not hesapla"""
        # Finding'lerin ağırlıklı ortalaması
        if not self.findings:
            return 70, "C"
        
        total_impact = sum(f.impact_score for f in self.findings)
        avg_impact = total_impact / len(self.findings)
        
        # Skor = 100 - ortalama impact (daha yüksek impact = daha büyük sorun)
        score = max(0, min(100, int(100 - avg_impact * 0.8)))
        
        # Kritik bulgular skoru düşürür
        critical_count = sum(1 for f in self.findings if f.severity == RiskLevel.CRITICAL)
        high_count = sum(1 for f in self.findings if f.severity == RiskLevel.HIGH)
        
        score -= critical_count * 10
        score -= high_count * 5
        score = max(0, score)
        
        # Not belirleme
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        return score, grade
    
    def _get_verdict(self, grade: str) -> str:
        """Not için değerlendirme"""
        verdicts = {
            "A": "MÜKEMMEL",
            "B": "İYİ",
            "C": "ORTA",
            "D": "ZAYIF",
            "F": "KRİTİK"
        }
        return verdicts.get(grade, "BİLİNMİYOR")
    
    def _prioritize_recommendations(self) -> List[Dict[str, Any]]:
        """Önerileri önceliklendirip dictionary listesi olarak döndür"""
        sorted_recs = sorted(self.recommendations, key=lambda r: (r.priority, -r.impact_score))
        return [self._recommendation_to_dict(r) for r in sorted_recs]
    
    def _extract_key_issues(self) -> List[str]:
        """Ana sorunları çıkar"""
        critical_findings = [f for f in self.findings if f.severity in [RiskLevel.CRITICAL, RiskLevel.HIGH]]
        return [f.title for f in sorted(critical_findings, key=lambda x: -x.impact_score)[:5]]
    
    def _calculate_overall_risk(self) -> str:
        """Genel risk seviyesi"""
        critical_count = sum(1 for f in self.findings if f.severity == RiskLevel.CRITICAL)
        high_count = sum(1 for f in self.findings if f.severity == RiskLevel.HIGH)
        
        if critical_count > 0:
            return "critical"
        elif high_count >= 3:
            return "high"
        elif high_count >= 1:
            return "medium"
        else:
            return "low"
    
    def _generate_executive_summary(
        self,
        username: str,
        overall_score: int,
        overall_grade: str,
        bot_analysis: Dict[str, Any],
        engagement_analysis: Dict[str, Any],
        shadowban_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Yönetici özeti oluştur"""
        
        # Kritik sorunlar
        critical_issues = []
        
        # Bot sorunu
        bot_score = bot_analysis.get("bot_score", 0)
        if bot_score > 50:
            fb = bot_analysis.get("follower_breakdown", {})
            critical_issues.append(
                f"Yüksek bot/fake takipçi oranı (Bot skoru: {bot_score}/100, tahmini gerçek takipçi: ~{fb.get('real', 35)}%)"
            )
        
        # Engagement sorunu
        if engagement_analysis.get("is_critical"):
            er = engagement_analysis.get("current_engagement_rate", 0)
            vs_avg = engagement_analysis.get("vs_average_pct", 0)
            critical_issues.append(
                f"Kritik düşük engagement rate ({er:.2f}%, benchmark'ın %{vs_avg:.1f}'i)"
            )
        
        # Shadowban riski
        sb_risk = shadowban_analysis.get("risk_level", "low")
        if sb_risk in ["high", "critical"]:
            critical_issues.append(
                f"Yüksek shadowban riski (skor: {shadowban_analysis.get('risk_score', 0)}/100)"
            )
        
        # Acil aksiyonlar
        immediate_actions = []
        for rec in self.recommendations:
            if rec.timeframe == Timeframe.IMMEDIATE:
                immediate_actions.append(rec.action)
        
        # Güçlü yönler (düşük severity bulguları veya yok)
        strengths = []
        if bot_score < 30:
            strengths.append("Takipçi kalitesi iyi")
        if not engagement_analysis.get("is_below_average"):
            strengths.append("Engagement rate ortalamanın üzerinde")
        if shadowban_analysis.get("risk_level") == "low":
            strengths.append("Düşük shadowban riski")
        
        return {
            "account": username,
            "healthScore": overall_score,
            "healthGrade": overall_grade,
            "verdict": self._get_verdict(overall_grade),
            "summaryText": self._generate_summary_text(username, overall_score, overall_grade, critical_issues),
            "criticalIssues": critical_issues,
            "keyStrengths": strengths if strengths else ["Analiz yapılıyor..."],
            "immediateActions": immediate_actions[:3] if immediate_actions else ["Öncelikli önerilere bakın"],
            "riskOverview": {
                "botRisk": bot_analysis.get("risk_level", "unknown"),
                "engagementRisk": "critical" if engagement_analysis.get("is_critical") else ("high" if engagement_analysis.get("is_below_average") else "low"),
                "shadowbanRisk": sb_risk,
                "overallRisk": self._calculate_overall_risk()
            },
            "quickStats": {
                "engagementRate": engagement_analysis.get("current_engagement_rate", 0),
                "vsNicheAverage": engagement_analysis.get("vs_average_pct", 0),
                "estimatedRealFollowers": bot_analysis.get("follower_breakdown", {}).get("real", "N/A"),
                "findingsCount": len(self.findings),
                "recommendationsCount": len(self.recommendations)
            }
        }
    
    def _generate_summary_text(
        self,
        username: str,
        score: int,
        grade: str,
        issues: List[str]
    ) -> str:
        """Özet metin oluştur"""
        verdict = self._get_verdict(grade)
        
        if grade == "F":
            return (
                f"@{username} hesabı kritik durumda (Skor: {score}/100, Not: {grade}). "
                f"{len(issues)} kritik sorun tespit edildi. Engagement rate çok düşük, "
                f"bot/fake takipçi oranı yüksek ve algoritma cezası riski var. "
                f"Acil müdahale gerekiyor."
            )
        elif grade == "D":
            return (
                f"@{username} hesabı zayıf durumda (Skor: {score}/100, Not: {grade}). "
                f"Önemli iyileştirmeler gerekiyor. {len(issues)} önemli sorun var."
            )
        elif grade == "C":
            return (
                f"@{username} hesabı orta seviyede (Skor: {score}/100, Not: {grade}). "
                f"Potansiyel var ancak geliştirilmesi gereken alanlar mevcut."
            )
        else:
            return (
                f"@{username} hesabı {verdict.lower()} durumda (Skor: {score}/100, Not: {grade}). "
                f"Genel performans tatmin edici."
            )
    
    def _compile_risk_factors(self) -> List[Dict[str, Any]]:
        """Risk faktörlerini derle"""
        return [
            {
                "factor": f.title,
                "severity": f.severity.value,
                "impact": f.impact_score
            }
            for f in sorted(self.findings, key=lambda x: -x.impact_score)[:10]
        ]
    
    def _generate_content_strategy(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """İçerik stratejisi oluştur"""
        return {
            "weeklyContentCalendar": {
                "monday": "Eğitici içerik - Nasıl yapılır/İpuçları",
                "tuesday": "Karşılaştırma Reels",
                "wednesday": "Topluluk içeriği - Soru-Cevap",
                "thursday": "Ürün inceleme Carousel",
                "friday": "Haftanın en iyi fırsatları",
                "saturday": "Kullanıcı içeriği paylaşımı",
                "sunday": "Haftalık özet + gelecek hafta önizleme"
            },
            "contentPillars": [
                {"pillar": "Fiyat Karşılaştırma", "percentage": 35},
                {"pillar": "Alışveriş İpuçları", "percentage": 30},
                {"pillar": "Ürün İncelemeleri", "percentage": 20},
                {"pillar": "Topluluk Etkileşimi", "percentage": 15}
            ],
            "formatMix": self.OPTIMAL_FORMAT_MIX,
            "postingTimes": {
                "optimal": ["19:00", "20:00", "21:00"],
                "secondary": ["12:00", "13:00"],
                "weekend": ["10:00", "11:00", "20:00"]
            }
        }
    
    def _generate_growth_strategy(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Büyüme stratejisi oluştur"""
        return {
            "phase1": {
                "name": "Temel Düzeltmeler",
                "duration": "1-2 hafta",
                "actions": [
                    "Bot/ghost takipçi temizliği başlat",
                    "Bio ve profili optimize et",
                    "Hashtag stratejisini yenile"
                ],
                "targetGrowth": "Engagement stabilizasyonu"
            },
            "phase2": {
                "name": "Format Çeşitlendirme",
                "duration": "2-4 hafta",
                "actions": [
                    "Reels üretimine başla (haftada 3-4)",
                    "Carousel içerik ekle",
                    "Story etkileşimlerini artır"
                ],
                "targetGrowth": "+1-2% aylık takipçi artışı"
            },
            "phase3": {
                "name": "Topluluk Oluşturma",
                "duration": "1-3 ay",
                "actions": [
                    "İşbirlikleri başlat",
                    "UGC kampanyası oluştur",
                    "Sadakat programı tasarla"
                ],
                "targetGrowth": "+3-5% aylık takipçi artışı"
            }
        }
    
    def _generate_engagement_strategy(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Engagement stratejisi"""
        return {
            "hooks": {
                "templates": [
                    "[Sayı] kişinin bilmediği [konu] sırrı",
                    "Bu [ürün] nereden almalı? (Cevap şaşırtacak)",
                    "[Marka A] vs [Marka B]: Hangisi daha iyi?"
                ],
                "principles": ["Merak uyandır", "Değer vaat et", "Şaşırt"]
            },
            "ctas": {
                "templates": [
                    "Bu bilgiyi kaydet!",
                    "Arkadaşını etiketle",
                    "Yorumlarda fikrini söyle"
                ]
            },
            "responseStrategy": {
                "targetResponseRate": "85%+",
                "responseTime": "1 saat içinde",
                "personalizedResponses": True
            }
        }
    
    def _generate_community_strategy(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Topluluk stratejisi"""
        return {
            "rituals": [
                {"name": "Haftalık Soru-Cevap", "frequency": "weekly", "day": "Çarşamba"},
                {"name": "Ayın Superfan'ı", "frequency": "monthly"}
            ],
            "ugcCampaigns": [
                {"hashtag": "#bununfiyatinedeneyim", "theme": "Kullanıcı deneyimleri"}
            ],
            "loyaltyProgram": {
                "tiers": ["Takipçi", "Aktif Üye", "Superfan"],
                "benefits": ["Erken erişim", "Özel indirimler", "Shoutout"]
            }
        }
    
    def _generate_monitoring_actions(self) -> List[Dict[str, Any]]:
        """İzleme aksiyonları"""
        return [
            {"metric": "Engagement Rate", "frequency": "weekly", "target": ">1%", "alert": "<0.5%"},
            {"metric": "Reach", "frequency": "weekly", "target": "+10% WoW", "alert": "-20% WoW"},
            {"metric": "Follower Growth", "frequency": "monthly", "target": "+2%", "alert": "negative"},
            {"metric": "Save Rate", "frequency": "weekly", "target": ">2%", "alert": "<1%"},
            {"metric": "Comment Rate", "frequency": "weekly", "target": ">0.05%", "alert": "<0.02%"}
        ]
    
    def _generate_review_schedule(self) -> Dict[str, Any]:
        """Gözden geçirme takvimi"""
        return {
            "daily": ["Story performance", "Comment response"],
            "weekly": ["Engagement metrics", "Content performance", "Hashtag effectiveness"],
            "monthly": ["Growth analysis", "Content strategy review", "Competitor check"],
            "quarterly": ["Full account audit", "Strategy revision"]
        }
    
    def _generate_alert_thresholds(self) -> Dict[str, Any]:
        """Uyarı eşikleri"""
        return {
            "engagement_rate": {"warning": 0.5, "critical": 0.1},
            "reach_drop": {"warning": -20, "critical": -50},
            "follower_loss": {"warning": -100, "critical": -500},
            "bot_score": {"warning": 50, "critical": 70}
        }
    
    def _generate_action_plan(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aksiyon planı oluştur"""
        immediate = [r for r in recommendations if r.get("timeframe") == "immediate"]
        short_term = [r for r in recommendations if r.get("timeframe") == "1-2 weeks"]
        medium_term = [r for r in recommendations if r.get("timeframe") == "1-3 months"]
        
        return {
            "immediate": {
                "timeframe": "Bu hafta",
                "actions": [r["action"] for r in immediate[:3]],
                "priority": "Kritik"
            },
            "shortTerm": {
                "timeframe": "1-2 hafta",
                "actions": [r["action"] for r in short_term[:3]],
                "priority": "Yüksek"
            },
            "mediumTerm": {
                "timeframe": "1-3 ay",
                "actions": [r["action"] for r in medium_term[:3]],
                "priority": "Orta"
            },
            "quickWins": [r["action"] for r in recommendations if r.get("quick_win")][:5]
        }


# ==================== Ana Çalıştırma Fonksiyonu ====================

def run_advanced_analysis(
    analysis_id: str,
    account_data: Dict[str, Any],
    agent_results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Gelişmiş analiz çalıştır
    
    Args:
        analysis_id: Analiz ID'si
        account_data: Hesap verileri
        agent_results: Agent sonuçları
    
    Returns:
        Kapsamlı analiz raporu
    """
    engine = AdvancedAnalysisEngine()
    return engine.analyze(account_data, agent_results, analysis_id)


if __name__ == "__main__":
    # Test için örnek kullanım
    import sys
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        account_data = data.get("accountOverview", {}).get("statistics", {})
        account_data["username"] = data.get("accountOverview", {}).get("username", "unknown")
        account_data["bio"] = data.get("accountOverview", {}).get("bio", "")
        
        agent_results = data.get("agentAnalyses", {})
        analysis_id = data.get("reportMetadata", {}).get("analysisId", "test")
        
        report = run_advanced_analysis(analysis_id, account_data, agent_results)
        
        print(json.dumps(report, indent=2, ensure_ascii=False))
