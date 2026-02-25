# =============================================================================
# Test Suite - Instagram AI Agent System v2.0
# =============================================================================
"""
Unit tests for new v2.0 modules:
1. models.py - Pydantic validation
2. cot_prompting.py - Chain-of-Thought, self-correction
3. llm_manager.py - Multi-LLM management
4. output_serializer.py - Output normalization
5. structured_logger.py - Logging and error handling

Run tests:
    python -m pytest tests/ -v
    python -m pytest tests/test_v2_modules.py -v --tb=short
"""

import asyncio
import json
import pytest
from datetime import datetime
from typing import Dict, Any


# =============================================================================
# TEST DATA FIXTURES
# =============================================================================

@pytest.fixture
def sample_account_data():
    """Sample account data for testing"""
    return {
        "username": "test_account",
        "fullName": "Test Account",
        "followers": 15000,
        "following": 500,
        "posts": 250,
        "bio": "Digital marketing expert | Growth specialist | Contact: test@example.com",
        "profilePicUrl": "https://example.com/pic.jpg",
        "isVerified": False,
        "isPrivate": False,
        "isBusiness": True,
        "category": "Digital Marketing",
        "engagementRate": 3.5,
        "avgLikes": 525,
        "avgComments": 35,
    }


@pytest.fixture
def sample_posts_data():
    """Sample posts data for testing"""
    return [
        {
            "id": "post_1",
            "timestamp": "2024-01-15T10:00:00Z",
            "type": "Image",
            "caption": "New content strategy tips #marketing #growth",
            "likesCount": 580,
            "commentsCount": 42,
            "hashtags": ["marketing", "growth"],
        },
        {
            "id": "post_2",
            "timestamp": "2024-01-14T15:30:00Z",
            "type": "Carousel",
            "caption": "5 steps to boost engagement #socialmedia",
            "likesCount": 720,
            "commentsCount": 65,
            "hashtags": ["socialmedia"],
        },
    ]


@pytest.fixture
def sample_agent_result():
    """Sample agent result for testing"""
    return {
        "agentRole": "Growth Virality Agent",
        "findings": [
            {
                "type": "strength",
                "category": "growth",
                "finding": "Account shows consistent growth with 15% monthly follower increase over the past 6 months, indicating strong content resonance with target audience.",
                "evidence": "Monthly growth data from profile",
                "impact_score": 85
            },
            {
                "type": "weakness",
                "category": "engagement",
                "finding": "Comment-to-like ratio is below industry average at 5.8%, suggesting audience prefers passive engagement over active participation.",
                "evidence": "Average 35 comments vs 525 likes",
                "impact_score": 70
            }
        ],
        "recommendations": [
            {
                "priority": "high",
                "category": "engagement",
                "action": "Implement engagement-boosting strategies like asking questions in captions and creating content that encourages audience discussion",
                "expected_impact": "Expected 25-40% increase in comment rate within 30 days",
                "implementation": "Add open-ended questions to every post caption, respond to all comments within 2 hours",
                "difficulty": "easy",
                "timeline": "2 weeks",
                "kpi": "Comments per post"
            }
        ],
        "metrics": {
            "overallScore": 72.5,
            "confidence": 85.0,
            "growthScore": 78.0,
            "engagementScore": 65.0
        }
    }


# =============================================================================
# MODELS.PY TESTS
# =============================================================================

class TestModels:
    """Test Pydantic models in models.py"""
    
    def test_account_data_validation(self, sample_account_data):
        """Test AccountData model validation"""
        from agents.models import AccountData
        
        account = AccountData(**sample_account_data)
        
        assert account.username == "test_account"
        assert account.followers == 15000
        assert account.engagement_rate == 3.5
    
    def test_account_data_invalid_username(self):
        """Test AccountData rejects invalid username"""
        from agents.models import AccountData
        from pydantic import ValidationError as PydanticValidationError
        
        with pytest.raises(PydanticValidationError):
            AccountData(
                username="",  # Empty username should fail
                followers=1000,
            )
    
    def test_agent_finding_min_length(self):
        """Test AgentFinding enforces minimum length"""
        from agents.models import AgentFinding
        from pydantic import ValidationError as PydanticValidationError
        
        # Valid finding (>100 chars)
        valid_finding = AgentFinding(
            type="strength",
            category="growth",
            finding="A" * 100,  # Exactly 100 chars
            evidence="Supporting evidence",
            impact_score=75
        )
        assert len(valid_finding.finding) >= 100
        
        # Invalid finding (<100 chars)
        with pytest.raises(PydanticValidationError):
            AgentFinding(
                type="strength",
                category="growth",
                finding="Too short",  # Less than 100 chars
                evidence="Evidence",
                impact_score=75
            )
    
    def test_agent_recommendation_min_length(self):
        """Test AgentRecommendation enforces minimum length"""
        from agents.models import AgentRecommendation
        from pydantic import ValidationError as PydanticValidationError
        
        # Valid recommendation (>150 chars)
        valid_rec = AgentRecommendation(
            priority="high",
            category="growth",
            action="B" * 150,  # Exactly 150 chars
            expected_impact="25% growth expected",
            implementation="Step by step implementation guide",
            difficulty="medium",
            timeline="2 weeks",
            kpi="Follower count"
        )
        assert len(valid_rec.action) >= 150
        
        # Invalid recommendation (<150 chars)
        with pytest.raises(PydanticValidationError):
            AgentRecommendation(
                priority="high",
                category="growth",
                action="Too short",
                expected_impact="Impact",
                implementation="Implementation",
                difficulty="medium",
                timeline="2 weeks",
                kpi="KPI"
            )
    
    def test_score_bounds(self):
        """Test score values are bounded 0-100"""
        from agents.models import AgentResult
        from pydantic import ValidationError as PydanticValidationError
        
        # Score > 100 should fail
        with pytest.raises(PydanticValidationError):
            AgentResult(
                agent_name="test",
                agent_role="Test Agent",
                findings=[],
                recommendations=[],
                metrics={"overallScore": 150},  # Invalid: > 100
            )


# =============================================================================
# COT_PROMPTING.PY TESTS
# =============================================================================

class TestCoTPrompting:
    """Test Chain-of-Thought prompting module"""
    
    def test_validate_output_quality_valid(self, sample_agent_result):
        """Test quality validation passes for valid output"""
        from agents.cot_prompting import validate_output_quality
        
        is_valid, issues, score = validate_output_quality(sample_agent_result)
        
        assert is_valid == True
        assert score >= 60  # Should pass minimum threshold
        assert len(issues) == 0
    
    def test_validate_output_quality_short_finding(self):
        """Test quality validation fails for short findings"""
        from agents.cot_prompting import validate_output_quality
        
        bad_result = {
            "findings": [
                {"finding": "Too short", "type": "info", "category": "general"}
            ],
            "recommendations": [],
            "metrics": {"overallScore": 50}
        }
        
        is_valid, issues, score = validate_output_quality(bad_result)
        
        assert is_valid == False
        assert score < 60
        assert any("short" in issue.lower() for issue in issues)
    
    def test_cot_template_sections(self):
        """Test COT template has all required sections"""
        from agents.cot_prompting import COT_ANALYSIS_TEMPLATE
        
        required_sections = [
            "DATA REVIEW",
            "BENCHMARK",
            "PATTERN",
            "SWOT",
            "RECOMMENDATION",
            "SCORING"
        ]
        
        for section in required_sections:
            assert section in COT_ANALYSIS_TEMPLATE
    
    def test_calculate_viral_potential(self, sample_account_data):
        """Test viral potential calculation"""
        from agents.cot_prompting import calculate_viral_potential
        
        viral_score = calculate_viral_potential(
            engagement_rate=sample_account_data["engagementRate"],
            followers=sample_account_data["followers"],
            avg_comments=sample_account_data["avgComments"],
            avg_likes=sample_account_data["avgLikes"]
        )
        
        assert 0 <= viral_score <= 100
        assert isinstance(viral_score, float)
    
    def test_predict_growth_trajectory(self, sample_account_data):
        """Test growth trajectory prediction"""
        from agents.cot_prompting import predict_growth_trajectory
        
        trajectory = predict_growth_trajectory(
            current_followers=sample_account_data["followers"],
            monthly_growth_rate=5.0,  # 5% monthly growth
            engagement_rate=sample_account_data["engagementRate"]
        )
        
        assert "projected_6_months" in trajectory
        assert "projected_12_months" in trajectory
        assert trajectory["projected_6_months"] > sample_account_data["followers"]


# =============================================================================
# LLM_MANAGER.PY TESTS
# =============================================================================

class TestLLMManager:
    """Test Multi-LLM manager module"""
    
    def test_model_type_selection(self):
        """Test model type selection for different agents"""
        from agents.llm_manager import get_model_for_agent, ModelType
        
        # Domain master should use COMPLEX model
        model_type = get_model_for_agent("domainMaster")
        assert model_type == ModelType.COMPLEX
        
        # Content strategist should use BALANCED model
        model_type = get_model_for_agent("contentStrategist")
        assert model_type == ModelType.BALANCED
        
        # Unknown agent should default to BALANCED
        model_type = get_model_for_agent("unknownAgent")
        assert model_type == ModelType.BALANCED
    
    @pytest.mark.asyncio
    async def test_rate_limiter_basic(self):
        """Test rate limiter token acquisition"""
        from agents.llm_manager import AsyncRateLimiter
        
        limiter = AsyncRateLimiter(requests_per_minute=60)
        
        # First acquisition should succeed immediately
        start = asyncio.get_event_loop().time()
        await limiter.acquire()
        elapsed = asyncio.get_event_loop().time() - start
        
        assert elapsed < 0.1  # Should be nearly instant
    
    def test_model_provider_enum(self):
        """Test model provider enum values"""
        from agents.llm_manager import ModelProvider
        
        assert ModelProvider.GEMINI_FLASH.value == "gemini-2.0-flash"
        assert ModelProvider.GEMINI_PRO.value == "gemini-1.5-pro"
        assert ModelProvider.DEEPSEEK.value == "deepseek-chat"


# =============================================================================
# OUTPUT_SERIALIZER.PY TESTS
# =============================================================================

class TestOutputSerializer:
    """Test output serialization module"""
    
    def test_score_to_grade(self):
        """Test score to grade conversion"""
        from agents.output_serializer import score_to_grade
        
        # Test various scores
        grade, label, color = score_to_grade(95)
        assert grade == "A+"
        assert label == "Mükemmel"
        
        grade, label, color = score_to_grade(75)
        assert grade == "B+"
        assert label == "İyi"
        
        grade, label, color = score_to_grade(45)
        assert grade == "D+"
        assert label == "Zayıf"
        
        grade, label, color = score_to_grade(20)
        assert grade == "F"
        assert label == "Başarısız"
    
    def test_serialize_analysis(self, sample_account_data, sample_agent_result):
        """Test full analysis serialization"""
        from agents.output_serializer import serialize_analysis
        
        raw_results = {
            "analysisId": "test-123",
            "agentResults": {
                "growthVirality": sample_agent_result
            },
            "eli5Report": {},
            "finalVerdict": {},
        }
        
        serialized = serialize_analysis(raw_results, sample_account_data)
        
        # Check structure
        assert "metadata" in serialized
        assert "account" in serialized
        assert "overallScore" in serialized
        assert "agentResults" in serialized
        
        # Check account normalization
        assert serialized["account"]["username"] == "test_account"
        assert serialized["account"]["followers"] == 15000
        
        # Check overall score
        assert "grade" in serialized["overallScore"]
        assert "label" in serialized["overallScore"]
    
    def test_normalize_findings_from_string(self):
        """Test finding normalization from string"""
        from agents.output_serializer import OutputSerializer
        
        serializer = OutputSerializer()
        
        string_findings = [
            "This is a string finding that should be normalized to dict format"
        ]
        
        normalized = serializer._normalize_findings(string_findings)
        
        assert len(normalized) == 1
        assert isinstance(normalized[0], dict)
        assert "finding" in normalized[0]
        assert "type" in normalized[0]


# =============================================================================
# STRUCTURED_LOGGER.PY TESTS
# =============================================================================

class TestStructuredLogger:
    """Test structured logging module"""
    
    def test_get_logger(self):
        """Test logger creation"""
        from agents.structured_logger import get_logger
        
        logger = get_logger("test_agent")
        
        assert logger is not None
        assert "instagram_ai.test_agent" in logger.name
    
    def test_logger_caching(self):
        """Test logger instances are cached"""
        from agents.structured_logger import get_logger
        
        logger1 = get_logger("cached_test")
        logger2 = get_logger("cached_test")
        
        assert logger1 is logger2  # Same instance
    
    def test_agent_error_class(self):
        """Test AgentError exception class"""
        from agents.structured_logger import AgentError
        
        error = AgentError(
            message="Test error",
            agent_name="test_agent",
            details={"key": "value"}
        )
        
        assert str(error) == "Test error"
        assert error.agent_name == "test_agent"
        assert error.details == {"key": "value"}
        assert error.timestamp is not None
    
    def test_llm_error_class(self):
        """Test LLMError exception class"""
        from agents.structured_logger import LLMError
        
        error = LLMError(
            message="API rate limit exceeded",
            model="gemini-2.0-flash",
            agent_name="growth_virality"
        )
        
        assert "rate limit" in str(error)
        assert error.model == "gemini-2.0-flash"
    
    @pytest.mark.asyncio
    async def test_metrics_collector(self):
        """Test metrics collector"""
        from agents.structured_logger import MetricsCollector
        
        metrics = MetricsCollector()
        
        # Test counter
        await metrics.increment("api_calls", 1, {"agent": "test"})
        await metrics.increment("api_calls", 1, {"agent": "test"})
        
        # Test gauge
        await metrics.set_gauge("active_requests", 5.0)
        
        # Test histogram
        await metrics.observe("response_time_ms", 150.0)
        await metrics.observe("response_time_ms", 200.0)
        
        summary = metrics.get_metrics()
        
        assert summary["counters"]["api_calls{agent=test}"] == 2
        assert summary["gauges"]["active_requests"] == 5.0
        assert summary["histograms"]["response_time_ms"]["count"] == 2


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests for combined modules"""
    
    def test_full_pipeline_data_flow(self, sample_account_data, sample_agent_result):
        """Test data flows through all modules correctly"""
        from agents.models import AccountData, AgentResult
        from agents.cot_prompting import validate_output_quality
        from agents.output_serializer import serialize_analysis
        
        # 1. Validate input data
        account = AccountData(**sample_account_data)
        assert account.username == "test_account"
        
        # 2. Validate agent output quality
        is_valid, issues, score = validate_output_quality(sample_agent_result)
        assert is_valid == True
        
        # 3. Serialize for frontend/PDF
        raw_results = {
            "analysisId": "integration-test",
            "agentResults": {"growthVirality": sample_agent_result},
            "eli5Report": {},
            "finalVerdict": {},
        }
        
        serialized = serialize_analysis(raw_results, sample_account_data)
        
        # 4. Verify final output structure
        assert "overallScore" in serialized
        assert "agentResults" in serialized
        assert "chartsData" in serialized
    
    def test_error_handling_chain(self):
        """Test error handling through the system"""
        from agents.structured_logger import (
            AgentError, 
            LLMError, 
            ValidationError,
            get_logger
        )
        
        logger = get_logger("error_test")
        
        # Test error hierarchy
        agent_error = AgentError("Base error", agent_name="test")
        llm_error = LLMError("LLM error", model="gemini", agent_name="test")
        validation_error = ValidationError("Validation failed", field="score", value=150)
        
        # All should be instances of AgentError
        assert isinstance(agent_error, AgentError)
        assert isinstance(llm_error, AgentError)
        assert isinstance(validation_error, AgentError)


# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformance:
    """Performance benchmarks"""
    
    def test_serialization_speed(self, sample_account_data, sample_agent_result):
        """Test serialization completes in reasonable time"""
        import time
        from agents.output_serializer import serialize_analysis
        
        raw_results = {
            "analysisId": "perf-test",
            "agentResults": {f"agent_{i}": sample_agent_result for i in range(10)},
            "eli5Report": {},
            "finalVerdict": {},
        }
        
        start = time.time()
        for _ in range(100):
            serialize_analysis(raw_results, sample_account_data)
        elapsed = time.time() - start
        
        # Should complete 100 serializations in under 1 second
        assert elapsed < 1.0
        
    def test_validation_speed(self, sample_agent_result):
        """Test validation completes in reasonable time"""
        import time
        from agents.cot_prompting import validate_output_quality
        
        start = time.time()
        for _ in range(1000):
            validate_output_quality(sample_agent_result)
        elapsed = time.time() - start
        
        # Should complete 1000 validations in under 1 second
        assert elapsed < 1.0


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
