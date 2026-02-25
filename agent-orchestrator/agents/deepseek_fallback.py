# DeepSeek Secondary Helper
# Gemini (primary) başarısız olduğunda DeepSeek (secondary) devreye girer
"""
DeepSeek Secondary System

Gemini (primary model) başarısız olduğunda bu modül:
1. DeepSeek API'yi kullanarak aynı analizi yapar
2. Gemini ile uyumlu response formatı döner
3. Seamless secondary/fallback sağlar
"""

import asyncio
import json
import logging
import os
import httpx
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class DeepSeekFallback:
    """
    DeepSeek Secondary - Gemini (primary) başarısız olduğunda devreye girer
    
    OpenAI-compatible API kullanır
    """
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.timeout = httpx.Timeout(120.0, connect=15.0)
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            logger.warning("DeepSeek Secondary disabled - DEEPSEEK_API_KEY not set")
    
    async def generate_content(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 8192
    ) -> str:
        """
        Generate content using DeepSeek API
        
        Args:
            system_prompt: System instructions
            user_prompt: User query
            temperature: Sampling temperature
            max_tokens: Max output tokens
            
        Returns:
            Generated text response
        """
        if not self.enabled:
            raise RuntimeError("DeepSeek not configured - API key missing")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.error("DeepSeek also rate limited!")
                raise
            logger.error(f"DeepSeek HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"DeepSeek error: {e}")
            raise
    
    async def run_agent_analysis(
        self,
        agent_name: str,
        system_prompt: str,
        user_prompt: str
    ) -> Dict[str, Any]:
        """
        Run an agent's analysis using DeepSeek instead of Gemini
        
        Args:
            agent_name: Name of the agent
            system_prompt: Agent's system prompt
            user_prompt: Analysis prompt with data
            
        Returns:
            Parsed analysis result
        """
        logger.info(f"[DeepSeek Secondary] Running {agent_name}...")
        
        try:
            # Call DeepSeek
            response_text = await self.generate_content(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            # Parse JSON from response
            result = self._parse_json_response(response_text)
            
            # Add metadata
            result["agentName"] = agent_name
            result["modelUsed"] = f"deepseek-secondary:{self.model}"
            result["timestamp"] = datetime.utcnow().isoformat()
            result["fallback"] = True
            
            logger.info(f"[DeepSeek Secondary] ✓ {agent_name} completed")
            return result
            
        except Exception as e:
            logger.error(f"[DeepSeek Secondary] ✗ {agent_name} failed: {e}")
            return {
                "agent": agent_name,
                "error": True,
                "errorMessage": str(e),
                "fallback": True,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parse JSON from LLM response"""
        # Try direct JSON parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        import re
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON object in text
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Return as raw response
        return {
            "rawResponse": text,
            "parseError": True,
            "findings": [],
            "recommendations": [],
            "metrics": {"overallScore": 50}
        }


# Global instance
_deepseek_fallback: Optional[DeepSeekFallback] = None


def get_deepseek_fallback() -> DeepSeekFallback:
    """Get or create DeepSeek secondary instance"""
    global _deepseek_fallback
    if _deepseek_fallback is None:
        _deepseek_fallback = DeepSeekFallback()
    return _deepseek_fallback


def is_fallback_available() -> bool:
    """Check if DeepSeek secondary is available"""
    return get_deepseek_fallback().enabled
