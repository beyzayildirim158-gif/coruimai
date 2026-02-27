# Visual Brand Agent - Görsel Kimlik ve Marka Tutarlılığı Uzmanı
# Version: 2.0
# PhD Seviyesi Görsel Analiz ve Marka Değerlendirme

from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent
import json
from datetime import datetime


class VisualBrandAgent(BaseAgent):
    """
    Visual Brand Agent v2.0
    Role: Advanced visual identity analysis, brand consistency, and aesthetic optimization
    
    Kapsamlı Uzmanlık Alanları:
    - Renk teorisi ve psikolojisi
    - Tipografi kuralları ve font pairing
    - Kompozisyon ve layout prensipleri
    - Marka tutarlılığı analizi
    - Grid aesthetics değerlendirmesi
    - İçerik formatı optimizasyonu
    - Görsel kalite değerlendirmesi
    - Reels ve Carousel tasarım kalitesi
    """
    
    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "Visual Brand Strategist"
        self.role = "Brand Identity & Visual Consistency Expert"
        self.specialty = "Color psychology, typography, composition, grid aesthetics, visual quality"
        
        # Initialize all configuration data
        self.color_psychology = self._init_color_psychology()
        self.color_harmony_rules = self._init_color_harmony()
        self.typography_rules = self._init_typography()
        self.composition_rules = self._init_composition()
        self.grid_patterns = self._init_grid_patterns()
        self.format_performance = self._init_format_performance()
        self.optimal_format_mix = self._init_optimal_format_mix()
    
    def _init_color_psychology(self) -> Dict[str, Any]:
        """Initialize color psychology matrix"""
        return {
            "red": {
                "emotional_effect": ["energy", "passion", "urgency"],
                "suitable_niches": ["food", "fitness", "sale", "entertainment"],
                "avoid_niches": ["health", "peace", "wellness"],
                "hex_examples": ["#E74C3C", "#C0392B", "#FF6B6B"]
            },
            "blue": {
                "emotional_effect": ["trust", "professional", "calm"],
                "suitable_niches": ["b2b", "tech", "finance", "healthcare"],
                "avoid_niches": ["food", "energy", "entertainment"],
                "hex_examples": ["#3498DB", "#2980B9", "#1ABC9C"]
            },
            "green": {
                "emotional_effect": ["nature", "growth", "health"],
                "suitable_niches": ["wellness", "eco", "finance", "organic"],
                "avoid_niches": ["luxury", "tech", "fashion"],
                "hex_examples": ["#27AE60", "#2ECC71", "#1ABC9C"]
            },
            "yellow": {
                "emotional_effect": ["happiness", "attention", "optimism"],
                "suitable_niches": ["kids", "food", "creative", "entertainment"],
                "avoid_niches": ["luxury", "serious", "b2b"],
                "hex_examples": ["#F1C40F", "#F39C12", "#FFC312"]
            },
            "orange": {
                "emotional_effect": ["creativity", "warmth", "enthusiasm"],
                "suitable_niches": ["entertainment", "food", "sports", "youth"],
                "avoid_niches": ["corporate", "luxury", "healthcare"],
                "hex_examples": ["#E67E22", "#D35400", "#FF9F43"]
            },
            "purple": {
                "emotional_effect": ["luxury", "creativity", "spirituality"],
                "suitable_niches": ["beauty", "luxury", "spiritual", "creative"],
                "avoid_niches": ["budget_brand", "sports", "food"],
                "hex_examples": ["#9B59B6", "#8E44AD", "#A55EEA"]
            },
            "pink": {
                "emotional_effect": ["feminine", "romantic", "playful"],
                "suitable_niches": ["beauty", "fashion", "wedding", "lifestyle"],
                "avoid_niches": ["b2b", "tech", "finance"],
                "hex_examples": ["#E91E63", "#FF6B9D", "#FD79A8"]
            },
            "black": {
                "emotional_effect": ["luxury", "power", "elegance"],
                "suitable_niches": ["luxury", "fashion", "art", "photography"],
                "avoid_niches": ["kids", "eco", "healthcare"],
                "hex_examples": ["#2C3E50", "#1A1A2E", "#000000"]
            },
            "white": {
                "emotional_effect": ["minimalist", "clean", "pure"],
                "suitable_niches": ["health", "tech", "minimal", "luxury"],
                "avoid_niches": ["warm_niche", "food", "entertainment"],
                "hex_examples": ["#FFFFFF", "#ECF0F1", "#F5F5F5"]
            },
            "brown": {
                "emotional_effect": ["organic", "reliable", "earthy"],
                "suitable_niches": ["coffee", "organic", "outdoor", "vintage"],
                "avoid_niches": ["tech", "modern", "futuristic"],
                "hex_examples": ["#8B4513", "#A0522D", "#D2691E"]
            }
        }
    
    def _init_color_harmony(self) -> Dict[str, Any]:
        """Initialize color harmony rules"""
        return {
            "complementary": {
                "description": "Opposite colors on wheel (blue-orange)",
                "effect": "High contrast, attention-grabbing",
                "use_case": "Bold statements, CTAs",
                "difficulty": "medium"
            },
            "analogous": {
                "description": "Adjacent colors (blue-green-cyan)",
                "effect": "Harmonic, soothing",
                "use_case": "Cohesive feeds, calming content",
                "difficulty": "easy"
            },
            "triadic": {
                "description": "120° apart (red-yellow-blue)",
                "effect": "Dynamic, balanced",
                "use_case": "Vibrant brands, creative content",
                "difficulty": "hard"
            },
            "split_complementary": {
                "description": "Complement + neighbors",
                "effect": "Contrast but softer",
                "use_case": "Versatile branding",
                "difficulty": "medium"
            },
            "monochromatic": {
                "description": "Single color variations",
                "effect": "Sophisticated, consistent",
                "use_case": "Luxury, minimal brands",
                "difficulty": "easy"
            }
        }
    
    def _init_typography(self) -> Dict[str, Any]:
        """Initialize typography rules"""
        return {
            "font_categories": {
                "serif": {
                    "character": ["traditional", "reliable", "authoritative"],
                    "suitable_use": ["luxury", "editorial", "formal"],
                    "examples": ["Playfair Display", "Merriweather", "Lora"]
                },
                "sans_serif": {
                    "character": ["modern", "clean", "professional"],
                    "suitable_use": ["tech", "minimal", "b2b", "contemporary"],
                    "examples": ["Montserrat", "Open Sans", "Roboto", "Inter"]
                },
                "script": {
                    "character": ["elegant", "personal", "decorative"],
                    "suitable_use": ["wedding", "beauty", "luxury", "feminine"],
                    "examples": ["Great Vibes", "Pacifico", "Dancing Script"]
                },
                "display": {
                    "character": ["attention_grabbing", "bold", "unique"],
                    "suitable_use": ["headlines", "accent", "posters"],
                    "examples": ["Bebas Neue", "Oswald", "Anton"]
                },
                "handwritten": {
                    "character": ["personal", "authentic", "casual"],
                    "suitable_use": ["personal_brand", "food", "lifestyle"],
                    "examples": ["Caveat", "Kalam", "Shadows Into Light"]
                },
                "monospace": {
                    "character": ["technical", "retro", "precise"],
                    "suitable_use": ["tech", "coding", "gaming", "data"],
                    "examples": ["Fira Code", "Source Code Pro", "JetBrains Mono"]
                }
            },
            "pairing_rules": {
                "contrast_principle": [
                    "serif_plus_sans_serif",
                    "display_plus_clean_body",
                    "handwritten_plus_structured"
                ],
                "max_fonts": {
                    "optimal": 2,
                    "acceptable": 3,
                    "avoid": 4
                }
            },
            "instagram_best_practices": {
                "min_font_size_mobile": 24,
                "contrast_ratio_min": 4.5,
                "fancy_font_limit": "headlines_only"
            }
        }
    
    def _init_composition(self) -> Dict[str, Any]:
        """Initialize composition rules"""
        return {
            "rule_of_thirds": {
                "description": "Divide frame into 3x3 grid, place focal points on intersections",
                "impact": "Natural, engaging composition",
                "score_weight": 0.30
            },
            "golden_ratio": {
                "ratio": 1.618,
                "description": "Natural aesthetic proportions",
                "impact": "Pleasing, professional look",
                "score_weight": 0.20
            },
            "symmetry": {
                "symmetric": {
                    "effect": "formal, reliable, stable",
                    "use_case": "Corporate, luxury, architecture"
                },
                "asymmetric": {
                    "effect": "dynamic, modern, interesting",
                    "use_case": "Creative, lifestyle, fashion"
                }
            },
            "white_space": {
                "minimum_percent": 20,
                "optimal_percent": 30,
                "effect": "Premium feel, breathability",
                "cluttered_penalty": -20
            }
        }
    
    def _init_grid_patterns(self) -> Dict[str, Any]:
        """Initialize Instagram grid patterns"""
        return {
            "checkerboard": {
                "description": "Alternating colors/styles",
                "difficulty": "easy",
                "visual_impact": "high",
                "maintenance": "medium"
            },
            "row_by_row": {
                "description": "Each row different theme",
                "difficulty": "medium",
                "visual_impact": "medium",
                "maintenance": "medium"
            },
            "column": {
                "description": "Vertical consistency",
                "difficulty": "hard",
                "visual_impact": "high",
                "maintenance": "hard"
            },
            "puzzle": {
                "description": "Large image split across posts",
                "difficulty": "hard",
                "visual_impact": "very_high",
                "maintenance": "hard"
            },
            "rainbow": {
                "description": "Color gradient across grid",
                "difficulty": "hard",
                "visual_impact": "very_high",
                "maintenance": "very_hard"
            },
            "borders": {
                "description": "Consistent frames/borders",
                "difficulty": "easy",
                "visual_impact": "medium",
                "maintenance": "easy"
            },
            "tiles": {
                "description": "Repeating pattern",
                "difficulty": "medium",
                "visual_impact": "medium",
                "maintenance": "medium"
            },
            "no_pattern": {
                "description": "Random/no intentional pattern",
                "difficulty": "none",
                "visual_impact": "low",
                "maintenance": "none"
            }
        }
    
    def _init_format_performance(self) -> Dict[str, Any]:
        """Initialize format performance matrix"""
        return {
            "reels": {
                "reach": 5,
                "engagement": 4,
                "save": 3,
                "share": 5,
                "growth": 5,
                "priority": 1
            },
            "carousel": {
                "reach": 3,
                "engagement": 4,
                "save": 5,
                "share": 3,
                "growth": 3,
                "priority": 2
            },
            "single_image": {
                "reach": 2,
                "engagement": 3,
                "save": 2,
                "share": 2,
                "growth": 2,
                "priority": 3
            },
            "stories": {
                "reach": 2,
                "engagement": 4,
                "save": 0,
                "share": 3,
                "growth": 2,
                "priority": "daily"
            },
            "live": {
                "reach": 2,
                "engagement": 5,
                "save": 0,
                "share": 2,
                "growth": 3,
                "priority": "weekly"
            },
            "guides": {
                "reach": 1,
                "engagement": 2,
                "save": 4,
                "share": 2,
                "growth": 1,
                "priority": 4
            }
        }
    
    def _init_optimal_format_mix(self) -> Dict[str, Any]:
        """Initialize optimal format distribution for 2024-2025"""
        return {
            "reels": {"min": 40, "optimal": 45, "max": 50},
            "carousel": {"min": 30, "optimal": 35, "max": 40},
            "single_post": {"min": 10, "optimal": 15, "max": 20},
            "tolerance": 5  # ±5% acceptable deviation
        }
    
    def get_system_prompt(self) -> str:
        return """Sen Visual Brand Agent'sın - Görsel Kimlik ve Marka Tutarlılığı Uzmanı.

## TEMEL UZMANLIK ALANLARIN:

### 1. RENK TEORİSİ VE PSİKOLOJİSİ

**Renk Psikolojisi Matrisi:**
| Renk | Duygusal Etki | Uygun Niche'ler | Kaçınılacak |
|------|---------------|-----------------|-------------|
| Kırmızı | Enerji, tutku, acil | Food, fitness, sale | Sağlık, huzur |
| Mavi | Güven, profesyonel | B2B, tech, finans | Food, enerji |
| Yeşil | Doğa, büyüme, sağlık | Wellness, eco, finans | Lüks, tech |
| Sarı | Mutluluk, dikkat | Kids, food, creative | Lüks, ciddi |
| Turuncu | Yaratıcılık, sıcak | Entertainment, food | Kurumsal |
| Mor | Lüks, yaratıcılık | Beauty, luxury, spiritual | Budget brand |
| Pembe | Feminen, romantik | Beauty, fashion, wedding | B2B, tech |
| Siyah | Lüks, güç, elegans | Luxury, fashion, art | Kids, eco |
| Beyaz | Minimalist, temiz | Health, tech, minimal | Sıcak niche |
| Kahverengi | Organik, güvenilir | Coffee, organic, outdoor | Tech, modern |

**Renk Uyumu Kuralları:**
1. Complementary (Zıt): Yüksek kontrast
2. Analogous (Komşu): Harmonik, rahatlatıcı
3. Triadic (Üçlü): Dinamik, dengeli
4. Split-Complementary: Kontrast ama yumuşak
5. Monochromatic: Sofistike, tutarlı

**Instagram Renk Paleti:**
- Primary Color: %60 (ana marka)
- Secondary Color: %30 (destekleyici)
- Accent Color: %10 (vurgu)
- Optimal: 3-4 renk | Kabul: 5-6 | Tutarsız: 7+

### 2. TİPOGRAFİ KURALLARI

**Font Kategorileri:**
| Tip | Karakter | Uygun Kullanım |
|-----|----------|----------------|
| Serif | Geleneksel, güvenilir | Luxury, editorial |
| Sans-serif | Modern, temiz | Tech, minimal, B2B |
| Script | Elegant, kişisel | Wedding, beauty |
| Display | Dikkat çekici | Headlines, accent |
| Handwritten | Samimi, otantik | Personal brand, food |
| Monospace | Teknik, retro | Tech, coding, gaming |

**Font Pairing:**
- Contrast: Serif + Sans-serif
- Hiyerarşi: Display (headline) + Clean (body)
- Maksimum: 2 optimal, 3 kabul, 4+ kaçın

**Instagram Best Practices:**
- Min font: 24pt mobilde
- Kontrast oranı: min 4.5:1
- Fancy font: sadece headlines

### 3. KOMPOZİSYON VE LAYOUT

**Temel Prensipler:**
1. Rule of Thirds: 3x3 grid, focal points kesişim noktalarında
2. Golden Ratio (1:1.618): Doğal estetik
3. Symmetry: Formal vs Dynamic
4. White Space: Min %20-30 boş alan (premium hissi)

**Instagram Grid Patterns:**
1. Checkerboard: Alternatif renkler/stiller
2. Row by Row: Her satır farklı tema
3. Column: Dikey tutarlılık
4. Puzzle: Büyük görsel parçaları
5. Rainbow: Renk gradyanı
6. Borders: Çerçeveli tutarlılık
7. Tiles: Tekrarlayan pattern

**Carousel Layout:**
- Slide 1: Hook (dikkat çekici)
- Slide 2-8: Content (değer)
- Slide 9: Summary/CTA
- Slide 10: Engagement prompt

### 4. MARKA TUTARLILIĞI ANALİZİ

**Visual Consistency Score (0-100):**
```
Consistency = (Color × 0.30) + (Typography × 0.20) + (Layout × 0.20) + (Filter × 0.15) + (Element × 0.15)
```

**Color Consistency:**
- Variance <15%: 100 puan
- 15-25%: 80 puan
- 25-35%: 60 puan
- 35-50%: 40 puan
- >50%: 20 puan

**Brand Recognition Score:**
```
Recognition = (Instant × 0.35) + (Unique × 0.30) + (Memorable × 0.20) + (Different × 0.15)
```

**Logo Presence:**
- Her post'ta: 100 | %50+: 70 | Sadece profil: 40 | Yok: 0

### 5. GRID AESTHETICS

**Grid Score:**
```
Grid = (Visual_Flow × 0.30) + (Color_Harmony × 0.25) + (Content_Balance × 0.25) + (First_Impression × 0.20)
```

**Visual Flow:** Smooth transitions, intentional pattern, no jarring contrasts
**Color Harmony:** Cohesive palette, balanced distribution, no clashes
**Content Balance:** Mix of types, text/image balance, variety without chaos
**First Impression (3-sec test):** Professional, clear niche, inviting

### 6. FORMAT ANALİZİ

**Format Performance (★ out of 5):**
| Format | Reach | Engage | Save | Share | Growth |
|--------|-------|--------|------|-------|--------|
| Reels | ★★★★★ | ★★★★ | ★★★ | ★★★★★ | ★★★★★ |
| Carousel | ★★★ | ★★★★ | ★★★★★ | ★★★ | ★★★ |
| Single | ★★ | ★★★ | ★★ | ★★ | ★★ |
| Stories | ★★ | ★★★★ | N/A | ★★★ | ★★ |
| Live | ★★ | ★★★★★ | N/A | ★★ | ★★★ |

**Optimal Format Mix (2024-2025):**
- Reels: %40-50
- Carousel: %30-40
- Single: %10-20

### 7. GÖRSEL KALİTE

**Image Quality Score:**
```
Quality = (Technical × 0.35) + (Composition × 0.25) + (Editing × 0.25) + (Relevance × 0.15)
```

**Technical:** Resolution (1080px+), Sharpness, Exposure
**Composition:** Rule of thirds, focal point, balance, framing
**Editing:** Color correction, consistent filter, not over-edited
**Relevance:** Matches caption, niche, brand

**Video Quality Score:**
```
Video = (Technical × 0.30) + (Audio × 0.20) + (Editing × 0.25) + (Content × 0.25)
```

**Reels Quality Checklist:**
- Technical (40%): 1080x1920, 30fps+, lighting, audio, stability, focus
- Creative (35%): Hook 0-3sec, pacing, transitions, text, music, ending
- Brand (25%): Color grading, font, logo, style match

**Carousel Quality:**
- Slide Design (40%): Template, text size, hierarchy, layout
- Flow & Narrative (30%): Progression, swipe motivation, conclusion
- Engagement (30%): Hook slide, value, CTA slide

### 8. EDGE CASES

1. **Yeni Hesap:** Brand identity "establishing", guideline önerileri sun
2. **Rebrand:** Transition period, eski vs yeni karşılaştır
3. **Multi-Product:** Sub-brand tutarlılığı, umbrella elements
4. **UGC Ağırlıklı:** Curation quality, brand overlay elements
5. **Personal Brand:** Yüz tutarlılığı, authenticity > polish
6. **Niche Spesifik:**
   - Food: Renk canlılığı kritik
   - Fashion: Trend alignment
   - B2B: Professional > creative
   - Art: Tutarsızlık kabul edilebilir

### 9. 2026 GÖRSEL MARKA PRENSİPLERİ - RAW AESTHETIC

**🎨 RAW AESTHETIC (Ham Estetik) AKIMI - 2026 TRENDİ:**

AI Yorgunluğu çağında kullanıcılar aşırı yapay içeriklere KARŞI:
- Stüdyo ışığı < Doğal ışık
- Profesyonel setup < Telefondan çekim
- Kusursuz edit < Ham footage
- AI metinleri < İnsan yazımı

**✅ RAW AESTHETIC ELEMENTLER (Olumlu Sinyaller):**
- Doğal ışıklandırma
- Arka planda günlük yaşam unsurları
- Hafif titremeli/stabilizasyonsuz çekimler
- Kendiliğinden oluşan kompozisyonlar
- Düzenlenmemiş/az düzenlenmiş renkler
- Gerçek ses (arka plan gürültüsü dahil)
- İnsan kusurları (ter, yorgunluk, hata)

**❌ AŞIRI PRODÜKSIYON UYARILARI (Olumsuz Sinyaller):**
- Her karede mükemmel aydınlatma
- Aşırı filtre/renk düzeltme
- Robotik/yapay caption'lar
- Her post'ta aynı template
- Stok fotoğraf kullanımı
- AI-generated görüntüler
- Aşırı photoshop/facetune

**📊 RAW vs POLISHED DENGE:**
- Personal Brand: %70 Raw, %30 Polished
- E-commerce: %40 Raw (BTS), %60 Polished (ürün)
- Education: %60 Raw, %40 Polished
- Entertainment: %80 Raw, %20 Polished
- B2B: %50 Raw, %50 Polished

**🎬 VİDEO KALİTESİ - 2026:**
- Dosya boyutu >1 MB ZORUNLU
- Netlik YÜKSEK tutulmalı (RAW ≠ düşük kalite)
- CapCut/Alight Motion ile KESKİNLEŞTİRME
- RAW estetik = kasıtlı kusur, teknik kalite DÜŞÜK DEĞİL

**🌟 CONTRARIAN VISUAL:**
- Sektörde herkes X yapıyorsa, Y dene
- Farklılık = Dikkat çekme
- Örnek: Herkes beyaz arka plan kullanıyorsa, renkli dene

**👤 "GERÇEK İNSAN" SİNYALLERİ:**
- Yüz ifadeleri (şaşkınlık, mutluluk, hayal kırıklığı)
- Günlük aktiviteler (çay/kahve içme, yemek)
- Behind-the-scenes anlar
- Küçük hatalar ve düzeltmeler
- Doğal konuşma (eee, ııı dahil)

🔴 KRİTİK ALAN KISITLAMASI - SADECE GÖRSEL KONULARDA KONUŞ! 🔴

✅ SENİN ALANIN (KONUŞMAN GEREKEN):
- Renk paleti ve uyumu
- Tipografi ve font seçimi
- Grid düzeni ve estetik
- Görsel tutarlılık
- Marka kimliği görsel unsurları
- Fotoğraf/video kalitesi
- Filtre tutarlılığı
- Carousel slide tasarımı

❌ BAŞKA AJANLARIN ALANI (KONUŞMA!):
- Etkileşim oranları → Community Loyalty ajanının işi
- Satış/gelir/monetizasyon → Sales Conversion ajanının işi
- Büyüme/niş analizi → Domain Master ajanının işi
- Hook/caption yazımı → Attention Architect ajanının işi
- Viral potansiyel → Growth Virality ajanının işi

⚠️ ETKİLEŞİM KENDİ PERSPEKTİFİNDEN BAHSEDİLEBİLİR:
- ✅ DOĞRU: "Tutarsız grid, profil ziyaretçilerinin %40'ının 3 saniyede çıkmasına neden oluyor"
- ❌ YANLIŞ: "Düşük etkileşim oranı algoritma sıralamasını düşürüyor"

OUTPUT FORMAT: Sadece geçerli JSON objesi döndür."""

    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        username = account_data.get('username', 'unknown')
        followers = account_data.get('followers', 0)
        posts = account_data.get('posts', 0)
        niche = account_data.get('niche', 'General')
        bio = account_data.get('bio', 'No bio')
        is_business = account_data.get('isBusiness', False)
        verified = account_data.get('verified', False)
        
        # Visual data
        visual_data = account_data.get('visualData', {})
        dominant_colors = visual_data.get('dominantColors', [])
        detected_fonts = visual_data.get('detectedFonts', [])
        grid_pattern = visual_data.get('gridPattern', 'unknown')
        filter_consistency = visual_data.get('filterConsistency', 0)
        
        # Format data
        format_data = account_data.get('formatData', {})
        reels_ratio = format_data.get('reelsRatio', 0)
        carousel_ratio = format_data.get('carouselRatio', 0)
        single_ratio = format_data.get('singleRatio', 0)
        
        # Quality data
        quality_data = account_data.get('qualityData', {})
        avg_image_quality = quality_data.get('avgImageQuality', 0)
        avg_video_quality = quality_data.get('avgVideoQuality', 0)
        
        # Get niche-appropriate colors
        niche_colors = self._get_niche_colors(niche)
        
        return f"""Bu Instagram hesabı için kapsamlı Visual Brand analizi yap:

## HESAP VERİLERİ:
- Username: @{username}
- Takipçi: {followers:,}
- Gönderi Sayısı: {posts:,}
- Niche: {niche}
- Bio: {bio}
- İş Hesabı: {is_business}
- Onaylı: {verified}

## GÖRSEL VERİLER:
- Dominant Renkler: {json.dumps(dominant_colors, indent=2) if dominant_colors else 'Analiz gerekli'}
- Tespit Edilen Fontlar: {detected_fonts if detected_fonts else 'Analiz gerekli'}
- Grid Pattern: {grid_pattern}
- Filter Tutarlılığı: {filter_consistency}%

## FORMAT DAĞILIMI:
- Reels: %{reels_ratio}
- Carousel: %{carousel_ratio}
- Single Post: %{single_ratio}

## KALİTE VERİLERİ:
- Ortalama Görsel Kalitesi: {avg_image_quality}/100
- Ortalama Video Kalitesi: {avg_video_quality}/100

## NİCHE İÇİN ÖNERİLEN RENKLER:
{json.dumps(niche_colors, indent=2)}

## ANALİZ GÖREVLERİ:

1. **Renk Analizi:**
   - Dominant renkleri belirle
   - Renk tutarlılığını değerlendir (%variance)
   - Palette uyumunu kontrol et (complementary/analogous/etc)
   - Niche ile renk psikolojisi uyumu
   - Primary/Secondary/Accent color önerisi

2. **Tipografi Analizi:**
   - Kullanılan font kategorilerini belirle
   - Font tutarlılığını değerlendir
   - Okunabilirlik skoru
   - Hiyerarşi netliği
   - Font pairing önerisi

3. **Grid Aesthetics Analizi:**
   - Grid pattern tespiti (checkerboard/row/column/puzzle/etc)
   - Visual flow değerlendirmesi
   - Color harmony across grid
   - Content variety balance
   - 3-saniye first impression

4. **Marka Tutarlılığı:**
   - Visual Consistency Score hesapla (0-100)
   - Brand Recognition Score hesapla (0-100)
   - Logo/watermark presence
   - Template usage değerlendirmesi
   - Signature elements tespiti

5. **Format Optimizasyonu:**
   - Current vs Optimal mix karşılaştır
   - Format Performance analizi
   - Deviation penalty hesapla
   - Format önerileri

6. **Görsel Kalite:**
   - Image Quality Score
   - Video Quality Score
   - Technical factors (resolution, sharpness, exposure)
   - Composition quality
   - Editing consistency
   - Professional level assessment

7. **Reels & Carousel Kalitesi:**
   - Reels: Technical + Creative + Brand alignment
   - Carousel: Slide design + Flow + Engagement elements

8. **Edge Case Kontrolü:**
   - Yeni hesap mı?
   - Rebrand sürecinde mi?
   - UGC ağırlıklı mı?
   - Personal brand mı?
   - Niche spesifik ayarlamalar

Aşağıdaki JSON yapısında yanıt ver:

{{
    "agent": "visual_brand",
    "analysis_timestamp": "{datetime.now().isoformat()}",
    "brand_overview": {{
        "visual_identity_strength": "low|medium|high",
        "primary_colors": ["#hex1", "#hex2", "#hex3"],
        "typography_style": "serif|sans_serif|mixed|undefined",
        "overall_aesthetic": "minimalist|bold|vibrant|elegant|casual|professional|undefined",
        "brand_maturity": "establishing|developing|established|premium",
        "visualArchetype": "minimalist_clean|bold_vibrant|elegant_luxury|casual_friendly|professional_corporate|artistic_creative|nature_organic|tech_modern"
    }},
    "metrics": {{
        "visualConsistency": 0,
        "brandRecognition": 0,
        "gridAesthetics": 0,
        "contentQuality": 0,
        "formatOptimization": 0,
        "overallVisualScore": 0,
        "colorConsistencyScore": 0,
        "gridProfessionalismScore": 0
    }},
    "colorConsistencyAnalysis": {{
        "score": 0,
        "formula_used": "Variance <15%: 100, 15-25%: 80, 25-35%: 60, 35-50%: 40, >50%: 20",
        "variance_percent": 0,
        "color_count_used": 0,
        "optimal_color_count": "3-4 colors (Primary 60%, Secondary 30%, Accent 10%)",
        "assessment": "consistent|moderate|inconsistent",
        "improvement_actions": ["string"]
    }},
    "dominantColors": [
        {{
            "hex": "#XXXXXX",
            "rgb": {{"r": 0, "g": 0, "b": 0}},
            "percentage": 0,
            "name": "Color Name",
            "psychology": "string emotion/association",
            "niche_fit": "excellent|good|neutral|poor",
            "usage_recommendation": "primary|secondary|accent|avoid"
        }}
    ],
    "recommendedPalette": {{
        "primary": {{
            "hex": "#XXXXXX",
            "name": "Color Name",
            "usage": "60% - main brand color, backgrounds, key elements",
            "psychology": "string"
        }},
        "secondary": {{
            "hex": "#XXXXXX",
            "name": "Color Name",
            "usage": "30% - supporting elements, headers",
            "psychology": "string"
        }},
        "accent": {{
            "hex": "#XXXXXX",
            "name": "Color Name",
            "usage": "10% - CTAs, highlights, emphasis",
            "psychology": "string"
        }},
        "harmony_type": "complementary|analogous|triadic|split_complementary|monochromatic",
        "rationale": "string explaining why this palette fits the niche"
    }},
    "gridProfessionalism": {{
        "score": 0,
        "formula_used": "Grid = (Visual_Flow × 0.30) + (Color_Harmony × 0.25) + (Content_Balance × 0.25) + (First_Impression × 0.20)",
        "components": {{
            "visual_flow": {{"score": 0, "assessment": "string"}},
            "color_harmony": {{"score": 0, "assessment": "string"}},
            "content_balance": {{"score": 0, "assessment": "string"}},
            "first_impression": {{"score": 0, "assessment": "string"}}
        }},
        "pattern_detected": "checkerboard|row_by_row|column|puzzle|rainbow|borders|tiles|no_pattern",
        "pattern_effectiveness": "high|medium|low",
        "grid_screenshot_analysis": {{
            "first_9_posts_cohesion": 0,
            "first_12_posts_cohesion": 0,
            "color_distribution_balance": 0,
            "visual_rhythm": "strong|moderate|weak|none"
        }},
        "improvement_suggestions": ["string"]
    }},
    "thumbnailAnalysis": {{
        "overall_score": 0,
        "posts_analyzed": [
            {{
                "post_index": 1,
                "post_type": "reel|carousel|image",
                "thumbnail_score": 0,
                "contrast_score": 0,
                "text_readability": 0,
                "face_presence": true|false,
                "emotion_detected": "neutral|happy|surprised|curious|serious",
                "scroll_stopping_potential": "low|medium|high",
                "improvements": ["string"]
            }}
        ],
        "average_thumbnail_score": 0,
        "scroll_stopping_principles": {{
            "contrast_usage": 0,
            "face_usage": 0,
            "text_overlay_effectiveness": 0,
            "color_brightness": 0,
            "curiosity_elements": 0
        }},
        "thumbnail_template_recommendation": {{
            "layout": "string",
            "text_style": "string",
            "text_placement": "top|center|bottom|corner",
            "color_scheme": "string",
            "emotion_to_convey": "string"
        }}
    }},
    "color_analysis": {{
        "dominant_colors": [
            {{"hex": "#XXXXXX", "percentage": 0, "name": "Color Name", "psychology_fit": "good|neutral|poor"}}
        ],
        "color_consistency": {{
            "score": 0,
            "variance_percent": 0,
            "assessment": "consistent|moderate|inconsistent"
        }},
        "palette_harmony": {{
            "type": "complementary|analogous|triadic|split_complementary|monochromatic|none",
            "score": 0,
            "assessment": "string"
        }},
        "niche_color_fit": {{
            "score": 0,
            "suitable_colors_used": [],
            "problematic_colors": [],
            "recommendation": "string"
        }},
        "recommended_palette": {{
            "primary": "#XXXXXX",
            "secondary": "#XXXXXX",
            "accent": "#XXXXXX",
            "rationale": "string"
        }}
    }},
    "typography_analysis": {{
        "fonts_detected": [],
        "font_categories_used": [],
        "font_consistency": {{
            "score": 0,
            "assessment": "consistent|moderate|inconsistent"
        }},
        "readability_score": 0,
        "hierarchy_clarity": 0,
        "font_count": 0,
        "font_pairing_assessment": "good|acceptable|needs_improvement",
        "recommendations": {{
            "primary_font": "Font Name",
            "secondary_font": "Font Name",
            "rationale": "string"
        }}
    }},
    "grid_analysis": {{
        "pattern_detected": "checkerboard|row_by_row|column|puzzle|rainbow|borders|tiles|no_pattern",
        "visual_flow": {{
            "score": 0,
            "smooth_transitions": true,
            "intentional_pattern": true,
            "jarring_elements": false
        }},
        "color_distribution": {{
            "score": 0,
            "balanced": true,
            "clashes_detected": false
        }},
        "content_variety": {{
            "score": 0,
            "format_mix": "good|limited|excessive",
            "visual_interest": "high|medium|low"
        }},
        "first_impression": {{
            "score": 0,
            "professional": true,
            "niche_clear": true,
            "inviting": true
        }},
        "grid_recommendation": "string"
    }},
    "consistency_analysis": {{
        "visual_consistency_score": 0,
        "formula_used": "Consistency = (Color × 0.30) + (Typography × 0.20) + (Layout × 0.20) + (Filter × 0.15) + (Element × 0.15)",
        "components": {{
            "color_consistency": 0,
            "typography_consistency": 0,
            "layout_consistency": 0,
            "filter_consistency": 0,
            "element_consistency": 0
        }},
        "consistency_level": "low|medium|high",
        "brand_recognition_score": 0,
        "recognition_formula": "Recognition = (Instant × 0.35) + (Unique × 0.30) + (Memorable × 0.20) + (Different × 0.15)",
        "recognition_factors": {{
            "logo_presence": 0,
            "color_signature": 0,
            "style_uniqueness": 0,
            "template_usage": 0,
            "visual_elements": 0
        }},
        "instant_recognition_test": {{
            "would_recognize_without_username": true|false,
            "distinctive_elements": ["string"],
            "similarity_to_competitors": "very_different|somewhat_different|similar|very_similar"
        }}
    }},
    "format_analysis": {{
        "current_mix": {{
            "reels": 0,
            "carousel": 0,
            "single_post": 0
        }},
        "optimal_mix": {{
            "reels": 45,
            "carousel": 35,
            "single_post": 20
        }},
        "deviation_score": 0,
        "format_performance": {{
            "reels": {{"avg_reach": 0, "avg_engagement": 0, "quality_score": 0}},
            "carousel": {{"avg_reach": 0, "avg_engagement": 0, "quality_score": 0}},
            "single_post": {{"avg_reach": 0, "avg_engagement": 0, "quality_score": 0}}
        }},
        "optimization_recommendations": []
    }},
    "quality_analysis": {{
        "image_quality": {{
            "score": 0,
            "technical": {{"resolution": 0, "sharpness": 0, "exposure": 0}},
            "composition": 0,
            "editing": 0,
            "relevance": 0
        }},
        "video_quality": {{
            "score": 0,
            "technical": {{"resolution": 0, "stability": 0, "lighting": 0}},
            "audio": 0,
            "editing": 0,
            "content": 0
        }},
        "reels_quality": {{
            "score": 0,
            "technical_score": 0,
            "creative_score": 0,
            "brand_alignment_score": 0
        }},
        "carousel_quality": {{
            "score": 0,
            "slide_design": 0,
            "flow_narrative": 0,
            "engagement_elements": 0
        }},
        "professional_level": "beginner|intermediate|professional|premium"
    }},
    "visualArchetypeAnalysis": {{
        "detected_archetype": "minimalist_clean|bold_vibrant|elegant_luxury|casual_friendly|professional_corporate|artistic_creative|nature_organic|tech_modern",
        "archetype_consistency": 0,
        "archetype_fit_for_niche": "excellent|good|moderate|poor",
        "archetype_characteristics": {{
            "color_mood": "string",
            "composition_style": "string",
            "emotion_conveyed": "string",
            "target_audience_match": "string"
        }},
        "alternative_archetypes": [
            {{
                "archetype": "string",
                "why_consider": "string",
                "transition_difficulty": "easy|medium|hard"
            }}
        ]
    }},
    "edge_cases": {{
        "is_new_account": false,
        "is_rebranding": false,
        "is_ugc_heavy": false,
        "is_personal_brand": false,
        "niche_specific_notes": "string"
    }},
    "findings": [
        {{
            "type": "strength|weakness|opportunity|threat",
            "category": "color|typography|grid|consistency|format|quality",
            "finding": "TÜRKÇE - örn: Grid düzeni tutarsız, 3x3 simetri bozulmuş ve bu profesyonellik algısını zayıflatıyor",
            "evidence": "TÜRKÇE - örn: Son 12 postun 8'i farklı renk tonlarında, 3 farklı filtre kullanılmış ve görsel bütünlük sağlanamamış",
            "impact_score": 75
        }},
        {{
            "type": "strength",
            "category": "quality",
            "finding": "TÜRKÇE - örn: Fotoğraf kalitesi yüksek, profesyonel ekipman kullanımı belirgin ve bu marka güvenilirliğini artırıyor",
            "evidence": "TÜRKÇE - örn: Tüm görsellerde 1080p üzeri çözünürlük, doğru ışık kullanımı ve net odaklama mevcut",
            "impact_score": 85
        }}
    ],
    "recommendations": [
        {{
            "priority": 1,
            "category": "TÜRKÇE - örn: Renk Paleti Standardizasyonu",
            "action": "TÜRKÇE - örn: Marka için 3 ana renk (primary, secondary, accent) belirleyip tüm içeriklerde tutarlı kullanın",
            "expected_impact": "TÜRKÇE - örn: Marka tanınırlığında %40 artış, profil ziyaretlerinin takibe dönüşüm oranında %15 iyileşme",
            "implementation": "TÜRKÇE - örn: 1) Mevcut en iyi performans gösteren postların renklerini analiz edin 2) Rakiplerin kullanmadığı ayırt edici bir palet seçin 3) Canva/Adobe'da şablon oluşturun",
            "difficulty": "easy|medium|hard"
        }}
    ],
    "brand_guidelines_suggestion": {{
        "primary_color": "#XXXXXX",
        "secondary_color": "#XXXXXX",
        "accent_color": "#XXXXXX",
        "primary_font": "Font Name",
        "secondary_font": "Font Name",
        "recommended_filters": [],
        "logo_placement": "top_left|top_right|bottom_left|bottom_right|center",
        "grid_strategy": "string",
        "visual_style_keywords": [],
        "mood_board_elements": ["string descriptions of visual elements to include"]
    }}
}}"""

    def _get_niche_colors(self, niche: str) -> Dict[str, Any]:
        """Get recommended colors for a specific niche"""
        niche_lower = (niche or 'general').lower()
        
        niche_color_map = {
            "fitness": {
                "recommended": ["red", "orange", "black"],
                "avoid": ["pink", "purple"],
                "rationale": "Energy, power, action"
            },
            "food": {
                "recommended": ["red", "orange", "yellow", "brown"],
                "avoid": ["blue", "purple"],
                "rationale": "Appetite stimulation, warmth"
            },
            "tech": {
                "recommended": ["blue", "black", "white"],
                "avoid": ["pink", "brown"],
                "rationale": "Trust, innovation, clean"
            },
            "beauty": {
                "recommended": ["pink", "purple", "gold", "white"],
                "avoid": ["brown", "green"],
                "rationale": "Femininity, luxury, elegance"
            },
            "fashion": {
                "recommended": ["black", "white", "gold"],
                "avoid": ["brown"],
                "rationale": "Elegance, versatility"
            },
            "wellness": {
                "recommended": ["green", "blue", "white"],
                "avoid": ["red", "black"],
                "rationale": "Nature, calm, health"
            },
            "business": {
                "recommended": ["blue", "black", "gray"],
                "avoid": ["pink", "yellow"],
                "rationale": "Trust, professionalism"
            },
            "lifestyle": {
                "recommended": ["neutral", "earth_tones", "pastels"],
                "avoid": ["neon"],
                "rationale": "Approachable, aesthetic"
            },
            "education": {
                "recommended": ["blue", "green", "orange"],
                "avoid": ["black_heavy"],
                "rationale": "Trust, growth, energy"
            },
            "travel": {
                "recommended": ["blue", "orange", "earth_tones"],
                "avoid": ["gray"],
                "rationale": "Adventure, nature, warmth"
            }
        }
        
        for key in niche_color_map:
            if key in niche_lower:
                return niche_color_map[key]
        
        return {
            "recommended": ["neutral", "brand_specific"],
            "avoid": [],
            "rationale": "Analyze specific niche requirements"
        }
    
    def calculate_visual_consistency(
        self,
        color_variance: float,
        typography_score: float,
        layout_score: float,
        filter_score: float,
        element_score: float
    ) -> Dict[str, Any]:
        """
        Calculate Visual Consistency Score (0-100)
        
        Formula:
        Consistency = (Color × 0.30) + (Typography × 0.20) + (Layout × 0.20) + (Filter × 0.15) + (Element × 0.15)
        """
        # Color consistency based on variance
        if color_variance < 15:
            color_score = 100
        elif color_variance < 25:
            color_score = 80
        elif color_variance < 35:
            color_score = 60
        elif color_variance < 50:
            color_score = 40
        else:
            color_score = 20
        
        consistency_score = (
            color_score * 0.30 +
            typography_score * 0.20 +
            layout_score * 0.20 +
            filter_score * 0.15 +
            element_score * 0.15
        )
        
        # Determine level
        if consistency_score >= 75:
            level = "high"
        elif consistency_score >= 40:
            level = "medium"
        else:
            level = "low"
        
        return {
            "score": round(consistency_score, 1),
            "level": level,
            "components": {
                "color": round(color_score, 1),
                "typography": round(typography_score, 1),
                "layout": round(layout_score, 1),
                "filter": round(filter_score, 1),
                "element": round(element_score, 1)
            }
        }
    
    def calculate_brand_recognition(
        self,
        logo_presence: float,
        color_signature: float,
        style_uniqueness: float,
        template_usage: float,
        visual_elements: float
    ) -> Dict[str, Any]:
        """
        Calculate Brand Recognition Score (0-100)
        
        Formula:
        Recognition = (Instant × 0.35) + (Unique × 0.30) + (Memorable × 0.20) + (Different × 0.15)
        """
        # Instant recognition components
        instant_recognition = (
            (logo_presence * 0.20) +
            (color_signature * 0.30) +
            (style_uniqueness * 0.30) +
            (template_usage * 0.20)
        )
        
        recognition_score = (
            instant_recognition * 0.35 +
            style_uniqueness * 0.30 +
            visual_elements * 0.20 +
            color_signature * 0.15
        )
        
        return {
            "score": round(recognition_score, 1),
            "factors": {
                "logo_presence": round(logo_presence, 1),
                "color_signature": round(color_signature, 1),
                "style_uniqueness": round(style_uniqueness, 1),
                "template_usage": round(template_usage, 1),
                "visual_elements": round(visual_elements, 1)
            }
        }
    
    def calculate_grid_aesthetics(
        self,
        visual_flow: float,
        color_harmony: float,
        content_balance: float,
        first_impression: float
    ) -> Dict[str, Any]:
        """
        Calculate Grid Aesthetics Score (0-100)
        
        Formula:
        Grid = (Visual_Flow × 0.30) + (Color_Harmony × 0.25) + (Content_Balance × 0.25) + (First_Impression × 0.20)
        """
        grid_score = (
            visual_flow * 0.30 +
            color_harmony * 0.25 +
            content_balance * 0.25 +
            first_impression * 0.20
        )
        
        return {
            "score": round(grid_score, 1),
            "components": {
                "visual_flow": round(visual_flow, 1),
                "color_harmony": round(color_harmony, 1),
                "content_balance": round(content_balance, 1),
                "first_impression": round(first_impression, 1)
            }
        }
    
    def calculate_format_optimization(
        self,
        current_mix: Dict[str, float],
        optimal_mix: Dict[str, float] = None
    ) -> Dict[str, Any]:
        """
        Calculate Format Optimization Score based on deviation from optimal
        """
        if optimal_mix is None:
            optimal_mix = {
                "reels": 45,
                "carousel": 35,
                "single_post": 20
            }
        
        tolerance = 5
        
        # Calculate deviation penalties
        penalties = {}
        for format_type, optimal in optimal_mix.items():
            current = current_mix.get(format_type, 0)
            deviation = abs(current - optimal)
            
            if deviation <= tolerance:
                penalties[format_type] = 100
            elif deviation <= 10:
                penalties[format_type] = 80
            elif deviation <= 15:
                penalties[format_type] = 60
            elif deviation <= 20:
                penalties[format_type] = 40
            else:
                penalties[format_type] = 20
        
        avg_score = sum(penalties.values()) / len(penalties)
        
        return {
            "score": round(avg_score, 1),
            "current_mix": current_mix,
            "optimal_mix": optimal_mix,
            "deviations": {
                k: round(abs(current_mix.get(k, 0) - v), 1)
                for k, v in optimal_mix.items()
            },
            "format_scores": penalties
        }
    
    def calculate_image_quality(
        self,
        resolution_score: float,
        sharpness_score: float,
        exposure_score: float,
        composition_score: float,
        editing_score: float,
        relevance_score: float
    ) -> Dict[str, Any]:
        """
        Calculate Image Quality Score (0-100)
        
        Formula:
        Quality = (Technical × 0.35) + (Composition × 0.25) + (Editing × 0.25) + (Relevance × 0.15)
        """
        technical_avg = (resolution_score + sharpness_score + exposure_score) / 3
        
        quality_score = (
            technical_avg * 0.35 +
            composition_score * 0.25 +
            editing_score * 0.25 +
            relevance_score * 0.15
        )
        
        return {
            "score": round(quality_score, 1),
            "technical": {
                "resolution": round(resolution_score, 1),
                "sharpness": round(sharpness_score, 1),
                "exposure": round(exposure_score, 1),
                "average": round(technical_avg, 1)
            },
            "composition": round(composition_score, 1),
            "editing": round(editing_score, 1),
            "relevance": round(relevance_score, 1)
        }
    
    def calculate_video_quality(
        self,
        resolution_score: float,
        stability_score: float,
        lighting_score: float,
        audio_score: float,
        editing_score: float,
        content_score: float
    ) -> Dict[str, Any]:
        """
        Calculate Video Quality Score (0-100)
        
        Formula:
        Video = (Technical × 0.30) + (Audio × 0.20) + (Editing × 0.25) + (Content × 0.25)
        """
        technical_avg = (resolution_score + stability_score + lighting_score) / 3
        
        video_score = (
            technical_avg * 0.30 +
            audio_score * 0.20 +
            editing_score * 0.25 +
            content_score * 0.25
        )
        
        # Determine professional level
        if video_score >= 90:
            level = "premium"
        elif video_score >= 75:
            level = "professional"
        elif video_score >= 60:
            level = "intermediate"
        else:
            level = "beginner"
        
        return {
            "score": round(video_score, 1),
            "technical": {
                "resolution": round(resolution_score, 1),
                "stability": round(stability_score, 1),
                "lighting": round(lighting_score, 1),
                "average": round(technical_avg, 1)
            },
            "audio": round(audio_score, 1),
            "editing": round(editing_score, 1),
            "content": round(content_score, 1),
            "professional_level": level
        }
    
    def calculate_reels_quality(
        self,
        technical_score: float,
        creative_score: float,
        brand_score: float
    ) -> Dict[str, Any]:
        """
        Calculate Reels Quality Score
        
        Formula:
        Reels = (Technical × 0.40) + (Creative × 0.35) + (Brand × 0.25)
        """
        reels_score = (
            technical_score * 0.40 +
            creative_score * 0.35 +
            brand_score * 0.25
        )
        
        # Benchmarks
        if reels_score >= 90:
            benchmark = "professional"
        elif reels_score >= 75:
            benchmark = "good"
        elif reels_score >= 60:
            benchmark = "acceptable"
        elif reels_score >= 40:
            benchmark = "needs_improvement"
        else:
            benchmark = "poor"
        
        return {
            "score": round(reels_score, 1),
            "technical": round(technical_score, 1),
            "creative": round(creative_score, 1),
            "brand_alignment": round(brand_score, 1),
            "benchmark": benchmark
        }
    
    def calculate_carousel_quality(
        self,
        slide_design: float,
        flow_narrative: float,
        engagement_elements: float
    ) -> Dict[str, Any]:
        """
        Calculate Carousel Quality Score
        
        Formula:
        Carousel = (Slide × 0.40) + (Flow × 0.30) + (Engagement × 0.30)
        """
        carousel_score = (
            slide_design * 0.40 +
            flow_narrative * 0.30 +
            engagement_elements * 0.30
        )
        
        return {
            "score": round(carousel_score, 1),
            "slide_design": round(slide_design, 1),
            "flow_narrative": round(flow_narrative, 1),
            "engagement_elements": round(engagement_elements, 1)
        }
    
    def detect_color_harmony(self, colors: List[str]) -> Dict[str, Any]:
        """
        Detect the color harmony type from a list of hex colors
        """
        if not colors or len(colors) < 2:
            return {"type": "undefined", "score": 0}
        
        # Simplified harmony detection based on color count and variety
        unique_hues = len(set(colors))
        
        if unique_hues == 1:
            return {"type": "monochromatic", "score": 90, "description": "Single color variations"}
        elif unique_hues == 2:
            return {"type": "complementary", "score": 80, "description": "Two contrasting colors"}
        elif unique_hues == 3:
            return {"type": "triadic", "score": 75, "description": "Three balanced colors"}
        elif unique_hues <= 4:
            return {"type": "analogous", "score": 70, "description": "Adjacent colors"}
        else:
            return {"type": "mixed", "score": 50, "description": "Multiple colors, less cohesive"}
    
    def get_grid_pattern_recommendation(self, niche: str, current_pattern: str) -> str:
        """Get grid pattern recommendation based on niche"""
        niche_patterns = {
            "fashion": "checkerboard or puzzle for visual impact",
            "food": "borders with consistent styling",
            "travel": "row_by_row with location themes",
            "fitness": "alternating content types (results/tips)",
            "beauty": "rainbow gradient or color blocks",
            "business": "tiles with consistent branding",
            "lifestyle": "checkerboard for variety",
            "education": "row_by_row by topic"
        }
        
        niche_lower = niche.lower()
        for key, recommendation in niche_patterns.items():
            if key in niche_lower:
                return recommendation
        
        return "checkerboard for balanced variety"
