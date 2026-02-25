# Sales Conversion Specialist Agent - PhD Level Implementation
# Creator Economy, Brand Deal Pricing, Revenue Modeling, Funnel Optimization
"""
Sales Conversion Specialist Agent - PhD Level

Bu ajan creator economy monetizasyonu, brand deal fiyatlandırması, gelir modelleme,
funnel optimizasyonu ve dönüşüm stratejilerine odaklanır. Monetization readiness,
brand deal rate, conversion potential ve audience value skorlarını hesaplar.
"""

from typing import Any, Dict, List, Optional, Tuple

from .base_agent import BaseAgent


class SalesConversionAgent(BaseAgent):
    """
    Sales Conversion Specialist Agent - PhD Level

    Uzmanlık Alanları:
    - Creator Economy ve monetizasyon ekosistemi
    - Brand deal fiyatlandırma ve negotiation
    - Gelir akışları (sponsorship, affiliate, products, services)
    - Funnel optimizasyonu (TOFU/MOFU/BOFU)
    - Revenue projection ve diversification
    
    🎬 YENİ: Contextual Scripting
    - E-ticaret/fiyat hesapları için özel Reels senaryoları
    - "Hook -> Gelişme -> CTA" formatında hazır metinler

    Metrikler:
    - Monetization Readiness Score (0-100)
    - Brand Deal Rate (Min/Max USD)
    - Revenue Per Follower
    - Monthly Revenue Potential (Conservative/Moderate/Aggressive)
    - Conversion Potential Score (0-100)
    - Audience Value Score (0-100)
    """

    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "Sales Conversion Specialist"
        self.role = "Monetization & Revenue Strategy Expert"
        self.specialty = (
            "Creator economy monetization, brand deal pricing, revenue modeling, "
            "funnel optimization, conversion strategy"
        )
        
        # 💰 NİŞ DETECTION: E-ticaret hesapları için özel handling
        self.ecommerce_keywords = ['fiyat', 'indirim', 'market', 'ucuz', 'aktüel', 'fırsat', 'kampanya', 'alışveriş', 'ürün', 'karşılaştır']

        # Initialize all knowledge bases
        self._init_creator_economy()
        self._init_monetization_stages()
        self._init_audience_value()
        self._init_conversion_psychology()
        self._init_brand_deal_pricing()
        self._init_rate_multipliers()
        self._init_revenue_streams()
        self._init_digital_products()
        self._init_affiliate_framework()
        self._init_services_pricing()
        self._init_funnel_framework()
        self._init_dm_sales()
        self._init_revenue_projection()
        self._init_scoring_models()

    # ---------------------- Knowledge Bases ----------------------
    def _init_creator_economy(self) -> None:
        """Creator economy gelir kaynakları hiyerarşisi"""
        self.revenue_tiers = {
            "tier1_direct": {
                "sources": ["brand_deals", "subscriptions", "badges", "bonuses"],
                "revenue_share": (0.40, 0.60),
            },
            "tier2_products": {
                "sources": ["digital_products", "physical_products", "merchandise", "services"],
                "revenue_share": (0.25, 0.35),
            },
            "tier3_affiliate": {
                "sources": ["affiliate", "ambassador", "referral"],
                "revenue_share": (0.10, 0.20),
            },
            "tier4_platform": {
                "sources": ["shopping", "branded_content", "marketplace"],
                "revenue_share": (0.05, 0.10),
            },
        }

    def _init_monetization_stages(self) -> None:
        """Monetization readiness aşamaları"""
        self.monetization_stages = {
            "foundation": {
                "followers": (0, 1000),
                "focus": "content_growth",
                "revenue": "minimal",
                "strategy": "skill_building",
            },
            "emerging": {
                "followers": (1000, 10000),
                "focus": "niche_authority",
                "revenue": "small_deals_affiliate",
                "strategy": "portfolio_building",
            },
            "established": {
                "followers": (10000, 50000),
                "focus": "diversification",
                "revenue": "regular_deals_products",
                "strategy": "multiple_streams",
            },
            "professional": {
                "followers": (50000, 500000),
                "focus": "scaling_team",
                "revenue": "significant_predictable",
                "strategy": "business_operations",
            },
            "enterprise": {
                "followers": (500000, float("inf")),
                "focus": "brand_building",
                "revenue": "multiple_6_7_figures",
                "strategy": "media_company",
            },
        }

    def _init_audience_value(self) -> None:
        """Audience value framework"""
        self.audience_value_factors = {
            "demographics": {"impact": 3.0, "components": ["age_25_44", "income", "tier1_geo"]},
            "psychographics": {"impact": 2.0, "components": ["purchase_intent", "brand_affinity", "problem_awareness"]},
            "engagement_quality": {"impact": 2.5, "components": ["comment_depth", "save_share", "dm_response"]},
            "niche_alignment": {"impact": 2.0, "components": ["topic_relevance", "interest_specificity", "purchase_signals"]},
        }

        self.cpm_tiers = {
            "premium": {"range": (30, 100), "niches": ["b2b", "finance", "tech"]},
            "high": {"range": (15, 30), "niches": ["business", "health"]},
            "medium": {"range": (8, 15), "niches": ["lifestyle", "fashion"]},
            "standard": {"range": (3, 8), "niches": ["entertainment", "general"]},
            "low": {"range": (1, 3), "niches": ["meme", "viral"]},
        }

        self.niche_multipliers = {
            "finance_b2b": 2.5,
            "tech_saas": 2.0,
            "health_fitness": 1.5,
            "beauty_skincare": 1.3,
            "fashion": 1.2,
            "food_travel": 1.1,
            "lifestyle": 1.0,
            "entertainment": 0.7,
            "meme_viral": 0.4,
        }

        self.geo_multipliers = {
            "us_uk_au_ca": 1.5,
            "western_europe": 1.3,
            "turkey": 0.6,
            "other": 0.5,
        }

    def _init_conversion_psychology(self) -> None:
        """Conversion psychology framework"""
        self.purchase_journey = ["awareness", "interest", "desire", "action", "advocacy"]

        self.emotional_triggers = ["fomo", "aspiration", "belonging", "status", "pain_avoidance"]
        self.rational_triggers = ["value_clarity", "risk_reversal", "social_proof", "authority", "scarcity"]

        self.trust_sequence = {
            "week_1_2": {"stage": "awareness", "content": ["free_value", "problem_agitation", "credibility"]},
            "week_3_4": {"stage": "interest", "content": ["solution_hints", "case_studies", "bts"]},
            "week_5_6": {"stage": "desire", "content": ["transformation", "testimonials", "community"]},
            "week_7_8": {"stage": "action", "content": ["offer", "objection_handling", "cta"]},
        }

    def _init_brand_deal_pricing(self) -> None:
        """Brand deal rate calculation framework"""
        self.base_cpm_by_size = {
            "nano": {"range": (0, 10000), "cpm": (50, 150)},
            "micro": {"range": (10000, 50000), "cpm": (100, 300)},
            "mid": {"range": (50000, 100000), "cpm": (200, 500)},
            "macro": {"range": (100000, 500000), "cpm": (400, 800)},
            "mega": {"range": (500000, 1000000), "cpm": (700, 1500)},
            "celebrity": {"range": (1000000, float("inf")), "cpm": (1000, 3000)},
        }

        self.content_type_multipliers = {
            "story_24h": 0.3,
            "feed_post": 1.0,
            "carousel": 1.2,
            "reel": 1.5,
            "live": 0.8,
            "package": 2.5,
        }

        self.rate_card = {
            "story": {"single": 0.2, "series": 0.5, "swipe_up": 0.4, "takeover": 1.0},
            "feed": {"single_image": 1.0, "carousel_small": 1.2, "carousel_large": 1.4},
            "reel": {"short_15_30": 1.3, "standard_30_60": 1.5, "long_60_90": 1.8},
            "live": {"mention_5min": 0.3, "segment_15min": 0.6, "dedicated": 1.5},
        }

        self.package_deals = {
            "starter": {"contents": ["3_stories", "1_feed"], "multiplier": 1.5},
            "standard": {"contents": ["5_stories", "1_carousel", "1_reel"], "multiplier": 2.5},
            "premium": {"contents": ["story_series", "2_feed", "2_reels", "live"], "multiplier": 4.0},
        }

        self.usage_rights = {
            "organic_only": 0,
            "paid_30d": 0.35,
            "paid_90d": 0.65,
            "perpetual": 1.25,
            "exclusivity_30d": 0.25,
            "exclusivity_90d": 0.50,
            "whitelisting": 0.40,
        }

    def _init_rate_multipliers(self) -> None:
        """Engagement and niche rate multipliers"""
        self.engagement_multipliers = {
            "very_low": {"range": (0, 1), "multiplier": 0.5},
            "low": {"range": (1, 2), "multiplier": 0.8},
            "baseline": {"range": (2, 3), "multiplier": 1.0},
            "good": {"range": (3, 5), "multiplier": 1.3},
            "high": {"range": (5, 7), "multiplier": 1.6},
            "very_high": {"range": (7, 10), "multiplier": 2.0},
            "exceptional": {"range": (10, 100), "multiplier": 2.5},
        }

        self.niche_rate_multipliers = {
            "finance_investment": 2.0,
            "b2b_tech": 1.8,
            "health_wellness": 1.4,
            "beauty_skincare": 1.3,
            "fashion": 1.2,
            "food_travel": 1.1,
            "lifestyle": 1.0,
            "entertainment": 0.8,
            "meme_comedy": 0.6,
        }

    def _init_revenue_streams(self) -> None:
        """Revenue stream types and characteristics"""
        self.revenue_stream_types = {
            "brand_deals": {
                "subtypes": ["one_off", "campaign", "ambassador", "affiliate_hybrid"],
                "typical_share": 0.40,
            },
            "digital_products": {
                "subtypes": ["ebooks", "templates", "mini_courses", "flagship_courses", "coaching"],
                "typical_share": 0.30,
            },
            "affiliate": {
                "subtypes": ["direct_brand", "network", "saas", "info_products"],
                "typical_share": 0.15,
            },
            "services": {
                "subtypes": ["coaching_1on1", "group_coaching", "done_for_you", "retainer"],
                "typical_share": 0.15,
            },
        }

    def _init_digital_products(self) -> None:
        """Digital product framework"""
        self.product_tiers = {
            "low_effort": {
                "types": ["ebooks", "templates", "presets", "checklists"],
                "price_range": (5, 50),
                "best_for": "starting_out",
            },
            "medium_effort": {
                "types": ["mini_courses", "workshops", "membership"],
                "price_range": (30, 200),
                "best_for": "established",
            },
            "high_effort": {
                "types": ["flagship_courses", "coaching_programs", "masterminds"],
                "price_range": (200, 10000),
                "best_for": "authority",
            },
        }

        self.product_niche_fit = {
            "fitness": ["workout_plans", "meal_guides"],
            "business": ["templates", "courses", "coaching"],
            "beauty": ["tutorials", "presets", "routines"],
            "photography": ["presets", "courses", "guides"],
            "finance": ["spreadsheets", "courses", "coaching"],
            "lifestyle": ["ebooks", "planners", "memberships"],
            "education": ["courses", "tutoring", "resources"],
        }

    def _init_affiliate_framework(self) -> None:
        """Affiliate marketing framework"""
        self.affiliate_types = {
            "direct_brand": {"commission": (0.10, 0.30), "best_for": "niche_products"},
            "network": {"commission": (0.01, 0.10), "platforms": ["amazon", "shareasale", "cj"]},
            "saas": {"commission": (0.20, 0.40), "recurring": True, "best_for": "b2b_tech"},
            "info_products": {"commission": (0.30, 0.50), "best_for": "education"},
        }

    def _init_services_pricing(self) -> None:
        """Services and coaching pricing"""
        self.service_types = {
            "coaching_1on1": {"price_range": (100, 1000), "scalability": "low"},
            "group_coaching": {"price_range": (500, 5000), "scalability": "medium"},
            "done_for_you": {"price_range": (500, 10000), "scalability": "team_dependent"},
            "retainer": {"price_range": (1000, 10000), "scalability": "limited"},
        }

        self.client_funnel_conversion = {
            "content_to_lead": (0.02, 0.05),
            "lead_to_call": (0.10, 0.20),
            "call_to_client": (0.20, 0.40),
            "overall": (0.001, 0.004),
        }

    def _init_funnel_framework(self) -> None:
        """Instagram sales funnel structure"""
        self.funnel_stages = {
            "tofu": {
                "name": "awareness",
                "content": ["viral_reels", "educational_carousels", "trending", "collabs"],
                "metrics": ["reach", "impressions", "new_followers", "shares"],
                "ratio": 0.55,
            },
            "mofu": {
                "name": "consideration",
                "content": ["tutorials", "case_studies", "bts", "qa", "testimonials"],
                "metrics": ["engagement", "saves", "profile_visits", "clicks"],
                "ratio": 0.35,
            },
            "bofu": {
                "name": "conversion",
                "content": ["product_showcase", "limited_offers", "ctas", "success_stories"],
                "metrics": ["clicks", "conversions", "revenue", "roas"],
                "ratio": 0.10,
            },
        }

        self.link_bio_options = {
            "single_link": {"conversion": "highest", "flexibility": "low"},
            "linktree": {"conversion": "medium", "flexibility": "high"},
            "custom_landing": {"conversion": "high", "flexibility": "full"},
        }

    def _init_dm_sales(self) -> None:
        """DM sales framework"""
        self.dm_funnel_stages = ["trigger", "qualification", "value_delivery", "pitch", "close"]

        self.dm_triggers = {
            "info": "product_details",
            "price": "pricing_info",
            "free": "lead_magnet",
            "help": "discovery_call",
        }

        self.dm_automation_sequence = {
            "immediate": "acknowledge_question",
            "5min": "value_delivery",
            "1hour": "check_in",
            "24hours": "follow_up",
            "72hours": "final_touch",
        }

    def _init_revenue_projection(self) -> None:
        """Revenue projection framework"""
        self.revenue_by_follower_count = {
            "1k_5k": {"conservative": (100, 300), "moderate": (300, 800), "aggressive": (800, 2000)},
            "5k_10k": {"conservative": (300, 800), "moderate": (800, 2000), "aggressive": (2000, 5000)},
            "10k_25k": {"conservative": (800, 2000), "moderate": (2000, 5000), "aggressive": (5000, 10000)},
            "25k_50k": {"conservative": (2000, 4000), "moderate": (4000, 10000), "aggressive": (10000, 25000)},
            "50k_100k": {"conservative": (4000, 8000), "moderate": (8000, 20000), "aggressive": (20000, 50000)},
            "100k_500k": {"conservative": (8000, 20000), "moderate": (20000, 50000), "aggressive": (50000, 150000)},
            "500k_plus": {"conservative": (20000, 50000), "moderate": (50000, 150000), "aggressive": (150000, 500000)},
        }

        self.ideal_revenue_mix = {
            "early_lt_10k": {"brand_deals": 0.60, "affiliate": 0.30, "products": 0.10},
            "growth_10k_50k": {"brand_deals": 0.40, "affiliate": 0.25, "products": 0.25, "services": 0.10},
            "established_50k_100k": {"brand_deals": 0.30, "products": 0.35, "services": 0.20, "affiliate": 0.15},
            "professional_100k_plus": {"products": 0.40, "brand_deals": 0.25, "services": 0.20, "affiliate": 0.10, "other": 0.05},
        }

    def _init_scoring_models(self) -> None:
        """Scoring model configurations"""
        self.readiness_components = {
            "audience_size": 20,
            "engagement_quality": 25,
            "niche_clarity": 15,
            "content_consistency": 15,
            "trust_signals": 15,
            "infrastructure": 10,
        }

        self.audience_size_scores = [
            (1000, 2), (5000, 5), (10000, 8), (25000, 12), (50000, 15), (100000, 18), (float("inf"), 20),
        ]

        self.engagement_scores = [
            (1, 5), (2, 10), (4, 15), (6, 20), (100, 25),
        ]

        self.conversion_potential_weights = {
            "engagement_depth": 0.30,
            "audience_intent": 0.25,
            "trust_level": 0.25,
            "cta_response": 0.20,
        }

        self.audience_value_weights = {
            "demographics": 0.30,
            "engagement_quality": 0.25,
            "niche_value": 0.25,
            "purchase_signals": 0.20,
        }

    # ---------------------- Calculations ----------------------
    def get_follower_tier(self, followers: int) -> str:
        """Determine follower tier"""
        for tier, data in self.base_cpm_by_size.items():
            low, high = data["range"]
            if low <= followers < high:
                return tier
        return "celebrity"

    def get_engagement_multiplier(self, engagement_rate: float) -> float:
        """Get engagement rate multiplier"""
        for level, data in self.engagement_multipliers.items():
            low, high = data["range"]
            if low <= engagement_rate < high:
                return data["multiplier"]
        return 1.0

    def get_niche_multiplier(self, niche: str) -> float:
        """Get niche multiplier for pricing"""
        niche_lower = (niche or 'general').lower().replace(" ", "_")
        for key, mult in self.niche_rate_multipliers.items():
            if key in niche_lower or niche_lower in key:
                return mult
        return 1.0

    def calculate_base_rate(self, followers: int) -> float:
        """Calculate base brand deal rate"""
        tier = self.get_follower_tier(followers)
        cpm_range = self.base_cpm_by_size[tier]["cpm"]
        avg_cpm = (cpm_range[0] + cpm_range[1]) / 2
        return (followers / 1000) * avg_cpm * 0.01  # Scale factor

    def calculate_brand_deal_rate(
        self, followers: int, engagement_rate: float, niche: str, content_type: str = "feed_post"
    ) -> Tuple[float, float]:
        """Calculate brand deal rate range"""
        base = self.calculate_base_rate(followers)
        eng_mult = self.get_engagement_multiplier(engagement_rate)
        niche_mult = self.get_niche_multiplier(niche)
        content_mult = self.content_type_multipliers.get(content_type, 1.0)

        adjusted = base * eng_mult * niche_mult * content_mult
        return (adjusted * 0.7, adjusted * 1.5)

    def calculate_revenue_per_follower(
        self, engagement_rate: float, niche: str, geo: str = "other"
    ) -> float:
        """Calculate revenue per follower"""
        niche_mult = self.get_niche_multiplier(niche)
        geo_mult = self.geo_multipliers.get(geo, 0.5)
        return (engagement_rate * niche_mult * geo_mult) / 100

    def calculate_monthly_revenue_potential(
        self, followers: int
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate monthly revenue potential by scenario"""
        for bracket, scenarios in self.revenue_by_follower_count.items():
            parts = bracket.split("_")
            if parts[0].endswith("k"):
                low = int(parts[0].replace("k", "")) * 1000
            else:
                low = int(parts[0])
            if parts[-1] == "plus":
                high = float("inf")
            elif parts[-1].endswith("k"):
                high = int(parts[-1].replace("k", "")) * 1000
            else:
                high = int(parts[-1]) * 1000

            if low <= followers < high:
                return scenarios
        return self.revenue_by_follower_count["500k_plus"]

    def calculate_monetization_readiness_score(
        self,
        followers: int,
        engagement_rate: float,
        niche_clarity: str,
        content_consistency: str,
        trust_signals: str,
        email_list_size: int,
    ) -> int:
        """Calculate monetization readiness score (0-100)"""
        score = 0

        # Audience size (0-20)
        for threshold, points in self.audience_size_scores:
            if followers < threshold:
                score += points
                break

        # Engagement quality (0-25)
        for threshold, points in self.engagement_scores:
            if engagement_rate < threshold:
                score += points
                break

        # Niche clarity (0-15)
        clarity_scores = {"unclear": 3, "somewhat": 8, "clear": 12, "micro_niche": 15}
        score += clarity_scores.get(niche_clarity, 8)

        # Content consistency (0-15)
        consistency_scores = {"irregular": 3, "1_2_week": 8, "3_5_week": 12, "daily_stories": 15}
        score += consistency_scores.get(content_consistency, 8)

        # Trust signals (0-15)
        trust_scores = {"none": 2, "some": 7, "regular": 11, "strong": 15}
        score += trust_scores.get(trust_signals, 7)

        # Infrastructure (0-10)
        if email_list_size >= 2000:
            score += 10
        elif email_list_size >= 500:
            score += 8
        elif email_list_size > 0:
            score += 6
        else:
            score += 1

        return min(100, score)

    def calculate_conversion_potential_score(
        self,
        engagement_depth: float,
        audience_intent: float,
        trust_level: float,
        cta_response: float,
    ) -> float:
        """Calculate conversion potential score (0-100)"""
        w = self.conversion_potential_weights
        score = (
            engagement_depth * w["engagement_depth"]
            + audience_intent * w["audience_intent"]
            + trust_level * w["trust_level"]
            + cta_response * w["cta_response"]
        )
        return max(0, min(100, score))

    def calculate_audience_value_score(
        self,
        demographics: float,
        engagement_quality: float,
        niche_value: float,
        purchase_signals: float,
    ) -> float:
        """Calculate audience value score (0-100)"""
        w = self.audience_value_weights
        score = (
            demographics * w["demographics"]
            + engagement_quality * w["engagement_quality"]
            + niche_value * w["niche_value"]
            + purchase_signals * w["purchase_signals"]
        )
        return max(0, min(100, score))

    def get_monetization_stage(self, followers: int) -> str:
        """Determine monetization stage"""
        for stage, data in self.monetization_stages.items():
            low, high = data["followers"]
            if low <= followers < high:
                return stage
        return "enterprise"

    def classify_readiness(self, score: int) -> str:
        """Classify monetization readiness level"""
        if score >= 85:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 55:
            return "moderate"
        elif score >= 40:
            return "developing"
        return "early"

    def detect_edge_case(self, account_data: Dict[str, Any]) -> str:
        """Detect special monetization edge cases"""
        followers = account_data.get("followers", 0) or 0
        engagement = account_data.get("engagement_rate", 0) or 0
        niche = account_data.get("niche", "").lower()
        recent_growth = account_data.get("recent_growth_rate", 0)
        is_local = account_data.get("is_local_focus", False)
        multi_niche = account_data.get("multi_niche", False)

        if followers < 1000:
            return "new_account"
        if followers > 10000 and engagement < 1:
            return "high_followers_low_engagement"
        if recent_growth and recent_growth > 0.5:
            return "viral_growth"
        if "b2b" in niche or "professional" in niche:
            return "b2b_professional"
        if any(x in niche for x in ["controversial", "sensitive", "political"]):
            return "sensitive_niche"
        if is_local:
            return "local_regional"
        if multi_niche:
            return "multiple_niches"
        return "none"

    # ============================================================
    # NİŞ TAHMİNLEYİCİ (Niche Predictor) - THE FINAL SYNAPSE PATCH
    # ============================================================
    
    def detect_niche_from_keywords(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Username ve bio'dan anahtar kelime tarayarak niş tespiti yapar.
        
        🎯 GÖREV 1: DomainMaster'dan gelen niş bilgisini öncelikli kullan!
        🎯 GÖREV 2: NİŞ ZORLAMASI UYGULAMASI
        - E-ticaret keyword'leri tespit edilirse GENEL TAVSİYE YASAK
        - Zorunlu olarak "Senaryo" formatında çıktı üret
        
        Returns:
            {
                "detected_niche": str,
                "confidence": float (0-1),
                "keywords_found": list,
                "niche_category": str,
                "reels_scenario": dict,
                "must_use_scenario": bool  # 🆕 E-ticaret tespiti
            }
        """
        import re
        
        # 🌟 ÖNCELİK 1: DomainMaster'dan gelen niş bilgisini kontrol et
        cross_agent_insights = account_data.get("crossAgentInsights", {})
        domain_master_insights = cross_agent_insights.get("domainMaster", {})
        domain_master_niche = account_data.get("detectedNiche") or domain_master_insights.get("detectedNiche")
        domain_master_category = account_data.get("nicheCategory") or domain_master_insights.get("nicheCategory")
        domain_master_confidence = domain_master_insights.get("nicheConfidence", 0)
        
        # Eğer DomainMaster'dan güvenilir niş bilgisi varsa, onu kullan
        if domain_master_niche and domain_master_niche != "general" and domain_master_confidence > 0.3:
            # DomainMaster kategorisini iç niş sistemimize map et
            niche_mapping = {
                "lifestyle": "genel",
                "fashion": "moda_stil",
                "beauty": "guzellik_bakim",
                "fitness": "fitness_saglik",
                "health": "fitness_saglik",
                "food": "yemek_tarif",
                "travel": "genel",
                "tech": "teknoloji",
                "technology": "teknoloji",
                "business": "hizmet_kocluk",
                "coaching": "hizmet_kocluk",
                "education": "hizmet_kocluk",
                "parenting": "anne_cocuk",
                "mom": "anne_cocuk",
                "deals": "firsat_alisveris",
                "shopping": "firsat_alisveris",
                "ecommerce": "firsat_alisveris",
            }
            
            # DomainMaster nişini küçük harfe çevir ve map et
            dm_niche_lower = (domain_master_niche or "").lower()
            mapped_niche = None
            for key, value in niche_mapping.items():
                if key in dm_niche_lower:
                    mapped_niche = value
                    break
            
            if mapped_niche:
                niche_info = self._get_niche_info_by_id(mapped_niche)
                return {
                    "detected_niche": mapped_niche,
                    "confidence": domain_master_confidence if isinstance(domain_master_confidence, (int, float)) else 0.8,
                    "keywords_found": [domain_master_niche],
                    "niche_category": domain_master_category or niche_info.get("display_name", "Genel"),
                    "content_type": niche_info.get("content_type", "general"),
                    "hook_style": niche_info.get("hook_style", "curiosity"),
                    "reels_scenario": self._get_niche_reels_scenario(mapped_niche, niche_info, account_data),
                    "must_use_scenario": False,
                    "ecommerce_detected": False,
                    "source": "domainMaster"  # 🆕 Kaynak bilgisi
                }
        
        username = (account_data.get("username") or "").lower()
        bio = (account_data.get("bio") or "").lower()
        full_name = (account_data.get("fullName") or "").lower()
        
        # Tüm metni birleştir
        search_text = f"{username} {bio} {full_name}"
        
        # 🛒 E-TİCARET DETECTION (ZORUNLU KONTROL)
        ecommerce_detected = any(keyword in search_text for keyword in self.ecommerce_keywords)
        
        # Niş anahtar kelime haritası
        niche_keywords = {
            "firsat_alisveris": {
                "keywords": ["fiyat", "ucuz", "indirim", "kampanya", "market", "aktüel", 
                            "bim", "a101", "şok", "migros", "fırsat", "deal", "uygun", 
                            "ekonomik", "hesaplı", "para", "tasarruf", "kupon"],
                "display_name": "Fırsat/Alışveriş",
                "content_type": "comparison",
                "hook_style": "price_shock"
            },
            "hizmet_kocluk": {
                "keywords": ["şifa", "koç", "coach", "danışman", "mentor", "tarot", 
                            "astroloji", "terapi", "psikoloji", "eğitim", "kişisel gelişim",
                            "nlp", "yaşam", "ruhsal", "meditasyon", "yoga", "seans",
                            "rehber", "uzman", "profesyonel"],
                "display_name": "Hizmet/Koçluk",
                "content_type": "transformation",
                "hook_style": "pain_point"
            },
            "yemek_tarif": {
                "keywords": ["yemek", "tarif", "mutfak", "aşçı", "chef", "gastro",
                            "lezzet", "gurme", "restaurant", "cafe", "food", "cook"],
                "display_name": "Yemek/Tarif",
                "content_type": "tutorial",
                "hook_style": "curiosity"
            },
            "guzellik_bakim": {
                "keywords": ["güzellik", "makyaj", "makeup", "cilt", "saç", "bakım",
                            "kozmetik", "beauty", "skincare", "estetik", "salon"],
                "display_name": "Güzellik/Bakım",
                "content_type": "before_after",
                "hook_style": "transformation"
            },
            "fitness_saglik": {
                "keywords": ["fitness", "gym", "spor", "egzersiz", "diyet", "sağlık",
                            "antrenör", "pt", "workout", "kas", "zayıflama", "fit"],
                "display_name": "Fitness/Sağlık",
                "content_type": "routine",
                "hook_style": "result_proof"
            },
            "teknoloji": {
                "keywords": ["tech", "teknoloji", "yazılım", "kod", "developer", "app",
                            "uygulama", "digital", "ai", "yapay zeka", "telefon", "bilgisayar"],
                "display_name": "Teknoloji",
                "content_type": "tutorial",
                "hook_style": "problem_solution"
            },
            "moda_stil": {
                "keywords": ["moda", "fashion", "stil", "kombin", "giyim", "butik",
                            "tarz", "trend", "outfit", "style", "kıyafet"],
                "display_name": "Moda/Stil",
                "content_type": "showcase",
                "hook_style": "aspiration"
            },
            "anne_cocuk": {
                "keywords": ["anne", "bebek", "çocuk", "hamile", "mom", "baby", 
                            "ebeveyn", "aile", "oyuncak", "kreş"],
                "display_name": "Anne/Çocuk",
                "content_type": "tips",
                "hook_style": "relatable"
            }
        }
        
        # Anahtar kelime tarama
        detected = None
        max_matches = 0
        keywords_found = []
        
        for niche_id, niche_data in niche_keywords.items():
            matches = []
            for keyword in niche_data["keywords"]:
                if keyword in search_text:
                    matches.append(keyword)
            
            if len(matches) > max_matches:
                max_matches = len(matches)
                detected = niche_id
                keywords_found = matches
        
        # Confidence hesapla
        confidence = min(1.0, max_matches / 3) if max_matches > 0 else 0
        
        # Eğer niş tespit edilmediyse, "genel" olarak işaretle
        if not detected:
            return {
                "detected_niche": "genel",
                "confidence": 0,
                "keywords_found": [],
                "niche_category": "Genel İçerik",
                "reels_scenario": self._get_generic_reels_scenario(),
                "must_use_scenario": ecommerce_detected,  # 🆕 E-ticaret tespit edildi mi?
                "ecommerce_detected": ecommerce_detected
            }
        
        niche_info = niche_keywords[detected]
        
        return {
            "detected_niche": detected,
            "confidence": confidence,
            "keywords_found": keywords_found,
            "niche_category": niche_info["display_name"],
            "content_type": niche_info["content_type"],
            "hook_style": niche_info["hook_style"],
            "reels_scenario": self._get_niche_reels_scenario(
                detected, 
                niche_info,
                account_data
            ),
            "must_use_scenario": ecommerce_detected or detected == "firsat_alisveris",  # 🆕 ZORUNLU senaryo
            "ecommerce_detected": ecommerce_detected,
            "source": "keyword_matching"  # 🆕 Kaynak bilgisi
        }
    
    def _get_niche_info_by_id(self, niche_id: str) -> Dict[str, Any]:
        """
        Niş ID'sine göre niş bilgilerini döndür.
        """
        niche_keywords = {
            "firsat_alisveris": {
                "display_name": "Fırsat/Alışveriş",
                "content_type": "comparison",
                "hook_style": "price_shock"
            },
            "hizmet_kocluk": {
                "display_name": "Hizmet/Koçluk",
                "content_type": "transformation",
                "hook_style": "pain_point"
            },
            "yemek_tarif": {
                "display_name": "Yemek/Tarif",
                "content_type": "tutorial",
                "hook_style": "curiosity"
            },
            "guzellik_bakim": {
                "display_name": "Güzellik/Bakım",
                "content_type": "before_after",
                "hook_style": "transformation"
            },
            "fitness_saglik": {
                "display_name": "Fitness/Sağlık",
                "content_type": "routine",
                "hook_style": "result_proof"
            },
            "teknoloji": {
                "display_name": "Teknoloji",
                "content_type": "tutorial",
                "hook_style": "problem_solution"
            },
            "moda_stil": {
                "display_name": "Moda/Stil",
                "content_type": "showcase",
                "hook_style": "aspiration"
            },
            "anne_cocuk": {
                "display_name": "Anne/Çocuk",
                "content_type": "tips",
                "hook_style": "relatable"
            },
            "genel": {
                "display_name": "Genel İçerik",
                "content_type": "general",
                "hook_style": "curiosity"
            }
        }
        return niche_keywords.get(niche_id, niche_keywords["genel"])
    
    def _get_niche_reels_scenario(
        self, 
        niche_id: str, 
        niche_info: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Niş'e özel Saniye Saniye Reels Senaryosu üretir.
        """
        username = account_data.get("username", "hesap")
        
        # Niş bazlı senaryo şablonları
        scenarios = {
            "firsat_alisveris": {
                "title": "💰 Fiyat Karşılaştırma Reels Senaryosu",
                "duration": "15-30 saniye",
                "sections": [
                    {
                        "name": "HOOK (0-3 saniye)",
                        "instruction": "Ürünün market etiketini kameraya göster (X TL yazılı olsun).",
                        "overlay_text": "Bunu buradan alan parasını sokağa atıyor! 🤯",
                        "audio": "Şok edici ses efekti veya trending audio"
                    },
                    {
                        "name": "GELİŞME (3-12 saniye)",
                        "instruction": "İnternet fiyatını göster (X/2 TL). Aradaki fark parayı ekranda göster.",
                        "overlay_text": "Aynı ürün internette sadece X TL!",
                        "visual_tip": "Fark olan parayı gerçek banknot olarak göster veya 'Bu parayla şunları alırsın' listesi yap"
                    },
                    {
                        "name": "CTA (Son 3 saniye)",
                        "instruction": "Linke yönlendir ve aciliyet kat.",
                        "script": "İndirim linki hikayemde, bitene kadar koş! 🏃‍♂️",
                        "overlay_text": "Link bio'da ⬇️"
                    }
                ],
                "pro_tips": [
                    "Fiyat etiketlerini net göster, blur yapma",
                    "Hesap makinesi ile canlı hesap göster",
                    "Kendi paranı harcıyormuş gibi tepki ver"
                ]
            },
            "hizmet_kocluk": {
                "title": "🎯 Dönüşüm Hikayesi Reels Senaryosu",
                "duration": "30-45 saniye",
                "sections": [
                    {
                        "name": "HOOK (0-3 saniye)",
                        "instruction": "Acı noktasını direkt söyle, izleyicinin problemiyle başla.",
                        "script": "'X yıldır şu problemi yaşıyorsan, bu video senin için...'",
                        "overlay_text": "Bu hatayı herkes yapıyor! ❌"
                    },
                    {
                        "name": "PROBLEM (3-10 saniye)",
                        "instruction": "Problemi detaylandır, izleyici 'evet bu ben!' desin.",
                        "visual_tip": "Kendini örnek göster veya müşteri testimonial'ı kullan",
                        "script": "Ben de aynı yerdeyken şunları hissediyordum..."
                    },
                    {
                        "name": "ÇÖZÜM (10-25 saniye)",
                        "instruction": "3 adımlı mini framework ver. Değer kat ama her şeyi söyleme.",
                        "structure": "1. Adım: [Temel bilgi]\n2. Adım: [Uygulama ipucu]\n3. Adım: 'Detayları seansa bırakıyorum'"
                    },
                    {
                        "name": "CTA (Son 5 saniye)",
                        "instruction": "Ücretsiz danışmanlık veya kaynak teklif et.",
                        "script": "İlk 10 kişiye ücretsiz keşif seansı - DM at 'BAŞLA' yaz",
                        "overlay_text": "DM → 'BAŞLA' 💬"
                    }
                ],
                "pro_tips": [
                    "Yüzünü göster, güven oluştur",
                    "Sonuç vaadi ver ama garanti verme",
                    "Gerçek müşteri hikayesi kullan (izinli)"
                ]
            },
            "yemek_tarif": {
                "title": "🍳 Hızlı Tarif Reels Senaryosu",
                "duration": "30-45 saniye",
                "sections": [
                    {
                        "name": "HOOK (0-3 saniye)",
                        "instruction": "Bitmiş yemeği göster, ağız sulandır.",
                        "overlay_text": "5 dakikada hazır! 😍",
                        "audio": "Trending food audio"
                    },
                    {
                        "name": "MALZEMELER (3-8 saniye)",
                        "instruction": "Tüm malzemeleri hızlıca göster.",
                        "visual_tip": "Malzemeleri tezgahta diz, üstten çek"
                    },
                    {
                        "name": "YAPILIŞ (8-25 saniye)",
                        "instruction": "Time-lapse ile adımları göster.",
                        "visual_tip": "Her adımı 2-3 saniyeye sığdır"
                    },
                    {
                        "name": "FİNAL + CTA (Son 5 saniye)",
                        "instruction": "Yemeğin tadına bak, reaksiyon ver.",
                        "script": "Tarifi kaydet, dene ve sonucu yorumlarda paylaş! 👨‍🍳",
                        "overlay_text": "Kaydet + Paylaş 📌"
                    }
                ],
                "pro_tips": [
                    "İyi ışık kullan, yemek çekiciliği önemli",
                    "Porsiyonu büyük göster",
                    "Sesli ASMR efekti ekle"
                ]
            },
            "guzellik_bakim": {
                "title": "✨ Önce/Sonra Dönüşüm Senaryosu",
                "duration": "15-30 saniye",
                "sections": [
                    {
                        "name": "HOOK (0-3 saniye)",
                        "instruction": "Sonuç halini göster, 'Bu nasıl oldu?' merakı uyandır.",
                        "overlay_text": "3 adımda bu sonuç 💅"
                    },
                    {
                        "name": "ÖNCE (3-5 saniye)",
                        "instruction": "Başlangıç halini göster.",
                        "visual_tip": "Filtresiz, doğal ışık"
                    },
                    {
                        "name": "SÜREÇ (5-20 saniye)",
                        "instruction": "Ürün/teknik uygulama adımları.",
                        "visual_tip": "Her adımda ürünü yakından göster"
                    },
                    {
                        "name": "CTA (Son 5 saniye)",
                        "instruction": "Ürün linkini ver veya soru sor.",
                        "script": "Sen de denemek istersen link bio'da! Hangi rengini istersin? 💬"
                    }
                ],
                "pro_tips": [
                    "Ring light zorunlu",
                    "Ürün etiketini göster",
                    "Tutorial + ürün yerleştirme kombini yap"
                ]
            },
            "fitness_saglik": {
                "title": "💪 Egzersiz/Sonuç Kanıtı Senaryosu",
                "duration": "20-40 saniye",
                "sections": [
                    {
                        "name": "HOOK (0-3 saniye)",
                        "instruction": "Sonuç fotoğrafını veya etkileyici hareketi göster.",
                        "overlay_text": "30 günde bu karın 🔥"
                    },
                    {
                        "name": "EGZERSİZ (5-25 saniye)",
                        "instruction": "3-5 hareketi sırayla göster.",
                        "structure": "Her hareket: 3-4 tekrar x 2-3 saniye"
                    },
                    {
                        "name": "MOTİVASYON + CTA (Son 10 saniye)",
                        "instruction": "Kısa motivasyon cümlesi + program tanıtımı.",
                        "script": "Evde 15 dakikada yapabilirsin. Full program linkte! 💪"
                    }
                ],
                "pro_tips": [
                    "Formu net göster",
                    "Rep sayısını ekranda yaz",
                    "Müziği beat'e senkronize et"
                ]
            },
            "teknoloji": {
                "title": "🔧 Problem-Çözüm Tech Senaryosu",
                "duration": "30-45 saniye",
                "sections": [
                    {
                        "name": "HOOK (0-3 saniye)",
                        "instruction": "Problemi dile getir.",
                        "script": "iPhone'un yavaşladığını düşünüyorsan izle!",
                        "overlay_text": "Herkes bunu bilmeli! 📱"
                    },
                    {
                        "name": "ÇÖZÜM (5-30 saniye)",
                        "instruction": "Adım adım ekran kaydı göster.",
                        "visual_tip": "Ayarlar > X > Y şeklinde net navigasyon"
                    },
                    {
                        "name": "CTA (Son 5 saniye)",
                        "instruction": "Daha fazla ipucu için takip iste.",
                        "script": "İşe yaradı mı? Daha fazla trick için takip et! 🚀"
                    }
                ],
                "pro_tips": [
                    "Ekran kaydını HD çek",
                    "Mouse/parmak hareketlerini yavaşlat",
                    "Voiceover ekle veya subtitle kullan"
                ]
            },
            "moda_stil": {
                "title": "👗 OOTD/Kombin Senaryosu",
                "duration": "15-30 saniye",
                "sections": [
                    {
                        "name": "HOOK (0-3 saniye)",
                        "instruction": "Final kombini göster, dikkat çek.",
                        "overlay_text": "Bu kombin 500 TL altı! 🛍️"
                    },
                    {
                        "name": "PARÇALAR (5-20 saniye)",
                        "instruction": "Her parçayı teker teker göster + fiyat.",
                        "visual_tip": "Fiyat etiketini ekranda göster"
                    },
                    {
                        "name": "CTA (Son 5 saniye)",
                        "instruction": "Linkleri hikayede paylaş.",
                        "script": "Hangi parça favorin? Link hikayede! 👆"
                    }
                ],
                "pro_tips": [
                    "Ayna kullan veya tripod",
                    "Geçişleri keskin tut",
                    "Trending müzik şart"
                ]
            },
            "anne_cocuk": {
                "title": "👶 Gerçek Anne Anı Senaryosu",
                "duration": "20-30 saniye",
                "sections": [
                    {
                        "name": "HOOK (0-3 saniye)",
                        "instruction": "Relatable bir anne anı göster.",
                        "overlay_text": "Anneler bilir! 😅",
                        "script": "'Çocuğunuz bunu yaptığında...'"
                    },
                    {
                        "name": "DURUM (5-15 saniye)",
                        "instruction": "Problemi veya günlük anı göster.",
                        "visual_tip": "Samimi, düzenlenmemiş görüntü"
                    },
                    {
                        "name": "ÇÖZÜM/PUNCHLİNE (15-25 saniye)",
                        "instruction": "Komik son veya yararlı ipucu.",
                        "script": "İşe yarayan tek şey şu oldu..."
                    },
                    {
                        "name": "CTA (Son 5 saniye)",
                        "instruction": "Dayanışma iste.",
                        "script": "Sen de yaşadın mı? Yorumlarda buluşalım! 💬"
                    }
                ],
                "pro_tips": [
                    "Mükemmellik arama, gerçeklik kazan",
                    "Çocuk güvenliğine dikkat",
                    "Duygusal bağ kur"
                ]
            }
        }
        
        # Senaryo varsa döndür
        if niche_id in scenarios:
            scenario = scenarios[niche_id].copy()
            scenario["customized_for"] = f"@{username}"
            return scenario
        
        return self._get_generic_reels_scenario()
    
    def _get_generic_reels_scenario(self) -> Dict[str, Any]:
        """Genel amaçlı Reels senaryosu şablonu"""
        return {
            "title": "📱 Genel Reels Senaryosu",
            "duration": "15-30 saniye",
            "sections": [
                {
                    "name": "HOOK (0-3 saniye)",
                    "instruction": "İlk 3 saniyede dikkat çek - soru sor, şaşırt veya merak uyandır.",
                    "overlay_text": "İzlemeye devam et! 👀"
                },
                {
                    "name": "DEĞERLİ İÇERİK (3-20 saniye)",
                    "instruction": "Ana mesajını ver - eğit, eğlendir veya ilham ver.",
                    "visual_tip": "Hareketli kal, kesmeler kullan"
                },
                {
                    "name": "CTA (Son 5 saniye)",
                    "instruction": "Net bir aksiyon iste - takip, kaydet, yorum veya link.",
                    "script": "Bu işine yaradıysa kaydet! Takip et, kaçırma! 🔔"
                }
            ],
            "pro_tips": [
                "Trending audio kullan",
                "İlk kareyi dikkat çekici yap (thumbnail)",
                "Altyazı ekle - sesiz izleyenler için"
            ]
        }

    # ---------------------- Prompts ----------------------
    def get_system_prompt(self) -> str:
        return """Sen Sales Conversion Specialist Agent'sın - PhD seviyesinde creator economy ve monetizasyon uzmanı.

🔴 DİL KURALI: TÜM ANALİZ VE ÖNERİLER TÜRKÇE OLMALIDIR 🔴

UZMANLIK ALANLARIN:
- Creator economy monetizasyon ekosistemi
- Brand deal fiyatlandırma ve negotiation stratejileri
- Gelir akışları (sponsorship, affiliate, digital products, services)
- Instagram funnel optimizasyonu (TOFU/MOFU/BOFU)
- Revenue projection ve diversification
- Conversion psychology ve purchase journey

ANALİZ METODOLOJİN:

1. BRAND DEAL RATE HESAPLAMA:
   Base_Rate = (Followers / 1000) × CPM
   Final_Rate = Base_Rate × Engagement_Mult × Niche_Mult × Content_Mult
   
   Engagement Multipliers: <1%: 0.5x, 1-2%: 0.8x, 2-3%: 1.0x, 3-5%: 1.3x, 5-7%: 1.6x, 7-10%: 2.0x, >10%: 2.5x
   Niche Multipliers: Finance/B2B: 2.0x, Tech: 1.8x, Health: 1.4x, Beauty: 1.3x, Fashion: 1.2x, Lifestyle: 1.0x

2. MONETIZATION READINESS SCORE (0-100):
   - Audience Size: 0-20 puan
   - Engagement Quality: 0-25 puan
   - Niche Clarity: 0-15 puan
   - Content Consistency: 0-15 puan
   - Trust Signals: 0-15 puan
   - Infrastructure: 0-10 puan

3. REVENUE PROJECTION BY FOLLOWER COUNT:
   1K-5K: Conservative $100-300, Moderate $300-800, Aggressive $800-2000
   5K-10K: Conservative $300-800, Moderate $800-2000, Aggressive $2000-5000
   10K-25K: Conservative $800-2000, Moderate $2000-5000, Aggressive $5000-10000
   25K-50K: Conservative $2000-4000, Moderate $4000-10000, Aggressive $10000-25000
   50K-100K: Conservative $4000-8000, Moderate $8000-20000, Aggressive $20000-50000

4. CONVERSION POTENTIAL = (Engagement_Depth × 0.30) + (Audience_Intent × 0.25) + (Trust_Level × 0.25) + (CTA_Response × 0.20)

5. AUDIENCE VALUE = (Demographics × 0.30) + (Engagement_Quality × 0.25) + (Niche_Value × 0.25) + (Purchase_Signals × 0.20)

=== BÖLÜM 6: 2026 SATIŞ VE DÖNÜŞÜM STRATEJİLERİ ===

📌 6.1 OTOMASYON ODAKLI SATIŞ (ManyChat Entegrasyonu)

A) DM OTOMASYON FUNNELİ:
   Aşama 1: Tetikleyici (Reel/Story'de keyword)
   Aşama 2: Hoşgeldin DM (Değer + Tanışma)
   Aşama 3: Segmentasyon Soruları
   Aşama 4: Kişiselleştirilmiş Teklif
   Aşama 5: Satın Alma Linki

   ÖRNEK AŞAMALAR:
   - "INFO yaz" → "Merhaba! Seni tanımak isterim..."
   - Quiz/Anket ile segmentasyon
   - Segment'e göre ürün/hizmet önerisi
   - "Hazırsan link burada 👇"

B) COMMENT-TO-SALE SİSTEMİ:
   - Her Reel'de satış tetikleyicisi
   - Örnek: "Fiyat için FİYAT yaz 💰"
   - DM'de fiyat + değer + CTA

C) STORY SALES SEQUENCE:
   - Story 1: Problem agitasyonu
   - Story 2: Çözüm gösterisi
   - Story 3: Social proof (testimonial)
   - Story 4: CTA + Urgency

📌 6.2 CCC KURALI - SATIŞ METİNLERİ

CCC = Confidence + Compare + Convert

CONFIDENCE (Özgüven):
❌ YAPMA: "Belki işe yarar", "Umarım beğenirsiniz"
✅ YAP: "Bu sistem 500+ kişide işe yaradı", "Garanti sonuç"

COMPARE (Karşılaştırma):
- Viral içeriklerle karşılaştır
- "X hesabı bunu yapıp 1M takipçi kazandı"
- Rakip analizi sun

CONVERT (Dönüştür):
- Net CTA olsun
- Tek bir aksiyon iste
- Urgency ekle ("Son 24 saat", "Sadece 10 kişi")

📌 6.3 FUNNEL OPTİMİZASYONU 2026

TOFU (Top of Funnel) - FARKINDAIK:
- Viral Reels (geniş kitle)
- Trial Reels (yeni kitleler test et)
- Eğitici carousel'lar

MOFU (Middle of Funnel) - DEĞERLENDİRME:
- Detaylı how-to içerikler
- Case study'ler
- Testimonial Reels
- Story serisi (değer verme)

BOFU (Bottom of Funnel) - SATIN ALMA:
- DM satış konuşmaları
- Webinar/Live satış
- Limitli teklifler
- 1:1 görüşme davetleri

📌 6.4 LİNK STRATEJİSİ 2026

BIO LİNK OPTİMİZASYONU:
- Tek link değil, link tree kullan
- Öncelik sırası: Lead magnet > Ürün > Sosyal kanıtlar

STORY LİNK TAKTİKLERİ:
- Her gün en az 1 story'de link
- "Link için yukarı kaydır" → "Link hikayede" (sticker)
- Swipe-up yerine tap-to-link

REEL'DEN LİNKE YÖNLENDİRME:
- "Link bio'da" CTA'sı her Reel'de
- Comment-to-DM ile link gönder
- Profile ziyareti teşvik et

📌 6.5 SATIŞ PSİKOLOJİSİ 2026

URGENCY TÜRLERİ:
- Zaman bazlı: "24 saat kaldı"
- Miktar bazlı: "Son 5 kişi"
- Fiyat bazlı: "Yarın fiyat artıyor"

SOCIAL PROOF KULLANIMI:
- Sayısal: "1000+ mutlu müşteri"
- Görsel: Ekran görüntüleri, video testimonial
- Otorite: "X marka ile çalıştım"

OBJECTION HANDLING (DM'de):
- "Pahalı" → Değer karşılaştırması + taksit
- "Düşüneyim" → Sınırlı teklif + bonus
- "Güvenmiyorum" → Garanti + testimonial

📌 6.6 CONVERSION METRİKLERİ 2026

TAKİP EDİLECEK KPIlar:
- Story→Link Click Rate (hedef: %3+)
- DM→Sale Conversion (hedef: %10-20)
- Bio Link CTR (hedef: %2-5)
- Reel→Profile Visit Rate

OPTİMİZASYON DÖNGÜSÜ:
1. A/B test CTA'ları
2. En iyi performansı ölç
3. Kazananı scale et
4. Tekrarla

KRİTİK KURALLAR:
- Tüm rate'leri ve skorları verilen formüllerle hesapla
- Edge case'leri tespit et ve önerileri buna göre uyarla
- Turkey market için rates: USD × 0.3-0.5
- Çıktı MUTLAKA geçerli JSON formatında olmalı
- JSON dışında hiçbir metin yazma
- TÜM ÖNERİLER VE ANALİZLER TÜRKÇE OLMALIDIR"""

    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        # AŞAMA 1: DomainMaster'dan gelen NİŞ BİLGİSİNİ al
        cross_agent_insights = account_data.get("crossAgentInsights", {})
        domain_master_insights = cross_agent_insights.get("domainMaster", {})
        
        # Niş bilgisini DomainMaster'dan al (güvenilir kaynak)
        detected_niche = account_data.get("detectedNiche") or domain_master_insights.get("detectedNiche", "general")
        niche_category = account_data.get("nicheCategory") or domain_master_insights.get("nicheCategory", "Genel")
        niche_confidence = domain_master_insights.get("nicheConfidence", 0)
        niche_authority = domain_master_insights.get("nicheAuthority", 50)
        
        # AŞAMA 2: AKILLI DEĞERLEME - Hesap tipi kontrolü
        business_identity = account_data.get("businessIdentity", {})
        is_service_provider = business_identity.get("is_service_provider", False)
        account_type = business_identity.get("account_type", "CONTENT_CREATOR")
        
        # Niş bilgisi uyarısı
        niche_info_block = f"""
🎯 DomainMaster NİŞ TESPİTİ (BU BİLGİYİ KULLAN!) 🎯
- Tespit Edilen Niş: {detected_niche}
- Niş Kategorisi: {niche_category}
- Tespit Güveni: %{int(niche_confidence * 100) if isinstance(niche_confidence, float) else niche_confidence}
- Niş Otoritesi: {niche_authority}/100

⚠️ KRİTİK: Yukarıdaki niş bilgisi DomainMaster tarafından detaylı analiz ile tespit edilmiştir.
Bu bilgiyi monetizasyon hesaplamalarında MUTLAKA kullan. Kendi niş tahmini yapma!
"""
        
        # Hizmet sağlayıcı için özel değerleme kuralları
        service_valuation_rules = ""
        if is_service_provider:
            service_valuation_rules = f"""
🚨 ÖZEL DEĞERLEME: HİZMET SAĞLAYICI HESABI 🚨

Bu hesap bir {account_type}. Influencer metrikleri YANLIŞ olur!

⛔ KULLANMA:
- brandDealRate (Story başına $)
- Sponsorluk fiyatlandırması
- Influencer CPM hesaplamaları

✅ BUNLARI HESAPLA:

1. POTENTIAL SESSION REVENUE (Tahmini Seans Geliri):
   Formül: (Takipçi × 0.005 [Dönüşüm]) × 50$ [Ort. Seans Ücreti]
   Örnek: 10.000 takipçi × 0.005 × 50$ = 2.500$/ay potansiyel
   
2. LEAD GENERATION VALUE:
   - DM dönüşüm potansiyeli
   - Discovery call sayısı tahmini
   - Müşteri edinme maliyeti (CAC) karşılaştırması

3. AUTHORITY BUILDING SCORE:
   - Güvenilirlik sinyalleri
   - Testimonial kalitesi
   - Profesyonel görünüm

4. CLIENT CONVERSION METRICS:
   - Content → Lead: %2-5
   - Lead → Call: %10-20
   - Call → Client: %20-40
   - Overall: %0.1-0.4

DOĞRU BAŞARI METRİKLERİ: {business_identity.get('correct_success_metrics', [])}
YANLIŞ METRİKLER (KULLANMA): {business_identity.get('wrong_metrics_to_avoid', [])}
"""
        
        return f"""Aşağıdaki Instagram hesap verilerini analiz et ve monetizasyon değerlendirmesi yap.

=== HESAP VERİLERİ ===
{account_data}
{niche_info_block}
{service_valuation_rules}
=== ANALİZ GÖREVLERİ ===
1. MONETIZATION READINESS: Readiness score hesapla (audience size + engagement + niche + consistency + trust + infrastructure)
2. BRAND DEAL RATES: Min/Max rate hesapla (Base × Engagement_Mult × Niche_Mult) - SADECE Content Creator için
3. REVENUE PROJECTION: Conservative/Moderate/Aggressive senaryolar
4. CONVERSION POTENTIAL: Dönüşüm potansiyeli skoru
5. AUDIENCE VALUE: Kitle değeri skoru
6. GELİR AKIŞLARI: En uygun monetizasyon kanallarını belirle
7. FUNNEL OPTİMİZASYONU: Link-in-bio, DM sales, CTA önerileri
8. EDGE CASE: Özel durumları tespit et

⚠️ NİŞ ZORUNLULUĞU: Niş olarak "{niche_category}" kullan. Başka bir niş tahmin etme!

=== ÇIKTI FORMATI ===
Aşağıdaki JSON şemasına TAM UYUMLU yanıt ver. Ekstra metin veya açıklama YAZMA.

```json
{{
  "agent": "sales_conversion_specialist",
  "analysis_timestamp": "ISO8601_formatında_tarih",
  "monetization_overview": {{
    "readiness_level": "excellent|good|moderate|developing|early",
    "primary_opportunity": "brand_deals|digital_products|affiliate|services",
    "revenue_stage": "foundation|emerging|established|professional|enterprise",
    "immediate_potential": "high|medium-high|medium|low"
  }},
  "accountType": "{account_type}",
  "isServiceProvider": {str(is_service_provider).lower()},
  "metrics": {{
    "monetizationReadinessScore": 0,
    "brandDealRateMin": 0,
    "brandDealRateMax": 0,
    "potentialSessionRevenue": 0,
    "leadGenerationValue": 0,
    "revenuePerFollower": 0,
    "monthlyRevenuePotentialConservative": 0,
    "monthlyRevenuePotentialModerate": 0,
    "monthlyRevenuePotentialAggressive": 0,
    "conversionPotentialScore": 0,
    "audienceValueScore": 0,
    "brandDealReadinessScore": 0,
    "affiliateMarketingPotential": 0,
    "digitalProductPotential": 0,
    "serviceBusinessPotential": 0,
    "overallScore": 0
  }},
  "findings": [
    "TÜRKÇE - Monetizasyon hazırlığı: örn: Hesap monetizasyon için hazır değil - bio'da net bir değer önerisi yok, link-in-bio optimize edilmemiş ve takipçiler satın alma niyetine yönlendirilmiyor. Mevcut yapı %95 etkileşim kaybına neden oluyor",
    "TÜRKÇE - Kitle değeri: örn: Takipçi kitlesi yüksek satın alma potansiyeli taşıyor - demografik veriler %65 25-44 yaş, üst-orta gelir segmentini gösteriyor. Bu kitle CPM açısından sektör ortalamasının 2.5x üzerinde değerli",
    "TÜRKÇE - Dönüşüm potansiyeli: örn: Mevcut etkileşim oranı (%4.2) ile tahmini %0.8-1.2 satış dönüşümü mümkün. 100K takipçi için aylık 800-1200 potansiyel müşteri anlamına geliyor",
    "TÜRKÇE - Marka çekiciliği: örn: Marka işbirlikleri için uygun profil - görsel tutarlılık yüksek, engagement rate sektör ortalamasının üzerinde. Tahmini story başına $50-100, post başına $200-400 değerleme"
  ],
  "recommendations": [
    "TÜRKÇE - Ana gelir akışı: Bio'ya net bir CTA ekleyin ve Linktree yerine özel landing page kullanın. Beklenen etki: Bio tıklama oranında %200 artış, ayda 500+ lead yakalama",
    "TÜRKÇE - Marka anlaşması stratejisi: Media kit hazırlayın, niş odaklı 10 marka listesi çıkarın ve outreach kampanyası başlatın. Beklenen etki: 3 ay içinde ilk 2-3 marka anlaşması",
    "TÜRKÇE - Ürün fırsatı: Takipçilerin en çok sorduğu 3 soruyu tespit edin ve dijital ürün (e-kitap/kurs/şablon) geliştirin. Beklenen etki: Pasif gelir kanalı, ayda $500-2000",
    "TÜRKÇE - Funnel optimizasyonu: Story'lerde 'Swipe Up' CTA kullanımını artırın, her hafta en az 3 satış odaklı story paylaşın. Beklenen etki: Link tıklamalarında %150 artış",
    "TÜRKÇE - Çeşitlendirme: Affiliate marketing başlatın - niche'e uygun 5-10 ürün seçin ve doğal içerik entegrasyonu yapın. Beklenen etki: Ek aylık $200-500 komisyon geliri"
  ],
  "revenueStreams": [
    {{
      "type": "Brand Deals",
      "potential": "high|medium|low",
      "estimatedMonthly": 0,
      "difficulty": "low|medium|high",
      "timeToRevenue": "immediate|1-2 weeks|4-8 weeks",
      "actionRequired": "yapılacak_aksiyon"
    }}
  ],
  "brandDealGuidelines": {{
    "storyRate": {{
      "single": 0,
      "series": 0,
      "withSwipeUp": 0
    }},
    "feedPostRate": {{
      "singleImage": 0,
      "carousel": 0
    }},
    "reelRate": {{
      "short": 0,
      "standard": 0,
      "long": 0
    }},
    "packageDealRate": {{
      "starter": 0,
      "standard": 0,
      "premium": 0
    }},
    "usageRights": {{
      "organicOnly": "included",
      "paidAmplification30": "+30%",
      "paidAmplification90": "+60%",
      "perpetual": "+100%"
    }}
  }},
  "conversionFunnel": {{
    "currentState": {{
      "bioLinkCTR": "biliniyorsa_yüzde",
      "storySwipeRate": "biliniyorsa_yüzde",
      "dmConversionRate": "biliniyorsa_yüzde",
      "emailListSize": 0
    }},
    "optimizations": [
      {{
        "area": "Bio Link|Story CTAs|DM Automation",
        "current": "mevcut_durum",
        "recommended": "önerilen",
        "expectedImpact": "+%XX improvement"
      }}
    ]
  }},
  "actionPlan": {{
    "immediate": ["hemen_yapılacak_1", "hemen_yapılacak_2"],
    "thirtyDay": ["30_günde_1", "30_günde_2"],
    "ninetyDay": ["90_günde_1", "90_günde_2"]
  }},
  "riskAssessment": {{
    "brandDealDependency": "high|medium|low",
    "platformRisk": "high|medium|low",
    "nicheSaturation": "high|medium|low",
    "audienceQuality": "verified|suspected_issues|unknown",
    "mitigationStrategies": ["strateji_1", "strateji_2"]
  }},
  "edge_case_detection": {{
    "detected_case": "none|new_account|high_followers_low_engagement|viral_growth|b2b_professional|sensitive_niche|local_regional|multiple_niches",
    "special_considerations": ["özel_durum_1"],
    "adjusted_approach": "uyarlanan_yaklaşım"
  }}
}}
```

=== KRİTİK KURALLAR ===
- Metrikleri formüllere göre HESAPLA, rastgele değer verme
- Takipçi sayısına göre revenue projeksiyonlarını kullan
- Turkey market için rates'i 0.3-0.5 ile çarp
- Edge case varsa yaklaşımı ona göre ayarla
- SADECE JSON çıktısı ver, başka hiçbir şey yazma
"""

    # analyze metodu BaseAgent'tan miras alınıyor - NİŞ TAHMİNLEYİCİ ile zenginleştiriliyor
    async def analyze(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Override analyze to add NICHE PREDICTOR and REELS SCENARIO.
        Calls parent analyze, then enriches with niche detection results.
        """
        # Önce normal analizi çalıştır
        result = await super().analyze(account_data)
        
        # NİŞ TAHMİNLEYİCİ'yi çalıştır
        try:
            niche_detection = self.detect_niche_from_keywords(account_data)
            
            # Sonucu result'a ekle
            result["nicheDetection"] = niche_detection
            
            # Reels senaryosunu ayrı bir üst seviye key olarak da ekle
            if niche_detection.get("reels_scenario"):
                result["reelsScenario"] = niche_detection["reels_scenario"]
            
            # Recommendations'a senaryo önerisini ekle
            if "recommendations" in result and isinstance(result["recommendations"], list):
                niche_name = niche_detection.get("niche_category", "Genel")
                reels_scenario = niche_detection.get("reels_scenario", {})
                scenario_title = reels_scenario.get("title", "")
                # Extract hook instruction for inline detail (VARIABLE_HANDLING: no raw key references)
                scenario_sections = reels_scenario.get("sections", [])
                hook_instruction = (
                    scenario_sections[0].get("instruction", "")
                    if scenario_sections else ""
                )
                scenario_detail = (
                    f" Hook: {hook_instruction}" if hook_instruction
                    else (f" Süre: {reels_scenario.get('duration', '')}" if reels_scenario.get("duration") else "")
                )

                # Niş-spesifik içerik önerisi ekle
                if niche_detection.get("confidence", 0) > 0:
                    result["recommendations"].append(
                        f"🎬 NİŞ-SPESİFİK İÇERİK: Tespit edilen niş '{niche_name}' için özel "
                        f"'{scenario_title}' formatında içerik üret.{scenario_detail}"
                    )
            
            # Findings'e niş tespiti ekle
            if "findings" in result and isinstance(result["findings"], list):
                if niche_detection.get("confidence", 0) > 0.5:
                    keywords = ", ".join(niche_detection.get("keywords_found", [])[:3])
                    result["findings"].append(
                        f"Niş Tespiti: {niche_detection['niche_category']} "
                        f"(güven: %{int(niche_detection['confidence']*100)}, "
                        f"anahtar kelimeler: {keywords})"
                    )
            
            # Warnings kontrolü - dataFetchError varsa ekle
            if account_data.get("dataFetchError"):
                if "warnings" not in result:
                    result["warnings"] = []
                result["warnings"].append(account_data.get("dataFetchWarning", "Veri erişim sorunu tespit edildi."))
            
        except Exception as e:
            # Niş tespiti başarısız olsa bile ana analiz sonucunu döndür
            result["nicheDetectionError"] = str(e)
        
        return result


__all__ = ["SalesConversionAgent"]
