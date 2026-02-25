# DeepSeek Final Analyst Agent
# Tüm agent sonuçlarını okuyup kullanıcıya son, bütünleşik yorumu veren ajan
"""
DeepSeek Final Analyst

Bu ajan:
1. Tüm PhD ajanlarının sonuçlarını okur
2. Governor audit sonuçlarını değerlendirir
3. Tutarsızlıkları tespit eder
4. Kullanıcıya acımasız, dürüst ve yapıcı bir final yorum verir
5. "Patron gibi konuş" - direkt, aksiyona yönelik, vakit kaybettirmeyen

DeepSeek API: OpenAI uyumlu endpoint kullanır
"""

import asyncio
import json
import logging
import os
import httpx
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DeepSeekFinalAnalyst:
    """
    DeepSeek Final Analyst - Tüm analizlerin sentezleyicisi
    
    Rol: "Acımasız Danışman" - Yağcılık yok, gerçekler var
    
    Çıktı Formatı:
    1. DURUM ÖZETİ (3 cümle max)
    2. EN KRİTİK 3 SORUN (öncelik sırasıyla)
    3. HEMEN YAPILACAKLAR (bu hafta)
    4. YAPMAMASI GEREKENLER (yaygın hatalar)
    5. BAŞARI TAHMİNİ (brutally honest)
    """
    
    # DeepSeek System Prompt - Acımasız Danışman Karakteri
    SYSTEM_PROMPT = """Sen "Chief Reality Officer" - Acımasız Instagram Danışmanısın.

KARAKTERİN:
- Vakit kaybetmezsin, direkt konuşursun
- Yağcılık YASAK - kötüyse "kötü" dersin
- Rakamlar yalan söylemez - her yorumun veriyle desteklenmeli
- "Potansiyel var" gibi boş laflar YASAK
- Kullanıcı senden övgü değil, ÇÖZÜM bekliyor

KONUŞMA TARZI:
- Patron gibi konuş (CEO'ya rapor veriyorsun)
- Kısa cümleler, net mesajlar
- Emoji YASAK
- "Belki", "muhtemelen", "olabilir" YASAK - kesin konuş
- Türkçe yaz

YASAKLI KELİMELER (bunları ASLA kullanma):
- "harika", "mükemmel", "süper", "muhteşem"
- "potansiyel", "umut verici", "gelecek vadeden"
- "ancak", "fakat" ile başlayan pozitif cümleler
- "biraz daha çalışarak" gibi yumuşatıcı ifadeler

FORMAT:
1. DURUM (max 3 cümle - acı gerçek)
2. KRİTİK SORUNLAR (3 madde, öncelik sırasıyla)
3. BU HAFTA YAP (somut 3 aksiyon)
4. YAPMA (2 yaygın hata uyarısı)
5. TAHMİN (6 ay sonra nerede olur - koşullu)"""

    def __init__(self):
        """Initialize DeepSeek client"""
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        if not self.api_key:
            logger.warning("DEEPSEEK_API_KEY not set - Final Analyst will be disabled")
        
        # HTTP client with timeout
        self.timeout = httpx.Timeout(60.0, connect=10.0)
        
    async def analyze(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tüm analiz sonuçlarını değerlendirip final yorum üret
        
        Args:
            analysis_data: Tüm agent sonuçlarını içeren dict
            
        Returns:
            Final analyst raporu
        """
        if not self.api_key:
            return self._get_disabled_response()
        
        try:
            # Analiz verilerini hazırla
            context = self._prepare_context(analysis_data)
            
            # DeepSeek API'ye gönder
            response = await self._call_deepseek(context)
            
            # Yanıtı parse et
            parsed = self._parse_response(response)
            
            return {
                "agent": "deepseekFinalAnalyst",
                "error": False,
                "finalVerdict": parsed,
                "rawResponse": response,
                "timestamp": datetime.utcnow().isoformat(),
                "modelUsed": self.model
            }
            
        except Exception as e:
            logger.error(f"DeepSeek Final Analyst error: {e}")
            return {
                "agent": "deepseekFinalAnalyst",
                "error": True,
                "errorMessage": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _prepare_context(self, analysis_data: Dict[str, Any]) -> str:
        """Tüm analiz verilerini DeepSeek için hazırla"""
        
        username = analysis_data.get("username", "unknown")
        final_score = analysis_data.get("finalScore", 0)
        final_grade = analysis_data.get("finalGrade", "F")
        agent_results = analysis_data.get("agentResults", {})
        business_identity = analysis_data.get("businessIdentity", {})
        hard_validation = analysis_data.get("hardValidation", {})
        
        # Temel metrikleri çıkar
        basic_metrics = self._extract_basic_metrics(analysis_data)
        
        # Agent sonuçlarını özetle
        agent_summaries = self._summarize_agents(agent_results)
        
        # Validation ihlallerini listele
        violations = hard_validation.get("violations", [])
        violation_text = "\n".join([f"- {v.get('rule')}: {v.get('message')}" for v in violations]) if violations else "Yok"
        
        context = f"""
HESAP: @{username}
GENEL SKOR: {final_score}/100 (Not: {final_grade})

TEMEL METRİKLER:
{json.dumps(basic_metrics, indent=2, ensure_ascii=False)}

İŞLETME KİMLİĞİ:
- Tip: {business_identity.get('account_type', 'Belirsiz')}
- Hizmet Sağlayıcı mı: {business_identity.get('is_service_provider', False)}
- Doğru Başarı Metrikleri: {business_identity.get('correct_success_metrics', [])}

AGENT ANALİZ ÖZETLERİ:
{agent_summaries}

VALİDASYON İHLALLERİ:
{violation_text}

GÖREV: Bu verilere dayanarak kullanıcıya final yorumunu ver. Acımasız ol, gerçekleri söyle, somut aksiyonlar öner.
"""
        return context
    
    def _extract_basic_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Temel metrikleri çıkar"""
        # Account data'dan
        account = data.get("accountData", data)
        
        return {
            "followers": account.get("followers", account.get("followersCount", 0)),
            "following": account.get("following", account.get("followingCount", 0)),
            "posts": account.get("posts", account.get("postsCount", 0)),
            "engagement_rate": account.get("engagementRate", 0),
            "avg_likes": account.get("avgLikes", 0),
            "avg_comments": account.get("avgComments", 0),
        }
    
    def _summarize_agents(self, agent_results: Dict[str, Any]) -> str:
        """Agent sonuçlarını özetli metin haline getir"""
        summaries = []
        
        for agent_name, result in agent_results.items():
            if not isinstance(result, dict):
                continue
            
            # Agent skoru
            metrics = result.get("metrics", {})
            score = metrics.get("overallScore", metrics.get("score", "N/A"))
            
            # Findings özeti
            findings = result.get("findings", [])
            findings_text = ""
            if findings:
                if isinstance(findings[0], dict):
                    findings_text = "; ".join([f.get("finding", "")[:100] for f in findings[:3]])
                else:
                    findings_text = "; ".join([str(f)[:100] for f in findings[:3]])
            
            # Veto durumu
            vetoed = " [VETOED]" if result.get("vetoed") else ""
            
            summaries.append(f"""
{agent_name.upper()}{vetoed}:
- Skor: {score}
- Bulgular: {findings_text[:200]}...
""")
        
        return "\n".join(summaries)
    
    async def _call_deepseek(self, context: str) -> str:
        """DeepSeek API'yi çağır"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": context}
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """DeepSeek yanıtını yapılandırılmış formata çevir"""
        
        sections = {
            "situation": "",
            "critical_issues": [],
            "this_week_actions": [],
            "dont_do": [],
            "prediction": ""
        }
        
        lines = response.strip().split("\n")
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Section headers
            line_lower = line.lower()
            if "durum" in line_lower or "özet" in line_lower:
                if current_section and current_content:
                    sections[current_section] = self._process_section(current_section, current_content)
                current_section = "situation"
                current_content = []
            elif "kritik" in line_lower or "sorun" in line_lower:
                if current_section and current_content:
                    sections[current_section] = self._process_section(current_section, current_content)
                current_section = "critical_issues"
                current_content = []
            elif "bu hafta" in line_lower or "yap" in line_lower and "yapma" not in line_lower:
                if current_section and current_content:
                    sections[current_section] = self._process_section(current_section, current_content)
                current_section = "this_week_actions"
                current_content = []
            elif "yapma" in line_lower:
                if current_section and current_content:
                    sections[current_section] = self._process_section(current_section, current_content)
                current_section = "dont_do"
                current_content = []
            elif "tahmin" in line_lower or "6 ay" in line_lower:
                if current_section and current_content:
                    sections[current_section] = self._process_section(current_section, current_content)
                current_section = "prediction"
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Son section'ı kaydet
        if current_section and current_content:
            sections[current_section] = self._process_section(current_section, current_content)
        
        # Parse edilemezse ham response'u kullan
        if not any(sections.values()):
            sections["situation"] = response[:500]
            sections["critical_issues"] = ["Detaylı analiz için ham yanıta bakın"]
            sections["prediction"] = "Manuel değerlendirme gerekli"
        
        return sections
    
    def _process_section(self, section: str, content: List[str]) -> Any:
        """Section içeriğini işle"""
        if section in ["critical_issues", "this_week_actions", "dont_do"]:
            # Liste formatında döndür
            items = []
            for line in content:
                # Madde işaretlerini temizle
                cleaned = line.lstrip("-•*0123456789.) ").strip()
                if cleaned:
                    items.append(cleaned)
            return items
        else:
            # String olarak birleştir
            return " ".join(content)
    
    def _get_disabled_response(self) -> Dict[str, Any]:
        """API key yoksa döndürülecek yanıt"""
        return {
            "agent": "deepseekFinalAnalyst",
            "error": False,
            "disabled": True,
            "message": "DeepSeek Final Analyst devre dışı - DEEPSEEK_API_KEY ayarlanmamış",
            "timestamp": datetime.utcnow().isoformat()
        }


# Factory function
def create_deepseek_analyst() -> DeepSeekFinalAnalyst:
    """Create DeepSeek Final Analyst instance"""
    return DeepSeekFinalAnalyst()
