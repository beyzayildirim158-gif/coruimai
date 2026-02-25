# ELI5 Formatter Agent - Explain Like I'm 5
# Converts technical PhD-level reports to simple, actionable language
"""
ELI5 Formatter Agent

Bu ajan teknik PhD seviyesindeki raporları:
- [KUSUR] + [APTALA ANLATIR GİBİ] + [AKSİYON] formatına çevirir
- Hook'ları psikolojik tetikleyicilerle yeniden yazar
- Acımasız ama aksiyon odaklı geri bildirim verir
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import json
import re


class ELI5FormatterAgent(BaseAgent):
    """
    ELI5 Formatter Agent
    
    Role: Convert technical analysis to brutally honest, actionable language
    
    Output Format:
    [KUSUR]: Teknik bulgu (kısa ve sert)
    [APTALA ANLATIR GİBİ]: Metafor ile açıklama (herkes anlasın)
    [AKSİYON]: Net komut (YAPIN dil ile)
    """
    
    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "ELI5 Formatter"
        self.role = "Simple Language & Hook Writer"
        self.specialty = "Translating complex analysis to actionable insights"
        
        # Hook psikoloji tetikleyicileri
        self._init_hook_psychology()
    
    def _init_hook_psychology(self):
        """Hook yazımı için psikolojik tetikleyiciler"""
        
        # 🗣️ GÖREV 3: TEKNİK TERİM HUMANİZASYONU
        self.technical_term_humanization = {
            # Teknik Terim: Sohbet Dili Karşılığı
            "viral coefficient": "Videolarını arkadaşlarına gönderme oranı",
            "viral_coefficient": "İnsanlar senin videolarını kaç kişiye gönderiyor",
            "hook effectiveness": "İlk 3 saniyede dikkat çekme gücün",
            "hook_effectiveness": "İzleyiciyi ilk saniyede durdurabiliyor musun",
            "engagement rate": "İçeriklerinle ne kadar etkileşim alıyorsun",
            "engagement_rate": "İnsanlar videolarını görüp beğeniyor mu, yoksa kaydırıp geçiyor mu",
            "shadowban risk": "Instagram seni gizlice cezalandırıyor olabilir mi",
            "shadowban_risk": "Algoritma seni görünmez yapıyor mu",
            "follower quality": "Takipçilerin gerçek mi, bot mu",
            "follower_quality": "Takipçilerin zombi mi, yoksa gerçek insan mı",
            "bot score": "Hesabında ne kadar sahte takipçi var",
            "bot_score": "Takipçilerinin yüzde kaçı sahte/bot",
            "reach": "Kaç kişi senin içeriğini gördü",
            "impressions": "Kaç kez gösterildin toplam",
            "save rate": "İçeriğini kaydedip daha sonra bakma oranı",
            "save_rate": "İnsanlar videolarını 'daha sonra izlemek' için kaydediyor mu",
            "share rate": "Kimse videolarını paylaşmıyor",
            "share_rate": "İnsanlar videolarını arkadaşlarına gönderiyor mu",
            "algorithm penalty": "Instagram seni cezalandırıyor",
            "algorithm_penalty": "Algoritma seni sorunlu buluyor ve göstermiyor",
            "content distribution": "İçerik dağılımın dengesiz",
            "content_distribution": "Hep aynı tipte içerik yapıyorsun",
            "niche clarity": "Nişin belli değil",
            "niche_clarity": "İnsanlar senin hesabının ne hakkında olduğunu anlamıyor",
            "conversion funnel": "İzleyiciden müşteriye dönüşüm yolculuğu",
            "conversion_funnel": "Nasıl izleyicini para veren müşteriye çeviriyorsun",
            "cpm": "1000 gösterimden kazanç",
            "CPM": "Bin kişiye gösterimden ne kadar kazanırsın",
            "ctr": "Tıklama oranı",
            "CTR": "100 kişi görünce kaç kişi tıklıyor"
        }
        
        self.hook_triggers = {
            "fear": {
                "description": "Korku/kayıp aversion - kaybetme korkusu",
                "templates": [
                    "Bu hatayı yapıyorsan {X}'ı kaybediyorsun",
                    "{X} yapmazsanız başınıza gelecek 3 felaket",
                    "Çoğu kişi {X} yüzünden batıyor (sen de mi?)",
                    "{X} sızdırıyorsa başınıza gelecek şey..."
                ],
                "power_level": 9,
                "use_when": "Acil aksiyon gerektiğinde"
            },
            "curiosity": {
                "description": "Merak - eksik bilgi hissi",
                "templates": [
                    "Kimsenin söylemediği {X} sırrı",
                    "{X} hakkında bilmediğin tek şey",
                    "Neden {X} yapan herkes kazanıyor?",
                    "{X}'ın karanlık tarafı (kimse konuşmuyor)"
                ],
                "power_level": 8,
                "use_when": "Bilgi paylaşımı içeriklerinde"
            },
            "benefit": {
                "description": "Fayda/kazanç odaklı",
                "templates": [
                    "{X} yaparak {Y} kazandım",
                    "Bu {X} sayesinde hayatım değişti",
                    "{X} için tek yapman gereken {Y}",
                    "30 günde {X} - nasıl mı?"
                ],
                "power_level": 7,
                "use_when": "Dönüşüm hikayeleri, rehber içeriklerde"
            },
            "social_proof": {
                "description": "Sosyal kanıt - başkaları yapıyor",
                "templates": [
                    "10K takipçili hesapların hepsinin ortak noktası",
                    "Başarılı {X}'lar bunu bilir",
                    "İlk %1'in sırrı (kimse paylaşmıyor)",
                    "{X} yapan herkes zengin. Neden sen değil?"
                ],
                "power_level": 8,
                "use_when": "Otorite oluşturma içeriklerinde"
            },
            "controversy": {
                "description": "Karşıtlık/tartışma yaratma",
                "templates": [
                    "Herkes {X} diyor. YANLIŞ.",
                    "Popüler olan {X} seni batırır",
                    "{X} aslında işe yaramıyor (kanıt içeride)",
                    "Kimse duymak istemiyor ama {X}"
                ],
                "power_level": 9,
                "use_when": "Dikkat çekme, viral potansiyel"
            },
            "urgency": {
                "description": "Aciliyet - şimdi hareket et",
                "templates": [
                    "DURMA! Önce bunu oku",
                    "Bugün yapmazsan yarın çok geç",
                    "Son 48 saat - {X} için son şans",
                    "Hemen {X} yap (sonra çok geç)"
                ],
                "power_level": 7,
                "use_when": "CTA içeriklerde, kampanyalarda"
            }
        }
        
        # Kötü hook kalıpları (KAÇINILACAK)
        self.bad_hook_patterns = [
            "Bugün sizlerle {X} paylaşmak istiyorum",
            "Merhaba arkadaşlar",
            "Biliyorsunuz ki {X}",
            "Uzun zamandır {X}",
            "Günün ipucu:",
            "Önemli bir bilgi:"
        ]
    
    def get_system_prompt(self) -> str:
        return """Sen Metrik Yorum Formatter Agent'sın.

🚨 ZORUNLU FORMAT: Her bulgu 3 BÖLÜMDEN oluşmalı:

[SORUN]: Teknik bulgu - sert, kısa, sayılarla
[AÇIKLAMA]: Anlaşılır açıklama - metafor ile
[AKSİYON]: Net komut - "YAPIN" diliyle, belirsizlik YOK

ÖRNEK:
[SORUN]: Etkileşim oranın %0.4 - sektör ortalaması %2.5
[AÇIKLAMA]: Bir parti verdin, 1000 kişi çağırdın ama sadece 4 kişi geldi. Diğerleri davetiyeyi bile açmadı.
[AKSİYON]: Hook'larını değiştir. İlk cümlede KORKU veya MERAK tetikle. "Bunu yapmazsanız..." ile başla.

YASAKLI İFADELER (KULLANMA!):
- "Potansiyel var/vadediyor"
- "Gelişmekte/Gelişme aşamasında"  
- "Umut verici/vadediyor"
- "İyi yolda/Doğru yolda"
- "Fena değil/Kötü değil"
- "Ortalamanın üzerinde" (kötüyse)

ZORUNLU TON:
- ACMASIZ: Gerçekleri yumuşatma
- GERÇEKÇİ: Sayı kötüyse "KÖTÜ" de
- EMİR VERİCİ: "Belki yapabilirsiniz" değil, "YAPIN"

HOOK YAZIM PSİKOLOJİSİ:
Üçgen: KORKU + MERAK + FAYDA

Kötü Hook: "Aura temizliği hakkında bilmeniz gerekenler"
İyi Hook: "Auranız sızdırıyorsa başınıza gelecek 3 FELAKET"

Kötü Hook: "Bugün sizlerle Instagram büyütme paylaşacağım"
İyi Hook: "Bu hatayı yapan HERKES takipçi kaybediyor (sen de mi?)"

ÇIKTI KURALLARI:
- SADECE JSON formatında yanıt ver
- Türkçe yaz
- Hiçbir açıklama veya ek metin ekleme"""

    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        # Extract agent results from account_data
        agent_results = account_data.get("agentResults", {})
        recent_posts = account_data.get("recentPosts", [])[:3]
        username = account_data.get("username", "unknown")
        
        # Format recent posts for hook rewriting
        posts_text = ""
        for i, post in enumerate(recent_posts, 1):
            caption = post.get("caption", "")[:200] if post.get("caption") else "Başlık yok"
            posts_text += f"\nPost {i}: {caption}..."
        
        return f"""Aşağıdaki teknik analiz raporunu 3 BÖLÜMLÜ formata çevir ve hook'ları yeniden yaz.

=== HESAP: @{username} ===
Takipçi: {account_data.get('followers', 0):,}
Etkileşim Oranı: {account_data.get('engagementRate', 0):.2f}%

=== TEKNİK AJAN RAPORLARI ===
{json.dumps(agent_results, ensure_ascii=False, indent=2)[:8000]}

=== SON 3 POST (Hook için) ===
{posts_text if posts_text else "Post verisi yok"}

=== ÇIKTI FORMATI ===
```json
{{
  "executiveSummary": {{
    "headline": "🔥 Tek cümlelik SERT özet",
    "grade": "A/B/C/D/F",
    "gradeExplanation": "Bu not şu anlama geliyor: [AÇIK İFADE]",
    "overallVerdict": "BAŞARILI/GELİŞTİRMELİ/SORUNLU/KRİTİK"
  }},
  "findings": [
    {{
      "category": "Etkileşim",
      "kusur": "[SORUN]: Teknik bulgu - sert ifade",
      "aciklama": "[AÇIKLAMA]: Metafor açıklama",
      "aksiyon": "[AKSİYON]: Net komut - YAPIN dili"
    }},
    {{
      "category": "İçerik Kalitesi",
      "kusur": "[SORUN]: Teknik bulgu",
      "aciklama": "[AÇIKLAMA]: Metafor açıklama",
      "aksiyon": "[AKSİYON]: Net komut"
    }},
    {{
      "category": "Büyüme",
      "kusur": "[SORUN]: Teknik bulgu",
      "aciklama": "[AÇIKLAMA]: Metafor açıklama",
      "aksiyon": "[AKSİYON]: Net komut"
    }},
    {{
      "category": "Görsel Kimlik",
      "kusur": "[SORUN]: Teknik bulgu",
      "aciklama": "[AÇIKLAMA]: Metafor açıklama",
      "aksiyon": "[AKSİYON]: Net komut"
    }},
    {{
      "category": "Kitle Kalitesi",
      "kusur": "[SORUN]: Teknik bulgu",
      "aciklama": "[AÇIKLAMA]: Metafor açıklama",
      "aksiyon": "[AKSİYON]: Net komut"
    }}
  ],
  "rewrittenHooks": [
    {{
      "originalCaption": "Orijinal caption özet",
      "badHook": "Mevcut ilk cümle (kötü)",
      "newHook": "YENİ PSİKOLOJİK HOOK",
      "triggerUsed": "fear/curiosity/benefit/social_proof/controversy/urgency",
      "whyItWorks": "Neden daha iyi (psikolojik açıklama)"
    }},
    {{
      "originalCaption": "Orijinal caption özet",
      "badHook": "Mevcut ilk cümle (kötü)",
      "newHook": "YENİ PSİKOLOJİK HOOK",
      "triggerUsed": "fear/curiosity/benefit/social_proof/controversy/urgency",
      "whyItWorks": "Neden daha iyi"
    }},
    {{
      "originalCaption": "Orijinal caption özet",
      "badHook": "Mevcut ilk cümle (kötü)",
      "newHook": "YENİ PSİKOLOJİK HOOK",
      "triggerUsed": "fear/curiosity/benefit/social_proof/controversy/urgency",
      "whyItWorks": "Neden daha iyi"
    }}
  ],
  "supremeHookFormula": {{
    "accountNiche": "Hesabın niş alanı",
    "bestTrigger": "En uygun psikolojik tetikleyici",
    "templateFormula": "Bu hesap için özel hook formülü",
    "examples": [
      "Örnek Hook 1 (bu hesaba özel)",
      "Örnek Hook 2 (bu hesaba özel)",
      "Örnek Hook 3 (bu hesaba özel)"
    ]
  }},
  "weeklyActionPlan": {{
    "monday": "PAZARTESİ: Spesifik görev",
    "wednesday": "ÇARŞAMBA: Spesifik görev",
    "friday": "CUMA: Spesifik görev",
    "weekend": "HAFTA SONU: Spesifik görev"
  }},
  "criticalWarning": "⚠️ YAPMAZSAN: En kötü senaryo (1 cümle, korku tetikle)",
  "motivationalKick": "💪 Motivasyon mesajı (sert ama destekleyici)"
}}
```

KRİTİK: 
1. Her finding'de [SORUN]/[AÇIKLAMA]/[AKSİYON] formatı ZORUNLU
2. Hook'larda PSİKOLOJİK TETİKLEYİCİ kullan
3. Yumuşak dil YASAK - acımasız ol
4. Sadece JSON döndür"""

    def rewrite_hook_with_psychology(
        self, 
        original_caption: str, 
        niche: str = "general",
        trigger_type: str = "auto"
    ) -> Dict[str, str]:
        """
        Tek bir hook'u psikolojik tetikleyicilerle yeniden yaz
        
        Args:
            original_caption: Orijinal caption metni
            niche: Hesabın nişi
            trigger_type: Kullanılacak tetikleyici (auto için en uygununu seç)
            
        Returns:
            Yeniden yazılmış hook ve açıklama
        """
        # İlk cümleyi bul
        first_sentence = original_caption.split('.')[0] if original_caption else ""
        first_sentence = first_sentence.split('\n')[0]  # Satır başlarını da kontrol et
        
        # Kötü hook kalıbı mı kontrol et
        is_bad_pattern = False
        for bad_pattern in self.bad_hook_patterns:
            if any(word.lower() in first_sentence.lower() for word in bad_pattern.split()):
                is_bad_pattern = True
                break
        
        # Trigger seç
        if trigger_type == "auto":
            # Nişe göre en uygun trigger'ı seç
            niche_trigger_map = {
                "spiritual": "fear",
                "business": "social_proof",
                "fitness": "benefit",
                "education": "curiosity",
                "entertainment": "controversy",
                "lifestyle": "curiosity"
            }
            trigger_type = niche_trigger_map.get((niche or 'general').lower(), "fear")  # Default: fear (en güçlü)
        
        trigger_info = self.hook_triggers.get(trigger_type, self.hook_triggers["fear"])
        
        return {
            "original_hook": first_sentence,
            "is_weak_hook": is_bad_pattern,
            "suggested_trigger": trigger_type,
            "trigger_power": trigger_info["power_level"],
            "template_to_use": trigger_info["templates"][0],
            "psychology_note": trigger_info["description"]
        }

    async def format_report(
        self,
        account_data: Dict[str, Any],
        agent_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Format technical report to simple language with 3-part format
        
        Args:
            account_data: Raw account data
            agent_results: Results from all PhD agents
            
        Returns:
            Simplified, actionable report with [KUSUR]/[AÇIKLAMA]/[AKSİYON] format
        """
        # Merge agent results into account data for prompt
        enriched_data = {**account_data, "agentResults": agent_results}
        
        # Run analysis (inherited from BaseAgent)
        result = await self.analyze(enriched_data)
        
        # 🗣️ GÖREV 3: Post-process ile teknik terimleri humanize et
        result = self._humanize_technical_terms(result)
        
        return result
    
    def _humanize_technical_terms(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        JSON çıktısındaki description alanlarını post-process ederek
        teknik terimleri sohbet diline çevirir.
        
        GÖREV 3: Teknik terimleri 5 yaşındaki çocuğun anlayacağı dile çevir
        """
        import json
        import re
        
        # Report'u string'e çevir
        report_str = json.dumps(report, ensure_ascii=False)
        
        # Her teknik terimi sohbet diliyle değiştir
        for technical, human in self.technical_term_humanization.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(technical), re.IGNORECASE)
            report_str = pattern.sub(human, report_str)
        
        # String'i tekrar dict'e çevir
        try:
            return json.loads(report_str)
        except:
            # JSON parse hatası olursa orijinalini döndür
            return report
