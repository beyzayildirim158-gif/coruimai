"""
Global Benchmark Data - Single Source of Truth

This module provides centralized benchmark data for all agents and components.
Both LLM prompts and frontend displays should use this same data to ensure consistency.

Usage:
    from agents.global_benchmarks import NICHE_BENCHMARKS, get_benchmarks_for_niche, get_engagement_verdict
"""

from typing import Dict, Any, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL NICHE BENCHMARKS - SINGLE SOURCE OF TRUTH
# ═══════════════════════════════════════════════════════════════════════════════

NICHE_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "fashion": {
        "avg_engagement_rate": 2.1,
        "top_engagement_rate": 5.5,
        "avg_growth_rate": 4.5,
        "top_growth_rate": 12.0,
        "optimal_posts_per_week": (5, 7),
        "reels_percentage": 45,
        "avg_save_rate": 3.2,
        "avg_follower_following_ratio": 8.0,
        "top_follower_following_ratio": 25.0,
        "avg_bot_score": 20,
        "acceptable_bot_score": 15,
        "display_name_tr": "Moda",
        "display_name_en": "Fashion"
    },
    "beauty": {
        "avg_engagement_rate": 2.8,
        "top_engagement_rate": 6.5,
        "avg_growth_rate": 5.2,
        "top_growth_rate": 14.0,
        "optimal_posts_per_week": (5, 6),
        "reels_percentage": 50,
        "avg_save_rate": 4.5,
        "avg_follower_following_ratio": 6.0,
        "top_follower_following_ratio": 20.0,
        "avg_bot_score": 22,
        "acceptable_bot_score": 18,
        "display_name_tr": "Güzellik",
        "display_name_en": "Beauty"
    },
    "fitness": {
        "avg_engagement_rate": 3.5,
        "top_engagement_rate": 8.0,
        "avg_growth_rate": 6.0,
        "top_growth_rate": 15.0,
        "optimal_posts_per_week": (6, 7),
        "reels_percentage": 55,
        "avg_save_rate": 5.8,
        "avg_follower_following_ratio": 10.0,
        "top_follower_following_ratio": 30.0,
        "avg_bot_score": 18,
        "acceptable_bot_score": 12,
        "display_name_tr": "Fitness",
        "display_name_en": "Fitness"
    },
    "food": {
        "avg_engagement_rate": 3.2,
        "top_engagement_rate": 7.5,
        "avg_growth_rate": 5.5,
        "top_growth_rate": 13.0,
        "optimal_posts_per_week": (5, 7),
        "reels_percentage": 40,
        "avg_save_rate": 6.2,
        "avg_follower_following_ratio": 7.0,
        "top_follower_following_ratio": 22.0,
        "avg_bot_score": 19,
        "acceptable_bot_score": 14,
        "display_name_tr": "Yemek",
        "display_name_en": "Food"
    },
    "travel": {
        "avg_engagement_rate": 4.0,
        "top_engagement_rate": 9.0,
        "avg_growth_rate": 4.0,
        "top_growth_rate": 10.0,
        "optimal_posts_per_week": (3, 5),
        "reels_percentage": 50,
        "avg_save_rate": 7.5,
        "avg_follower_following_ratio": 5.0,
        "top_follower_following_ratio": 18.0,
        "avg_bot_score": 17,
        "acceptable_bot_score": 12,
        "display_name_tr": "Seyahat",
        "display_name_en": "Travel"
    },
    "business_b2b": {
        "avg_engagement_rate": 1.5,
        "top_engagement_rate": 4.0,
        "avg_growth_rate": 3.5,
        "top_growth_rate": 8.0,
        "optimal_posts_per_week": (4, 5),
        "reels_percentage": 30,
        "avg_save_rate": 4.0,
        "avg_follower_following_ratio": 4.0,
        "top_follower_following_ratio": 12.0,
        "avg_bot_score": 25,
        "acceptable_bot_score": 20,
        "display_name_tr": "İş/B2B",
        "display_name_en": "Business/B2B"
    },
    "personal_development": {
        "avg_engagement_rate": 2.5,
        "top_engagement_rate": 6.0,
        "avg_growth_rate": 5.0,
        "top_growth_rate": 12.0,
        "optimal_posts_per_week": (5, 6),
        "reels_percentage": 35,
        "avg_save_rate": 5.5,
        "avg_follower_following_ratio": 6.0,
        "top_follower_following_ratio": 18.0,
        "avg_bot_score": 20,
        "acceptable_bot_score": 15,
        "display_name_tr": "Kişisel Gelişim",
        "display_name_en": "Personal Development"
    },
    "parenting": {
        "avg_engagement_rate": 3.8,
        "top_engagement_rate": 8.5,
        "avg_growth_rate": 5.5,
        "top_growth_rate": 12.0,
        "optimal_posts_per_week": (4, 6),
        "reels_percentage": 45,
        "avg_save_rate": 4.8,
        "avg_follower_following_ratio": 5.0,
        "top_follower_following_ratio": 15.0,
        "avg_bot_score": 16,
        "acceptable_bot_score": 12,
        "display_name_tr": "Ebeveynlik",
        "display_name_en": "Parenting"
    },
    "tech": {
        "avg_engagement_rate": 1.8,
        "top_engagement_rate": 4.5,
        "avg_growth_rate": 4.0,
        "top_growth_rate": 10.0,
        "optimal_posts_per_week": (4, 5),
        "reels_percentage": 40,
        "avg_save_rate": 3.5,
        "avg_follower_following_ratio": 5.0,
        "top_follower_following_ratio": 15.0,
        "avg_bot_score": 22,
        "acceptable_bot_score": 18,
        "display_name_tr": "Teknoloji",
        "display_name_en": "Technology"
    },
    "entertainment": {
        "avg_engagement_rate": 4.5,
        "top_engagement_rate": 10.0,
        "avg_growth_rate": 7.0,
        "top_growth_rate": 18.0,
        "optimal_posts_per_week": (7, 10),
        "reels_percentage": 60,
        "avg_save_rate": 4.0,
        "avg_follower_following_ratio": 12.0,
        "top_follower_following_ratio": 40.0,
        "avg_bot_score": 25,
        "acceptable_bot_score": 18,
        "display_name_tr": "Eğlence",
        "display_name_en": "Entertainment"
    },
    "education": {
        "avg_engagement_rate": 2.5,
        "top_engagement_rate": 6.0,
        "avg_growth_rate": 4.5,
        "top_growth_rate": 11.0,
        "optimal_posts_per_week": (4, 6),
        "reels_percentage": 35,
        "avg_save_rate": 6.5,
        "avg_follower_following_ratio": 6.0,
        "top_follower_following_ratio": 20.0,
        "avg_bot_score": 18,
        "acceptable_bot_score": 14,
        "display_name_tr": "Eğitim",
        "display_name_en": "Education"
    },
    "spiritual": {
        "avg_engagement_rate": 3.0,
        "top_engagement_rate": 7.0,
        "avg_growth_rate": 4.0,
        "top_growth_rate": 10.0,
        "optimal_posts_per_week": (5, 7),
        "reels_percentage": 30,
        "avg_save_rate": 5.5,
        "avg_follower_following_ratio": 5.0,
        "top_follower_following_ratio": 15.0,
        "avg_bot_score": 15,
        "acceptable_bot_score": 10,
        "display_name_tr": "Dini/Manevi",
        "display_name_en": "Spiritual"
    },
    "general": {
        "avg_engagement_rate": 2.5,
        "top_engagement_rate": 6.0,
        "avg_growth_rate": 5.0,
        "top_growth_rate": 12.0,
        "optimal_posts_per_week": (5, 7),
        "reels_percentage": 45,
        "avg_save_rate": 4.5,
        "avg_follower_following_ratio": 6.0,
        "top_follower_following_ratio": 18.0,
        "avg_bot_score": 20,
        "acceptable_bot_score": 15,
        "display_name_tr": "Genel",
        "display_name_en": "General"
    }
}

# Default benchmarks for unknown niches
DEFAULT_BENCHMARKS = NICHE_BENCHMARKS["general"]


def get_benchmarks_for_niche(niche: str) -> Dict[str, Any]:
    """
    Get benchmark data for a specific niche.
    Falls back to 'general' benchmarks if niche not found.
    
    Args:
        niche: The niche identifier (e.g., 'fitness', 'fashion')
        
    Returns:
        Dictionary containing all benchmark values for the niche
    """
    niche_key = niche.lower().replace(" ", "_").replace("-", "_")
    return NICHE_BENCHMARKS.get(niche_key, DEFAULT_BENCHMARKS)


def get_engagement_verdict(
    engagement_rate: float, 
    niche: str = "general"
) -> Tuple[str, str]:
    """
    Get verdict label and color for engagement rate.
    
    Args:
        engagement_rate: The engagement rate percentage
        niche: The niche for benchmark comparison
        
    Returns:
        Tuple of (verdict_label, color_class)
    """
    benchmarks = get_benchmarks_for_niche(niche)
    avg = benchmarks["avg_engagement_rate"]
    top = benchmarks["top_engagement_rate"]
    
    if engagement_rate >= top * 0.9:
        return ("Üst Düzey", "green")
    elif engagement_rate >= avg:
        return ("Ortalamanın Üstünde", "green")
    elif engagement_rate >= avg * 0.7:
        return ("Ortalama", "yellow")
    else:
        return ("Ortalamanın Altında", "red")


def get_bot_score_verdict(
    bot_score: float,
    niche: str = "general"
) -> Tuple[str, str]:
    """
    Get verdict label and color for bot score.
    NOTE: Lower bot score is better.
    
    Args:
        bot_score: The bot risk score (0-100)
        niche: The niche for benchmark comparison
        
    Returns:
        Tuple of (verdict_label, color_class)
    """
    benchmarks = get_benchmarks_for_niche(niche)
    avg = benchmarks["avg_bot_score"]
    acceptable = benchmarks["acceptable_bot_score"]
    
    if bot_score <= acceptable:
        return ("Düşük Risk", "green")
    elif bot_score <= avg:
        return ("Normal", "green")
    elif bot_score <= avg * 1.3:
        return ("Dikkat", "yellow")
    else:
        return ("Yüksek Risk", "red")


def get_growth_verdict(
    growth_rate: float,
    niche: str = "general"
) -> Tuple[str, str]:
    """
    Get verdict label and color for growth rate.
    
    Args:
        growth_rate: The monthly growth rate percentage
        niche: The niche for benchmark comparison
        
    Returns:
        Tuple of (verdict_label, color_class)
    """
    benchmarks = get_benchmarks_for_niche(niche)
    avg = benchmarks["avg_growth_rate"]
    top = benchmarks["top_growth_rate"]
    
    if growth_rate >= top * 0.9:
        return ("Hızlı Büyüme", "green")
    elif growth_rate >= avg:
        return ("Ortalamanın Üstünde", "green")
    elif growth_rate >= avg * 0.5:
        return ("Ortalama", "yellow")
    elif growth_rate > 0:
        return ("Yavaş Büyüme", "yellow")
    else:
        return ("Durgun/Negatif", "red")


def format_benchmarks_for_llm(niche: str = "general", locale: str = "tr") -> str:
    """
    Format benchmark data for LLM prompt injection.
    Ensures LLM uses the same benchmark values as the UI.
    
    Args:
        niche: The niche for benchmarks
        locale: Language code ('tr' or 'en')
        
    Returns:
        Formatted string for LLM context
    """
    benchmarks = get_benchmarks_for_niche(niche)
    display_name = benchmarks.get(f"display_name_{locale}", benchmarks.get("display_name_en", niche))
    
    if locale == "tr":
        return f"""
=== {display_name} NİŞİ BENCHMARK DEĞERLERİ ===
• Etkileşim Oranı: Ortalama %{benchmarks['avg_engagement_rate']}, Üst %10: %{benchmarks['top_engagement_rate']}
• Büyüme Oranı: Ortalama %{benchmarks['avg_growth_rate']}/ay, Üst %10: %{benchmarks['top_growth_rate']}/ay
• Bot Skoru: Ortalama {benchmarks['avg_bot_score']}, Kabul Edilebilir: <{benchmarks['acceptable_bot_score']}
• Kaydetme Oranı: Ortalama %{benchmarks['avg_save_rate']}
• Takipçi/Takip Oranı: Ortalama {benchmarks['avg_follower_following_ratio']}x, Üst %10: {benchmarks['top_follower_following_ratio']}x
• Optimal Gönderi: Haftada {benchmarks['optimal_posts_per_week'][0]}-{benchmarks['optimal_posts_per_week'][1]} gönderi
• Reels Oranı: %{benchmarks['reels_percentage']}
=======================================
"""
    else:
        return f"""
=== {display_name} NICHE BENCHMARK VALUES ===
• Engagement Rate: Average {benchmarks['avg_engagement_rate']}%, Top 10%: {benchmarks['top_engagement_rate']}%
• Growth Rate: Average {benchmarks['avg_growth_rate']}%/month, Top 10%: {benchmarks['top_growth_rate']}%/month
• Bot Score: Average {benchmarks['avg_bot_score']}, Acceptable: <{benchmarks['acceptable_bot_score']}
• Save Rate: Average {benchmarks['avg_save_rate']}%
• Follower/Following Ratio: Average {benchmarks['avg_follower_following_ratio']}x, Top 10%: {benchmarks['top_follower_following_ratio']}x
• Optimal Posts: {benchmarks['optimal_posts_per_week'][0]}-{benchmarks['optimal_posts_per_week'][1]} posts/week
• Reels Percentage: {benchmarks['reels_percentage']}%
=======================================
"""


def get_all_benchmarks_for_api() -> Dict[str, Any]:
    """
    Get all benchmark data formatted for API response.
    Used to send consistent data to frontend.
    
    Returns:
        Dictionary with all niche benchmarks
    """
    return {
        "benchmarks": NICHE_BENCHMARKS,
        "default": "general",
        "version": "1.0"
    }
