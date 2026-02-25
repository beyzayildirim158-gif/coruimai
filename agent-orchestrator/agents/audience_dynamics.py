# Audience Dynamics Agent - Hedef Kitle Analizi Uzmanı
# Version: 2.0
# PhD Seviyesi Takipçi Analizi ve Davranış Modelleme

from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent
import math
import json
from datetime import datetime, timedelta


class AudienceDynamicsAgent(BaseAgent):
    """
    Audience Dynamics Agent v2.0
    Role: Advanced audience psychology, segmentation, quality analysis, and growth dynamics
    
    Kapsamlı Uzmanlık Alanları:
    - Sosyal medya kullanıcı psikolojisi ve motivasyon analizi
    - Takipçi segmentasyon modeli (Advocates, Engagers, Regulars, Lurkers, Ghosts, Bots)
    - Demografik ve psikografik analiz
    - Aktivite ve zamanlama optimizasyonu
    - Bot/Fake takipçi tespiti
    - Büyüme trendi ve churn analizi
    - Audience-Content fit değerlendirmesi
    - Persona oluşturma ve gap analizi
    """
    
    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "Audience Dynamics Analyst"
        self.role = "Audience Psychology & Behavior Analysis Expert"
        self.specialty = "Audience segmentation, fake detection, growth analysis, timing optimization"
        
        # Initialize all configuration data
        self.motivation_matrix = self._init_motivation_matrix()
        self.engagement_pyramid = self._init_engagement_pyramid()
        self.follower_segments = self._init_follower_segments()
        self.timing_multipliers = self._init_timing_multipliers()
        self.niche_timing = self._init_niche_timing()
        self.bot_detection_weights = self._init_bot_detection_weights()
        self.acquisition_channels = self._init_acquisition_channels()
    
    def _init_motivation_matrix(self) -> Dict[str, Any]:
        """Initialize user motivation matrix"""
        return {
            "entertainment": {
                "behavior_pattern": "scroll, passive",
                "content_preference": ["reels", "memes", "short_video"],
                "engagement_type": "like",
                "priority_metric": "watch_time"
            },
            "information": {
                "behavior_pattern": "save, bookmark",
                "content_preference": ["carousel", "tutorial", "how_to"],
                "engagement_type": "save",
                "priority_metric": "save_rate"
            },
            "inspiration": {
                "behavior_pattern": "share, screenshot",
                "content_preference": ["quotes", "transformation", "success_stories"],
                "engagement_type": "share",
                "priority_metric": "share_rate"
            },
            "connection": {
                "behavior_pattern": "comment, dm",
                "content_preference": ["personal", "behind_scenes", "q_and_a"],
                "engagement_type": "comment",
                "priority_metric": "comment_rate"
            },
            "identity": {
                "behavior_pattern": "repost, tag",
                "content_preference": ["lifestyle", "aesthetic", "values"],
                "engagement_type": "share",
                "priority_metric": "repost_rate"
            },
            "escape": {
                "behavior_pattern": "binge_watch",
                "content_preference": ["entertainment", "asmr", "relaxing"],
                "engagement_type": "watch",
                "priority_metric": "session_duration"
            }
        }
    
    def _init_engagement_pyramid(self) -> Dict[str, float]:
        """Initialize engagement pyramid percentages"""
        return {
            "dm_purchase": 0.01,      # 1% - Top of pyramid
            "share": 0.03,             # 3%
            "comment": 0.05,           # 5%
            "save": 0.08,              # 8%
            "like": 0.25,              # 25%
            "view": 1.00               # 100% - Base
        }
    
    def _init_follower_segments(self) -> Dict[str, Any]:
        """Initialize follower segment definitions"""
        return {
            "advocates": {
                "percentage_range": (0.02, 0.05),
                "characteristics": "Every post engagement, DMs, defends brand",
                "value_multiplier": 10,
                "detection_criteria": "80%+ engagement in 30 days",
                "strategy": "VIP treatment, early access, mentions"
            },
            "engagers": {
                "percentage_range": (0.10, 0.15),
                "characteristics": "Regular like/comment, occasional share",
                "value_multiplier": 5,
                "detection_criteria": "40-80% engagement in 30 days",
                "strategy": "Community feeling, questions, polls"
            },
            "regulars": {
                "percentage_range": (0.20, 0.30),
                "characteristics": "Regular viewing, selective engagement",
                "value_multiplier": 2,
                "detection_criteria": "20-40% engagement in 30 days",
                "strategy": "Value content, hook optimization"
            },
            "lurkers": {
                "percentage_range": (0.40, 0.50),
                "characteristics": "Views but no engagement",
                "value_multiplier": 1,
                "detection_criteria": "View exists, engagement none",
                "strategy": "Save-worthy content, soft CTA"
            },
            "ghosts": {
                "percentage_range": (0.10, 0.20),
                "characteristics": "Inactive, no views",
                "value_multiplier": 0,  # Negative algorithm impact
                "detection_criteria": "90+ days inactive",
                "strategy": "Cleanup or reactivation campaign"
            },
            "bots_fake": {
                "percentage_range": (0.05, 0.30),  # Varies by account
                "characteristics": "Fake profile, spam behavior",
                "value_multiplier": -1,  # Negative
                "detection_criteria": "Pattern analysis (see bot detection)",
                "strategy": "Detection and cleanup"
            }
        }
    
    def _init_timing_multipliers(self) -> Dict[str, Dict[str, List[float]]]:
        """Initialize timing multipliers for Turkey timezone (UTC+3)"""
        # Hours: 06-08, 08-10, 10-12, 12-14, 14-16, 16-18, 18-20, 20-22, 22-00, 00-06
        return {
            "monday": [0.6, 0.9, 1.0, 1.3, 0.9, 1.0, 1.4, 1.5, 1.2, 0.4],
            "tuesday": [0.6, 0.9, 1.0, 1.3, 0.9, 1.0, 1.4, 1.5, 1.2, 0.4],
            "wednesday": [0.6, 0.9, 1.0, 1.3, 0.9, 1.0, 1.4, 1.5, 1.2, 0.4],
            "thursday": [0.6, 0.9, 1.0, 1.3, 0.9, 1.0, 1.4, 1.5, 1.2, 0.4],
            "friday": [0.5, 0.8, 1.0, 1.2, 0.9, 1.0, 1.3, 1.4, 1.3, 0.5],
            "saturday": [0.4, 0.6, 0.9, 1.0, 0.8, 0.9, 1.2, 1.5, 1.4, 0.6],
            "sunday": [0.3, 0.5, 0.8, 1.0, 0.9, 1.0, 1.2, 1.4, 1.2, 0.5]
        }
    
    def _init_niche_timing(self) -> Dict[str, Any]:
        """Initialize niche-specific optimal timing"""
        return {
            "b2b_professional": {
                "prime": ["08:00-09:00", "12:00-13:00"],
                "secondary": ["17:00-18:00"],
                "avoid": ["weekends", "night"],
                "notes": "Business hours, lunch breaks"
            },
            "fitness": {
                "prime": ["06:00-07:00", "18:00-20:00"],
                "secondary": ["12:00-13:00"],
                "avoid": ["22:00+"],
                "notes": "Morning workout, evening gym"
            },
            "entertainment_lifestyle": {
                "prime": ["20:00-23:00"],
                "secondary": ["12:00-14:00", "17:00-19:00"],
                "avoid": ["early_morning"],
                "notes": "Relax time viewing"
            },
            "parenting": {
                "prime": ["10:00-11:00", "21:00-22:00"],
                "secondary": ["14:00-15:00"],
                "avoid": ["07:00-09:00", "17:00-19:00"],
                "notes": "When kids sleep/at school"
            },
            "student_genz": {
                "prime": ["21:00-01:00"],
                "secondary": ["12:00-14:00"],
                "avoid": ["06:00-10:00"],
                "notes": "Night owls, lunch breaks"
            },
            "food": {
                "prime": ["11:00-13:00", "17:00-19:00"],
                "secondary": ["08:00-09:00"],
                "avoid": ["late_night"],
                "notes": "Meal planning times"
            },
            "tech": {
                "prime": ["09:00-11:00", "19:00-21:00"],
                "secondary": ["14:00-16:00"],
                "avoid": ["early_morning"],
                "notes": "Work hours and evening learning"
            },
            "fashion_beauty": {
                "prime": ["10:00-12:00", "19:00-21:00"],
                "secondary": ["15:00-17:00"],
                "avoid": ["early_morning"],
                "notes": "Getting ready times"
            }
        }
    
    def _init_bot_detection_weights(self) -> Dict[str, Any]:
        """Initialize bot/fake detection signal weights"""
        return {
            "profile_quality": {
                "weight": 0.25,
                "signals": {
                    "no_profile_photo": 30,
                    "empty_bio": 20,
                    "post_count_0_5": 25,
                    "generic_username": 15,  # user123456 pattern
                    "account_age_under_30_days": 10
                }
            },
            "follower_following_ratio": {
                "weight": 0.20,
                "signals": {
                    "following_follower_ratio_over_10": 40,  # mass follower
                    "following_over_5000": 30,
                    "followers_0_10": 20,
                    "following_follower_ratio_under_0_01": 10  # fake influencer
                }
            },
            "activity_pattern": {
                "weight": 0.25,
                "signals": {
                    "no_posts_90_days": 35,
                    "burst_following_100_plus_day": 30,
                    "no_engagement_activity": 25,
                    "only_generic_comments": 10
                }
            },
            "engagement_quality": {
                "weight": 0.30,
                "signals": {
                    "generic_comment_content": 35,  # "nice!", "👍", "follow me"
                    "comment_timing_under_3_seconds": 30,  # bot
                    "same_comment_multiple_posts": 25,
                    "engagement_only_specific_hours": 10
                }
            }
        }
    
    def _init_acquisition_channels(self) -> Dict[str, Any]:
        """Initialize follower acquisition channel quality metrics"""
        return {
            "organic_search": {
                "quality": "high",
                "retention": 0.80,
                "engagement": "high",
                "ideal_percentage": 0.15
            },
            "hashtag": {
                "quality": "medium",
                "retention": 0.60,
                "engagement": "medium",
                "ideal_percentage": 0.20
            },
            "explore": {
                "quality": "medium",
                "retention": 0.50,
                "engagement": "medium_low",
                "ideal_percentage": 0.15
            },
            "reels": {
                "quality": "variable",
                "retention": 0.40,
                "engagement": "low_medium",
                "ideal_percentage": 0.25
            },
            "shares": {
                "quality": "high",
                "retention": 0.70,
                "engagement": "high",
                "ideal_percentage": 0.10
            },
            "mentions": {
                "quality": "high",
                "retention": 0.75,
                "engagement": "high",
                "ideal_percentage": 0.08
            },
            "suggested_users": {
                "quality": "medium",
                "retention": 0.50,
                "engagement": "medium",
                "ideal_percentage": 0.05
            },
            "ads": {
                "quality": "low",
                "retention": 0.30,
                "engagement": "low",
                "ideal_percentage": 0.02
            },
            "follow4follow": {
                "quality": "very_low",
                "retention": 0.15,
                "engagement": "very_low",
                "ideal_percentage": 0.00  # Avoid
            }
        }
    
    def get_system_prompt(self) -> str:
        return """Sen Audience Dynamics Agent'sın - Hedef Kitle Psikolojisi ve Davranış Analizi Uzmanı.

## TEMEL UZMANLIK ALANLARIN:

### 1. SOSYAL MEDYA KULLANICI PSİKOLOJİSİ

**Motivasyon Matrisi:**
| Motivasyon | Davranış | İçerik Tercihi |
|------------|----------|----------------|
| Eğlence | Scroll, passive | Reels, memes |
| Bilgi | Save, bookmark | Carousel, tutorial |
| İlham | Share, screenshot | Quotes, transformation |
| Bağlantı | Comment, DM | Personal, behind-scenes |
| Kimlik | Repost, tag | Lifestyle, aesthetic |
| Kaçış | Binge watch | Entertainment, ASMR |

**Engagement Piramidi:**
- DM/Purchase: %1 (zirve)
- Share: %3
- Comment: %5
- Save: %8
- Like: %25
- View: %100 (taban)

### 2. TAKİPÇİ SEGMENTASYON MODELİ

| Segment | Oran | Değer Çarpanı | Tespit Kriteri |
|---------|------|---------------|----------------|
| ADVOCATES | %2-5 | ×10 | 30 günde %80+ etkileşim |
| ENGAGERS | %10-15 | ×5 | 30 günde %40-80 etkileşim |
| REGULARS | %20-30 | ×2 | 30 günde %20-40 etkileşim |
| LURKERS | %40-50 | ×1 | View var, engagement yok |
| GHOSTS | %10-20 | ×0 (zararlı) | 90+ gün inaktif |
| BOTS/FAKE | %5-30 | ×(-1) | Pattern analizi |

### 3. ZAMANLAMA OPTİMİZASYONU

**Türkiye (UTC+3) Engagement Multipliers:**
- PRIME TIME (>1.2): 12:00-14:00, 18:00-22:00
- NORMAL (0.8-1.2): 10:00-12:00, 14:00-18:00
- OFF-PEAK (<0.8): 00:00-08:00

**Niche Bazlı Optimal Saatler:**
- B2B: 08:00-09:00, 12:00-13:00 (hafta içi)
- Fitness: 06:00-07:00, 18:00-20:00
- Entertainment: 20:00-23:00
- Parenting: 10:00-11:00, 21:00-22:00
- Student/GenZ: 21:00-01:00

### 4. BOT/FAKE TESPİT SİSTEMİ

**Fake Probability Scoring (0-100):**

Profil Kalitesi (%25):
- Profil fotoğrafı yok: +30
- Bio boş: +20
- Post 0-5: +25
- Generic username: +15
- Hesap yaşı <30 gün: +10

Takipçi/Takip Oranı (%20):
- Following/Follower >10: +40
- Following >5000: +30
- Follower 0-10: +20

Aktivite Paterni (%25):
- 90 gün 0 post: +35
- Burst following 100+/gün: +30
- Engagement yok: +25

Engagement Kalitesi (%30):
- Generic comment: +35
- Comment <3 saniye: +30
- Aynı comment tekrar: +25

**Sonuç Sınıflandırması:**
- 0-20: Gerçek
- 21-40: Muhtemelen gerçek
- 41-60: Şüpheli
- 61-80: Muhtemelen fake
- 81-100: Kesinlikle fake/bot

### 5. ENGAGEMENT AUTHENTICITY

**Red Flags:**
- Generic comment >%50: -25
- Emoji-only >%70: -15
- Comment/Like <0.01: -10 (bot like)
- Comment/Like >0.5: -10 (comment pod)
- İlk 10 like <10 sn: -20 (bot)
- %80 engagement ilk 5 dk: -15 (pod)
- Aynı 10 hesaptan >%30: -25

### 6. FOLLOWER QUALITY SCORE (0-100)

**Formül:**
Quality = (Real_Ratio × 0.35) + (Active_Ratio × 0.30) + (Relevant_Ratio × 0.20) + (Engaged_Ratio × 0.15)

**Hedefler:**
- Real Ratio: >%85
- Active Ratio: >%40
- Relevant Ratio: >%60
- Engaged Ratio: >%15

**Quality Grade:**
- 90-100: A (Exceptional)
- 75-89: B (Good)
- 60-74: C (Average)
- 45-59: D (Below Average)
- 0-44: F (Poor)

### 7. BÜYÜME TRENDİ ANALİZİ

**Growth Pattern Sınıfları:**
- EXPONENTIAL: Her ay >%20 artış (sürdürülemez)
- LINEAR: Sabit aylık artış ±%5 (ideal)
- LOGARITHMIC: Azalan büyüme hızı (platoya yaklaşma)
- STAGNANT: ±%2 değişim (müdahale gerekli)
- DECLINING: Negatif büyüme (acil müdahale)

**Trend Sınıflandırması:**
- >%10/ay: Rapidly Growing
- %5-10/ay: Growing
- %2-5/ay: Slowly Growing
- ±%2/ay: Stable
- -%2 ile -%5/ay: Slowly Declining
- <-%5/ay: Rapidly Declining

### 8. CHURN ANALİZİ

**Unfollow Nedenleri:**
- İçerik uyumsuzluğu: %35
- Engagement eksikliği: %25
- Aşırı promosyon: %20
- Algoritma görünmezliği: %15
- Dış faktörler: %5

**Churn Warning Signals:**
- Story view düşüşü: Early warning
- Comment azalması: Medium warning
- Save rate düşüşü: Strong warning
- Profile visit düşüşü: Critical warning

### 9. ACQUISITION SOURCE KALİTESİ

| Kaynak | Kalite | Retention | Engagement |
|--------|--------|-----------|------------|
| Organic Search | Yüksek | %80+ | Yüksek |
| Hashtag | Orta | %50-70 | Orta |
| Explore | Orta | %40-60 | Orta-Düşük |
| Reels | Değişken | %30-50 | Düşük-Orta |
| Shares | Yüksek | %70+ | Yüksek |
| Mentions | Yüksek | %75+ | Yüksek |
| Ads | Düşük | %20-40 | Düşük |
| Follow4Follow | Çok Düşük | %10-20 | Çok Düşük |

**İdeal Dağılım:**
- Organic >%50
- Content (Reels+Shares) %25-35
- Social (Mentions+Suggested) %15-25
- Paid <%10

### 10. AUDIENCE-CONTENT FIT

**Alignment Score Formülü:**
Alignment = (Demographic_Fit × 0.25) + (Interest_Fit × 0.30) + (Behavior_Fit × 0.25) + (Expectation_Fit × 0.20)

**Gap Severity:**
- Critical (>%30): Acil düzeltme
- Significant (%15-30): Kısa vadede
- Minor (%5-15): Orta vadede
- Aligned (<%5): Devam

### 11. EDGE CASES

1. **Yeni Hesap (<1000):** Segment analizi güvenilir değil
2. **Viral Spike:** 30 gün bekle, retention tracking
3. **Niche Değişikliği:** 90 gün geçiş süresi
4. **Global Audience:** Distributed timing
5. **B2B:** Quality > Quantity
6. **Celebrity:** Farklı benchmark

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
        
        # Demographics data
        demographics = account_data.get('demographics', {})
        age_distribution = demographics.get('ageDistribution', {})
        gender_distribution = demographics.get('genderDistribution', {})
        top_locations = demographics.get('topLocations', [])
        top_countries = demographics.get('topCountries', [])
        
        # Activity data
        activity_data = account_data.get('activityData', {})
        peak_hours = activity_data.get('peakHours', [])
        peak_days = activity_data.get('peakDays', [])
        timezone_distribution = activity_data.get('timezoneDistribution', {})
        
        # Growth data
        growth_data = account_data.get('growthData', {})
        monthly_growth_rate = growth_data.get('monthlyGrowthRate', 0)
        weekly_new_followers = growth_data.get('weeklyNewFollowers', 0)
        weekly_lost_followers = growth_data.get('weeklyLostFollowers', 0)
        
        # Engagement data
        engagement_data = account_data.get('engagementData', {})
        comment_samples = engagement_data.get('commentSamples', [])
        top_engagers = engagement_data.get('topEngagers', [])
        
        # Calculate basic metrics
        comment_rate = (avg_comments / followers * 100) if followers > 0 else 0
        save_rate = (avg_saves / followers * 100) if followers > 0 else 0
        share_rate = (avg_shares / followers * 100) if followers > 0 else 0
        follower_following_ratio = followers / max(following, 1)
        
        return f"""Bu Instagram hesabı için kapsamlı Audience Dynamics analizi yap:

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
- Comment Rate: {comment_rate:.3f}%
- Save Rate: {save_rate:.3f}%
- Share Rate: {share_rate:.3f}%
- Follower/Following Ratio: {follower_following_ratio:.2f}
- Niche: {niche}
- Bio: {bio}

## DEMOGRAFİK VERİLER:
- Yaş Dağılımı: {json.dumps(age_distribution, indent=2) if age_distribution else 'Veri yok'}
- Cinsiyet Dağılımı: {json.dumps(gender_distribution, indent=2) if gender_distribution else 'Veri yok'}
- Top Lokasyonlar: {json.dumps(top_locations, indent=2) if top_locations else 'Veri yok'}
- Top Ülkeler: {json.dumps(top_countries, indent=2) if top_countries else 'Veri yok'}

## AKTİVİTE VERİLERİ:
- Peak Saatler: {peak_hours if peak_hours else 'Veri yok'}
- Peak Günler: {peak_days if peak_days else 'Veri yok'}
- Timezone Dağılımı: {json.dumps(timezone_distribution, indent=2) if timezone_distribution else 'Veri yok'}

## BÜYÜME VERİLERİ:
- Aylık Büyüme Oranı: %{monthly_growth_rate:.2f}
- Haftalık Yeni Takipçi: {weekly_new_followers}
- Haftalık Kaybedilen: {weekly_lost_followers}
- Net Haftalık Büyüme: {weekly_new_followers - weekly_lost_followers}

## ANALİZ GÖREVLERİ:

1. **Takipçi Segmentasyonu:**
   - Advocates, Engagers, Regulars, Lurkers, Ghosts, Bots oranlarını tahmin et
   - Her segment için strateji öner

2. **Demografik Analiz:**
   - 4 katman analizi (Temel, Psikografik, Davranışsal, Ekonomik)
   - Demografik denge değerlendirmesi

3. **Timing Analizi:**
   - {niche} niche'i için optimal posting saatleri
   - Timezone bazlı strateji
   - Peak hours belirleme

4. **Takipçi Kalitesi:**
   - Fake/Bot oranı tahmini
   - Engagement authenticity değerlendirmesi
   - Quality Score hesaplama (0-100)
   - Quality Grade belirleme (A-F)

5. **Büyüme Trendi:**
   - Growth pattern sınıflandırması (Exponential/Linear/Logarithmic/Stagnant/Declining)
   - Trend değerlendirmesi (growing/stable/declining)
   - Churn risk analizi

6. **Acquisition Source Analizi:**
   - Tahmini kaynak dağılımı
   - Kaynak kalitesi değerlendirmesi

7. **Audience-Content Fit:**
   - Alignment Score hesaplama
   - Gap analizi
   - Persona önerileri

8. **Edge Case Kontrolü:**
   - Yeni hesap mı? (<1000 takipçi)
   - Viral spike var mı?
   - Niche değişikliği var mı?
   - Global audience mı?
   - B2B hesap mı?

9. **Data Confidence:**
   - Veri güvenilirlik seviyesi (high/medium/low)
   - Limitasyonlar

Aşağıdaki JSON yapısında yanıt ver:

{{
    "agent": "audience_dynamics",
    "analysis_timestamp": "{datetime.now().isoformat()}",
    "audience_profile": {{
        "total_followers": {followers},
        "estimated_real_followers": 0,
        "fake_ratio": 0.0,
        "active_ratio": 0.0,
        "primary_segment": "engagers|regulars|lurkers",
        "segment_distribution": {{
            "advocates": 0.0,
            "engagers": 0.0,
            "regulars": 0.0,
            "lurkers": 0.0,
            "ghosts": 0.0,
            "bots_fake": 0.0
        }},
        "segment_strategies": {{
            "advocates": "VIP treatment recommendation",
            "engagers": "Community building recommendation",
            "regulars": "Hook optimization recommendation",
            "lurkers": "Save-worthy content recommendation",
            "ghosts": "Cleanup or reactivation recommendation"
        }}
    }},
    "followerSegmentation": {{
        "advocates": {{
            "count": 0,
            "percentage": 0.0,
            "benchmark_range": "2-5%",
            "value_multiplier": 10,
            "characteristics": "Every post engagement, DMs, defends brand",
            "detection_criteria": "80%+ engagement in 30 days",
            "strategy": "VIP treatment, early access, mentions"
        }},
        "engagers": {{
            "count": 0,
            "percentage": 0.0,
            "benchmark_range": "10-15%",
            "value_multiplier": 5,
            "characteristics": "Regular like/comment, occasional share",
            "detection_criteria": "40-80% engagement in 30 days",
            "strategy": "Community feeling, questions, polls"
        }},
        "lurkers": {{
            "count": 0,
            "percentage": 0.0,
            "benchmark_range": "40-50%",
            "value_multiplier": 1,
            "characteristics": "Views but no engagement",
            "detection_criteria": "View exists, engagement none",
            "strategy": "Save-worthy content, soft CTA"
        }},
        "ghosts": {{
            "count": 0,
            "percentage": 0.0,
            "benchmark_range": "10-20%",
            "value_multiplier": 0,
            "characteristics": "Inactive, no views",
            "detection_criteria": "90+ days inactive",
            "strategy": "Cleanup or reactivation campaign"
        }},
        "bots": {{
            "count": 0,
            "percentage": 0.0,
            "benchmark_range": "5-30% varies",
            "value_multiplier": -1,
            "characteristics": "Fake profile, spam behavior",
            "detection_criteria": "Pattern analysis",
            "strategy": "Detection and cleanup"
        }},
        "segment_health": "healthy|needs_attention|critical",
        "primary_action": "string recommendation"
    }},
    "botDetectionScore": {{
        "overall_score": 0,
        "formula_used": "Fake_Prob = (Profile×0.25) + (Ratio×0.20) + (Activity×0.25) + (Engagement×0.30)",
        "classification": "real|likely_real|suspicious|likely_fake|fake",
        "components": {{
            "profile_quality_score": {{
                "score": 0,
                "weight": 0.25,
                "flags": ["no_profile_photo", "empty_bio", "post_count_0_5", "generic_username", "account_age_under_30_days"]
            }},
            "follower_following_ratio_score": {{
                "score": 0,
                "weight": 0.20,
                "flags": ["following_follower_ratio_over_10", "following_over_5000", "followers_0_10"]
            }},
            "activity_pattern_score": {{
                "score": 0,
                "weight": 0.25,
                "flags": ["no_posts_90_days", "burst_following_100_plus_day", "no_engagement_activity"]
            }},
            "engagement_quality_score": {{
                "score": 0,
                "weight": 0.30,
                "flags": ["generic_comment_content", "comment_timing_under_3_seconds", "same_comment_multiple_posts"]
            }}
        }},
        "estimated_fake_followers": 0,
        "estimated_fake_percentage": 0.0,
        "cleanup_recommendation": "string",
        "risk_level": "low|medium|high"
    }},
    "demographics": {{
        "age_distribution": {{
            "13-17": 0.0,
            "18-24": 0.0,
            "25-34": 0.0,
            "35-44": 0.0,
            "45-54": 0.0,
            "55+": 0.0
        }},
        "gender_distribution": {{
            "female": 0.0,
            "male": 0.0,
            "other": 0.0
        }},
        "top_locations": [
            {{"city": "string", "percentage": 0.0}}
        ],
        "top_countries": [
            {{"country": "string", "percentage": 0.0}}
        ],
        "primary_language": "Türkçe",
        "psychographic_profile": {{
            "interests": [],
            "lifestyle_indicators": [],
            "values": []
        }},
        "economic_indicators": {{
            "estimated_income_level": "low|medium|high",
            "purchase_behavior": "string"
        }}
    }},
    "metrics": {{
        "audienceAlignmentScore": 0,
        "audienceQuality": 0,
        "demographicFit": 0,
        "engagementPotential": 0,
        "demographicBalance": "low|medium|high",
        "engagementTiming": "peak hours: HH:MM-HH:MM",
        "followerGrowthTrend": "declining|stable|growing",
        "audienceQualityScore": 0,
        "audienceQualityGrade": "A|B|C|D|F",
        "fakeFollowerRatio": 0,
        "segmentHealthScore": 0,
        "timingOptimizationScore": 0,
        "churnRiskScore": 0,
        "growthPotentialScore": 0,
        "advocatePercentage": 0,
        "ghostPercentage": 0,
        "engagementRate": 0,
        "overallScore": 0
    }},
    "detailed_analysis": {{
        "timing_analysis": {{
            "best_day": "string",
            "best_time": "HH:MM-HH:MM",
            "worst_day": "string",
            "worst_time": "HH:MM-HH:MM",
            "timezone_concentration": "UTC+X (X%)",
            "niche_adjusted_times": {{
                "prime": ["HH:MM-HH:MM"],
                "secondary": ["HH:MM-HH:MM"],
                "avoid": ["description"]
            }},
            "global_audience_strategy": "single_timezone|dual_timezone|distributed"
        }},
        "growth_metrics": {{
            "monthly_growth_rate": 0.0,
            "weekly_average_new": 0,
            "weekly_average_lost": 0,
            "net_weekly_growth": 0,
            "growth_trajectory": "exponential|linear|logarithmic|stagnant|declining",
            "growth_sustainability": "high|medium|low",
            "growth_rate_category": "rapidly_growing|growing|slowly_growing|stable|slowly_declining|rapidly_declining"
        }},
        "quality_indicators": {{
            "authenticity_score": 0,
            "bot_risk_level": "low|medium|high",
            "engagement_authenticity": 0,
            "follower_quality_grade": "A|B|C|D|F",
            "fake_detection_details": {{
                "profile_quality_score": 0,
                "ratio_score": 0,
                "activity_pattern_score": 0,
                "engagement_quality_score": 0,
                "total_fake_probability": 0,
                "classification": "real|likely_real|suspicious|likely_fake|fake"
            }},
            "engagement_authenticity_details": {{
                "generic_comment_ratio": 0.0,
                "comment_timing_flags": [],
                "source_concentration_flags": [],
                "authenticity_red_flags": []
            }}
        }},
        "churn_analysis": {{
            "churn_risk_level": "low|medium|high",
            "warning_signals": [],
            "primary_churn_risk_factors": [],
            "retention_recommendations": []
        }},
        "acquisition_analysis": {{
            "estimated_sources": {{
                "organic_search": 0.0,
                "hashtag": 0.0,
                "explore": 0.0,
                "reels": 0.0,
                "shares": 0.0,
                "mentions": 0.0,
                "suggested": 0.0,
                "ads": 0.0
            }},
            "source_quality_assessment": "good|needs_improvement|poor",
            "organic_ratio": 0.0,
            "recommendations": []
        }}
    }},
    "audience_content_fit": {{
        "alignment_score": 0,
        "demographic_fit": 0,
        "interest_fit": 0,
        "behavior_fit": 0,
        "expectation_fit": 0,
        "gap_analysis": [
            {{
                "dimension": "format|tone|length|topic|frequency|timing",
                "audience_wants": "string",
                "content_provides": "string",
                "gap_severity": "critical|significant|minor|aligned",
                "recommendation": "string"
            }}
        ]
    }},
    "personas": [
        {{
            "persona_id": 1,
            "name": "Descriptive Name (e.g., 'Career-Focused Millennial')",
            "percentage_of_audience": 0,
            "size_estimate": 0,
            "demographic": {{
                "age_range": "string",
                "primary_age": 0,
                "gender": "string",
                "location": "string",
                "education": "string",
                "occupation": "string",
                "income_level": "low|medium|high"
            }},
            "psychographic": {{
                "values": ["achievement", "growth", "balance"],
                "interests": ["career development", "productivity", "wellness"],
                "lifestyle": "string description",
                "personality_traits": ["ambitious", "organized", "curious"],
                "motivations": ["career growth", "personal development"],
                "fears_challenges": ["falling behind", "burnout"]
            }},
            "behavioral": {{
                "active_hours": "HH:MM-HH:MM",
                "active_days": ["weekdays"],
                "preferred_content_types": ["carousel", "tips", "case_studies"],
                "engagement_style": "saves_and_comments|likes_only|passive_viewer",
                "purchase_likelihood": "high|medium|low",
                "brand_loyalty": "high|medium|low",
                "device_preference": "mobile|desktop|both"
            }},
            "content_preferences": {{
                "likes": ["educational carousels", "quick tips", "success stories"],
                "dislikes": ["overly promotional", "low quality", "irrelevant"],
                "ideal_post_length": "short|medium|long",
                "ideal_video_length": "15-30s|30-60s|60s+",
                "cta_response": "high|medium|low"
            }},
            "pain_points": [
                "specific pain point 1",
                "specific pain point 2"
            ],
            "goals": [
                "specific goal 1",
                "specific goal 2"
            ],
            "content_hooks_that_work": [
                "How to...",
                "X mistakes to avoid",
                "My journey from..."
            ],
            "monetization_potential": {{
                "willingness_to_pay": "high|medium|low",
                "preferred_products": ["courses", "ebooks", "coaching"],
                "price_sensitivity": "low|medium|high",
                "estimated_ltv": "low|medium|high"
            }}
        }}
    ],
    "personaInsights": {{
        "total_personas_identified": 0,
        "dominant_persona": "string name",
        "dominant_persona_percentage": 0,
        "persona_diversity": "high|medium|low",
        "content_strategy_by_persona": [
            {{
                "persona": "string name",
                "content_focus": "string",
                "posting_time": "HH:MM",
                "cta_type": "string"
            }}
        ],
        "underserved_segments": ["string"],
        "growth_opportunities": ["string"]
    }},
    "edge_cases": {{
        "is_new_account": {str(followers < 1000).lower()},
        "has_viral_spike": false,
        "niche_change_detected": false,
        "is_global_audience": false,
        "is_b2b_account": false,
        "is_celebrity_account": false,
        "special_handling_notes": []
    }},
    "data_confidence": {{
        "level": "high|medium|low",
        "limitations": [],
        "recommendation_confidence": 0.0
    }},
    "findings": [
        {{
            "type": "strength|weakness|opportunity|threat",
            "category": "demographics|quality|timing|growth|engagement|acquisition",
            "finding": "TÜRKÇE - örn: Takipçi kalitesi düşük, tahmini %25 bot/sahte hesap oranı tespit edildi ve bu etkileşim metriklerini olumsuz etkiliyor",
            "evidence": "TÜRKÇE - örn: 311K takipçiden sadece 12K'sı son 30 günde herhangi bir etkileşim gösterdi. Takipçilerin %18'i profil fotoğrafsız hesaplar",
            "impact_score": 82
        }},
        {{
            "type": "opportunity",
            "category": "demographics",
            "finding": "TÜRKÇE - örn: Hedef kitle 25-34 yaş kadın ağırlıklı ancak içerikler 18-24 yaş grubuna hitap ediyor, uyumsuzluk var",
            "evidence": "TÜRKÇE - örn: Demografik veriler %62 kadın ve %45 25-34 yaş gösteriyor, ancak içerik tonu ve referanslar genç kitleye yönelik",
            "impact_score": 70
        }}
    ],
    "recommendations": [
        {{
            "priority": 1,
            "category": "TÜRKÇE - örn: Takipçi Kalitesi İyileştirme",
            "action": "TÜRKÇE - örn: Sahte/inaktif takipçi temizliği için 3 aylık plan başlatın - ayda 5K sahte hesap temizleyin ve organik büyümeye odaklanın",
            "expected_impact": "TÜRKÇE - örn: Etkileşim oranında %40-60 artış, algoritma skorunda iyileşme, marka işbirlikleri için daha çekici metrikler",
            "implementation": "TÜRKÇE - örn: 1) Bot tespit aracı kullanın 2) 30+ gün inaktif takipçileri listeleyin 3) Toplu engelleme yapın 4) Kaliteli içerikle organik büyüme sağlayın",
            "timeframe": "immediate|short-term|long-term"
        }}
    ]
}}"""

    def calculate_fake_probability(
        self,
        profile_data: Dict[str, bool],
        ratio_data: Dict[str, float],
        activity_data: Dict[str, bool],
        engagement_data: Dict[str, bool]
    ) -> Dict[str, Any]:
        """
        Calculate fake/bot probability score (0-100)
        
        Formula: Fake_Probability = Σ(signal_weight × signal_score) / 100
        """
        weights = self.bot_detection_weights
        
        # Profile Quality Score (25%)
        profile_score = 0
        if profile_data.get('no_profile_photo'):
            profile_score += 30
        if profile_data.get('empty_bio'):
            profile_score += 20
        if profile_data.get('post_count_0_5'):
            profile_score += 25
        if profile_data.get('generic_username'):
            profile_score += 15
        if profile_data.get('account_age_under_30_days'):
            profile_score += 10
        
        # Follower/Following Ratio Score (20%)
        ratio_score = 0
        if ratio_data.get('following_follower_ratio', 0) > 10:
            ratio_score += 40
        if ratio_data.get('following', 0) > 5000:
            ratio_score += 30
        if ratio_data.get('followers', 0) <= 10:
            ratio_score += 20
        if ratio_data.get('following_follower_ratio', 1) < 0.01:
            ratio_score += 10
        
        # Activity Pattern Score (25%)
        activity_score = 0
        if activity_data.get('no_posts_90_days'):
            activity_score += 35
        if activity_data.get('burst_following'):
            activity_score += 30
        if activity_data.get('no_engagement_activity'):
            activity_score += 25
        if activity_data.get('only_generic_comments'):
            activity_score += 10
        
        # Engagement Quality Score (30%)
        engagement_score = 0
        if engagement_data.get('generic_comment_content'):
            engagement_score += 35
        if engagement_data.get('comment_timing_under_3_seconds'):
            engagement_score += 30
        if engagement_data.get('same_comment_multiple_posts'):
            engagement_score += 25
        if engagement_data.get('engagement_only_specific_hours'):
            engagement_score += 10
        
        # Weighted total
        total_score = (
            profile_score * 0.25 +
            ratio_score * 0.20 +
            activity_score * 0.25 +
            engagement_score * 0.30
        )
        
        # Classification
        if total_score <= 20:
            classification = "real"
        elif total_score <= 40:
            classification = "likely_real"
        elif total_score <= 60:
            classification = "suspicious"
        elif total_score <= 80:
            classification = "likely_fake"
        else:
            classification = "fake"
        
        return {
            "profile_quality_score": profile_score,
            "ratio_score": ratio_score,
            "activity_pattern_score": activity_score,
            "engagement_quality_score": engagement_score,
            "total_fake_probability": round(total_score, 1),
            "classification": classification
        }
    
    def calculate_engagement_authenticity(
        self,
        comment_data: Dict[str, float],
        timing_data: Dict[str, bool],
        source_data: Dict[str, float],
        growth_data: Dict[str, bool]
    ) -> Dict[str, Any]:
        """
        Calculate engagement authenticity score (0-100)
        
        Formula: Authenticity_Score = 100 - Σ(red_flags)
        """
        red_flags = []
        penalty = 0
        
        # Comment Analysis
        if comment_data.get('generic_ratio', 0) > 0.5:
            penalty += 25
            red_flags.append("generic_comments_over_50_percent")
        if comment_data.get('emoji_only_ratio', 0) > 0.7:
            penalty += 15
            red_flags.append("emoji_only_comments_over_70_percent")
        if comment_data.get('avg_comment_words', 10) < 3:
            penalty += 10
            red_flags.append("avg_comment_under_3_words")
        
        comment_like_ratio = comment_data.get('comment_like_ratio', 0.05)
        if comment_like_ratio < 0.01:
            penalty += 10
            red_flags.append("comment_like_ratio_too_low_bot_likes")
        if comment_like_ratio > 0.5:
            penalty += 10
            red_flags.append("comment_like_ratio_too_high_comment_pod")
        
        # Timing Analysis
        if timing_data.get('first_10_likes_under_10_seconds'):
            penalty += 20
            red_flags.append("bot_like_pattern")
        if timing_data.get('80_percent_engagement_first_5_min'):
            penalty += 15
            red_flags.append("engagement_pod_pattern")
        if timing_data.get('night_engagement_spike'):
            penalty += 15
            red_flags.append("suspicious_night_engagement")
        if timing_data.get('too_regular_pattern'):
            penalty += 10
            red_flags.append("too_regular_engagement_pattern")
        
        # Source Analysis
        if source_data.get('top_10_accounts_ratio', 0) > 0.3:
            penalty += 25
            red_flags.append("engagement_concentrated_in_few_accounts")
        if source_data.get('fake_engagers_ratio', 0) > 0.5:
            penalty += 30
            red_flags.append("majority_engagers_are_fake")
        if source_data.get('niche_mismatch_ratio', 0) > 0.5:
            penalty += 10
            red_flags.append("engagers_not_in_niche")
        if source_data.get('location_mismatch'):
            penalty += 15
            red_flags.append("engagement_from_mismatched_locations")
        
        # Growth Correlation
        if growth_data.get('growth_engagement_mismatch'):
            penalty += 20
            red_flags.append("follower_growth_engagement_mismatch")
        if growth_data.get('spike_without_viral'):
            penalty += 25
            red_flags.append("follower_spike_without_viral_content")
        if growth_data.get('er_not_declining_with_growth'):
            penalty += 15
            red_flags.append("er_should_decline_with_follower_growth")
        
        authenticity_score = max(0, 100 - penalty)
        
        return {
            "authenticity_score": authenticity_score,
            "penalty_total": penalty,
            "red_flags": red_flags,
            "risk_level": "low" if authenticity_score >= 70 else "medium" if authenticity_score >= 50 else "high"
        }
    
    def calculate_follower_quality_score(
        self,
        real_ratio: float,
        active_ratio: float,
        relevant_ratio: float,
        engaged_ratio: float
    ) -> Dict[str, Any]:
        """
        Calculate Follower Quality Score (0-100)
        
        Formula: Quality = (Real × 0.35) + (Active × 0.30) + (Relevant × 0.20) + (Engaged × 0.15)
        """
        # Normalize ratios to 0-100 scale based on benchmarks
        real_score = min(100, (real_ratio / 0.85) * 100)  # Target >85%
        active_score = min(100, (active_ratio / 0.40) * 100)  # Target >40%
        relevant_score = min(100, (relevant_ratio / 0.60) * 100)  # Target >60%
        engaged_score = min(100, (engaged_ratio / 0.15) * 100)  # Target >15%
        
        quality_score = (
            real_score * 0.35 +
            active_score * 0.30 +
            relevant_score * 0.20 +
            engaged_score * 0.15
        )
        
        # Grade assignment
        if quality_score >= 90:
            grade = "A"
        elif quality_score >= 75:
            grade = "B"
        elif quality_score >= 60:
            grade = "C"
        elif quality_score >= 45:
            grade = "D"
        else:
            grade = "F"
        
        return {
            "score": round(quality_score, 1),
            "grade": grade,
            "components": {
                "real_score": round(real_score, 1),
                "active_score": round(active_score, 1),
                "relevant_score": round(relevant_score, 1),
                "engaged_score": round(engaged_score, 1)
            },
            "benchmarks": {
                "real_ratio": {"actual": real_ratio, "target": 0.85, "met": real_ratio >= 0.85},
                "active_ratio": {"actual": active_ratio, "target": 0.40, "met": active_ratio >= 0.40},
                "relevant_ratio": {"actual": relevant_ratio, "target": 0.60, "met": relevant_ratio >= 0.60},
                "engaged_ratio": {"actual": engaged_ratio, "target": 0.15, "met": engaged_ratio >= 0.15}
            }
        }
    
    def classify_growth_trend(
        self,
        monthly_rates: List[float]
    ) -> Dict[str, Any]:
        """
        Classify growth trajectory and trend
        """
        if not monthly_rates or len(monthly_rates) < 2:
            return {
                "trajectory": "unknown",
                "trend": "stable",
                "avg_rate": 0,
                "sustainability": "unknown"
            }
        
        avg_rate = sum(monthly_rates) / len(monthly_rates)
        recent_rate = monthly_rates[-1] if monthly_rates else 0
        
        # Trajectory classification
        if len(monthly_rates) >= 3:
            # Check for exponential (accelerating)
            accelerating = all(monthly_rates[i] > monthly_rates[i-1] * 1.15 
                             for i in range(1, len(monthly_rates)))
            # Check for logarithmic (decelerating)
            decelerating = all(monthly_rates[i] < monthly_rates[i-1] * 0.85 
                             for i in range(1, len(monthly_rates)))
            # Check for stagnant
            stagnant = all(abs(r) < 2 for r in monthly_rates)
            # Check for declining
            declining = all(r < 0 for r in monthly_rates)
            
            if accelerating and avg_rate > 20:
                trajectory = "exponential"
                sustainability = "low"
            elif decelerating and avg_rate > 0:
                trajectory = "logarithmic"
                sustainability = "medium"
            elif stagnant:
                trajectory = "stagnant"
                sustainability = "medium"
            elif declining:
                trajectory = "declining"
                sustainability = "critical"
            else:
                trajectory = "linear"
                sustainability = "high"
        else:
            trajectory = "linear"
            sustainability = "medium"
        
        # Trend classification
        if avg_rate > 10:
            trend = "rapidly_growing"
            trend_simple = "growing"
        elif avg_rate > 5:
            trend = "growing"
            trend_simple = "growing"
        elif avg_rate > 2:
            trend = "slowly_growing"
            trend_simple = "growing"
        elif avg_rate >= -2:
            trend = "stable"
            trend_simple = "stable"
        elif avg_rate >= -5:
            trend = "slowly_declining"
            trend_simple = "declining"
        else:
            trend = "rapidly_declining"
            trend_simple = "declining"
        
        return {
            "trajectory": trajectory,
            "trend": trend_simple,
            "trend_detailed": trend,
            "avg_monthly_rate": round(avg_rate, 2),
            "recent_rate": round(recent_rate, 2),
            "sustainability": sustainability
        }
    
    def calculate_audience_alignment(
        self,
        demographic_fit: float,
        interest_fit: float,
        behavior_fit: float,
        expectation_fit: float
    ) -> Dict[str, Any]:
        """
        Calculate Audience Alignment Score (0-100)
        
        Formula: Alignment = (Demo × 0.25) + (Interest × 0.30) + (Behavior × 0.25) + (Expectation × 0.20)
        """
        alignment_score = (
            demographic_fit * 0.25 +
            interest_fit * 0.30 +
            behavior_fit * 0.25 +
            expectation_fit * 0.20
        )
        
        return {
            "alignment_score": round(alignment_score, 1),
            "components": {
                "demographic_fit": round(demographic_fit, 1),
                "interest_fit": round(interest_fit, 1),
                "behavior_fit": round(behavior_fit, 1),
                "expectation_fit": round(expectation_fit, 1)
            },
            "alignment_level": "high" if alignment_score >= 75 else "medium" if alignment_score >= 50 else "low"
        }
    
    def assess_demographic_balance(
        self,
        target_demo: Dict[str, float],
        actual_demo: Dict[str, float]
    ) -> str:
        """
        Assess demographic balance (high/medium/low)
        """
        if not target_demo or not actual_demo:
            return "medium"
        
        # Calculate overlap
        total_match = 0
        total_weight = 0
        
        for key, target_value in target_demo.items():
            actual_value = actual_demo.get(key, 0)
            match = 1 - abs(target_value - actual_value)
            total_match += match * target_value
            total_weight += target_value
        
        match_ratio = total_match / max(total_weight, 0.01)
        
        # Check concentration
        max_segment = max(actual_demo.values()) if actual_demo else 0
        
        if match_ratio >= 0.6 and max_segment < 0.4:
            return "high"
        elif match_ratio >= 0.4 or max_segment < 0.6:
            return "medium"
        else:
            return "low"
    
    def determine_peak_hours(
        self,
        hourly_engagement: Dict[str, float],
        niche: str
    ) -> str:
        """
        Determine peak engagement hours
        """
        if not hourly_engagement:
            # Use niche defaults
            niche_key = niche.lower().replace(' ', '_').replace('/', '_')
            niche_timing = self.niche_timing.get(niche_key, self.niche_timing.get('entertainment_lifestyle', {}))
            prime = niche_timing.get('prime', ['19:00-22:00'])
            return f"peak hours: {', '.join(prime)}"
        
        # Find top hours
        sorted_hours = sorted(hourly_engagement.items(), key=lambda x: x[1], reverse=True)
        top_hours = sorted_hours[:4]  # Top 4 hours
        
        # Group consecutive hours
        hours = sorted([int(h.split(':')[0]) for h, _ in top_hours])
        
        if not hours:
            return "peak hours: 19:00-22:00"
        
        # Find ranges
        ranges = []
        start = hours[0]
        end = hours[0]
        
        for h in hours[1:]:
            if h == end + 1:
                end = h
            else:
                ranges.append(f"{start:02d}:00-{end+1:02d}:00")
                start = h
                end = h
        ranges.append(f"{start:02d}:00-{end+1:02d}:00")
        
        return f"peak hours: {', '.join(ranges)}"
    
    def segment_followers(
        self,
        engagement_data: Dict[str, Any],
        followers: int
    ) -> Dict[str, float]:
        """
        Estimate follower segment distribution
        """
        # Base distribution
        segments = {
            "advocates": 0.03,
            "engagers": 0.12,
            "regulars": 0.25,
            "lurkers": 0.45,
            "ghosts": 0.10,
            "bots_fake": 0.05
        }
        
        engagement_rate = engagement_data.get('engagement_rate', 3.0)
        comment_rate = engagement_data.get('comment_rate', 0.5)
        save_rate = engagement_data.get('save_rate', 1.0)
        
        # Adjust based on engagement metrics
        if engagement_rate > 6:
            # High engagement - more advocates and engagers
            segments["advocates"] = 0.05
            segments["engagers"] = 0.15
            segments["lurkers"] = 0.40
            segments["ghosts"] = 0.08
        elif engagement_rate < 2:
            # Low engagement - more lurkers and ghosts
            segments["advocates"] = 0.02
            segments["engagers"] = 0.08
            segments["lurkers"] = 0.50
            segments["ghosts"] = 0.15
            segments["bots_fake"] = 0.10
        
        # Adjust for comment rate (indicates community strength)
        if comment_rate > 1:
            segments["advocates"] += 0.01
            segments["engagers"] += 0.02
        
        # Normalize to ensure sum = 1
        total = sum(segments.values())
        segments = {k: round(v/total, 3) for k, v in segments.items()}
        
        return segments
    
    def assess_churn_risk(
        self,
        engagement_trend: str,
        content_consistency: float,
        response_rate: float,
        promotional_ratio: float
    ) -> Dict[str, Any]:
        """
        Assess churn risk level and factors
        """
        risk_score = 0
        risk_factors = []
        warnings = []
        
        # Engagement trend impact
        if engagement_trend == "declining":
            risk_score += 30
            risk_factors.append("declining_engagement")
            warnings.append("story_view_decline")
        
        # Content consistency
        if content_consistency < 0.5:
            risk_score += 25
            risk_factors.append("content_inconsistency")
        
        # Response rate
        if response_rate < 0.3:
            risk_score += 20
            risk_factors.append("low_response_rate")
            warnings.append("engagement_unanswered")
        
        # Promotional content
        if promotional_ratio > 0.3:
            risk_score += 25
            risk_factors.append("excessive_promotion")
        
        # Risk level
        if risk_score >= 60:
            risk_level = "high"
        elif risk_score >= 30:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        recommendations = []
        if "declining_engagement" in risk_factors:
            recommendations.append("Analyze recent content changes, return to what worked")
        if "content_inconsistency" in risk_factors:
            recommendations.append("Establish consistent posting schedule and content pillars")
        if "low_response_rate" in risk_factors:
            recommendations.append("Dedicate time daily to respond to comments and DMs")
        if "excessive_promotion" in risk_factors:
            recommendations.append("Follow 80/20 rule: 80% value, 20% promotion")
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "warning_signals": warnings,
            "recommendations": recommendations
        }
