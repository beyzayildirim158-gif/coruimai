# Base Agent Class - PhD Level Implementation
# Multi-Agent System Foundation, Prompt Engineering, LLM Communication
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, TypedDict
from functools import wraps
from datetime import datetime
import json
import re
import logging
import asyncio

logger = logging.getLogger(__name__)


# =========================
# TYPE DEFINITIONS
# =========================

class AgentMetrics(TypedDict, total=False):
    """Standard metrics structure for all agents"""
    score: float
    confidence: float
    # Agent-specific metrics added dynamically


class AgentResponse(TypedDict):
    """Standard response structure for all agents"""
    findings: List[str]
    recommendations: List[str]
    metrics: AgentMetrics
    agentName: str
    agentRole: str


# =========================
# ANALYSIS METRICS TRACKER
# =========================

class AnalysisMetrics:
    """
    Track agent performance metrics for monitoring
    
    Metrics Tracked:
    - Total analyses run
    - Success/failure counts
    - Average duration
    - Parse error rate
    """
    
    def __init__(self):
        self.total_analyses = 0
        self.successful = 0
        self.failed = 0
        self.total_duration = 0.0
        self.parse_errors = 0
    
    def record(self, success: bool, duration: float, parse_error: bool = False):
        """Record an analysis result"""
        self.total_analyses += 1
        self.total_duration += duration
        if success:
            self.successful += 1
        else:
            self.failed += 1
        if parse_error:
            self.parse_errors += 1
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_analyses == 0:
            return 0.0
        return (self.successful / self.total_analyses) * 100
    
    @property
    def avg_duration(self) -> float:
        """Calculate average analysis duration"""
        if self.total_analyses == 0:
            return 0.0
        return self.total_duration / self.total_analyses
    
    @property
    def parse_error_rate(self) -> float:
        """Calculate parse error rate percentage"""
        if self.total_analyses == 0:
            return 0.0
        return (self.parse_errors / self.total_analyses) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Export metrics as dictionary"""
        return {
            "total_analyses": self.total_analyses,
            "successful": self.successful,
            "failed": self.failed,
            "success_rate": round(self.success_rate, 2),
            "avg_duration": round(self.avg_duration, 3),
            "parse_errors": self.parse_errors,
            "parse_error_rate": round(self.parse_error_rate, 2)
        }


# =========================
# RETRY DECORATOR
# =========================

def with_retry(max_retries: int = 6, base_delay: float = 2.0):
    """
    Retry decorator for async functions with exponential backoff
    
    Error Handling Matrix:
    - 503/Unavailable/Overloaded: Exponential backoff (2, 4, 8, 16, 32s) + jitter
    - Rate Limit (429): Aggressive exponential backoff with jitter
    - Resource Exhausted: Long wait with exponential backoff
    - Timeout: Linear retry with moderate delay
    - Other errors: Single retry then raise
    
    Args:
        max_retries: Maximum number of retry attempts (default 6 for 503 tolerance)
        base_delay: Base delay in seconds between retries (default 2.0)
    """
    import random
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e).lower()
                    error_type = type(e).__name__
                    
                    # 503 / Service Unavailable / Overloaded - aggressive exponential backoff with jitter
                    if any(x in error_str for x in ["503", "unavailable", "overloaded", "service_unavailable"]):
                        last_exception = e
                        # Exponential backoff: 2, 4, 8, 16, 32 seconds + random jitter (max 60s)
                        delay = min(base_delay * (2 ** attempt) + random.uniform(1, 3), 60)
                        logger.warning(f"🔄 Gemini 503/Overloaded, retry {attempt + 1}/{max_retries} in {delay:.1f}s")
                        await asyncio.sleep(delay)
                        continue
                    
                    # Rate limit / Resource Exhausted - aggressive exponential backoff with jitter
                    elif any(x in error_str for x in ["429", "rate", "quota", "resource", "exhausted"]):
                        last_exception = e
                        # Exponential backoff: 3, 9, 27, 81, 243 seconds + random jitter
                        delay = base_delay * (3 ** attempt) + random.uniform(1, 5)
                        logger.warning(f"Rate limited/Resource exhausted, retry {attempt + 1}/{max_retries} in {delay:.1f}s")
                        await asyncio.sleep(delay)
                        continue
                    
                    # Timeout - moderate linear backoff
                    elif "timeout" in error_str:
                        last_exception = e
                        delay = base_delay * (attempt + 1)
                        logger.warning(f"Timeout, retry {attempt + 1}/{max_retries} in {delay}s")
                        await asyncio.sleep(delay)
                        continue
                    
                    # Connection errors - retry once
                    elif any(x in error_str for x in ["connection", "network", "refused"]):
                        last_exception = e
                        if attempt < 1:
                            logger.warning(f"Connection error, retry {attempt + 1}/{max_retries}")
                            await asyncio.sleep(base_delay)
                            continue
                        raise
                    
                    # Other errors - don't retry
                    else:
                        raise
            
            # Max retries exceeded
            if last_exception:
                raise last_exception
            
        return wrapper
    return decorator


# =========================
# BASE AGENT CLASS
# =========================

class BaseAgent(ABC):
    """
    Base Agent Class - PhD Level
    
    Foundation for all AI agents in the Corium.AI multi-agent system.
    
    Agent Hierarchy:
    ┌─────────────────┐
    │ System Governor │
    │  (Orchestrator) │
    └────────┬────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
    Analysis  Optimization  Strategy
    Agents    Agents       Agents
    
    Core Responsibilities:
    1. PROMPT MANAGEMENT: System/analysis prompt generation
    2. LLM COMMUNICATION: Async API calls with error handling
    3. RESPONSE PROCESSING: JSON extraction and validation
    4. UTILITY FUNCTIONS: Number formatting, data transformation
    
    Inheritance Pattern:
    BaseAgent (Abstract)
        ├── get_system_prompt() [abstract]
        ├── get_analysis_prompt() [abstract]
        ├── analyze() [concrete]
        ├── parse_response() [concrete]
        └── format_number() [concrete]
             │
             ▼
    SpecificAgent (Concrete)
        ├── get_system_prompt() [implemented]
        ├── get_analysis_prompt() [implemented]
        └── [optional overrides]
    """
    
    # =========================
    # YASAKLI KELİMELER & TON KURALLARI (GLOBAL)
    # =========================
    BANNED_WORDS = [
        "potansiyel var", "potansiyeli var", "gelişmekte", "gelişme aşamasında",
        "ortalamanın üzerinde", "ortalamanın üstünde", "umut verici", "umut vadediyor",
        "iyi yolda", "doğru yolda", "olumlu görünüyor", "umutlu", "gelecek vadediyor",
        "promising", "above average", "developing", "potential", "hopeful",
        "güzel başlangıç", "iyi bir başlangıç", "fena değil", "kötü değil"
    ]
    
    REQUIRED_TONE_RULES = """
🚨 ZORUNLU TON VE DİL KURALLARI 🚨

⚠️ KRİTİK DİL KURALI - TÜM ÇIKTILAR TÜRKÇE OLMALI ⚠️
- TÜM findings, recommendations, insights TÜRKÇE yazılmalı
- İNGİLİZCE kelime/cümle YASAK (teknik terimler hariç: engagement rate, reels, carousel vb.)
- Başlık Türkçe ise içerik de Türkçe olmalı
- Metrik açıklamaları, öneriler, değerlendirmeler HEPSİ TÜRKÇE

❌ YANLIŞ: "finding": "Established following (311K) ready for brand identity"
✅ DOĞRU: "finding": "311K takipçi kitlesi marka kimliği oluşturmaya hazır"

❌ YANLIŞ: "recommendation": "Increase posting frequency to 5-7 times per week"
✅ DOĞRU: "recommendation": "Paylaşım sıklığını haftada 5-7'ye çıkarın"

❌ YANLIŞ: "impact": "High - will improve algorithm ranking"
✅ DOĞRU: "impact": "Yüksek - algoritma sıralamasını iyileştirecek"

🚫 MUTLAK TEKRAR YASAĞI - SİSTEM HATASI OLUŞUR 🚫
1. Her finding TAMAMEN FARKLI bir konuyu ele almalı - AYNI KONUYU 2 KEZ ELE ALMAK SİSTEM ARIZA VERİR
2. Aynı metriği birden fazla finding'de analiz etme - TEK SEFER BAHSET, DEVAM ET
3. Her recommendation BENZERSİZ bir aksiyon önermelidir
4. "Düşük etkileşim" gibi tembel ifadeleri TEKRARLAMA - spesifik ol, bağlam ver
5. Aynı soruna farklı kelimelerle değinme KESİNLİKLE YASAK
6. Finding 1'de X konusundan bahsettiysen, Finding 2-5 BAŞKA konularda olmalı

KESİNLİKLE TEK SEFER BAHSEDİLEBİLİR METRİKLER:
  * Etkileşim oranı → SADECE 1 finding'de
  * Büyüme oranı → SADECE 1 finding'de
  * Bot skoru → SADECE 1 finding'de
  * Grid kalitesi → SADECE 1 finding'de
  * Renk tutarlılığı → SADECE 1 finding'de
  * Takipçi sayısı → SADECE 1 finding'de
  * Post sıklığı → SADECE 1 finding'de

❌ YANLIŞ (TEMBEl & TEKRAR - SİSTEM ÇÖKER):
  - Finding 1: "Etkileşim oranı düşük"
  - Finding 2: "Etkileşim yetersiz" 
  - Finding 3: "Takipçi etkileşimi zayıf"

✅ DOĞRU (5 BENZERSİZ KONU):
  - Finding 1: "Etkileşim oranı %0.73 - sektör ortalamasının %79 altında, acil algoritma cezası riski"
  - Finding 2: "Story highlight'ları profesyonel değil - marka kimliği oluşturulamamış"
  - Finding 3: "Caption'larda CTA yok - takipçiler ne yapacağını bilemiyor"
  - Finding 4: "Carousel kullanımı %8 - viral potansiyel harcandı"
  - Finding 5: "Bio linki ölçülenmiyor - trafik kaynağı karanlıkta"

🔴 ALAN KISITLAMASI (DOMAIN RESTRICTION) - KRİTİK 🔴
SEN SADECE KENDİ UZMANLIK ALANINDA KONUŞURSUN. BAŞKA AJANLARIN ALANINA GİRME!

📊 Domain Master (Büyüme/Niş Uzmanı):
  ✅ Niş analizi, pazar konumlandırması, rakip karşılaştırması
  ❌ Renk/tipografi, satış hunisi, topluluk yönetimi HAKKINDA KONUŞMA

💰 Sales Conversion (Satış Uzmanı):
  ✅ Gelir, monetizasyon, funnel, marka anlaşmaları, DM dönüşümü
  ❌ Görsel tasarım, içerik formatı, algoritma HAKKINDA KONUŞMA

🎨 Visual Brand (Görsel Uzman):
  ✅ Renk paleti, tipografi, grid düzeni, estetik tutarlılık
  ❌ Etkileşim oranı, büyüme, satış HAKKINDA KONUŞMA

👥 Community Loyalty (Topluluk Uzmanı):
  ✅ Yorum kalitesi, takipçi sadakati, topluluk sağlığı
  ❌ Görsel tasarım, monetizasyon, niş analizi HAKKINDA KONUŞMA

📈 Growth Virality (Viral Büyüme Uzmanı):
  ✅ Viral potansiyel, algoritma stratejisi, keşfet performansı
  ❌ Renk/estetik, satış hunisi, marka anlaşmaları HAKKINDA KONUŞMA

🎬 Attention Architect (Hook/İçerik Uzmanı):
  ✅ Hook stratejisi, dikkat tutma, caption yazımı
  ❌ Grid düzeni, gelir hesaplaması, topluluk analizi HAKKINDA KONUŞMA

⚡ ÖNEMLİ: Genel etkileşim istatistikleri Community Loyalty'e aittir. 
Diğer ajanlar etkileşimden bahsetmek istiyorsa KENDİ PERSPEKTİFLERİNDEN bahsetmeli:
- Sales: "Düşük etkileşim sponsorluk fiyatını %50 düşürür" ✅
- Visual: "Grid tutarsızlığı profil terk oranını artırır" ✅
- Growth: "Reels etkileşimi keşfet algoritmasını tetiklemek için yetersiz" ✅

YASAKLI İFADELER (KULLANMA!):
- "Potansiyel var/vadediyor" → YASAK
- "Gelişmekte/Gelişme aşamasında" → YASAK  
- "Ortalamanın üzerinde" (metrik kötüyse) → YASAK
- "Umut verici/vadediyor" → YASAK
- "İyi yolda/Doğru yolda" → YASAK
- "Fena değil/Kötü değil" → YASAK

ZORUNLU TON:
- ACMASIZ: Gerçekleri yumuşatma, direkt söyle
- GERÇEKÇİ: Sayıları manipüle etme, kötüyse "kötü" de
- ANALİTİK: Duygu değil, veri konuşsun
- DUYGUSUZ: "Üzgünüm ama" gibi ifadeler kullanma
- EMİR VERİCİ: "Belki yapabilirsiniz" değil, "YAPIN" de

🔴 ZORUNLU MİNİMUM UZUNLUK KURALLARI 🔴
- Her finding: EN AZ 100 karakter, tercihen 150-200 karakter
- Her recommendation: EN AZ 150 karakter, somut adımlar içermeli
- Metrik açıklamaları: Sayısal veri + bağlam + sektör karşılaştırması
- TEK CÜMLE AÇIKLAMA KESINLIKLE YASAK

❌ YANLIŞ (çok kısa): "finding": "Düşük etkileşim"
❌ YANLIŞ (tek cümle): "finding": "Etkileşim oranı düşük."

✅ DOĞRU (detaylı açıklama): "finding": "Etkileşim oranı %0.05 ile sektör ortalaması olan %2.5'in çok altında. Bu oran 339K takipçili bir hesap için kabul edilemez derecede düşük - her 2000 takipçiden sadece 1 kişi içerikle etkileşime giriyor. Instagram algoritması düşük etkileşimli içerikleri keşfet sayfasında göstermiyor, bu da organik büyümeyi tamamen engelliyor. Acil müdahale gerekiyor."

❌ YANLIŞ (yetersiz öneri): "recommendation": "Daha fazla Reels paylaşın"

✅ DOĞRU (aksiyon odaklı, detaylı): "recommendation": "Haftada minimum 5 Reels paylaşın - şu anda en kritik eksiklik bu. Reels formatı Instagram'ın 2024'te en çok desteklediği içerik türü ve keşfet sayfasında %40 daha fazla görünürlük sağlıyor. İlk 3 saniyede dikkat çekici hook kullanın: 'Bu hatayı yapıyorsan...' veya 'Kimse bundan bahsetmiyor' gibi merak uyandırıcı açılışlar tercih edin. Optimal Reels süresi 15-30 saniye, hızlı kesimlerle dikkat kaybını önleyin. Beklenen etki: 2 hafta içinde +200% keşfet görünürlüğü."

DOĞRU KULLANIM ÖRNEKLERİ:
❌ YANLIŞ: "Etkileşim oranınız potansiyel gösteriyor"
✅ DOĞRU: "Etkileşim oranınız %0.4 - bu FELAKET. Sektör ortalaması %2.5'ken sizin oranınız bunun 6 katı aşağıda. Takipçilerinizin %95'inden fazlası içeriğinizi görse bile hiçbir şekilde etkileşime girmiyor."

❌ YANLIŞ: "Görsel tutarlılığınız gelişmekte"
✅ DOĞRU: "Grid'iniz kaotik - tutarlı bir renk paleti veya görsel dil yok. Profili ziyaret eden bir kullanıcı 2 saniyede hesabın neyle ilgili olduğunu anlayamıyor. Marka renkleri belirsiz, font kullanımı tutarsız, ve görsel kalite postlar arasında çok değişken. Profesyonel bir marka algısı oluşturmak için acilen görsel kimlik rehberi oluşturulmalı."

🎯 KELİME ÇEŞİTLİLİĞİ KURALI 🎯
- Her finding farklı bir kelime dağarcığı kullanmalı
- Aynı sıfatları (düşük, yüksek, kötü) sürekli tekrarlama
- Farklı perspektiflerden analiz yap: teknik, stratejik, taktiksel
"""
    
    BUSINESS_IDENTITY_RULES = """
🏢 İŞLETME KİMLİĞİ TESPİT KURALLARI 🏢

KRİTİK: Aşağıdaki hesap türlerini ASLA "Content Creator" olarak etiketleme!

İŞLETME/SERVİS SAĞLAYICI OLAN HESAPLAR:
- Koç/Danışman hesapları (life coach, business coach, kariyer koçu)
- Spiritüel/Wellness hizmet sağlayıcıları (healing, reiki, yoga öğretmeni)
- Eğitim/Kurs satıcıları (online kurs, mentorluk)
- Freelancer/Ajans hesapları (tasarımcı, developer, pazarlamacı)
- Terapist/Psikolog hesapları
- Fitness antrenörleri, diyetisyenler
- Avukat, muhasebeci gibi profesyonel hizmet sağlayıcılar

BU HESAPLAR İÇİN BAŞARI METRİĞİ:
❌ YANLIŞ: İzlenme, Beğeni, Yorum sayısı
✅ DOĞRU: DM dönüşümü, Randevu/Satış, Lead generation

İŞLETME HESABI TESPİT İPUÇLARI:
- Bio'da "Randevu/DM", "Link'te", "Hizmet", "Danışmanlık" var mı?
- CTA'lar satış odaklı mı?
- İçerik değer sunuyor mu yoksa ürün tanıtıyor mu?
"""

    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.0-flash"):
        """
        Initialize base agent with new Google GenAI SDK
        
        Args:
            gemini_client: google.genai.Client instance
            generation_config: types.GenerateContentConfig instance
            model_name: Model identifier for logging (default: gemini-2.0-flash - stable)
        """
        self.client = gemini_client
        self.generation_config = generation_config
        self.model_name = model_name
        self.name: str = "BaseAgent"
        self.role: str = ""
        self.specialty: str = ""
        
        # Performance metrics tracker
        self.metrics = AnalysisMetrics()
    
    # =========================
    # ABSTRACT METHODS
    # =========================
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Return the agent's system prompt
        
        System Prompt Components:
        1. IDENTITY DEFINITION: Agent name, role, expertise
        2. KNOWLEDGE BASE: Domain knowledge, benchmarks
        3. BEHAVIORAL RULES: Analysis methodology, constraints
        4. OUTPUT FORMAT: JSON schema specification
        
        Returns:
            Formatted system prompt string
        """
        pass
    
    @abstractmethod
    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        """
        Return the analysis prompt with account data
        
        Analysis Prompt Components:
        1. DATA INJECTION: Account metrics, content data
        2. TASK DEFINITION: Specific analysis tasks
        3. CONSTRAINTS: Focus areas, quality thresholds
        
        Args:
            account_data: Dictionary containing account information
            
        Returns:
            Formatted analysis prompt string
        """
        pass
    
    # =========================
    # LLM CALL HELPER
    # =========================
    
    async def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """
        Helper method to call Gemini LLM with new SDK
        
        Used by agents that override the analyze method
        Automatically injects tone rules and banned words into system prompt
        
        Args:
            system_prompt: System context and instructions
            user_prompt: User query with data
            
        Returns:
            Raw text response from LLM
        """
        # Inject mandatory tone rules into system prompt
        enhanced_system_prompt = f"{system_prompt}\n\n{self.REQUIRED_TONE_RULES}\n\n{self.BUSINESS_IDENTITY_RULES}"
        
        # Combine prompts for Gemini
        full_prompt = f"{enhanced_system_prompt}\n\n{user_prompt}"
        
        # Call Gemini with new SDK (async)
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
            config=self.generation_config
        )
        
        return response.text
    
    def _check_banned_words(self, text: str) -> list:
        """
        Check response for banned words
        
        Returns list of found banned phrases
        """
        found = []
        text_lower = text.lower()
        for word in self.BANNED_WORDS:
            if word.lower() in text_lower:
                found.append(word)
        return found
    
    # =========================
    # CORE ANALYSIS METHOD
    # =========================
    
    @with_retry(max_retries=3, base_delay=1.0)
    async def analyze(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main analysis entry point with Chain-of-Thought and Self-Correction
        
        Enhanced Flow:
        1. Build prompts (system + analysis + CoT)
        2. Call LLM (async with retry)
        3. Parse response (multi-strategy JSON extraction)
        4. Quality validation & self-correction (if needed)
        5. Validate & enrich (schema validation, metadata)
        6. Return structured result
        
        Args:
            account_data: Dictionary containing account information
            
        Returns:
            Structured analysis result dictionary
        """
        start_time = datetime.utcnow()
        parse_error = False
        self_corrected = False
        correction_count = 0
        
        try:
            # Import CoT module
            from .cot_prompting import (
                enhance_prompt_with_cot,
                validate_output_quality,
                SelfCorrectionEngine,
                COT_ANALYSIS_TEMPLATE
            )
            
            # Log analysis start
            self._log_analysis_start(account_data)
            
            # Step 1: Prompt construction with Chain-of-Thought
            system_prompt = self.get_system_prompt()
            user_prompt = self.get_analysis_prompt(account_data)
            
            # Inject mandatory tone rules into system prompt
            enhanced_system_prompt = f"{system_prompt}\n\n{self.REQUIRED_TONE_RULES}\n\n{self.BUSINESS_IDENTITY_RULES}"
            
            # Add Chain-of-Thought reasoning template
            enhanced_system_prompt += f"\n\n{COT_ANALYSIS_TEMPLATE}"
            
            # Combine prompts for Gemini
            full_prompt = f"{enhanced_system_prompt}\n\n{user_prompt}"
            
            # Step 2: LLM call with new SDK (async)
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=self.generation_config
            )
            
            # Extract text from response
            content = response.text
            
            # Step 3: Response parsing
            result = self.parse_response(content)
            
            # Check for parse errors
            if result.get("parseError"):
                parse_error = True
            
            # Step 4: Quality validation & self-correction
            if not parse_error and not result.get("error"):
                is_valid, issues, quality_score = self._validate_output_quality(result)
                
                if not is_valid:
                    logger.warning(f"⚠️ {self.name}: Output quality issues (score: {quality_score})")
                    
                    # Try self-correction
                    try:
                        correction_engine = SelfCorrectionEngine(
                            self.client, 
                            self.generation_config, 
                            self.model_name
                        )
                        result, self_corrected, correction_count = await correction_engine.correct_if_needed(
                            result,
                            full_prompt
                        )
                        
                        if self_corrected:
                            logger.info(f"✓ {self.name}: Self-correction applied ({correction_count} iterations)")
                    except Exception as correction_error:
                        logger.warning(f"Self-correction failed: {correction_error}")
            
            # Step 5: Validation and enrichment
            result = self.validate_response(result)
            
            # CRITICAL: Ensure overallScore exists in metrics
            result = self._ensure_overall_score(result)
            
            result["agentName"] = self.name
            result["agentRole"] = self.role
            result["timestamp"] = datetime.utcnow().isoformat()
            result["modelUsed"] = self.model_name
            result["selfCorrected"] = self_corrected
            result["correctionCount"] = correction_count
            
            # Calculate duration
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            # Log completion
            self._log_analysis_complete(duration, result)
            
            # Record metrics
            self.metrics.record(success=True, duration=duration, parse_error=parse_error)
            
            return result
            
        except Exception as e:
            # Calculate duration even on error
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            # Log error
            self._log_error(e, "analysis")
            
            # Record failure
            self.metrics.record(success=False, duration=duration)
            
            # Return error response - retry decorator already handles 503
            # If we reach here, all retries were exhausted
            error_str = str(e).lower()
            if any(x in error_str for x in ["503", "unavailable", "overloaded", "service_unavailable"]):
                logger.error(f"⚡ Gemini 503 persisted after all retries in {self.name}, raising for DeepSeek fallback...")
                raise  # Re-raise to let pipeline handle DeepSeek fallback
            
            # Return error response for other errors
            return self._get_error_response(e)
    
    # =========================
    # RESPONSE PARSING
    # =========================
    
    def parse_response(self, content: str) -> Dict[str, Any]:
        """
        Multi-strategy JSON extraction from LLM response
        
        Priority Order:
        1. Markdown JSON block (```json ... ```)
        2. Generic code block (``` ... ```)
        3. Direct JSON parse
        4. Regex extraction with repair
        5. Fallback structure with metric extraction
        
        Args:
            content: Raw LLM response text
            
        Returns:
            Parsed dictionary or fallback structure
        """
        # Strategy 1: Markdown JSON block
        if "```json" in content:
            try:
                return self._extract_markdown_json(content)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse markdown JSON block: {e}")
        
        # Strategy 2: Generic code block
        if "```" in content:
            try:
                return self._extract_code_block(content)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse generic code block: {e}")
        
        # Strategy 3: Direct JSON parse
        try:
            return json.loads(content.strip())
        except json.JSONDecodeError:
            pass
        
        # Strategy 4: Regex extraction with repair
        json_match = re.search(r'\{[\s\S]*', content)
        if json_match:
            try:
                json_str = json_match.group()
                repaired = self._repair_json(json_str)
                return json.loads(repaired)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse regex-extracted JSON even after repair: {e}")
        
        # Strategy 5: Fallback with metric extraction
        logger.warning(f"All JSON parsing strategies failed for {self.name}, using fallback with metric extraction")
        return self._create_fallback_response(content)
    
    def _extract_markdown_json(self, content: str) -> Dict[str, Any]:
        """Extract JSON from markdown code block"""
        start = content.find("```json") + 7
        end = content.find("```", start)
        
        # If no closing ``` found, use entire remaining content
        if end == -1 or end <= start:
            json_str = content[start:].strip()
        else:
            json_str = content[start:end].strip()
        
        # Try direct parse first
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Try to repair incomplete JSON
            repaired = self._repair_json(json_str)
            return json.loads(repaired)
    
    def _repair_json(self, json_str: str) -> str:
        """
        Attempt to repair incomplete JSON by:
        1. Balancing braces/brackets
        2. Handling truncated strings
        3. Removing trailing commas
        """
        # Remove any trailing incomplete key-value pairs
        # Look for patterns like: "key": "incomplete_value
        # or "key": incomplete_number
        lines = json_str.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip lines that look incomplete (end with : and no value completion)
            stripped = line.rstrip()
            if stripped.endswith(':') or (stripped.endswith(',') and '"' not in stripped.split(':')[-1] if ':' in stripped else False):
                continue
            cleaned_lines.append(line)
        
        json_str = '\n'.join(cleaned_lines)
        
        # Count braces and brackets
        open_braces = json_str.count('{')
        close_braces = json_str.count('}')
        open_brackets = json_str.count('[')
        close_brackets = json_str.count(']')
        
        # Remove trailing comma before closing
        json_str = re.sub(r',\s*$', '', json_str)
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        # Handle truncated strings - find unclosed quotes
        quote_count = json_str.count('"') - json_str.count('\\"')
        if quote_count % 2 != 0:
            # Find last unclosed quote and close it
            last_quote_idx = json_str.rfind('"')
            # Check if this quote is opening or closing
            before_quote = json_str[:last_quote_idx]
            if before_quote.count('"') % 2 != 0:
                # This is an opening quote without closing
                json_str = json_str + '"'
        
        # Balance braces and brackets
        missing_braces = open_braces - close_braces
        missing_brackets = open_brackets - close_brackets
        
        # Add missing closing brackets first (they're usually inside braces)
        if missing_brackets > 0:
            json_str = json_str.rstrip()
            if json_str.endswith(','):
                json_str = json_str[:-1]
            json_str += ']' * missing_brackets
        
        # Then add missing closing braces
        if missing_braces > 0:
            json_str = json_str.rstrip()
            if json_str.endswith(','):
                json_str = json_str[:-1]
            json_str += '}' * missing_braces
        
        return json_str
    
    def _extract_code_block(self, content: str) -> Dict[str, Any]:
        """Extract JSON from generic code block"""
        start = content.find("```") + 3
        # Skip language identifier if present
        if content[start:start+1].isalpha():
            start = content.find("\n", start) + 1
        end = content.find("```", start)
        
        if end == -1 or end <= start:
            json_str = content[start:].strip()
        else:
            json_str = content[start:end].strip()
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            repaired = self._repair_json(json_str)
            return json.loads(repaired)
    
    def _create_fallback_response(self, content: str) -> Dict[str, Any]:
        """Create fallback response when parsing fails, but try to extract metrics"""
        # Try to extract metrics from raw content even if full JSON parse fails
        metrics = self._extract_metrics_from_raw(content)
        
        # Try to extract findings
        findings = self._extract_findings_from_raw(content)
        
        return {
            "findings": findings if findings else [content[:500] if len(content) > 500 else content],
            "recommendations": ["Manual review required - JSON parsing failed"],
            "metrics": metrics,
            "rawResponse": content,
            "parseError": True
        }
    
    def _extract_metrics_from_raw(self, content: str) -> Dict[str, Any]:
        """Extract metrics dictionary from raw content using regex"""
        metrics = {}
        
        # Try to find the metrics block
        metrics_pattern = r'"metrics"\s*:\s*\{([^}]+)\}'
        match = re.search(metrics_pattern, content, re.DOTALL)
        
        if match:
            metrics_str = match.group(1)
            # Extract key-value pairs
            kv_pattern = r'"(\w+)"\s*:\s*([0-9.]+|"[^"]*")'
            for kv_match in re.finditer(kv_pattern, metrics_str):
                key = kv_match.group(1)
                value_str = kv_match.group(2)
                try:
                    if value_str.startswith('"'):
                        metrics[key] = value_str.strip('"')
                    elif '.' in value_str:
                        metrics[key] = float(value_str)
                    else:
                        metrics[key] = int(value_str)
                except ValueError:
                    metrics[key] = value_str
        
        return metrics
    
    def _extract_findings_from_raw(self, content: str) -> List[str]:
        """Extract findings array from raw content"""
        findings = []
        
        # Try to find findings array with string items
        findings_pattern = r'"findings"\s*:\s*\[(.*?)\]'
        match = re.search(findings_pattern, content, re.DOTALL)
        
        if match:
            findings_str = match.group(1)
            # Extract individual string items
            item_pattern = r'"([^"]+)"'
            for item_match in re.finditer(item_pattern, findings_str):
                finding = item_match.group(1)
                if len(finding) > 20:  # Filter out short matches that might be keys
                    findings.append(finding)
        
        return findings[:10]  # Limit to 10 findings
    
    # =========================
    # QUALITY VALIDATION (overridable)
    # =========================

    def _validate_output_quality(self, output: Dict[str, Any]):
        """
        Validate output quality. Subclasses can override this method to
        implement agent-specific quality checks instead of the generic one.
        Returns: (is_valid, issues, quality_score)
        """
        from .cot_prompting import validate_output_quality
        return validate_output_quality(output)

    # =========================
    # VALIDATION
    # =========================
    
    def validate_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure response matches expected schema
        
        Validation Steps:
        1. Ensure required fields exist with defaults
        2. Type coercion for list/dict fields
        3. Score clamping (0-100 range)
        4. Normalize metrics
        
        Args:
            result: Parsed response dictionary
            
        Returns:
            Validated and normalized dictionary
        """
        # Required fields with defaults
        validated = {
            "findings": result.get("findings", []),
            "recommendations": result.get("recommendations", []),
            "metrics": result.get("metrics", {}),
        }
        
        # Preserve all other fields from result
        for key, value in result.items():
            if key not in validated:
                validated[key] = value
        
        # Type coercion for findings
        if not isinstance(validated["findings"], list):
            validated["findings"] = [str(validated["findings"])]
        
        # Type coercion for recommendations
        if not isinstance(validated["recommendations"], list):
            validated["recommendations"] = [str(validated["recommendations"])]
        
        # Type coercion for metrics
        if not isinstance(validated["metrics"], dict):
            validated["metrics"] = {}
        
        # Metric validation - clamp scores to 0-100
        validated["metrics"] = self._validate_metrics(validated["metrics"])
        
        # AŞAMA 3: Output sanitization - prompt kalıntıları ve hataları temizle
        validated = self.sanitize_output(validated)
        
        return validated
    
    def _validate_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize metrics"""
        validated_metrics = {}
        
        for key, value in metrics.items():
            # Handle numeric values
            if isinstance(value, (int, float)):
                # Clamp scores to 0-100
                if "score" in key.lower() or key.lower().endswith("score"):
                    value = max(0, min(100, value))
                # Round floats
                if isinstance(value, float):
                    value = round(value, 2)
            
            validated_metrics[key] = value
        
        return validated_metrics
    
    def _ensure_overall_score(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        CRITICAL: Ensure every agent response has an overallScore in metrics
        
        This method guarantees that even if the LLM fails to produce an overallScore,
        we calculate one from available metrics or assign a default.
        
        Priority:
        1. Use existing overallScore if valid
        2. Extract scores from nested analysis objects
        3. Calculate from available score metrics (excluding zeros)
        4. Fall back to default (50.0)
        
        IMPORTANT: Zero scores are excluded from calculation to prevent
        agents with missing data from reporting artificially low scores.
        
        Args:
            result: The parsed and validated response
            
        Returns:
            Result with guaranteed overallScore in metrics
        """
        metrics = result.get("metrics", {})
        
        # Check if overallScore already exists and is valid
        existing_score = metrics.get("overallScore")
        if existing_score is not None and isinstance(existing_score, (int, float)) and existing_score > 0:
            # Ensure it's clamped
            metrics["overallScore"] = max(0, min(100, float(existing_score)))
            result["metrics"] = metrics
            return result
        
        # Try to extract scores from nested analysis objects in result
        nested_scores = self._extract_nested_scores(result)
        
        # Also extract from flat metrics
        flat_scores = []
        flat_keys = []
        zero_metrics = []  # Track metrics that are 0 for debugging
        
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                key_lower = key.lower()
                # Look for score-like keys
                if any(term in key_lower for term in ['score', 'rating', 'index', 'quality']):
                    if 0 <= value <= 100:
                        if value > 0:  # CRITICAL: Exclude zeros from calculation
                            flat_scores.append(float(value))
                            flat_keys.append(key)
                        else:
                            zero_metrics.append(key)
        
        # Filter out zeros from nested scores too
        nested_scores_filtered = [s for s in nested_scores if s > 0]
        
        # Combine all non-zero scores
        all_scores = nested_scores_filtered + flat_scores
        
        # Track zero metrics for transparency
        if zero_metrics:
            metrics["_zeroMetrics"] = zero_metrics
        
        if all_scores:
            # Calculate weighted average from non-zero scores only
            calculated_score = sum(all_scores) / len(all_scores)
            metrics["overallScore"] = round(max(0, min(100, calculated_score)), 2)
            logger.info(f"[{self.name}] Calculated overallScore={metrics['overallScore']:.2f} from {len(all_scores)} non-zero scores (nested: {len(nested_scores_filtered)}, flat: {len(flat_scores)}, zeros excluded: {len(zero_metrics)})")
        else:
            # No valid score metrics found, use default
            metrics["overallScore"] = 50.0
            logger.warning(f"[{self.name}] No non-zero score metrics found, using default overallScore=50.0")
        
        # Enrich metrics with extracted nested scores
        result = self._enrich_metrics_from_nested(result)
        result["metrics"] = metrics
        return result
    
    def _extract_nested_scores(self, result: Dict[str, Any]) -> List[float]:
        """
        Extract scores from nested analysis objects like grid_analysis, color_analysis, etc.
        
        This handles structures like:
        - grid_analysis.visual_flow.score
        - color_analysis.color_consistency.score
        - consistency_analysis.visual_consistency_score
        """
        scores = []
        
        # Keys that might contain nested scores
        nested_keys = [
            'grid_analysis', 'color_analysis', 'typography_analysis', 
            'consistency_analysis', 'format_analysis', 'quality_analysis',
            'thumbnailAnalysis', 'gridProfessionalism', 'colorConsistencyAnalysis',
            'visualArchetypeAnalysis', 'brand_overview'
        ]
        
        for key in nested_keys:
            if key in result and isinstance(result[key], dict):
                scores.extend(self._extract_scores_recursive(result[key]))
        
        return scores
    
    def _extract_scores_recursive(self, obj: Any, depth: int = 0) -> List[float]:
        """Recursively extract numeric scores from nested objects (max depth 3)"""
        if depth > 3:
            return []
        
        scores = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                key_lower = key.lower()
                # Direct score values
                if isinstance(value, (int, float)):
                    if 'score' in key_lower or key_lower == 'score':
                        if 0 <= value <= 100:
                            scores.append(float(value))
                # Nested objects
                elif isinstance(value, dict):
                    scores.extend(self._extract_scores_recursive(value, depth + 1))
        
        return scores
    
    def _enrich_metrics_from_nested(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich the metrics object with key scores extracted from nested analysis objects.
        
        This ensures frontend can display important metrics even if they're deeply nested.
        """
        metrics = result.get("metrics", {})
        
        # Visual Brand specific enrichment
        if "grid_analysis" in result:
            grid = result["grid_analysis"]
            if isinstance(grid, dict):
                # Extract component scores
                if "visual_flow" in grid and isinstance(grid["visual_flow"], dict):
                    metrics["gridVisualFlow"] = grid["visual_flow"].get("score", 0)
                if "color_distribution" in grid and isinstance(grid["color_distribution"], dict):
                    metrics["gridColorHarmony"] = grid["color_distribution"].get("score", 0)
                if "content_variety" in grid and isinstance(grid["content_variety"], dict):
                    metrics["gridContentBalance"] = grid["content_variety"].get("score", 0)
                if "first_impression" in grid and isinstance(grid["first_impression"], dict):
                    metrics["gridFirstImpression"] = grid["first_impression"].get("score", 0)
                
                # Calculate gridAesthetics if not present
                if "gridAesthetics" not in metrics or metrics["gridAesthetics"] == 0:
                    grid_scores = [
                        metrics.get("gridVisualFlow", 0),
                        metrics.get("gridColorHarmony", 0),
                        metrics.get("gridContentBalance", 0),
                        metrics.get("gridFirstImpression", 0)
                    ]
                    valid_scores = [s for s in grid_scores if s > 0]
                    if valid_scores:
                        metrics["gridAesthetics"] = round(sum(valid_scores) / len(valid_scores), 1)
        
        # Color analysis enrichment
        if "color_analysis" in result:
            color = result["color_analysis"]
            if isinstance(color, dict):
                if "color_consistency" in color and isinstance(color["color_consistency"], dict):
                    metrics["colorConsistencyScore"] = color["color_consistency"].get("score", 0)
                if "palette_harmony" in color and isinstance(color["palette_harmony"], dict):
                    metrics["paletteHarmonyScore"] = color["palette_harmony"].get("score", 0)
                if "niche_color_fit" in color and isinstance(color["niche_color_fit"], dict):
                    metrics["nicheColorFitScore"] = color["niche_color_fit"].get("score", 0)
        
        # Consistency analysis enrichment
        if "consistency_analysis" in result:
            consistency = result["consistency_analysis"]
            if isinstance(consistency, dict):
                if "visual_consistency_score" in consistency:
                    metrics["visualConsistency"] = consistency["visual_consistency_score"]
                if "brand_recognition_score" in consistency:
                    metrics["brandRecognition"] = consistency["brand_recognition_score"]
        
        # Format analysis enrichment
        if "format_analysis" in result:
            fmt = result["format_analysis"]
            if isinstance(fmt, dict):
                if "deviation_score" in fmt:
                    metrics["formatOptimization"] = 100 - fmt["deviation_score"]  # Invert deviation
        
        # Quality analysis enrichment
        if "quality_analysis" in result:
            quality = result["quality_analysis"]
            if isinstance(quality, dict):
                if "image_quality" in quality and isinstance(quality["image_quality"], dict):
                    metrics["imageQualityScore"] = quality["image_quality"].get("score", 0)
                if "video_quality" in quality and isinstance(quality["video_quality"], dict):
                    metrics["videoQualityScore"] = quality["video_quality"].get("score", 0)
        
        # Calculate overallVisualScore if we have enriched metrics
        visual_metrics = [
            metrics.get("gridAesthetics", 0),
            metrics.get("colorConsistencyScore", 0),
            metrics.get("visualConsistency", 0),
            metrics.get("brandRecognition", 0),
            metrics.get("formatOptimization", 0),
        ]
        valid_visual = [m for m in visual_metrics if m > 0]
        if valid_visual and ("overallVisualScore" not in metrics or metrics["overallVisualScore"] == 0):
            metrics["overallVisualScore"] = round(sum(valid_visual) / len(valid_visual), 1)
        
        # Set gridProfessionalismScore
        if "gridProfessionalismScore" not in metrics or metrics["gridProfessionalismScore"] == 0:
            metrics["gridProfessionalismScore"] = metrics.get("gridAesthetics", 0)
        
        # Calculate contentQuality from quality analysis
        quality_metrics = [
            metrics.get("imageQualityScore", 0),
            metrics.get("videoQualityScore", 0),
        ]
        valid_quality = [m for m in quality_metrics if m > 0]
        if valid_quality and ("contentQuality" not in metrics or metrics["contentQuality"] == 0):
            metrics["contentQuality"] = round(sum(valid_quality) / len(valid_quality), 1)
        
        # ========================================
        # GROWTH VIRALITY ENRICHMENT
        # ========================================
        if "growth_metrics" in result:
            gm = result["growth_metrics"]
            if isinstance(gm, dict):
                metrics["netGrowthRate"] = gm.get("net_growth_rate", 0)
                metrics["grossGrowthRate"] = gm.get("gross_growth_rate", 0)
                metrics["churnRate"] = gm.get("churn_rate", 0)
                metrics["growthVelocity"] = gm.get("growth_velocity", 0)
                metrics["cmgr"] = gm.get("cmgr", 0)
        
        if "growth_analysis" in result:
            ga = result["growth_analysis"]
            if isinstance(ga, dict) and "growth_sources" in ga:
                sources = ga["growth_sources"]
                if isinstance(sources, dict):
                    metrics["explorePagePotential"] = sources.get("explore_page", 0)
                    metrics["reelsViralPotential"] = sources.get("reels", 0)
                if "pattern_analysis" in ga and isinstance(ga["pattern_analysis"], dict):
                    sustainability = ga["pattern_analysis"].get("sustainability", "low")
                    metrics["sustainabilityScore"] = {"high": 90, "medium": 60, "low": 30}.get(sustainability, 50)
        
        # ========================================
        # ATTENTION ARCHITECT ENRICHMENT
        # ========================================
        if "retentionPrediction" in result:
            rp = result["retentionPrediction"]
            if isinstance(rp, dict):
                if "first3Seconds" in rp and isinstance(rp["first3Seconds"], dict):
                    metrics["first3SecondsRetention"] = rp["first3Seconds"].get("retentionRate", 0)
                    metrics["scrollStopProbability"] = rp["first3Seconds"].get("scrollStopProbability", 0)
                if "scrollStopProbability" in rp:
                    metrics["scrollStopProbability"] = rp["scrollStopProbability"]
                metrics["patternInterruptScore"] = 80 if rp.get("patternInterruptDetected") else 30
                metrics["curiosityGapScore"] = 80 if rp.get("curiosityGapPresent") else 30
                if "watchTimeEstimate" in rp and isinstance(rp["watchTimeEstimate"], dict):
                    metrics["expectedCompletionRate"] = rp["watchTimeEstimate"].get("expectedCompletionRate", 0)
                    metrics["replayProbability"] = rp["watchTimeEstimate"].get("replayProbability", 0)
        
        if "emotionalTriggers" in result and isinstance(result["emotionalTriggers"], list):
            strong_triggers = sum(1 for t in result["emotionalTriggers"] if t.get("strength") == "strong")
            total_triggers = len(result["emotionalTriggers"])
            if total_triggers > 0:
                metrics["emotionalTriggerStrength"] = round((strong_triggers / total_triggers) * 100)
        
        # ========================================
        # COMMUNITY LOYALTY ENRICHMENT
        # ========================================
        if "communityInsights" in result:
            ci = result["communityInsights"]
            if isinstance(ci, dict):
                total_followers = (ci.get("estimatedSuperfans", 0) + ci.get("activeEngagers", 0) + 
                                   ci.get("passiveFollowers", 0) + ci.get("ghostFollowers", 0))
                if total_followers > 0:
                    metrics["activeEngagersRatio"] = round((ci.get("activeEngagers", 0) / total_followers) * 100)
                    metrics["passiveFollowersRatio"] = round((ci.get("passiveFollowers", 0) / total_followers) * 100)
                    metrics["ghostFollowersRatio"] = round((ci.get("ghostFollowers", 0) / total_followers) * 100)
        
        # ========================================
        # SALES CONVERSION ENRICHMENT
        # ========================================
        if "monthlyRevenuePotential" in result:
            mrp = result["monthlyRevenuePotential"]
            if isinstance(mrp, dict):
                metrics["monthlyRevenuePotentialConservative"] = mrp.get("conservative", 0)
                metrics["monthlyRevenuePotentialModerate"] = mrp.get("moderate", 0)
                metrics["monthlyRevenuePotentialAggressive"] = mrp.get("aggressive", 0)
        
        if "revenueStreams" in result and isinstance(result["revenueStreams"], list):
            high_potential_count = sum(1 for s in result["revenueStreams"] if s.get("potential") == "high")
            metrics["revenueStreamDiversity"] = len(result["revenueStreams"])
            if len(result["revenueStreams"]) > 0:
                metrics["highPotentialStreamRatio"] = round((high_potential_count / len(result["revenueStreams"])) * 100)
        
        # ========================================
        # DOMAIN MASTER ENRICHMENT
        # ========================================
        if "niche_analysis" in result:
            na = result["niche_analysis"]
            if isinstance(na, dict):
                metrics["marketSaturationScore"] = na.get("saturation", 0)
                competition_map = {"very_high": 90, "high": 70, "medium": 50, "low": 30}
                metrics["competitionScore"] = competition_map.get(na.get("competition_level"), 50)
                growth_map = {"high": 90, "medium-high": 75, "medium": 60, "low": 40}
                metrics["growthPotentialScore"] = growth_map.get(na.get("growth_potential"), 50)
        
        if "benchmark_comparison" in result:
            bc = result["benchmark_comparison"]
            if isinstance(bc, dict):
                if "engagement_rate" in bc and isinstance(bc["engagement_rate"], dict):
                    metrics["engagementPercentile"] = bc["engagement_rate"].get("percentile", 0)
                if "growth_rate" in bc and isinstance(bc["growth_rate"], dict):
                    metrics["growthPercentile"] = bc["growth_rate"].get("percentile", 0)
        
        # ========================================
        # CONTENT STRATEGIST ENRICHMENT
        # ========================================
        if "detailed_scores" in result:
            ds = result["detailed_scores"]
            if isinstance(ds, dict):
                if "content_effectiveness" in ds and isinstance(ds["content_effectiveness"], dict):
                    metrics["contentEffectivenessScore"] = ds["content_effectiveness"].get("score", 0)
                if "hashtag_effectiveness" in ds and isinstance(ds["hashtag_effectiveness"], dict):
                    metrics["hashtagEffectiveness"] = ds["hashtag_effectiveness"].get("score", 0)
                if "format_diversity" in ds and isinstance(ds["format_diversity"], dict):
                    metrics["formatDiversityScore"] = ds["format_diversity"].get("score", 0)
                if "engagement_quality" in ds and isinstance(ds["engagement_quality"], dict):
                    metrics["engagementQualityScore"] = ds["engagement_quality"].get("score", 0)
        
        if "posting_analysis" in result:
            pa = result["posting_analysis"]
            if isinstance(pa, dict):
                metrics["postsPerWeek"] = pa.get("posts_per_week", 0)
                consistency_map = {"high": 90, "medium": 60, "low": 30}
                metrics["postingConsistencyScore"] = consistency_map.get(pa.get("consistency"), 50)
        
        if "format_breakdown" in result:
            fb = result["format_breakdown"]
            if isinstance(fb, dict):
                total_posts = sum(fb.values()) if fb else 1
                if total_posts > 0:
                    metrics["reelsRatio"] = round((fb.get("reels", 0) / total_posts) * 100)
                    metrics["carouselRatio"] = round((fb.get("carousel", 0) / total_posts) * 100)
                    metrics["singlePostRatio"] = round((fb.get("single", 0) / total_posts) * 100)
        
        # ========================================
        # AUDIENCE DYNAMICS ENRICHMENT
        # ========================================
        if "audience_segments" in result and isinstance(result["audience_segments"], list):
            total_pct = sum(s.get("percentage", 0) for s in result["audience_segments"])
            high_quality_pct = sum(s.get("percentage", 0) for s in result["audience_segments"] 
                                   if s.get("quality") in ["premium", "high"])
            if total_pct > 0:
                metrics["audienceQuality"] = round((high_quality_pct / total_pct) * 100)
        
        if "engagement_patterns" in result:
            ep = result["engagement_patterns"]
            if isinstance(ep, dict):
                metrics["engagementRate"] = ep.get("average_engagement_rate", 0)
        
        # ========================================
        # GENERIC overallScore CALCULATION
        # ========================================
        # If no overallScore exists, try to calculate from available metrics
        if "overallScore" not in metrics or metrics.get("overallScore", 0) == 0:
            all_scores = [v for k, v in metrics.items() 
                         if isinstance(v, (int, float)) and k.endswith("Score") and v > 0]
            if all_scores:
                metrics["overallScore"] = round(sum(all_scores) / len(all_scores), 1)
        
        result["metrics"] = metrics
        return result
    
    # =========================
    # OUTPUT SANITIZATION (AŞAMA 3)
    # =========================
    
    # Temizlenecek kalıplar - prompt sızıntıları ve hata kodları
    SANITIZATION_PATTERNS = [
        (r'^TÜRKÇE\s*[-:]\s*', ''),  # "TÜRKÇE - " öneki
        (r'^Bulgu\s*\d+\s*[-:]\s*', ''),  # "Bulgu 1: " öneki
        (r'^Finding\s*\d+\s*[-:]\s*', ''),  # "Finding 1: " öneki
        (r'^Öneri\s*\d+\s*[-:]\s*', ''),  # "Öneri 1: " öneki
        (r'^Recommendation\s*\d+\s*[-:]\s*', ''),  # "Recommendation 1: " öneki
        (r'^\d+\.\s*', ''),  # "1. " sayı öneki
        (r'\s*\[Error:.*?\]', ''),  # [Error: ...] kalıntıları
        (r'\s*\{Error:.*?\}', ''),  # {Error: ...} kalıntıları
        (r'Error\s*\d{3}', ''),  # Error 429, Error 503 vb.
        (r'Resource\s+Exhausted', ''),  # Resource Exhausted
        (r'Rate\s+Limit', ''),  # Rate Limit
        (r'API\s+Error', ''),  # API Error
        (r'Exception:', ''),  # Exception:
        (r'^\s*[-•]\s*', ''),  # Madde işaretleri
    ]
    
    # Hata göstergeleri - bu stringler varsa "analiz edilemedi" olarak işaretle
    ERROR_INDICATORS = [
        "error", "exception", "429", "503", "resource exhausted", 
        "rate limit", "timeout", "unavailable", "failed to", "could not"
    ]
    
    def sanitize_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Çıktı temizliği - prompt kalıntıları ve hataları temizle
        
        AŞAMA 3: ÇIKTI TEMİZLİĞİ (SANITIZATION)
        - Regex ile TÜRKÇE-, Bulgu 1: gibi önekleri sil
        - API hata kodlarını tespit et ve standart mesajla değiştir
        - 0.0 ve null değerleri kontrol et
        """
        # Findings temizle
        if "findings" in result:
            result["findings"] = self._sanitize_list(result["findings"])
        
        # Recommendations temizle
        if "recommendations" in result:
            result["recommendations"] = self._sanitize_list(result["recommendations"])
        
        # Insights temizle (varsa)
        if "insights" in result:
            result["insights"] = self._sanitize_list(result["insights"])
        
        # Hata kontrolü
        result = self._check_for_errors(result)
        
        # Metriklerdeki 0.0 değerleri kontrol et
        if "metrics" in result:
            result["metrics"] = self._sanitize_metrics(result["metrics"])
        
        return result
    
    def _sanitize_string(self, text: str) -> str:
        """Tek bir string'i temizle"""
        if not isinstance(text, str):
            return str(text) if text else ""
        
        cleaned = text.strip()
        
        # Tüm pattern'leri uygula
        for pattern, replacement in self.SANITIZATION_PATTERNS:
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()
    
    def _sanitize_list(self, items: list) -> list:
        """Liste içindeki tüm string'leri temizle"""
        if not isinstance(items, list):
            return [self._sanitize_string(str(items))] if items else []
        
        sanitized = []
        for item in items:
            if isinstance(item, str):
                cleaned = self._sanitize_string(item)
                if cleaned:  # Boş string'leri atla
                    sanitized.append(cleaned)
            elif isinstance(item, dict):
                # Dict içindeki string alanları temizle
                sanitized_dict = {}
                for key, value in item.items():
                    if isinstance(value, str):
                        sanitized_dict[key] = self._sanitize_string(value)
                    else:
                        sanitized_dict[key] = value
                sanitized.append(sanitized_dict)
            else:
                sanitized.append(item)
        
        return sanitized
    
    def _check_for_errors(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hata göstergelerini kontrol et ve standart mesajla değiştir
        """
        error_found = False
        error_locations = []
        
        # Findings'de hata ara
        findings = result.get("findings", [])
        for i, finding in enumerate(findings):
            finding_str = str(finding).lower() if finding else ""
            if any(indicator in finding_str for indicator in self.ERROR_INDICATORS):
                error_found = True
                error_locations.append(f"finding_{i}")
        
        # Recommendations'da hata ara
        recommendations = result.get("recommendations", [])
        for i, rec in enumerate(recommendations):
            rec_str = str(rec).lower() if rec else ""
            if any(indicator in rec_str for indicator in self.ERROR_INDICATORS):
                error_found = True
                error_locations.append(f"recommendation_{i}")
        
        # Hata bulunduysa standart mesajla değiştir
        if error_found:
            result["hadApiError"] = True
            result["errorLocations"] = error_locations
            
            # Hatalı içerikleri filtrele
            result["findings"] = [f for f in findings if not any(
                indicator in str(f).lower() for indicator in self.ERROR_INDICATORS
            )]
            result["recommendations"] = [r for r in recommendations if not any(
                indicator in str(r).lower() for indicator in self.ERROR_INDICATORS
            )]
            
            # Boşsa varsayılan mesaj ekle
            if not result["findings"]:
                result["findings"] = [{
                    "type": "warning",
                    "category": "system",
                    "finding": "⚠️ Bu modül şu an yoğunluk nedeniyle veriye erişemedi. Lütfen daha sonra tekrar deneyin.",
                    "impact_score": 50
                }]
        
        return result
    
    def _sanitize_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Metriklerdeki 0.0 ve null değerleri kontrol et
        AŞAMA 4: 0.0 Toleransı - 0 değerleri N/A olarak işaretle
        """
        sanitized = {}
        zero_metrics = []
        
        for key, value in metrics.items():
            # Null kontrolü
            if value is None:
                sanitized[key] = None
                sanitized[f"{key}_display"] = "N/A"
                zero_metrics.append(key)
                continue
            
            # 0.0 kontrolü (score metrikleri için)
            if isinstance(value, (int, float)) and value == 0:
                if "score" in key.lower() or "rate" in key.lower():
                    sanitized[key] = 0
                    sanitized[f"{key}_display"] = "N/A"
                    sanitized[f"{key}_note"] = "Veri mevcut değil"
                    zero_metrics.append(key)
                    continue
            
            sanitized[key] = value
        
        # Sıfır metrikleri işaretle
        if zero_metrics:
            sanitized["_zeroMetrics"] = zero_metrics
        
        return sanitized
    
    # =========================
    # DATA NORMALIZATION
    # =========================
    
    def normalize_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardize metric formats across agents
        
        Operations:
        - Convert string numbers to floats
        - Normalize key names to camelCase
        - Round float values
        
        Args:
            metrics: Raw metrics dictionary
            
        Returns:
            Normalized metrics dictionary
        """
        normalized = {}
        
        for key, value in metrics.items():
            # Convert string numbers
            if isinstance(value, str):
                try:
                    value = float(value.replace('%', '').replace(',', ''))
                except ValueError:
                    pass
            
            # Standardize key names
            normalized_key = self._normalize_key(key)
            
            # Round floats
            if isinstance(value, float):
                value = round(value, 2)
            
            normalized[normalized_key] = value
        
        return normalized
    
    def _normalize_key(self, key: str) -> str:
        """Convert various key formats to camelCase"""
        # Handle snake_case
        if '_' in key:
            components = key.split('_')
            return components[0].lower() + ''.join(x.title() for x in components[1:])
        return key
    
    # =========================
    # ERROR HANDLING
    # =========================
    
    def _get_error_response(self, error: Exception) -> Dict[str, Any]:
        """
        Generate standardized error response
        
        CRITICAL: Even on error, we must provide an overallScore
        This ensures the final score calculation never fails.
        
        Args:
            error: The exception that occurred
            
        Returns:
            Structured error response dictionary with default score
        """
        return {
            "agentName": self.name,
            "agentRole": self.role,
            "error": True,
            "errorType": type(error).__name__,
            "errorMessage": str(error),
            "findings": [f"Analysis could not be completed due to {type(error).__name__}"],
            "recommendations": ["Retry analysis", "Check input data validity", "Verify API connectivity"],
            "metrics": {
                "overallScore": 50.0,  # Default score for error cases
                "errorOccurred": True
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # =========================
    # NUMBER FORMATTING
    # =========================
    
    def format_number(self, num: float) -> str:
        """
        Format large numbers for display
        
        Examples:
            1500000 → "1.5M"
            25000 → "25.0K"
            999 → "999"
        
        Args:
            num: Number to format
            
        Returns:
            Formatted string
        """
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        return str(int(num))
    
    def format_percentage(self, value: float, decimals: int = 2) -> str:
        """
        Format percentage values
        
        Args:
            value: Percentage value
            decimals: Number of decimal places
            
        Returns:
            Formatted percentage string
        """
        return f"{value:.{decimals}f}%"
    
    def format_currency(self, value: float, currency: str = "TRY") -> str:
        """
        Format currency values
        
        Args:
            value: Currency amount
            currency: Currency code (TRY, USD, EUR)
            
        Returns:
            Formatted currency string
        """
        symbols = {"TRY": "₺", "USD": "$", "EUR": "€", "GBP": "£"}
        symbol = symbols.get(currency, currency)
        return f"{symbol}{value:,.2f}"
    
    # =========================
    # DATA TRANSFORMATION
    # =========================
    
    def calculate_engagement_rate(self, likes: int, comments: int, 
                                  followers: int) -> float:
        """
        Calculate standard engagement rate
        
        Formula: ((likes + comments) / followers) × 100
        Clamped to [0, 100] range to prevent impossible values.
        
        Args:
            likes: Total likes
            comments: Total comments
            followers: Follower count
            
        Returns:
            Engagement rate percentage (0-100)
        """
        if followers == 0:
            return 0.0
        # Clamp to valid range - engagement rate cannot be negative or exceed 100%
        rate = ((likes + comments) / followers) * 100
        return round(max(0.0, min(100.0, rate)), 2)
    
    def calculate_growth_rate(self, current: int, previous: int) -> float:
        """
        Calculate percentage growth
        
        Formula: ((current - previous) / previous) × 100
        
        Args:
            current: Current value
            previous: Previous value
            
        Returns:
            Growth rate percentage
        """
        if previous == 0:
            return 0.0 if current == 0 else 100.0
        return round(((current - previous) / previous) * 100, 2)
    
    def get_percentile(self, value: float, benchmarks: List[float]) -> int:
        """
        Calculate percentile rank
        
        Args:
            value: Value to rank
            benchmarks: List of comparison values
            
        Returns:
            Percentile (0-100)
        """
        if not benchmarks:
            return 50
        sorted_benchmarks = sorted(benchmarks)
        count_below = sum(1 for b in sorted_benchmarks if b < value)
        return int((count_below / len(sorted_benchmarks)) * 100)
    
    def categorize_score(self, score: float) -> str:
        """
        Convert numeric score to category
        
        Categories:
        - 90+: exceptional
        - 75-89: excellent
        - 60-74: good
        - 45-59: average
        - 30-44: below_average
        - <30: poor
        
        Args:
            score: Numeric score (0-100)
            
        Returns:
            Category string
        """
        if score >= 90:
            return "exceptional"
        elif score >= 75:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 45:
            return "average"
        elif score >= 30:
            return "below_average"
        return "poor"
    
    def get_grade(self, score: float) -> str:
        """
        Convert numeric score to letter grade
        
        Grades:
        - 90+: A+
        - 80-89: A
        - 70-79: B
        - 60-69: C
        - 50-59: D
        - <50: F
        
        Args:
            score: Numeric score (0-100)
            
        Returns:
            Letter grade string
        """
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        return "F"
    
    # =========================
    # CONTENT DATA FORMATTING
    # =========================
    
    def _format_content_data(self, account_data: Dict[str, Any]) -> str:
        """
        Format content data for prompt injection
        
        Args:
            account_data: Account data dictionary
            
        Returns:
            Formatted content string
        """
        posts = account_data.get('recentPosts', [])
        
        if not posts:
            return "No recent posts available for analysis."
        
        lines = [f"Recent {len(posts)} posts analyzed:"]
        
        for i, post in enumerate(posts[:5], 1):  # Show top 5
            likes = post.get('likes', 0)
            comments = post.get('comments', 0)
            post_type = post.get('type', 'unknown')
            lines.append(f"  {i}. {post_type.upper()}: {self.format_number(likes)} likes, {self.format_number(comments)} comments")
        
        if len(posts) > 5:
            lines.append(f"  ... and {len(posts) - 5} more posts")
        
        return "\n".join(lines)
    
    def _format_metrics_summary(self, account_data: Dict[str, Any]) -> str:
        """
        Format key metrics for prompt injection
        
        Args:
            account_data: Account data dictionary
            
        Returns:
            Formatted metrics string
        """
        metrics = []
        
        if 'followers' in account_data:
            metrics.append(f"Followers: {self.format_number(account_data['followers'])}")
        if 'following' in account_data:
            metrics.append(f"Following: {self.format_number(account_data['following'])}")
        if 'posts' in account_data:
            metrics.append(f"Total Posts: {self.format_number(account_data['posts'])}")
        if 'engagementRate' in account_data:
            metrics.append(f"Engagement Rate: {self.format_percentage(account_data['engagementRate'])}")
        if 'avgLikes' in account_data:
            metrics.append(f"Avg Likes: {self.format_number(account_data['avgLikes'])}")
        if 'avgComments' in account_data:
            metrics.append(f"Avg Comments: {self.format_number(account_data['avgComments'])}")
        
        return " | ".join(metrics)
    
    # =========================
    # LOGGING
    # =========================
    
    def _log_analysis_start(self, account_data: Dict[str, Any]):
        """Log analysis start"""
        username = account_data.get('username', 'unknown')
        logger.info(f"[{self.name}] Starting analysis for @{username}")
    
    def _log_analysis_complete(self, duration: float, result: Dict[str, Any]):
        """Log analysis completion"""
        logger.info(f"[{self.name}] Analysis complete in {duration:.2f}s")
        
        # Log key metrics if available
        if 'metrics' in result:
            metrics_count = len(result['metrics'])
            logger.debug(f"[{self.name}] Generated {metrics_count} metrics")
        
        findings_count = len(result.get('findings', []))
        recs_count = len(result.get('recommendations', []))
        logger.debug(f"[{self.name}] Findings: {findings_count}, Recommendations: {recs_count}")
    
    def _log_error(self, error: Exception, context: str = ""):
        """Log error with context"""
        logger.error(f"[{self.name}] Error in {context}: {type(error).__name__}: {error}")
    
    # =========================
    # PERFORMANCE METRICS
    # =========================
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get agent performance metrics
        
        Returns:
            Dictionary with performance statistics
        """
        return {
            "agent": self.name,
            "role": self.role,
            "metrics": self.metrics.to_dict()
        }
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.metrics = AnalysisMetrics()


# =========================
# AGENT EXTENSION TEMPLATE
# =========================

"""
NEW AGENT TEMPLATE (for google.genai SDK):

from typing import Dict, Any
from .base_agent import BaseAgent


class NewSpecificAgent(BaseAgent):
    '''
    [Agent Name] Agent
    Role: [Brief role description]
    '''
    
    def __init__(self, gemini_client, generation_config=None, model_name: str = "gemini-2.5-flash"):
        super().__init__(gemini_client, generation_config, model_name)
        self.name = "[Agent Name]"
        self.role = "[Role Title]"
        self.specialty = "[Specialty areas]"
        
        # Initialize agent-specific knowledge bases
        self._init_knowledge_base()
    
    def _init_knowledge_base(self):
        '''Initialize agent-specific data'''
        pass
    
    def get_system_prompt(self) -> str:
        return '''You are the [Agent Name], a [role] expert specializing in:
- [Specialty 1]
- [Specialty 2]
- [Specialty 3]

# KNOWLEDGE BASE
[Domain-specific knowledge]

# ANALYSIS METHODOLOGY
[Step-by-step methodology]

# CRITICAL RULES
1. [Rule 1]
2. [Rule 2]

# OUTPUT FORMAT
Respond ONLY with valid JSON:
{
    "findings": ["finding1", "finding2"],
    "recommendations": ["rec1", "rec2"],
    "metrics": {
        "specificScore1": 0,
        "specificScore2": 0,
        "overallScore": 0
    }
}'''
    
    def get_analysis_prompt(self, account_data: Dict[str, Any]) -> str:
        return f'''Analyze [specific aspect] for this Instagram account:

ACCOUNT DATA:
- Username: @{account_data.get('username', 'unknown')}
- Followers: {account_data.get('followers', 0):,}
- Engagement Rate: {account_data.get('engagementRate', 0):.2f}%

ANALYSIS TASKS:
1. [Task 1]
2. [Task 2]

Respond with the JSON structure specified in system prompt.'''
    
    # Optional: Override parse_response for custom handling
    def parse_response(self, content: str) -> Dict[str, Any]:
        result = super().parse_response(content)
        # Add agent-specific processing
        return result
"""
