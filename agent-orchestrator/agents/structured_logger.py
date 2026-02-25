# =============================================================================
# Structured Logger - Error Handling ve Monitoring Modülü
# Version 2.0 - Instagram AI Agent System
# =============================================================================
"""
Merkezi logging ve error handling sistemi:
1. Yapılandırılmış JSON log formatı
2. Agent-bazlı log filtreleme
3. Performance metrikleri
4. Error tracking ve alerting

Kullanım:
    from agents.structured_logger import get_logger, LogContext, track_execution
    
    logger = get_logger("agent_name")
    
    with LogContext(logger, "operation_name", user_id="123"):
        result = do_something()
        
    @track_execution(logger)
    async def my_function():
        pass
"""

import json
import logging
import sys
import time
import traceback
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Optional
import asyncio


# =============================================================================
# CONFIGURATION
# =============================================================================

LOG_LEVEL = logging.INFO
LOG_FORMAT = "json"  # "json" or "text"
LOG_FILE = "agent_orchestrator.log"
ENABLE_FILE_LOGGING = True
ENABLE_CONSOLE_LOGGING = True

# Performance thresholds (seconds)
SLOW_OPERATION_THRESHOLD = 5.0
VERY_SLOW_OPERATION_THRESHOLD = 30.0


# =============================================================================
# JSON FORMATTER
# =============================================================================

class JsonFormatter(logging.Formatter):
    """
    JSON formatında log çıktısı üretir
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields
        if hasattr(record, 'agent_name'):
            log_data["agent_name"] = record.agent_name
        if hasattr(record, 'operation'):
            log_data["operation"] = record.operation
        if hasattr(record, 'duration_ms'):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, 'analysis_id'):
            log_data["analysis_id"] = record.analysis_id
        if hasattr(record, 'username'):
            log_data["username"] = record.username
        if hasattr(record, 'user_id'):
            log_data["user_id"] = record.user_id
        if hasattr(record, 'error_type'):
            log_data["error_type"] = record.error_type
        if hasattr(record, 'error_details'):
            log_data["error_details"] = record.error_details
        if hasattr(record, 'model_used'):
            log_data["model_used"] = record.model_used
        if hasattr(record, 'token_count'):
            log_data["token_count"] = record.token_count
        if hasattr(record, 'quality_score'):
            log_data["quality_score"] = record.quality_score
        if hasattr(record, 'self_corrected'):
            log_data["self_corrected"] = record.self_corrected
        if hasattr(record, 'extra_data'):
            log_data["extra_data"] = record.extra_data
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info) if record.exc_info[2] else None
            }
        
        return json.dumps(log_data, ensure_ascii=False)


class TextFormatter(logging.Formatter):
    """
    Okunabilir text formatında log çıktısı
    """
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Build base message
        msg = f"{timestamp} | {color}{record.levelname:8}{reset} | {record.name:20} | {record.getMessage()}"
        
        # Add context if available
        extras = []
        if hasattr(record, 'agent_name'):
            extras.append(f"agent={record.agent_name}")
        if hasattr(record, 'operation'):
            extras.append(f"op={record.operation}")
        if hasattr(record, 'duration_ms'):
            extras.append(f"duration={record.duration_ms}ms")
        if hasattr(record, 'analysis_id'):
            extras.append(f"analysis={record.analysis_id[:8]}...")
        
        if extras:
            msg += f" [{', '.join(extras)}]"
        
        return msg


# =============================================================================
# LOGGER SETUP
# =============================================================================

_loggers: Dict[str, logging.Logger] = {}


def get_logger(name: str) -> logging.Logger:
    """
    Named logger al veya oluştur
    
    Args:
        name: Logger adı (örn: "orchestrator", "growth_virality")
        
    Returns:
        Configured logger instance
    """
    if name in _loggers:
        return _loggers[name]
    
    logger = logging.getLogger(f"instagram_ai.{name}")
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler
    if ENABLE_CONSOLE_LOGGING:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(LOG_LEVEL)
        
        if LOG_FORMAT == "json":
            console_handler.setFormatter(JsonFormatter())
        else:
            console_handler.setFormatter(TextFormatter())
        
        logger.addHandler(console_handler)
    
    # File handler
    if ENABLE_FILE_LOGGING:
        try:
            file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
            file_handler.setLevel(LOG_LEVEL)
            file_handler.setFormatter(JsonFormatter())  # Always JSON for files
            logger.addHandler(file_handler)
        except Exception:
            pass  # Skip file logging if can't create file
    
    _loggers[name] = logger
    return logger


# =============================================================================
# LOG CONTEXT MANAGER
# =============================================================================

@contextmanager
def LogContext(
    logger: logging.Logger,
    operation: str,
    **context_data
):
    """
    Context manager for logging operations with timing
    
    Usage:
        with LogContext(logger, "analyze_account", username="test_user"):
            result = analyze()
    """
    start_time = time.time()
    
    # Log start
    extra = {
        "operation": operation,
        **context_data
    }
    logger.info(f"Starting {operation}", extra=extra)
    
    error_occurred = None
    try:
        yield
    except Exception as e:
        error_occurred = e
        duration_ms = int((time.time() - start_time) * 1000)
        
        extra.update({
            "duration_ms": duration_ms,
            "error_type": type(e).__name__,
            "error_details": str(e)
        })
        logger.error(
            f"Failed {operation}: {str(e)}",
            extra=extra,
            exc_info=True
        )
        raise
    finally:
        if error_occurred is None:
            duration_ms = int((time.time() - start_time) * 1000)
            extra["duration_ms"] = duration_ms
            
            # Check for slow operations
            if duration_ms > VERY_SLOW_OPERATION_THRESHOLD * 1000:
                logger.warning(f"Very slow operation {operation}", extra=extra)
            elif duration_ms > SLOW_OPERATION_THRESHOLD * 1000:
                logger.warning(f"Slow operation {operation}", extra=extra)
            else:
                logger.info(f"Completed {operation}", extra=extra)


# =============================================================================
# DECORATORS
# =============================================================================

def track_execution(logger: logging.Logger):
    """
    Decorator to track function execution with timing
    
    Usage:
        @track_execution(logger)
        async def my_function():
            pass
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            operation = f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            
            extra = {"operation": operation}
            
            try:
                result = await func(*args, **kwargs)
                duration_ms = int((time.time() - start_time) * 1000)
                extra["duration_ms"] = duration_ms
                
                logger.debug(f"Executed {func.__name__}", extra=extra)
                return result
                
            except Exception as e:
                duration_ms = int((time.time() - start_time) * 1000)
                extra.update({
                    "duration_ms": duration_ms,
                    "error_type": type(e).__name__,
                    "error_details": str(e)
                })
                logger.error(
                    f"Error in {func.__name__}: {str(e)}",
                    extra=extra,
                    exc_info=True
                )
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            operation = f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            
            extra = {"operation": operation}
            
            try:
                result = func(*args, **kwargs)
                duration_ms = int((time.time() - start_time) * 1000)
                extra["duration_ms"] = duration_ms
                
                logger.debug(f"Executed {func.__name__}", extra=extra)
                return result
                
            except Exception as e:
                duration_ms = int((time.time() - start_time) * 1000)
                extra.update({
                    "duration_ms": duration_ms,
                    "error_type": type(e).__name__,
                    "error_details": str(e)
                })
                logger.error(
                    f"Error in {func.__name__}: {str(e)}",
                    extra=extra,
                    exc_info=True
                )
                raise
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


def log_agent_result(logger: logging.Logger):
    """
    Decorator specifically for agent analyze methods
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, data: Dict[str, Any], *args, **kwargs):
            agent_name = getattr(self, 'agent_name', 'unknown')
            analysis_id = data.get('analysis_id', 'N/A')
            username = data.get('username', data.get('account', {}).get('username', 'N/A'))
            
            start_time = time.time()
            
            extra = {
                "agent_name": agent_name,
                "analysis_id": analysis_id,
                "username": username,
                "operation": "analyze"
            }
            
            logger.info(f"Agent {agent_name} starting analysis", extra=extra)
            
            try:
                result = await func(self, data, *args, **kwargs)
                
                duration_ms = int((time.time() - start_time) * 1000)
                
                # Extract result metadata
                if isinstance(result, dict):
                    extra.update({
                        "duration_ms": duration_ms,
                        "model_used": result.get("modelUsed", ""),
                        "self_corrected": result.get("selfCorrected", False),
                        "findings_count": len(result.get("findings", [])),
                        "recommendations_count": len(result.get("recommendations", [])),
                        "quality_score": result.get("qualityScore", None),
                    })
                else:
                    extra["duration_ms"] = duration_ms
                
                logger.info(f"Agent {agent_name} completed analysis", extra=extra)
                return result
                
            except Exception as e:
                duration_ms = int((time.time() - start_time) * 1000)
                extra.update({
                    "duration_ms": duration_ms,
                    "error_type": type(e).__name__,
                    "error_details": str(e)
                })
                logger.error(
                    f"Agent {agent_name} failed: {str(e)}",
                    extra=extra,
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator


# =============================================================================
# ERROR CLASSES
# =============================================================================

class AgentError(Exception):
    """Base exception for agent errors"""
    
    def __init__(self, message: str, agent_name: str = None, details: Dict = None):
        super().__init__(message)
        self.agent_name = agent_name
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()


class LLMError(AgentError):
    """LLM API related errors"""
    
    def __init__(self, message: str, model: str = None, **kwargs):
        super().__init__(message, **kwargs)
        self.model = model


class ValidationError(AgentError):
    """Data validation errors"""
    
    def __init__(self, message: str, field: str = None, value: Any = None, **kwargs):
        super().__init__(message, **kwargs)
        self.field = field
        self.value = value


class RateLimitError(AgentError):
    """Rate limit exceeded errors"""
    
    def __init__(self, message: str, retry_after: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ScrapingError(AgentError):
    """Instagram scraping errors"""
    
    def __init__(self, message: str, username: str = None, **kwargs):
        super().__init__(message, **kwargs)
        self.username = username


# =============================================================================
# METRICS COLLECTOR
# =============================================================================

class MetricsCollector:
    """
    Simple in-memory metrics collector
    """
    
    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, list] = {}
        self._lock = asyncio.Lock() if asyncio.get_event_loop().is_running() else None
    
    async def increment(self, name: str, value: int = 1, labels: Dict = None):
        """Increment a counter"""
        key = self._make_key(name, labels)
        if self._lock:
            async with self._lock:
                self.counters[key] = self.counters.get(key, 0) + value
        else:
            self.counters[key] = self.counters.get(key, 0) + value
    
    async def set_gauge(self, name: str, value: float, labels: Dict = None):
        """Set a gauge value"""
        key = self._make_key(name, labels)
        self.gauges[key] = value
    
    async def observe(self, name: str, value: float, labels: Dict = None):
        """Observe a value for histogram"""
        key = self._make_key(name, labels)
        if key not in self.histograms:
            self.histograms[key] = []
        self.histograms[key].append(value)
        
        # Keep only last 1000 observations
        if len(self.histograms[key]) > 1000:
            self.histograms[key] = self.histograms[key][-1000:]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics"""
        result = {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {}
        }
        
        for key, values in self.histograms.items():
            if values:
                sorted_vals = sorted(values)
                result["histograms"][key] = {
                    "count": len(values),
                    "min": sorted_vals[0],
                    "max": sorted_vals[-1],
                    "avg": sum(values) / len(values),
                    "p50": sorted_vals[len(sorted_vals) // 2],
                    "p95": sorted_vals[int(len(sorted_vals) * 0.95)],
                    "p99": sorted_vals[int(len(sorted_vals) * 0.99)],
                }
        
        return result
    
    def _make_key(self, name: str, labels: Optional[Dict]) -> str:
        """Create metric key with labels"""
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"


# Global metrics collector
metrics = MetricsCollector()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def log_analysis_start(
    logger: logging.Logger,
    analysis_id: str,
    username: str,
    user_id: str = None
):
    """Log analysis start event"""
    logger.info(
        f"Analysis started for @{username}",
        extra={
            "analysis_id": analysis_id,
            "username": username,
            "user_id": user_id,
            "operation": "analysis_start"
        }
    )


def log_analysis_complete(
    logger: logging.Logger,
    analysis_id: str,
    username: str,
    duration_ms: int,
    overall_score: float = None,
    agents_completed: int = None
):
    """Log analysis completion event"""
    logger.info(
        f"Analysis completed for @{username}",
        extra={
            "analysis_id": analysis_id,
            "username": username,
            "duration_ms": duration_ms,
            "quality_score": overall_score,
            "operation": "analysis_complete",
            "extra_data": {"agents_completed": agents_completed}
        }
    )


def log_llm_call(
    logger: logging.Logger,
    model: str,
    prompt_tokens: int = None,
    completion_tokens: int = None,
    duration_ms: int = None,
    success: bool = True,
    error: str = None
):
    """Log LLM API call"""
    extra = {
        "operation": "llm_call",
        "model_used": model,
        "token_count": (prompt_tokens or 0) + (completion_tokens or 0),
        "extra_data": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens
        }
    }
    
    if duration_ms:
        extra["duration_ms"] = duration_ms
    
    if success:
        logger.debug(f"LLM call to {model} succeeded", extra=extra)
    else:
        extra["error_type"] = "LLMError"
        extra["error_details"] = error
        logger.warning(f"LLM call to {model} failed: {error}", extra=extra)
