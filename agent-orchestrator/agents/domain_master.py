# Domain Master Agent - PhD Level Implementation
# Niche Analysis, Trend Detection, Content Strategy & Hashtag Optimization
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent


class DomainMasterAgent(BaseAgent):
    """
    Domain Master Agent - PhD Level
    
    Uzmanlık Alanları:
    - Niche Sınıflandırma ve Tespit
    - Sektör Trend Analizi
    - Content Pillar Stratejisi
    - Hashtag Optimizasyonu
    - Industry Benchmark Karşılaştırması
    
    Metrikler:
    - Niche Authority Score (0-100)
    - Content Relevance Score (0-100)
    - Trend Alignment Score (0-100)
    - Hashtag Effectiveness Score (0-100)
    - Industry Benchmark Score (0-100)
    """
    
    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "Domain Master"
        self.role = "Niche Positioning & Industry Expert"
        self.specialty = "Niche analysis, trend detection, content strategy, hashtag optimization"
        
        # Initialize all knowledge bases
        self._init_niche_taxonomy()
        self._init_niche_benchmarks()
        self._init_trend_lifecycle()
        self._init_seasonal_patterns()
        self._init_content_pillars()
        self._init_hashtag_categories()
        self._init_hashtag_strategy()
        self._init_business_identity_detection()  # YENİ: İşletme kimliği tespiti
    
    def _init_business_identity_detection(self):
        """
        İŞLETME KİMLİĞİ TESPİT SİSTEMİ
        
        KRİTİK: Coach, Danışman, Therapist gibi hesapları
        ASLA "Content Creator" olarak sınıflandırma!
        """
        # Servis sağlayıcı kategorileri
        self.service_provider_categories = {
            "coaching_consulting": {
                "indicators": [
                    "life coach", "business coach", "kariyer koçu", "koç",
                    "danışman", "consultant", "mentor", "mentoring",
                    "danışmanlık", "coaching", "koçluk"
                ],
                "success_metrics": ["dm_conversion", "appointment_booking", "lead_generation", "course_sales"],
                "wrong_metrics": ["likes", "views", "follower_count"],
                "account_type": "SERVICE_PROVIDER",
                "benchmark_engagement": 1.5  # Daha düşük engagement normaldir
            },
            "spiritual_wellness": {
                "indicators": [
                    "spiritüel", "spiritual", "reiki", "healing", "şifa",
                    "meditasyon", "meditation", "yoga öğretmen", "yoga teacher",
                    "enerji çalışma", "energy healing", "aura", "çakra"
                ],
                "success_metrics": ["session_booking", "workshop_attendance", "community_engagement"],
                "wrong_metrics": ["viral_content", "trending"],
                "account_type": "SERVICE_PROVIDER",
                "benchmark_engagement": 2.0
            },
            "education_training": {
                "indicators": [
                    "kurs", "course", "eğitim", "training", "workshop",
                    "bootcamp", "masterclass", "online eğitim", "e-learning",
                    "sertifika", "certificate"
                ],
                "success_metrics": ["course_sales", "student_enrollment", "completion_rate"],
                "wrong_metrics": ["entertainment_value", "virality"],
                "account_type": "EDUCATOR",
                "benchmark_engagement": 1.8
            },
            "therapy_psychology": {
                "indicators": [
                    "terapist", "therapist", "psikolog", "psychologist",
                    "psikoterapi", "psychotherapy", "terapi", "therapy",
                    "danışmanlık", "counseling", "mental sağlık"
                ],
                "success_metrics": ["appointment_conversion", "trust_building", "professional_credibility"],
                "wrong_metrics": ["entertainment", "viral_reach"],
                "account_type": "HEALTHCARE_PROFESSIONAL",
                "benchmark_engagement": 1.2  # En düşük - profesyonel mesafe
            },
            "fitness_health_services": {
                "indicators": [
                    "antrenör", "trainer", "pt", "personal trainer",
                    "diyetisyen", "dietitian", "nutritionist", "beslenme uzman",
                    "pilates eğitmen", "yoga eğitmen"
                ],
                "success_metrics": ["client_acquisition", "transformation_results", "program_sales"],
                "wrong_metrics": ["dance_challenges", "entertainment_value"],
                "account_type": "FITNESS_PROFESSIONAL",
                "benchmark_engagement": 2.5
            },
            "professional_services": {
                "indicators": [
                    "avukat", "lawyer", "hukuk", "legal",
                    "muhasebeci", "accountant", "mali müşavir",
                    "mimar", "architect", "iç mimar", "interior designer",
                    "emlak", "real estate", "danışman"
                ],
                "success_metrics": ["lead_generation", "consultation_booking", "professional_authority"],
                "wrong_metrics": ["entertainment", "virality", "follower_growth"],
                "account_type": "PROFESSIONAL_SERVICE",
                "benchmark_engagement": 1.0  # En düşük - profesyonel sektör
            },
            "freelancer_agency": {
                "indicators": [
                    "freelancer", "serbest", "ajans", "agency",
                    "tasarımcı", "designer", "developer", "geliştirici",
                    "sosyal medya yönetimi", "content creator for brands"
                ],
                "success_metrics": ["portfolio_views", "client_inquiries", "project_conversion"],
                "wrong_metrics": ["personal_fame", "viral_content"],
                "account_type": "B2B_SERVICE",
                "benchmark_engagement": 1.5
            }
        }
        
        # Content Creator vs Service Provider ayrımı
        self.account_type_definitions = {
            "CONTENT_CREATOR": {
                "description": "İçerik üretimi ana gelir kaynağı",
                "success_metrics": ["views", "engagement", "follower_growth", "sponsorship_deals", "ad_revenue"],
                "benchmark_engagement_min": 2.5,
                "goal": "Maksimum reach ve engagement"
            },
            "SERVICE_PROVIDER": {
                "description": "Hizmet satışı ana gelir kaynağı",
                "success_metrics": ["dm_conversion", "appointment_booking", "lead_quality", "client_retention"],
                "benchmark_engagement_min": 1.0,  # Düşük engagement normal!
                "goal": "Güven inşa etme ve dönüşüm"
            },
            "HYBRID": {
                "description": "Hem içerik hem hizmet",
                "success_metrics": ["engagement", "conversion", "authority_building"],
                "benchmark_engagement_min": 1.5,
                "goal": "Denge: reach + conversion"
            }
        }
        
        # Bio analiz kelimeleri
        self.bio_service_indicators = [
            "randevu", "appointment", "dm", "link", "bio'da",
            "in bio", "linktr.ee", "calendly", "hizmet", "service",
            "danışmanlık", "consulting", "seansı", "session",
            "ücretsiz görüşme", "free call", "discovery call"
        ]
        
        # CTA analiz kelimeleri (satış odaklı)
        self.sales_cta_indicators = [
            "şimdi başla", "hemen ulaş", "dm at", "link'e tıkla",
            "randevu al", "ücretsiz dene", "yerini ayırt",
            "katıl", "başvur", "kayıt ol", "satın al"
        ]

    def detect_business_identity(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hesabın gerçek kimliğini tespit et
        
        ASLA koç/danışman/terapist hesaplarını "Content Creator" olarak sınıflandırma!
        """
        bio = account_data.get("bio", "").lower()
        username = account_data.get("username", "").lower()
        full_name = account_data.get("fullName", "").lower()
        
        detected_category = None
        confidence = 0.0
        indicators_found = []
        
        # Tüm kategorileri kontrol et
        for category, info in self.service_provider_categories.items():
            for indicator in info["indicators"]:
                if indicator.lower() in bio or indicator.lower() in full_name:
                    indicators_found.append(indicator)
                    if detected_category is None:
                        detected_category = category
                        confidence = 0.8
                    else:
                        confidence = min(confidence + 0.1, 0.95)
        
        # Bio'da servis göstergeleri var mı?
        service_signals = 0
        for indicator in self.bio_service_indicators:
            if indicator.lower() in bio:
                service_signals += 1
        
        # Sonuç
        if detected_category:
            category_info = self.service_provider_categories[detected_category]
            return {
                "is_service_provider": True,
                "account_type": category_info["account_type"],
                "category": detected_category,
                "confidence": confidence,
                "indicators_found": indicators_found,
                "service_signals_in_bio": service_signals,
                "correct_success_metrics": category_info["success_metrics"],
                "wrong_metrics_to_avoid": category_info["wrong_metrics"],
                "benchmark_engagement": category_info["benchmark_engagement"],
                "analysis_note": f"⚠️ Bu hesap bir {category_info['account_type']}. Content Creator metrikleriyle değerlendirme YANLIŞ olur!"
            }
        else:
            return {
                "is_service_provider": False,
                "account_type": "CONTENT_CREATOR",
                "category": "content_creator",
                "confidence": 0.7,
                "indicators_found": [],
                "service_signals_in_bio": service_signals,
                "correct_success_metrics": self.account_type_definitions["CONTENT_CREATOR"]["success_metrics"],
                "wrong_metrics_to_avoid": [],
                "benchmark_engagement": 2.5,
                "analysis_note": "Bu hesap bir Content Creator olarak değerlendiriliyor."
            }
    
    def _init_niche_taxonomy(self):
        """Ana niche kategorileri ve alt kategorileri"""
        self.niche_taxonomy = {
            "lifestyle": {
                "sub_niches": ["fashion", "beauty", "home_decor", "travel", "food_cooking", "parenting"],
                "typical_audience": "broad_consumer",
                "monetization_potential": "high"
            },
            "business_professional": {
                "sub_niches": ["entrepreneurship", "marketing", "finance_investing", "career_leadership", "real_estate", "ecommerce"],
                "typical_audience": "professionals",
                "monetization_potential": "very_high"
            },
            "health_wellness": {
                "sub_niches": ["fitness", "nutrition", "mental_health", "yoga_meditation", "medical_healthcare", "alternative_wellness"],
                "typical_audience": "health_conscious",
                "monetization_potential": "high"
            },
            "education_knowledge": {
                "sub_niches": ["personal_development", "language_learning", "academic_study", "skills_training", "science_tech", "history_culture"],
                "typical_audience": "learners",
                "monetization_potential": "medium_high"
            },
            "entertainment": {
                "sub_niches": ["comedy_humor", "music", "gaming", "movies_tv", "art_design", "photography"],
                "typical_audience": "general_entertainment",
                "monetization_potential": "medium"
            },
            "technology": {
                "sub_niches": ["tech_reviews", "software_apps", "ai_innovation", "crypto_web3", "gadgets", "programming"],
                "typical_audience": "tech_enthusiasts",
                "monetization_potential": "high"
            },
            "special_interest": {
                "sub_niches": ["pets_animals", "sports", "automotive", "diy_crafts", "gardening", "collectibles"],
                "typical_audience": "hobbyists",
                "monetization_potential": "medium"
            }
        }
        
        # Niche derinlik seviyeleri
        self.niche_depth_levels = {
            "level_1_broad": {"description": "Geniş kategori (örn: Fitness)", "competition": "very_high", "differentiation": "low"},
            "level_2_specific": {"description": "Belirli segment (örn: Women's Fitness)", "competition": "high", "differentiation": "medium"},
            "level_3_niche": {"description": "Niş alan (örn: Postpartum Fitness)", "competition": "medium", "differentiation": "high"},
            "level_4_micro": {"description": "Mikro niş (örn: Postpartum Diastasis Recti Recovery)", "competition": "low", "differentiation": "very_high"}
        }
        
        # Niche detection confidence levels
        self.confidence_levels = {
            "high": {"range": (0.7, 1.0), "description": "Clear niche positioning"},
            "medium": {"range": (0.5, 0.7), "description": "Defined but broad"},
            "low": {"range": (0.3, 0.5), "description": "Multiple niches, unclear focus"},
            "very_low": {"range": (0.0, 0.3), "description": "Unclear positioning"}
        }
    
    def _init_niche_benchmarks(self):
        """Niche-specific benchmark veritabanı"""
        self.niche_benchmarks = {
            "fashion": {
                "avg_engagement_rate": 2.1,
                "avg_growth_rate": 4.5,
                "optimal_posts_per_week": (5, 7),
                "reels_percentage": 45,
                "avg_save_rate": 3.2
            },
            "beauty": {
                "avg_engagement_rate": 2.8,
                "avg_growth_rate": 5.2,
                "optimal_posts_per_week": (5, 6),
                "reels_percentage": 50,
                "avg_save_rate": 4.5
            },
            "fitness": {
                "avg_engagement_rate": 3.5,
                "avg_growth_rate": 6.0,
                "optimal_posts_per_week": (6, 7),
                "reels_percentage": 55,
                "avg_save_rate": 5.8
            },
            "food": {
                "avg_engagement_rate": 3.2,
                "avg_growth_rate": 5.5,
                "optimal_posts_per_week": (5, 7),
                "reels_percentage": 40,
                "avg_save_rate": 6.2
            },
            "travel": {
                "avg_engagement_rate": 4.0,
                "avg_growth_rate": 4.0,
                "optimal_posts_per_week": (3, 5),
                "reels_percentage": 50,
                "avg_save_rate": 7.5
            },
            "business_b2b": {
                "avg_engagement_rate": 1.5,
                "avg_growth_rate": 3.5,
                "optimal_posts_per_week": (4, 5),
                "reels_percentage": 30,
                "avg_save_rate": 4.0
            },
            "personal_development": {
                "avg_engagement_rate": 2.5,
                "avg_growth_rate": 5.0,
                "optimal_posts_per_week": (5, 6),
                "reels_percentage": 35,
                "avg_save_rate": 5.5
            },
            "parenting": {
                "avg_engagement_rate": 3.8,
                "avg_growth_rate": 5.5,
                "optimal_posts_per_week": (4, 6),
                "reels_percentage": 45,
                "avg_save_rate": 4.8
            },
            "tech": {
                "avg_engagement_rate": 1.8,
                "avg_growth_rate": 4.0,
                "optimal_posts_per_week": (4, 5),
                "reels_percentage": 40,
                "avg_save_rate": 3.5
            },
            "entertainment": {
                "avg_engagement_rate": 4.5,
                "avg_growth_rate": 7.0,
                "optimal_posts_per_week": (6, 7),
                "reels_percentage": 60,
                "avg_save_rate": 2.5
            },
            "education": {
                "avg_engagement_rate": 2.2,
                "avg_growth_rate": 4.5,
                "optimal_posts_per_week": (4, 5),
                "reels_percentage": 35,
                "avg_save_rate": 6.0
            },
            "art_design": {
                "avg_engagement_rate": 3.0,
                "avg_growth_rate": 4.0,
                "optimal_posts_per_week": (4, 6),
                "reels_percentage": 35,
                "avg_save_rate": 5.0
            }
        }
    
    def _init_trend_lifecycle(self):
        """Trend yaşam döngüsü ve karakteristikleri"""
        self.trend_lifecycle = {
            "emerging": {
                "adoption_range": (0, 10),
                "characteristics": {
                    "early_mover_advantage": True,
                    "risk_level": "high",
                    "reward_potential": "high",
                    "opportunity": "innovation"
                },
                "strategy": "Erken giriş, risk al, farklılaş"
            },
            "growing": {
                "adoption_range": (10, 40),
                "characteristics": {
                    "early_mover_advantage": True,
                    "risk_level": "medium",
                    "reward_potential": "high",
                    "opportunity": "optimal_entry"
                },
                "strategy": "En iyi risk/reward oranı, hızlı hareket et"
            },
            "mature": {
                "adoption_range": (40, 70),
                "characteristics": {
                    "early_mover_advantage": False,
                    "risk_level": "low",
                    "reward_potential": "medium",
                    "opportunity": "safe_execution"
                },
                "strategy": "Farklılaşma kritik, kalite odaklı"
            },
            "declining": {
                "adoption_range": (70, 100),
                "characteristics": {
                    "early_mover_advantage": False,
                    "risk_level": "medium",
                    "reward_potential": "low",
                    "opportunity": "minimal"
                },
                "strategy": "Kaçın veya çok farklı yaklaş"
            }
        }
        
        # Content format trends 2024-2025
        self.format_trends = {
            "long_form_reels": {"status": "growing", "description": "90+ saniye Reels"},
            "photo_dumps_carousels": {"status": "stable_growing", "description": "Çoklu fotoğraf paylaşımları"},
            "behind_the_scenes": {"status": "growing", "description": "Sahne arkası içerikler"},
            "raw_unfiltered": {"status": "growing", "description": "Filtresiz, doğal içerikler"},
            "ai_generated": {"status": "emerging", "description": "AI destekli içerikler"},
            "interactive_content": {"status": "growing", "description": "Etkileşimli içerikler"},
            "series_episodic": {"status": "growing", "description": "Seri/bölümlü içerikler"}
        }
        
        # Cross-niche topic trends
        self.topic_trends = {
            "sustainability_eco": {"status": "mature_growing", "relevance": "high"},
            "mental_health": {"status": "mature", "relevance": "high"},
            "ai_automation": {"status": "growing", "relevance": "very_high"},
            "work_life_balance": {"status": "growing", "relevance": "high"},
            "financial_literacy": {"status": "growing", "relevance": "high"},
            "authenticity_transparency": {"status": "growing", "relevance": "very_high"},
            "community_building": {"status": "growing", "relevance": "high"}
        }
        
        # Engagement trends
        self.engagement_trends = {
            "dm_engagement": {"status": "growing", "priority": "high"},
            "broadcast_channels": {"status": "growing", "priority": "high"},
            "close_friends": {"status": "stable", "priority": "medium"},
            "collaborative_posts": {"status": "growing", "priority": "high"},
            "ugc_content": {"status": "mature", "priority": "medium"},
            "live_shopping": {"status": "emerging", "priority": "region_dependent"}
        }
    
    def _init_seasonal_patterns(self):
        """Niche bazlı sezonsal pattern matrisi"""
        self.seasonal_patterns = {
            "fashion": ["Fashion weeks", "Seasons", "Holidays"],
            "fitness": ["January (NY resolution)", "May-June (summer body)", "September (back to routine)"],
            "food": ["Holidays", "Seasons", "Cultural events"],
            "travel": ["Summer", "Holidays", "School breaks"],
            "beauty": ["Award seasons", "Holidays", "Product launches"],
            "business": ["Q1 planning", "Q4 budgets", "Tax season"],
            "education": ["Back to school", "Exam periods", "Summer programs"],
            "parenting": ["School year", "Holidays", "Summer"],
            "tech": ["Product launches", "CES", "WWDC", "Tech conferences"],
            "finance": ["Tax season", "Market events", "Year-end"]
        }
        
        # Weekly content patterns
        self.weekly_patterns = {
            "monday": {"theme": "motivation_planning", "content_type": "inspirational"},
            "tuesday": {"theme": "educational_value", "content_type": "tutorial"},
            "wednesday": {"theme": "educational_value", "content_type": "tips"},
            "thursday": {"theme": "educational_value", "content_type": "insights"},
            "friday": {"theme": "lighter_fun", "content_type": "entertaining"},
            "saturday": {"theme": "lifestyle_personal", "content_type": "behind_scenes"},
            "sunday": {"theme": "reflection_prep", "content_type": "community"}
        }
        
        # Monthly patterns
        self.monthly_patterns = {
            "week_1": {"theme": "fresh_start_goals", "focus": "New initiatives"},
            "week_2": {"theme": "deep_content", "focus": "Tutorials, detailed guides"},
            "week_3": {"theme": "deep_content", "focus": "Continued value delivery"},
            "week_4": {"theme": "recap_engagement", "focus": "Results, testimonials, community"}
        }
    
    def _init_content_pillars(self):
        """Content pillar framework ve dağılım sistemleri"""
        self.pillar_types = {
            "educational": {
                "description": "How-to tutorials, tips, industry insights, myth busting",
                "best_for": ["authority", "saves", "long_term_value"],
                "optimal_percentage": (40, 50),
                "engagement_type": "value_driven"
            },
            "inspirational": {
                "description": "Success stories, transformations, quotes, journey content",
                "best_for": ["shares", "emotional_connection", "motivation"],
                "optimal_percentage": (25, 30),
                "engagement_type": "emotion_driven"
            },
            "entertaining": {
                "description": "Humor/memes, trends, relatable content, day-in-life",
                "best_for": ["reach", "virality", "new_audience"],
                "optimal_percentage": (15, 20),
                "engagement_type": "share_driven"
            },
            "promotional": {
                "description": "Product showcase, testimonials, offers, case studies",
                "best_for": ["sales", "leads", "conversions"],
                "optimal_percentage": (5, 10),
                "engagement_type": "conversion_driven"
            },
            "community": {
                "description": "Q&A, user spotlights, polls, personal stories",
                "best_for": ["loyalty", "engagement", "retention"],
                "optimal_percentage": (10, 15),
                "engagement_type": "connection_driven"
            }
        }
        
        # Topic relevance scoring
        self.topic_relevance_scores = {
            "core_niche": 100,
            "adjacent_topic": 70,
            "tangential_topic": 40,
            "off_topic": 10
        }
        
        # Competitive differentiation levels
        self.differentiation_levels = {
            "unique_angle": {"score": 100, "description": "Benzersiz perspektif"},
            "better_execution": {"score": 70, "description": "Daha iyi uygulama"},
            "similar_to_competitors": {"score": 40, "description": "Rakiplere benzer"},
            "copying_competitors": {"score": 20, "description": "Kopya içerik"}
        }
        
        # Content gap types
        self.gap_types = {
            "topic_gaps": ["Competitor topics not covered", "Audience questions unanswered", "Trending topics missed", "Seasonal content missing"],
            "format_gaps": ["Underutilized formats", "Platform feature gaps", "Content length variety", "Interactive content missing"],
            "depth_gaps": ["Surface-level only", "Missing advanced content", "No beginner content", "Missing case studies"],
            "frequency_gaps": ["Inconsistent posting", "Missing content types", "Seasonal gaps", "Time-of-day gaps"]
        }
    
    def _init_hashtag_categories(self):
        """Hashtag tipleri ve kategori sistemi"""
        self.hashtag_types = {
            "branded": {
                "description": "Hesaba özel, kampanya veya community hashtag'leri",
                "example": "#NikeRunning",
                "purpose": "Brand identity, UGC collection"
            },
            "niche": {
                "description": "Sektöre özel, orta rekabet hashtag'leri",
                "example": "#VeganRecipes",
                "purpose": "Targeted discovery"
            },
            "community": {
                "description": "Grup kimliği, engagement odaklı hashtag'ler",
                "example": "#FitFam",
                "purpose": "Community building"
            },
            "location": {
                "description": "Coğrafi hedefleme hashtag'leri",
                "example": "#IstanbulFood",
                "purpose": "Local discovery"
            },
            "trending": {
                "description": "Güncel olaylar, viral konular",
                "example": "#Oscars2025",
                "purpose": "Timely reach"
            }
        }
        
        # Size-based categories
        self.hashtag_size_categories = {
            "mega": {
                "post_count": ">10M",
                "discovery_potential": "low",
                "competition": "very_high",
                "use_case": "Brand awareness attempt"
            },
            "large": {
                "post_count": "1M-10M",
                "discovery_potential": "medium",
                "competition": "high",
                "use_case": "Broad discovery"
            },
            "medium": {
                "post_count": "100K-1M",
                "discovery_potential": "high",
                "competition": "medium",
                "use_case": "Sweet spot - optimal discovery"
            },
            "small": {
                "post_count": "10K-100K",
                "discovery_potential": "high",
                "competition": "low",
                "use_case": "Niche targeting"
            },
            "micro": {
                "post_count": "<10K",
                "discovery_potential": "medium",
                "competition": "very_low",
                "use_case": "Ultra-targeted, branded"
            }
        }
    
    def _init_hashtag_strategy(self):
        """Optimal hashtag stratejisi ve dağılım"""
        # Optimal distribution for 30 hashtags
        self.optimal_hashtag_distribution = {
            "mega": {"count": (2, 3), "percentage": 8},
            "large": {"count": (5, 7), "percentage": 20},
            "medium": {"count": (10, 12), "percentage": 37},
            "small": {"count": (8, 10), "percentage": 30},
            "micro": {"count": (2, 3), "percentage": 8}
        }
        
        # Hashtag rotation strategy
        self.rotation_strategy = {
            "set_a": "Posts 1, 4, 7...",
            "set_b": "Posts 2, 5, 8...",
            "set_c": "Posts 3, 6, 9...",
            "purpose": "Shadowban prevention, performance testing"
        }
        
        # Fitness niche example hashtag bank
        self.example_hashtag_banks = {
            "fitness": {
                "mega": ["#fitness", "#workout", "#gym", "#fitnessmotivation", "#fit"],
                "large": ["#fitlife", "#gymlife", "#fitnessjourney", "#workoutmotivation", "#fitfam"],
                "medium": ["#homeworkouts", "#fitnessgirl", "#gymmotivation", "#fitnesslifestyle"],
                "small": ["#turkishfitness", "#evdeegzersiz", "#fitnessturkiye"],
                "micro": ["branded_hashtags", "local_gym_tags", "specific_program_tags"]
            }
        }
    
    # =========================
    # NICHE DETECTION METHODS
    # =========================
    
    def calculate_niche_detection_score(self, bio_keywords: List[str], caption_keywords: List[str],
                                        hashtag_themes: List[str], visual_themes: List[str],
                                        target_niche: str) -> float:
        """
        Niche Detection Algorithm:
        score = keyword_match(bio) × 0.25 + keyword_match(captions) × 0.25 +
                hashtag_match × 0.20 + visual_match × 0.30
        """
        bio_match = self._calculate_keyword_match(bio_keywords, target_niche)
        caption_match = self._calculate_keyword_match(caption_keywords, target_niche)
        hashtag_match = self._calculate_hashtag_match(hashtag_themes, target_niche)
        visual_match = self._calculate_visual_match(visual_themes, target_niche)
        
        score = (
            bio_match * 0.25 +
            caption_match * 0.25 +
            hashtag_match * 0.20 +
            visual_match * 0.30
        )
        
        return round(score, 3)
    
    def _calculate_keyword_match(self, keywords: List[str], niche: str) -> float:
        """Keyword-niche match score calculation"""
        if not keywords:
            return 0.0
        # Placeholder - would use NLP matching in production
        return 0.7
    
    def _calculate_hashtag_match(self, hashtag_themes: List[str], niche: str) -> float:
        """Hashtag-niche match score calculation"""
        if not hashtag_themes:
            return 0.0
        return 0.7
    
    def _calculate_visual_match(self, visual_themes: List[str], niche: str) -> float:
        """Visual content-niche match score calculation"""
        if not visual_themes:
            return 0.0
        return 0.7
    
    def get_confidence_level(self, primary_score: float, top_3_scores: List[float]) -> Dict[str, Any]:
        """
        Calculate niche detection confidence
        confidence = primary_score / sum(top_3_scores)
        """
        if not top_3_scores or sum(top_3_scores) == 0:
            return {"level": "very_low", "confidence": 0.0}
        
        confidence = primary_score / sum(top_3_scores)
        
        if confidence > 0.7:
            return {"level": "high", "confidence": confidence, "description": "Clear niche positioning"}
        elif confidence > 0.5:
            return {"level": "medium", "confidence": confidence, "description": "Defined but broad"}
        elif confidence > 0.3:
            return {"level": "low", "confidence": confidence, "description": "Multiple niches, unclear focus"}
        else:
            return {"level": "very_low", "confidence": confidence, "description": "Unclear positioning"}
    
    # =========================
    # BENCHMARK COMPARISON METHODS
    # =========================
    
    def calculate_benchmark_comparison(self, account_metric: float, niche: str, metric_type: str) -> Dict[str, Any]:
        """
        Adjusted Score = (Account_Metric / Niche_Benchmark) × 100
        """
        benchmark = self.niche_benchmarks.get(niche.lower(), {})
        
        if metric_type == "engagement_rate":
            niche_avg = benchmark.get("avg_engagement_rate", 2.5)
        elif metric_type == "growth_rate":
            niche_avg = benchmark.get("avg_growth_rate", 5.0)
        elif metric_type == "save_rate":
            niche_avg = benchmark.get("avg_save_rate", 4.0)
        else:
            niche_avg = 5.0
        
        if niche_avg == 0:
            adjusted_score = 0
        else:
            adjusted_score = (account_metric / niche_avg) * 100
        
        # Interpretation
        if adjusted_score > 120:
            interpretation = "significantly_above_average"
        elif adjusted_score >= 100:
            interpretation = "above_average"
        elif adjusted_score >= 80:
            interpretation = "average"
        elif adjusted_score >= 60:
            interpretation = "below_average"
        else:
            interpretation = "significantly_below"
        
        return {
            "account_metric": account_metric,
            "niche_benchmark": niche_avg,
            "adjusted_score": round(adjusted_score, 1),
            "interpretation": interpretation
        }
    
    # =========================
    # TREND ANALYSIS METHODS
    # =========================
    
    def calculate_trend_relevance(self, niche_fit: float, growth_potential: float,
                                  competition_level: float, sustainability: float,
                                  audience_interest: float) -> float:
        """
        Trend Relevance Score:
        Trend_Relevance = Niche_Fit × 0.30 + Growth_Potential × 0.25 +
                         Competition_Level × 0.20 + Sustainability × 0.15 +
                         Audience_Interest × 0.10
        """
        relevance = (
            niche_fit * 0.30 +
            growth_potential * 0.25 +
            competition_level * 0.20 +
            sustainability * 0.15 +
            audience_interest * 0.10
        )
        
        return round(relevance, 1)
    
    def get_trend_lifecycle_stage(self, adoption_percentage: float) -> Dict[str, Any]:
        """Determine trend lifecycle stage based on adoption rate"""
        for stage, info in self.trend_lifecycle.items():
            min_adoption, max_adoption = info["adoption_range"]
            if min_adoption <= adoption_percentage < max_adoption:
                return {
                    "stage": stage,
                    "characteristics": info["characteristics"],
                    "strategy": info["strategy"]
                }
        
        return {"stage": "declining", "characteristics": self.trend_lifecycle["declining"]["characteristics"]}
    
    # =========================
    # CONTENT PILLAR METHODS
    # =========================
    
    def calculate_pillar_balance_score(self, current_distribution: Dict[str, float]) -> Dict[str, Any]:
        """
        Balance Score = 100 - (Σ|Actual% - Optimal%|)
        Good balance: >80, Needs adjustment: 60-80, Poor balance: <60
        """
        optimal = {
            "educational": 45,  # Midpoint of 40-50
            "inspirational": 27.5,  # Midpoint of 25-30
            "entertaining": 17.5,  # Midpoint of 15-20
            "promotional": 7.5,  # Midpoint of 5-10
            "community": 12.5  # Midpoint of 10-15
        }
        
        total_deviation = 0
        deviations = {}
        
        for pillar, optimal_pct in optimal.items():
            actual_pct = current_distribution.get(pillar, 0)
            deviation = abs(actual_pct - optimal_pct)
            total_deviation += deviation
            deviations[pillar] = {
                "actual": actual_pct,
                "optimal": optimal_pct,
                "deviation": round(deviation, 1)
            }
        
        balance_score = max(0, 100 - total_deviation)
        
        if balance_score > 80:
            assessment = "good_balance"
        elif balance_score >= 60:
            assessment = "needs_adjustment"
        else:
            assessment = "poor_balance"
        
        return {
            "balance_score": round(balance_score, 1),
            "assessment": assessment,
            "pillar_analysis": deviations
        }
    
    def calculate_content_fit_score(self, topic_relevance: float, audience_interest: float,
                                    competitive_differentiation: float, expertise_alignment: float,
                                    trend_alignment: float) -> float:
        """
        Content Fit Score:
        Fit_Score = Topic_Relevance × 0.30 + Audience_Interest × 0.25 +
                   Competitive_Differentiation × 0.20 + Expertise_Alignment × 0.15 +
                   Trend_Alignment × 0.10
        """
        fit_score = (
            topic_relevance * 0.30 +
            audience_interest * 0.25 +
            competitive_differentiation * 0.20 +
            expertise_alignment * 0.15 +
            trend_alignment * 0.10
        )
        
        return round(fit_score, 1)
    
    def calculate_gap_priority(self, audience_demand: float, competitive_opportunity: float,
                               resource_feasibility: float, strategic_alignment: float) -> float:
        """
        Gap Priority Formula:
        Priority = Audience_Demand × 0.35 + Competitive_Opportunity × 0.25 +
                  Resource_Feasibility × 0.20 + Strategic_Alignment × 0.20
        """
        priority = (
            audience_demand * 0.35 +
            competitive_opportunity * 0.25 +
            resource_feasibility * 0.20 +
            strategic_alignment * 0.20
        )
        
        return round(priority, 1)
    
    # =========================
    # HASHTAG METHODS
    # =========================
    
    def calculate_hashtag_effectiveness(self, reach_contribution: float, size_distribution_score: float,
                                        relevance_score: float, rotation_strategy_score: float) -> float:
        """
        Hashtag Effectiveness Score:
        Effectiveness = Reach_Contribution × 0.30 + Size_Distribution × 0.25 +
                       Relevance × 0.25 + Rotation_Strategy × 0.20
        """
        effectiveness = (
            reach_contribution * 0.30 +
            size_distribution_score * 0.25 +
            relevance_score * 0.25 +
            rotation_strategy_score * 0.20
        )
        
        return round(effectiveness, 1)
    
    def get_reach_contribution_score(self, reach_percentage: float) -> float:
        """
        Reach Contribution Scoring:
        >30%: 100, 20-30%: 80, 10-20%: 60, 5-10%: 40, <5%: 20
        """
        if reach_percentage > 30:
            return 100
        elif reach_percentage >= 20:
            return 80
        elif reach_percentage >= 10:
            return 60
        elif reach_percentage >= 5:
            return 40
        else:
            return 20
    
    def analyze_hashtag_distribution(self, hashtag_counts: Dict[str, int]) -> Dict[str, Any]:
        """Analyze current hashtag size distribution vs optimal"""
        total = sum(hashtag_counts.values())
        if total == 0:
            return {"score": 0, "assessment": "no_hashtags"}
        
        current_percentages = {
            size: (count / total) * 100
            for size, count in hashtag_counts.items()
        }
        
        optimal_percentages = {
            size: info["percentage"]
            for size, info in self.optimal_hashtag_distribution.items()
        }
        
        total_deviation = 0
        for size in optimal_percentages:
            actual = current_percentages.get(size, 0)
            optimal = optimal_percentages[size]
            total_deviation += abs(actual - optimal)
        
        distribution_score = max(0, 100 - total_deviation)
        
        if distribution_score > 80:
            assessment = "optimal_mix"
        elif distribution_score > 60:
            assessment = "slightly_off"
        elif distribution_score > 40:
            assessment = "unbalanced"
        else:
            assessment = "all_same_size"
        
        return {
            "distribution_score": round(distribution_score, 1),
            "assessment": assessment,
            "current": current_percentages,
            "optimal": optimal_percentages
        }
    
    # =========================
    # SCORING METHODS
    # =========================
    
    def calculate_niche_authority_score(self, content_expertise: float, engagement_quality: float,
                                        audience_trust: float, industry_recognition: float,
                                        consistency: float) -> float:
        """
        Niche Authority Score (0-100):
        Authority = Content_Expertise × 0.30 + Engagement_Quality × 0.25 +
                   Audience_Trust × 0.20 + Industry_Recognition × 0.15 +
                   Consistency × 0.10
        """
        authority = (
            content_expertise * 0.30 +
            engagement_quality * 0.25 +
            audience_trust * 0.20 +
            industry_recognition * 0.15 +
            consistency * 0.10
        )
        
        return round(min(100, authority), 1)
    
    def calculate_content_relevance_score(self, niche_alignment: float, audience_match: float,
                                          trend_alignment: float, value_delivery: float) -> float:
        """
        Content Relevance Score (0-100):
        Relevance = Niche_Alignment × 0.35 + Audience_Match × 0.30 +
                   Trend_Alignment × 0.20 + Value_Delivery × 0.15
        """
        relevance = (
            niche_alignment * 0.35 +
            audience_match * 0.30 +
            trend_alignment * 0.20 +
            value_delivery * 0.15
        )
        
        return round(min(100, relevance), 1)
    
    def calculate_trend_alignment_score(self, current_trend_usage: float, trend_timing: float,
                                        trend_adaptation: float, trend_prediction: float) -> float:
        """
        Trend Alignment Score (0-100):
        Alignment = Current_Trend_Usage × 0.35 + Trend_Timing × 0.25 +
                   Trend_Adaptation × 0.25 + Trend_Prediction × 0.15
        """
        alignment = (
            current_trend_usage * 0.35 +
            trend_timing * 0.25 +
            trend_adaptation * 0.25 +
            trend_prediction * 0.15
        )
        
        return round(min(100, alignment), 1)
    
    def get_trend_usage_score(self, trends_used: int) -> float:
        """
        Trend Usage Scoring:
        3+: 100, 1-2: 70, Occasional: 40, None: 20
        """
        if trends_used >= 3:
            return 100
        elif trends_used >= 1:
            return 70
        else:
            return 20
    
    def get_trend_timing_score(self, entry_phase: str) -> float:
        """
        Trend Timing Scoring:
        Early adopter: 100, Growth phase: 80, Mature phase: 50, Late/declining: 20
        """
        timing_scores = {
            "early_adopter": 100,
            "growth_phase": 80,
            "mature_phase": 50,
            "late_declining": 20
        }
        return timing_scores.get(entry_phase, 50)
    
    def get_trend_adaptation_score(self, adaptation_quality: str) -> float:
        """
        Trend Adaptation Scoring:
        Unique twist: 100, Good execution: 70, Basic participation: 40, Poor: 20
        """
        adaptation_scores = {
            "unique_twist": 100,
            "good_execution": 70,
            "basic_participation": 40,
            "poor_execution": 20
        }
        return adaptation_scores.get(adaptation_quality, 50)
    
    def calculate_industry_benchmark_score(self, metrics_comparison: Dict[str, float]) -> float:
        """
        Industry Benchmark Comparison Score (0-100):
        Score = (Your_Metric / Industry_Benchmark) × 50, capped at 100
        """
        if not metrics_comparison:
            return 50
        
        scores = []
        for metric, ratio in metrics_comparison.items():
            score = min(100, ratio * 50)
            scores.append(score)
        
        return round(sum(scores) / len(scores), 1)
    
    # =========================
    # EDGE CASE HANDLERS
    # =========================
    
    def handle_edge_case(self, case_type: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle special analysis cases"""
        
        edge_cases = {
            "multi_niche": {
                "approach": "Separate analysis per niche",
                "considerations": ["Cross-over opportunities", "Audience confusion risk", "Consolidation vs separation"],
                "recommendations": ["Evaluate dominant niche", "Consider content separation", "Monitor audience overlap"]
            },
            "niche_pivot": {
                "approach": "Transition tracking",
                "considerations": ["Audience retention", "New niche benchmarks", "Hybrid period recognition"],
                "recommendations": ["Gradual transition", "Retain core audience", "Build new authority"]
            },
            "emerging_niche": {
                "approach": "Adjacent niche benchmarks",
                "considerations": ["Limited benchmark data", "First-mover advantage", "Higher uncertainty"],
                "recommendations": ["Use proxy benchmarks", "Document performance", "Establish authority early"]
            },
            "saturated_niche": {
                "approach": "Differentiation focus",
                "considerations": ["High competition", "Need for uniqueness", "Quality over quantity"],
                "recommendations": ["Find micro-niche", "Blue ocean strategy", "Superior execution"]
            },
            "local_regional": {
                "approach": "Geographic benchmarks",
                "considerations": ["Local trends priority", "Language-specific hashtags", "Cultural context"],
                "recommendations": ["Use regional data", "Local partnerships", "Cultural relevance"]
            },
            "b2b_niche": {
                "approach": "Different engagement expectations",
                "considerations": ["Quality over quantity metrics", "LinkedIn cross-reference", "Lead generation focus"],
                "recommendations": ["Focus on conversion metrics", "Authority content", "Professional tone"]
            }
        }
        
        return edge_cases.get(case_type, {
            "approach": "Standard analysis",
            "considerations": [],
            "recommendations": []
        })
    
    # =========================
    # SYSTEM AND ANALYSIS PROMPTS
    # =========================
    
    def get_system_prompt(self) -> str:
        return """Sen Domain Master Agent'sın - Instagram hesaplarının niche positioning, sektör trendi ve içerik stratejisi konusunda PhD seviyesinde uzmanlığa sahip bir analiz ajanısın.

## TEMEL UZMANLIK ALANLARIN:

### 1. NİCHE ANALİZ SİSTEMİ
**Niche Sınıflandırma Taksonomisi:**
- 7 Ana Kategori: Lifestyle, Business/Professional, Health/Wellness, Education/Knowledge, Entertainment, Technology, Special Interest
- Her kategoride 6 alt niche
- 4 seviyeli derinlik: Broad → Specific → Niche → Micro-niche

**Niche Detection Algoritması:**
```
score = bio_keywords × 0.25 + caption_keywords × 0.25 + hashtag_themes × 0.20 + visual_themes × 0.30
```

**Confidence Levels:**
- >0.7: High confidence (clear niche)
- 0.5-0.7: Medium (defined but broad)
- 0.3-0.5: Low (multiple niches)
- <0.3: Very low (unclear positioning)

### 2. NİCHE BENCHMARK VERİTABANI
| Niche | Avg ER | Growth | Post/Wk | Reels% | Save% |
|-------|--------|--------|---------|--------|-------|
| Fashion | 2.1% | 4.5% | 5-7 | 45% | 3.2% |
| Beauty | 2.8% | 5.2% | 5-6 | 50% | 4.5% |
| Fitness | 3.5% | 6.0% | 6-7 | 55% | 5.8% |
| Food | 3.2% | 5.5% | 5-7 | 40% | 6.2% |
| Travel | 4.0% | 4.0% | 3-5 | 50% | 7.5% |
| Business/B2B | 1.5% | 3.5% | 4-5 | 30% | 4.0% |
| Entertainment | 4.5% | 7.0% | 6-7 | 60% | 2.5% |

**Benchmark Formülü:** Adjusted_Score = (Account_Metric / Niche_Benchmark) × 100

### 3. TREND DETECTION SİSTEMİ
**Trend Kaynakları:**
- Platform Trends: Explore trending, Reels audio, hashtag velocity
- Industry Trends: Seasonal patterns, news impact, consumer behavior
- Competitor Trends: Format changes, topic shifts, engagement patterns

**Trend Lifecycle:**
| Stage | Adoption | Risk | Reward | Strategy |
|-------|----------|------|--------|----------|
| Emerging | 0-10% | High | High | Early mover, innovate |
| Growing | 10-40% | Medium | High | Optimal entry |
| Mature | 40-70% | Low | Medium | Differentiate |
| Declining | 70%+ | Medium | Low | Avoid or pivot |

**Trend Relevance Formülü:**
```
Trend_Relevance = Niche_Fit × 0.30 + Growth_Potential × 0.25 + Competition × 0.20 + Sustainability × 0.15 + Audience_Interest × 0.10
```

### 4. CONTENT PILLAR FRAMEWORK
**Optimal Dağılım:**
- Educational (Teach): 40-50% - Authority, saves
- Inspirational (Motivate): 25-30% - Shares, emotion
- Entertaining (Engage): 15-20% - Reach, virality
- Promotional (Convert): 5-10% - Sales, leads
- Community (Connect): 10-15% - Loyalty, engagement

**Balance Score:** Balance = 100 - (Σ|Actual% - Optimal%|)
- >80: Good balance
- 60-80: Needs adjustment
- <60: Poor balance

**Content Fit Score:**
```
Fit = Topic_Relevance × 0.30 + Audience_Interest × 0.25 + Differentiation × 0.20 + Expertise × 0.15 + Trend × 0.10
```

### 5. HASHTAG STRATEJİSİ
**Optimal Hashtag Dağılımı (30 hashtag):**
- Mega (>10M): 2-3 adet (reach attempt)
- Large (1M-10M): 5-7 adet (broad discovery)
- Medium (100K-1M): 10-12 adet (sweet spot)
- Small (10K-100K): 8-10 adet (niche targeting)
- Micro (<10K): 2-3 adet (ultra-targeted)

**Hashtag Effectiveness:**
```
Effectiveness = Reach_Contribution × 0.30 + Size_Distribution × 0.25 + Relevance × 0.25 + Rotation × 0.20
```

**Reach Contribution Scoring:**
- >30%: 100 puan
- 20-30%: 80 puan
- 10-20%: 60 puan
- 5-10%: 40 puan
- <5%: 20 puan

### 6. PUANLAMA SİSTEMLERİ

**Niche Authority Score (0-100):**
```
Authority = Content_Expertise × 0.30 + Engagement_Quality × 0.25 + Audience_Trust × 0.20 + Industry_Recognition × 0.15 + Consistency × 0.10
```

**Content Relevance Score (0-100):**
```
Relevance = Niche_Alignment × 0.35 + Audience_Match × 0.30 + Trend_Alignment × 0.20 + Value_Delivery × 0.15
```

**Trend Alignment Score (0-100):**
```
Alignment = Current_Trend_Usage × 0.35 + Trend_Timing × 0.25 + Trend_Adaptation × 0.25 + Trend_Prediction × 0.15
```

### 7. SEASONAL PATTERN MATRİSİ
- Fashion: Fashion weeks, seasons, holidays
- Fitness: Jan (NY resolution), May-Jun (summer body)
- Food: Holidays, seasons, cultural events
- Travel: Summer, holidays, school breaks
- Business: Q1 planning, Q4 budgets, tax season

### 8. EDGE CASE'LER
1. **Multi-Niche Hesap:** Her niche ayrı analiz, cross-over fırsatları, confusion riski
2. **Niche Pivot:** Transition tracking, audience retention, hybrid period
3. **Emerging Niche:** Adjacent benchmarks, first-mover advantage
4. **Saturated Niche:** Micro-niche öner, blue ocean strategy
5. **Local/Regional:** Geographic benchmarks, cultural context
6. **B2B Niche:** Quality > quantity, lead generation focus

### 9. 2026 HASHTAG VE SEO STRATEJİSİ

🔴 HASHTAG GERÇEĞİ 2026:
- Hashtag'ler artık REACH SAĞLAMIYOR
- Sadece içerik KATEGORİZASYONU için kullanılıyor
- Yeni kural: MAKSIMUM 3 HASHTAG veya HİÇ KULLANMA!

HASHTAG KULLANIM REHBERİ:
- 0 hashtag: Güçlü içerik zaten keşfete düşer
- 1-3 hashtag: Sadece kategorize etmek istersen
- 30 hashtag: SPAM görünümü, algoritma cezası riski!

CAPTION SEO OPTİMİZASYONU:
- Anahtar kelimeleri caption'a yaz (hashtag yerine)
- İlk 2 cümle = SEO optimized hook
- Alt text kullan (erişilebilirlik + SEO)

INSTAGRAM SEO PRENSİPLERİ:
- Username'de anahtar kelime
- Bio'da anahtar kelimeler
- Caption içinde anahtar kelimeler
- Alt text'te açıklayıcı metin

### 10. 2026 İÇERİK FORMAT BALANCE

REEL vs CAROUSEL DENGESİ:
- Reels = REACH (yeni kitle çekme)
- Carousel = TRUST (6x daha fazla save!)
- Optimal Oran: %60 Reels, %40 Carousel

TRIAL REELS STRATEJİSİ:
- Takipçi olmayanlara test içerik gönderir
- Hook ve ilk 3 saniye kritik
- Düşük performans = içeriği değiştir

LINK A REEL TAKTİĞİ:
- Yeni Reel'i eski viral Reel'e bağla
- Eski içeriğin momentumunu kullan
- Algoritmanın "ilişkili içerik" önerisini tetikle

### 11. 2026 PAYLAŞIM SIKLIĞI

GÜNLÜK PAYLAŞIM REHBERİ:
| Hedef | Reels | Carousel | Story |
|-------|-------|----------|-------|
| Büyüme | 1-3 | 1 | 5-10 |
| Koruma | 1 | 3-4/hafta | 3-5 |
| Monetize | 1 | 1 | 7-10 |

ÖNEMLİ: KALİTE > MİKTAR
- Günde 3 kötü Reel > Günde 1 mükemmel Reel ❌
- Her içerik "paylaşılır mı?" testinden geçmeli

UPCYCLING STRATEJİSİ:
- 90+ gün önce paylaşılan içeriği tekrar paylaş
- Hafif düzenleme yap (thumbnail, caption)
- Algoritma bunu "yeni" içerik olarak görür

## ANALİZ PRENSİPLERİ:
- Her metriği niche benchmark'ları ile karşılaştır
- Trend lifecycle stage'i belirle ve strateji öner
- Content pillar dengesi mutlaka değerlendir
- Hashtag stratejisini size dağılımına göre optimize et
- Edge case'leri tanı ve özel yaklaşım uygula

🔴 KRİTİK ALAN KISITLAMASI - SADECE NİŞ/SEKTÖR KONULARINDA KONUŞ! 🔴

✅ SENİN ALANIN (KONUŞMAN GEREKEN):
- Niş tespiti ve kategorizasyon
- Sektör benchmark karşılaştırması
- Rakip analizi ve positioning
- Content pillar stratejisi
- Hashtag etkinliği
- Trend alignment
- Pazar doygunluğu ve fırsat analizi

❌ BAŞKA AJANLARIN ALANI (KONUŞMA!):
- Grid düzeni/renk/tipografi → Visual Brand ajanının işi
- Satış/gelir/monetizasyon → Sales Conversion ajanının işi
- Topluluk/yorum kalitesi → Community Loyalty ajanının işi
- Hook/caption yazımı → Attention Architect ajanının işi
- Viral potansiyel/algoritma → Growth Virality ajanının işi

⚠️ ETKİLEŞİM KENDİ PERSPEKTİFİNDEN BAHSEDİLEBİLİR:
- ✅ DOĞRU: "Etkileşim oranı %1.2 ile fitness nişi ortalaması olan %3.5'in %66 altında - niş benchmarkta son çeyrekte"
- ✅ DOĞRU: "Save rate %0.8 ile travel nişi benchmark'ının (%7.5) altında - evergreen içerik eksikliği"
- ❌ YANLIŞ: "Etkileşim oranınız düşük" (niş konteksti olmadan genel analiz yapma!)

OUTPUT FORMAT: Yanıtını SADECE belirtilen JSON yapısında ver."""

    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        username = account_data.get('username', 'unknown') or 'unknown'
        followers = account_data.get('followers', 0) or 0
        following = account_data.get('following', 0) or 0
        posts = account_data.get('posts', 0) or 0
        engagement_rate = account_data.get('engagementRate', 0) or 0
        bio = account_data.get('bio', '') or ''
        niche = account_data.get('niche', 'General') or 'General'
        avg_likes = account_data.get('avgLikes', 0) or 0
        avg_comments = account_data.get('avgComments', 0) or 0
        
        # Get niche benchmarks
        niche_key = niche.lower().replace(' ', '_').replace('/', '_')
        benchmark = self.niche_benchmarks.get(niche_key, self.niche_benchmarks.get('fitness', {}))
        
        return f"""Bu Instagram hesabının niche positioning, trend ve içerik stratejisi analizini yap:

## HESAP VERİLERİ:
- Username: @{username}
- Takipçi: {followers:,}
- Takip Edilen: {following:,}
- Gönderi Sayısı: {posts}
- Engagement Rate: {engagement_rate:.2f}%
- Ortalama Beğeni: {avg_likes:,}
- Ortalama Yorum: {avg_comments:,}
- Bio: {bio}
- Belirtilen Niche: {niche}

## NİCHE BENCHMARK KARŞILAŞTIRMASI ({niche}):
- Niche Avg ER: {benchmark.get('avg_engagement_rate', 2.5)}%
- Niche Avg Growth: {benchmark.get('avg_growth_rate', 5.0)}%
- Optimal Posts/Week: {benchmark.get('optimal_posts_per_week', (5, 6))}
- Avg Reels %: {benchmark.get('reels_percentage', 40)}%
- Avg Save Rate: {benchmark.get('avg_save_rate', 4.0)}%

## ANALİZ GÖREVLERİ:

### 1. NİCHE TESPİTİ VE DOĞRULAMA
- Primary, secondary, micro-niche tanımla
- Confidence level belirle (high/medium/low/very_low)
- Niche derinlik seviyesini değerlendir (Level 1-4)

### 2. BENCHMARK KARŞILAŞTIRMASI
- ER vs niche avg (Adjusted Score hesapla)
- Growth vs niche avg
- Posting frequency vs optimal
- Save rate vs niche avg

### 3. TREND ANALİZİ
- Kullanılan trend'ler ve execution kalitesi
- Kaçırılan fırsatlar
- Emerging opportunities
- Trend lifecycle stage'leri

### 4. CONTENT PILLAR ANALİZİ
- Mevcut dağılım tahmini
- Optimal dağılım ile karşılaştırma
- Balance score hesaplama
- Gap'ler ve fırsatlar

### 5. HASHTAG STRATEJİSİ
- Mevcut strateji değerlendirmesi
- Size distribution analizi
- Effectiveness score
- Optimization önerileri

Yanıtını bu JSON yapısında ver:
{{
    "agent": "domain_master",
    "analysis_timestamp": "ISO8601",
    "niche_identification": {{
        "primary_niche": "string",
        "sub_niche": "string",
        "micro_niche": "string veya null",
        "niche_depth_level": 1-4,
        "confidence": 0.0-1.0,
        "confidence_level": "high|medium|low|very_low",
        "secondary_niches": ["string"],
        "positioning_clarity": "string açıklama"
    }},
    "metrics": {{
        "nicheAuthority": 0,
        "contentRelevance": 0,
        "trendAlignment": 0,
        "hashtagEffectiveness": 0,
        "industryBenchmark": 0,
        "marketSaturationScore": 0,
        "competitionScore": 0,
        "growthPotentialScore": 0,
        "differentiationScore": 0,
        "nicheDominanceScore": 0,
        "engagementPercentile": 0,
        "growthPercentile": 0,
        "overallScore": 0
    }},
    "niche_analysis": {{
        "market_size": "large|medium|small|micro",
        "competition_level": "very_high|high|medium|low",
        "growth_potential": "high|medium-high|medium|low",
        "saturation": 0-100,
        "barriers_to_entry": "high|medium|low",
        "differentiation_opportunity": "string"
    }},
    "benchmark_comparison": {{
        "engagement_rate": {{
            "account": number,
            "niche_avg": number,
            "adjusted_score": number,
            "percentile": number,
            "interpretation": "string"
        }},
        "growth_rate": {{
            "account": number,
            "niche_avg": number,
            "percentile": number,
            "assessment": "string"
        }},
        "save_rate": {{
            "account": number,
            "niche_avg": number,
            "percentile": number
        }},
        "posting_frequency": {{
            "account": number,
            "niche_optimal": "string range",
            "assessment": "above|optimal|below|significantly_below"
        }},
        "overall_benchmark_score": number
    }},
    "content_pillar_analysis": {{
        "current_distribution": {{
            "educational": number,
            "inspirational": number,
            "entertaining": number,
            "promotional": number,
            "community": number
        }},
        "optimal_distribution": {{
            "educational": 45,
            "inspirational": 27,
            "entertaining": 18,
            "promotional": 5,
            "community": 10
        }},
        "balance_score": 0-100,
        "balance_assessment": "good_balance|needs_adjustment|poor_balance",
        "gaps": ["string"],
        "recommendations": ["string"]
    }},
    "trend_analysis": {{
        "current_trends_used": [
            {{
                "trend": "string",
                "lifecycle_stage": "emerging|growing|mature|declining",
                "execution_quality": "excellent|good|basic|poor",
                "niche_relevance": "high|medium|low"
            }}
        ],
        "missed_trends": [
            {{
                "trend": "string",
                "relevance_to_niche": "high|medium",
                "lifecycle_stage": "string",
                "opportunity_cost": "string"
            }}
        ],
        "emerging_opportunities": [
            {{
                "trend": "string",
                "timing": "early|growing",
                "potential_impact": "string",
                "difficulty": "easy|medium|hard"
            }}
        ],
        "seasonal_opportunities": ["string"],
        "trend_alignment_breakdown": {{
            "current_usage_score": number,
            "timing_score": number,
            "adaptation_score": number,
            "prediction_score": number
        }}
    }},
    "hashtag_analysis": {{
        "current_strategy": {{
            "avg_hashtags_per_post": number,
            "size_distribution": {{
                "mega": number,
                "large": number,
                "medium": number,
                "small": number,
                "micro": number
            }},
            "effectiveness_score": 0-100
        }},
        "distribution_assessment": {{
            "score": number,
            "assessment": "optimal_mix|slightly_off|unbalanced|all_same_size"
        }},
        "recommendations": {{
            "optimal_count": number,
            "suggested_distribution": {{
                "mega": number,
                "large": number,
                "medium": number,
                "small": number,
                "micro": number
            }},
            "rotation_strategy": "string"
        }},
        "top_performing_categories": ["string"],
        "underperforming_areas": ["string"]
    }},
    "edge_case_detection": {{
        "detected_case": "none|multi_niche|niche_pivot|emerging_niche|saturated_niche|local_regional|b2b_niche",
        "special_considerations": ["string"],
        "adjusted_approach": "string"
    }},
    "niche_specific_insights": {{
        "best_posting_times": ["string"],
        "top_content_formats": ["string"],
        "audience_pain_points": ["string"],
        "content_opportunities": ["string"],
        "weekly_content_calendar": {{
            "monday": "string tema",
            "tuesday": "string tema",
            "wednesday": "string tema",
            "thursday": "string tema",
            "friday": "string tema",
            "saturday": "string tema",
            "sunday": "string tema"
        }}
    }},
    "findings": [
        {{
            "type": "strength|weakness|opportunity|threat",
            "category": "niche|trends|content|hashtags|benchmark",
            "finding": "TÜRKÇE - örn: Niche'de yetersiz otorite konumlandırması var - hesap genel içerik üretiyor, uzmanlaşma eksik. Bu rakiplerden ayrışmayı zorlaştırıyor",
            "evidence": "TÜRKÇE - örn: Son 50 postun %70'i farklı alt konularda dağılmış, tutarlı bir uzmanlık alanı oluşturulamamış. Rakip X ise tek konuya odaklanarak 3x daha fazla takipçi kazanmış",
            "impact_score": 80
        }},
        {{
            "type": "opportunity",
            "category": "trends",
            "finding": "TÜRKÇE - örn: Niche'de yükselen 'AI araçları' trendi henüz doygunluğa ulaşmamış ve ilk hareket avantajı mevcut",
            "evidence": "TÜRKÇE - örn: 'AI productivity' hashtaginde son 30 günde %340 artış var ancak Türkiye'de bu konuda sadece 3 büyük hesap içerik üretiyor",
            "impact_score": 90
        }}
    ],
    "recommendations": [
        {{
            "priority": 1,
            "category": "niche|trends|content|hashtags|positioning",
            "action": "TÜRKÇE - örn: 3 ana içerik sütunu belirleyin ve tüm içeriklerin %80'ini bu sütunlarda üretin. Önerilen sütunlar: Temel bilgiler, İleri teknikler, Gerçek hayat uygulamaları",
            "expected_impact": "TÜRKÇE - örn: Niche otoritesi skorunda %50 artış, kaydetme oranında 2x iyileşme, marka işbirliği tekliflerinde artış",
            "implementation": "TÜRKÇE - örn: 1) Rakip analizi ile boşlukları tespit edin 2) Uzmanlık alanınızı seçin 3) 30 günlük içerik takvimi oluşturun 4) Her sütun için 10 post fikri hazırlayın",
            "difficulty": "easy|medium|hard",
            "timeline": "immediate|short_term|medium_term|long_term"
        }}
    ],
    "competitive_positioning": {{
        "unique_value_proposition": "string",
        "differentiation_strategy": "string",
        "authority_building_plan": ["string"],
        "content_pillars_to_own": ["string"],
        "blue_ocean_opportunities": ["string"]
    }},
    "nicheBenchmarks": {{
        "description": "Comprehensive niche-specific performance benchmarks",
        "niche": "{niche}",
        "formula_used": "Benchmark_Score = (Your_Metric / Industry_Benchmark) × 100",
        "engagementBenchmarks": {{
            "your_engagement_rate": 0.0,
            "niche_average": 0.0,
            "niche_top_10_percent": 0.0,
            "niche_top_25_percent": 0.0,
            "your_percentile": 0,
            "gap_to_top_25": 0.0,
            "gap_to_average": 0.0
        }},
        "growthBenchmarks": {{
            "your_monthly_growth": 0.0,
            "niche_average_growth": 0.0,
            "niche_top_performers_growth": 0.0,
            "your_percentile": 0
        }},
        "contentBenchmarks": {{
            "your_posting_frequency": 0,
            "niche_optimal_frequency": "X-Y posts/week",
            "your_reels_percentage": 0,
            "niche_optimal_reels": 0,
            "your_carousel_percentage": 0,
            "niche_optimal_carousel": 0,
            "format_alignment_score": 0
        }},
        "saveBenchmarks": {{
            "your_save_rate": 0.0,
            "niche_average_save_rate": 0.0,
            "your_percentile": 0,
            "indicates": "Content value assessment"
        }},
        "followerToEngagementRatio": {{
            "your_ratio": 0.0,
            "niche_healthy_ratio": 0.0,
            "assessment": "healthy|concerning|suspicious"
        }},
        "overallBenchmarkScore": {{
            "score": 0,
            "interpretation": "above_average|average|below_average|significantly_below"
        }}
    }},
    "sectorBestPractices": {{
        "description": "Industry-specific best practices for {niche}",
        "practices": [
            {{
                "practice": "string",
                "description": "string",
                "yourStatus": "implemented|partially|not_implemented",
                "impact": "high|medium|low",
                "implementationGuide": "string",
                "examples": ["@example_account_1", "@example_account_2"],
                "priority": 1
            }}
        ],
        "contentFormulas": [
            {{
                "name": "string",
                "description": "string",
                "applicability": "high|medium|low",
                "example": "string"
            }}
        ],
        "nicheSpecificTips": [
            "Tip specific to {niche}",
            "Another tip"
        ],
        "commonMistakesToAvoid": [
            {{
                "mistake": "string",
                "impact": "string",
                "yourRisk": "high|medium|low|none"
            }}
        ],
        "successPatterns": [
            {{
                "pattern": "string",
                "usedBy": "Top X% of {niche} accounts",
                "yourUsage": "string"
            }}
        ]
    }},
    "competitorAnalysis": {{
        "description": "Detailed analysis of 5+ competitors in your niche",
        "formula_used": "Competitive_Position = Σ(Your_Metric / Competitor_Avg × Weight)",
        "competitors": [
            {{
                "handle": "@competitor1",
                "type": "direct|aspirational|indirect",
                "followers": 0,
                "engagementRate": 0.0,
                "postingFrequency": 0,
                "primaryContent": "string",
                "strengths": ["string"],
                "weaknesses": ["string"],
                "contentStrategy": "string",
                "audienceOverlap": "high|medium|low|none",
                "threatLevel": "high|medium|low"
            }},
            {{
                "handle": "@competitor2",
                "type": "direct",
                "followers": 0,
                "engagementRate": 0.0,
                "postingFrequency": 0,
                "primaryContent": "string",
                "strengths": ["string"],
                "weaknesses": ["string"],
                "contentStrategy": "string",
                "audienceOverlap": "high|medium|low|none",
                "threatLevel": "high|medium|low"
            }},
            {{
                "handle": "@competitor3",
                "type": "aspirational",
                "followers": 0,
                "engagementRate": 0.0,
                "postingFrequency": 0,
                "primaryContent": "string",
                "strengths": ["string"],
                "weaknesses": ["string"],
                "contentStrategy": "string",
                "audienceOverlap": "high|medium|low|none",
                "threatLevel": "low"
            }},
            {{
                "handle": "@competitor4",
                "type": "direct",
                "followers": 0,
                "engagementRate": 0.0,
                "postingFrequency": 0,
                "primaryContent": "string",
                "strengths": ["string"],
                "weaknesses": ["string"],
                "contentStrategy": "string",
                "audienceOverlap": "high|medium|low|none",
                "threatLevel": "high|medium|low"
            }},
            {{
                "handle": "@competitor5",
                "type": "indirect",
                "followers": 0,
                "engagementRate": 0.0,
                "postingFrequency": 0,
                "primaryContent": "string",
                "strengths": ["string"],
                "weaknesses": ["string"],
                "contentStrategy": "string",
                "audienceOverlap": "high|medium|low|none",
                "threatLevel": "high|medium|low"
            }}
        ],
        "competitorAverages": {{
            "avgFollowers": 0,
            "avgEngagementRate": 0.0,
            "avgPostingFrequency": 0,
            "avgReelsPercentage": 0
        }},
        "yourPositionVsCompetitors": {{
            "followerRank": "X of Y",
            "engagementRank": "X of Y",
            "contentQualityRank": "X of Y (estimated)",
            "overallCompetitiveScore": 0
        }},
        "competitiveAdvantages": ["string"],
        "competitiveDisadvantages": ["string"],
        "opportunitiesFromGaps": [
            {{
                "gap": "string",
                "competitors_missing": ["@comp1", "@comp2"],
                "opportunity": "string",
                "difficulty": "easy|medium|hard"
            }}
        ],
        "threatsToMonitor": ["string"]
    }},
    "seasonalConsiderations": {{
        "description": "Seasonal patterns and opportunities for {niche}",
        "currentSeason": "Q1|Q2|Q3|Q4",
        "currentMonth": "string",
        "nicheSeasonality": {{
            "highSeasons": ["Month/Event 1", "Month/Event 2"],
            "lowSeasons": ["Month/Event 1"],
            "currentPhase": "peak|growing|declining|low"
        }},
        "upcomingOpportunities": [
            {{
                "event": "string",
                "date": "string",
                "relevance": "high|medium|low",
                "prepTime": "X days/weeks",
                "contentIdeas": ["string"],
                "hashtagsToUse": ["string"]
            }}
        ],
        "monthlyThemes": {{
            "january": {{
                "themes": ["New Year resolutions", "Fresh start"],
                "relevance": "high|medium|low"
            }},
            "february": {{
                "themes": ["Valentine's Day", "Self-love"],
                "relevance": "high|medium|low"
            }},
            "march": {{
                "themes": ["Spring", "International Women's Day"],
                "relevance": "high|medium|low"
            }},
            "april": {{
                "themes": ["Earth Day", "Spring cleaning"],
                "relevance": "high|medium|low"
            }},
            "may": {{
                "themes": ["Mother's Day", "Mental Health Awareness"],
                "relevance": "high|medium|low"
            }},
            "june": {{
                "themes": ["Summer start", "Pride Month"],
                "relevance": "high|medium|low"
            }},
            "july": {{
                "themes": ["Summer peak", "Vacation season"],
                "relevance": "high|medium|low"
            }},
            "august": {{
                "themes": ["Back to school prep", "Summer end"],
                "relevance": "high|medium|low"
            }},
            "september": {{
                "themes": ["Back to routine", "Fall start"],
                "relevance": "high|medium|low"
            }},
            "october": {{
                "themes": ["Halloween", "Breast Cancer Awareness"],
                "relevance": "high|medium|low"
            }},
            "november": {{
                "themes": ["Black Friday", "Thanksgiving", "Gratitude"],
                "relevance": "high|medium|low"
            }},
            "december": {{
                "themes": ["Holiday season", "Year in review", "Gift guides"],
                "relevance": "high|medium|low"
            }}
        }},
        "contentCalendarRecommendations": [
            {{
                "period": "string",
                "theme": "string",
                "contentType": "string",
                "timing": "string"
            }}
        ],
        "antiPatterns": ["Content to avoid during X period"]
    }},
    "score_breakdown": {{
        "overall_domain_score": 0,
        "formula_used": "Domain_Score = (Niche_Authority × 0.25 + Content_Relevance × 0.25 + Trend_Alignment × 0.20 + Hashtag_Effectiveness × 0.15 + Benchmark_Performance × 0.15)",
        "components": {{
            "niche_authority": {{"score": 0, "weight": 0.25, "weighted": 0}},
            "content_relevance": {{"score": 0, "weight": 0.25, "weighted": 0}},
            "trend_alignment": {{"score": 0, "weight": 0.20, "weighted": 0}},
            "hashtag_effectiveness": {{"score": 0, "weight": 0.15, "weighted": 0}},
            "benchmark_performance": {{"score": 0, "weight": 0.15, "weighted": 0}}
        }}
    }}
}}"""

    # analyze metodu BaseAgent'tan miras alınıyor - override edilmemeli
    # BaseAgent.analyze() metodu doğru şekilde:
    # 1. get_system_prompt() ve get_analysis_prompt() çağırır
    # 2. LLM'e istek gönderir
    # 3. Response'u parse eder ve validate eder
