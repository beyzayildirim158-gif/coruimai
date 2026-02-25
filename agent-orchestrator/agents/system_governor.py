# System Governor Agent - PhD Level Implementation
# Data Validation, Bot Detection, Account Health Assessment, Cross-Validation
"""
System Governor Agent - PhD Level

Bu ajan veri doğrulama, bot tespiti, hesap sağlığı değerlendirmesi ve
çapraz doğrulama sistemlerini yönetir. Authenticity, bot risk, follower
quality, data consistency skorlarını hesaplar ve tüm agent sonuçlarını validate eder.
"""

from typing import Any, Dict, List, Optional, Tuple

from .base_agent import BaseAgent


class SystemGovernorAgent(BaseAgent):
    """
    System Governor Agent - PhD Level

    Uzmanlık Alanları:
    - Instagram veri yapısı ve güvenilirlik
    - Veri tutarlılık kontrolleri ve anomali tespiti
    - Bot ve fake follower tespit algoritmaları
    - Engagement pod tespiti
    - Hesap sağlığı değerlendirmesi
    - Shadowban ve risk tespiti
    - Çapraz doğrulama ve kalite güvencesi

    Metrikler:
    - Authenticity Score (0-100)
    - Bot Risk Level (low/medium/high)
    - Follower Quality Score (0-100)
    - Engagement Authenticity Score (0-100)
    - Data Consistency Score (0-100)
    - Overall Health Grade (A/B/C/D/F)
    
    GÖREV 2: Post-Process özellikleri:
    - Deduplication (tekilleştirme)
    - Anlamsız karakter temizliği
    - Boş liste varsayılan mesajı
    """

    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "System Governor"
        self.role = "Data Validation & Bot Detection Specialist"
        self.specialty = (
            "Data validation, bot detection, account health assessment, "
            "cross-validation, quality assurance"
        )

        # Initialize all knowledge bases
        self._init_data_reliability()
        self._init_consistency_rules()
        self._init_anomaly_framework()
        self._init_bot_taxonomy()
        self._init_bot_detection_algorithm()
        self._init_pod_detection()
        self._init_health_framework()
        self._init_shadowban_detection()
        self._init_growth_patterns()
        self._init_cross_validation()
        self._init_quality_assurance()
        self._init_scoring_models()
        self._init_edge_cases()

    # ---------------------- Knowledge Bases ----------------------
    def _init_data_reliability(self) -> None:
        """Veri güvenilirlik matrisi"""
        self.data_categories = {
            "profile_data": {"reliability": "high", "source": "api_scrape"},
            "metric_data": {"reliability": "high", "source": "real_time"},
            "engagement_data": {"reliability": "medium", "source": "sampling"},
            "derived_data": {"reliability": "variable", "source": "calculation"},
            "behavioral_data": {"reliability": "medium", "source": "observation"},
        }

        self.data_accuracy = {
            "follower_count": {"accuracy": 0.99, "freshness": "real_time"},
            "engagement_rate": {"accuracy": (0.85, 0.95), "freshness": "delayed"},
            "bot_score": {"accuracy": (0.70, 0.85), "freshness": "snapshot"},
            "growth_rate": {"accuracy": (0.80, 0.90), "freshness": "periodic"},
            "audience_demo": {"accuracy": (0.60, 0.80), "freshness": "inferred"},
        }

    def _init_consistency_rules(self) -> None:
        """Veri tutarlılık kuralları"""
        self.consistency_rules = {
            "follower_engagement_correlation": {
                "description": "Higher followers = lower ER%",
                "check": "er_within_niche_range",
                "red_flag": "very_high_er_with_high_followers",
            },
            "like_comment_ratio": {
                "expected_range": (50, 200),  # likes:comments
                "healthy_comment_pct": (0.02, 0.05),
                "red_flag_low": 0.01,
                "red_flag_high": 0.10,
            },
            "follower_following_balance": {
                "influencer": "followers >> following",
                "normal_tolerance": 0.50,
                "red_flag": "following >> followers",
            },
            "post_count_age": {
                "expected": "consistent_posting",
                "red_flag": "few_posts_many_followers",
            },
            "engagement_distribution": {
                "expected": "normal_distribution",
                "red_flag": "identical_engagement_numbers",
            },
        }

        self.consistency_penalties = {
            "minor": 5,
            "moderate": 15,
            "major": 30,
            "critical": 50,
        }

    def _init_anomaly_framework(self) -> None:
        """Anomali tespit framework"""
        self.anomaly_types = {
            "statistical": {
                "description": "Values outside 3σ",
                "detection": "z_score_analysis",
                "examples": ["sudden_metric_jumps", "impossible_values"],
            },
            "pattern": {
                "description": "Unnatural patterns",
                "detection": "pattern_matching",
                "examples": ["unnatural_growth", "timing_irregularities"],
            },
            "behavioral": {
                "description": "Unusual behavior",
                "detection": "behavioral_analysis",
                "examples": ["posting_unusual_hours", "activity_spikes"],
            },
            "relational": {
                "description": "Metric relationship breaks",
                "detection": "correlation_analysis",
                "examples": ["cross_metric_contradictions", "historical_inconsistencies"],
            },
        }

        self.anomaly_severity = {
            "low": (1, 3),
            "medium": (4, 6),
            "high": (7, 9),
            "critical": (10, 10),
        }

        self.anomaly_confidence = {
            "low": (0.3, 0.5),
            "medium": (0.5, 0.7),
            "high": (0.7, 0.9),
            "certain": (0.9, 1.0),
        }

        self.anomaly_thresholds = {
            "normal": (0, 10),
            "monitor": (11, 25),
            "warning": (26, 50),
            "alert": (51, 75),
            "critical": (76, 100),
        }

    def _init_bot_taxonomy(self) -> None:
        """Bot ve fake follower sınıflandırması"""
        self.bot_types = {
            "ghost_followers": {
                "characteristics": ["inactive", "no_engagement", "old_follows"],
                "detection_difficulty": "medium",
                "harm_level": "low_medium",
                "prevalence": (0.20, 0.40),
            },
            "purchased_bots": {
                "characteristics": ["fake_profiles", "no_content", "random_usernames", "stock_photos"],
                "detection_difficulty": "easy",
                "harm_level": "high",
                "prevalence": "variable",
            },
            "engagement_bots": {
                "characteristics": ["automated_engagement", "generic_comments", "timing_patterns"],
                "detection_difficulty": "medium",
                "harm_level": "high",
                "prevalence": (0.05, 0.15),
            },
            "sophisticated_bots": {
                "characteristics": ["ai_generated", "realistic_activity", "varied_engagement"],
                "detection_difficulty": "hard",
                "harm_level": "medium",
                "prevalence": (0.01, 0.05),
            },
            "follow_unfollow": {
                "characteristics": ["mass_following", "high_following_count", "low_engagement_given"],
                "detection_difficulty": "easy",
                "harm_level": "low",
                "prevalence": (0.10, 0.20),
            },
            "engagement_pods": {
                "characteristics": ["coordinated", "reciprocal", "timing_correlation"],
                "detection_difficulty": "medium_hard",
                "harm_level": "medium",
                "prevalence": (0.05, 0.10),
            },
        }

    def _init_bot_detection_algorithm(self) -> None:
        """Bot tespit algoritması"""
        self.profile_quality_weights = {
            "has_profile_pic": 15,
            "has_bio": 10,
            "bio_length_score": 10,
            "has_posts": 20,
            "post_count_score": 15,
            "account_age_score": 15,
            "has_highlights": 5,
            "username_quality": 10,
        }

        self.username_penalties = {
            "random_characters": -20,
            "excessive_numbers": -15,
            "no_vowels": -10,
            "very_long": -5,
            "normal": 0,
        }

        self.activity_pattern_weights = {
            "posting_consistency": 25,
            "engagement_given": 20,
            "story_activity": 15,
            "comment_quality": 20,
            "interaction_diversity": 20,
        }

        self.suspicious_activity_penalties = {
            "only_likes_no_comments": -15,
            "generic_comments_only": -20,
            "same_comment_repeated": -30,
            "exact_interval_engagement": -25,
            "burst_then_silence": -20,
        }

        self.suspicious_ratios = {
            "following_over_followers_5x": "high_bot_risk",
            "following_over_5000": "follow_unfollow_suspect",
            "followers_over_following_100x_small": "purchased",
            "both_very_low_old_account": "ghost",
        }

        self.engagement_auth_weights = {
            "like_timing_variance": 20,
            "comment_diversity": 25,
            "engagement_source_quality": 30,
            "engagement_growth_correlation": 25,
        }

        self.engagement_red_flags = [
            "likes_spike_first_5min_then_stop",
            "comments_from_no_post_accounts",
            "same_accounts_every_post",
            "engagement_doesnt_match_reach",
            "high_engagement_low_saves_shares",
        ]

        self.bot_score_weights = {
            "profile_quality": 0.25,
            "activity_score": 0.25,
            "ratio_score": 0.20,
            "engagement_auth": 0.30,
        }

        self.bot_score_interpretation = {
            "very_low_risk": (0, 20),
            "low_risk": (21, 40),
            "moderate_risk": (41, 60),
            "high_risk": (61, 80),
            "very_high_risk": (81, 100),
        }

    def _init_pod_detection(self) -> None:
        """Engagement pod tespit sistemi"""
        self.pod_characteristics = {
            "timing": ["engagement_1_5min", "consistent_timing", "stops_after_burst"],
            "source": ["same_accounts_repeatedly", "same_niche_network", "reciprocal_visible"],
            "content": ["generic_positive_comments", "similar_styles", "emoji_heavy"],
        }

        self.pod_weights = {
            "timing_correlation": 0.30,
            "source_repetition": 0.30,
            "comment_similarity": 0.20,
            "reciprocity_score": 0.20,
        }

        self.pod_thresholds = {
            "repeat_engager_flag": 0.30,  # >30% same accounts = flag
        }

        self.pod_risk_levels = {
            "none": (0, 25),
            "possible": (26, 50),
            "likely": (51, 75),
            "definite": (76, 100),
        }

    def _init_health_framework(self) -> None:
        """Hesap sağlığı değerlendirme framework"""
        self.health_dimensions = {
            "authenticity": {"weight": 0.30, "components": ["follower_quality", "engagement_auth", "growth_legitimacy"]},
            "engagement": {"weight": 0.25, "components": ["rate", "depth", "consistency"]},
            "content": {"weight": 0.20, "components": ["posting_consistency", "quality_signals", "diversity"]},
            "growth": {"weight": 0.15, "components": ["rate", "sustainability", "retention"]},
            "compliance": {"weight": 0.10, "components": ["policy_adherence", "shadowban_risk", "standing"]},
        }

        self.health_grades = {
            "A": (90, 100),
            "B": (80, 89),
            "C": (70, 79),
            "D": (60, 69),
            "F": (0, 59),
        }

    def _init_shadowban_detection(self) -> None:
        """Shadowban risk değerlendirmesi"""
        self.shadowban_high_risk = {
            "signals": ["reach_drop_50pct", "hashtag_reach_zero", "explore_reach_zero", "non_followers_cant_find"],
            "multiplier": 3.0,
        }

        self.shadowban_medium_risk = {
            "signals": ["gradual_reach_decline", "lower_hashtag_performance", "reduced_discovery"],
            "multiplier": 2.0,
        }

        self.shadowban_low_risk = {
            "signals": ["slight_reach_fluctuation", "algorithm_impact", "seasonal_variation"],
            "multiplier": 1.0,
        }

        self.shadowban_causes = {
            "content_violations": {"risk": "high", "examples": ["banned_hashtags", "reported", "copyright"]},
            "behavioral_violations": {"risk": "high", "examples": ["excessive_actions", "automation", "spam"]},
            "technical_issues": {"risk": "medium", "examples": ["third_party_apps", "suspicious_login", "vpn"]},
        }

        self.shadowban_risk_levels = {
            "low": (0, 20),
            "moderate": (21, 40),
            "elevated": (41, 60),
            "high": (61, 80),
            "critical": (81, 100),
        }

    def _init_growth_patterns(self) -> None:
        """Büyüme kalıpları analizi"""
        self.healthy_patterns = {
            "organic": {
                "description": "Gradual, consistent increase",
                "characteristics": ["content_correlation", "proportional_engagement", "natural_fluctuations"],
                "pattern": "logarithmic",
            },
            "viral": {
                "description": "Sudden spike from viral content",
                "characteristics": ["stabilization_after", "some_follower_loss_normal", "engagement_spike_normalize"],
                "pattern": "step_function",
            },
            "collaboration": {
                "description": "Spikes around collaborations",
                "characteristics": ["retention_varies", "new_audience_engagement"],
                "pattern": "periodic_spikes",
            },
        }

        self.suspicious_patterns = {
            "purchased_followers": {
                "indicators": ["sudden_large_increase", "no_content_correlation", "no_engagement_increase", "followed_by_drop"],
                "pattern": "vertical_spike",
            },
            "follow_unfollow": {
                "indicators": ["steady_growth", "high_following", "low_er", "churn_after_initial"],
                "pattern": "linear_hollow",
            },
            "bot_inflation": {
                "indicators": ["consistent_small_increases", "too_perfect_curve", "engagement_mismatch", "ghost_accumulation"],
                "pattern": "artificial_linear",
            },
        }

        self.growth_auth_weights = {
            "pattern_naturalness": 0.30,
            "engagement_correlation": 0.30,
            "retention_rate": 0.25,
            "source_diversity": 0.15,
        }

    def _init_cross_validation(self) -> None:
        """Çapraz doğrulama sistemi"""
        self.validation_types = {
            "internal_consistency": ["metrics_align", "findings_support_recommendations", "scores_justify_conclusions"],
            "cross_agent_consistency": ["metrics_agree", "no_contradictions", "recommendations_compatible"],
            "data_alignment": ["results_match_input", "calculations_verifiable", "assumptions_reasonable"],
            "reality_check": ["projections_realistic", "benchmarks_appropriate", "recommendations_achievable"],
        }

        self.validation_rules = {
            "metric_bounds": {"scores": (0, 100), "percentages": (0, 100)},
            "logical_consistency": {
                "high_bot_score": "low_authenticity",
                "low_engagement": "lower_monetization",
                "new_account": "limited_historical",
            },
        }

        self.metric_tolerance = {
            "score_metrics": 10,
            "percentage_metrics": 5,
            "rate_metrics": 20,
        }

        self.priority_hierarchy = ["raw_data", "calculated_metrics", "agent_analysis", "projections"]

        self.confidence_adjustments = {
            "minor_contradiction": -0.05,
            "moderate_contradiction": -0.10,
            "major_contradiction": -0.20,
            "data_quality_issue": -0.15,
            "minimum": 0.50,
        }

    def _init_quality_assurance(self) -> None:
        """Kalite güvence kontrolleri"""
        self.qa_checklist = {
            "data_completeness": ["all_required_fields", "no_null_values", "historical_available", "engagement_sufficient"],
            "data_freshness": ["timestamp_recent_24h", "current_state", "no_stale_cache"],
            "calculation_accuracy": ["formulas_correct", "rounding_appropriate", "edge_cases_handled"],
            "output_validity": ["json_correct", "all_fields_present", "values_in_range"],
            "recommendation_quality": ["actionable", "specific_to_account", "prioritized"],
        }

        self.qa_weights = {
            "completeness": 0.25,
            "freshness": 0.20,
            "accuracy": 0.25,
            "validity": 0.15,
            "recommendation_quality": 0.15,
        }

        self.qa_thresholds = {
            "production_ready": (90, 100),
            "acceptable_with_notes": (75, 89),
            "review_required": (60, 74),
            "reject_reprocess": (0, 59),
        }
        
        # =============================================================
        # SERT VALİDASYON KURALLARI (Chief Truth & Rigor Architect)
        # =============================================================
        self.hard_validation_rules = {
            # Kural 1: Düşük etkileşim = SWOT'ta güçlü yön YOK
            "engagement_strength_rule": {
                "condition": "engagement_rate < 1.0",
                "action": "remove_from_swot_strengths",
                "message": "Engagement <%1 = SWOT'ta 'Güçlü Yön' yazılamaz. Hiçbir 'strengths' girmeni istemiyorum.",
                "severity": "critical"
            },
            
            # Kural 2: Düşük trust = Maksimum skor sınırı
            "trust_score_ceiling_rule": {
                "condition": "trust_score < 50",
                "action": "cap_overall_score_at_60",
                "message": "Trust Score <50 = Genel skor maximum %60. Güvenilirlik düşükse başarı skoru yükselemez.",
                "severity": "critical"
            },
            
            # Kural 3: Görsel kaos = Grid skoru düşür
            "visual_chaos_grid_rule": {
                "condition": "visual_chaos_score > 70",
                "action": "cap_grid_score_at_40",
                "message": "Visual Chaos >70 = Grid skoru maximum 40. Kaotik görünüm = düşük grid kalitesi.",
                "severity": "major"
            },
            
            # Kural 4: Bot riski yüksek = Authenticity skoru düşür
            "bot_risk_authenticity_rule": {
                "condition": "bot_risk_score > 60",
                "action": "cap_authenticity_at_40",
                "message": "Bot Risk >60 = Authenticity maksimum 40. Bot takipçi = sahte hesap.",
                "severity": "critical"
            },
            
            # Kural 5: Posting tutarsızlık = Content stratejisi zayıf
            "posting_consistency_rule": {
                "condition": "posting_frequency_std > 5",
                "action": "mark_content_strategy_weak",
                "message": "Posting tutarsız (std>5 gün) = Content stratejisi 'Zayıf' olarak işaretle.",
                "severity": "major"
            },
            
            # Kural 6: Follower/Following oranı anormal = Red flag
            "follower_ratio_rule": {
                "condition": "following > followers * 2",
                "action": "add_red_flag_follow_unfollow",
                "message": "Following > 2x Followers = Follow/Unfollow taktiği kullanıyor. Red flag ekle.",
                "severity": "major"
            },
            
            # Kural 7: Growth rate çok yüksek = Satın alınmış olabilir
            "growth_rate_rule": {
                "condition": "monthly_growth_rate > 50",
                "action": "flag_potential_purchased_followers",
                "message": "Aylık büyüme >%50 = Muhtemelen satın alınmış takipçi. Investigate et.",
                "severity": "major"
            },
            
            # Kural 8: Like/Comment oranı anormal = Pod kullanımı
            "like_comment_ratio_rule": {
                "condition": "likes_per_comment > 200 or likes_per_comment < 20",
                "action": "flag_pod_or_bot_usage",
                "message": "Like/Comment oranı anormal = Pod veya bot kullanımı şüphesi.",
                "severity": "moderate"
            }
        }
        
        # Validation sonuç mesajları
        self.validation_failure_messages = {
            "engagement_too_low": "❌ SERT KURAL: Etkileşim oranı %{value} - sektör ortalamasının altında. SWOT'ta güçlü yön YAZILAMAZ.",
            "trust_too_low": "❌ SERT KURAL: Güvenilirlik skoru {value}/100 - genel skor %60'ı geçemez.",
            "visual_chaos": "❌ SERT KURAL: Görsel kaos skoru {value}/100 - grid kalitesi 40'ı geçemez.",
            "bot_risk_high": "❌ SERT KURAL: Bot riski %{value} - hesap güvenilirliği sorgulanır.",
            "follow_unfollow": "❌ SERT KURAL: Following/Followers oranı {value} - manipülatif büyüme stratejisi.",
            "purchased_followers": "❌ SERT KURAL: Aylık büyüme %{value} - organik değil.",
            "pod_detected": "❌ SERT KURAL: Engagement pod kullanımı tespit edildi."
        }

    def _init_scoring_models(self) -> None:
        """Puanlama model konfigürasyonları"""
        self.authenticity_weights = {
            "follower_quality": 0.30,
            "engagement_authenticity": 0.30,
            "growth_legitimacy": 0.25,
            "profile_authenticity": 0.15,
        }

        self.authenticity_interpretation = {
            "highly_authentic": (90, 100),
            "authentic": (75, 89),
            "mostly_authentic": (60, 74),
            "questionable": (45, 59),
            "likely_inauthentic": (30, 44),
            "highly_inauthentic": (0, 29),
        }

        self.follower_quality_weights = {
            "real": 0.35,
            "active": 0.30,
            "relevant": 0.20,
            "engaged": 0.15,
        }

        self.follower_quality_benchmarks = {
            "excellent": (85, 100),
            "good": (70, 84),
            "average": (55, 69),
            "below_average": (40, 54),
            "poor": (0, 39),
        }

    def _init_edge_cases(self) -> None:
        """Edge case tanımları ve confidence ayarlamaları"""
        self.edge_cases = {
            "new_account": {
                "threshold_months": 3,
                "confidence_adjustment": -0.20,
                "min_confidence": 0.60,
                "strategy": "conservative_scoring",
            },
            "viral_growth": {
                "threshold_growth_rate": 0.50,
                "confidence_adjustment": -0.15,
                "min_confidence": 0.65,
                "strategy": "context_aware",
            },
            "celebrity_verified": {
                "confidence_adjustment": -0.10,
                "min_confidence": 0.70,
                "strategy": "celebrity_thresholds",
            },
            "obvious_bots": {
                "confidence_adjustment": -0.30,
                "min_confidence": 0.50,
                "strategy": "flag_immediately",
            },
            "pod_detected": {
                "confidence_adjustment": -0.15,
                "min_confidence": 0.65,
                "strategy": "discount_pod_engagement",
            },
            "shadowbanned": {
                "confidence_adjustment": -0.25,
                "min_confidence": 0.55,
                "strategy": "resolve_first",
            },
            "incomplete_data": {
                "confidence_adjustment": -0.20,
                "min_confidence": 0.60,
                "strategy": "confidence_adjustment",
            },
            "regional_account": {
                "confidence_adjustment": -0.10,
                "min_confidence": 0.70,
                "strategy": "localized_thresholds",
            },
        }

    # ---------------------- Calculations ----------------------
    def calculate_consistency_score(self, violations: List[Dict[str, Any]]) -> float:
        """Calculate data consistency score"""
        score = 100.0
        for violation in violations:
            severity = violation.get("severity", "minor")
            penalty = self.consistency_penalties.get(severity, 5)
            score -= penalty
        return max(0, score)

    def calculate_anomaly_score(self, anomalies: List[Dict[str, Any]]) -> float:
        """Calculate total anomaly score"""
        score = 0.0
        for anomaly in anomalies:
            severity = anomaly.get("severity", 1)
            confidence = anomaly.get("confidence", 0.5)
            score += severity * confidence
        return min(100, score)

    def get_anomaly_alert_level(self, score: float) -> str:
        """Get anomaly alert level from score"""
        for level, (low, high) in self.anomaly_thresholds.items():
            if low <= score <= high:
                return level
        return "critical"

    def calculate_bot_score(
        self,
        profile_quality: float,
        activity_score: float,
        ratio_score: float,
        engagement_auth: float,
    ) -> float:
        """Calculate composite bot score (0-100, higher = more bot risk)"""
        w = self.bot_score_weights
        authenticity = (
            profile_quality * w["profile_quality"]
            + activity_score * w["activity_score"]
            + ratio_score * w["ratio_score"]
            + engagement_auth * w["engagement_auth"]
        )
        return max(0, min(100, 100 - authenticity))

    def get_bot_risk_level(self, bot_score: float) -> str:
        """Get bot risk level from score"""
        if bot_score <= 30:
            return "low"
        elif bot_score <= 60:
            return "medium"
        return "high"

    def calculate_pod_probability(
        self,
        timing_correlation: float,
        source_repetition: float,
        comment_similarity: float,
        reciprocity_score: float,
    ) -> float:
        """Calculate engagement pod probability"""
        w = self.pod_weights
        return (
            timing_correlation * w["timing_correlation"]
            + source_repetition * w["source_repetition"]
            + comment_similarity * w["comment_similarity"]
            + reciprocity_score * w["reciprocity_score"]
        )

    def get_pod_risk_level(self, probability: float) -> str:
        """Get pod risk level from probability"""
        for level, (low, high) in self.pod_risk_levels.items():
            if low <= probability <= high:
                return level
        return "definite"

    def calculate_authenticity_score(
        self,
        follower_quality: float,
        engagement_auth: float,
        growth_legitimacy: float,
        profile_auth: float,
    ) -> float:
        """Calculate overall authenticity score"""
        w = self.authenticity_weights
        return (
            follower_quality * w["follower_quality"]
            + engagement_auth * w["engagement_authenticity"]
            + growth_legitimacy * w["growth_legitimacy"]
            + profile_auth * w["profile_authenticity"]
        )

    def get_authenticity_level(self, score: float) -> str:
        """Get authenticity level from score"""
        for level, (low, high) in self.authenticity_interpretation.items():
            if low <= score <= high:
                return level
        return "highly_inauthentic"

    def calculate_follower_quality_score(
        self,
        real_pct: float,
        active_pct: float,
        relevant_pct: float,
        engaged_pct: float,
    ) -> float:
        """Calculate follower quality score"""
        w = self.follower_quality_weights
        return (
            real_pct * w["real"]
            + active_pct * w["active"]
            + relevant_pct * w["relevant"]
            + engaged_pct * w["engaged"]
        ) * 100

    def calculate_health_score(
        self,
        authenticity: float,
        engagement_health: float,
        content_health: float,
        growth_health: float,
        compliance: float,
    ) -> float:
        """Calculate overall health score"""
        dims = self.health_dimensions
        return (
            authenticity * dims["authenticity"]["weight"]
            + engagement_health * dims["engagement"]["weight"]
            + content_health * dims["content"]["weight"]
            + growth_health * dims["growth"]["weight"]
            + compliance * dims["compliance"]["weight"]
        )

    def get_health_grade(self, score: float) -> str:
        """Get health grade from score"""
        for grade, (low, high) in self.health_grades.items():
            if low <= score <= high:
                return grade
        return "F"

    def calculate_shadowban_risk(self, indicators: List[Dict[str, Any]]) -> float:
        """Calculate shadowban risk score"""
        score = 0.0
        for indicator in indicators:
            severity = indicator.get("severity", 1)
            confidence = indicator.get("confidence", 0.5)
            multiplier = indicator.get("multiplier", 1.0)
            score += severity * confidence * multiplier
        return min(100, score)

    def get_shadowban_risk_level(self, score: float) -> str:
        """Get shadowban risk level from score"""
        for level, (low, high) in self.shadowban_risk_levels.items():
            if low <= score <= high:
                return level
        return "critical"

    def calculate_growth_authenticity(
        self,
        pattern_naturalness: float,
        engagement_correlation: float,
        retention_rate: float,
        source_diversity: float,
    ) -> float:
        """Calculate growth authenticity score"""
        w = self.growth_auth_weights
        return (
            pattern_naturalness * w["pattern_naturalness"]
            + engagement_correlation * w["engagement_correlation"]
            + retention_rate * w["retention_rate"]
            + source_diversity * w["source_diversity"]
        )

    def calculate_qa_score(
        self,
        completeness: float,
        freshness: float,
        accuracy: float,
        validity: float,
        recommendation_quality: float,
    ) -> float:
        """Calculate QA score"""
        w = self.qa_weights
        return (
            completeness * w["completeness"]
            + freshness * w["freshness"]
            + accuracy * w["accuracy"]
            + validity * w["validity"]
            + recommendation_quality * w["recommendation_quality"]
        )

    def get_qa_status(self, score: float) -> str:
        """Get QA status from score"""
        for status, (low, high) in self.qa_thresholds.items():
            if low <= score <= high:
                return status
        return "reject_reprocess"

    def adjust_confidence(self, base_confidence: float, issues: List[str]) -> float:
        """Adjust confidence based on issues"""
        confidence = base_confidence
        for issue in issues:
            adjustment = self.confidence_adjustments.get(issue, 0)
            confidence += adjustment
        return max(self.confidence_adjustments["minimum"], confidence)

    def detect_edge_case(self, account_data: Dict[str, Any]) -> str:
        """Detect special edge cases"""
        followers = account_data.get("followers", 0) or 0
        account_age_months = account_data.get("account_age_months", 12)
        growth_rate = account_data.get("recent_growth_rate", 0)
        is_verified = account_data.get("verified", False)
        bot_score = account_data.get("bot_score", 0)
        pod_detected = account_data.get("pod_detected", False)
        reach_drop = account_data.get("reach_drop_pct", 0)
        data_completeness = account_data.get("data_completeness", 1.0)

        if account_age_months < 3:
            return "new_account"
        if growth_rate > 0.50:
            return "viral_growth"
        if is_verified:
            return "celebrity_verified"
        if bot_score > 80:
            return "obvious_bots"
        if pod_detected:
            return "pod_detected"
        if reach_drop > 50:
            return "shadowbanned"
        if data_completeness < 0.80:
            return "incomplete_data"
        return "none"

    # ---------------------- Prompts ----------------------
    def get_system_prompt(self) -> str:
        return """Sen System Governor Agent'sın - PhD seviyesinde veri doğrulama ve bot tespit uzmanı.

UZMANLIK ALANLARIN:
- Instagram veri yapısı ve güvenilirlik analizi
- Veri tutarlılık kontrolleri ve anomali tespiti
- Bot, fake follower ve engagement pod tespiti
- Hesap sağlığı değerlendirmesi (authenticity, engagement, growth, compliance)
- Shadowban risk analizi
- Çapraz doğrulama ve kalite güvencesi

ANALİZ METODOLOJİN:

1. BOT SCORE HESAPLAMA (0-100, yüksek = riskli):
   Bot_Score = 100 - (Profile_Quality × 0.25 + Activity_Score × 0.25 + Ratio_Score × 0.20 + Engagement_Auth × 0.30)
   
   Risk Levels: 0-20: Very Low, 21-40: Low, 41-60: Medium, 61-80: High, 81-100: Very High

2. AUTHENTICITY SCORE (0-100):
   Authenticity = (Follower_Quality × 0.30) + (Engagement_Auth × 0.30) + (Growth_Legitimacy × 0.25) + (Profile_Auth × 0.15)
   
   Interpretation: 90-100: Highly Authentic, 75-89: Authentic, 60-74: Mostly Authentic, 45-59: Questionable, <45: Likely Inauthentic

3. FOLLOWER QUALITY SCORE (0-100):
   Quality = (Real × 0.35 + Active × 0.30 + Relevant × 0.20 + Engaged × 0.15) × 100

4. DATA CONSISTENCY SCORE (0-100):
   Consistency = 100 - Σ(violation_penalties)
   Penalties: Minor -5, Moderate -15, Major -30, Critical -50

5. HEALTH GRADE:
   Health = (Authenticity × 0.30) + (Engagement × 0.25) + (Content × 0.20) + (Growth × 0.15) + (Compliance × 0.10)
   Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)

6. POD DETECTION:
   Pod_Probability = (Timing_Correlation × 0.30) + (Source_Repetition × 0.30) + (Comment_Similarity × 0.20) + (Reciprocity × 0.20)

TUTARLILIK KONTROL KURALLARI:
- Follower/Engagement Correlation: Yüksek follower = düşük ER%
- Like/Comment Ratio: 50:1 ile 200:1 arası normal
- Follower/Following Balance: Account tipine uygun olmalı
- Engagement Distribution: Normal dağılım beklenir

KRİTİK KURALLAR:
- Tüm skorları verilen formüllerle hesapla
- Edge case'leri tespit et ve confidence'ı ayarla
- Çıktı MUTLAKA geçerli JSON formatında olmalı
- JSON dışında hiçbir metin yazma

PRINCIPAL AUDITOR ENFORCEMENT (ZORUNLU):
1) Mathematical Immutability
    - Follower/Following Ratio = Followers / Following (ASLA post sayısına bölme)
    - Engagement Rate = (Avg Likes + Avg Comments) / Followers * 100
    - Post sayısı > 0 ise format dağılımı (Reels/Carousel/Image) toplamı 100% olmalı
    - Churn null ise Net Growth = "Insufficient Data"

2) Logic Synchronization Lock
    - Engagement < 0.5% ise overall health "good/high" olamaz
    - Passive follower ratio > 90% ise Community Health Score en fazla 50/100
    - Agent'lar arası bot risk çelişkisinde "INTEGRITY CONFLICT" flag'i üret

3) Dedup & Loop Prevention
    - Aynı stratejiyi raporda tekrar tekrar tanımlama
    - Tekrar durumunda cross-reference kullan (detayı yeniden yazma)
    - Farklı modüllerin next-step maddeleri benzersiz olmalı

4) Hallucination Containment
    - Metric tablosu sadece 0/null ise nitel içgörü üretme
    - Zorunlu çıktı: "Insufficient data to generate specific visual insights."
    - Büyük içgörülerde veri noktasına izlenebilirlik sağla

5) Tone Standard
    - Yasak kelimeler: ÇÖP, SIFIR, ALARM, FELAKET vb.
    - Stil: Clinical, Objective, Action-Oriented, Advisory
    - "Bad" yerine "Critical Underperformance" kullan

6) Advanced Analytics Modules (yalnızca veri varsa)
    - PERFORMANCE_POLARITY: Son 24 posttan Top 3 / Bottom 3 ER ve post_id
    - AUDIENCE_CHRONOBIOLOGY: timestamp varsa Golden Window (Gün/Saat)
    - SENTIMENT_CLOUD_ENGINE: Son 100 yorumdan Top 5 keyword + Pos/Neg/Neu
    - COMPETITIVE_BENCHMARK: Growth/ER/Frequency için WIN/LOSS
    - Veri yoksa zorunlu çıktı: "Insufficient Data"

7) Output Sanitization
    - Şunları nihai çıktıda asla gösterme:
      "JSON parsing failed", "Manual review required", "mismatch detected",
      ve ham prompt kalıntıları (ör. "line_1: [WHO]")

Çıktı dili: Türkçe"""

    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        return f"""Aşağıdaki Instagram hesap verilerini analiz et ve veri doğrulama / bot tespit değerlendirmesi yap.

=== HESAP VERİLERİ ===
{account_data}

=== ANALİZ GÖREVLERİ ===
1. BOT TESPİTİ: Profile quality, activity patterns, ratios, engagement authenticity analiz et
2. FOLLOWER KALİTESİ: Real, active, relevant, engaged follower yüzdelerini tahmin et
3. ENGAGEMENT AUTHENTİCİTY: Organik engagement %, timing naturalness, comment quality değerlendir
4. DATA CONSİSTENCY: Tutarlılık kurallarını kontrol et, ihlalleri tespit et
5. POD TESPİTİ: Engagement pod aktivitesi var mı kontrol et
6. SHADOWBAN RİSK: Reach drop, hashtag performance, discovery indicators
7. GROWTH PATTERN: Büyüme kalıbı organik mi yoksa şüpheli mi?
8. HEALTH GRADE: Overall health grade belirle
9. EDGE CASE: Özel durumları tespit et ve confidence ayarla

=== ÇIKTI FORMATI ===
Aşağıdaki JSON şemasına TAM UYUMLU yanıt ver. Ekstra metin veya açıklama YAZMA.

```json
{{
  "agent": "system_governor",
  "analysis_timestamp": "ISO8601_formatında_tarih",
  "validation_summary": {{
    "data_quality": "excellent|good|fair|poor",
    "analysis_confidence": 0.0,
    "issues_detected": 0,
    "critical_alerts": 0
  }},
  "metrics": {{
    "authenticityScore": 0,
    "botRiskLevel": "low|medium|high",
    "followerQualityScore": 0,
    "engagementAuthenticityScore": 0,
    "dataConsistencyScore": 0,
    "overallHealthGrade": "A|B|C|D|F"
  }},
  "findings": [
    "Authenticity Assessment: Detaylı açıklama",
    "Bot Risk Analysis: Detaylı açıklama",
    "Data Consistency: Detaylı açıklama",
    "Growth Pattern: Detaylı açıklama"
  ],
  "recommendations": [
    "Öneri 1: Detaylı aksiyon",
    "Öneri 2: Detaylı aksiyon"
  ],
  "alerts": ["Kritik uyarı varsa"],
  "detailed_analysis": {{
    "bot_detection": {{
      "overall_bot_score": 0,
      "risk_level": "low|medium|high",
      "breakdown": {{
        "profile_quality_score": 0,
        "activity_pattern_score": 0,
        "follower_ratio_score": 0,
        "engagement_authenticity_score": 0
      }},
      "suspicious_signals": [
        {{
          "signal": "sinyal_açıklaması",
          "severity": "low|medium|high",
          "confidence": 0.0,
          "recommendation": "öneri"
        }}
      ],
      "pod_detection": {{
        "probability": 0,
        "evidence": "kanıt_açıklaması",
        "timing_correlation": "normal|suspicious|high",
        "source_repetition": "low|medium|high"
      }}
    }},
    "follower_analysis": {{
      "estimated_real_followers": "yüzde",
      "estimated_active_followers": "yüzde",
      "estimated_ghost_followers": "yüzde",
      "estimated_bot_followers": "yüzde",
      "quality_distribution": {{
        "high_quality": "yüzde",
        "medium_quality": "yüzde",
        "low_quality": "yüzde"
      }}
    }},
    "engagement_analysis": {{
      "organic_engagement_estimate": "yüzde",
      "engagement_timing": {{
        "pattern": "natural|suspicious|artificial",
        "peak_hours": ["HH:MM"],
        "distribution": "normal|skewed|artificial"
      }},
      "comment_quality": {{
        "average_length": "short|medium|long",
        "sentiment": "positive|neutral|negative|mixed",
        "diversity": "low|medium|good|high",
        "bot_comment_estimate": "yüzde"
      }}
    }},
    "growth_analysis": {{
      "pattern_type": "organic|viral|collaboration|purchased|follow_unfollow|bot_inflation",
      "growth_rate": "healthy|slow|fast|suspicious",
      "sustainability": "high|medium|low",
      "anomalies_detected": false,
      "retention_estimate": "yüzde"
    }}
  }},
  "validation": {{
    "dataComplete": true,
    "dataConsistent": true,
    "anomaliesDetected": false,
    "dataFreshness": "fresh|acceptable|stale",
    "calculationAccuracy": "verified|estimated|uncertain"
  }},
  "risk_assessment": {{
    "shadowban_risk": {{
      "score": 0,
      "level": "low|moderate|elevated|high|critical",
      "indicators": ["indicator1"]
    }},
    "account_standing": {{
      "status": "good|warning|at_risk|poor",
      "violations": [],
      "warnings": []
    }},
    "platform_risk": {{
      "algorithm_sensitivity": "low|medium|high",
      "policy_compliance": "high|medium|low"
    }}
  }},
  "quality_assurance": {{
    "qa_score": 0,
    "status": "production_ready|acceptable_with_notes|review_required|reject_reprocess",
    "checks": {{
      "completeness": "complete|partial|incomplete",
      "freshness": "fresh|acceptable|stale",
      "accuracy": "accurate|minor_errors|major_errors",
      "validity": "valid|warnings|invalid",
      "recommendation_quality": "high|medium|low"
    }}
  }},
  "confidence_metrics": {{
    "overall_confidence": 0.0,
    "authenticity_confidence": 0.0,
    "bot_detection_confidence": 0.0,
    "data_quality_confidence": 0.0,
    "factors_affecting_confidence": ["faktör1", "faktör2"]
  }},
  "edge_case_detection": {{
    "detected_case": "none|new_account|viral_growth|celebrity_verified|obvious_bots|pod_detected|shadowbanned|incomplete_data|regional_account",
    "special_considerations": ["özel_durum"],
    "adjusted_approach": "yaklaşım_açıklaması"
  }}
}}
```

=== KRİTİK KURALLAR ===
- Metrikleri formüllere göre HESAPLA, rastgele değer verme
- Bot tespiti için tüm sinyalleri değerlendir
- Tutarlılık kontrollerini uygula ve ihlalleri raporla
- Edge case varsa confidence'ı ayarla
- SADECE JSON çıktısı ver, başka hiçbir şey yazma
"""

    # analyze metodu BaseAgent'tan miras alınıyor - override edilmemeli
    # BaseAgent.analyze() metodu doğru şekilde:
    # 1. get_system_prompt() ve get_analysis_prompt() çağırır
    # 2. LLM'e istek gönderir
    # 3. Response'u parse eder ve validate eder

    async def validate_all(
        self,
        agent_results: Dict[str, Any],
        account_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Validate results from all other agents - cross-validation function."""
        validation_prompt = f"""Tüm agent sonuçlarını çapraz doğrula.

=== HESAP ===
Username: @{account_data.get('username', 'unknown')}
Followers: {account_data.get('followers', 0):,}
Engagement Rate: {account_data.get('engagementRate', 0):.2f}%

=== AGENT SONUÇLARI ===
{agent_results}

=== DOĞRULAMA GÖREVLERİ ===
1. Agent'lar arası metrik tutarlılığını kontrol et (±10 puan tolerans)
2. Çelişkili bulgular var mı tespit et
3. Önerilerin hesap boyutuna uygun olup olmadığını değerlendir
4. Gerçekçi olmayan projeksiyonları işaretle
5. Ham veriyle sonuçların uyumunu doğrula

=== ÇIKTI ===
```json
{{
  "validated": true,
  "confidence": 0.95,
  "issues": [
    {{
      "type": "contradiction|inconsistency|error",
      "agents": ["agent1", "agent2"],
      "description": "sorun_açıklaması",
      "severity": "low|medium|high",
      "resolution": "çözüm_açıklaması"
    }}
  ],
  "adjustments": [
    {{
      "agent": "agent_adı",
      "metric": "metrik_adı",
      "original": 0,
      "adjusted": 0,
      "reason": "düzeltme_nedeni"
    }}
  ],
  "cross_validation_summary": {{
    "agents_checked": 0,
    "contradictions_found": 0,
    "minor_discrepancies": 0,
    "data_alignment": "aligned|minor_issues|major_issues",
    "recommendation_feasibility": "feasible|needs_adjustment|unrealistic"
  }}
}}
```

SADECE JSON çıktısı ver.
"""

        full_prompt = f"{self.get_system_prompt()}\n\n{validation_prompt}"
        response = await self.model.generate_content_async(full_prompt)
        return self.parse_response(response.text)

    def apply_hard_validation_rules(
        self, 
        analysis_result: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        SERT VALİDASYON KURALLARI UYGULA
        
        Bu kurallar MUTLAKA uygulanmalı - AI'ın yorumuna bırakılmaz.
        Giriş verilerine göre skorları ve SWOT'u zorla düzelt.
        
        Args:
            analysis_result: Tüm agent'lardan gelen birleşik analiz sonucu
            account_data: Ham hesap verisi
            
        Returns:
            Düzeltilmiş analiz sonucu
        """
        violations = []
        adjustments = []
        
        # Metrikleri güvenli şekilde al
        metrics = analysis_result.get("metrics", {})
        engagement_rate = account_data.get("engagementRate", 0)
        trust_score = metrics.get("trustScore", 100)
        visual_chaos = metrics.get("visualChaosScore", 0)
        bot_risk = metrics.get("botRiskScore", 0)
        followers = account_data.get("followers", 0)
        following = account_data.get("following", 0)
        overall_score = metrics.get("overallScore", 50)
        
        # =============================================
        # KURAL 1: Engagement < 1% = SWOT'ta strength YOK
        # =============================================
        if engagement_rate < 1.0:
            violations.append({
                "rule": "engagement_strength_rule",
                "message": self.validation_failure_messages["engagement_too_low"].format(value=f"{engagement_rate:.2f}"),
                "severity": "critical"
            })
            
            # SWOT'tan tüm strength'leri kaldır
            if "swot" in analysis_result:
                if analysis_result["swot"].get("strengths"):
                    original_strengths = analysis_result["swot"]["strengths"]
                    analysis_result["swot"]["strengths"] = []
                    adjustments.append({
                        "field": "swot.strengths",
                        "original": original_strengths,
                        "adjusted": [],
                        "reason": f"Engagement rate {engagement_rate:.2f}% < 1% - hiçbir güçlü yön yazılamaz"
                    })
        
        # =============================================
        # KURAL 2: Trust Score < 50 = Overall max 60
        # =============================================
        if trust_score < 50:
            violations.append({
                "rule": "trust_score_ceiling_rule",
                "message": self.validation_failure_messages["trust_too_low"].format(value=trust_score),
                "severity": "critical"
            })
            
            if overall_score > 60:
                original_score = overall_score
                analysis_result["metrics"]["overallScore"] = 60
                adjustments.append({
                    "field": "metrics.overallScore",
                    "original": original_score,
                    "adjusted": 60,
                    "reason": f"Trust score {trust_score}/100 < 50 - genel skor 60'ı geçemez"
                })
        
        # =============================================
        # KURAL 3: Visual Chaos > 70 = Grid max 40
        # =============================================
        if visual_chaos > 70:
            violations.append({
                "rule": "visual_chaos_grid_rule",
                "message": self.validation_failure_messages["visual_chaos"].format(value=visual_chaos),
                "severity": "major"
            })
            
            grid_score = metrics.get("gridConsistencyScore", 100)
            if grid_score > 40:
                analysis_result["metrics"]["gridConsistencyScore"] = 40
                adjustments.append({
                    "field": "metrics.gridConsistencyScore",
                    "original": grid_score,
                    "adjusted": 40,
                    "reason": f"Visual chaos {visual_chaos}/100 > 70 - grid skoru 40'ı geçemez"
                })
        
        # =============================================
        # KURAL 4: Bot Risk > 60 = Authenticity max 40
        # =============================================
        if bot_risk > 60:
            violations.append({
                "rule": "bot_risk_authenticity_rule",
                "message": self.validation_failure_messages["bot_risk_high"].format(value=bot_risk),
                "severity": "critical"
            })
            
            auth_score = metrics.get("authenticityScore", 100)
            if auth_score > 40:
                analysis_result["metrics"]["authenticityScore"] = 40
                adjustments.append({
                    "field": "metrics.authenticityScore",
                    "original": auth_score,
                    "adjusted": 40,
                    "reason": f"Bot risk {bot_risk}% > 60 - authenticity 40'ı geçemez"
                })
        
        # =============================================
        # KURAL 5: Following > 2x Followers = Red Flag
        # =============================================
        if followers > 0 and following > followers * 2:
            ratio = following / followers
            violations.append({
                "rule": "follower_ratio_rule",
                "message": self.validation_failure_messages["follow_unfollow"].format(value=f"{ratio:.1f}x"),
                "severity": "major"
            })
            
            # Red flag ekle
            if "red_flags" not in analysis_result:
                analysis_result["red_flags"] = []
            analysis_result["red_flags"].append({
                "type": "follow_unfollow_tactic",
                "severity": "high",
                "description": f"Following ({following:,}) takipçinin ({followers:,}) 2 katından fazla - manipülatif büyüme stratejisi"
            })
        
        # =============================================
        # KURAL 6: Aylık büyüme > 50% = Satın alınmış şüphesi
        # =============================================
        monthly_growth = account_data.get("monthlyGrowthRate", 0)
        if monthly_growth > 50:
            violations.append({
                "rule": "growth_rate_rule",
                "message": self.validation_failure_messages["purchased_followers"].format(value=monthly_growth),
                "severity": "major"
            })
            
            if "red_flags" not in analysis_result:
                analysis_result["red_flags"] = []
            analysis_result["red_flags"].append({
                "type": "purchased_followers_suspected",
                "severity": "high",
                "description": f"Aylık büyüme %{monthly_growth} - organik büyüme için çok yüksek"
            })
        
        # Validation sonuçlarını rapora ekle
        analysis_result["hard_validation_results"] = {
            "rules_checked": len(self.hard_validation_rules),
            "violations_found": len(violations),
            "adjustments_made": len(adjustments),
            "violations": violations,
            "adjustments": adjustments,
            "validation_status": "PASS" if len(violations) == 0 else "FAIL_WITH_CORRECTIONS"
        }
        
        return analysis_result


    # =============================================
    # GÖREV 2: POST-PROCESS FINDINGS
    # =============================================
    def post_process_findings(self, findings: List[Any]) -> List[str]:
        """
        GÖREV 2: Findings listesini post-process et
        
        1. DEDUPLICATION: Aynı anlama gelen veya birebir aynı cümleleri sil
        2. TEMİZLİK: Anlamsız karakterler içeren maddeleri filtrele
        3. FORMAT: Liste boşsa varsayılan mesaj ekle
        
        Args:
            findings: Ham findings listesi
            
        Returns:
            Temizlenmiş ve tekilleştirilmiş findings listesi
        """
        if not findings:
            return ["Veri tutarlılığı doğrulandı, kritik bir anormallik yok."]
        
        cleaned_findings: List[str] = []
        seen_normalized: set = set()
        
        for finding in findings:
            # String'e dönüştür
            if isinstance(finding, dict):
                text = finding.get("finding") or finding.get("text") or finding.get("description") or str(finding)
            else:
                text = str(finding)
            
            # Temizlik - anlamsız karakterleri kontrol et
            text = text.strip()
            
            # Sadece parantez veya anlamsız karakterler içeren maddeleri filtrele
            if not text:
                continue
            if text in ["(", ")", "()", "[]", "{}", "-", "--", "...", "•", "●"]:
                continue
            if len(text) < 5:  # Çok kısa maddeler anlamsız
                continue
            if text.count("(") + text.count(")") == len(text):  # Sadece parantezlerden oluşuyor
                continue
            
            # Deduplication - normalize edilmiş versiyonu kontrol et
            normalized = self._normalize_text_for_dedup(text)
            if normalized in seen_normalized:
                continue
            
            # Benzer cümle kontrolü
            is_duplicate = False
            for seen in seen_normalized:
                if self._is_similar_text(normalized, seen):
                    is_duplicate = True
                    break
            
            if is_duplicate:
                continue
            
            seen_normalized.add(normalized)
            cleaned_findings.append(text)
        
        # Liste boşsa varsayılan mesaj
        if not cleaned_findings:
            return ["Veri tutarlılığı doğrulandı, kritik bir anormallik yok."]
        
        return cleaned_findings
    
    def _normalize_text_for_dedup(self, text: str) -> str:
        """Metni karşılaştırma için normalize et"""
        import re
        # Küçük harfe çevir
        normalized = text.lower()
        # Sayıları kaldır
        normalized = re.sub(r'\d+', '', normalized)
        # Özel karakterleri kaldır
        normalized = re.sub(r'[^\w\s]', '', normalized)
        # Fazla boşlukları temizle
        normalized = ' '.join(normalized.split())
        return normalized
    
    def _is_similar_text(self, text1: str, text2: str, threshold: float = 0.8) -> bool:
        """İki metnin benzer olup olmadığını kontrol et (Jaccard similarity)"""
        if not text1 or not text2:
            return False
        
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return False
        
        intersection = words1 & words2
        union = words1 | words2
        
        similarity = len(intersection) / len(union)
        return similarity >= threshold
    
    def post_process_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        GÖREV 2: Tüm sonucu post-process et
        
        Bu metot analyze() sonucuna uygulanmalı
        """
        if not result:
            return result
        
        # Findings'i post-process et
        if "findings" in result:
            result["findings"] = self.post_process_findings(result["findings"])
        
        # Recommendations'ı da temizle (aynı mantıkla)
        if "recommendations" in result:
            result["recommendations"] = self.post_process_findings(result["recommendations"])
        
        # Alerts'i de temizle
        if "alerts" in result:
            result["alerts"] = self.post_process_findings(result["alerts"])
        
        return result


__all__ = ["SystemGovernorAgent"]
