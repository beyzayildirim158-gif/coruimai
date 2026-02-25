# Content Plan Generator - 7-Day Dynamic Content Planning
# Synthesizes insights from ALL 7 agents to create actionable content plans
"""
Content Plan Generator Agent

This agent generates a fully dynamic 7-day content plan by synthesizing
outputs from all 7 analysis agents. NO hardcoded content is used - 
everything is derived from the analyzed account data.

Input Sources:
- Attention Architect: Hooks, retention data, pattern interrupts
- Visual Brand: Color palette, visual style, brand archetype
- Audience Dynamics: Posting times, personas, pain points, language
- Content Strategist: Content mix, hashtags, caption formulas
- Growth Architect: Growth tactics, viral loops, competitor gaps
- Domain Master: Niche benchmarks, trends, seasonal content

Output: Complete 7-day content plan with topics, hooks, captions,
hashtags, visual guidelines, and story schedule.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from google import genai
from google.genai import types

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ContentPlanGenerator(BaseAgent):
    """
    7-Day Content Plan Generator
    
    Generates dynamic, data-driven content plans by synthesizing
    insights from all 7 analysis agents.
    
    CRITICAL: No hardcoded content. All output derived from analysis data.
    """
    
    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.agent_name = "content_plan_generator"
        
        # Initialize content plan configuration
        self._init_day_purposes()
        self._init_hook_templates()
        self._init_caption_structures()
        self._init_story_templates()
        self._init_validation_rules()
    
    def _init_day_purposes(self):
        """Define the strategic purpose for each day of the week"""
        self.day_purposes = {
            1: {
                "name": "HOOK_DAY",
                "purpose": "Maximum reach, stop the scroll",
                "topic_source": "top_performing_theme",
                "content_focus": "viral_potential",
                "hook_priority": "highest_retention"
            },
            2: {
                "name": "VALUE_DAY",
                "purpose": "Educate, drive saves",
                "topic_source": "primary_pain_point",
                "content_focus": "save_worthy",
                "hook_priority": "question_or_statement"
            },
            3: {
                "name": "ENGAGEMENT_DAY",
                "purpose": "Drive comments, algorithm boost",
                "topic_source": "trending_topic",
                "content_focus": "discussion_starter",
                "hook_priority": "controversial_opinion"
            },
            4: {
                "name": "AUTHORITY_DAY",
                "purpose": "Build trust, establish expertise",
                "topic_source": "core_expertise",
                "content_focus": "credibility",
                "hook_priority": "story_or_statement"
            },
            5: {
                "name": "VIRAL_ATTEMPT_DAY",
                "purpose": "Maximum shares, reach explosion",
                "topic_source": "competitor_gap",
                "content_focus": "share_worthy",
                "hook_priority": "shock_or_emotion"
            },
            6: {
                "name": "COMMUNITY_DAY",
                "purpose": "Deepen connection, humanize brand",
                "topic_source": "behind_the_scenes",
                "content_focus": "relatability",
                "hook_priority": "story_hook"
            },
            7: {
                "name": "SOFT_SELL_DAY",
                "purpose": "Convert followers to customers",
                "topic_source": "offer_aligned",
                "content_focus": "conversion",
                "hook_priority": "pain_solution"
            }
        }
    
    def _init_hook_templates(self):
        """
        Hook formula templates - variables filled from analysis data
        These are STRUCTURE templates, not content templates
        """
        self.hook_structures = {
            "question": {
                "patterns": [
                    "Son {time_period} içinde kaç kez {pain_point} yaşadın?",
                    "{pain_point} seni de {emotion} hissettiriyor mu?",
                    "Neden {common_belief} aslında yanlış?",
                    "{audience_desire} istiyorsan neden hala {wrong_action} yapıyorsun?",
                    "Bu {niche_topic} hakkında ne kadar bilgilisin?"
                ],
                "engagement_type": "comment_driver",
                "best_for": ["value_day", "engagement_day"]
            },
            "statement": {
                "patterns": [
                    "{shocking_stat} ve kimse bundan bahsetmiyor.",
                    "{pain_point} yaşıyorsan, bu senin için.",
                    "Bunu bilmeden {desired_outcome} imkansız.",
                    "{niche_topic} hakkında öğrendiğim en önemli şey.",
                    "3 yılda {achievement} - işte nasıl yaptım."
                ],
                "engagement_type": "save_driver",
                "best_for": ["authority_day", "value_day"]
            },
            "story": {
                "patterns": [
                    "{time_reference} önce ben de {relatable_struggle} yaşıyordum...",
                    "Bir {client_type} bana şunu söyledi...",
                    "Herkes {common_action} yapıyor ama...",
                    "{personal_moment} yaşadığımda her şey değişti.",
                    "Bu hikayeyi daha önce hiç anlatmadım..."
                ],
                "engagement_type": "connection_driver",
                "best_for": ["community_day", "authority_day"]
            },
            "shock": {
                "patterns": [
                    "{common_belief}? Tamamen yanlış.",
                    "Bu yüzden {negative_outcome} yaşıyorsun.",
                    "{authority_figure} bile bunu yanlış yapıyor.",
                    "{popular_advice} sana zarar veriyor.",
                    "Kimsenin söylemediği gerçek: {hidden_truth}"
                ],
                "engagement_type": "share_driver",
                "best_for": ["viral_day", "engagement_day"]
            },
            "curiosity": {
                "patterns": [
                    "{outcome} için tek ihtiyacın olan şey...",
                    "{number} kişiden sadece {small_number}'i bunu biliyor.",
                    "Bu {simple_thing} hayatımı değiştirdi.",
                    "{niche_topic}'in gizli sırrı.",
                    "Bunu öğrenince {old_belief} hakkında düşüncen değişecek."
                ],
                "engagement_type": "watch_time_driver",
                "best_for": ["hook_day", "viral_day"]
            },
            "pain_solution": {
                "patterns": [
                    "{pain_point} yaşıyorsan çözümü buldum.",
                    "{negative_state}'dan {positive_state}'a geçmek için...",
                    "{pain_point} ile mücadele etmeyi bırak.",
                    "Artık {pain_point} yaşamak zorunda değilsin.",
                    "{desired_outcome} için eksik olan tek şey bu."
                ],
                "engagement_type": "conversion_driver",
                "best_for": ["soft_sell_day", "value_day"]
            }
        }
    
    def _init_caption_structures(self):
        """Caption structure templates based on brand voice"""
        self.caption_structures = {
            "educational": {
                "structure": "hook → problem → solution_steps → cta",
                "emoji_density": "low",
                "line_breaks": "paragraph",
                "length_range": (800, 1500)
            },
            "inspirational": {
                "structure": "hook → story → lesson → cta",
                "emoji_density": "medium",
                "line_breaks": "short",
                "length_range": (600, 1200)
            },
            "conversational": {
                "structure": "hook → relatable_point → question → cta",
                "emoji_density": "medium",
                "line_breaks": "short",
                "length_range": (400, 800)
            },
            "authoritative": {
                "structure": "hook → facts → expertise → cta",
                "emoji_density": "low",
                "line_breaks": "paragraph",
                "length_range": (600, 1200)
            },
            "casual": {
                "structure": "hook → quick_value → engagement_question",
                "emoji_density": "high",
                "line_breaks": "frequent",
                "length_range": (300, 600)
            }
        }
    
    def _init_story_templates(self):
        """Story slot purposes and types"""
        self.story_slots = {
            "slot1": {
                "purpose": "engagement",
                "types": ["poll", "question_sticker", "quiz"],
                "timing": "morning_active"
            },
            "slot2": {
                "purpose": "value",
                "types": ["quick_tip", "mini_tutorial", "insight"],
                "timing": "midday_active"
            },
            "slot3": {
                "purpose": "teaser",
                "types": ["post_preview", "countdown", "hint"],
                "timing": "pre_post"
            },
            "slot4": {
                "purpose": "promotion",
                "types": ["post_share", "engagement_prompt", "reply_request"],
                "timing": "post_post"
            },
            "slot5": {
                "purpose": "personal",
                "types": ["behind_scenes", "day_in_life", "casual_chat"],
                "timing": "evening_active"
            }
        }
    
    def _init_validation_rules(self):
        """Validation rules to ensure dynamic content"""
        # Updated for new pipeline - removed audienceDynamics and contentStrategist
        # as they are no longer in the new pipeline architecture
        self.required_agent_data = {
            "domainMaster": [
                "niche_identification", "benchmark_comparison", "trend_analysis",
                "hashtag_analysis", "content_pillar_analysis"
            ],
            "attentionArchitect": [
                "hookTemplates", "captionFormulas", "retentionPrediction",
                "emotionalTriggers", "thumbnailRecommendations"
            ],
            "visualBrand": [
                "dominantColors", "recommendedPalette", "gridProfessionalism",
                "thumbnailAnalysis", "brand_guidelines_suggestion"
            ],
            "growthVirality": [
                "growth_overview", "projections", "channel_analysis",
                "competitorGapAnalysis", "funnelAnalysis"
            ],
            "communityLoyalty": [
                "communityInsights", "engagementStrategies", "loyaltyBuilders",
                "sentiment_breakdown"
            ],
            "salesConversion": [
                "monetization_overview", "revenueStreams", "brandDealGuidelines",
                "conversionFunnel"
            ]
        }
    
    def get_system_prompt(self) -> str:
        return """Sen Content Plan Generator Agent'sın - 7 günlük içerik planı oluşturma uzmanısın.

## KRİTİK KURAL: HARDCODED İÇERİK YASAK

⛔ **ASLA** örnek hesap, konu, hook veya hashtag kullanma
⛔ **ASLA** analiz verisi olmadan varsayımda bulunma
⛔ **TÜM** içerik 7-agent analiz çıktısından dinamik üretilmeli

## TEMEL GÖREVİN:

7 farklı ajanın analiz çıktılarını sentezleyerek, tamamen VERİYE DAYALI 
7 günlük içerik planı oluşturmak.

## VERİ KAYNAKLARIN:

1. **Attention Architect**: Hook'lar, retention, pattern interrupt'lar
2. **Visual Brand**: Renk paleti, görsel stil, marka arketipi  
3. **Audience Dynamics**: Paylaşım saatleri, persona'lar, acı noktalar
4. **Content Strategist**: İçerik mixi, hashtag'ler, caption formülleri
5. **Growth Architect**: Rakip boşlukları, büyüme taktikleri
6. **Domain Master**: Niche benchmark'lar, trendler, sezonsal içerik
7. **Community Loyalty**: Topluluk sağlığı, sadakat göstergeleri
8. **Sales Conversion**: Monetizasyon hazırlığı, teklif uyumu

## GÜN BAZLI STRATEJİ:

**Gün 1 - HOOK GÜNÜ**: Maximum reach, scroll durdurma
**Gün 2 - DEĞER GÜNÜ**: Eğitim, kaydetme odaklı
**Gün 3 - ETKİLEŞİM GÜNÜ**: Yorum, algoritma boost
**Gün 4 - OTORİTE GÜNÜ**: Güven inşa, uzmanlık
**Gün 5 - VİRAL GÜNÜ**: Paylaşım, reach patlaması
**Gün 6 - TOPLULUK GÜNÜ**: Bağ derinleştirme, insanlaştırma
**Gün 7 - SOFT SELL GÜNÜ**: Dönüşüm, müşteri kazanma

## HOOK ÜRETİM KURALLARI:

Hook'ları şu formüllerle üret (değişkenler analiz verisinden):

1. **Soru Hook'u**: "{acı_nokta} seni de {duygu} hissettiriyor mu?"
2. **İfade Hook'u**: "{şok_istatistik} ve kimse bundan bahsetmiyor."
3. **Hikaye Hook'u**: "{zaman} önce ben de {ilişkilendirilebilir_mücadele} yaşıyordum..."
4. **Şok Hook'u**: "{yaygın_inanış}? Tamamen yanlış."
5. **Merak Hook'u**: "{sonuç} için tek ihtiyacın olan şey..."
6. **Acı-Çözüm Hook'u**: "{acı_nokta} yaşıyorsan çözümü buldum."

## CAPTION ÜRETİM KURALLARI:

1. Marka sesine (brand voice) uygun ton kullan
2. Optimal uzunluğu analiz verisinden al
3. CTA stilini engagement verisinden belirle
4. Kitle dilini (language patterns) kullan

## HASHTAG ROTASYONU:

3 set oluştur, günlere dağıt:
- Set 1 (Gün 1-2): Yüksek reach + niche
- Set 2 (Gün 3-4): Yüksek engagement + trend
- Set 3 (Gün 5-7): Mix + branded

## STORY STRATEJİSİ:

Günde 5 story slot'u:
1. Sabah aktif saat: Engagement (poll/soru)
2. Öğlen aktif saat: Değer (hızlı ipucu)
3. Post'tan 1 saat önce: Teaser
4. Post'tan 1 saat sonra: Paylaşım + CTA
5. Akşam aktif saat: Kişisel/BTS

## DOĞRULAMA KURALLARI:

Her içerik için kontrol et:
✅ Konu analiz verisinden türetilmiş
✅ Hook kitle diline uygun
✅ Hashtag'ler hesabın cluster'ından
✅ Paylaşım saati kitle aktivitesine uygun
✅ Görsel yönergeler marka paletine uygun
✅ CTA hesabın teklifiyle uyumlu

OUTPUT FORMAT: Yanıtını SADECE belirtilen JSON yapısında ver."""

    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        """Generate the content plan prompt with all agent data"""
        
        # Extract account basics
        username = account_data.get('username', 'unknown') or 'unknown'
        followers = account_data.get('followers', 0) or 0
        niche = account_data.get('niche', 'General') or 'General'
        
        # Extract cross-agent insights (from orchestrator enrichment)
        cross_insights = account_data.get('crossAgentInsights', {})
        agent_results = account_data.get('agentResults', {})
        
        # Get current date for planning
        start_date = datetime.now()
        plan_dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') 
                      for i in range(7)]
        day_names = [(start_date + timedelta(days=i)).strftime('%A') 
                     for i in range(7)]
        
        # Build comprehensive data summary from all agents
        data_summary = self._build_data_summary(account_data, agent_results, cross_insights)
        
        # Extract timezone and posting times from audience data
        audience_data = agent_results.get('audienceDynamics', {})
        posting_times = audience_data.get('optimal_posting_times', {})
        timezone = audience_data.get('account_timezone', account_data.get('timezone', 'Europe/Istanbul'))
        
        # Extract visual brand data
        visual_data = agent_results.get('visualBrand', {})
        color_palette = visual_data.get('brand_colors', visual_data.get('color_palette', {}))
        visual_archetype = visual_data.get('visualArchetypeAnalysis', {}).get('archetype', 'N/A')
        
        # Extract pain points from audience dynamics
        pain_points = audience_data.get('pain_points', [])
        personas = audience_data.get('personas', [])
        
        # Extract hashtag data from content strategist
        content_data = agent_results.get('contentStrategist', {})
        hashtag_clusters = content_data.get('hashtag_clusters', content_data.get('hashtagAnalysis', {}))
        
        # Extract domain-specific hashtags
        domain_data = agent_results.get('domainMaster', {})
        niche_hashtags = domain_data.get('niche_hashtags', [])
        trending_hashtags = domain_data.get('trending_hashtags', [])
        
        return f"""Bu Instagram hesabı için 7 günlük içerik planı oluştur:

## HESAP BİLGİLERİ:
- Username: @{username}
- Takipçi: {followers:,}
- Niche: {niche}
- Timezone: {timezone}

## PLAN TARİHLERİ:
{json.dumps(dict(zip(range(1, 8), zip(plan_dates, day_names))), indent=2, ensure_ascii=False)}

## KRİTİK VERİ KAYNAKLARI (Bu verilerden dinamik üret):

### POSTING TIMES (Audience Dynamics'ten):
{json.dumps(posting_times, ensure_ascii=False, indent=2)}

### COLOR PALETTE (Visual Brand'den):
{json.dumps(color_palette, ensure_ascii=False, indent=2)}

### VISUAL ARCHETYPE:
{visual_archetype}

### PAIN POINTS (Audience Dynamics'ten):
{json.dumps(pain_points[:5] if isinstance(pain_points, list) else pain_points, ensure_ascii=False, indent=2)}

### PERSONAS (Audience Dynamics'ten):
{json.dumps(personas[:3] if isinstance(personas, list) else personas, ensure_ascii=False, indent=2)}

### HASHTAG CLUSTERS (Content Strategist'ten):
{json.dumps(hashtag_clusters, ensure_ascii=False, indent=2)[:2000]}

### NICHE HASHTAGS (Domain Master'dan):
{json.dumps(niche_hashtags[:20] if isinstance(niche_hashtags, list) else niche_hashtags, ensure_ascii=False)}

### TRENDING HASHTAGS (Domain Master'dan):
{json.dumps(trending_hashtags[:10] if isinstance(trending_hashtags, list) else trending_hashtags, ensure_ascii=False)}

## 7 AJAN ANALİZ VERİLERİ:

{data_summary}

## İÇERİK PLANI OLUŞTURMA TALİMATLARI:

### 1. HAFTALIK STRATEJİ
- Ana tema: Kitle acı noktaları + niche trendlerinden türet
- Hedefler: Mevcut metrikler + iyileştirme hedeflerinden
- İçerik mixi: Content Strategist analizinden

### 2. GÜNLÜK PLAN (7 GÜN) - KRİTİK DETAYLAR

⚠️ **HER GÜN İÇİN ZORUNLU ALANLAR:**

**A. POSTING TIME (Kitle Aktivitesinden)**
- time: "HH:MM" formatında (örn: "18:30")
- timezone: "{timezone}"
- reason: Neden bu saat seçildi

**B. FULL CAPTION TEXT (200-600 karakter)**
- fullText: Tam caption metni (emoji dahil)
- charCount: Karakter sayısı
- cta.text: best_performing_ctas'tan
- emojiUsage: brand_emoji_patterns'ten

**C. HASHTAG SETS (Toplam 15)**
- primary.tags: hashtag_clusters.high_reach'ten 5 adet
- niche.tags: domain_master.niche_hashtags'ten 5 adet
- trending.tags: domain_master.trending_hashtags'ten 3-5 adet

**D. DAILY STORY PLAN (5 story)**
- Her story için spesifik saat (audience_active_times'tan)
- Story 1: Morning (poll/soru)
- Story 2: Midday (teaser)
- Story 3: Post+30dk (paylaşım + CTA)
- Story 4: Evening (BTS)
- Story 5: Night (Q&A)

**E. VISUAL GUIDELINES**
- colorPalette: visual_brand.brand_colors'tan hex değerleri
- thumbnailText: hook + topic'ten max 5 kelime
- style.archetype: visual_brand.visual_archetype'tan

**F. PAIN POINT MAPPING**
- linkedPainPoint: audience_dynamics.pain_points'ten
- audienceRelevance.primaryPersonaMatch: hangi persona

### 3. HASHTAG ROTASYONU
- 3 set oluştur
- Her sette 15-20 hashtag
- Niche + reach + engagement dengesi

### 4. KPI'LAR
- Hedef engagement rate
- Hedef reach
- Hedef takipçi büyümesi
- Hedef kaydetme oranı

⛔ **DOĞRULAMA KURALI**: Her {{ZORUNLU}} alanı gerçek analiz verisinden doldur - boş bırakma!

Aşağıdaki JSON yapısında yanıt ver:

{{
    "generatedFor": {{
        "handle": "@{username}",
        "niche": "{{analiz verisinden}}",
        "subNiche": "{{analiz verisinden}}",
        "analysisId": "{account_data.get('analysisId', 'N/A')}",
        "generatedDate": "{start_date.isoformat()}",
        "planPeriod": {{
            "startDate": "{plan_dates[0]}",
            "endDate": "{plan_dates[6]}"
        }}
    }},
    "dataSourcesSummary": {{
        "audienceDynamics": {{
            "primaryPersona": "{{analiz verisinden}}",
            "topPainPoints": ["{{analiz verisinden}}", "{{analiz verisinden}}", "{{analiz verisinden}}"],
            "optimalPostingTimes": ["{{analiz verisinden}}"],
            "languageStyle": "{{analiz verisinden}}"
        }},
        "contentStrategist": {{
            "contentPillars": ["{{analiz verisinden}}"],
            "brandVoice": "{{analiz verisinden}}",
            "topPerformingThemes": ["{{analiz verisinden}}"],
            "optimalCaptionLength": 0
        }},
        "attentionArchitect": {{
            "bestHookTypes": ["{{analiz verisinden}}"],
            "avgRetention": 0,
            "topEmotionalTriggers": ["{{analiz verisinden}}"]
        }},
        "domainMaster": {{
            "currentTrends": ["{{analiz verisinden}}"],
            "seasonalOpportunities": ["{{analiz verisinden}}"],
            "nicheHashtags": ["{{analiz verisinden}}"]
        }},
        "visualBrand": {{
            "colorPalette": ["{{analiz verisinden}}"],
            "visualArchetype": "{{analiz verisinden}}",
            "thumbnailStyle": "{{analiz verisinden}}"
        }},
        "growthArchitect": {{
            "competitorGaps": ["{{analiz verisinden}}"],
            "viralPatterns": ["{{analiz verisinden}}"],
            "growthProjection30Day": 0
        }}
    }},
    "weeklyStrategy": {{
        "theme": "{{kitle acı noktaları + niche trendlerinden dinamik üretilmiş}}",
        "goals": [
            "{{spesifik, ölçülebilir hedef 1}}",
            "{{spesifik, ölçülebilir hedef 2}}",
            "{{spesifik, ölçülebilir hedef 3}}"
        ],
        "contentMixRatio": {{
            "reels": 0,
            "carousels": 0,
            "staticPosts": 0,
            "stories": 0
        }},
        "focusAreas": ["{{analiz verisinden}}", "{{analiz verisinden}}"],
        "avoidAreas": ["{{analiz verisinden zayıf alanlar}}"]
    }},
    "dailyPlan": [
        {{
            "day": 1,
            "date": "{plan_dates[0]}",
            "dayOfWeek": "{day_names[0]}",
            "postingTime": {{
                "time": "{{ZORUNLU: audience_active_times'dan optimal saat - örn: '18:30'}}",
                "timezone": "{timezone}",
                "reason": "{{Bu saatin neden seçildiği - kitle aktivitesinden}}"
            }},
            "dayPurpose": {{
                "name": "HOOK_DAY",
                "objective": "Maximum reach, scroll durdurma",
                "primaryMetric": "reach"
            }},
            "topic": {{
                "title": "{{ZORUNLU: analiz verisinden dinamik konu}}",
                "angle": "{{benzersiz açı}}",
                "source": "{{hangi analiz verisinden türetildi}}",
                "linkedPainPoint": "{{ZORUNLU: audience_dynamics.pain_points'ten spesifik acı nokta}}",
                "audienceRelevance": {{
                    "score": 0,
                    "primaryPersonaMatch": "{{hangi persona ile eşleşiyor}}",
                    "engagementPotential": "high/medium/low"
                }}
            }},
            "content": {{
                "type": "{{en iyi performans gösteren format: reel/carousel/static}}",
                "hook": {{
                    "text": "{{ZORUNLU: kitle diline uygun, dinamik üretilmiş hook - 10-20 kelime}}",
                    "type": "{{hook tipi: question/statement/story/shock/curiosity}}",
                    "formula": "{{kullanılan formül}}",
                    "targetEmotion": "{{hedef duygu: curiosity/fear/excitement/frustration}}",
                    "expectedRetention": 0
                }},
                "script": {{
                    "intro": "{{hook'tan sonraki açılış - 2-3 cümle}}",
                    "body": [
                        "{{ana nokta 1}}",
                        "{{ana nokta 2}}",
                        "{{ana nokta 3}}"
                    ],
                    "cta": "{{engagement optimizer'dan en iyi CTA}}",
                    "duration": "{{saniye/dakika}}",
                    "pacing": "{{hızlı/orta/yavaş}}"
                }}
            }},
            "caption": {{
                "fullText": "{{ZORUNLU: 200-600 karakter tam caption metni - marka sesine uygun, emoji'li}}",
                "charCount": 0,
                "structure": "hook → value → cta",
                "cta": {{
                    "text": "{{ZORUNLU: best_performing_ctas'tan seçilmiş CTA}}",
                    "type": "{{comment/save/share/link}}",
                    "placement": "end"
                }},
                "emojiUsage": {{
                    "count": 0,
                    "emojis": ["{{brand_emoji_patterns'ten seçilmiş emojiler}}"],
                    "density": "low/medium/high"
                }},
                "lineBreaks": 0
            }},
            "hashtags": {{
                "primary": {{
                    "tags": ["{{ZORUNLU: hashtag_clusters.high_reach'ten 5 hashtag}}"],
                    "avgReach": "{{tahmini reach}}"
                }},
                "niche": {{
                    "tags": ["{{ZORUNLU: domain_master.niche_hashtags'ten 5 hashtag}}"],
                    "relevanceScore": 0
                }},
                "trending": {{
                    "tags": ["{{ZORUNLU: domain_master.trending_hashtags'ten 3 hashtag}}"],
                    "trendingUntil": "{{ne zamana kadar trend}}"
                }},
                "branded": ["{{varsa branded hashtag}}"],
                "total": 15,
                "rotationSet": "set1"
            }},
            "stories": [
                {{
                    "slot": 1,
                    "time": "{{ZORUNLU: audience_morning_active saatinden - örn: '09:00'}}",
                    "type": "Poll",
                    "content": "{{ZORUNLU: daily_topic ile ilgili poll sorusu}}",
                    "sticker": "poll",
                    "options": ["{{seçenek 1}}", "{{seçenek 2}}"],
                    "purpose": "engagement_boost"
                }},
                {{
                    "slot": 2,
                    "time": "{{ZORUNLU: audience_midday_active saatinden - örn: '12:30'}}",
                    "type": "Teaser",
                    "content": "{{ZORUNLU: daily_post için teaser metni}}",
                    "visualHint": "{{blur/partial/countdown}}",
                    "purpose": "anticipation_build"
                }},
                {{
                    "slot": 3,
                    "time": "{{ZORUNLU: post saatinden 30dk sonra - örn: '19:00'}}",
                    "type": "Post Share",
                    "content": "{{ZORUNLU: engagement prompt - yorum/kaydetme isteği}}",
                    "sticker": "link_to_post",
                    "engagementCTA": "{{spesifik CTA}}",
                    "purpose": "post_promotion"
                }},
                {{
                    "slot": 4,
                    "time": "{{ZORUNLU: audience_evening_active saatinden - örn: '20:30'}}",
                    "type": "Behind Scenes",
                    "content": "{{kişisel/BTS içerik - günle ilgili}}",
                    "sticker": "question_box",
                    "purpose": "connection_building"
                }},
                {{
                    "slot": 5,
                    "time": "{{ZORUNLU: gece aktif saat - örn: '22:00'}}",
                    "type": "Q&A",
                    "content": "{{soru kutusu veya AMA}}",
                    "sticker": "question_sticker",
                    "purpose": "audience_insight"
                }}
            ],
            "visualGuidelines": {{
                "colorPalette": {{
                    "primary": "{{ZORUNLU: visual_brand.brand_colors'tan - hex}}",
                    "secondary": "{{ZORUNLU: visual_brand.brand_colors'tan - hex}}",
                    "accent": "{{ZORUNLU: visual_brand.brand_colors'tan - hex}}",
                    "background": "{{önerilen arkaplan rengi - hex}}"
                }},
                "thumbnailText": {{
                    "text": "{{ZORUNLU: hook + topic'ten türetilmiş thumbnail metni - max 5 kelime}}",
                    "font": "{{önerilen font stili}}",
                    "position": "{{center/top/bottom}}"
                }},
                "style": {{
                    "archetype": "{{ZORUNLU: visual_brand.visual_archetype'tan}}",
                    "mood": "{{görsel ruh hali}}",
                    "composition": "{{rule of thirds/centered/asymmetric}}",
                    "lighting": "{{bright/moody/natural}}"
                }},
                "facePresence": {{
                    "recommended": true,
                    "expression": "{{önerilen yüz ifadesi}}",
                    "eyeContact": true
                }}
            }},
            "engagement": {{
                "commentPrompt": "{{kitle diline uygun soru}}",
                "replyStrategy": "{{ilk X yoruma yanıt}}",
                "expectedMetrics": {{
                    "likes": 0,
                    "comments": 0,
                    "saves": 0,
                    "shares": 0,
                    "reach": 0
                }}
            }}
        }}
    ],
    "weeklyHashtagRotation": {{
        "set1": {{
            "days": [1, 2],
            "hashtags": ["{{analiz verisinden 15-20 hashtag}}"],
            "focus": "reach_focused",
            "totalReach": "{{tahmini reach}}"
        }},
        "set2": {{
            "days": [3, 4],
            "hashtags": ["{{analiz verisinden 15-20 hashtag}}"],
            "focus": "engagement_focused",
            "totalReach": "{{tahmini reach}}"
        }},
        "set3": {{
            "days": [5, 6, 7],
            "hashtags": ["{{analiz verisinden 15-20 hashtag}}"],
            "focus": "mixed_niche",
            "totalReach": "{{tahmini reach}}"
        }},
        "avoidHashtags": ["{{shadowban riski olanlar}}"],
        "rotationRationale": "{{neden bu dağılım}}"
    }},
    "contentPillars": {{
        "identified": ["{{Content Strategist'ten}}"],
        "weeklyDistribution": {{
            "pillar1": 0,
            "pillar2": 0,
            "pillar3": 0
        }},
        "recommendations": ["{{pillar optimizasyon önerileri}}"]
    }},
    "kpis": {{
        "currentMetrics": {{
            "engagementRate": 0,
            "avgReach": 0,
            "avgSaves": 0,
            "followerGrowthRate": 0
        }},
        "weeklyTargets": {{
            "targetEngagementRate": 0,
            "targetReach": 0,
            "targetSaves": 0,
            "targetFollowerGrowth": 0,
            "targetComments": 0
        }},
        "improvementPercentages": {{
            "engagementImprovement": "+X%",
            "reachImprovement": "+X%",
            "savesImprovement": "+X%"
        }},
        "trackingRecommendations": ["{{nasıl takip edilmeli}}"]
    }},
    "implementationNotes": {{
        "criticalSuccessFactors": ["{{başarı için kritik faktörler}}"],
        "potentialChallenges": ["{{olası zorluklar}}"],
        "adaptationGuidelines": "{{plana nasıl adapte olunmalı}}",
        "reviewSchedule": "{{ne zaman gözden geçirilmeli}}"
    }},
    "validationReport": {{
        "allTopicsFromAnalysis": true,
        "hooksMatchAudienceLanguage": true,
        "hashtagsFromAnalyzedClusters": true,
        "postingTimesMatchActivity": true,
        "visualsMatchBrandPalette": true,
        "ctasAlignedWithOffer": true,
        "noHardcodedContent": true,
        "dataCompleteness": 0
    }}
}}

**ÖNEMLİ**: Yukarıdaki tüm {{}} içindeki değerler, sağlanan analiz verilerinden dinamik olarak doldurulmalıdır. Hiçbir örnek veya varsayılan değer kullanma. Eksik veri varsa, ilgili alanı "Analiz verisi eksik" olarak işaretle."""

    def _build_data_summary(
        self, 
        account_data: Dict[str, Any], 
        agent_results: Dict[str, Any],
        cross_insights: Dict[str, Any]
    ) -> str:
        """Build comprehensive data summary from all agent outputs"""
        
        summary_parts = []
        
        # 1. Audience Dynamics Data - CRITICAL FOR POSTING TIMES & PAIN POINTS
        audience_data = agent_results.get('audienceDynamics', {})
        cross_audience = cross_insights.get('audienceDynamics', {})
        
        # Extract posting times specifically
        optimal_times = audience_data.get('optimal_posting_times', 
                         audience_data.get('audience_analysis', {}).get('optimal_posting_times', {}))
        active_hours = audience_data.get('active_hours', 
                        audience_data.get('audience_analysis', {}).get('active_hours', {}))
        
        # Extract pain points specifically
        pain_points = audience_data.get('pain_points',
                       audience_data.get('audience_analysis', {}).get('pain_points', []))
        
        # Extract language patterns for caption generation
        language_patterns = audience_data.get('language_patterns',
                             audience_data.get('audience_analysis', {}).get('language_patterns', {}))
        
        # Extract emoji patterns
        emoji_patterns = audience_data.get('emoji_patterns',
                          audience_data.get('audience_analysis', {}).get('emoji_patterns', []))
        
        summary_parts.append(f"""
### AUDIENCE DYNAMICS - KRİTİK VERİLER:

**POSTING TIMES (Content Plan için ZORUNLU):**
{json.dumps(optimal_times, ensure_ascii=False, indent=2)}

**ACTIVE HOURS BY TIME OF DAY:**
{json.dumps(active_hours, ensure_ascii=False, indent=2)}

**PAIN POINTS (Her gün için topic mapping ZORUNLU):**
{json.dumps(pain_points, ensure_ascii=False, indent=2)}

**LANGUAGE PATTERNS (Caption generation için):**
{json.dumps(language_patterns, ensure_ascii=False, indent=2)[:1000]}

**EMOJI PATTERNS (Caption emoji usage için):**
{json.dumps(emoji_patterns, ensure_ascii=False)}

**PERSONAS (Relevance scoring için):**
{json.dumps(cross_audience.get('topPersonas', []), ensure_ascii=False, indent=2)}

- Segmentasyon: {json.dumps(cross_audience.get('followerSegmentation', {}), ensure_ascii=False, indent=2)}
- Kitle Kalitesi: {cross_audience.get('audienceQuality', 'N/A')}
""")
        
        # 2. Content Strategist Data - CRITICAL FOR HASHTAGS & CTAs
        content_data = agent_results.get('contentStrategist', {})
        cross_content = cross_insights.get('contentStrategist', {})
        
        # Extract hashtag clusters specifically
        hashtag_analysis = content_data.get('hashtagAnalysis', 
                            content_data.get('hashtag_analysis', {}))
        high_reach_hashtags = hashtag_analysis.get('high_reach', 
                               hashtag_analysis.get('topPerforming', []))
        
        # Extract best CTAs
        best_ctas = content_data.get('best_performing_ctas',
                     content_data.get('hookAnalysis', {}).get('best_ctas', []))
        
        # Extract brand voice
        brand_voice = content_data.get('brand_voice',
                       content_data.get('content_analysis', {}).get('brand_voice', {}))
        
        summary_parts.append(f"""
### CONTENT STRATEGIST - KRİTİK VERİLER:

**HASHTAG CLUSTERS (Her gün için ZORUNLU):**
- High Reach Tags: {json.dumps(high_reach_hashtags, ensure_ascii=False)}
- Full Analysis: {json.dumps(hashtag_analysis, ensure_ascii=False, indent=2)[:1500]}

**BEST PERFORMING CTAs (Caption için ZORUNLU):**
{json.dumps(best_ctas, ensure_ascii=False, indent=2)}

**BRAND VOICE (Caption generation için):**
{json.dumps(brand_voice, ensure_ascii=False, indent=2)}

- İçerik Sütunları: {json.dumps(cross_content.get('contentPillars', []), ensure_ascii=False)}
- Hook Analizi: {json.dumps(cross_content.get('hookAnalysis', {}), ensure_ascii=False, indent=2)[:1000]}
- Caption Kalitesi: {cross_content.get('captionQuality', 'N/A')}
- Optimal Caption Length: {content_data.get('optimal_caption_length', 'N/A')}
""")
        
        # 3. Attention Architect Data
        attention_data = agent_results.get('attentionArchitect', {})
        summary_parts.append(f"""
### ATTENTION ARCHITECT:
- Retention Prediction: {json.dumps(attention_data.get('retentionPrediction', {}), ensure_ascii=False, indent=2)}
- Emotional Triggers: {json.dumps(attention_data.get('emotionalTriggers', []), ensure_ascii=False, indent=2)}
- Post Level Analysis: {json.dumps(attention_data.get('postLevelAnalysis', [])[:3], ensure_ascii=False, indent=2)}
- Hook Effectiveness: {json.dumps(attention_data.get('hook_analysis', {}), ensure_ascii=False, indent=2)[:1500]}
- Pattern Interrupts: {json.dumps(attention_data.get('pattern_interrupts', {}), ensure_ascii=False, indent=2)[:1000]}
""")
        
        # 4. Visual Brand Data - CRITICAL FOR VISUAL GUIDELINES
        visual_data = agent_results.get('visualBrand', {})
        cross_visual = cross_insights.get('visualBrand', {})
        
        # Extract brand colors specifically
        brand_colors = visual_data.get('brand_colors',
                        visual_data.get('brand_analysis', {}).get('color_palette', {}))
        
        # Extract visual archetype
        visual_archetype = visual_data.get('visualArchetypeAnalysis',
                            visual_data.get('visual_archetype', {}))
        
        summary_parts.append(f"""
### VISUAL BRAND - KRİTİK VERİLER:

**BRAND COLORS (Visual guidelines için ZORUNLU):**
{json.dumps(brand_colors, ensure_ascii=False, indent=2)}

**VISUAL ARCHETYPE (Style için ZORUNLU):**
{json.dumps(visual_archetype, ensure_ascii=False, indent=2)}

**DOMINANT COLORS:**
{json.dumps(cross_visual.get('dominantColors', []), ensure_ascii=False)}

- Renk Tutarlılığı: {json.dumps(cross_visual.get('colorConsistencyScore', {}), ensure_ascii=False, indent=2)}
- Grid Profesyonelliği: {json.dumps(cross_visual.get('gridProfessionalism', {}), ensure_ascii=False, indent=2)}
- Thumbnail Analizi: {json.dumps(cross_visual.get('thumbnailAnalysis', {}), ensure_ascii=False, indent=2)[:1000]}
""")
        
        # 5. Growth Architect Data
        growth_data = agent_results.get('growthVirality', {})
        summary_parts.append(f"""
### GROWTH ARCHITECT:
- Growth Projection: {json.dumps(growth_data.get('growthProjection', {}), ensure_ascii=False, indent=2)[:1500]}
- Competitor Gap Analysis: {json.dumps(growth_data.get('competitorGapAnalysis', {}), ensure_ascii=False, indent=2)[:1500]}
- Funnel Analysis: {json.dumps(growth_data.get('funnelAnalysis', {}), ensure_ascii=False, indent=2)[:1000]}
- Viral Loop Strategy: {json.dumps(growth_data.get('viralLoopStrategy', {}), ensure_ascii=False, indent=2)[:1000]}
- Projections: {json.dumps(growth_data.get('projections', {}), ensure_ascii=False, indent=2)}
""")
        
        # 6. Domain Master Data - CRITICAL FOR NICHE HASHTAGS
        domain_data = agent_results.get('domainMaster', {})
        
        # Extract niche hashtags specifically
        niche_hashtags = domain_data.get('niche_hashtags',
                          domain_data.get('nicheBenchmarks', {}).get('recommended_hashtags', []))
        
        # Extract trending hashtags
        trending_hashtags = domain_data.get('trending_hashtags',
                             domain_data.get('trend_analysis', {}).get('trending_tags', []))
        
        # Extract seasonal content
        seasonal = domain_data.get('seasonalConsiderations', {})
        
        summary_parts.append(f"""
### DOMAIN MASTER - KRİTİK VERİLER:

**NICHE HASHTAGS (Her gün için ZORUNLU):**
{json.dumps(niche_hashtags, ensure_ascii=False, indent=2)}

**TRENDING HASHTAGS (Güncel trendler):**
{json.dumps(trending_hashtags, ensure_ascii=False, indent=2)}

**SEASONAL CONSIDERATIONS:**
{json.dumps(seasonal, ensure_ascii=False, indent=2)}

- Niche: {json.dumps(domain_data.get('niche_identification', {}), ensure_ascii=False, indent=2)}
- Niche Benchmarks: {json.dumps(domain_data.get('nicheBenchmarks', {}), ensure_ascii=False, indent=2)[:1000]}
- Sector Best Practices: {json.dumps(domain_data.get('sectorBestPractices', {}), ensure_ascii=False, indent=2)[:1000]}
- Competitor Analysis: {json.dumps(domain_data.get('competitorAnalysis', {}), ensure_ascii=False, indent=2)[:1000]}
""")
        
        # 7. Community Loyalty Data
        community_data = agent_results.get('communityLoyalty', {})
        summary_parts.append(f"""
### COMMUNITY LOYALTY:
- Community Health: {json.dumps(community_data.get('community_health', {}), ensure_ascii=False, indent=2)[:1000]}
- Loyalty Indicators: {json.dumps(community_data.get('loyalty_analysis', {}), ensure_ascii=False, indent=2)[:1000]}
- Engagement Patterns: {json.dumps(community_data.get('engagement_patterns', {}), ensure_ascii=False, indent=2)[:1000]}
""")
        
        # 8. Sales Conversion Data
        sales_data = agent_results.get('salesConversion', {})
        summary_parts.append(f"""
### SALES CONVERSION:
- Monetization Readiness: {json.dumps(sales_data.get('monetization_readiness', {}), ensure_ascii=False, indent=2)[:1000]}
- Offer Alignment: {json.dumps(sales_data.get('offer_analysis', {}), ensure_ascii=False, indent=2)[:1000]}
- Conversion Potential: {json.dumps(sales_data.get('conversion_analysis', {}), ensure_ascii=False, indent=2)[:1000]}
""")
        
        # 9. Level 0 Summary (from orchestrator)
        level0_summary = account_data.get('level0Summary', {})
        summary_parts.append(f"""
### LEVEL 0 ÖZET:
- Ortalama İçerik Skoru: {level0_summary.get('avgContentScore', 'N/A')}
- Ortalama Kitle Skoru: {level0_summary.get('avgAudienceScore', 'N/A')}
- Ortalama Görsel Skoru: {level0_summary.get('avgVisualScore', 'N/A')}
- Genel Level 0 Skoru: {level0_summary.get('overallLevel0Score', 'N/A')}
- Kritik Sorunlar: {json.dumps(level0_summary.get('criticalIssues', []), ensure_ascii=False)}
- Güçlü Yönler: {json.dumps(level0_summary.get('topStrengths', []), ensure_ascii=False)}
""")
        
        return "\n".join(summary_parts)
    
    def validate_required_data(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that all required data is present from agent analyses.
        Returns validation status and missing fields.
        """
        missing = []
        warnings = []
        
        # Handle case where full results object is passed instead of just agentResults
        if "agentResults" in agent_results:
            agent_results = agent_results["agentResults"]
        elif "agent_details" in agent_results:
            agent_results = agent_results["agent_details"]
        
        # Ensure agent_results is a dict
        if not isinstance(agent_results, dict):
            logger.error(f"agent_results is not a dict: {type(agent_results)}")
            return {
                "status": "invalid",
                "completeness": 0,
                "missing_agents": ["Invalid agent_results format"],
                "warnings": [],
                "can_generate": False,
                "recommendation": "Agent results formatı geçersiz"
            }
        
        for agent, required_fields in self.required_agent_data.items():
            if agent not in agent_results:
                missing.append(f"{agent}: Agent sonucu eksik")
                continue
            
            result = agent_results[agent]
            
            # Skip if result is not a dict
            if not isinstance(result, dict):
                warnings.append(f"{agent}: Sonuç formatı geçersiz (dict değil)")
                continue
                
            if result.get('error_flag'):
                warnings.append(f"{agent}: Hata ile tamamlandı - {result.get('error', 'Unknown')}")
                continue
            
            for field in required_fields:
                # Check in various locations
                found = False
                if field in result:
                    found = True
                elif 'metrics' in result and field in result['metrics']:
                    found = True
                elif 'analysis' in result and isinstance(result['analysis'], dict):
                    if field in result['analysis']:
                        found = True
                
                if not found:
                    warnings.append(f"{agent}.{field}: Alan bulunamadı")
        
        is_valid = len(missing) == 0
        completeness = 1.0 - (len(missing) + len(warnings) * 0.5) / (
            sum(len(fields) for fields in self.required_agent_data.values())
        )
        
        return {
            "status": "valid" if is_valid else "incomplete",
            "completeness": max(0, min(1, completeness)),
            "missing_agents": missing,
            "warnings": warnings,
            "can_generate": completeness >= 0.5,  # Need at least 50% data
            "recommendation": "Tam sonuçlar için eksik ajanları yeniden çalıştırın" if not is_valid else "Veri tam"
        }
    
    async def generate_content_plan(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a 7-day content plan from all agent analysis results.
        
        This is the main entry point for content plan generation.
        """
        logger.info(f"Starting content plan generation for @{account_data.get('username', 'unknown')}")
        
        # Step 1: Validate required data
        validation = self.validate_required_data(agent_results)
        
        if not validation['can_generate']:
            logger.warning(f"Insufficient data for content plan: {validation}")
            return {
                "error": "Yetersiz analiz verisi",
                "validation": validation,
                "recommendation": "En az %50 veri tamamlanması gerekiyor"
            }
        
        # Step 2: Prepare enriched data with all agent results
        enriched_data = account_data.copy()
        enriched_data['agentResults'] = agent_results
        
        # Step 3: Generate content plan using LLM
        try:
            result = await self.analyze(enriched_data)
            
            # Step 4: Post-process and validate output
            if result and not result.get('error'):
                result['_metadata'] = {
                    'generatedAt': datetime.now().isoformat(),
                    'dataValidation': validation,
                    'generatorVersion': '1.0.0'
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Content plan generation failed: {e}")
            return {
                "error": str(e),
                "validation": validation,
                "partialData": True
            }


# Export the generator
__all__ = ['ContentPlanGenerator']
