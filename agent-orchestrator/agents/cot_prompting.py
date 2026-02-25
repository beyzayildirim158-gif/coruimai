# =============================================================================
# Chain-of-Thought Prompting & Self-Correction Module
# Enhanced reasoning and quality control for LLM outputs
# =============================================================================
"""
Bu modül LLM çıktı kalitesini artırmak için:
1. Chain-of-Thought (CoT) prompting
2. Self-correction mekanizması (çıktı kısa/eksikse düzelt)
3. Output validation ve kalite kontrolü
4. Structured output schemas

Kullanım:
    from agents.cot_prompting import (
        get_cot_prompt_template,
        self_correct_output,
        validate_output_quality,
        OUTPUT_SCHEMA
    )
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


# =============================================================================
# CHAIN-OF-THOUGHT PROMPT TEMPLATES
# =============================================================================

COT_ANALYSIS_TEMPLATE = """
🧠 ANALİZ SÜRECİ - ADIM ADIM DÜŞÜN

Analizini yaparken şu adımları takip et:

## ADIM 1: VERİ İNCELEME (Data Review)
- Verilen metrikleri listele
- Her metriğin ne anlama geldiğini belirt
- Eksik veya şüpheli verileri işaretle

## ADIM 2: BENCHMARK KARŞILAŞTIRMA (Benchmark Comparison)
- Her metriği sektör ortalamasıyla karşılaştır
- Sapmaları hesapla (% olarak)
- Üstün ve düşük performans alanlarını belirle

## ADIM 3: ÖRÜNTÜ TESPİTİ (Pattern Recognition)
- Veriler arasındaki ilişkileri analiz et
- Neden-sonuç ilişkilerini kur
- Gizli örüntüleri ortaya çıkar

## ADIM 4: SWOT ANALİZİ (SWOT Analysis)
- Güçlü yönleri listele (Strengths)
- Zayıf yönleri listele (Weaknesses)
- Fırsatları belirle (Opportunities)
- Tehditleri değerlendir (Threats)

## ADIM 5: ÖNERİ GELİŞTİRME (Recommendation Development)
- Her zayıf yön için spesifik aksiyon öner
- Önceliklendirme yap (kritik > yüksek > orta > düşük)
- Beklenen etki ve timeline belirt
- Uygulama adımlarını detaylandır

## ADIM 6: SKORLAMA (Scoring)
- Her alt kategori için 0-100 skor ver
- Ağırlıklı ortalama ile genel skor hesapla
- Güven seviyesi belirt

⚠️ ÖNEMLİ: Her adımı açıkça düşün ve sonuçlarını yaz. Kısa yoldan gitme!
"""

COT_REASONING_MARKERS = """
📊 DÜŞÜNME SÜRECİ:

1. GÖZLEM: [Verilerden ne görüyorum?]
2. ANALİZ: [Bu ne anlama geliyor?]
3. KARŞILAŞTIRMA: [Sektör/benchmark ile nasıl?]
4. SONUÇ: [Çıkarımım nedir?]
5. ÖNERİ: [Ne yapılmalı?]

Her bulgu için bu formatı kullan.
"""


# =============================================================================
# STRUCTURED OUTPUT SCHEMA
# =============================================================================

OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["findings", "recommendations", "metrics"],
    "properties": {
        "findings": {
            "type": "array",
            "minItems": 3,
            "items": {
                "type": "object",
                "required": ["type", "category", "finding", "impact_score"],
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["strength", "weakness", "opportunity", "threat", "info", "warning", "critical"]
                    },
                    "category": {
                        "type": "string",
                        "minLength": 2,
                        "maxLength": 50
                    },
                    "finding": {
                        "type": "string",
                        "minLength": 100,
                        "description": "Detaylı bulgu açıklaması - EN AZ 100 karakter"
                    },
                    "evidence": {
                        "type": "string",
                        "minLength": 20,
                        "description": "Bulguyu destekleyen kanıt"
                    },
                    "impact_score": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 100
                    }
                }
            }
        },
        "recommendations": {
            "type": "array",
            "minItems": 3,
            "items": {
                "type": "object",
                "required": ["priority", "category", "action", "expected_impact"],
                "properties": {
                    "priority": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"]
                    },
                    "category": {
                        "type": "string",
                        "minLength": 2
                    },
                    "action": {
                        "type": "string",
                        "minLength": 150,
                        "description": "Spesifik aksiyon önerisi - EN AZ 150 karakter"
                    },
                    "expected_impact": {
                        "type": "string",
                        "minLength": 30
                    },
                    "implementation": {
                        "type": "string",
                        "minLength": 50,
                        "description": "Uygulama adımları"
                    },
                    "difficulty": {
                        "type": "string",
                        "enum": ["easy", "medium", "hard", "expert"]
                    },
                    "timeline": {
                        "type": "string"
                    },
                    "kpi": {
                        "type": "string",
                        "description": "Başarı metriği"
                    }
                }
            }
        },
        "metrics": {
            "type": "object",
            "required": ["overallScore"],
            "properties": {
                "overallScore": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "default": 80
                }
            }
        }
    }
}

# Schema'yı string olarak da tut (prompt'a eklemek için)
OUTPUT_SCHEMA_STRING = json.dumps(OUTPUT_SCHEMA, indent=2, ensure_ascii=False)


# =============================================================================
# QUALITY THRESHOLDS
# =============================================================================

QUALITY_THRESHOLDS = {
    "min_finding_length": 100,
    "min_recommendation_length": 150,
    "min_findings_count": 3,
    "min_recommendations_count": 3,
    "min_total_content_length": 2000,
    "max_allowed_generic_phrases": 2,
}

GENERIC_PHRASES = [
    "daha fazla paylaşım",
    "içerik kalitesini artır",
    "tutarlı ol",
    "etkileşimi artır",
    "düzenli paylaş",
    "kaliteli içerik",
    "hedef kitleni tanı",
    "more content",
    "be consistent",
    "increase engagement",
    "improve quality",
]


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_output_quality(output: Dict[str, Any]) -> Tuple[bool, List[str], int]:
    """
    LLM çıktısının kalitesini değerlendir
    
    Args:
        output: LLM'den gelen parsed output
        
    Returns:
        (is_valid, issues, quality_score)
    """
    issues = []
    quality_score = 100
    
    # 1. Findings kontrolü
    findings = output.get("findings", [])
    if len(findings) < QUALITY_THRESHOLDS["min_findings_count"]:
        issues.append(f"Yetersiz bulgu sayısı: {len(findings)}/{QUALITY_THRESHOLDS['min_findings_count']}")
        quality_score -= 20
    
    for i, finding in enumerate(findings):
        finding_text = finding.get("finding", "") if isinstance(finding, dict) else str(finding)
        if len(finding_text) < QUALITY_THRESHOLDS["min_finding_length"]:
            issues.append(f"Bulgu {i+1} çok kısa: {len(finding_text)} karakter")
            quality_score -= 10
    
    # 2. Recommendations kontrolü
    recommendations = output.get("recommendations", [])
    if len(recommendations) < QUALITY_THRESHOLDS["min_recommendations_count"]:
        issues.append(f"Yetersiz öneri sayısı: {len(recommendations)}/{QUALITY_THRESHOLDS['min_recommendations_count']}")
        quality_score -= 20
    
    for i, rec in enumerate(recommendations):
        rec_text = rec.get("action", "") if isinstance(rec, dict) else str(rec)
        if len(rec_text) < QUALITY_THRESHOLDS["min_recommendation_length"]:
            issues.append(f"Öneri {i+1} çok kısa: {len(rec_text)} karakter")
            quality_score -= 10
    
    # 3. Generic phrase kontrolü
    all_text = json.dumps(output, ensure_ascii=False).lower()
    generic_count = sum(1 for phrase in GENERIC_PHRASES if phrase in all_text)
    if generic_count > QUALITY_THRESHOLDS["max_allowed_generic_phrases"]:
        issues.append(f"Çok fazla genel ifade: {generic_count} adet")
        quality_score -= generic_count * 5
    
    # 4. Toplam içerik uzunluğu
    total_length = len(all_text)
    if total_length < QUALITY_THRESHOLDS["min_total_content_length"]:
        issues.append(f"Toplam içerik çok kısa: {total_length} karakter")
        quality_score -= 15
    
    # 5. Metrics kontrolü
    metrics = output.get("metrics", {})
    if "overallScore" not in metrics:
        issues.append("overallScore eksik")
        quality_score -= 10
    
    quality_score = max(0, quality_score)
    is_valid = quality_score >= 60 and len(issues) <= 3
    
    return is_valid, issues, quality_score


def get_self_correction_prompt(original_output: Dict[str, Any], issues: List[str]) -> str:
    """
    Self-correction için prompt oluştur
    
    Args:
        original_output: İlk LLM çıktısı
        issues: Tespit edilen sorunlar
        
    Returns:
        Düzeltme prompt'u
    """
    issues_text = "\n".join(f"- {issue}" for issue in issues)
    
    return f"""
🔄 ÇIKTI DÜZELTME TALEBİ

Önceki çıktında şu sorunlar tespit edildi:

{issues_text}

ÖNCEKİ ÇIKTIN:
```json
{json.dumps(original_output, indent=2, ensure_ascii=False)[:3000]}
```

DÜZELTME TALİMATLARI:
1. Her bulguyu EN AZ 100 karakter olacak şekilde detaylandır
2. Her öneriyi EN AZ 150 karakter olacak şekilde genişlet
3. Genel ifadeler yerine SPESİFİK, AKSİYON ODAKLI ifadeler kullan
4. Sayısal veriler ve sektör karşılaştırmaları ekle
5. Metrics kısmında overallScore (0-100) olduğundan emin ol

⚠️ SADECE DÜZELTİLMİŞ JSON'I DÖNDÜR, BAŞKA BİR ŞEY YAZMA!

```json
"""


# =============================================================================
# ENHANCED PROMPT GENERATOR
# =============================================================================

def enhance_prompt_with_cot(base_prompt: str, include_schema: bool = True) -> str:
    """
    Base prompt'a Chain-of-Thought ve structured output ekle
    
    Args:
        base_prompt: Orijinal prompt
        include_schema: JSON schema eklensin mi
        
    Returns:
        Zenginleştirilmiş prompt
    """
    enhanced = f"""
{base_prompt}

{COT_ANALYSIS_TEMPLATE}

{COT_REASONING_MARKERS}

📝 ÇIKTI FORMATI:

Analizini aşağıdaki JSON formatında ver:

"""
    
    if include_schema:
        enhanced += f"""
JSON SCHEMA (buna UYGUN çıktı üret):
{OUTPUT_SCHEMA_STRING[:2000]}...

"""
    
    enhanced += """
⚠️ KRİTİK: 
- Sadece JSON döndür, başka metin yazma
- Her finding EN AZ 100 karakter
- Her recommendation EN AZ 150 karakter
- metrics.overallScore ZORUNLU (0-100)

```json
"""
    
    return enhanced


# =============================================================================
# SELF-CORRECTION ENGINE
# =============================================================================

class SelfCorrectionEngine:
    """
    LLM çıktılarını otomatik düzelten motor
    """
    
    def __init__(self, gemini_client, generation_config, model_name: str):
        self.client = gemini_client
        self.config = generation_config
        self.model_name = model_name
        self.max_corrections = 2
    
    async def correct_if_needed(
        self,
        output: Dict[str, Any],
        original_prompt: str = ""
    ) -> Tuple[Dict[str, Any], bool, int]:
        """
        Çıktıyı kontrol et ve gerekirse düzelt
        
        Args:
            output: LLM çıktısı
            original_prompt: Orijinal prompt (referans için)
            
        Returns:
            (corrected_output, was_corrected, correction_count)
        """
        is_valid, issues, quality_score = validate_output_quality(output)
        
        if is_valid:
            logger.info(f"✓ Output quality OK (score: {quality_score})")
            return output, False, 0
        
        logger.warning(f"⚠️ Output quality issues detected (score: {quality_score}): {issues}")
        
        corrected_output = output
        correction_count = 0
        
        for attempt in range(self.max_corrections):
            # Düzeltme prompt'u oluştur
            correction_prompt = get_self_correction_prompt(corrected_output, issues)
            
            try:
                # LLM'den düzeltme iste
                logger.info(f"🔄 Self-correction attempt {attempt + 1}/{self.max_corrections}")
                
                response = await self.client.aio.models.generate_content(
                    model=self.model_name,
                    contents=correction_prompt,
                    config=self.config
                )
                
                # Yanıtı parse et
                corrected_text = response.text
                corrected_output = self._parse_correction(corrected_text)
                correction_count += 1
                
                # Tekrar kontrol et
                is_valid, issues, quality_score = validate_output_quality(corrected_output)
                
                if is_valid:
                    logger.info(f"✓ Correction successful (score: {quality_score})")
                    return corrected_output, True, correction_count
                
                logger.warning(f"⚠️ Still has issues after correction: {issues}")
                
            except Exception as e:
                logger.error(f"Self-correction failed: {e}")
                break
        
        # Max corrections reached, return best effort
        logger.warning(f"⚠️ Max corrections reached, returning best effort (score: {quality_score})")
        return corrected_output, correction_count > 0, correction_count
    
    def _parse_correction(self, text: str) -> Dict[str, Any]:
        """Düzeltme yanıtını parse et"""
        # JSON block'u bul
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            if end == -1:
                json_str = text[start:]
            else:
                json_str = text[start:end]
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end == -1:
                json_str = text[start:]
            else:
                json_str = text[start:end]
        else:
            json_str = text
        
        # Parse
        try:
            return json.loads(json_str.strip())
        except json.JSONDecodeError:
            # Repair attempt
            json_str = self._repair_json(json_str)
            return json.loads(json_str)
    
    def _repair_json(self, json_str: str) -> str:
        """Truncated JSON'ı onar"""
        import re
        
        # Remove trailing comma
        json_str = re.sub(r',\s*$', '', json_str)
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        # Balance braces
        open_braces = json_str.count('{')
        close_braces = json_str.count('}')
        open_brackets = json_str.count('[')
        close_brackets = json_str.count(']')
        
        if open_brackets > close_brackets:
            json_str += ']' * (open_brackets - close_brackets)
        if open_braces > close_braces:
            json_str += '}' * (open_braces - close_braces)
        
        return json_str


# =============================================================================
# PREDICTIVE ANALYTICS HELPERS
# =============================================================================

def calculate_viral_potential(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Viral potansiyel hesapla (basit ML yaklaşımı)
    
    Viral potansiyel faktörleri:
    - Engagement rate
    - Save rate
    - Share rate
    - Comment-to-like ratio
    - Growth trend
    """
    engagement_rate = metrics.get("engagementRate", 0)
    save_rate = metrics.get("saveRate", 0)
    share_rate = metrics.get("shareRate", 0)
    comment_like_ratio = metrics.get("commentLikeRatio", 0)
    growth_rate = metrics.get("growthRate", 0)
    
    # Ağırlıklı viral score
    viral_score = (
        engagement_rate * 0.25 +
        save_rate * 100 * 0.20 +
        share_rate * 100 * 0.25 +
        comment_like_ratio * 100 * 0.15 +
        growth_rate * 0.15
    )
    
    # Normalize to 0-100
    viral_score = min(100, max(0, viral_score))
    
    # Kategorize
    if viral_score >= 80:
        viral_category = "high"
        description = "Yüksek viral potansiyel - içerikler keşfet'te öne çıkabilir"
    elif viral_score >= 50:
        viral_category = "medium"
        description = "Orta viral potansiyel - belirli içerikler viral olabilir"
    else:
        viral_category = "low"
        description = "Düşük viral potansiyel - organik büyüme zor olacak"
    
    return {
        "viralScore": round(viral_score, 1),
        "viralCategory": viral_category,
        "description": description,
        "factors": {
            "engagementContribution": round(engagement_rate * 0.25, 2),
            "saveContribution": round(save_rate * 100 * 0.20, 2),
            "shareContribution": round(share_rate * 100 * 0.25, 2),
            "commentContribution": round(comment_like_ratio * 100 * 0.15, 2),
            "growthContribution": round(growth_rate * 0.15, 2),
        }
    }


def predict_growth_trajectory(
    current_followers: int,
    growth_rate: float,
    engagement_rate: float,
    months: int = 6
) -> Dict[str, Any]:
    """
    Büyüme trajektorisi tahmin et
    
    Basit exponential growth model:
    followers(t) = followers(0) * (1 + adjusted_rate)^t
    
    adjusted_rate = base_rate * engagement_factor
    """
    import math
    
    # Engagement faktörü (yüksek engagement = daha hızlı büyüme)
    engagement_factor = 1 + (engagement_rate / 100)
    
    # Adjusted growth rate
    adjusted_rate = (growth_rate / 100) * engagement_factor
    
    # Aylik tahminler
    projections = []
    for month in range(1, months + 1):
        projected = current_followers * math.pow(1 + adjusted_rate, month)
        projections.append({
            "month": month,
            "projected_followers": int(projected),
            "growth_from_current": round((projected - current_followers) / current_followers * 100, 1)
        })
    
    # 6 aylık tahmin
    final_projection = projections[-1]["projected_followers"] if projections else current_followers
    
    return {
        "current_followers": current_followers,
        "base_growth_rate": growth_rate,
        "adjusted_growth_rate": round(adjusted_rate * 100, 2),
        "engagement_factor": round(engagement_factor, 2),
        "projections": projections,
        "6_month_projection": final_projection,
        "6_month_growth_percent": round((final_projection - current_followers) / current_followers * 100, 1),
        "confidence": "medium" if engagement_rate > 1.5 else "low"
    }
