# =============================================================================
# Multi-LLM Manager - Load Balancing & Hybrid Model Support
# Version 2.0 - Instagram AI Agent System
# =============================================================================
"""
Bu modül çoklu LLM desteği sağlar:
1. Gemini Flash (hızlı, basit analizler için)
2. Gemini Pro (kompleks analizler için)
3. DeepSeek (fallback)
4. Async queue ile rate limiting
5. Load balancing

Kullanım:
    from agents.llm_manager import LLMManager, ModelType

    manager = LLMManager()
    result = await manager.generate(
        prompt="...",
        model_type=ModelType.FAST  # veya COMPLEX, BALANCED
    )
"""

import asyncio
import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS & TYPES
# =============================================================================

class ModelType(str, Enum):
    """Model seçim türleri"""
    FAST = "fast"           # Hızlı yanıt, basit analiz (Flash)
    COMPLEX = "complex"     # Derin analiz (Pro)
    BALANCED = "balanced"   # Dengeli (Flash with fallback to Pro)
    FALLBACK = "fallback"   # Yedek (DeepSeek)


class ModelProvider(str, Enum):
    """Model sağlayıcıları"""
    GEMINI_FLASH = "gemini-2.0-flash"
    GEMINI_PRO = "gemini-1.5-pro"
    DEEPSEEK = "deepseek-chat"


@dataclass
class ModelConfig:
    """Model konfigürasyonu"""
    provider: ModelProvider
    max_tokens: int = 8192
    temperature: float = 0.7
    top_p: float = 0.9
    rpm_limit: int = 15  # Requests per minute
    daily_limit: Optional[int] = None
    priority: int = 1  # Düşük = yüksek öncelik
    
    # Cost tracking
    cost_per_1k_tokens: float = 0.0


@dataclass
class RequestMetrics:
    """API istek metrikleri"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency: float = 0.0
    total_tokens: int = 0
    rate_limit_hits: int = 0
    last_request_time: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def avg_latency(self) -> float:
        if self.successful_requests == 0:
            return 0.0
        return self.total_latency / self.successful_requests


# =============================================================================
# RATE LIMITER
# =============================================================================

class AsyncRateLimiter:
    """
    Token bucket rate limiter - async uyumlu
    """
    
    def __init__(self, rpm: int = 15, burst: int = 3):
        self.rpm = rpm
        self.burst = burst
        self.tokens = float(burst)
        self.last_update = time.time()
        self.lock = asyncio.Lock()
        self.min_interval = 60.0 / rpm
        self.last_request = 0
    
    async def acquire(self) -> float:
        """
        Token al, gerekirse bekle
        
        Returns:
            Beklenen süre (saniye)
        """
        async with self.lock:
            now = time.time()
            
            # Token'ları yenile
            elapsed = now - self.last_update
            self.tokens = min(self.burst, self.tokens + elapsed * (self.rpm / 60))
            self.last_update = now
            
            # Minimum interval kontrolü
            time_since_last = now - self.last_request
            if time_since_last < self.min_interval:
                wait_time = self.min_interval - time_since_last
                await asyncio.sleep(wait_time)
            
            # Token bekle
            wait_total = 0.0
            while self.tokens < 1:
                wait_time = 0.5
                await asyncio.sleep(wait_time)
                wait_total += wait_time
                
                # Yenile
                now = time.time()
                elapsed = now - self.last_update
                self.tokens = min(self.burst, self.tokens + elapsed * (self.rpm / 60))
                self.last_update = now
            
            self.tokens -= 1
            self.last_request = time.time()
            
            return wait_total
    
    def reset(self):
        """Rate limiter'ı sıfırla"""
        self.tokens = float(self.burst)
        self.last_update = time.time()
        self.last_request = 0


# =============================================================================
# REQUEST QUEUE
# =============================================================================

@dataclass
class QueuedRequest:
    """Sıraya alınmış istek"""
    id: str
    prompt: str
    model_type: ModelType
    priority: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    callback: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class RequestQueue:
    """
    Priority-based async request queue
    """
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=max_size)
        self.processing = False
        self._counter = 0
    
    async def enqueue(self, request: QueuedRequest) -> bool:
        """
        İstek sıraya ekle
        
        Returns:
            True if enqueued, False if queue is full
        """
        if self.queue.full():
            logger.warning("Request queue is full")
            return False
        
        # Priority tuple: (priority, counter, request)
        # Counter ensures FIFO for same priority
        self._counter += 1
        await self.queue.put((request.priority, self._counter, request))
        return True
    
    async def dequeue(self) -> Optional[QueuedRequest]:
        """Sonraki isteği al"""
        try:
            _, _, request = await asyncio.wait_for(self.queue.get(), timeout=1.0)
            return request
        except asyncio.TimeoutError:
            return None
    
    @property
    def size(self) -> int:
        return self.queue.qsize()
    
    @property
    def is_empty(self) -> bool:
        return self.queue.empty()


# =============================================================================
# LLM MANAGER
# =============================================================================

class LLMManager:
    """
    Multi-LLM Manager with Load Balancing
    
    Features:
    - Multiple model support (Gemini Flash, Pro, DeepSeek)
    - Automatic model selection based on task complexity
    - Rate limiting per model
    - Fallback chain
    - Metrics tracking
    """
    
    def __init__(self, gemini_client=None):
        self.gemini_client = gemini_client
        
        # Model configurations
        self.models: Dict[ModelProvider, ModelConfig] = {
            ModelProvider.GEMINI_FLASH: ModelConfig(
                provider=ModelProvider.GEMINI_FLASH,
                max_tokens=16384,
                temperature=0.7,
                rpm_limit=15,
                priority=1,
                cost_per_1k_tokens=0.0001
            ),
            ModelProvider.GEMINI_PRO: ModelConfig(
                provider=ModelProvider.GEMINI_PRO,
                max_tokens=32768,
                temperature=0.7,
                rpm_limit=10,
                priority=2,
                cost_per_1k_tokens=0.001
            ),
            ModelProvider.DEEPSEEK: ModelConfig(
                provider=ModelProvider.DEEPSEEK,
                max_tokens=16384,
                temperature=0.7,
                rpm_limit=30,
                priority=3,
                cost_per_1k_tokens=0.0002
            ),
        }
        
        # Rate limiters per model
        self.rate_limiters: Dict[ModelProvider, AsyncRateLimiter] = {
            provider: AsyncRateLimiter(config.rpm_limit)
            for provider, config in self.models.items()
        }
        
        # Metrics per model
        self.metrics: Dict[ModelProvider, RequestMetrics] = {
            provider: RequestMetrics()
            for provider in self.models.keys()
        }
        
        # Request queue
        self.queue = RequestQueue()
        
        # Circuit breaker state
        self.circuit_breakers: Dict[ModelProvider, Dict] = {
            provider: {"open": False, "failures": 0, "last_failure": None}
            for provider in self.models.keys()
        }
        
        logger.info("LLMManager initialized with models: " + ", ".join(p.value for p in self.models.keys()))
    
    def select_model(self, model_type: ModelType) -> ModelProvider:
        """
        Task türüne göre model seç
        
        Args:
            model_type: İstek türü (FAST, COMPLEX, BALANCED)
            
        Returns:
            Seçilen model provider
        """
        if model_type == ModelType.FAST:
            return ModelProvider.GEMINI_FLASH
        elif model_type == ModelType.COMPLEX:
            return ModelProvider.GEMINI_PRO
        elif model_type == ModelType.FALLBACK:
            return ModelProvider.DEEPSEEK
        else:  # BALANCED
            # Check circuit breakers and load
            flash_healthy = not self.circuit_breakers[ModelProvider.GEMINI_FLASH]["open"]
            pro_healthy = not self.circuit_breakers[ModelProvider.GEMINI_PRO]["open"]
            
            if flash_healthy:
                return ModelProvider.GEMINI_FLASH
            elif pro_healthy:
                return ModelProvider.GEMINI_PRO
            else:
                return ModelProvider.DEEPSEEK
    
    def get_fallback_chain(self, primary: ModelProvider) -> List[ModelProvider]:
        """
        Fallback zincirini al
        
        Args:
            primary: Birincil model
            
        Returns:
            Sıralı fallback listesi
        """
        chain = []
        
        if primary == ModelProvider.GEMINI_FLASH:
            chain = [ModelProvider.GEMINI_PRO, ModelProvider.DEEPSEEK]
        elif primary == ModelProvider.GEMINI_PRO:
            chain = [ModelProvider.GEMINI_FLASH, ModelProvider.DEEPSEEK]
        else:
            chain = [ModelProvider.GEMINI_FLASH, ModelProvider.GEMINI_PRO]
        
        # Filter out models with open circuit breakers
        return [m for m in chain if not self.circuit_breakers[m]["open"]]
    
    async def generate(
        self,
        prompt: str,
        model_type: ModelType = ModelType.BALANCED,
        config_override: Optional[Dict[str, Any]] = None,
        retry_on_fallback: bool = True
    ) -> Dict[str, Any]:
        """
        LLM ile metin üret
        
        Args:
            prompt: Input prompt
            model_type: Model seçim türü
            config_override: Konfigürasyon override
            retry_on_fallback: Fallback'te tekrar dene
            
        Returns:
            {
                "success": bool,
                "text": str,
                "model_used": str,
                "latency": float,
                "tokens_used": int,
                "fallback_used": bool
            }
        """
        start_time = time.time()
        primary_model = self.select_model(model_type)
        fallback_chain = self.get_fallback_chain(primary_model) if retry_on_fallback else []
        
        models_to_try = [primary_model] + fallback_chain
        last_error = None
        fallback_used = False
        
        for i, model in enumerate(models_to_try):
            if i > 0:
                fallback_used = True
                logger.info(f"🔄 Falling back to {model.value}")
            
            try:
                result = await self._call_model(model, prompt, config_override)
                
                if result["success"]:
                    result["fallback_used"] = fallback_used
                    result["models_tried"] = i + 1
                    return result
                
                last_error = result.get("error", "Unknown error")
                
            except Exception as e:
                last_error = str(e)
                self._record_failure(model)
                logger.warning(f"Model {model.value} failed: {e}")
        
        # All models failed
        return {
            "success": False,
            "text": "",
            "model_used": primary_model.value,
            "latency": time.time() - start_time,
            "tokens_used": 0,
            "fallback_used": fallback_used,
            "error": last_error
        }
    
    async def _call_model(
        self,
        model: ModelProvider,
        prompt: str,
        config_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Belirli bir modeli çağır
        """
        start_time = time.time()
        config = self.models[model]
        
        # Rate limiting
        rate_limiter = self.rate_limiters[model]
        wait_time = await rate_limiter.acquire()
        
        if wait_time > 0:
            logger.debug(f"Rate limited, waited {wait_time:.2f}s for {model.value}")
        
        try:
            if model in [ModelProvider.GEMINI_FLASH, ModelProvider.GEMINI_PRO]:
                result = await self._call_gemini(model, prompt, config, config_override)
            else:
                result = await self._call_deepseek(prompt, config, config_override)
            
            # Record success
            latency = time.time() - start_time
            self._record_success(model, latency, result.get("tokens_used", 0))
            
            return result
            
        except Exception as e:
            self._record_failure(model)
            raise
    
    async def _call_gemini(
        self,
        model: ModelProvider,
        prompt: str,
        config: ModelConfig,
        config_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Gemini API çağrısı"""
        from google.genai import types
        
        if not self.gemini_client:
            raise ValueError("Gemini client not initialized")
        
        gen_config = types.GenerateContentConfig(
            temperature=config_override.get("temperature", config.temperature) if config_override else config.temperature,
            top_p=config_override.get("top_p", config.top_p) if config_override else config.top_p,
            max_output_tokens=config_override.get("max_tokens", config.max_tokens) if config_override else config.max_tokens,
        )
        
        response = await self.gemini_client.aio.models.generate_content(
            model=model.value,
            contents=prompt,
            config=gen_config
        )
        
        return {
            "success": True,
            "text": response.text,
            "model_used": model.value,
            "latency": 0,  # Will be calculated outside
            "tokens_used": 0  # Gemini doesn't always return token count
        }
    
    async def _call_deepseek(
        self,
        prompt: str,
        config: ModelConfig,
        config_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """DeepSeek API çağrısı"""
        import httpx
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not set")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": config_override.get("temperature", config.temperature) if config_override else config.temperature,
                    "max_tokens": config_override.get("max_tokens", config.max_tokens) if config_override else config.max_tokens,
                }
            )
            
            data = response.json()
            
            if response.status_code != 200:
                raise Exception(f"DeepSeek API error: {data}")
            
            return {
                "success": True,
                "text": data["choices"][0]["message"]["content"],
                "model_used": "deepseek-chat",
                "latency": 0,
                "tokens_used": data.get("usage", {}).get("total_tokens", 0)
            }
    
    def _record_success(self, model: ModelProvider, latency: float, tokens: int):
        """Başarılı istek kaydet"""
        metrics = self.metrics[model]
        metrics.total_requests += 1
        metrics.successful_requests += 1
        metrics.total_latency += latency
        metrics.total_tokens += tokens
        metrics.last_request_time = datetime.utcnow()
        
        # Reset circuit breaker
        self.circuit_breakers[model]["failures"] = 0
        self.circuit_breakers[model]["open"] = False
    
    def _record_failure(self, model: ModelProvider):
        """Başarısız istek kaydet"""
        metrics = self.metrics[model]
        metrics.total_requests += 1
        metrics.failed_requests += 1
        metrics.last_request_time = datetime.utcnow()
        
        # Update circuit breaker
        cb = self.circuit_breakers[model]
        cb["failures"] += 1
        cb["last_failure"] = datetime.utcnow()
        
        # Open circuit after 3 consecutive failures
        if cb["failures"] >= 3:
            cb["open"] = True
            logger.warning(f"🔴 Circuit breaker OPENED for {model.value}")
            
            # Schedule reset after 60 seconds
            asyncio.create_task(self._reset_circuit_breaker(model, 60))
    
    async def _reset_circuit_breaker(self, model: ModelProvider, delay: int):
        """Circuit breaker'ı belirli süre sonra sıfırla"""
        await asyncio.sleep(delay)
        self.circuit_breakers[model]["open"] = False
        self.circuit_breakers[model]["failures"] = 0
        logger.info(f"🟢 Circuit breaker RESET for {model.value}")
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Tüm metriklerin özetini al"""
        return {
            model.value: {
                "total_requests": metrics.total_requests,
                "success_rate": round(metrics.success_rate, 2),
                "avg_latency": round(metrics.avg_latency, 3),
                "total_tokens": metrics.total_tokens,
                "rate_limit_hits": metrics.rate_limit_hits,
                "circuit_open": self.circuit_breakers[model]["open"]
            }
            for model, metrics in self.metrics.items()
        }


# =============================================================================
# AGENT MODEL SELECTOR
# =============================================================================

def get_model_for_agent(agent_name: str) -> ModelType:
    """
    Agent'a göre uygun model türünü belirle
    
    Complexity mapping:
    - Simple agents (ELI5, basic metrics) -> FAST
    - Complex agents (Domain Master, Governor) -> COMPLEX
    - Standard agents -> BALANCED
    """
    fast_agents = [
        "eli5Formatter",
        "contentPlanGenerator",
    ]
    
    complex_agents = [
        "domainMaster",
        "systemGovernor",
        "deepseekFinalAnalyst",
    ]
    
    if agent_name in fast_agents:
        return ModelType.FAST
    elif agent_name in complex_agents:
        return ModelType.COMPLEX
    else:
        return ModelType.BALANCED


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_llm_manager(gemini_client=None) -> LLMManager:
    """LLM Manager factory"""
    return LLMManager(gemini_client)
