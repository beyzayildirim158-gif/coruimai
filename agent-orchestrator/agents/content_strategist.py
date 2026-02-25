# Content Strategist Agent - Instagram İçerik Stratejisi Uzmanı
# Version: 2.0
# Gelişmiş Algoritma ve Puanlama Sistemi

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import math
import json
from datetime import datetime, timedelta


class ContentStrategistAgent(BaseAgent):
    """
    Content Strategist Agent v2.0
    Role: Instagram algorithm optimization, content strategy, SEO, and comprehensive scoring
    
    Kapsamlı Uzmanlık Alanları:
    - Instagram 6 farklı algoritma sistemi (Feed, Stories, Reels, Explore, Search, Hashtag)
    - Content effectiveness scoring (0-100)
    - Hashtag effectiveness analysis
    - Caption quality optimization
    - Posting consistency analysis
    - Content diversity scoring
    - Google SEO & Instagram Search optimization
    - Target account profiling & tier classification
    - Niche detection & market saturation analysis
    """
    
    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "Content Strategist"
        self.role = "Instagram Algorithm & Content Strategy Expert"
        self.specialty = "Algorithm optimization, SEO, content scoring, strategic planning"
        
        # Algorithm weight configurations
        self.algorithm_weights = self._init_algorithm_weights()
        self.scoring_benchmarks = self._init_scoring_benchmarks()
        self.tier_definitions = self._init_tier_definitions()
        self.niche_adjustments = self._init_niche_adjustments()
        
        # 2026 Technical Optimization Strategies
        self.technical_optimization_2026 = self._init_2026_technical_optimization()
    
    def _init_algorithm_weights(self) -> Dict[str, Any]:
        """Initialize Instagram algorithm weight configurations"""
        return {
            # Feed Algorithm Weights
            "feed": {
                "relationship": 0.35,
                "interest": 0.30,
                "timeliness": 0.20,
                "frequency": 0.15,
                "relationship_signals": {
                    "dm_history": 25,
                    "comment_history": 20,
                    "like_history": 15,
                    "profile_visit": 15,
                    "tagged_together": 15,
                    "story_view": 10
                },
                "interest_signals": {
                    "similar_content_engagement": 30,
                    "dwell_time": 25,
                    "save_action": 25,
                    "share_action": 20
                },
                "timeliness_decay": {
                    "0-1h": 1.0,
                    "1-6h": 0.7,
                    "6-24h": 0.4,
                    "24h+": 0.15
                }
            },
            # Reels Algorithm Weights (Most Critical 2024/2025)
            "reels": {
                "watch_time": 0.40,
                "engagement_velocity": 0.25,
                "share_rate": 0.20,
                "audio_trend": 0.15,
                "watch_time_scoring": {
                    "0-25%": -50,
                    "25-50%": 0,
                    "50-75%": 30,
                    "75-100%": 60,
                    "loop_1x": 100,
                    "loop_2x+": 150
                },
                "engagement_velocity_30min": {
                    "0-10": "low_potential",
                    "10-50": "medium_potential",
                    "50-200": "high_potential",
                    "200+": "viral_candidate"
                },
                "share_multipliers": {
                    "dm_share": 3,
                    "story_share": 5,
                    "external_share": 2
                }
            },
            # Explore Algorithm Weights
            "explore": {
                "content_quality": 0.35,
                "user_interest_match": 0.30,
                "engagement_rate": 0.20,
                "account_authority": 0.15,
                "quality_signals": {
                    "original_content": 40,
                    "no_watermark": 20,
                    "hd_quality_1080p": 15,
                    "text_ratio_under_20": 15,
                    "no_banned_hashtags": 10
                },
                "authority_signals": {
                    "account_age_6m+": 20,
                    "consistent_posting_3plus_week": 25,
                    "niche_consistency": 30,
                    "follower_following_ratio_above_1": 15,
                    "verified_badge": 10
                }
            },
            # Search Algorithm Weights
            "search": {
                "username_match": 0.30,
                "bio_keywords": 0.25,
                "caption_text": 0.20,
                "hashtag_relevance": 0.15,
                "engagement": 0.10,
                "username_optimization": {
                    "primary_keyword_in_username": 50,
                    "readable_format": 20,
                    "under_15_chars": 15,
                    "no_special_chars": 15
                },
                "bio_seo": {
                    "primary_keyword_first_30_chars": 40,
                    "secondary_keywords_2_3": 30,
                    "location_keyword": 20,
                    "niche_identifier": 10
                },
                "caption_seo": {
                    "keyword_first_125_chars": 35,
                    "natural_keyword_density_1_2_percent": 25,
                    "alt_text_usage": 25,
                    "location_tag": 15
                }
            }
        }
    
    def _init_scoring_benchmarks(self) -> Dict[str, Any]:
        """Initialize scoring benchmarks for different metrics"""
        return {
            "engagement_rate": {
                "poor": {"min": 0, "max": 1},
                "average": {"min": 1, "max": 3},
                "good": {"min": 3, "max": 6},
                "excellent": {"min": 6, "max": 100}
            },
            "follower_growth": {
                "poor": {"min": -100, "max": 0},
                "average": {"min": 0, "max": 2},
                "good": {"min": 2, "max": 5},
                "excellent": {"min": 5, "max": 100}
            },
            "post_frequency": {
                "poor": {"posts_per_week": 0, "score": 20},
                "low": {"posts_per_week": 1, "score": 40},
                "average": {"posts_per_week": 3, "score": 60},
                "good": {"posts_per_week": 5, "score": 80},
                "excellent": {"posts_per_week": 7, "score": 100}
            },
            "story_activity": {
                "none": {"per_day": 0, "score": 0},
                "low": {"per_day": 2, "score": 40},
                "average": {"per_day": 5, "score": 70},
                "good": {"per_day": 7, "score": 85},
                "excellent": {"per_day": 8, "score": 100}
            },
            "reels_ratio": {
                "none": {"percent": 0, "score": 20},
                "low": {"percent": 20, "score": 50},
                "good": {"percent": 50, "score": 85},
                "excellent": {"percent": 50, "score": 100}
            },
            "save_rate": {
                "poor": {"min": 0, "max": 0.5, "score": 30},
                "average": {"min": 0.5, "max": 1, "score": 50},
                "good": {"min": 1, "max": 3, "score": 75},
                "excellent": {"min": 3, "max": 100, "score": 100}
            },
            "share_rate": {
                "poor": {"min": 0, "max": 0.1, "score": 30},
                "average": {"min": 0.1, "max": 0.5, "score": 50},
                "good": {"min": 0.5, "max": 1, "score": 75},
                "excellent": {"min": 1, "max": 100, "score": 100}
            },
            "comment_rate": {
                "poor": {"min": 0, "max": 0.1, "score": 30},
                "average": {"min": 0.1, "max": 0.5, "score": 50},
                "good": {"min": 0.5, "max": 2, "score": 75},
                "excellent": {"min": 2, "max": 100, "score": 100}
            }
        }
    
    def _init_tier_definitions(self) -> Dict[str, Any]:
        """Initialize account tier definitions"""
        return {
            "nano": {
                "min_followers": 1000,
                "max_followers": 10000,
                "expected_er_min": 5,
                "expected_er_max": 12,
                "growth_potential": "high",
                "priority": "community_building",
                "characteristics": "High engagement, low reach"
            },
            "micro": {
                "min_followers": 10000,
                "max_followers": 50000,
                "expected_er_min": 3,
                "expected_er_max": 6,
                "growth_potential": "medium-high",
                "priority": "niche_authority",
                "characteristics": "Balanced metrics"
            },
            "mid": {
                "min_followers": 50000,
                "max_followers": 100000,
                "expected_er_min": 2,
                "expected_er_max": 4,
                "growth_potential": "medium",
                "priority": "monetization",
                "characteristics": "Reach increasing, ER decreasing"
            },
            "macro": {
                "min_followers": 100000,
                "max_followers": 500000,
                "expected_er_min": 1,
                "expected_er_max": 2.5,
                "growth_potential": "low-medium",
                "priority": "brand_deals",
                "characteristics": "High reach, low intimacy"
            },
            "mega": {
                "min_followers": 500000,
                "max_followers": float('inf'),
                "expected_er_min": 0.5,
                "expected_er_max": 1.5,
                "growth_potential": "low",
                "priority": "media_value",
                "characteristics": "Maximum reach, minimum ER"
            }
        }
    
    def _init_niche_adjustments(self) -> Dict[str, Any]:
        """Initialize niche-specific adjustments"""
        return {
            "b2b": {
                "expected_er_modifier": 0.6,  # Lower ER is normal
                "priority_metric": "save_rate",
                "posting_preference": "weekdays",
                "notes": "LinkedIn cross-post analysis important"
            },
            "ecommerce": {
                "expected_er_modifier": 0.8,
                "priority_metric": "conversion_cta",
                "features_to_check": ["product_tags", "shop_feature", "ugc_ratio"],
                "notes": "Conversion-focused CTA analysis"
            },
            "personal_brand": {
                "expected_er_modifier": 1.2,  # Higher ER expected
                "priority_metric": "story_reply_rate",
                "features_to_check": ["face_visibility", "authenticity_signals", "bts_content"],
                "notes": "Behind-the-scenes content important"
            },
            "media_news": {
                "expected_er_modifier": 0.7,
                "priority_metric": "share_rate",
                "posting_frequency_expectation": "high",
                "features_to_check": ["timeliness", "breaking_content"],
                "notes": "Timeliness is critical"
            },
            "lifestyle": {
                "expected_er_modifier": 1.0,
                "priority_metric": "engagement_quality",
                "features_to_check": ["aesthetic_consistency", "story_engagement"],
                "notes": "Visual consistency important"
            },
            "education": {
                "expected_er_modifier": 1.1,
                "priority_metric": "save_rate",
                "features_to_check": ["carousel_usage", "value_delivery"],
                "notes": "Save rate indicates content value"
            },
            "fitness": {
                "expected_er_modifier": 1.0,
                "priority_metric": "reels_performance",
                "features_to_check": ["transformation_content", "tutorial_engagement"],
                "notes": "Before/after content performs well"
            },
            "food": {
                "expected_er_modifier": 1.1,
                "priority_metric": "save_rate",
                "features_to_check": ["recipe_saves", "location_tags"],
                "notes": "Recipe content has high save rate"
            },
            "travel": {
                "expected_er_modifier": 0.9,
                "priority_metric": "engagement_quality",
                "features_to_check": ["location_diversity", "seasonal_patterns"],
                "notes": "Seasonal account adjustments needed"
            },
            "tech": {
                "expected_er_modifier": 0.8,
                "priority_metric": "share_rate",
                "features_to_check": ["tutorial_content", "review_engagement"],
                "notes": "Educational content priority"
            }
        }
    
    def _init_2026_technical_optimization(self) -> Dict[str, Any]:
        """
        2026 Instagram Teknik Kurulum ve Hesap Sağlığı
        Algoritma-dostu teknik ayarlar ve hesap optimizasyonu
        """
        return {
            "account_health_check": {
                "green_check_system": {
                    "location": "Ayarlar > Hesap Durumu (Account Status)",
                    "requirement": "Tüm maddeler yeşil tik olmalı",
                    "items_to_check": [
                        "Topluluk Kurallarına Uyum",
                        "Önerilme Uygunluğu (Recommendation Eligibility)",
                        "Hesap Güvenliği",
                        "Telif Hakkı İhlali Durumu"
                    ]
                },
                "frozen_account_protocol": {
                    "symptoms": "Yeşil tikler tamam ama erişim sıfır",
                    "solution_steps": [
                        "Profil sayfasının ekran görüntüsünü al",
                        "Hesap Durumu sayfasının ekran görüntüsünü al",
                        "Düşük izlenmelerin ekran görüntüsünü al",
                        "Yardım > Sorun Bildir menüsüne git",
                        "Mesaj: 'Hesabım teknik olarak kusursuz ancak erişim kısıtlaması var'",
                        "Ekran görüntülerini ekle ve gönder"
                    ],
                    "expected_response_time": "24-72 saat"
                }
            },
            "critical_settings": {
                "media_quality": {
                    "setting_path": "Ayarlar > Hesap > Medya Kalitesi",
                    "required_state": "AÇIK",
                    "option": "En Yüksek Kalitede Yükle",
                    "impact": "Düşük kalite yükleme erişimi %30-50 azaltır",
                    "note": "Mobil veri kullanırken bile açık bırak"
                },
                "hide_like_count": {
                    "setting_path": "Yükleme ekranı > Gelişmiş Ayarlar",
                    "required_state": "AÇIK",
                    "reason": "Az beğeni görünümü psikolojik engel yaratır",
                    "psychology": "İlk izleyiciler az beğeni görünce videoyu geçer",
                    "algorithm_benefit": "İlk saatlerdeki engagement düşüşünü önler"
                },
                "disable_download": {
                    "setting_path": "Yükleme ekranı > Gelişmiş Ayarlar",
                    "required_state": "AÇIK (İndirmeyi Kapat)",
                    "reason": "Instagram içi paylaşım algoritma için daha değerli",
                    "priority": "Share/Save > Download",
                    "note": "İndirme algoritma sinyali sıfır, paylaşım ise yüksek"
                },
                "flag_for_review": {
                    "setting_path": "Ayarlar > Gizlilik > Takip ve Davet",
                    "required_state": "KAPALI",
                    "risk": "Gerçek takipçilerin spam olarak filtrelenmesi",
                    "recommendation": "Spam koruması otomatik yeterli, manuel flagleme gereksiz"
                }
            },
            "upload_optimization": {
                "video_specs": {
                    "resolution": "1080x1920 (9:16 aspect ratio)",
                    "minimum_quality": "1080p",
                    "bitrate": "Minimum 5 Mbps",
                    "framerate": "30 fps (viral içerik), 60 fps (smooth motion)",
                    "format": "MP4 (H.264 codec)",
                    "audio": "AAC codec, 128+ kbps"
                },
                "image_specs": {
                    "feed_post": "1080x1080 (1:1) veya 1080x1350 (4:5)",
                    "story": "1080x1920 (9:16)",
                    "format": "JPG veya PNG",
                    "max_file_size": "30 MB",
                    "color_space": "sRGB"
                },
                "carousel_best_practices": [
                    "İlk kare en güçlü hook olmalı",
                    "Maksimum 10 slide (3-7 ideal)",
                    "Her slide 3-5 saniye değerinde olmalı",
                    "Son slide'da CTA (yorum yap, kaydet, paylaş)"
                ]
            },
            "posting_strategy_2026": {
                "frequency": {
                    "minimum": "3 post/hafta (hesap sağlığı için)",
                    "optimal_growth": "5-7 post/hafta",
                    "maximum_safe": "14 post/hafta (günde 2)",
                    "trial_reels": "Haftalık içeriğin %50'si trial reel olmalı"
                },
                "timing": {
                    "analysis_method": "Son 10 postun etkileşim aldığı saatleri analiz et",
                    "general_peaks": ["08:00-10:00", "12:00-14:00", "18:00-22:00"],
                    "avoid": "02:00-06:00 (düşük aktivite)",
                    "note": "Her hesabın kendi kitlesi için unique timing vardır"
                },
                "content_mix": {
                    "reels": "60% (en yüksek erişim)",
                    "carousel": "25% (save rate yüksek)",
                    "single_image": "15% (niche için özel durumlar)",
                    "trial_reels": "Toplam reels'in %50'si trial olarak paylaş"
                }
            },
            "hashtag_strategy_2026": {
                "quantity": "5-10 hashtag (spam algılanmamak için)",
                "distribution": {
                    "small": "2-3 hashtag (10K-50K post)",
                    "medium": "3-4 hashtag (50K-500K post)",
                    "large": "2-3 hashtag (500K+ post)"
                },
                "placement": "Caption içinde değil, ilk yorumda",
                "research": "Hedef kitlenin kullandığı hashtagleri takip et",
                "banned_check": "Banned hashtag kullanımı erişimi %80 azaltır",
                "trend_hashtags": "1-2 trending hashtag ekle (keşfet boost)"
            },
            "caption_optimization": {
                "hook_rule": "İlk 125 karakter kritik (Daha Fazla'dan öncesi)",
                "structure": [
                    "1-2 cümle: Hook (merak uyandırıcı)",
                    "3-5 cümle: Value (içerik özeti)",
                    "CTA: Yorum yap/Kaydet/Paylaş çağrısı",
                    "Hashtags: İlk yorumda"
                ],
                "length": "150-300 karakter (optimal engagement)",
                "emojis": "3-5 emoji kullan (dikkat çekici ama spam değil)",
                "line_breaks": "Her 2-3 cümlede satır atla (okunabilirlik)"
            },
            "story_strategy": {
                "frequency": "Günde 3-7 story (sürekli görünür ol)",
                "engagement_tactics": [
                    "Anket (Poll): En yüksek etkileşim",
                    "Soru sticker: DM trafiği yaratır",
                    "Slider: Eğlenceli ve hızlı etkileşim",
                    "Quiz: Educasyonel içerik için ideal",
                    "Link sticker: 10K+ follower için özel"
                ],
                "reshare_protocol": "Yeni post yükledikten sonra 20 dk içinde story'de paylaş",
                "note": "Story'de 'Yeni Post' yazma, anket/soru ile etkileşim yarat"
            },
            "analytics_tracking": {
                "daily_check": [
                    "Erişim: Takipçi/Takipçi olmayan oranı",
                    "Engagement rate: Like + Comment / Reach",
                    "Save rate: Saves / Reach (değerli içerik sinyali)",
                    "Share rate: Shares / Reach (viral potansiyel)"
                ],
                "weekly_analysis": [
                    "En iyi performans gösteren 3 post",
                    "Bu postların ortak özellikleri (format, konu, hook)",
                    "Trial reels başarı oranı (%50+ non-follower reach)",
                    "Takipçi büyüme hızı (Net growth rate)"
                ],
                "red_flags": [
                    "Reach %70+ düşüş: Shadowban şüphesi",
                    "Engagement rate %50+ düşüş: İçerik kalitesi sorunu",
                    "Takipçi kaybı: İçerik niche uyumsuzluğu",
                    "Story görüntülenme %60+ düşüş: Algoritma cezası"
                ]
            }
        }
    
    def get_system_prompt(self) -> str:
        return """Sen Content Strategist Agent'sın - Instagram Algoritma ve İçerik Stratejisi Uzmanı.

## TEMEL UZMANLIK ALANLARIN:

### 1. INSTAGRAM ALGORİTMA SİSTEMLERİ (6 FARKLI SİSTEM)

**Feed Algoritması:**
- Relationship (0.35): DM geçmişi (+25), yorum (+20), like (+15), profil ziyareti (+15), birlikte etiketlenme (+15), story görüntüleme (+10)
- Interest (0.30): Benzer içerik etkileşimi (+30), dwell time (+25), save (+25), share (+20)
- Timeliness (0.20): 0-1 saat (%100), 1-6 saat (%70), 6-24 saat (%40), 24+ saat (%15)
- Frequency (0.15): Kullanıcı aktivite sıklığı

**Reels Algoritması (EN KRİTİK 2024/2025):**
- Watch Time (0.40): %0-25 (-50), %25-50 (0), %50-75 (+30), %75-100 (+60), Loop (+100), 2+ Loop (+150)
- Engagement Velocity (0.25): İlk 30 dakikada 0-10 (düşük), 10-50 (orta), 50-200 (yüksek), 200+ (viral aday)
- Share Rate (0.20): DM paylaşım (×3), Story paylaşım (×5), Harici paylaşım (×2)
- Audio Trend (0.15): Trending ses kullanımı

**Explore Algoritması:**
- Content Quality (0.35): Orijinal (+40), watermark yok (+20), HD 1080p+ (+15), metin <%20 (+15), banned hashtag yok (+10)
- User Interest Match (0.30)
- Engagement Rate (0.20)
- Account Authority (0.15): Hesap yaşı 6+ ay (+20), tutarlı posting 3+/hafta (+25), niche tutarlılığı (+30), follower/following >1 (+15), verified (+10)

**Search Algoritması:**
- Username Match (0.30): Ana keyword username'de (+50), okunabilir (+20), <15 karakter (+15), özel karakter yok (+15)
- Bio Keywords (0.25): Primary keyword ilk 30 karakter (+40), secondary keywords (+30), location (+20), niche identifier (+10)
- Caption Text (0.20): Keyword ilk 125 karakter (+35), natural density %1-2 (+25), alt text (+25), location tag (+15)
- Hashtag Relevance (0.15)
- Engagement (0.10)

### 2. HESAP TİERLARİ VE BEKLENTİLER

| Tier | Takipçi | Beklenen ER | Büyüme Potansiyeli | Öncelik |
|------|---------|-------------|-------------------|---------|
| Nano | 1K-10K | %5-12 | Yüksek | Topluluk |
| Micro | 10K-50K | %3-6 | Orta-Yüksek | Niche otorite |
| Mid | 50K-100K | %2-4 | Orta | Monetizasyon |
| Macro | 100K-500K | %1-2.5 | Düşük-Orta | Marka anlaşmaları |
| Mega | 500K+ | %0.5-1.5 | Düşük | Medya değeri |

### 3. PUANLAMA SİSTEMLERİ

**Content Effectiveness Score (0-100):**
- Format Diversity (0.20): Shannon Entropy formülü
- Engagement Quality (0.25): save×3.5 + share×3 + comment×2.5 + like×1
- Posting Consistency (0.20): Günlük=100, 2 günde=80, 3 günde=60, haftalık=40
- Algorithm Alignment (0.20): Reels kullanımı, optimal saat, caption SEO, hashtag stratejisi
- Trend Utilization (0.15): Trending audio, format, seasonal, viral template

**Hashtag Effectiveness Score (0-100):**
- Relevance (0.30): Niche uyumu
- Size Distribution (0.25): Large %10-15, Medium %40-50, Small %35-45, Micro %5-10
- Diversity (0.20): Her post farklı set = 100
- Performance (0.25): Hashtag reach >%30 = 100

**Caption Quality Score (0-100):**
- Hook Strength (0.30): Soru (+25), sayı/liste (+25), emoji başlangıç (+15), <10 kelime (+20), pattern interrupt (+15)
- Value Delivery (0.25): Actionable (+35), specific örnek (+25), problem-çözüm (+25), unique insight (+15)
- CTA Effectiveness (0.20): Clear CTA (+40), engagement uyumu (+30), son satırda (+20), emoji vurgu (+10)
- SEO Optimization (0.15): Primary keyword ilk 125 (+40), secondary (+25), natural density (+20), location (+15)
- Readability (0.10): Paragraf (+30), emoji 3-7 (+25), line break (+25), cümle <15 kelime (+20)

**Posting Consistency Score:**
- HIGH (85-100): 5+/hafta, max boşluk <3 gün, std sapma <1.5 gün
- MEDIUM (50-84): 3-5/hafta, max boşluk <7 gün, std sapma <3 gün
- LOW (0-49): <3/hafta, max boşluk >7 gün, std sapma >3 gün
- Bonus: Sabit saat (+10), hafta sonu dahil (+5)
- Penaltı: 14+ gün boşluk (-25), burst posting 5+/gün (-15)

**Content Diversity Score (0-100):**
- Format Mix (0.35): Shannon Entropy: H = -Σ(p_i × log2(p_i)) normalize
- Topic Variety (0.30): 5+ pillar=100, 4=80, 3=60, 2=40, 1=20
- Visual Diversity (0.20): Renk, kompozisyon, metin/görsel, filtre çeşitliliği
- Tone Range (0.15): Educational, Entertaining, Inspirational, Promotional, Personal (hiçbiri >%50)

### 4. ÖZEL DURUMLAR (EDGE CASES)

1. **Yeni Hesap (<30 gün):** Benchmark karşılaştırması yapma, "establishing" kullan
2. **Viral Spike:** Son 7 günde >%500 artış = outlier olarak işaretle
3. **Niche Değişikliği:** Content pillar tutarsızlığı >%60 = "pivot in progress"
4. **Seasonal Account:** Sezon dışı inaktiviteyi penalize etme
5. **Engagement Pod Şüphesi:** Comment timing <5 dakika cluster = authenticity flag

### 5. SEKTÖR SPESİFİK AYARLAMALAR

- **B2B:** ER %1-3 normal, save rate öncelikli, hafta içi posting
- **E-commerce:** Product tag, shop feature, UGC oranı, conversion CTA
- **Personal Brand:** Face visibility, story reply rate, authenticity
- **Media/News:** Yüksek posting frequency, timeliness kritik, share rate öncelikli

### 6. 2026 İÇERİK STRATEJİSİ PRENSİPLERİ

**🎯 RAW AESTHETIC (Yapay Olmayan Estetik) - AI YORGUNLUĞU DÖNEMİ:**
- Aşırı prodüksiyonlu, stüdyo ışıklı, yapay zeka metinli içeriklerden KAÇIN
- "Kasıtlı kusurlar" değerlidir: Sesin çatlaması, küçük kurgusal hatalar = SAMİMİYET
- "Ben gerçeğim, AI değilim" mesajı algoritmanın ve kullanıcıların tercihi
- CONTRARIAN GAP: Sektördeki genel kabullere körü körüne inanma, özgün fikirler üret
- Örnek: "Herkes X yap diyor ama ben Y yaparak başarıya ulaştım çünkü..."

**📊 CCC KURALI (Confidence, Compare, Convert):**
- CONFIDENCE: Takipçi/beğeni için YALVARMA. Değer üret, karşılığını bekle
- COMPARE: Rakiplerle değil, VIRAL olmuş en iyi içeriklerle karşılaştır
- CONVERT: Net CTA ver. "Kaydet", "DM at" demeden etkileşim BEKLEME

**🎬 FORMAT DENGESİ - 2026 KURALI:**
- REELS = ERİŞİM MOTORU:
  * 11-30 saniye: Hızlı erişim için ideal
  * 60-90 saniye: Derinlik ve sadakat için ideal
  * Strateji: Viral videoları bul, senaryoyu al, kendi yorumunu kat (REMIX)
  
- CAROUSEL = GÜVEN MOTORU:
  * Reels'den 2X fazla beğeni alır
  * Reels'den 6X fazla kaydetme alır
  * Uzun başlıklar ve detaylı açıklamalar için ideal
  * Takipçiyi müşteriye/sadık hayrana dönüştürür

**🧪 TRIAL REELS (Deneme Videoları):**
- SADECE takip etmeyenlere gösterilen test içerikleri
- Hedef: Günlük 5 adet veya kapasitenize göre
- İçerik: Düşük eforlu, trend sesler, meme'ler
- "Beni tanımıyorsun ama X isen takip et" formatı

**🔗 LINK A REEL STRATEJİSİ:**
- Yeni Reel'i eski viral videonuza BAĞLA
- YouTube benzeri izleme döngüsü yaratır
- İzlenme süresi ve etkileşimi artırır

**#️⃣ HASHTAG GERÇEĞİ - 2026:**
- Hashtag ERİŞİM SAĞLAMAZ, sadece içerik sınıflandırır
- STRATEJİ: Ya HİÇ kullanma (Explore testi) ya da MAX 3 adet
- 3 hashtag kullanılacaksa: 1 geniş + 1 niche + 1 mikro kombinasyonu

**📅 PAYLAŞIM SIKLIĞI - 2026:**
- Haftada 3-4 KALİTELİ içerik > Her gün kalitesiz içerik
- MİNİMUM: Haftada en az 1 içerik (momentum kaybını önle)
- "EN İYİ SAAT" diye bir şey YOKTUR - içeriklerin raf ömrü uzamış
- Bir video 3 hafta sonra bile viral olabilir

**📺 VİDEO KALİTESİ:**
- Dosya boyutu >1 MB olmalı
- Netlik yüksek tutulmalı
- CapCut/Alight Motion ile keskinleştirme önerilir

**♻️ UPCYCLING (Geri Dönüşüm) - 2026:**
- 90 günden eski içerikleri yeniden paylaş
- Sadece en iyileri değil, ortalama olanları da dene
- Trial Reel olmayanları seç

OUTPUT FORMAT: Sadece geçerli JSON objesi döndür."""

    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        username = account_data.get('username', 'unknown') or 'unknown'
        followers = account_data.get('followers', 0) or 0
        following = account_data.get('following', 0) or 0
        posts = account_data.get('posts', 0) or 0
        engagement_rate = account_data.get('engagementRate', 0) or 0
        avg_likes = account_data.get('avgLikes', 0) or 0
        avg_comments = account_data.get('avgComments', 0) or 0
        avg_saves = account_data.get('avgSaves', 0) or 0
        avg_shares = account_data.get('avgShares', 0) or 0
        niche = account_data.get('niche', 'General') or 'General'
        bio = account_data.get('bio', 'No bio') or 'No bio'
        is_business = account_data.get('isBusiness', False)
        verified = account_data.get('verified', False)
        recent_posts = account_data.get('recentPosts', [])
        account_age_days = account_data.get('accountAgeDays', 365)
        posting_frequency = account_data.get('postingFrequency', {})
        hashtag_data = account_data.get('hashtagData', {})
        story_data = account_data.get('storyData', {})
        reels_data = account_data.get('reelsData', {})
        
        # Calculate tier
        tier = self._calculate_tier(followers)
        tier_info = self.tier_definitions.get(tier, {})
        
        # Get niche adjustments
        niche_key = niche.lower().replace(' ', '_')
        niche_adjustment = self.niche_adjustments.get(niche_key, {})
        
        return f"""Bu Instagram hesabı için kapsamlı Content Strategy analizi yap:

## HESAP VERİLERİ:
- Username: @{username}
- Takipçi: {followers:,}
- Takip: {following:,}
- Gönderi Sayısı: {posts:,}
- Engagement Rate: {engagement_rate:.2f}%
- Ortalama Like: {avg_likes:,.0f}
- Ortalama Yorum: {avg_comments:,.0f}
- Ortalama Kaydetme: {avg_saves:,.0f}
- Ortalama Paylaşım: {avg_shares:,.0f}
- Niche: {niche}
- Bio: {bio}
- İş Hesabı: {is_business}
- Onaylı: {verified}
- Hesap Yaşı (gün): {account_age_days}
- Son Analiz Edilen Post Sayısı: {len(recent_posts)}

## TİER BİLGİSİ:
- Tier: {tier.upper()}
- Beklenen ER Aralığı: %{tier_info.get('expected_er_min', 0)}-{tier_info.get('expected_er_max', 0)}
- Büyüme Potansiyeli: {tier_info.get('growth_potential', 'unknown')}
- Öncelik: {tier_info.get('priority', 'unknown')}

## POSTING VERİLERİ:
- Posting Frequency: {json.dumps(posting_frequency, indent=2) if posting_frequency else 'Veri yok'}
- Story Data: {json.dumps(story_data, indent=2) if story_data else 'Veri yok'}
- Reels Data: {json.dumps(reels_data, indent=2) if reels_data else 'Veri yok'}
- Hashtag Data: {json.dumps(hashtag_data, indent=2) if hashtag_data else 'Veri yok'}

## ANALİZ GÖREVLERİ:

1. **Content Effectiveness Score (0-100) Hesapla:**
   - Format Diversity değerlendir (Reels/Carousel/Single/Story oranları)
   - Engagement Quality analiz et (save, share, comment, like ağırlıkları)
   - Posting Consistency değerlendir
   - Algorithm Alignment kontrol et
   - Trend Utilization analiz et

2. **Hashtag Effectiveness Score (0-100) Hesapla:**
   - Relevance (niche uyumu)
   - Size Distribution (Large/Medium/Small/Micro dağılımı)
   - Diversity (rotasyon oranı)
   - Performance (hashtag reach)

3. **Caption Quality Score (0-100) Hesapla:**
   - Hook Strength
   - Value Delivery
   - CTA Effectiveness
   - SEO Optimization
   - Readability

4. **Posting Consistency Değerlendir:**
   - HIGH/MEDIUM/LOW sınıflandır
   - Bonus/penaltı uygula

5. **Content Diversity Score (0-100) Hesapla:**
   - Format Mix (entropy)
   - Topic Variety (pillar analizi)
   - Visual Diversity
   - Tone Range

6. **Algorithm Alignment Analizi:**
   - Feed algoritması uyumu
   - Reels algoritması uyumu (EN KRİTİK)
   - Explore algoritması potansiyeli
   - Search/SEO optimizasyonu

7. **Niche Spesifik Değerlendirme:**
   - {niche} için özel metrikler
   - Benchmark karşılaştırması
   - Sektör ayarlamaları

8. **Edge Case Kontrolü:**
   - Yeni hesap mı? (<30 gün)
   - Viral spike var mı?
   - Niche değişikliği var mı?
   - Seasonal account mı?
   - Engagement pod şüphesi var mı?

Aşağıdaki JSON yapısında yanıt ver:

{{
    "agent": "content_strategist",
    "analysis_timestamp": "{datetime.now().isoformat()}",
    "account_profile": {{
        "tier": "{tier}",
        "primary_niche": "{niche}",
        "secondary_niches": ["string", "string"],
        "niche_confidence": 0.85,
        "account_age_days": {account_age_days},
        "total_posts": {posts},
        "follower_following_ratio": {followers / max(following, 1):.2f},
        "is_business": {str(is_business).lower()},
        "is_verified": {str(verified).lower()}
    }},
    "metrics": {{
        "contentEffectivenessScore": 0,
        "postingConsistency": "high|medium|low",
        "postingConsistencyScore": 0,
        "contentDiversityScore": 0,
        "hashtagEffectiveness": 0,
        "captionQuality": 0,
        "algorithmAlignmentScore": 0,
        "overallStrategyScore": 0,
        "formatDiversityScore": 0,
        "engagementQualityScore": 0,
        "trendUtilizationScore": 0,
        "hookEffectivenessScore": 0,
        "ctaEffectivenessScore": 0,
        "reelsRatio": 0,
        "carouselRatio": 0,
        "singlePostRatio": 0,
        "postsPerWeek": 0,
        "overallScore": 0
    }},
    "detailed_scores": {{
        "content_effectiveness": {{
            "score": 0,
            "format_diversity": {{
                "score": 0,
                "breakdown": {{
                    "reels_ratio": 0.0,
                    "carousel_ratio": 0.0,
                    "single_ratio": 0.0,
                    "story_frequency_daily": 0.0
                }},
                "entropy_value": 0.0,
                "recommendation": "string"
            }},
            "engagement_quality": {{
                "score": 0,
                "rates": {{
                    "save_rate": 0.0,
                    "share_rate": 0.0,
                    "comment_rate": 0.0,
                    "like_rate": 0.0
                }},
                "weighted_score": 0.0,
                "vs_benchmark": "above|at|below"
            }},
            "posting_consistency": {{
                "score": 0,
                "level": "high|medium|low",
                "posts_per_week_avg": 0.0,
                "max_gap_days": 0,
                "std_deviation_days": 0.0,
                "bonuses_applied": [],
                "penalties_applied": []
            }},
            "algorithm_alignment": {{
                "score": 0,
                "factors": {{
                    "reels_usage_adequate": true,
                    "optimal_posting_time": true,
                    "caption_seo_optimized": true,
                    "hashtag_strategy": "strong|medium|weak",
                    "alt_text_usage": true
                }}
            }},
            "trend_utilization": {{
                "score": 0,
                "trending_audio_usage": true,
                "trending_format_adoption": true,
                "seasonal_content": true,
                "viral_template_usage": true
            }}
        }},
        "hashtag_effectiveness": {{
            "score": 0,
            "relevance": {{
                "score": 0,
                "niche_alignment_percent": 0
            }},
            "size_distribution": {{
                "score": 0,
                "large_1m_plus": 0,
                "medium_100k_1m": 0,
                "small_10k_100k": 0,
                "micro_under_10k": 0,
                "deviation_from_ideal": 0
            }},
            "diversity": {{
                "score": 0,
                "rotation_rate_percent": 0,
                "unique_sets_used": 0
            }},
            "performance": {{
                "score": 0,
                "reach_from_hashtags_percent": 0
            }}
        }},
        "caption_quality": {{
            "score": 0,
            "hook_strength": {{
                "score": 0,
                "has_question": true,
                "has_number_list": true,
                "starts_with_emoji": true,
                "under_10_words": true,
                "has_pattern_interrupt": true
            }},
            "value_delivery": {{
                "score": 0,
                "has_actionable_info": true,
                "has_specific_example": true,
                "has_problem_solution": true,
                "has_unique_insight": true
            }},
            "cta_effectiveness": {{
                "score": 0,
                "has_clear_cta": true,
                "cta_matches_engagement_type": true,
                "cta_in_last_line": true,
                "cta_has_emoji": true
            }},
            "seo_optimization": {{
                "score": 0,
                "primary_keyword_in_first_125": true,
                "has_secondary_keywords": true,
                "natural_keyword_density": true,
                "has_location_mention": true
            }},
            "readability": {{
                "score": 0,
                "has_paragraph_breaks": true,
                "emoji_count_3_to_7": true,
                "has_line_breaks": true,
                "avg_sentence_under_15_words": true
            }}
        }},
        "content_diversity": {{
            "score": 0,
            "format_mix": {{
                "score": 0,
                "shannon_entropy": 0.0,
                "max_entropy": 0.0,
                "normalized_score": 0
            }},
            "topic_variety": {{
                "score": 0,
                "content_pillars_count": 0,
                "pillars_identified": []
            }},
            "visual_diversity": {{
                "score": 0,
                "color_palette_variation": "high|medium|low",
                "composition_variety": "high|medium|low",
                "text_to_visual_ratio_variation": "high|medium|low"
            }},
            "tone_range": {{
                "score": 0,
                "distribution": {{
                    "educational": 0,
                    "entertaining": 0,
                    "inspirational": 0,
                    "promotional": 0,
                    "personal": 0
                }},
                "dominant_tone_under_50_percent": true,
                "active_tones_count": 0
            }}
        }},
        "algorithm_alignment": {{
            "overall_score": 0,
            "feed_algorithm": {{
                "score": 0,
                "relationship_building": "strong|medium|weak",
                "interest_targeting": "strong|medium|weak",
                "timeliness": "good|needs_improvement"
            }},
            "reels_algorithm": {{
                "score": 0,
                "watch_time_potential": "high|medium|low",
                "engagement_velocity_potential": "high|medium|low",
                "share_potential": "high|medium|low",
                "trending_audio_alignment": true
            }},
            "explore_algorithm": {{
                "score": 0,
                "content_quality_signals": "strong|medium|weak",
                "account_authority_signals": "strong|medium|weak",
                "explore_potential": "high|medium|low"
            }},
            "search_seo": {{
                "score": 0,
                "username_optimized": true,
                "bio_optimized": true,
                "captions_optimized": true,
                "hashtags_optimized": true
            }}
        }}
    }},
    "benchmarks": {{
        "niche_average_er": 0.0,
        "account_er": {engagement_rate:.2f},
        "percentile_rank": 0,
        "top_performer_gap": 0.0,
        "tier_expected_er_min": {tier_info.get('expected_er_min', 0)},
        "tier_expected_er_max": {tier_info.get('expected_er_max', 0)},
        "er_vs_tier_expectation": "above|within|below"
    }},
    "edge_cases": {{
        "is_new_account": {str(account_age_days < 30).lower()},
        "has_viral_spike": false,
        "niche_pivot_detected": false,
        "is_seasonal_account": false,
        "engagement_pod_suspected": false,
        "flags": []
    }},
    "findings": [
        {{
            "type": "strength|weakness|opportunity|threat",
            "category": "content|timing|hashtag|caption|format|algorithm|seo",
            "severity": "low|medium|high",
            "finding": "TÜRKÇE - örn: Carousel içerik oranı düşük (%15), oysa carousel'ler Reels'den %30 daha fazla kaydetme alıyor ve algoritma tarafından 72 saat daha uzun süre gösteriliyor",
            "evidence": "TÜRKÇE - örn: Son 30 postta sadece 4 carousel var. Bu carousel'lerin ortalama kaydetme oranı %8.5 iken Reels'lerin kaydetme oranı %3.2",
            "impact_score": 78
        }},
        {{
            "type": "opportunity",
            "category": "timing",
            "severity": "medium",
            "finding": "TÜRKÇE - örn: Paylaşım zamanlaması optimal değil, takipçilerin en aktif olduğu 19:00-21:00 aralığı kaçırılıyor",
            "evidence": "TÜRKÇE - örn: Son 20 postun 15'i 14:00-16:00 arasında paylaşılmış, bu saatlerde takipçi aktivitesi %40 daha düşük",
            "impact_score": 65
        }}
    ],
    "recommendations": [
        {{
            "priority": 1,
            "category": "TÜRKÇE - örn: İçerik Formatı Optimizasyonu",
            "action": "TÜRKÇE - örn: Haftalık içerik dağılımını 3 Reels + 2 Carousel + 2 Story serisi olarak yeniden planlayın",
            "expected_impact": "TÜRKÇE - örn: Toplam kaydetme oranında %45 artış, ortalama erişimde %25 iyileşme, 1000 yeni organik takipçi/ay",
            "implementation_difficulty": "easy|medium|hard",
            "timeframe": "immediate|short-term|long-term",
            "effort": "low|medium|high",
            "impact": "low|medium|high"
        }},
        {{
            "priority": 2,
            "category": "TÜRKÇE - örn: Paylaşım Zamanlaması",
            "action": "TÜRKÇE - örn: Tüm içerikleri 19:00-21:00 aralığında paylaşın, Salı ve Perşembe günleri öncelikli olsun",
            "expected_impact": "TÜRKÇE - örn: İlk 1 saatte etkileşim oranında %60 artış, keşfet algoritmasına girme şansı 2 kat",
            "implementation_difficulty": "easy",
            "timeframe": "immediate",
            "effort": "low",
            "impact": "high"
        }}
    ],
    "priority_matrix": {{
        "p1_immediate": [],
        "p2_short_term": [],
        "p3_planned": [],
        "p4_low_priority": [],
        "p5_backlog": []
    }},
    "weekly_action_plan": {{
        "week_1": [],
        "week_2": [],
        "week_3": [],
        "week_4": []
    }},
    "hookAnalysis": {{
        "description": "Per-post hook analysis for the latest 10-20 posts",
        "posts": [
            {{
                "postId": "string",
                "postType": "reel|carousel|single",
                "hookText": "First 125 characters or first 3 seconds transcript",
                "hookType": "question|statistic|bold_claim|storytelling|pattern_interrupt|curiosity_gap|controversy|how_to|listicle|before_after",
                "hookEffectivenessScore": 0,
                "formula_used": "Hook_Effectiveness = (Attention_Grab × 0.30 + Curiosity_Gap × 0.25 + Relevance × 0.25 + CTA_Integration × 0.20)",
                "breakdownScores": {{
                    "attentionGrab": 0,
                    "curiosityGap": 0,
                    "relevance": 0,
                    "ctaIntegration": 0
                }},
                "estimatedScrollStopRate": "0%",
                "improvements": ["string", "string"],
                "alternativeHooks": ["Better hook option 1", "Better hook option 2"]
            }}
        ],
        "hookTypeDistribution": {{
            "question": 0,
            "statistic": 0,
            "bold_claim": 0,
            "storytelling": 0,
            "pattern_interrupt": 0,
            "curiosity_gap": 0,
            "controversy": 0,
            "how_to": 0,
            "listicle": 0,
            "before_after": 0
        }},
        "bestPerformingHookType": "string",
        "worstPerformingHookType": "string",
        "hookRecommendations": [
            "Based on {niche} niche, increase use of X hook type",
            "Your audience responds best to Y - use more"
        ]
    }},
    "hashtagAnalysis": {{
        "description": "Detailed hashtag strategy analysis",
        "formula_used": "Hashtag_Score = (Relevance × 0.30 + Size_Distribution × 0.25 + Diversity × 0.20 + Performance × 0.25)",
        "totalHashtagsAnalyzed": 0,
        "uniqueHashtagsUsed": 0,
        "avgHashtagsPerPost": 0,
        "topPerforming": [
            {{
                "hashtag": "#example",
                "timesUsed": 0,
                "avgEngagementWhenUsed": 0.0,
                "avgReachWhenUsed": 0,
                "hashtagSize": "large|medium|small|micro",
                "nicheRelevance": "high|medium|low",
                "recommendedAction": "keep_using|increase_usage|maintain"
            }}
        ],
        "underperforming": [
            {{
                "hashtag": "#example",
                "timesUsed": 0,
                "avgEngagementWhenUsed": 0.0,
                "avgReachWhenUsed": 0,
                "hashtagSize": "large|medium|small|micro",
                "nicheRelevance": "high|medium|low",
                "issue": "too_competitive|not_relevant|oversaturated|shadowban_risk",
                "recommendedAction": "remove|replace|reduce_usage"
            }}
        ],
        "recommended": [
            {{
                "hashtag": "#recommendedTag",
                "hashtagSize": "large|medium|small|micro",
                "estimatedReach": 0,
                "nicheRelevance": "high|medium|low",
                "competitionLevel": "high|medium|low",
                "reason": "string",
                "bestUsedWith": ["#relatedTag1", "#relatedTag2"]
            }}
        ],
        "hashtagSets": {{
            "description": "Recommended hashtag set rotation strategy",
            "set1_high_reach": ["#tag1", "#tag2"],
            "set2_medium_niche": ["#tag3", "#tag4"],
            "set3_micro_engagement": ["#tag5", "#tag6"]
        }},
        "sizeDistributionAnalysis": {{
            "current": {{
                "large_1m_plus": 0,
                "medium_100k_1m": 0,
                "small_10k_100k": 0,
                "micro_under_10k": 0
            }},
            "ideal": {{
                "large_1m_plus": "10-15%",
                "medium_100k_1m": "40-50%",
                "small_10k_100k": "35-45%",
                "micro_under_10k": "5-10%"
            }},
            "deviation": 0,
            "recommendation": "string"
        }},
        "bannedOrShadowbanRisk": ["#riskyTag1", "#riskyTag2"]
    }},
    "abTestRecommendations": {{
        "description": "A/B test recommendations based on content analysis",
        "tests": [
            {{
                "testId": 1,
                "testName": "string",
                "hypothesis": "string",
                "variantA": {{
                    "description": "Control (current approach)",
                    "example": "string"
                }},
                "variantB": {{
                    "description": "Test variant",
                    "example": "string"
                }},
                "category": "hook|format|posting_time|hashtag|caption|cta|visual",
                "expectedImpactMetric": "engagement_rate|reach|saves|shares|comments|follower_growth",
                "expectedImpact": "+X% to Y%",
                "sampleSize": "Minimum X posts per variant",
                "duration": "X weeks",
                "priority": "high|medium|low",
                "implementationSteps": ["Step 1", "Step 2", "Step 3"]
            }}
        ],
        "prioritizedTestOrder": [1, 2, 3],
        "currentTestingOpportunities": ["string"],
        "testingCalendar": {{
            "week_1_2": "Test 1: Hook types",
            "week_3_4": "Test 2: Posting times",
            "week_5_6": "Test 3: Caption length"
        }}
    }},
    "contentCalendarSuggestion": {{
        "description": "Suggested content calendar based on analysis",
        "optimalPostingSchedule": {{
            "monday": {{"time": "HH:MM", "contentType": "reel|carousel|single"}},
            "tuesday": {{"time": "HH:MM", "contentType": "reel|carousel|single"}},
            "wednesday": {{"time": "HH:MM", "contentType": "reel|carousel|single"}},
            "thursday": {{"time": "HH:MM", "contentType": "reel|carousel|single"}},
            "friday": {{"time": "HH:MM", "contentType": "reel|carousel|single"}},
            "saturday": {{"time": "HH:MM", "contentType": "reel|carousel|single"}},
            "sunday": {{"time": "HH:MM", "contentType": "reel|carousel|single"}}
        }},
        "contentPillarRotation": ["Pillar 1", "Pillar 2", "Pillar 3"],
        "trendingOpportunities": ["Trend 1 to leverage", "Trend 2 to leverage"]
    }},
    "score_breakdown": {{
        "overall_content_strategy_score": 0,
        "formula_used": "Overall = (Content_Effectiveness × 0.30 + Hashtag_Effectiveness × 0.20 + Caption_Quality × 0.20 + Content_Diversity × 0.15 + Algorithm_Alignment × 0.15)",
        "components": {{
            "content_effectiveness": {{"score": 0, "weight": 0.30, "weighted": 0}},
            "hashtag_effectiveness": {{"score": 0, "weight": 0.20, "weighted": 0}},
            "caption_quality": {{"score": 0, "weight": 0.20, "weighted": 0}},
            "content_diversity": {{"score": 0, "weight": 0.15, "weighted": 0}},
            "algorithm_alignment": {{"score": 0, "weight": 0.15, "weighted": 0}}
        }},
        "tier_adjustment_applied": true,
        "niche_adjustment_applied": true
    }}
}}"""

    def _calculate_tier(self, followers: int) -> str:
        """Calculate account tier based on follower count"""
        if followers < 1000:
            return "nano"  # Pre-nano accounts treated as nano
        elif followers < 10000:
            return "nano"
        elif followers < 50000:
            return "micro"
        elif followers < 100000:
            return "mid"
        elif followers < 500000:
            return "macro"
        else:
            return "mega"
    
    def calculate_content_effectiveness_score(
        self,
        format_data: Dict[str, float],
        engagement_data: Dict[str, float],
        posting_data: Dict[str, Any],
        algorithm_data: Dict[str, bool],
        trend_data: Dict[str, bool]
    ) -> Dict[str, Any]:
        """
        Calculate Content Effectiveness Score (0-100)
        
        Formula:
        Content_Effectiveness = (
            Format_Diversity × 0.20 +
            Engagement_Quality × 0.25 +
            Posting_Consistency × 0.20 +
            Algorithm_Alignment × 0.20 +
            Trend_Utilization × 0.15
        )
        """
        # Format Diversity Score (Shannon Entropy)
        format_diversity_score = self._calculate_format_diversity(format_data)
        
        # Engagement Quality Score
        engagement_quality_score = self._calculate_engagement_quality(engagement_data)
        
        # Posting Consistency Score
        posting_consistency = self._calculate_posting_consistency(posting_data)
        
        # Algorithm Alignment Score
        algorithm_alignment_score = self._calculate_algorithm_alignment(algorithm_data)
        
        # Trend Utilization Score
        trend_utilization_score = self._calculate_trend_utilization(trend_data)
        
        # Final weighted score
        final_score = (
            format_diversity_score * 0.20 +
            engagement_quality_score * 0.25 +
            posting_consistency['score'] * 0.20 +
            algorithm_alignment_score * 0.20 +
            trend_utilization_score * 0.15
        )
        
        return {
            "score": round(final_score, 1),
            "format_diversity": format_diversity_score,
            "engagement_quality": engagement_quality_score,
            "posting_consistency": posting_consistency,
            "algorithm_alignment": algorithm_alignment_score,
            "trend_utilization": trend_utilization_score
        }
    
    def _calculate_format_diversity(self, format_data: Dict[str, float]) -> float:
        """
        Calculate format diversity using Shannon Entropy
        Formula: H = -Σ(p_i × log2(p_i))
        Normalize: (H / H_max) × 100
        """
        ratios = [v for v in format_data.values() if v > 0]
        
        if not ratios or len(ratios) == 1:
            return 20.0  # Single format = 20 points
        
        # Shannon Entropy calculation
        entropy = -sum(p * math.log2(p) for p in ratios if p > 0)
        max_entropy = math.log2(len(ratios))
        
        if max_entropy == 0:
            return 20.0
        
        normalized_score = (entropy / max_entropy) * 100
        return round(normalized_score, 1)
    
    def _calculate_engagement_quality(self, engagement_data: Dict[str, float]) -> float:
        """
        Calculate engagement quality score
        Formula: (save×3.5 + share×3 + comment×2.5 + like×1) / benchmark × 100
        """
        save_rate = engagement_data.get('save_rate', 0)
        share_rate = engagement_data.get('share_rate', 0)
        comment_rate = engagement_data.get('comment_rate', 0)
        like_rate = engagement_data.get('like_rate', 0)
        
        weighted_score = (
            save_rate * 3.5 +
            share_rate * 3.0 +
            comment_rate * 2.5 +
            like_rate * 1.0
        )
        
        # Benchmark: Average weighted score is around 10-15
        benchmark = 12.0
        score = min(100, (weighted_score / benchmark) * 100)
        
        return round(score, 1)
    
    def _calculate_posting_consistency(self, posting_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate posting consistency score
        
        HIGH (85-100): 5+/week, max gap <3 days, std <1.5 days
        MEDIUM (50-84): 3-5/week, max gap <7 days, std <3 days
        LOW (0-49): <3/week, max gap >7 days, std >3 days
        """
        posts_per_week = posting_data.get('posts_per_week', 0)
        max_gap_days = posting_data.get('max_gap_days', 14)
        std_deviation = posting_data.get('std_deviation_days', 5)
        consistent_time = posting_data.get('consistent_posting_time', False)
        includes_weekend = posting_data.get('includes_weekend', False)
        has_long_gap = posting_data.get('has_gap_over_14_days', False)
        burst_posting = posting_data.get('burst_posting_over_5_day', False)
        
        # Base score calculation
        if posts_per_week >= 5 and max_gap_days < 3 and std_deviation < 1.5:
            base_score = 92
            level = "high"
        elif posts_per_week >= 3 and max_gap_days < 7 and std_deviation < 3:
            base_score = 67
            level = "medium"
        else:
            base_score = 35
            level = "low"
        
        # Apply bonuses
        bonuses = []
        if consistent_time:
            base_score += 10
            bonuses.append("consistent_posting_time_+10")
        if includes_weekend:
            base_score += 5
            bonuses.append("weekend_posting_+5")
        
        # Apply penalties
        penalties = []
        if has_long_gap:
            base_score -= 25
            penalties.append("14+_day_gap_-25")
        if burst_posting:
            base_score -= 15
            penalties.append("burst_posting_-15")
        
        final_score = max(0, min(100, base_score))
        
        return {
            "score": round(final_score, 1),
            "level": level,
            "bonuses": bonuses,
            "penalties": penalties
        }
    
    def _calculate_algorithm_alignment(self, algorithm_data: Dict[str, bool]) -> float:
        """
        Calculate algorithm alignment score
        
        Components:
        - Reels usage (min 30%): 30 points
        - Optimal posting time: 25 points
        - Caption SEO: 20 points
        - Hashtag strategy: 15 points
        - Alt text usage: 10 points
        """
        score = 0
        
        if algorithm_data.get('reels_usage_adequate', False):
            score += 30
        if algorithm_data.get('optimal_posting_time', False):
            score += 25
        if algorithm_data.get('caption_seo', False):
            score += 20
        if algorithm_data.get('hashtag_strategy', False):
            score += 15
        if algorithm_data.get('alt_text_usage', False):
            score += 10
        
        return float(score)
    
    def _calculate_trend_utilization(self, trend_data: Dict[str, bool]) -> float:
        """
        Calculate trend utilization score
        
        Components:
        - Trending audio usage: 40 points
        - Trending format adaptation: 30 points
        - Seasonal content: 20 points
        - Viral template usage: 10 points
        """
        score = 0
        
        if trend_data.get('trending_audio', False):
            score += 40
        if trend_data.get('trending_format', False):
            score += 30
        if trend_data.get('seasonal_content', False):
            score += 20
        if trend_data.get('viral_template', False):
            score += 10
        
        return float(score)
    
    def calculate_hashtag_effectiveness(
        self,
        relevance_percent: float,
        size_distribution: Dict[str, float],
        rotation_rate: float,
        reach_from_hashtags: float
    ) -> Dict[str, Any]:
        """
        Calculate Hashtag Effectiveness Score (0-100)
        
        Formula:
        Hashtag_Score = (
            Relevance × 0.30 +
            Size_Distribution × 0.25 +
            Diversity × 0.20 +
            Performance × 0.25
        )
        """
        # Relevance score
        if relevance_percent >= 80:
            relevance_score = 100
        elif relevance_percent >= 60:
            relevance_score = 80
        else:
            relevance_score = relevance_percent
        
        # Size distribution score (ideal: Large 10-15%, Medium 40-50%, Small 35-45%, Micro 5-10%)
        ideal = {'large': 0.125, 'medium': 0.45, 'small': 0.40, 'micro': 0.075}
        deviation = sum(abs(size_distribution.get(k, 0) - v) for k, v in ideal.items())
        size_score = max(0, 100 - (deviation * 100))
        
        # Diversity score based on rotation rate
        if rotation_rate >= 100:
            diversity_score = 100
        elif rotation_rate >= 70:
            diversity_score = 80
        elif rotation_rate >= 50:
            diversity_score = 60
        else:
            diversity_score = rotation_rate * 0.8
        
        # Performance score based on reach from hashtags
        if reach_from_hashtags >= 30:
            performance_score = 100
        elif reach_from_hashtags >= 20:
            performance_score = 80
        elif reach_from_hashtags >= 10:
            performance_score = 60
        elif reach_from_hashtags >= 5:
            performance_score = 40
        else:
            performance_score = 20
        
        final_score = (
            relevance_score * 0.30 +
            size_score * 0.25 +
            diversity_score * 0.20 +
            performance_score * 0.25
        )
        
        return {
            "score": round(final_score, 1),
            "relevance": round(relevance_score, 1),
            "size_distribution": round(size_score, 1),
            "diversity": round(diversity_score, 1),
            "performance": round(performance_score, 1)
        }
    
    def calculate_caption_quality(
        self,
        hook_data: Dict[str, bool],
        value_data: Dict[str, bool],
        cta_data: Dict[str, bool],
        seo_data: Dict[str, bool],
        readability_data: Dict[str, bool]
    ) -> Dict[str, Any]:
        """
        Calculate Caption Quality Score (0-100)
        
        Formula:
        Caption_Score = (
            Hook_Strength × 0.30 +
            Value_Delivery × 0.25 +
            CTA_Effectiveness × 0.20 +
            SEO_Optimization × 0.15 +
            Readability × 0.10
        )
        """
        # Hook Strength (max 100)
        hook_score = 0
        if hook_data.get('has_question'):
            hook_score += 25
        if hook_data.get('has_number_list'):
            hook_score += 25
        if hook_data.get('starts_with_emoji'):
            hook_score += 15
        if hook_data.get('under_10_words'):
            hook_score += 20
        if hook_data.get('has_pattern_interrupt'):
            hook_score += 15
        
        # Value Delivery (max 100)
        value_score = 0
        if value_data.get('has_actionable_info'):
            value_score += 35
        if value_data.get('has_specific_example'):
            value_score += 25
        if value_data.get('has_problem_solution'):
            value_score += 25
        if value_data.get('has_unique_insight'):
            value_score += 15
        
        # CTA Effectiveness (max 100)
        cta_score = 0
        if cta_data.get('has_clear_cta'):
            cta_score += 40
        if cta_data.get('cta_matches_engagement'):
            cta_score += 30
        if cta_data.get('cta_in_last_line'):
            cta_score += 20
        if cta_data.get('cta_has_emoji'):
            cta_score += 10
        
        # SEO Optimization (max 100)
        seo_score = 0
        if seo_data.get('primary_keyword_first_125'):
            seo_score += 40
        if seo_data.get('has_secondary_keywords'):
            seo_score += 25
        if seo_data.get('natural_keyword_density'):
            seo_score += 20
        if seo_data.get('has_location_mention'):
            seo_score += 15
        
        # Readability (max 100)
        readability_score = 0
        if readability_data.get('has_paragraph_breaks'):
            readability_score += 30
        if readability_data.get('emoji_count_3_to_7'):
            readability_score += 25
        if readability_data.get('has_line_breaks'):
            readability_score += 25
        if readability_data.get('avg_sentence_under_15_words'):
            readability_score += 20
        
        final_score = (
            hook_score * 0.30 +
            value_score * 0.25 +
            cta_score * 0.20 +
            seo_score * 0.15 +
            readability_score * 0.10
        )
        
        return {
            "score": round(final_score, 1),
            "hook_strength": hook_score,
            "value_delivery": value_score,
            "cta_effectiveness": cta_score,
            "seo_optimization": seo_score,
            "readability": readability_score
        }
    
    def calculate_content_diversity(
        self,
        format_ratios: Dict[str, float],
        content_pillars: List[str],
        visual_diversity: str,
        tone_distribution: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculate Content Diversity Score (0-100)
        
        Formula:
        Diversity = (
            Format_Mix × 0.35 +
            Topic_Variety × 0.30 +
            Visual_Diversity × 0.20 +
            Tone_Range × 0.15
        )
        """
        # Format Mix (Shannon Entropy)
        format_mix_score = self._calculate_format_diversity(format_ratios)
        
        # Topic Variety
        pillar_count = len(content_pillars)
        if pillar_count >= 5:
            topic_score = 100
        elif pillar_count == 4:
            topic_score = 80
        elif pillar_count == 3:
            topic_score = 60
        elif pillar_count == 2:
            topic_score = 40
        else:
            topic_score = 20
        
        # Visual Diversity
        visual_scores = {'high': 100, 'medium': 60, 'low': 30}
        visual_score = visual_scores.get(visual_diversity, 50)
        
        # Tone Range
        max_tone = max(tone_distribution.values()) if tone_distribution else 0
        active_tones = sum(1 for v in tone_distribution.values() if v > 0.05)
        
        if max_tone <= 50 and active_tones >= 3:
            tone_score = 100
        elif max_tone <= 60 and active_tones >= 3:
            tone_score = 80
        elif active_tones >= 2:
            tone_score = 60
        else:
            tone_score = 40
        
        final_score = (
            format_mix_score * 0.35 +
            topic_score * 0.30 +
            visual_score * 0.20 +
            tone_score * 0.15
        )
        
        return {
            "score": round(final_score, 1),
            "format_mix": round(format_mix_score, 1),
            "topic_variety": topic_score,
            "visual_diversity": visual_score,
            "tone_range": tone_score
        }
    
    def detect_edge_cases(
        self,
        account_data: Dict[str, Any],
        engagement_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Detect edge cases that require special handling
        """
        flags = []
        
        account_age_days = account_data.get('accountAgeDays', 365)
        
        # 1. New Account (<30 days)
        is_new_account = account_age_days < 30
        if is_new_account:
            flags.append("new_account_no_benchmark_comparison")
        
        # 2. Viral Spike (>500% engagement increase in last 7 days)
        has_viral_spike = False
        if engagement_history and len(engagement_history) >= 7:
            recent_avg = sum(e.get('engagement', 0) for e in engagement_history[:7]) / 7
            older_avg = sum(e.get('engagement', 0) for e in engagement_history[7:14]) / max(len(engagement_history[7:14]), 1)
            if older_avg > 0 and recent_avg > older_avg * 5:
                has_viral_spike = True
                flags.append("viral_spike_detected_outlier")
        
        # 3. Niche Pivot (>60% content pillar inconsistency)
        niche_pivot_detected = False
        content_pillars = account_data.get('contentPillars', [])
        if content_pillars:
            recent_pillars = content_pillars[:10]
            older_pillars = content_pillars[10:20]
            if recent_pillars and older_pillars:
                overlap = len(set(recent_pillars) & set(older_pillars))
                if overlap < len(recent_pillars) * 0.4:
                    niche_pivot_detected = True
                    flags.append("niche_pivot_in_progress")
        
        # 4. Seasonal Account
        is_seasonal = account_data.get('isSeasonalAccount', False)
        if is_seasonal:
            flags.append("seasonal_account_adjusted_scoring")
        
        # 5. Engagement Pod Suspicion
        engagement_pod_suspected = False
        comment_timing = account_data.get('commentTimingData', [])
        if comment_timing:
            # Check for cluster of comments within 5 minutes
            clustered = sum(1 for c in comment_timing if c.get('seconds_after_post', 999) < 300)
            if clustered > len(comment_timing) * 0.5:
                engagement_pod_suspected = True
                flags.append("engagement_pod_suspected_authenticity_warning")
        
        return {
            "is_new_account": is_new_account,
            "has_viral_spike": has_viral_spike,
            "niche_pivot_detected": niche_pivot_detected,
            "is_seasonal_account": is_seasonal,
            "engagement_pod_suspected": engagement_pod_suspected,
            "flags": flags
        }
    
    def prioritize_recommendations(
        self,
        recommendations: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """
        Prioritize recommendations using impact/effort matrix
        
        Priority Matrix:
        P1 (Immediate): High impact, Low effort
        P2 (Short-term): High impact, Medium effort OR Medium impact, Low effort
        P3 (Planned): High impact, High effort OR Medium impact, Medium effort
        P4 (Low Priority): Medium impact, High effort OR Low impact, Low/Medium effort
        P5 (Backlog): Low impact, High effort
        """
        matrix = {
            "p1_immediate": [],
            "p2_short_term": [],
            "p3_planned": [],
            "p4_low_priority": [],
            "p5_backlog": []
        }
        
        for rec in recommendations:
            impact = rec.get('impact', 'medium')
            effort = rec.get('effort', 'medium')
            action = rec.get('action', '')
            
            if impact == 'high' and effort == 'low':
                matrix["p1_immediate"].append(action)
            elif (impact == 'high' and effort == 'medium') or (impact == 'medium' and effort == 'low'):
                matrix["p2_short_term"].append(action)
            elif (impact == 'high' and effort == 'high') or (impact == 'medium' and effort == 'medium'):
                matrix["p3_planned"].append(action)
            elif (impact == 'medium' and effort == 'high') or (impact == 'low' and effort in ['low', 'medium']):
                matrix["p4_low_priority"].append(action)
            else:
                matrix["p5_backlog"].append(action)
        
        return matrix
    
    def get_niche_benchmarks(self, niche: str, tier: str) -> Dict[str, Any]:
        """
        Get niche-specific benchmarks for comparison
        """
        # Base benchmarks by tier
        tier_benchmarks = {
            "nano": {"avg_er": 7.0, "growth_rate": 8.0, "save_rate": 2.0, "share_rate": 0.8},
            "micro": {"avg_er": 4.5, "growth_rate": 5.0, "save_rate": 1.5, "share_rate": 0.5},
            "mid": {"avg_er": 3.0, "growth_rate": 3.0, "save_rate": 1.2, "share_rate": 0.4},
            "macro": {"avg_er": 1.8, "growth_rate": 2.0, "save_rate": 0.8, "share_rate": 0.3},
            "mega": {"avg_er": 1.0, "growth_rate": 1.0, "save_rate": 0.5, "share_rate": 0.2}
        }
        
        base = tier_benchmarks.get(tier, tier_benchmarks["micro"])
        
        # Apply niche modifier
        niche_key = niche.lower().replace(' ', '_')
        niche_mod = self.niche_adjustments.get(niche_key, {})
        modifier = niche_mod.get('expected_er_modifier', 1.0)
        
        return {
            "niche_average_er": round(base["avg_er"] * modifier, 2),
            "niche_growth_rate": base["growth_rate"],
            "niche_save_rate": round(base["save_rate"] * modifier, 2),
            "niche_share_rate": round(base["share_rate"] * modifier, 2),
            "adjustment_applied": modifier != 1.0,
            "niche_notes": niche_mod.get('notes', '')
        }
