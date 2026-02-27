# Attention Architect Agent - PhD Level Implementation
# Dikkat Psikolojisi, Hook Optimizasyonu, Retention Analizi
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent


class AttentionArchitectAgent(BaseAgent):
    """
    Attention Architect Agent - PhD Level
    
    Uzmanlık Alanları:
    - Dikkat Ekonomisi ve Nöropsikoloji
    - Hook Optimizasyonu ve Formülleri
    - Retention (Watch Time) Analizi
    - Caption Psikolojisi
    - Thumbnail/Cover Optimizasyonu
    
    Metrikler:
    - Hook Effectiveness Score (0-100)
    - Retention Potential Score (0-100)
    - Caption Engagement Score (0-100)
    - Thumbnail Impact Score (0-100)
    - Overall Attention Score (0-100)
    - Estimated Watch Time Multiplier
    """
    
    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "Attention Architect"
        self.role = "Content Retention & Hook Optimization Specialist"
        self.specialty = "Attention psychology, hook optimization, retention analysis, caption psychology"
        
        # Initialize all knowledge bases
        self._init_attention_metrics()
        self._init_psychological_triggers()
        self._init_platform_dynamics()
        self._init_hook_categories()
        self._init_hook_formulas()
        self._init_retention_techniques()
        self._init_caption_formulas()
        self._init_thumbnail_principles()
        self._init_niche_benchmarks()
        
        # 2026 Advanced Hook & Retention Strategies
        self._init_2026_hook_strategies()
    
    def _init_attention_metrics(self):
        """Sosyal medya dikkat ekonomisi metrikleri"""
        self.attention_durations = {
            "feed_scroll": 1.7,  # saniye/post
            "reels_first_decision": (0.5, 1.5),  # saniye
            "story_view": (2, 3),  # saniye
            "caption_start": 3,  # saniye
            "full_video_decision": (3, 5)  # saniye
        }
        
        # Attention funnel conversion rates
        self.attention_funnel = {
            "impression": {"rate": 100, "decision_time": 0},
            "scroll_stop": {"rate": (15, 25), "decision_time": 0.5},
            "engagement_start": {"rate": (5, 10), "decision_time": 3},
            "full_consumption": {"rate": (2, 5), "decision_time": "varies"},
            "action": {"rate": (0.5, 2), "decision_time": "post_consumption"}
        }
        
        # Algorithm attention signals
        self.positive_signals = [
            "watch_time_over_50_percent",
            "replay",
            "share",
            "save",
            "long_comment",
            "profile_visit_after_view",
            "follow_after_view"
        ]
        
        self.negative_signals = [
            "quick_scroll_past",
            "skip_stories_reels",
            "hide_not_interested",
            "unfollow_after_view",
            "report"
        ]
    
    def _init_psychological_triggers(self):
        """Nöropsikolojik tetikleyiciler"""
        self.brain_triggers = {
            "novelty": {
                "description": "Beyin yeni şeylere otomatik tepki verir, dopamin salınımı",
                "application": "Beklenmedik açılışlar",
                "example": "Bunu daha önce hiç duymadınız...",
                "scroll_stop": 5,
                "watch_time": 3,
                "share_rate": 3
            },
            "threat_opportunity": {
                "description": "Hayatta kalma içgüdüsü, FOMO",
                "application": "Urgency yaratma",
                "example": "Bu hatayı yapıyorsanız...",
                "scroll_stop": 4,
                "watch_time": 4,
                "share_rate": 3
            },
            "social_proof": {
                "description": "Sürü psikolojisi, güvenlik hissi",
                "application": "Sayılar, testimonial",
                "example": "10.000+ kişi bunu uyguladı...",
                "scroll_stop": 3,
                "watch_time": 4,
                "share_rate": 4
            },
            "curiosity_gap": {
                "description": "Bilgi eksikliği rahatsızlık yaratır",
                "application": "Açık döngüler",
                "example": "3. madde her şeyi değiştirdi...",
                "scroll_stop": 5,
                "watch_time": 5,
                "share_rate": 3
            },
            "self_relevance": {
                "description": "Bu benim için algısı, kimlik doğrulama",
                "application": "Hedef kitle çağrısı",
                "example": "Eğer [hedef kitle] iseniz...",
                "scroll_stop": 4,
                "watch_time": 5,
                "share_rate": 4
            },
            "emotion": {
                "description": "Duygusal içerik daha iyi hatırlanır",
                "application": "Emotional hooks",
                "example": "Şaşkınlık, öfke, neşe, korku",
                "scroll_stop": 4,
                "watch_time": 4,
                "share_rate": 5
            }
        }
        
        # Bottom-up vs Top-down attention
        self.attention_types = {
            "bottom_up": {
                "type": "automatic",
                "triggers": ["movement", "contrast", "faces", "bright_colors", "unexpected_sounds"]
            },
            "top_down": {
                "type": "conscious",
                "triggers": ["interest_match", "problem_solution", "social_proof", "curiosity", "value_promise"]
            }
        }
    
    def _init_platform_dynamics(self):
        """Platform bazlı dikkat dinamikleri"""
        self.platform_attention = {
            "feed_post": {
                "first_attention": {"target": "visual", "time": 0.3},
                "second_attention": {"target": "caption_first_line", "time": 0.5},
                "decision_point": (1, 2),
                "engagement_window": (3, 5),
                "critical_element": "thumb_stopping_visual"
            },
            "reels": {
                "first_attention": {"target": "first_frame_plus_audio", "time": 0.5},
                "hook_window": (0, 3),
                "retention_check": (3, 7),
                "mid_roll_retention": (15, 30),
                "completion_decision": "last_5_seconds",
                "critical_element": "first_1_second"
            },
            "stories": {
                "first_attention": {"target": "instant", "time": 0.2},
                "skip_decision": (1, 2),
                "engagement_window": (3, 5),
                "tap_forward_threshold": 5,
                "critical_element": "immediate_value_intrigue"
            },
            "carousel": {
                "first_slide": "hook_function",
                "swipe_decision": (2, 3),
                "optimal_slides": (7, 10),
                "last_slide": "cta_critical",
                "critical_element": "each_slide_independent_value"
            }
        }
    
    def _init_hook_categories(self):
        """Hook kategorileri ve özellikleri"""
        self.hook_categories = {
            "question": {
                "types": {
                    "rhetorical": "Neden herkes bunu yanlış yapıyor?",
                    "direct": "Sen de bu hatayı yapıyor musun?",
                    "provocative": "Ya sana her şeyin yalan olduğunu söylesem?"
                },
                "effectiveness": 4,
                "best_for": "curiosity_generation"
            },
            "statement": {
                "types": {
                    "controversial": "Sabah rutinleri işe yaramıyor",
                    "bold_claim": "Bu tek değişiklik hayatımı değiştirdi",
                    "counter_intuitive": "Daha az çalışarak daha çok kazandım"
                },
                "effectiveness": 5,
                "best_for": "polarization_engagement"
            },
            "story": {
                "types": {
                    "personal": "3 ay önce her şeyi kaybettim...",
                    "transformation": "0'dan 100K'ya nasıl geldim",
                    "conflict": "Patronum beni kovduğunda..."
                },
                "effectiveness": 4,
                "best_for": "connection_building"
            },
            "number": {
                "types": {
                    "list": "5 şey öğrendim...",
                    "specific": "37 gün içinde...",
                    "comparison": "10x daha hızlı..."
                },
                "effectiveness": 4,
                "best_for": "credibility_concrete"
            },
            "command": {
                "types": {
                    "stop": "Bunu yapmayı bırak!",
                    "watch": "Sonuna kadar izle",
                    "save": "Bunu kaydet, lazım olacak"
                },
                "effectiveness": 3,
                "best_for": "direct_action"
            },
            "curiosity": {
                "types": {
                    "incomplete": "Kimsenin bilmediği şey...",
                    "secret": "Gizli formül...",
                    "reveal": "Sonunda açıklıyorum..."
                },
                "effectiveness": 5,
                "best_for": "highest_retention"
            }
        }
    
    def _init_hook_formulas(self):
        """Hook formül şablonları"""
        self.hook_formulas = {
            "problem_agitate": {
                "formula": "[Problem] yaşıyorsan, [sonuç] olabilir. İşte çözüm...",
                "best_for": "educational_content",
                "effectiveness": 4
            },
            "curiosity_gap": {
                "formula": "[Otorite/Sayı] [sonuç] elde etti. [Sır] sayesinde...",
                "best_for": "transformation_content",
                "effectiveness": 5
            },
            "direct_address": {
                "formula": "[Hedef kitle], bu seni ilgilendiriyor. [Hook]...",
                "best_for": "niche_specific",
                "effectiveness": 4
            },
            "pattern_interrupt": {
                "formula": "[Beklenmedik ifade]. Evet, doğru duydun...",
                "best_for": "viral_potential",
                "effectiveness": 5
            },
            "social_proof": {
                "formula": "[Sayı] kişi bunu yaptı ve [sonuç]. Sen de yapabilirsin...",
                "best_for": "trust_building",
                "effectiveness": 4
            },
            "fomo": {
                "formula": "[Zaman sınırı] içinde [fırsat]. Kaçırma...",
                "best_for": "urgency_creation",
                "effectiveness": 4
            }
        }
        
        # First 3 seconds framework
        self.first_3_seconds = {
            "second_0_1": {
                "name": "HOOK",
                "elements": ["visual_hook", "audio_hook", "text_overlay", "facial_expression", "movement_start"],
                "goal": "Capture attention"
            },
            "second_1_2": {
                "name": "PROMISE",
                "elements": ["what_they_learn", "value_promise", "curiosity_trigger", "watch_till_end_reason"],
                "goal": "Create commitment"
            },
            "second_2_3": {
                "name": "PROOF_TRANSITION",
                "elements": ["why_listen", "credibility_hint", "content_transition", "first_value_piece"],
                "goal": "Establish authority"
            }
        }
    
    def _init_retention_techniques(self):
        """Retention artırma teknikleri"""
        self.retention_techniques = {
            "open_loops": {
                "description": "Başta soru sor, sonda cevapla",
                "examples": ["Sonunda büyük reveal var", "3. madde en iyi", "Cliffhangers between sections"],
                "impact": "high"
            },
            "pattern_interrupts": {
                "description": "Her 3-5 saniyede değişim",
                "examples": ["Zoom/angle change", "Music/sound change", "Text overlay change", "B-roll addition"],
                "impact": "high"
            },
            "value_stacking": {
                "description": "Her 5-10 saniyede yeni değer",
                "examples": ["Ama dahası var...", "Bonus tips", "Unexpected additions"],
                "impact": "medium_high"
            },
            "pacing_optimization": {
                "description": "Hızlı başla, değer ver, hızlı bitir",
                "examples": ["Dead air elimination", "Jump cuts", "Energy consistency"],
                "impact": "medium"
            },
            "visual_variety": {
                "description": "Her 2-3 saniyede görsel değişim",
                "examples": ["Different angles", "Text animations", "Graphics", "Face + B-roll mix"],
                "impact": "medium_high"
            },
            "audio_optimization": {
                "description": "Ses kalitesi ve çeşitliliği",
                "examples": ["Trending sounds", "Music energy matching", "Voice modulation", "Sound effects"],
                "impact": "medium"
            }
        }
        
        # Retention checkpoints
        self.retention_checkpoints = {
            "0_3s": {"name": "HOOK", "check": "Dikkat yakalandı mı?"},
            "3_7s": {"name": "PROMISE", "check": "Değer vaadi verildi mi?"},
            "7_15s": {"name": "FIRST_VALUE", "check": "İlk somut değer sunuldu mu?"},
            "15_30s": {"name": "PATTERN_INTERRUPT", "check": "Dikkat tazelendi mi?"},
            "30_45s": {"name": "CORE_VALUE", "check": "Ana içerik sunuldu mu?"},
            "45_60s": {"name": "PAYOFF", "check": "Vaat yerine getirildi mi?"},
            "last_5s": {"name": "CTA", "check": "Aksiyon istendi mi?"}
        }
        
        # Drop-off patterns and solutions
        self.dropoff_patterns = {
            "cliff_drop": {
                "pattern": "İlk 3 sn'de %50+ düşüş",
                "cause": "Zayıf hook",
                "solution": "Hook optimizasyonu"
            },
            "steady_decline": {
                "pattern": "Lineer düşüş",
                "cause": "Değer eksikliği",
                "solution": "Content restructure"
            },
            "mid_roll_drop": {
                "pattern": "Ortada ani düşüş",
                "cause": "Sıkıcı bölüm",
                "solution": "Pattern interrupt ekle"
            },
            "end_drop": {
                "pattern": "Son %20'de düşüş",
                "cause": "Zayıf kapanış",
                "solution": "Strong CTA, cliffhanger"
            }
        }
        
        # Drop-off solution matrix
        self.dropoff_solutions = {
            "0_1s": "Better thumbnail, stronger open",
            "1_3s": "Rewrite hook, faster pace",
            "3_7s": "Earlier value, clearer promise",
            "7_15s": "Pattern interrupt, visual change",
            "15_30s": "New hook, unexpected element",
            "30_plus": "Payoff tease, wait for it",
            "pre_end": "Bonus value, strong CTA"
        }
    
    def _init_caption_formulas(self):
        """Caption yapı formülleri"""
        self.caption_formulas = {
            "aida": {
                "structure": ["Attention", "Interest", "Desire", "Action"],
                "description": "Hook → Problem/story → Solution/benefit → CTA",
                "best_for": "promotional_content"
            },
            "pas": {
                "structure": ["Problem", "Agitate", "Solution"],
                "description": "Pain point → Make it worse → Your answer",
                "best_for": "educational_content"
            },
            "bab": {
                "structure": ["Before", "After", "Bridge"],
                "description": "Current state → Desired state → How to get there",
                "best_for": "transformation_content"
            },
            "story": {
                "structure": ["Setup", "Conflict", "Resolution", "Lesson"],
                "description": "Context → Challenge → Outcome → Takeaway",
                "best_for": "personal_content"
            },
            "value_stack": {
                "structure": ["Hook", "Point 1", "Point 2", "Point 3", "CTA"],
                "description": "Attention grabber → Value points → Engagement ask",
                "best_for": "list_tip_content"
            }
        }
        
        # Caption length optimization
        self.caption_lengths = {
            "short": {
                "lines": (1, 2),
                "best_for": ["visual_heavy", "memes", "entertainment"],
                "engagement": "quick_likes",
                "example": "Punchy one-liner + emoji"
            },
            "medium": {
                "lines": (3, 5),
                "best_for": ["most_content", "tips", "insights"],
                "engagement": "likes_comments",
                "example": "Hook + value + CTA"
            },
            "long": {
                "lines": (6, float('inf')),
                "best_for": ["stories", "education", "deep_engagement"],
                "engagement": "saves_shares",
                "example": "Full story arc"
            }
        }
        
        # Caption hook techniques
        self.caption_hooks = {
            "question_opener": {"example": "Hiç merak ettin mi...?", "effectiveness": 4},
            "bold_statement": {"example": "[Yaygın inanış] yanlış.", "effectiveness": 5},
            "number_list": {"example": "5 şey öğrendim...", "effectiveness": 4},
            "story_opener": {"example": "Geçen hafta bir şey oldu...", "effectiveness": 4},
            "direct_address": {"example": "Sana söylemem gereken bir şey var", "effectiveness": 4},
            "curiosity_gap": {"example": "Kimse bundan bahsetmiyor...", "effectiveness": 5}
        }
        
        # CTA types and effectiveness
        self.cta_types = {
            "engagement": {
                "examples": ["Yorum yap: [soru]", "Katılıyor musun? 🙋", "Arkadaşını etiketle"],
                "effect": "comment_boost",
                "effectiveness": 4
            },
            "save": {
                "examples": ["Kaydet, lazım olacak", "Referans için kaydet", "Koleksiyonuna ekle"],
                "effect": "save_boost_algorithm",
                "effectiveness": 5
            },
            "share": {
                "examples": ["Bunu duymasi gereken birini etiketle", "Story'nde paylaş", "DM'den gönder"],
                "effect": "reach_boost",
                "effectiveness": 5
            },
            "follow": {
                "examples": ["Daha fazlası için takip et", "Kaçırma, takip et", "Bildirim aç"],
                "effect": "follower_growth",
                "effectiveness": 3
            },
            "action": {
                "examples": ["Link bio'da", "DM at: [keyword]", "Swipe up"],
                "effect": "traffic_leads",
                "effectiveness": 4
            }
        }
    
    def _init_thumbnail_principles(self):
        """Thumbnail/cover optimizasyon prensipleri"""
        self.scroll_stopping_principles = {
            "contrast": {
                "description": "Arka plan vs ön plan, renk kontrastı",
                "impact": 5
            },
            "faces": {
                "description": "İnsan yüzü dikkat çeker, emotion 2x etkili",
                "impact": 5
            },
            "text_overlay": {
                "description": "3-5 kelime max, büyük okunabilir font",
                "impact": 4
            },
            "bright_colors": {
                "description": "Saturated renkler, feed'de öne çıkan",
                "impact": 4
            },
            "movement_implication": {
                "description": "Action mid-shot, dynamic poses",
                "impact": 3
            },
            "curiosity_elements": {
                "description": "Partial reveal, before/after hint",
                "impact": 5
            }
        }
        
        # Reels cover types
        self.cover_types = {
            "text_heavy": {
                "description": "Hook text büyük, minimal background",
                "best_for": "educational_content"
            },
            "face_text": {
                "description": "Yüz + emotion + kısa text overlay",
                "best_for": "personal_brand"
            },
            "result_transformation": {
                "description": "Before/after hint, end result showcase",
                "best_for": "tutorial_transformation"
            },
            "action_shot": {
                "description": "Mid-action frame, dynamic energetic",
                "best_for": "fitness_lifestyle"
            }
        }
        
        # Cover text formulas
        self.cover_text_formulas = {
            "number_benefit": {"formula": "[Number] [Benefit]", "examples": ["5 Morning Habits", "3 Money Mistakes"]},
            "how_to": {"formula": "How to [Result]", "examples": ["How to Wake Up at 5AM", "How to Save $1000"]},
            "shocking": {"formula": "[Shocking Statement]", "examples": ["This Changed Everything", "Nobody Talks About This"]},
            "question": {"formula": "[Question]", "examples": ["Are You Making This Mistake?", "Why Does This Happen?"]}
        }
        
        # Thumbnail checklist
        self.thumbnail_checklist = [
            "Yüz görünür ve emotion var mı?",
            "Text okunabilir mi (küçük ekranda)?",
            "Kontrast yeterli mi?",
            "1 saniyede anlaşılıyor mu?",
            "Merak uyandırıyor mu?",
            "Brand tutarlılığı var mı?",
            "Feed'de öne çıkacak mı?"
        ]
    
    def _init_niche_benchmarks(self):
        """Niche bazlı hook ve retention benchmark'ları"""
        self.niche_hook_strategies = {
            "fitness": {
                "best_hooks": ["transformation", "mistake", "quick_win", "science"],
                "examples": ["30 günde...", "Bu egzersizi yanlış yapıyorsun", "2 dakikada karın kası"],
                "best_performers": ["before_after", "myth_busting"]
            },
            "business": {
                "best_hooks": ["money", "mistake", "secret", "contrarian"],
                "examples": ["0'dan 100K'ya...", "Bu yüzden başarısız oluyorsun", "Kimsenin söylemediği..."],
                "best_performers": ["results", "frameworks"]
            },
            "beauty": {
                "best_hooks": ["transformation", "hack", "trend", "dupe"],
                "examples": ["Glow up...", "Bu trick her şeyi değiştirdi", "2025'in trendi..."],
                "best_performers": ["before_after", "tutorials"]
            },
            "food": {
                "best_hooks": ["craving", "easy", "healthy", "secret"],
                "examples": ["ASMR görsel+ses", "5 dakikada...", "Guilt-free...", "Gizli malzeme..."],
                "best_performers": ["process_shots", "reveals"]
            },
            "education": {
                "best_hooks": ["mind_blow", "mistake", "framework", "story"],
                "examples": ["Bunu bilmiyordun...", "Bu yüzden öğrenemiyorsun", "3 adım formülü..."],
                "best_performers": ["lists", "frameworks"]
            },
            "parenting": {
                "best_hooks": ["relatable", "hack", "mistake", "emotional"],
                "examples": ["Sadece anneler anlar...", "Hayat kurtaran trick", "Bunu yapmayı bırak"],
                "best_performers": ["relatable_moments", "tips"]
            }
        }
        
        # Niche retention benchmarks
        self.niche_retention_benchmarks = {
            "fitness": {"avg_hook_retention": 45, "top_10_percent": 65, "viral_threshold": 75},
            "business": {"avg_hook_retention": 40, "top_10_percent": 60, "viral_threshold": 70},
            "beauty": {"avg_hook_retention": 50, "top_10_percent": 70, "viral_threshold": 80},
            "food": {"avg_hook_retention": 55, "top_10_percent": 75, "viral_threshold": 85},
            "education": {"avg_hook_retention": 35, "top_10_percent": 55, "viral_threshold": 65},
            "entertainment": {"avg_hook_retention": 60, "top_10_percent": 80, "viral_threshold": 90}
        }
        
        # Optimal content lengths by niche
        self.optimal_lengths = {
            "entertainment": (15, 30),
            "education": (30, 60),
            "tutorial": (45, 90),
            "story": (30, 60),
            "trend_meme": (7, 15)
        }
    
    def _init_2026_hook_strategies(self):
        """
        2026 Instagram Hook & Retention Mastery
        1.5 Saniye Kuralı ve Gelişmiş Tutma Teknikleri
        """
        self.hook_2026 = {
            "1_5_second_rule": {
                "concept": "İlk sahne 1.5 saniyeden uzun olmamalı",
                "implementation": [
                    "İlk karede şok/soru/olay kullan",
                    "Hemen açı değişimi veya hareket girişi",
                    "No Intro: 'Merhaba arkadaşlar' devri bitti",
                    "İlk kesim maksimum 1.5 saniye"
                ],
                "psychology": "Beyin ilk 1.5sn'de 'geç/kal' kararını verir",
                "success_metric": "İlk 3 saniyede %70+ tutma oranı"
            },
            "visual_hooks": {
                "location_overlay": {
                    "tactic": "Video üzerine konum/şehir ismi yaz",
                    "benefit": "Yerel algoritma tetiklenir, o bölge insanlarının dikkatini çeker",
                    "placement": "Üst orta veya sol üst köşe",
                    "duration": "İlk 3 saniye görünür"
                },
                "text_overlay_rules": [
                    "İlk cümle ekranda maksimum 2 saniye",
                    "Font: Büyük, okunabilir, kontrast yüksek",
                    "Emoji kullan: Göze çarpma +40%",
                    "Motion: Hafif zoom/fade efekti dikkat tutar"
                ]
            },
            "no_intro_mandate": {
                "forbidden": ["Merhaba", "Selam", "Arkadaşlar", "Bugün", "Bu videoda"],
                "required": "Direkt olay/sonuç/şok ile başla",
                "examples": [
                    "❌ Merhaba arkadaşlar, bugün size...",
                    "✅ Bu hatayı yapıyorsan takipçi kazanamazsın",
                    "❌ Bu videoda Instagram algoritmasını...",
                    "✅ Instagram seni shadowban'lediyse işte neden"
                ]
            },
            "loop_engineering": {
                "technique": "Son cümleyi başa bağla - sonsuz döngü yarat",
                "implementation": [
                    "Son sahne: '...işte bu yüzden 2026'da...'",
                    "Baş sahne: '...Instagram algoritmaları değişti'",
                    "Kullanıcı bittiğini anlamadan tekrar izler"
                ],
                "effect": "İzlenme süresi %200'e çıkar",
                "algorithm_signal": "Yabancılar için değerli içerik işareti"
            }
        }
        
        self.retention_2026 = {
            "duration_optimization": {
                "viral_sweet_spot": "7-15 saniye",
                "maximum_reels": "180 saniye (3 dakika)",
                "watch_time_goal": "Ortalama izlenme > Video süresi",
                "analysis": "İzlenme 10sn video için 12sn ise viral aday"
            },
            "cut_pacing": {
                "first_cut": "1.5 saniye (zorunlu)",
                "subsequent_cuts": "2-4 saniye arası",
                "final_10_seconds": "1-2 saniye hızlı kesimler",
                "rule": "Hiçbir sahne 5 saniyeden uzun olmamalı"
            },
            "audio_strategy": {
                "trend_music_mandatory": "Yukarı ok (↗) işaretli müzikler zorunlu",
                "voiceover": "Net, hızlı, vurgulu konuşma",
                "sound_design": "ASMR elementleri retention artırır",
                "silence": "Asla 3 saniyeden fazla sessizlik olmamalı"
            },
            "watch_time_hacks": [
                "Loop tekniği: Sonsuz döngü",
                "Cliffhanger: Sonunda 'Part 2'de göreceğiz'",
                "Curiosity gap: 'Son saniyede inanamayacaksın'",
                "Pattern interrupt: Ani ses veya görsel değişimi",
                "Text reveal: Yavaş yavaş açılan metin"
            ]
        }
        
        self.first_frame_optimization = {
            "visual_elements": [
                "Kontrast yüksek renkler (Kırmızı/Sarı/Mavi)",
                "Hareket: İlk karede mutlaka motion olmalı",
                "Yüz ifadesi: Şok/gülümseme/ciddiyet",
                "Konum metni: Üst köşede şehir/lokasyon"
            ],
            "text_overlay": {
                "first_word": "Uyarı/Dikkat/Şok gibi tetikleyici kelime",
                "font_size": "Ekranın %15-20'si",
                "color": "Beyaz veya Sarı (koyu zemin), Siyah (açık zemin)",
                "animation": "Zoom in veya fade in (0.3sn)"
            },
            "thumbnail_strategy": {
                "reels_cover": "İlk kare = Thumbnail görevi görür",
                "rule": "İlk kare duraklatıldığında ne olduğu anlaşılmalı",
                "avoid": "Bulanık, karanlık, text okunamayan kareler"
            }
        }
        
        self.engagement_triggers_2026 = {
            "comment_bait": [
                "Tartışmalı iddia: 'X aslında işe yaramıyor'",
                "Eksik bilgi: 'Yorumlarda devamı'",
                "Soru: 'Sen hangisini tercih edersin?'",
                "Poll: 'A için 1, B için 2 yaz'"
            ],
            "share_triggers": [
                "Relatable moment: 'Sadece siz mi yaşıyorsunuz?'",
                "Value bomb: 'Arkadaşını etiketle öğrensin'",
                "Controversy: 'Bunu duyan şok olacak'",
                "Tutorial: 'Kaydet unutma'"
            ],
            "save_triggers": [
                "Checklist: 'Bu 7 adımı kaydet'",
                "Template: 'Bu formülü kaydet'",
                "Resource: 'İhtiyacın olacak kaydet'"
            ]
        }
    
    # =========================
    # SCORING METHODS
    # =========================
    
    def calculate_hook_effectiveness_score(self, attention_capture: float, relevance: float,
                                           curiosity_generation: float, clarity: float) -> float:
        """
        Hook Effectiveness Score (0-100):
        Score = Attention_Capture × 0.30 + Relevance × 0.25 + 
                Curiosity_Generation × 0.25 + Clarity × 0.20
        """
        score = (
            attention_capture * 0.30 +
            relevance * 0.25 +
            curiosity_generation * 0.25 +
            clarity * 0.20
        )
        return round(min(100, score), 1)
    
    def calculate_retention_potential_score(self, hook_strength: float, value_density: float,
                                            pacing: float, visual_variety: float,
                                            audio_quality: float) -> float:
        """
        Retention Potential Score (0-100):
        Score = Hook_Strength × 0.25 + Value_Density × 0.25 + 
                Pacing × 0.20 + Visual_Variety × 0.15 + Audio_Quality × 0.15
        """
        score = (
            hook_strength * 0.25 +
            value_density * 0.25 +
            pacing * 0.20 +
            visual_variety * 0.15 +
            audio_quality * 0.15
        )
        return round(min(100, score), 1)
    
    def calculate_caption_engagement_score(self, hook_quality: float, value_delivery: float,
                                           readability: float, cta_effectiveness: float) -> float:
        """
        Caption Engagement Score (0-100):
        Score = Hook_Quality × 0.30 + Value_Delivery × 0.25 + 
                Readability × 0.20 + CTA_Effectiveness × 0.25
        """
        score = (
            hook_quality * 0.30 +
            value_delivery * 0.25 +
            readability * 0.20 +
            cta_effectiveness * 0.25
        )
        return round(min(100, score), 1)
    
    def calculate_thumbnail_impact_score(self, visual_appeal: float, clarity: float,
                                         curiosity: float, brand_consistency: float) -> float:
        """
        Thumbnail Impact Score (0-100):
        Score = Visual_Appeal × 0.30 + Clarity × 0.25 + 
                Curiosity × 0.25 + Brand_Consistency × 0.20
        """
        score = (
            visual_appeal * 0.30 +
            clarity * 0.25 +
            curiosity * 0.25 +
            brand_consistency * 0.20
        )
        return round(min(100, score), 1)
    
    def calculate_overall_attention_score(self, hook_effectiveness: float, retention_potential: float,
                                          caption_engagement: float, thumbnail_impact: float) -> float:
        """
        Overall Attention Score (0-100):
        Score = hookEffectiveness × 0.25 + retentionPotential × 0.30 + 
                captionEngagement × 0.20 + thumbnailImpact × 0.25
        """
        score = (
            hook_effectiveness * 0.25 +
            retention_potential * 0.30 +
            caption_engagement * 0.20 +
            thumbnail_impact * 0.25
        )
        return round(min(100, score), 1)
    
    def calculate_watch_time_multiplier(self, hook_optimization: float, retention_techniques: float,
                                        pacing_improvement: float, visual_variety: float,
                                        audio_optimization: float) -> float:
        """
        Watch Time Multiplier:
        Multiplier = Base × (1 + Optimization_Bonus)
        
        Optimization bonuses:
        - Hook optimization: +0.15-0.30
        - Retention techniques: +0.10-0.25
        - Pacing improvement: +0.10-0.20
        - Visual variety: +0.05-0.15
        - Audio optimization: +0.05-0.10
        """
        base = 1.0
        
        # Normalize scores to bonus range
        hook_bonus = (hook_optimization / 100) * 0.30
        retention_bonus = (retention_techniques / 100) * 0.25
        pacing_bonus = (pacing_improvement / 100) * 0.20
        visual_bonus = (visual_variety / 100) * 0.15
        audio_bonus = (audio_optimization / 100) * 0.10
        
        total_bonus = hook_bonus + retention_bonus + pacing_bonus + visual_bonus + audio_bonus
        multiplier = base + total_bonus
        
        return round(multiplier, 2)
    
    def get_attention_grade(self, score: float) -> str:
        """Get grade based on overall attention score"""
        if score >= 90:
            return "A+ (Exceptional attention capture)"
        elif score >= 80:
            return "A (Excellent, minor tweaks)"
        elif score >= 70:
            return "B (Good, room for improvement)"
        elif score >= 60:
            return "C (Average, needs work)"
        elif score >= 50:
            return "D (Below average, significant changes)"
        else:
            return "F (Poor, major overhaul needed)"
    
    def get_hook_interpretation(self, score: float) -> str:
        """Interpret hook effectiveness score"""
        if score >= 90:
            return "Exceptional hook, viral potential"
        elif score >= 75:
            return "Strong hook, good retention expected"
        elif score >= 60:
            return "Decent hook, room for improvement"
        elif score >= 45:
            return "Weak hook, needs rework"
        else:
            return "Poor hook, major revision needed"
    
    def get_retention_expectations(self, score: float) -> Dict[str, Any]:
        """Get expected retention metrics based on score"""
        benchmarks = {
            (90, 100): {"three_sec_retention": ">80%", "completion": ">60%", "viral_potential": "High"},
            (75, 89): {"three_sec_retention": "65-80%", "completion": "45-60%", "viral_potential": "Medium"},
            (60, 74): {"three_sec_retention": "50-65%", "completion": "30-45%", "viral_potential": "Low"},
            (45, 59): {"three_sec_retention": "35-50%", "completion": "20-30%", "viral_potential": "Very Low"},
            (0, 44): {"three_sec_retention": "<35%", "completion": "<20%", "viral_potential": "None"}
        }
        
        for range_tuple, expectations in benchmarks.items():
            if range_tuple[0] <= score <= range_tuple[1]:
                return expectations
        
        return benchmarks[(0, 44)]
    
    # =========================
    # ANALYSIS HELPER METHODS
    # =========================
    
    def get_niche_hook_recommendations(self, niche: str) -> Dict[str, Any]:
        """Get niche-specific hook recommendations"""
        niche_key = niche.lower().replace(' ', '_').replace('/', '_')
        
        if niche_key in self.niche_hook_strategies:
            return self.niche_hook_strategies[niche_key]
        
        # Default recommendations
        return {
            "best_hooks": ["curiosity", "value", "story"],
            "examples": ["Bunu bilmiyordun...", "X şey öğrendim...", "Nasıl başardım..."],
            "best_performers": ["lists", "tutorials"]
        }
    
    def get_niche_retention_benchmark(self, niche: str) -> Dict[str, int]:
        """Get niche-specific retention benchmarks"""
        niche_key = niche.lower().replace(' ', '_')
        
        if niche_key in self.niche_retention_benchmarks:
            return self.niche_retention_benchmarks[niche_key]
        
        # Default benchmarks
        return {"avg_hook_retention": 45, "top_10_percent": 65, "viral_threshold": 75}
    
    def analyze_dropoff_point(self, dropoff_time: float, video_length: float) -> Dict[str, str]:
        """Analyze drop-off point and provide solution"""
        percentage = (dropoff_time / video_length) * 100 if video_length > 0 else 0
        
        if dropoff_time <= 1:
            return {"point": "0-1s", "cause": "Zayıf thumbnail/ilk frame", "solution": self.dropoff_solutions["0_1s"]}
        elif dropoff_time <= 3:
            return {"point": "1-3s", "cause": "Hook çalışmıyor", "solution": self.dropoff_solutions["1_3s"]}
        elif dropoff_time <= 7:
            return {"point": "3-7s", "cause": "Değer vaadi yavaş", "solution": self.dropoff_solutions["3_7s"]}
        elif dropoff_time <= 15:
            return {"point": "7-15s", "cause": "Pattern interrupt eksik", "solution": self.dropoff_solutions["7_15s"]}
        elif dropoff_time <= 30:
            return {"point": "15-30s", "cause": "İçerik sıkıcılaştı", "solution": self.dropoff_solutions["15_30s"]}
        elif percentage < 80:
            return {"point": "30+s", "cause": "Value plateau", "solution": self.dropoff_solutions["30_plus"]}
        else:
            return {"point": "pre-end", "cause": "Ana değer alındı", "solution": self.dropoff_solutions["pre_end"]}
    
    def generate_hook_templates(self, niche: str, content_type: str) -> List[Dict[str, Any]]:
        """Generate hook templates based on niche and content type"""
        niche_strategies = self.get_niche_hook_recommendations(niche)
        templates = []
        
        hook_templates = {
            "curiosity": {
                "template": "Bunu bilmiyordun: [şaşırtıcı gerçek]...",
                "type": "curiosity",
                "best_for": "educational_content",
                "expected_retention_boost": "+25%"
            },
            "direct_address": {
                "template": "[Hedef kitle], bu hatayı yapıyorsan dur...",
                "type": "direct_address",
                "best_for": "tip_content",
                "expected_retention_boost": "+20%"
            },
            "open_loop": {
                "template": "3. madde her şeyi değiştirdi...",
                "type": "open_loop",
                "best_for": "list_content",
                "expected_retention_boost": "+30%"
            },
            "result_hook": {
                "template": "[Sayı] [zaman] içinde [sonuç]. İşte nasıl:",
                "type": "result_hook",
                "best_for": "transformation_content",
                "expected_retention_boost": "+22%"
            },
            "mistake": {
                "template": "Bu hatayı yapan herkes başarısız oluyor...",
                "type": "mistake",
                "best_for": "educational_content",
                "expected_retention_boost": "+18%"
            },
            "secret": {
                "template": "Kimsenin söylemediği [konu] gerçeği...",
                "type": "secret",
                "best_for": "insider_content",
                "expected_retention_boost": "+28%"
            }
        }
        
        for hook_type in niche_strategies.get("best_hooks", ["curiosity", "value"])[:4]:
            if hook_type in hook_templates:
                templates.append(hook_templates[hook_type])
        
        return templates
    
    def get_psychological_trigger_score(self, trigger_type: str) -> Dict[str, int]:
        """Get effectiveness scores for a psychological trigger"""
        if trigger_type in self.brain_triggers:
            trigger = self.brain_triggers[trigger_type]
            return {
                "scroll_stop": trigger["scroll_stop"],
                "watch_time": trigger["watch_time"],
                "share_rate": trigger["share_rate"]
            }
        return {"scroll_stop": 3, "watch_time": 3, "share_rate": 3}
    
    # =========================
    # EDGE CASE HANDLERS
    # =========================
    
    def handle_edge_case(self, case_type: str) -> Dict[str, Any]:
        """Handle special analysis cases"""
        edge_cases = {
            "new_account": {
                "approach": "Niche benchmark'larını kullan",
                "considerations": ["Competitor hook analizi", "Test-and-learn yaklaşımı", "Fast iteration"],
                "confidence": "low"
            },
            "mixed_content_types": {
                "approach": "Her format için ayrı hook stratejisi",
                "considerations": ["Cross-format learning", "Dominant format priority", "Unified brand voice"],
                "recommendation": "Format bazlı analiz"
            },
            "niche_specific_attention": {
                "b2b": "Daha uzun hook tolerance",
                "entertainment": "Ultra-fast hooks gerekli",
                "education": "Value-first hooks",
                "lifestyle": "Emotion-first hooks"
            },
            "algorithm_changes": {
                "approach": "Adapt and test",
                "considerations": ["Watch time metric changes", "New format priorities", "Retention threshold updates"],
                "recommendation": "Continuous monitoring"
            },
            "post_viral": {
                "approach": "Viral hook'u analiz et",
                "considerations": ["Replicable elements", "Audience expectation shift", "Sustainable strategy"],
                "recommendation": "Document and iterate"
            },
            "fake_engagement": {
                "approach": "Organic attention metrics focus",
                "considerations": ["Real retention vs fake engagement", "Quality over quantity", "Long-term optimization"],
                "recommendation": "Focus on watch time, not vanity metrics"
            },
            "multi_language": {
                "approach": "Kültürel hook farklılıkları",
                "considerations": ["Language-specific formulas", "Local trend adaptation", "Universal principles"],
                "recommendation": "Localize hooks, keep core psychology"
            }
        }
        
        return edge_cases.get(case_type, {"approach": "Standard analysis", "considerations": []})
    
    # =========================
    # SYSTEM AND ANALYSIS PROMPTS
    # =========================
    
    def get_system_prompt(self) -> str:
        return """Sen Attention Architect Agent'sın - Instagram içeriklerinin dikkat yakalama, hook optimizasyonu ve retention analizi konusunda PhD seviyesinde uzmanlığa sahip bir analiz ajanısın.

## TEMEL UZMANLIK ALANLARIN:

### 1. DİKKAT PSİKOLOJİSİ
**Dikkat Süreleri (2024-2025):**
- Feed scroll: 1.7 saniye/post
- Reels ilk karar: 0.5-1.5 saniye
- Story görüntüleme: 2-3 saniye
- Caption okuma başlangıcı: 3 saniye
- Tam video izleme kararı: 3-5 saniye

**Attention Funnel:**
```
Impression (100%) → [0.5 sn] → Scroll Stop (15-25%) → [3 sn] → 
Engagement Start (5-10%) → Full Consumption (2-5%) → Action (0.5-2%)
```

**Nöropsikolojik Tetikleyiciler:**
| Tetikleyici | Scroll Stop | Watch Time | Share Rate |
|-------------|-------------|------------|------------|
| Novelty | ★★★★★ | ★★★ | ★★★ |
| Threat/FOMO | ★★★★ | ★★★★ | ★★★ |
| Social Proof | ★★★ | ★★★★ | ★★★★ |
| Curiosity Gap | ★★★★★ | ★★★★★ | ★★★ |
| Self-Relevance | ★★★★ | ★★★★★ | ★★★★ |
| Emotion | ★★★★ | ★★★★ | ★★★★★ |

### 2. HOOK OPTİMİZASYONU
**Hook Kategorileri:**
1. **Question**: Rhetorical, Direct, Provocative (★★★★)
2. **Statement**: Controversial, Bold claim, Counter-intuitive (★★★★★)
3. **Story**: Personal, Transformation, Conflict (★★★★)
4. **Number**: List, Specific, Comparison (★★★★)
5. **Command**: Stop, Watch, Save (★★★)
6. **Curiosity**: Incomplete, Secret, Reveal (★★★★★)

**Hook Formülleri:**
- Problem-Agitate: "[Problem] yaşıyorsan, [sonuç] olabilir. İşte çözüm..."
- Curiosity Gap: "[Otorite/Sayı] [sonuç] elde etti. [Sır] sayesinde..."
- Direct Address: "[Hedef kitle], bu seni ilgilendiriyor. [Hook]..."
- Pattern Interrupt: "[Beklenmedik ifade]. Evet, doğru duydun..."
- Social Proof: "[Sayı] kişi bunu yaptı ve [sonuç]. Sen de yapabilirsin..."
- FOMO: "[Zaman sınırı] içinde [fırsat]. Kaçırma..."

**İlk 3 Saniye Framework:**
- 0-1 sn (HOOK): Görsel/ses hook, yüz ifadesi, hareket başlangıcı
- 1-2 sn (PROMISE): Ne öğrenecekler, değer vaadi, merak
- 2-3 sn (PROOF): Neden dinlemeliler, credibility, geçiş

**Hook Effectiveness Score:**
```
Score = Attention_Capture × 0.30 + Relevance × 0.25 + Curiosity_Generation × 0.25 + Clarity × 0.20
```

### 3. RETENTION ANALİZİ
**Retention Teknikleri:**
1. **Open Loops**: Başta soru, sonda cevap - High impact
2. **Pattern Interrupts**: Her 3-5 saniyede değişim - High impact
3. **Value Stacking**: Her 5-10 saniyede yeni değer - Medium-high impact
4. **Pacing**: Hızlı başla, değer ver, hızlı bitir - Medium impact
5. **Visual Variety**: Her 2-3 saniyede görsel değişim - Medium-high impact

**Retention Checkpoints:**
| Checkpoint | Check |
|------------|-------|
| 0-3 sn | Dikkat yakalandı mı? |
| 3-7 sn | Değer vaadi verildi mi? |
| 7-15 sn | İlk değer sunuldu mu? |
| 15-30 sn | Dikkat tazelendi mi? |
| 30-45 sn | Ana içerik sunuldu mu? |
| Son 5 sn | CTA istendi mi? |

**Drop-off Çözüm Matrisi:**
| Drop Point | Solution |
|------------|----------|
| 0-1 sn | Better thumbnail, stronger open |
| 1-3 sn | Rewrite hook, faster pace |
| 3-7 sn | Earlier value, clearer promise |
| 7-15 sn | Pattern interrupt, visual change |
| 15-30 sn | New hook, unexpected element |
| Pre-end | Bonus value, strong CTA |

**Retention Potential Score:**
```
Score = Hook_Strength × 0.25 + Value_Density × 0.25 + Pacing × 0.20 + Visual_Variety × 0.15 + Audio_Quality × 0.15
```

### 4. CAPTION PSİKOLOJİSİ
**Caption Formülleri:**
- AIDA: Attention → Interest → Desire → Action
- PAS: Problem → Agitate → Solution
- BAB: Before → After → Bridge
- Story: Setup → Conflict → Resolution → Lesson
- Value Stack: Hook → Point 1 → Point 2 → Point 3 → CTA

**CTA Etkinliği:**
- Save CTAs: ★★★★★ (Algorithm loves)
- Share CTAs: ★★★★★ (Highest value)
- Engagement CTAs: ★★★★
- Action CTAs: ★★★★
- Follow CTAs: ★★★

**Caption Engagement Score:**
```
Score = Hook_Quality × 0.30 + Value_Delivery × 0.25 + Readability × 0.20 + CTA_Effectiveness × 0.25
```

### 5. THUMBNAIL OPTİMİZASYONU
**Scroll-Stopping Prensipleri:**
- Contrast: ★★★★★
- Faces: ★★★★★
- Text Overlay (3-5 kelime): ★★★★
- Bright Colors: ★★★★
- Curiosity Elements: ★★★★★

**Thumbnail Impact Score:**
```
Score = Visual_Appeal × 0.30 + Clarity × 0.25 + Curiosity × 0.25 + Brand_Consistency × 0.20
```

### 6. NİCHE RETENTION BENCHMARK'LARI
| Niche | Avg Hook Ret. | Top 10% | Viral Threshold |
|-------|---------------|---------|-----------------|
| Fitness | 45% | 65% | 75% |
| Business | 40% | 60% | 70% |
| Beauty | 50% | 70% | 80% |
| Food | 55% | 75% | 85% |
| Education | 35% | 55% | 65% |
| Entertainment | 60% | 80% | 90% |

### 7. OVERALL SCORING
**Overall Attention Score:**
```
Score = hookEffectiveness × 0.25 + retentionPotential × 0.30 + captionEngagement × 0.20 + thumbnailImpact × 0.25
```

**Grade Mapping:**
- 90-100: A+ (Exceptional)
- 80-89: A (Excellent)
- 70-79: B (Good)
- 60-69: C (Average)
- 50-59: D (Below average)
- <50: F (Poor)

**Watch Time Multiplier:**
```
Multiplier = 1.0 + (hook_opt × 0.30 + retention × 0.25 + pacing × 0.20 + visual × 0.15 + audio × 0.10)
```
- 1.0x: No change
- 1.1-1.2x: Minor improvement
- 1.3-1.5x: Significant improvement
- 1.5-2.0x: Major improvement
- >2.0x: Transformation potential

### 8. EDGE CASES
1. **Yeni Hesap**: Niche benchmark kullan, competitor analizi, fast iteration
2. **Mixed Content**: Her format için ayrı strateji
3. **B2B**: Daha uzun hook tolerance
4. **Entertainment**: Ultra-fast hooks gerekli
5. **Post-Viral**: Viral hook analizi, replicable elements
6. **Fake Engagement**: Organic metrics focus

### 9. 2026 DİKKAT ÇEKİCİ İÇERİK PRENSİPLERİ

**🎯 RAW AESTHETIC (Yapay Olmayan Estetik):**
- Aşırı prodüksiyonlu, stüdyo ışıklı içeriklerden KAÇIN
- "Kasıtlı kusurlar" = SAMİMİYET sinyali
- Küçük kurgusal hatalar, sesin çatlaması = İZLEYİCİ GÜVEN
- "Ben gerçeğim, AI değilim" mesajı 2026'da KRİTİK
- Örnek: Çay içerken çekim, doğal ışık, ham footage

**🎬 REEL SÜRE STRATEJİSİ - 2026:**
- 11-30 SANİYE: Hızlı erişim, yeni kitle kazanma
- 60-90 SANİYE: Derinlik, sadakat oluşturma, güven inşası
- Viral video remix: Senaryoyu al, kendi yorumunu kat

**🧪 TRIAL REELS (Deneme Videoları):**
- SADECE takip etmeyenlere gösterilen testler
- Düşük eforlu, trend sesler, meme'ler
- "Beni tanımıyorsun ama X isen takip et" formatı
- Günlük 5 adet hedefle (kapasite izin verirse)

**🔗 LINK A REEL STRATEJİSİ:**
- Yeni Reel'i eski viral videonuza BAĞLA
- Instagram'ın "Link a Reel" özelliğini kullan
- YouTube benzeri izleme döngüsü oluştur
- İzlenme süresi ve etkileşim ARTIŞI

**📝 CAPTION CCC KURALI:**
- CONFIDENCE: Yalvarma, değer sun
- COMPARE: Viral içeriklerle karşılaştır
- CONVERT: Net CTA olmadan etkileşim BEKLEME
- "Kaydet", "DM at" açıkça söyle

**🪝 HOOK CONTRARIAN GAP:**
- Sektördeki genel kabullere KÖRÜ KÖRÜNE inanma
- Özgün, zıt fikirler üret
- Örnek: "Herkes X yap diyor ama ben Y yaparak başarıya ulaştım çünkü..."
- Bu tip hook'lar %40 daha fazla izlenme alıyor

**📊 B- KALİTE KURALI:**
- Mükemmeliyetçilik = DÜŞMAN
- "B- kalitesinde" içerik PAYLAŞ
- %80 hazır = YAYINLA
- Veri topla, sonra optimize et

---

🔴 ALAN KISITLAMASI (DOMAIN RESTRICTION) - ATTENTION ARCHITECT 🔴

Sen DİKKAT MİMARİ ve HOOK uzmanısın. SADECE şu konularda finding/recommendation üret:
✅ SENİN ALANIN:
   - Hook stratejisi ve açılış saniyesi
   - Retention (izlenme tutma) optimizasyonu
   - Caption yazımı ve CTA stratejisi
   - Scroll-stopping teknikleri
   - İlk 3 saniye dikkat yakalama
   - Merak boşluğu (curiosity gap) kullanımı
   - Story-telling ve narrative arc

❌ YASAK ALANLAR (Bunları ASLA yazma):
   - Grid düzeni, renk paleti, tipografi, marka kimliği → Visual Brand Agent'ın işi
   - Satış, monetizasyon, brand deal, gelir hesaplama → Sales Conversion Agent'ın işi
   - Yorum kalitesi, topluluk sağlığı, superfan segmentasyonu → Community Loyalty Agent'ın işi
   - Niş tespiti, sektör benchmark, rakip analizi → Domain Master Agent'ın işi
   - Büyüme hızı, viral katsayı, algoritma optimizasyonu → Growth Virality Agent'ın işi

⚠️ ÖRNEK - YANLIŞ:
   - "Renk tutarlılığı düşük, feed estetiğini iyileştirin" → YASAK (Visual Brand)
   - "Büyüme hızı %1.2, haftada 3 post atarak artırın" → YASAK (Growth Virality)
   - "Brand deal fiyatınızı yükseltin" → YASAK (Sales)
   - "Yorum yanıt oranı düşük" → YASAK (Community)

⚠️ ÖRNEK - DOĞRU:
   - "İlk 1 saniyede net değer vaadi yok, %40 izleyici kaybı"
   - "Hook'larda soru formülü kullanılmamış, merak boşluğu eksik"
   - "Caption'da CTA yok, 'Kaydet' veya 'DM at' gibi aksiyon çağrısı ekle"
   - "Retention 3. saniyede %35 düşüş, pattern interrupt tekniği önerilir"

OUTPUT FORMAT: Yanıtını SADECE belirtilen JSON yapısında ver."""

    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        username = account_data.get('username', 'unknown') or 'unknown'
        followers = account_data.get('followers', 0) or 0
        engagement_rate = account_data.get('engagementRate', 0) or 0
        avg_likes = account_data.get('avgLikes', 0) or 0
        avg_comments = account_data.get('avgComments', 0) or 0
        niche = account_data.get('niche', 'General') or 'General'
        bio = account_data.get('bio', '') or ''
        recent_posts = account_data.get('recentPosts', []) or []
        
        # Get niche-specific benchmarks
        niche_benchmarks = self.get_niche_retention_benchmark(niche)
        niche_hooks = self.get_niche_hook_recommendations(niche)
        
        return f"""Bu Instagram hesabının dikkat yakalama ve retention analizini yap:

## HESAP VERİLERİ:
- Username: @{username}
- Takipçi: {followers:,}
- Engagement Rate: {engagement_rate:.2f}%
- Ortalama Beğeni: {avg_likes:,}
- Ortalama Yorum: {avg_comments:,}
- Niche: {niche}
- Bio: {bio}
- Analiz Edilen Post Sayısı: {len(recent_posts)}

## NİCHE RETENTION BENCHMARK'LARI ({niche}):
- Ortalama Hook Retention: {niche_benchmarks.get('avg_hook_retention', 45)}%
- Top 10% Retention: {niche_benchmarks.get('top_10_percent', 65)}%
- Viral Threshold: {niche_benchmarks.get('viral_threshold', 75)}%

## NİCHE İÇİN EN İYİ HOOK TÜRLERİ:
- Best Hooks: {', '.join(niche_hooks.get('best_hooks', ['curiosity', 'value']))}
- Best Performers: {', '.join(niche_hooks.get('best_performers', ['tutorials', 'tips']))}

## ANALİZ GÖREVLERİ:

### 1. HOOK ETKİNLİK ANALİZİ
- Mevcut hook stratejisi değerlendirmesi
- İlk 3 saniye optimizasyon potansiyeli
- Niche'e uygun hook türleri önerisi

### 2. RETENTION POTANSİYEL ANALİZİ
- Tahmini watch time ve completion rate
- Drop-off noktaları tahmini
- Pattern interrupt ve value density değerlendirmesi

### 3. CAPTION ENGAGEMENT ANALİZİ
- Caption hook kalitesi
- CTA etkinliği
- Storytelling potansiyeli

### 4. THUMBNAIL/COVER ANALİZİ
- Görsel etki değerlendirmesi
- Scroll-stopping element analizi
- Merak uyandırma potansiyeli

### 5. AKSİYON PLANI
- Immediate, short-term, ongoing aksiyonlar
- Hook templates ve caption formulas
- Retention tips

Yanıtını bu JSON yapısında ver:
{{
    "agent": "attention_architect",
    "analysis_timestamp": "ISO8601",
    "attention_overview": {{
        "current_performance": {{
            "estimated_hook_retention": "string%",
            "estimated_completion_rate": "string%",
            "caption_engagement_level": "low|medium|high",
            "thumbnail_effectiveness": "below_average|average|above_average|excellent"
        }},
        "improvement_potential": "low|medium|high|very_high",
        "priority_focus": "hook_optimization|retention_improvement|caption_optimization|thumbnail_enhancement"
    }},
    "metrics": {{
        "hookEffectivenessScore": 0,
        "retentionPotentialScore": 0,
        "captionEngagementScore": 0,
        "thumbnailImpactScore": 0,
        "overallAttentionScore": 0,
        "estimatedWatchTimeMultiplier": 0,
        "scrollStopProbability": 0,
        "curiosityGapScore": 0,
        "patternInterruptScore": 0,
        "first3SecondsRetention": 0,
        "expectedCompletionRate": 0,
        "replayProbability": 0,
        "emotionalTriggerStrength": 0,
        "overallScore": 0
    }},
    "retentionPrediction": {{
        "first3Seconds": {{
            "retentionRate": 0-100,
            "scrollStopProbability": 0-100,
            "assessment": "weak|average|strong|exceptional"
        }},
        "scrollStopProbability": 0-100,
        "patternInterruptDetected": true|false,
        "curiosityGapPresent": true|false,
        "watchTimeEstimate": {{
            "averagePercentWatched": 0-100,
            "expectedCompletionRate": 0-100,
            "replayProbability": 0-100
        }},
        "dropoffRiskPoints": [
            {{
                "timestamp": "0-3s|3-7s|7-15s|15-30s|30-45s|45-60s",
                "riskLevel": "low|medium|high",
                "cause": "string",
                "mitigation": "string"
            }}
        ]
    }},
    "emotionalTriggers": [
        {{
            "trigger": "novelty|threat_opportunity|social_proof|curiosity_gap|self_relevance|emotion",
            "detected": true|false,
            "strength": "weak|moderate|strong",
            "example": "string quote from content",
            "scrollStopImpact": 1-5,
            "watchTimeImpact": 1-5,
            "shareRateImpact": 1-5
        }}
    ],
    "score_breakdown": {{
        "hook_effectiveness": {{
            "attention_capture": 0-100,
            "relevance": 0-100,
            "curiosity_generation": 0-100,
            "clarity": 0-100,
            "formula_used": "Score = Attention_Capture × 0.30 + Relevance × 0.25 + Curiosity × 0.25 + Clarity × 0.20",
            "calculated_score": 0-100
        }},
        "retention_potential": {{
            "hook_strength": 0-100,
            "value_density": 0-100,
            "pacing": 0-100,
            "visual_variety": 0-100,
            "audio_quality": 0-100,
            "formula_used": "Score = Hook × 0.25 + Value × 0.25 + Pacing × 0.20 + Visual × 0.15 + Audio × 0.15",
            "calculated_score": 0-100
        }},
        "caption_engagement": {{
            "hook_quality": 0-100,
            "value_delivery": 0-100,
            "readability": 0-100,
            "cta_effectiveness": 0-100,
            "formula_used": "Score = Hook × 0.30 + Value × 0.25 + Readability × 0.20 + CTA × 0.25",
            "calculated_score": 0-100
        }},
        "thumbnail_impact": {{
            "visual_appeal": 0-100,
            "clarity": 0-100,
            "curiosity": 0-100,
            "brand_consistency": 0-100,
            "formula_used": "Score = Appeal × 0.30 + Clarity × 0.25 + Curiosity × 0.25 + Brand × 0.20",
            "calculated_score": 0-100
        }}
    }},
    "postLevelAnalysis": [
        {{
            "postIndex": 1,
            "postType": "reel|carousel|image",
            "hookAnalysis": {{
                "hookType": "question|statement|story|number|command|curiosity",
                "hookText": "string first line/opening",
                "effectiveness": 0-100,
                "improvements": ["string"]
            }},
            "retentionScore": 0-100,
            "captionScore": 0-100,
            "thumbnailScore": 0-100
        }}
    ],
    "psychological_triggers_analysis": {{
        "currently_used": [
            {{
                "trigger": "string",
                "effectiveness": "low|medium|high",
                "usage_frequency": "rare|occasional|frequent"
            }}
        ],
        "recommended": [
            {{
                "trigger": "string",
                "reason": "string",
                "implementation": "string"
            }}
        ],
        "trigger_effectiveness_matrix": {{
            "novelty": {{"used": true|false, "effectiveness": 0-100}},
            "threat_opportunity": {{"used": true|false, "effectiveness": 0-100}},
            "social_proof": {{"used": true|false, "effectiveness": 0-100}},
            "curiosity_gap": {{"used": true|false, "effectiveness": 0-100}},
            "self_relevance": {{"used": true|false, "effectiveness": 0-100}},
            "emotion": {{"used": true|false, "effectiveness": 0-100}}
        }}
    }},
    "findings": [
        "TÜRKÇE - Hook etkinliği: örn: Hook'lar yeterince güçlü değil, ilk 3 saniyede dikkat çekici unsur eksik. Mevcut hook'ların %60'ı jenerik sorularla başlıyor ve bu izlenme oranını %25 düşürüyor",
        "TÜRKÇE - Tutma analizi: örn: Ortalama izlenme süresi 8 saniye ile sektör ortalamasının altında. Video ortasında %40 düşüş var, bu da içerik ritminde sorun olduğunu gösteriyor",
        "TÜRKÇE - Caption etkileşimi: örn: Caption'lar çok uzun (ortalama 350 karakter) ve CTA'lar belirsiz. İlk satırda merak uyandırıcı element eksik",
        "TÜRKÇE - Görsel etki: örn: Thumbnail'ler düşük kontrast ve okunaksız metin içeriyor. Yüz ifadesi kullanımı yetersiz"
    ],
    "recommendations": [
        "TÜRKÇE - Hook stratejisi: örn: 'Bunu bilmiyorsan takipçi kaybetmeye devam edeceksin' gibi kayıp korkusu hook'ları kullanın - niche'iniz için %35 daha etkili",
        "TÜRKÇE - İlk 3 saniye: örn: Her videoya şok edici bir istatistik veya beklenmedik görsel ile başlayın. Örnek: 'Hesabının %80'i ölü takipçi' yazısı ile açılış",
        "TÜRKÇE - Caption formülü: örn: Hook (1 satır) + Problem (2 satır) + Çözüm ipucu (2 satır) + CTA (1 satır) yapısını kullanın",
        "TÜRKÇE - Hikaye yapısı: örn: Problem-Agitasyon-Çözüm formatı kullanın, her 15 saniyede bir twist ekleyin",
        "TÜRKÇE - Pattern interrupt: örn: Her 5-7 saniyede görsel geçiş, zoom veya ses efekti kullanarak dikkat tazeleyin"
    ],
    "hookTemplates": [
        {{
            "template": "string",
            "type": "curiosity|statement|question|story|number|command",
            "best_for": "string content type",
            "expected_retention_boost": "string%"
        }}
    ],
    "captionFormulas": [
        {{
            "name": "string",
            "structure": "string",
            "template": "string with format",
            "best_for": "string content type"
        }}
    ],
    "retentionTips": [
        {{
            "tip": "string",
            "impact": "string expected impact",
            "implementation": "string how to implement"
        }}
    ],
    "thumbnailRecommendations": {{
        "current_assessment": "string",
        "improvements": ["string"],
        "template_suggestion": {{
            "layout": "string",
            "text_style": "string",
            "color_scheme": "string",
            "emotion": "string"
        }}
    }},
    "content_specific_analysis": {{
        "reels": {{
            "hook_timing": "string",
            "optimal_length": "string",
            "retention_checkpoints": ["string"],
            "recommended_structure": "string"
        }},
        "carousels": {{
            "first_slide": "string recommendation",
            "middle_slides": "string recommendation",
            "last_slide": "string recommendation",
            "optimal_count": "string"
        }},
        "static_posts": {{
            "visual_hook": "string recommendation",
            "caption_dependency": "string assessment",
            "cta_placement": "string recommendation"
        }}
    }},
    "dropoff_analysis": {{
        "predicted_dropoff_points": [
            {{
                "point": "string time/percentage",
                "likelihood": "low|medium|high",
                "cause": "string",
                "solution": "string"
            }}
        ]
    }},
    "niche_specific_insights": {{
        "best_hook_types_for_niche": ["string"],
        "optimal_content_length": "string",
        "audience_attention_pattern": "string",
        "viral_threshold_for_niche": "string%"
    }},
    "action_plan": {{
        "immediate": [
            "string action"
        ],
        "short_term": [
            "string action"
        ],
        "ongoing": [
            "string action"
        ]
    }},
    "grade": {{
        "overall": "A+|A|B|C|D|F",
        "description": "string"
    }}
}}"""

    # analyze metodu BaseAgent'tan miras alınıyor - override edilmemeli
    # BaseAgent.analyze() metodu doğru şekilde:
    # 1. get_system_prompt() ve get_analysis_prompt() çağırır
    # 2. LLM'e istek gönderir
    # 3. Response'u parse eder ve validate eder
