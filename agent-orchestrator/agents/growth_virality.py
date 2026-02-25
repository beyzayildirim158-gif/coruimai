# Growth Architect Agent - Büyüme Stratejisti ve Viral Potansiyel Uzmanı
# Version: 2.0
# PhD Seviyesi Büyüme Analizi ve Strateji Geliştirme

from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent
import json
import math
from datetime import datetime


class GrowthViralityAgent(BaseAgent):
    """
    Growth Architect Agent v2.0
    Role: Advanced growth strategy, viral potential analysis, and competitive intelligence
    
    Kapsamlı Uzmanlık Alanları:
    - Büyüme metrikleri ve formülleri
    - Büyüme pattern analizi
    - Organik ve paid büyüme kanalları
    - Viral büyüme metrikleri
    - Rekabet analizi
    - Büyüme stratejileri ve roadmap
    - Risk değerlendirmesi
    """
    
    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "Growth Architect"
        self.role = "Growth Strategy & Viral Potential Expert"
        self.specialty = "Growth metrics, competitor analysis, viral engineering, strategic planning"
        
        # Initialize all configuration data
        self.growth_categories = self._init_growth_categories()
        self.growth_benchmarks = self._init_growth_benchmarks()
        self.growth_patterns = self._init_growth_patterns()
        self.organic_channels = self._init_organic_channels()
        self.growth_playbook = self._init_growth_playbook()
        self.risk_matrix = self._init_risk_matrix()
        
        # 2026 Advanced Instagram Growth Strategies
        self.instagram_2026_strategies = self._init_2026_strategies()
    
    def _init_growth_categories(self) -> Dict[str, Any]:
        """Initialize growth rate categories"""
        return {
            "explosive": {
                "rate_min": 20,
                "rate_max": float('inf'),
                "assessment": "Viral/paid growth",
                "sustainability": "low",
                "typical_duration": "1-3 months"
            },
            "rapid": {
                "rate_min": 10,
                "rate_max": 20,
                "assessment": "Excellent organic",
                "sustainability": "medium",
                "typical_duration": "3-6 months"
            },
            "healthy": {
                "rate_min": 5,
                "rate_max": 10,
                "assessment": "Good performance",
                "sustainability": "high",
                "typical_duration": "6-12 months"
            },
            "moderate": {
                "rate_min": 2,
                "rate_max": 5,
                "assessment": "Average",
                "sustainability": "high",
                "typical_duration": "ongoing"
            },
            "slow": {
                "rate_min": 0,
                "rate_max": 2,
                "assessment": "Needs optimization",
                "sustainability": "high",
                "typical_duration": "ongoing"
            },
            "declining": {
                "rate_min": float('-inf'),
                "rate_max": 0,
                "assessment": "Urgent action needed",
                "sustainability": "n/a",
                "typical_duration": "n/a"
            }
        }
    
    def _init_growth_benchmarks(self) -> Dict[str, Dict[str, float]]:
        """Initialize growth benchmarks by follower tier"""
        return {
            "0-1K": {"low": 5, "average": 15, "good": 30, "excellent": 30},
            "1K-5K": {"low": 3, "average": 8, "good": 15, "excellent": 15},
            "5K-10K": {"low": 2, "average": 5, "good": 10, "excellent": 10},
            "10K-25K": {"low": 1.5, "average": 4, "good": 8, "excellent": 8},
            "25K-50K": {"low": 1, "average": 3, "good": 6, "excellent": 6},
            "50K-100K": {"low": 0.8, "average": 2, "good": 4, "excellent": 4},
            "100K-500K": {"low": 0.5, "average": 1.5, "good": 3, "excellent": 3},
            "500K+": {"low": 0.3, "average": 1, "good": 2, "excellent": 2}
        }
    
    def _init_growth_patterns(self) -> Dict[str, Any]:
        """Initialize growth pattern definitions"""
        return {
            "exponential": {
                "description": "Her dönem artan hızda büyüme",
                "indicator": "Growth rate artıyor",
                "cause": "Viral content, algorithm favor",
                "sustainability": "Düşük (3-6 ay)",
                "action": "Capitalize quickly, prepare for normalization"
            },
            "linear": {
                "description": "Sabit sayıda yeni takipçi",
                "indicator": "Tutarlı net adds",
                "cause": "Consistent content strategy",
                "sustainability": "Yüksek",
                "action": "Maintain and optimize"
            },
            "logarithmic": {
                "description": "Yavaşlayan büyüme",
                "indicator": "Growth rate düşüyor",
                "cause": "Niche saturation, plateau",
                "sustainability": "Medium",
                "action": "Pivot veya niche expansion"
            },
            "s_curve": {
                "description": "Yavaş→Hızlı→Yavaş",
                "indicator": "Inflection points",
                "cause": "Normal lifecycle",
                "sustainability": "Expected",
                "action": "Yeni S-curve başlat"
            },
            "stagnant": {
                "description": "Minimal değişim",
                "indicator": "<1% monthly change",
                "cause": "Content/strategy issues",
                "sustainability": "Poor",
                "action": "Major strategy revision"
            },
            "declining": {
                "description": "Net negatif büyüme",
                "indicator": "Unfollows > New follows",
                "cause": "Quality drop, relevance loss",
                "sustainability": "Critical",
                "action": "Urgent intervention"
            }
        }
    
    def _init_organic_channels(self) -> Dict[str, Any]:
        """Initialize organic growth channel analysis"""
        return {
            "explore_page": {
                "potential": 5,
                "quality": 4,
                "sustainability": 3,
                "optimization_factors": [
                    "High engagement rate (especially saves/shares)",
                    "Fast engagement velocity",
                    "Content relevance to user interests",
                    "Account authority score",
                    "No policy violations",
                    "Original content preference"
                ]
            },
            "reels_algorithm": {
                "potential": 5,
                "quality": 3,
                "sustainability": 3,
                "optimization_factors": [
                    "Watch time percentage (>50% ideal)",
                    "Replay rate",
                    "Share rate (highest weight)",
                    "Audio trend alignment",
                    "Caption/hashtag relevance",
                    "Posting consistency"
                ]
            },
            "hashtags": {
                "potential": 3,
                "quality": 3,
                "sustainability": 4,
                "optimization_factors": [
                    "Niche-specific selection",
                    "Size distribution (small/medium/large)",
                    "Relevance to content",
                    "Trending hashtag inclusion"
                ]
            },
            "search_seo": {
                "potential": 3,
                "quality": 5,
                "sustainability": 5,
                "optimization_factors": [
                    "Username optimization",
                    "Bio keywords",
                    "Caption SEO",
                    "Alt text usage"
                ]
            },
            "shares_dms": {
                "potential": 4,
                "quality": 5,
                "sustainability": 4,
                "optimization_factors": [
                    "Shareable content creation",
                    "Save-worthy value",
                    "Emotional triggers",
                    "Utility content"
                ]
            },
            "collaborations": {
                "potential": 4,
                "quality": 4,
                "sustainability": 3,
                "optimization_factors": [
                    "Partner selection",
                    "Audience overlap",
                    "Content quality",
                    "Cross-promotion strategy"
                ]
            },
            "cross_promotion": {
                "potential": 3,
                "quality": 4,
                "sustainability": 4,
                "optimization_factors": [
                    "Platform presence",
                    "Traffic funneling",
                    "Content repurposing",
                    "Link strategies"
                ]
            },
            "word_of_mouth": {
                "potential": 3,
                "quality": 5,
                "sustainability": 5,
                "optimization_factors": [
                    "Community building",
                    "Brand advocacy",
                    "User experience",
                    "Memorable content"
                ]
            }
        }
    
    def _init_growth_playbook(self) -> Dict[str, Any]:
        """Initialize growth strategy playbook"""
        return {
            "tier1_quick_wins": {
                "timeframe": "1-2 weeks",
                "strategies": {
                    "posting_optimization": {
                        "action": "Optimal saatlerde paylaşım, frekans artırma",
                        "expected_impact": "+10-20% reach",
                        "difficulty": "easy"
                    },
                    "hashtag_strategy": {
                        "action": "Niche-specific hashtags, size distribution optimize",
                        "expected_impact": "+15-25% discovery",
                        "difficulty": "easy"
                    },
                    "engagement_boost": {
                        "action": "İlk 1 saat aktif engagement, comment yanıtlama",
                        "expected_impact": "+20% algorithm favor",
                        "difficulty": "easy"
                    },
                    "bio_optimization": {
                        "action": "Clear value proposition, strong CTA",
                        "expected_impact": "+10-15% profile→follow",
                        "difficulty": "easy"
                    }
                }
            },
            "tier2_medium_term": {
                "timeframe": "1-3 months",
                "strategies": {
                    "content_pillar_expansion": {
                        "action": "Yeni content türleri test, winning formats scale",
                        "expected_impact": "+25-40% engagement",
                        "difficulty": "medium"
                    },
                    "reels_strategy": {
                        "action": "Trending audio kullanımı, hook optimization",
                        "expected_impact": "+50-100% reach",
                        "difficulty": "medium"
                    },
                    "collaboration_campaign": {
                        "action": "Niche influencer partnerships, cross-promotion",
                        "expected_impact": "+30-50% new followers",
                        "difficulty": "medium"
                    },
                    "series_content": {
                        "action": "Recurring content series, anticipation building",
                        "expected_impact": "+20% retention",
                        "difficulty": "medium"
                    }
                }
            },
            "tier3_strategic": {
                "timeframe": "3-6 months",
                "strategies": {
                    "community_building": {
                        "action": "Engagement rituals, user spotlight",
                        "expected_impact": "+40% loyalty",
                        "difficulty": "hard"
                    },
                    "cross_platform": {
                        "action": "TikTok/YouTube repurpose, traffic funneling",
                        "expected_impact": "+25% new audience",
                        "difficulty": "hard"
                    },
                    "authority_building": {
                        "action": "Expert positioning, media features",
                        "expected_impact": "+50% credibility",
                        "difficulty": "hard"
                    },
                    "viral_engineering": {
                        "action": "Trend hijacking, controversial takes",
                        "expected_impact": "Variable, high risk/reward",
                        "difficulty": "hard"
                    }
                }
            }
        }
    
    def _init_risk_matrix(self) -> Dict[str, Any]:
        """Initialize growth risk assessment matrix"""
        return {
            "high_risk": {
                "factors": [
                    "Algorithm dependency (single channel)",
                    "Viral-only growth strategy",
                    "Paid growth without organic base",
                    "Single content format reliance",
                    "Trend-dependent content"
                ],
                "mitigation": [
                    "Diversify content formats",
                    "Build email list",
                    "Cross-platform presence",
                    "Community-first approach"
                ]
            },
            "medium_risk": {
                "factors": [
                    "Competitor saturation",
                    "Niche size limitations",
                    "Platform policy changes",
                    "Audience fatigue",
                    "Creator burnout"
                ],
                "mitigation": [
                    "Unique positioning",
                    "Niche down further",
                    "Quality over quantity",
                    "First-mover on trends"
                ]
            },
            "low_risk": {
                "factors": [
                    "Diversified growth channels",
                    "Strong organic base",
                    "Engaged community",
                    "Multiple content formats",
                    "Sustainable posting pace"
                ],
                "mitigation": [
                    "Maintain current strategy",
                    "Gradual optimization",
                    "Monitor for changes"
                ]
            }
        }
    
    def _init_2026_strategies(self) -> Dict[str, Any]:
        """
        2026 Instagram Masterclass: Algoritma, Erişim ve Büyüme Mühendisliği
        Gelişmiş büyüme taktikleri ve viral stratejiler
        """
        return {
            "algorithm_pillars_2026": {
                "stop_rate": {
                    "description": "Kaydırmayı durdurma gücü - İlk 1.5 saniyede dikkat çekme",
                    "weight": 35,
                    "optimization": [
                        "İlk karede şok/soru/olay kullan",
                        "Giriş yok (No Intro) - direkt konuya gir",
                        "İlk kesim 1.5 saniyeden kısa olmalı",
                        "Görsel kanca: Konum/şehir ismi ekle (yerel algoritma tetikleyici)"
                    ]
                },
                "retention_rate": {
                    "description": "Tutma oranı - Videoyu sonuna kadar izletme",
                    "weight": 40,
                    "optimization": [
                        "İdeal video süresi: 7-15 saniye (viral formatlar için)",
                        "Maksimum süre: 3 dakika (Reels)",
                        "Loop suspense: Son cümleyi başa bağla (izlenme %200'e çıkar)",
                        "Ortalama izlenme süresi video süresini geçmeli (viral aday)"
                    ]
                },
                "reaction_speed": {
                    "description": "Tepki hızı - İlk dakikalarda etkileşim alma",
                    "weight": 25,
                    "critical_window": "20 dakika",
                    "tactics": [
                        "Yorum sabitle: Merak uyandıran tartışma başlatıcı",
                        "Hikayede anket ile paylaş (tıklama etkileşimi)",
                        "DM desteği: İkinci hesaptan 40-50 kişiye gönder",
                        "ManyChat entegrasyonu: 'X yaz link atayım' diyerek yorum artır"
                    ]
                }
            },
            "trial_reels_system": {
                "concept": "Takipçileri spmlemeden sırf yabancılara gösterilen deneme videoları",
                "strategy": {
                    "distribution": "50/50 kural: Haftalık içeriğin yarısı normal, yarısı trial",
                    "target_audience": "Sadece seni takip etmeyenler (Explore/Discovery)",
                    "content_source": "Geçmişte tutmuş videoları repost et (yeni üretim gerekmez)",
                    "testing": "Aynı videoyu 3 farklı hook ile test et"
                },
                "analysis_metrics": {
                    "success_threshold": "Takipçi olmayanlara erişim %50+",
                    "tracking_method": "Son 20 video Excel analizi",
                    "key_metric": "Ortalama izlenme süresi > Video süresi = Viral aday"
                },
                "implementation": [
                    "Geçmişte en çok takipçi kazandıran videoları bul",
                    "Hiç değiştirmeden Trial Reel olarak paylaş",
                    "Her gün 1-2 Trial Reel yayınla",
                    "Normal feed postları ile dengeye",
                    "24 saat sonra metrikleri analiz et"
                ]
            },
            "technical_optimization_2026": {
                "account_health": {
                    "green_check_rule": "Ayarlar > Hesap Durumu - Tüm maddeler yeşil tik olmalı",
                    "frozen_account_fix": [
                        "Profil, Hesap Durumu ve düşük izlenme ekran görüntüsü al",
                        "Yardım > Sorun Bildir: 'Teknik kusursuz ama erişim kısıtlaması' gönder"
                    ]
                },
                "critical_settings": {
                    "high_quality_upload": "AÇIK - Medya Kalitesi > En Yüksek Kalite",
                    "hide_like_count": "AÇIK - Az beğeni psikolojik engel yaratır",
                    "disable_download": "AÇIK - Instagram içi paylaşımı teşvik et",
                    "flag_for_review": "KAPALI - Gerçek takipçilerin spam filtresi riski"
                }
            },
            "viral_engineering": {
                "hook_tactics": {
                    "1.5_second_rule": "İlk sahne 1.5sn'den uzun olmamalı, hemen kesim değişmeli",
                    "no_intro": "Merhaba/Selam gibi girişler kullanma - direkt olay",
                    "visual_hook": "Video üzerine konum/şehir ismi yaz (yerel algoritma)",
                    "loop_technique": "Son cümleyi başa bağla - kullanıcı fark etmeden tekrar izler"
                },
                "format_optimization": {
                    "duration": {
                        "ideal_viral": "7-15 saniye",
                        "maximum_reels": "180 saniye (3 dakika)",
                        "minimum": "3 saniye"
                    },
                    "music": "Trend müzik kullan - Yukarı ok (↗) işaretli olanlar zorunlu",
                    "cuts": "İlk kesim kısa, ardından hızlı kesimler",
                    "text_overlay": "Konum adı mutlaka ekle (lokal boost)"
                }
            },
            "push_protocol": {
                "first_20_minutes": {
                    "importance": "Kader anı - Algoritma videoyu test eder",
                    "actions": [
                        "Uygulamadan çıkma - aktif kal",
                        "Yorum sabitle (tartışma başlatıcı)",
                        "Hikayede anket ile paylaş (tıklama etkileşimi)",
                        "İkinci hesaptan DM yoluyla 40-50 kişiye gönder"
                    ]
                },
                "manual_trigger": {
                    "dm_hack": "Farklı hesaptan yeni videonun linkini toplu gönder",
                    "simulation": "Dışarıdan paylaşım trafiği simülasyonu yaratır",
                    "signal": "Keşfet algoritmasına 'Bu video çok paylaşılıyor' sinyali"
                },
                "automation": {
                    "manychat": "Yoruma 'X yaz link atayım' otomasyonu",
                    "benefits": ["Yorum sayısı artar", "DM kutusu aktif olur", "Bot etkileşimi tetikler"]
                }
            },
            "success_indicators": {
                "viral_signals": [
                    "Takipçi olmayanlara erişim %50+",
                    "Ortalama izlenme süresi > Video süresi",
                    "İlk 20 dakikada %5+ etkileşim oranı",
                    "Paylaşım oranı yüksek (share > save)",
                    "Yorum/beğeni oranı %3+"
                ],
                "growth_indicators": [
                    "Trial Reels'ten düzenli takipçi akışı",
                    "Keşfet sayfası görünürlüğü artışı",
                    "DM/mesaj trafiği yükselişi",
                    "Profil ziyaret oranı artışı"
                ]
            },
            "7_step_implementation": {
                "step_1": "Kontrol: Hesap Durumu yeşil mi? (Ayarlar kontrolü)",
                "step_2": "Ayarla: Kalite AÇIK, Beğeni KAPALI, İndirme KAPALI",
                "step_3": "Seç: Geçmişte tutmuş video veya trend müzikli yeni video",
                "step_4": "Düzenle: 1.5sn kanca + konum metni + loop sonu",
                "step_5": "Paylaş: Trial Reel (deneme) olarak yayınla",
                "step_6": "Boost: 20dk içinde sabitle + anket + DM dağıt",
                "step_7": "Analiz: 24 saat sonra takipçi olmayan erişim %50+ kontrolü"
            }
        }
    
    def get_system_prompt(self) -> str:
        return """Sen Growth Architect Agent'sın - Büyüme Stratejisti ve Viral Potansiyel Uzmanı.

## VERİ EKSİKLİĞİ KURALI (KRİTİK)
Eğer sana sağlanan veride geçmiş takipçi büyüme geçmişi (followerHistory / followerGrowth) yoksa:
- Bunu kritik hata olarak değerlendirme.
- Şu ifadeyi kullan: "Yeterli geçmiş veri oluşana kadar büyüme hızı hesaplanmamaktadır."
- Mevcut post engagement verileri üzerinden büyüme potansiyelini tahmin et.
- Büyüme analizini tamamen atlama; post frequency, engagement trend ve içerik kalitesinden büyüme çıkarsaması yap.


## TEMEL UZMANLIK ALANLARIN:

### 1. BÜYÜME METRİKLERİ VE FORMÜLLER

**Temel Büyüme Hesaplamaları:**

1. Net Growth Rate (NGR):
   NGR = ((New_Followers - Unfollows) / Starting_Followers) × 100

2. Gross Growth Rate (GGR):
   GGR = (New_Followers / Starting_Followers) × 100

3. Churn Rate:
   Churn = (Unfollows / Starting_Followers) × 100

4. Growth Velocity:
   Velocity = Net_New_Followers / Time_Period

5. Compound Monthly Growth Rate (CMGR):
   CMGR = ((Ending_Followers / Starting_Followers)^(1/months) - 1) × 100

6. Follower Doubling Time:
   Doubling_Time = ln(2) / ln(1 + Monthly_Growth_Rate)

**Büyüme Kategorileri:**
| Aylık Büyüme | Kategori | Değerlendirme |
|--------------|----------|---------------|
| >20% | Explosive | Viral/paid growth |
| 10-20% | Rapid | Excellent organic |
| 5-10% | Healthy | Good performance |
| 2-5% | Moderate | Average |
| 0-2% | Slow | Needs optimization |
| <0% | Declining | Urgent action needed |

**Takipçi Büyüklüğüne Göre Benchmark:**
| Takipçi | Düşük | Orta | İyi | Harika |
|---------|-------|------|-----|--------|
| 0-1K | <5% | 5-15% | 15-30% | >30% |
| 1K-5K | <3% | 3-8% | 8-15% | >15% |
| 5K-10K | <2% | 2-5% | 5-10% | >10% |
| 10K-25K | <1.5% | 1.5-4% | 4-8% | >8% |
| 25K-50K | <1% | 1-3% | 3-6% | >6% |
| 50K-100K | <0.8% | 0.8-2% | 2-4% | >4% |
| 100K-500K | <0.5% | 0.5-1.5% | 1.5-3% | >3% |
| 500K+ | <0.3% | 0.3-1% | 1-2% | >2% |

### 2. BÜYÜME PATTERN ANALİZİ

**Pattern Tipleri:**

1. **Exponential (Üstel):**
   - Pattern: Her dönem artan hızda büyüme
   - Gösterge: Growth rate artıyor
   - Sebep: Viral content, algorithm favor
   - Sürdürülebilirlik: Düşük (3-6 ay)

2. **Linear (Doğrusal):**
   - Pattern: Sabit sayıda yeni takipçi
   - Gösterge: Tutarlı net adds
   - Sebep: Consistent content strategy
   - Sürdürülebilirlik: Yüksek

3. **Logarithmic (Logaritmik):**
   - Pattern: Yavaşlayan büyüme
   - Gösterge: Growth rate düşüyor
   - Sebep: Niche saturation, plateau
   - Aksiyon: Pivot veya niche expansion

4. **S-Curve:**
   - Pattern: Yavaş→Hızlı→Yavaş
   - Gösterge: Inflection points
   - Aksiyon: Yeni S-curve başlat

5. **Stagnant (Durağan):**
   - Pattern: Minimal değişim (<1%)
   - Aksiyon: Major strategy revision

6. **Declining (Düşüş):**
   - Pattern: Unfollows > New follows
   - Aksiyon: Urgent intervention

### 3. BÜYÜME KANALLARI

**Organik Kanal Etkinliği:**
| Kanal | Potansiyel | Kalite | Sürdürülebilir |
|-------|------------|--------|----------------|
| Explore Page | ★★★★★ | ★★★★ | ★★★ |
| Reels Algorithm | ★★★★★ | ★★★ | ★★★ |
| Hashtags | ★★★ | ★★★ | ★★★★ |
| Search/SEO | ★★★ | ★★★★★ | ★★★★★ |
| Shares/DMs | ★★★★ | ★★★★★ | ★★★★ |
| Collaborations | ★★★★ | ★★★★ | ★★★ |
| Cross-promotion | ★★★ | ★★★★ | ★★★★ |
| Word of Mouth | ★★★ | ★★★★★ | ★★★★★ |

**Kanal Etkinlik Formülü:**
Channel_Effectiveness = (Reach × 0.30) + (Quality × 0.30) + (Conversion × 0.25) + (Sustainability × 0.15)

### 4. PAID vs ORGANIC TESPİT

**Organic Growth Signals:**
- Gradual, consistent growth
- Engagement rate stable/improving
- Comments relevant and varied
- Demographics match content
- Growth correlates with content

**Paid/Inorganic Signals:**
- Sudden spikes without viral content
- ER drops significantly after growth
- Generic/bot-like comments
- Follower demographics mismatch
- High unfollow rate post-spike

### 5. VİRAL BÜYÜME ANALİZİ

**Viral Coefficient (K):**
K = Invites_Per_User × Conversion_Rate
- K > 1: Viral (self-sustaining)
- K = 1: Stable
- K < 1: Needs external acquisition

**Post-Viral Retention:**
- Excellent: >70%
- Good: 50-70%
- Average: 30-50%
- Poor: <30%

### 6. REKABET ANALİZİ

**Competitor Types:**
- Direct: Aynı niche, benzer size (0.5x-2x)
- Aspirational: 5-10x size, best practice
- Indirect: Farklı niche, aynı audience

**Competitive Position Score:**
Position = Σ(Your_Metric / Competitor_Avg × Weight)

Weights: Growth 0.25, Engagement 0.25, Content 0.20, Audience 0.15, Consistency 0.15

- >1.2: Market Leader
- 1.0-1.2: Strong Competitor
- 0.8-1.0: Average
- 0.6-0.8: Below Average
- <0.6: Lagging

### 7. GAP ANALİZİ

**Gap Türleri:**
- Content Gaps: Topics, formats, timing
- Audience Gaps: Demographics, segments, geo
- Strategy Gaps: Channels, features, monetization

**Gap Priority Matrix:**
|  | Easy to Close | Hard to Close |
|--|---------------|---------------|
| High Impact | PRIORITY 1 | PRIORITY 2 |
| Low Impact | PRIORITY 3 | IGNORE |

### 8. BÜYÜME STRATEJİLERİ

**Tier 1 - Quick Wins (1-2 hafta):**
- Posting Optimization: +10-20% reach
- Hashtag Strategy: +15-25% discovery
- Engagement Boost: +20% algorithm favor
- Bio Optimization: +10-15% profile→follow

**Tier 2 - Medium Term (1-3 ay):**
- Content Pillar Expansion: +25-40% engagement
- Reels Strategy: +50-100% reach
- Collaboration Campaign: +30-50% new followers
- Series Content: +20% retention

**Tier 3 - Strategic (3-6 ay):**
- Community Building: +40% loyalty
- Cross-Platform: +25% new audience
- Authority Building: +50% credibility
- Viral Engineering: Variable, high risk/reward

### 9. BÜYÜME PROJEKSİYONU

**Projeksiyon Modelleri:**
- Conservative: Current rate maintained
- Moderate: 1.5x current rate
- Aggressive: 2-3x current rate

**Confidence Levels:**
- 1-3 months: ±15%
- 3-6 months: ±25%
- 6-12 months: ±40%
- 12+ months: ±60%

**Milestone Calculation:**
Time_To_Milestone = ln(Target / Current) / ln(1 + Monthly_Rate)

### 10. RİSK DEĞERLENDİRMESİ

**High Risk Factors:**
- Algorithm dependency
- Viral-only strategy
- Paid without organic
- Single format reliance
- Trend dependency

**Mitigation Strategies:**
- Diversify channels
- Build email list
- Cross-platform presence
- Community-first approach

### 11. 2026 BÜYÜME MÜHENDİSLİĞİ (GROWTH HACKING) STRATEJİLERİ

**🤖 OTOMASYON KURULUMU (ManyChat vb.):**

1. **Yorum -> DM Sistemi:**
   - "Link için 'X' yaz" kurgusu kur
   - ÖNCELİKLE "Takip Kontrolü" yap
   - Takip etmiyorsa: "Önce takip etmelisin" mesajı gönder
   - Bu sistem etkileşimi %200-400 artırabilir

2. **Takip -> DM Sistemi:**
   - Yeni takipçiye otomatik "Hoş geldin" mesajı
   - SATIŞ YAPMA - sadece samimi karşılama
   - 5 DAKİKA GECİKMELİ gönder (spam algılanmasın)
   - Örnek: "Aramıza hoş geldin! Hangi konularda içerik görmek istersin?"

**⚡ STD STRATEJİSİ (Erişim Patlatma):**
- Erişim düştüğünde VEYA tatil dönüşü uygula:
  1. 48 SAAT SESSİZLİK - hikaye/post ATMA (algoritmayı sıfırla)
  2. TEK HİKAYE - sadece metin içeren hikaye paylaş
  3. DM ETKİLEŞİM TETİKLE - "İndirim kodu için 'KOD' yaz" gibi
  4. %100 etkileşim = ERİŞİMİ PATLAT

**♻️ UPCYCLING (Geri Dönüşüm) STRATEJİSİ:**
- 90 günden eski içerikleri yeniden paylaş
- Sadece en iyileri DEĞİL, ortalama olanları da dene
- Trial Reel OLMAYANLARI seç
- Aynı içerik farklı zamanda farklı performans gösterebilir

**📊 GÜNLÜK RUTİN (Maksimum Verim):**
- 10 dakika: Yorumlara cevap ver, SORUYLA BİTİR (yorum zinciri uzasın)
- Üretim: 1 adet "B-" kalitesinde Reel veya Carousel (mükemmel OLMAYAN)
- Test: Mümkünse 1 adet basit Trial Reel at

**📅 HAFTALIK RUTİN:**
- Analiz: Hangi hook çalıştı? Hangi konu çok kaydedildi?
- Upcycling: 3 ay öncesine git, eski post'u yeniden paylaş/düzenle
- Otomasyon Kontrolü: DM sistemleri düzgün çalışıyor mu?

**🧠 ZİHNİYET DEĞİŞİMİ - 2026:**
- MÜKEMMELİYETÇİLİK = DÜŞMAN
- PAYLAŞIM = Veri toplama aracı (performans verisi)
- TAKİPÇİ = Rakam değil, DİYALOG kurulacak insan

**🎯 MOMENTUM YÖNETİMİ:**
- Haftada MİNİMUM 1 içerik = Momentum kaybını önle
- 14+ gün boşluk = ALGORİTMA CEZA (-25% erişim)
- Burst posting (5+/gün) = SPAM algısı riski

OUTPUT FORMAT: Sadece geçerli JSON objesi döndür."""

    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        username = account_data.get('username', 'unknown') or 'unknown'
        followers = account_data.get('followers', 0) or 0
        following = account_data.get('following', 0) or 0
        posts = account_data.get('posts', 0) or 0
        engagement_rate = account_data.get('engagementRate', 0) or 0
        avg_likes = account_data.get('avgLikes', 0) or 0
        avg_comments = account_data.get('avgComments', 0) or 0
        niche = account_data.get('niche', 'General') or 'General'
        bio = account_data.get('bio', 'No bio') or 'No bio'
        is_business = account_data.get('isBusiness', False)
        verified = account_data.get('verified', False)
        
        # Growth data
        growth_data = account_data.get('growthData', {})
        monthly_growth_rates = growth_data.get('monthlyRates', [])
        recent_followers_gained = growth_data.get('recentGained', 0)
        recent_followers_lost = growth_data.get('recentLost', 0)
        
        # Content performance data
        content_data = account_data.get('contentData', {})
        viral_posts = content_data.get('viralPosts', 0)
        avg_reach = content_data.get('avgReach', 0)
        
        # Competitor data
        competitor_data = account_data.get('competitorData', {})
        
        # Get appropriate benchmark
        benchmark = self._get_benchmark_for_followers(followers)
        
        # Detect growth pattern
        pattern = self._detect_growth_pattern(monthly_growth_rates)
        
        return f"""Bu Instagram hesabı için kapsamlı Growth analizi yap:

## HESAP VERİLERİ:
- Username: @{username}
- Takipçi: {followers:,}
- Takip: {following:,}
- Gönderi Sayısı: {posts:,}
- Engagement Rate: {engagement_rate:.2f}%
- Ortalama Like: {avg_likes:,.0f}
- Ortalama Yorum: {avg_comments:,.0f}
- Niche: {niche}
- Bio: {bio}
- İş Hesabı: {is_business}
- Onaylı: {verified}

## BÜYÜME VERİLERİ:
- Aylık Büyüme Oranları: {json.dumps(monthly_growth_rates) if monthly_growth_rates else 'Veri yok'}
- Son Dönem Kazanılan: {recent_followers_gained:,}
- Son Dönem Kaybedilen: {recent_followers_lost:,}

## İÇERİK PERFORMANSI:
- Viral Postlar: {viral_posts}
- Ortalama Reach: {avg_reach:,}

## RAKİP VERİLERİ:
{json.dumps(competitor_data, indent=2) if competitor_data else 'Veri yok'}

## BENCHMARK (Bu Takipçi Seviyesi İçin):
{json.dumps(benchmark, indent=2)}

## TESPİT EDİLEN BÜYÜME PATTERNİ:
{pattern}

## ANALİZ GÖREVLERİ:

1. **Büyüme Metrikleri Hesapla:**
   - Net Growth Rate (NGR)
   - Gross Growth Rate (GGR)
   - Churn Rate
   - Growth Velocity
   - Varsa CMGR

2. **Büyüme Kategorisi Belirle:**
   - Explosive/Rapid/Healthy/Moderate/Slow/Declining

3. **Pattern Analizi:**
   - Exponential/Linear/Logarithmic/S-Curve/Stagnant/Declining
   - Pattern sürdürülebilirliği
   - Gerekli aksiyonlar

4. **Kanal Analizi:**
   - Hangi kanallardan büyüme geliyor?
   - Kanal etkinlik skorları
   - Kullanılmayan kanallar

5. **Paid vs Organic Değerlendirmesi:**
   - Organik sinyaller
   - Şüpheli aktivite var mı?

6. **Viral Potansiyel:**
   - Historical viral rate
   - Viral coefficient tahmini
   - Post-viral retention

7. **Rekabet Analizi:**
   - Competitive position score
   - Gap'ler
   - Fırsatlar ve tehditler

8. **Büyüme Projeksiyonları:**
   - Conservative (3/6/12 ay)
   - Moderate (3/6/12 ay)
   - Aggressive (3/6/12 ay)
   - Milestone hesaplamaları

9. **Strateji Önerileri:**
   - Quick wins (Tier 1)
   - Medium term (Tier 2)
   - Strategic (Tier 3)

10. **Risk Değerlendirmesi:**
    - Risk faktörleri
    - Mitigation strategies

Aşağıdaki JSON yapısında yanıt ver:

{{
    "agent": "growth_architect",
    "analysis_timestamp": "{datetime.now().isoformat()}",
    "growth_overview": {{
        "current_followers": {followers},
        "monthly_growth_rate": 0,
        "growth_category": "healthy|moderate|slow|declining|rapid|explosive",
        "growth_trend": "improving|stable|declining",
        "growth_pattern": "exponential|linear|logarithmic|s_curve|stagnant|declining",
        "projected_followers_6mo": 0,
        "follower_doubling_time_months": 0
    }},
    "metrics": {{
        "growthPotential": 0,
        "followerGrowthRate": 0,
        "competitorGap": 0,
        "viralPotential": 0,
        "strategyEffectiveness": 0,
        "netGrowthRate": 0,
        "grossGrowthRate": 0,
        "churnRate": 0,
        "growthVelocity": 0,
        "cmgr": 0,
        "explorePagePotential": 0,
        "reelsViralPotential": 0,
        "hashtagEffectiveness": 0,
        "organicGrowthScore": 0,
        "sustainabilityScore": 0,
        "overallScore": 0
    }},
    "growth_metrics": {{
        "net_growth_rate": 0,
        "gross_growth_rate": 0,
        "churn_rate": 0,
        "growth_velocity": 0,
        "cmgr": 0
    }},
    "growth_analysis": {{
        "monthly_breakdown": [
            {{"month": "string", "start": 0, "end": 0, "rate": 0, "net_adds": 0}}
        ],
        "growth_sources": {{
            "explore_page": 0,
            "reels": 0,
            "hashtags": 0,
            "shares": 0,
            "collaborations": 0,
            "other": 0
        }},
        "pattern_analysis": {{
            "detected_pattern": "string",
            "pattern_description": "string",
            "sustainability": "low|medium|high",
            "recommended_action": "string"
        }},
        "organic_vs_paid": {{
            "assessment": "organic|mixed|suspected_paid",
            "organic_signals": [],
            "suspicious_signals": [],
            "confidence": 0
        }}
    }},
    "channel_analysis": {{
        "primary_channel": "string",
        "channel_effectiveness": {{
            "explore_page": {{"contribution": 0, "efficiency": 0, "potential": 0}},
            "reels": {{"contribution": 0, "efficiency": 0, "potential": 0}},
            "hashtags": {{"contribution": 0, "efficiency": 0, "potential": 0}},
            "shares": {{"contribution": 0, "efficiency": 0, "potential": 0}},
            "search_seo": {{"contribution": 0, "efficiency": 0, "potential": 0}},
            "collaborations": {{"contribution": 0, "efficiency": 0, "potential": 0}}
        }},
        "underutilized_channels": [],
        "channel_recommendations": []
    }},
    "viral_analysis": {{
        "viral_coefficient": 0,
        "viral_interpretation": "viral|stable|needs_acquisition",
        "historical_viral_rate": 0,
        "content_shareability": 0,
        "post_viral_retention": 0,
        "viral_content_opportunities": []
    }},
    "competitor_analysis": {{
        "competitors_identified": 0,
        "your_rank": 0,
        "competitive_position_score": 0,
        "position_category": "market_leader|strong|average|below_average|lagging",
        "avg_competitor_growth": 0,
        "growth_gap": "string",
        "key_differentiators": [],
        "gaps_identified": {{
            "content_gaps": [],
            "audience_gaps": [],
            "strategy_gaps": []
        }},
        "gap_priorities": [
            {{"gap": "string", "impact": "high|low", "difficulty": "easy|hard", "priority": 1}}
        ]
    }},
    "projections": {{
        "conservative": {{
            "3_month": 0,
            "6_month": 0,
            "12_month": 0,
            "assumptions": "string"
        }},
        "moderate": {{
            "3_month": 0,
            "6_month": 0,
            "12_month": 0,
            "assumptions": "string"
        }},
        "aggressive": {{
            "3_month": 0,
            "6_month": 0,
            "12_month": 0,
            "assumptions": "string"
        }},
        "confidence_levels": {{
            "3_month": "high",
            "6_month": "medium",
            "12_month": "low"
        }}
    }},
    "milestones": {{
        "next_milestone": 0,
        "estimated_time_months": 0,
        "confidence": "high|medium|low",
        "milestones_roadmap": [
            {{"target": 0, "estimated_date": "string", "probability": 0}}
        ]
    }},
    "risk_assessment": {{
        "overall_risk_level": "low|medium|high",
        "high_risk_factors": [],
        "medium_risk_factors": [],
        "low_risk_factors": [],
        "mitigation_strategies": []
    }},
    "findings": [
        {{
            "type": "strength|weakness|opportunity|threat",
            "category": "growth|channels|viral|competition|strategy",
            "finding": "TÜRKÇE - örn: Aylık %8.5 büyüme oranı sektör ortalamasının 2 katı üzerinde, bu organik erişim stratejisinin etkili olduğunu gösteriyor",
            "evidence": "TÜRKÇE - örn: Son 3 ayda 25.000 net takipçi artışı, Reels içerikler %45 daha fazla keşfet sayfası görünümü sağladı",
            "impact_score": 85
        }},
        {{
            "type": "opportunity",
            "category": "channels",
            "finding": "TÜRKÇE - örn: Hashtag stratejisi optimize edilmemiş, niche-spesifik etiketler kullanılmıyor",
            "evidence": "TÜRKÇE - örn: Mevcut postlarda sadece 5-8 genel hashtag var, sektöre özel 15-20 hashtag kullanımı %30 daha fazla keşfedilme sağlayabilir",
            "impact_score": 70
        }}
    ],
    "recommendations": [
        {{
            "priority": 1,
            "tier": "quick_win|medium_term|strategic",
            "category": "TÜRKÇE - örn: Hashtag Optimizasyonu",
            "action": "TÜRKÇE - örn: Niche-spesifik 15-20 hashtag içeren bir hashtag bankaası oluşturun ve her post için rotasyonlu kullanın",
            "expected_impact": "TÜRKÇE - örn: Keşfet sayfası görünürlüğünde %25-30 artış, aylık 3.000-5.000 yeni organik takipçi",
            "implementation": "TÜRKÇE - örn: 1) Rakip analizi yapın 2) 50 potansiyel hashtag listesi çıkarın 3) Engagement oranlarına göre test edin 4) En iyi performans gösteren 20'yi seçin",
            "difficulty": "easy|medium|hard",
            "timeframe": "TÜRKÇE - örn: 1-2 hafta içinde uygulanabilir"
        }}
    ],
    "growth_roadmap": {{
        "phase_1": {{
            "duration": "Month 1-2",
            "focus": "string",
            "actions": [],
            "target_growth": "string"
        }},
        "phase_2": {{
            "duration": "Month 3-4",
            "focus": "string",
            "actions": [],
            "target_growth": "string"
        }},
        "phase_3": {{
            "duration": "Month 5-6",
            "focus": "string",
            "actions": [],
            "target_growth": "string"
        }}
    }},
    "edge_cases": {{
        "is_new_account": false,
        "post_viral_spike": false,
        "at_saturation_point": false,
        "seasonal_business": false,
        "rebranding": false,
        "algorithm_impact": false,
        "special_notes": "string"
    }},
    "growthProjection": {{
        "description": "Detailed follower growth projections with assumptions",
        "currentGrowthRate": 0,
        "30_day_projection": {{
            "conservative": {{
                "followers": 0,
                "growth_rate_used": 0,
                "net_new_followers": 0
            }},
            "moderate": {{
                "followers": 0,
                "growth_rate_used": 0,
                "net_new_followers": 0
            }},
            "aggressive": {{
                "followers": 0,
                "growth_rate_used": 0,
                "net_new_followers": 0
            }}
        }},
        "90_day_projection": {{
            "conservative": {{
                "followers": 0,
                "growth_rate_used": 0,
                "net_new_followers": 0
            }},
            "moderate": {{
                "followers": 0,
                "growth_rate_used": 0,
                "net_new_followers": 0
            }},
            "aggressive": {{
                "followers": 0,
                "growth_rate_used": 0,
                "net_new_followers": 0
            }}
        }},
        "assumptions": {{
            "conservative": "Current rate maintained, no major changes",
            "moderate": "Optimizations implemented, 1.5x current rate",
            "aggressive": "All recommendations implemented, 2.5x current rate, potential viral content"
        }},
        "keyMilestones": [
            {{
                "milestone": "10K followers",
                "currentDistance": 0,
                "estimatedDays_conservative": 0,
                "estimatedDays_moderate": 0,
                "estimatedDays_aggressive": 0,
                "unlocks": ["Swipe-up stories", "Creator fund eligibility"]
            }}
        ],
        "formula_used": "Projected_Followers = Current × (1 + Monthly_Rate)^Months",
        "confidence": {{
            "30_day": "±15%",
            "90_day": "±25%"
        }}
    }},
    "competitorGapAnalysis": {{
        "description": "Detailed comparison with 5+ competitors",
        "formula_used": "Gap_Score = (Competitor_Metric - Your_Metric) / Competitor_Metric × 100",
        "competitors": [
            {{
                "handle": "@competitor1",
                "type": "direct|aspirational|indirect",
                "followers": 0,
                "followerGap": 0,
                "engagementRate": 0.0,
                "engagementGap": 0.0,
                "postingFrequency": 0,
                "frequencyGap": 0,
                "contentFormats": {{"reels": 0, "carousels": 0, "singles": 0}},
                "formatGaps": ["More reels needed", "Less single posts"],
                "strengthsToLearn": ["Strong hooks", "Consistent branding"],
                "weaknessesToExploit": ["Low engagement", "Inconsistent posting"],
                "overallGapScore": 0
            }}
        ],
        "aggregatedGaps": {{
            "followerGap": {{
                "vsAverage": 0,
                "vsLeader": 0,
                "percentileRank": 0
            }},
            "engagementGap": {{
                "vsAverage": 0,
                "vsLeader": 0,
                "percentileRank": 0
            }},
            "contentGap": {{
                "formatsMissing": [],
                "topicsUnderexplored": [],
                "timingOpportunities": []
            }},
            "strategyGap": {{
                "channelsUnderutilized": [],
                "featuresNotUsed": [],
                "monetizationGaps": []
            }}
        }},
        "competitorBestPractices": [
            {{
                "practice": "string",
                "usedBy": ["@competitor1", "@competitor2"],
                "yourStatus": "not_implemented|partially|fully",
                "priority": "high|medium|low",
                "implementationGuide": "string"
            }}
        ],
        "marketPositioning": {{
            "yourPosition": "leader|challenger|follower|nicher",
            "positionScore": 0,
            "recommendedStrategy": "string"
        }}
    }},
    "funnelAnalysis": {{
        "description": "AIDA funnel conversion analysis",
        "formula_used": "Stage_Conversion = (Next_Stage_Count / Current_Stage_Count) × 100",
        "awareness": {{
            "reach": 0,
            "impressions": 0,
            "profileVisits": 0,
            "sourceBreakdown": {{
                "explore": 0,
                "reels": 0,
                "hashtags": 0,
                "shares": 0,
                "search": 0,
                "other": 0
            }}
        }},
        "interest": {{
            "profileVisitToFollowRate": 0,
            "averageTimeOnProfile": "seconds",
            "contentViewDepth": 0,
            "bioClickRate": 0
        }},
        "desire": {{
            "saveRate": 0,
            "shareRate": 0,
            "websiteClicks": 0,
            "dmInquiries": 0,
            "storyReplies": 0
        }},
        "action": {{
            "followConversion": 0,
            "linkClicks": 0,
            "purchases": 0,
            "signups": 0,
            "bookings": 0
        }},
        "conversionRates": {{
            "awareness_to_interest": 0,
            "interest_to_desire": 0,
            "desire_to_action": 0,
            "overall_funnel_efficiency": 0
        }},
        "funnelLeaks": [
            {{
                "stage": "awareness|interest|desire|action",
                "issue": "string",
                "dropoffRate": 0,
                "fix": "string",
                "priority": "high|medium|low"
            }}
        ],
        "benchmarkComparison": {{
            "your_funnel_efficiency": 0,
            "niche_average": 0,
            "top_performer": 0
        }}
    }},
    "viralLoopStrategy": {{
        "description": "Viral loop optimization recommendations",
        "formula_used": "Viral_Coefficient (K) = Invites_Per_User × Conversion_Rate; K > 1 = Viral",
        "currentViralCoefficient": 0,
        "targetViralCoefficient": 1.2,
        "shareabilityScore": 0,
        "viralMechanics": {{
            "contentShareability": {{
                "score": 0,
                "factors": {{
                    "emotional_triggers": true,
                    "practical_value": true,
                    "social_currency": true,
                    "storytelling": true,
                    "controversy_safe": true
                }},
                "improvements": []
            }},
            "invitationMechanics": {{
                "currentInviteRate": 0,
                "ctaEffectiveness": 0,
                "sharePrompts": {{
                    "inCaption": true,
                    "inStories": true,
                    "inBio": true
                }}
            }},
            "networkEffects": {{
                "tagUsage": 0,
                "mentionRate": 0,
                "duetPotential": 0,
                "collaborationFrequency": 0
            }}
        }},
        "viralContentBlueprints": [
            {{
                "type": "trend_riding|controversy|how_to|transformation|challenge|ugc",
                "description": "string",
                "successProbability": "high|medium|low",
                "implementationGuide": "string",
                "expectedReach": "string",
                "timing": "immediate|next_trend|planned"
            }}
        ],
        "referralStrategy": {{
            "currentReferralRate": 0,
            "recommendedIncentives": [],
            "ambassadorProgram": {{
                "feasibility": "high|medium|low",
                "potentialAmbassadors": 0,
                "implementation": "string"
            }}
        }},
        "viralReadinessScore": {{
            "score": 0,
            "formula_used": "Viral_Readiness = (Shareability × 0.35 + Network_Effects × 0.25 + Content_Quality × 0.25 + Timing × 0.15)",
            "components": {{
                "shareability": 0,
                "networkEffects": 0,
                "contentQuality": 0,
                "timing": 0
            }},
            "interpretation": "viral_ready|needs_optimization|not_ready"
        }}
    }},
    "score_breakdown": {{
        "overall_growth_score": 0,
        "formula_used": "Growth_Score = (Current_Rate × 0.25 + Trend × 0.20 + Channel_Diversity × 0.20 + Viral_Potential × 0.20 + Competitive_Position × 0.15)",
        "components": {{
            "current_rate": {{"score": 0, "weight": 0.25, "weighted": 0}},
            "growth_trend": {{"score": 0, "weight": 0.20, "weighted": 0}},
            "channel_diversity": {{"score": 0, "weight": 0.20, "weighted": 0}},
            "viral_potential": {{"score": 0, "weight": 0.20, "weighted": 0}},
            "competitive_position": {{"score": 0, "weight": 0.15, "weighted": 0}}
        }}
    }}
}}"""

    def _get_benchmark_for_followers(self, followers: int) -> Dict[str, Any]:
        """Get appropriate growth benchmark for follower count"""
        if followers < 1000:
            tier = "0-1K"
        elif followers < 5000:
            tier = "1K-5K"
        elif followers < 10000:
            tier = "5K-10K"
        elif followers < 25000:
            tier = "10K-25K"
        elif followers < 50000:
            tier = "25K-50K"
        elif followers < 100000:
            tier = "50K-100K"
        elif followers < 500000:
            tier = "100K-500K"
        else:
            tier = "500K+"
        
        return {
            "tier": tier,
            "benchmarks": self.growth_benchmarks.get(tier, {})
        }
    
    def _detect_growth_pattern(self, rates: List[float]) -> str:
        """Detect growth pattern from historical rates"""
        if not rates or len(rates) < 2:
            return "insufficient_data"
        
        # Check for exponential (each rate > previous)
        if all(rates[i] > rates[i-1] for i in range(1, len(rates))):
            return "exponential"
        
        # Check for declining (each rate < previous)
        if all(rates[i] < rates[i-1] for i in range(1, len(rates))):
            if all(r < 0 for r in rates):
                return "declining"
            return "logarithmic"
        
        # Check for stagnant (low variance)
        if len(rates) >= 3:
            avg_rate = sum(rates) / len(rates)
            variance = sum((r - avg_rate) ** 2 for r in rates) / len(rates)
            if variance < 1 and abs(avg_rate) < 1:
                return "stagnant"
        
        # Check for linear (consistent)
        variance = sum((r - (sum(rates)/len(rates))) ** 2 for r in rates) / len(rates)
        if variance < 2:
            return "linear"
        
        return "s_curve"
    
    def calculate_net_growth_rate(
        self,
        new_followers: int,
        unfollows: int,
        starting_followers: int
    ) -> float:
        """
        Calculate Net Growth Rate
        NGR = ((New_Followers - Unfollows) / Starting_Followers) × 100
        """
        if starting_followers <= 0:
            return 0
        return ((new_followers - unfollows) / starting_followers) * 100
    
    def calculate_gross_growth_rate(
        self,
        new_followers: int,
        starting_followers: int
    ) -> float:
        """
        Calculate Gross Growth Rate
        GGR = (New_Followers / Starting_Followers) × 100
        """
        if starting_followers <= 0:
            return 0
        return (new_followers / starting_followers) * 100
    
    def calculate_churn_rate(
        self,
        unfollows: int,
        starting_followers: int
    ) -> float:
        """
        Calculate Churn Rate
        Churn = (Unfollows / Starting_Followers) × 100
        """
        if starting_followers <= 0:
            return 0
        return (unfollows / starting_followers) * 100
    
    def calculate_growth_velocity(
        self,
        net_new_followers: int,
        time_period_days: int
    ) -> float:
        """
        Calculate Growth Velocity (followers per day)
        Velocity = Net_New_Followers / Time_Period
        """
        if time_period_days <= 0:
            return 0
        return net_new_followers / time_period_days
    
    def calculate_cmgr(
        self,
        ending_followers: int,
        starting_followers: int,
        months: int
    ) -> float:
        """
        Calculate Compound Monthly Growth Rate
        CMGR = ((Ending / Starting)^(1/months) - 1) × 100
        """
        if starting_followers <= 0 or months <= 0:
            return 0
        return ((ending_followers / starting_followers) ** (1 / months) - 1) * 100
    
    def calculate_doubling_time(self, monthly_growth_rate: float) -> float:
        """
        Calculate Follower Doubling Time in months
        Doubling_Time = ln(2) / ln(1 + Monthly_Growth_Rate/100)
        """
        if monthly_growth_rate <= 0:
            return float('inf')
        return math.log(2) / math.log(1 + monthly_growth_rate / 100)
    
    def calculate_time_to_milestone(
        self,
        current: int,
        target: int,
        monthly_rate: float
    ) -> float:
        """
        Calculate Time to reach a follower milestone
        Time = ln(Target / Current) / ln(1 + Monthly_Rate/100)
        """
        if current <= 0 or monthly_rate <= 0 or target <= current:
            return float('inf')
        return math.log(target / current) / math.log(1 + monthly_rate / 100)
    
    def calculate_growth_projections(
        self,
        current_followers: int,
        current_rate: float
    ) -> Dict[str, Any]:
        """Calculate growth projections for different scenarios"""
        def project(rate: float, months: int) -> int:
            return int(current_followers * ((1 + rate / 100) ** months))
        
        return {
            "conservative": {
                "3_month": project(current_rate, 3),
                "6_month": project(current_rate, 6),
                "12_month": project(current_rate, 12)
            },
            "moderate": {
                "3_month": project(current_rate * 1.5, 3),
                "6_month": project(current_rate * 1.5, 6),
                "12_month": project(current_rate * 1.5, 12)
            },
            "aggressive": {
                "3_month": project(current_rate * 2.5, 3),
                "6_month": project(current_rate * 2.5, 6),
                "12_month": project(current_rate * 2.5, 12)
            }
        }
    
    def calculate_channel_effectiveness(
        self,
        reach_contribution: float,
        follower_quality: float,
        conversion_rate: float,
        sustainability: float
    ) -> float:
        """
        Calculate Channel Effectiveness Score
        Effectiveness = (Reach × 0.30) + (Quality × 0.30) + (Conversion × 0.25) + (Sustainability × 0.15)
        """
        return (
            reach_contribution * 0.30 +
            follower_quality * 0.30 +
            conversion_rate * 0.25 +
            sustainability * 0.15
        )
    
    def calculate_competitive_position(
        self,
        your_metrics: Dict[str, float],
        competitor_avgs: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculate Competitive Position Score
        Position = Σ(Your_Metric / Competitor_Avg × Weight)
        """
        weights = {
            "growth_rate": 0.25,
            "engagement_rate": 0.25,
            "content_quality": 0.20,
            "audience_quality": 0.15,
            "posting_consistency": 0.15
        }
        
        position_score = 0
        for metric, weight in weights.items():
            your_value = your_metrics.get(metric, 0)
            comp_avg = competitor_avgs.get(metric, 1)
            if comp_avg > 0:
                position_score += (your_value / comp_avg) * weight
        
        # Determine category
        if position_score > 1.2:
            category = "market_leader"
        elif position_score >= 1.0:
            category = "strong"
        elif position_score >= 0.8:
            category = "average"
        elif position_score >= 0.6:
            category = "below_average"
        else:
            category = "lagging"
        
        return {
            "score": round(position_score, 2),
            "category": category,
            "percentile": min(100, int(position_score * 50))
        }
    
    def calculate_growth_potential(
        self,
        current_momentum: float,
        content_scalability: float,
        audience_expandability: float,
        channel_diversification: float,
        competitive_position: float,
        resource_capacity: float
    ) -> Dict[str, Any]:
        """
        Calculate Growth Potential Score (0-100)
        
        Potential = (Momentum × 0.25) + (Scalability × 0.20) + (Expandability × 0.20) + 
                   (Diversification × 0.15) + (Position × 0.10) + (Resources × 0.10)
        """
        potential_score = (
            current_momentum * 0.25 +
            content_scalability * 0.20 +
            audience_expandability * 0.20 +
            channel_diversification * 0.15 +
            competitive_position * 0.10 +
            resource_capacity * 0.10
        )
        
        return {
            "score": round(potential_score, 1),
            "components": {
                "momentum": round(current_momentum, 1),
                "scalability": round(content_scalability, 1),
                "expandability": round(audience_expandability, 1),
                "diversification": round(channel_diversification, 1),
                "competitive_position": round(competitive_position, 1),
                "resources": round(resource_capacity, 1)
            }
        }
    
    def calculate_viral_potential(
        self,
        historical_viral_rate: float,
        content_shareability: float,
        trend_alignment: float,
        audience_amplification: float,
        format_optimization: float
    ) -> Dict[str, Any]:
        """
        Calculate Viral Potential Score (0-100)
        
        Viral = (Historical × 0.30) + (Shareability × 0.25) + (Trend × 0.20) + 
               (Amplification × 0.15) + (Format × 0.10)
        """
        viral_score = (
            historical_viral_rate * 0.30 +
            content_shareability * 0.25 +
            trend_alignment * 0.20 +
            audience_amplification * 0.15 +
            format_optimization * 0.10
        )
        
        return {
            "score": round(viral_score, 1),
            "components": {
                "historical_rate": round(historical_viral_rate, 1),
                "shareability": round(content_shareability, 1),
                "trend_alignment": round(trend_alignment, 1),
                "amplification": round(audience_amplification, 1),
                "format_optimization": round(format_optimization, 1)
            }
        }
    
    def calculate_strategy_effectiveness(
        self,
        goal_achievement: float,
        efficiency: float,
        consistency: float,
        adaptability: float
    ) -> Dict[str, Any]:
        """
        Calculate Strategy Effectiveness Score (0-100)
        
        Effectiveness = (Goals × 0.35) + (Efficiency × 0.25) + (Consistency × 0.20) + (Adaptability × 0.20)
        """
        effectiveness_score = (
            goal_achievement * 0.35 +
            efficiency * 0.25 +
            consistency * 0.20 +
            adaptability * 0.20
        )
        
        return {
            "score": round(effectiveness_score, 1),
            "components": {
                "goal_achievement": round(goal_achievement, 1),
                "efficiency": round(efficiency, 1),
                "consistency": round(consistency, 1),
                "adaptability": round(adaptability, 1)
            }
        }
    
    def categorize_growth_rate(self, rate: float) -> Dict[str, Any]:
        """Categorize a growth rate"""
        for category, config in self.growth_categories.items():
            if config["rate_min"] <= rate < config["rate_max"]:
                return {
                    "category": category,
                    "assessment": config["assessment"],
                    "sustainability": config["sustainability"]
                }
        return {"category": "unknown", "assessment": "Unable to categorize", "sustainability": "unknown"}
    
    def assess_growth_trend(self, rates: List[float]) -> str:
        """Assess if growth trend is improving, stable, or declining"""
        if len(rates) < 3:
            return "insufficient_data"
        
        recent = rates[-3:]
        if all(recent[i] > recent[i-1] for i in range(1, len(recent))):
            return "improving"
        elif all(recent[i] < recent[i-1] for i in range(1, len(recent))):
            return "declining"
        else:
            variance = sum((r - sum(recent)/len(recent))**2 for r in recent) / len(recent)
            if variance < 1:
                return "stable"
            return "fluctuating"
    
    def generate_milestone_roadmap(
        self,
        current: int,
        monthly_rate: float
    ) -> List[Dict[str, Any]]:
        """Generate milestone roadmap"""
        milestones = [1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
        roadmap = []
        
        for milestone in milestones:
            if milestone > current:
                months = self.calculate_time_to_milestone(current, milestone, monthly_rate)
                if months != float('inf') and months < 60:  # Max 5 years projection
                    probability = max(0, min(100, 100 - (months * 2)))  # Simple probability estimation
                    roadmap.append({
                        "target": milestone,
                        "estimated_months": round(months, 1),
                        "probability": round(probability)
                    })
        
        return roadmap[:5]  # Return top 5 milestones
