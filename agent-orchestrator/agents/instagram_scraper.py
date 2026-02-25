# Instagram Data Acquisition Agent - PhD Level Implementation
# Orchestrates data collection from Instagram using authenticated login scraping and Apify
"""
Instagram Data Acquisition Agent - PhD Level

Bu ajan Instagram hesaplarından veri toplamayı orkestre eder.
İki ana mod destekler:
1. Full Access (Kendi Hesabım): Login scrape + Apify
2. Public Only (Rakip Analizi): Sadece Apify

Kaynak: Login Scrape (özel veriler) + Apify (herkese açık veriler)
"""

import asyncio
import logging
import os
import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

import httpx

logger = logging.getLogger(__name__)


# =========================
# ENUMS & TYPE DEFINITIONS
# =========================

class AnalysisMode(Enum):
    """Analysis mode types"""
    FULL_ACCESS = "full_access"
    PUBLIC_ONLY = "public_only"


class DataSource(Enum):
    """Data source types"""
    APIFY = "apify"
    LOGIN_SCRAPE = "login_scrape"


class AcquisitionError(Enum):
    """Error types for data acquisition"""
    # Auth errors
    AUTH_FAILED = "Login failed - check credentials"
    TWO_FA_REQUIRED = "2FA code needed"
    TWO_FA_INVALID = "Invalid 2FA code"
    SESSION_EXPIRED = "Session expired"
    
    # Scrape errors
    ACCOUNT_PRIVATE = "Target account is private"
    ACCOUNT_NOT_FOUND = "Account does not exist"
    RATE_LIMITED = "Rate limited - retry later"
    APIFY_FAILED = "Apify scrape failed"
    
    # Data errors
    NO_BUSINESS_ACCOUNT = "Not a business/creator account - no insights"
    INSUFFICIENT_DATA = "Not enough posts to analyze"


# =========================
# DATA STRUCTURES
# =========================

@dataclass
class AnalysisRequest:
    """Analysis request structure"""
    analysis_type: str  # "own_account" | "competitor"
    own_account: Optional[Dict[str, Any]] = None
    competitor: Optional[Dict[str, Any]] = None


@dataclass
class DailyMetric:
    """Daily metric data point"""
    date: str
    value: int


@dataclass
class Location:
    """Location data"""
    name: str
    percentage: float


@dataclass
class AgeGroup:
    """Age group demographic"""
    range: str
    percentage: float


@dataclass
class ActivityHour:
    """Activity hour data"""
    hour: int
    day: str
    activity_level: float


@dataclass
class ProfileData:
    """Public profile data"""
    username: str
    full_name: str
    bio: str
    follower_count: int
    following_count: int
    post_count: int
    is_verified: bool
    is_business: bool
    profile_pic_url: str
    external_url: Optional[str] = None


@dataclass
class PostData:
    """Post data structure"""
    post_id: str
    shortcode: str
    type: str  # "image" | "video" | "carousel" | "reel"
    caption: str
    hashtags: List[str]
    mentions: List[str]
    likes: int
    comments: int
    timestamp: str
    url: str
    media_urls: List[str]
    # Optional private metrics
    reach: Optional[int] = None
    impressions: Optional[int] = None
    saves: Optional[int] = None
    shares: Optional[int] = None
    discovery: Optional[Dict[str, Any]] = None


@dataclass
class StoryData:
    """Story insight data (private)"""
    story_id: str
    views: int
    replies: int
    shares: int
    link_clicks: int
    navigation: Dict[str, int] = field(default_factory=dict)


@dataclass
class AudienceData:
    """Audience demographic data (private)"""
    total_followers: int
    gender: Dict[str, float]
    age_groups: List[AgeGroup]
    top_cities: List[Location]
    top_countries: List[Location]
    active_hours: List[ActivityHour]


@dataclass
class InsightsTimeline:
    """Insights timeline data (private)"""
    reach: List[DailyMetric]
    impressions: List[DailyMetric]
    profile_visits: List[DailyMetric]
    website_clicks: List[DailyMetric]
    engagement: List[DailyMetric]


@dataclass
class EstimatedMetrics:
    """Estimated metrics for competitor analysis"""
    estimated_engagement_rate: float
    estimated_reach_per_post: float
    estimated_saves_per_post: float
    estimated_shares_per_post: float
    confidence: str  # "low" | "medium" | "high"
    disclaimer: str


@dataclass
class AcquisitionMetadata:
    """Metadata for acquisition response"""
    sources_used: List[str]
    data_coverage: str  # "100%" | "30%"
    scrape_timestamp: str
    data_freshness: Dict[str, Optional[str]]


@dataclass
class DataLimitations:
    """Limitations in data acquisition"""
    unavailable_metrics: List[str]
    reason: str


# =========================
# CONFIGURATION
# =========================

class AntiDetectionConfig:
    """Anti-detection configuration for login scraping"""
    
    def __init__(self):
        self.browser = "puppeteer-extra + stealth"
        self.webdriver = False
        self.fingerprint = "randomized"
        self.user_agent_pool = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]
        self.delays = {
            "click": (100, 300),  # ms
            "type": (50, 200),  # ms
            "navigate": (2000, 4000),  # ms
            "between_actions": (1000, 3000),  # ms
        }
        self.rate_limits = {
            "requests_per_minute": 20,
            "session_cooldown_hours": 4,
        }
    
    def get_random_user_agent(self) -> str:
        """Get a random user agent from pool"""
        return random.choice(self.user_agent_pool)
    
    def get_random_delay(self, action: str) -> float:
        """Get random delay for an action in seconds"""
        min_ms, max_ms = self.delays.get(action, (500, 1000))
        return random.randint(min_ms, max_ms) / 1000


class ApifyConfig:
    """Apify scraper configuration"""
    
    def __init__(self):
        self.actor = "apify/instagram-scraper"
        self.api_token = os.getenv("APIFY_API_TOKEN", "")
        self.api_base_url = "https://api.apify.com/v2"
        
        # ============================================================
        # OPERATION SIGHT RESTORATION - KRİTİK KONFİGÜRASYON
        # resultsType MUTLAKA 'posts' olmalı yoksa sadece profil çeker!
        # resultsLimit en az 20 olmalı doğru engagement hesabı için
        # ============================================================
        self.default_input = {
            "resultsType": "posts",   # KRİTİK: 'details' değil 'posts' olmalı!
            "resultsLimit": 30,       # KRİTİK: En az 20-30 post çek
            "searchType": "user",
            "searchLimit": 1,         # YENİ: Sadece 1 hesap ara (doğru hesabı bul)
            "addParentData": True,    # Profil bilgisini postlarla birlikte getir
            "commentsCount": 10,      # YENİ: Her post için en fazla 10 yorum çek (sentiment için)
            "extendOutputFunction": """async ({ data, item, page, request, customData }) => {
                return {
                    ...item,
                    likesCount: item.likesCount || 0,
                    commentsCount: item.commentsCount || 0,
                    timestamp: item.timestamp,
                    type: item.type,
                    __typename: item.__typename || '',
                    product_type: item.productType || item.product_type || ''
                };
            }""",
        }
        
        # Competitor benchmarking configuration
        self.competitor_config = {
            "resultsType": "posts",   # KRİTİK: Rakipler için de 'posts' şart!
            "resultsLimit": 20,       # Rakip için de yeterli post (12 yetersiz!)
            "searchType": "user",
            "searchLimit": 1,         # YENİ: Sadece 1 hesap
            "addParentData": True,
        }


class RateLimits:
    """Rate limiting configuration"""
    
    def __init__(self):
        self.login_scrape = {
            "requests_per_minute": 20,
            "sessions_per_day": 3,
            "cooldown_hours": 4,
        }
        self.apify = {
            "requests_per_minute": 60,
            "daily_limit": 1000,
        }


class CompetitorConfig:
    """Configuration for competitor benchmarking"""
    
    def __init__(self):
        # Default competitors for spiritual/healing niche
        # These can be overridden via environment variable or API
        self.default_competitors = {
            "spiritual_healing": [
                "spiritfairy",  # Spiritual content creator
                "thegoodtrade",  # Wellness/mindful living
                "mindbodygreen",  # Health & wellness
            ],
            "fitness": [
                "kaikialafit",
                "blogilates",
                "whitneyysimmons",
            ],
            "business": [
                "garyvee",
                "foundr",
                "entrepreneur",
            ],
        }
        
        # Load custom competitors from env
        custom = os.getenv("TARGET_COMPETITORS", "")
        self.custom_competitors = [c.strip() for c in custom.split(",") if c.strip()]
    
    def get_competitors_for_niche(self, niche: str) -> list:
        """Get competitor list for a specific niche"""
        if self.custom_competitors:
            return self.custom_competitors
        
        # Normalize niche name
        niche_lower = niche.lower().replace(" ", "_")
        
        # Map similar niches
        niche_mapping = {
            "spirituel": "spiritual_healing",
            "spiritüel": "spiritual_healing",
            "ruhsal": "spiritual_healing",
            "healing": "spiritual_healing",
            "bioenerji": "spiritual_healing",
            "meditasyon": "spiritual_healing",
            "wellness": "spiritual_healing",
            "fitness": "fitness",
            "spor": "fitness",
            "business": "business",
            "iş": "business",
        }
        
        mapped_niche = niche_mapping.get(niche_lower, "spiritual_healing")
        return self.default_competitors.get(mapped_niche, self.default_competitors["spiritual_healing"])


def calculate_engagement_metrics(posts_list: list, follower_count: int = 1) -> dict:
    """
    Calculate engagement metrics from posts list.
    
    OPERATION SIGHT RESTORATION - GÜVENLİ MATEMATİK
    
    Bu AUTHORITATIVE fonksiyon engagement hesaplama için.
    Tüm ajanlar bu fonksiyonun döndürdüğü metrikleri kullanmalı.
    
    KRİTİK DEĞİŞİKLİK:
    - Veri yoksa 0 DEĞİL, None döndürür
    - None = "veri yok/çekilemedi"
    - 0 = "gerçekten sıfır etkileşim"
    - Ajanlar bu farkı anlayabilmeli!
    
    Args:
        posts_list: List of post dictionaries with likesCount/commentsCount
        follower_count: Total follower count for rate calculation
    
    Returns:
        Dictionary with calculated engagement metrics (None-safe)
    """
    # Handle edge cases - VERİ YOK durumu
    if not posts_list or not isinstance(posts_list, list):
        logger.warning("⚠️ HAYALET VERİ: Empty or invalid posts_list, returning NULL metrics (not zero!)")
        return {
            "avg_likes": None,        # None = veri yok, 0 değil!
            "avg_comments": None,     # None = veri yok, 0 değil!
            "engagement_rate": None,  # None = veri yok, 0 değil!
            "total_posts_analyzed": 0,
            "data_quality": "no_data",
            "data_fetch_error": True,
            "warning": "NO_POSTS_SCRAPED: Post listesi boş - API çekemedi veya hesap gizli olabilir"
        }
    
    # Filter valid posts (last 12 for accurate recent engagement)
    valid_posts = [
        p for p in posts_list[:12] 
        if isinstance(p, dict) and (p.get("likes", 0) > 0 or p.get("likesCount", 0) > 0)
    ]
    
    if not valid_posts:
        # Try with all posts if recent 12 have no data
        valid_posts = [
            p for p in posts_list 
            if isinstance(p, dict) and (p.get("likes", 0) > 0 or p.get("likesCount", 0) > 0)
        ]
    
    if not valid_posts:
        # Post var ama hepsinde 0 engagement - bu HAYALET VERİ durumu!
        logger.warning(f"⚠️ HAYALET VERİ: {len(posts_list)} post var ama hepsinde 0 engagement!")
        logger.warning("   Bu muhtemelen API kısıtlaması - likes/comments çekilemedi")
        return {
            "avg_likes": None,        # None = veri çekilemedi
            "avg_comments": None,     # None = veri çekilemedi
            "engagement_rate": None,  # None = veri çekilemedi
            "total_posts_analyzed": len(posts_list),
            "data_quality": "zero_engagement",
            "data_fetch_error": True,
            "warning": "SCRAPER_BLOCKED: Postlar bulundu ancak engagement verileri çekilemedi - muhtemel API kısıtlaması veya cookie gerekli"
        }
    
    # Calculate averages (support both field naming conventions)
    total_likes = sum(
        p.get("likes", 0) or p.get("likesCount", 0) or 0 
        for p in valid_posts
    )
    total_comments = sum(
        p.get("comments", 0) or p.get("commentsCount", 0) or 0 
        for p in valid_posts
    )
    
    post_count = len(valid_posts)
    avg_likes = total_likes / post_count if post_count > 0 else 0
    avg_comments = total_comments / post_count if post_count > 0 else 0
    
    # Calculate engagement rate
    follower_count = max(1, follower_count)  # Prevent division by zero
    engagement_rate = ((avg_likes + avg_comments) / follower_count) * 100
    
    # Determine data quality
    data_quality = "high" if post_count >= 10 else "medium" if post_count >= 5 else "low"
    
    return {
        "avg_likes": round(avg_likes, 2),
        "avg_comments": round(avg_comments, 2),
        "engagement_rate": round(engagement_rate, 4),
        "total_posts_analyzed": post_count,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "data_quality": data_quality,
        "posts_with_data": post_count,
        "posts_without_data": len(posts_list) - post_count,
    }


# =========================
# APIFY CLIENT
# =========================

class ApifyClient:
    """Client for Apify Instagram scraper"""
    
    def __init__(self):
        self.config = ApifyConfig()
        self.http_client = httpx.AsyncClient(timeout=120.0)
    
    async def scrape_profile(self, username: str) -> Dict[str, Any]:
        """Scrape public profile data using Apify"""
        logger.info(f"Starting Apify scrape for @{username}")
        
        if not self.config.api_token:
            logger.warning("APIFY_API_TOKEN not configured, using mock data")
            return await self._get_mock_data(username)
        
        try:
            # Start actor run
            run_url = f"{self.config.api_base_url}/acts/{self.config.actor}/runs"
            
            input_data = {
                **self.config.default_input,
                "directUrls": [f"https://www.instagram.com/{username}/"],
            }
            
            headers = {
                "Authorization": f"Bearer {self.config.api_token}",
                "Content-Type": "application/json",
            }
            
            response = await self.http_client.post(
                run_url,
                json=input_data,
                headers=headers,
            )
            
            if response.status_code != 201:
                logger.error(f"Apify run failed: {response.text}")
                raise Exception(f"Apify run failed: {response.status_code}")
            
            run_data = response.json()
            run_id = run_data.get("data", {}).get("id")
            
            # Wait for run to complete
            result = await self._wait_for_run(run_id)
            
            return self._parse_apify_result(result)
            
        except Exception as e:
            logger.error(f"Apify scrape error: {e}")
            # Fallback to mock data for development
            return await self._get_mock_data(username)
    
    async def _wait_for_run(self, run_id: str, max_wait: int = 120) -> Dict[str, Any]:
        """Wait for Apify run to complete"""
        status_url = f"{self.config.api_base_url}/actor-runs/{run_id}"
        headers = {"Authorization": f"Bearer {self.config.api_token}"}
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            response = await self.http_client.get(status_url, headers=headers)
            data = response.json().get("data", {})
            
            status = data.get("status")
            
            if status == "SUCCEEDED":
                # Get dataset items
                dataset_id = data.get("defaultDatasetId")
                return await self._get_dataset_items(dataset_id)
            
            elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                raise Exception(f"Apify run {status}: {data.get('statusMessage', 'Unknown error')}")
            
            await asyncio.sleep(5)
        
        raise Exception("Apify run timed out")
    
    async def _get_dataset_items(self, dataset_id: str) -> Dict[str, Any]:
        """Get items from Apify dataset"""
        url = f"{self.config.api_base_url}/datasets/{dataset_id}/items"
        headers = {"Authorization": f"Bearer {self.config.api_token}"}
        
        response = await self.http_client.get(url, headers=headers)
        return response.json()
    
    def _parse_apify_result(self, result: Any) -> Dict[str, Any]:
        """Parse Apify result into our format with proper engagement calculation"""
        profile = {}
        posts = []
        
        # Handle different Apify result formats
        if isinstance(result, list):
            for item in result:
                if not isinstance(item, dict):
                    continue
                
                # Check if this is a profile or post based on available fields
                if item.get("followersCount") or item.get("postsCount"):
                    # This is profile data
                    profile = item
                elif item.get("likesCount") is not None or item.get("commentsCount") is not None:
                    # This is post data
                    posts.append(item)
                elif item.get("shortCode") or item.get("id"):
                    # Also post data (different structure)
                    posts.append(item)
        elif isinstance(result, dict):
            profile = result
            posts = result.get("latestPosts", []) or result.get("posts", [])
        
        logger.info(f"Parsed Apify result: profile={bool(profile)}, posts={len(posts)}")
        
        # Parse posts with engagement data
        parsed_posts = []
        for p in posts:
            likes = p.get("likesCount", 0) or p.get("likes", 0) or 0
            comments = p.get("commentsCount", 0) or p.get("comments", 0) or 0
            
            # ── Post Type Inference (Action Plan #1) ──────────────────────────
            # Priority 1: __typename field (most reliable from GraphQL)
            # Priority 2: product_type / productType
            # Priority 3: type field
            # Priority 4: Fallback signals (videoUrl, videoViewCount)
            typename    = p.get("__typename", "") or ""
            product_type_raw = (p.get("productType") or p.get("product_type") or "").lower()
            type_field  = (p.get("type") or "").lower()

            if product_type_raw in ("clips",) or typename == "GraphVideo" and product_type_raw in ("clips", "feed_clip", "reel", "reels"):
                post_type = "reel"
            elif typename == "GraphVideo" and product_type_raw not in ("clips", "feed_clip"):
                # Plain video (IGTV etc.) — treat as reel only if product_type says so
                is_clips = product_type_raw in ("clips", "reel", "reels", "feed_clip")
                post_type = "reel" if is_clips else "video"
            elif typename == "GraphSidecar" or type_field in ("carousel", "sidecar", "carousel_container"):
                post_type = "carousel"
            elif typename == "GraphImage" or type_field in ("image", "photo", "graphimage"):
                post_type = "image"
            elif type_field in ("clips", "reel", "reels", "feed_clip"):
                post_type = "reel"
            elif type_field in ("video", "igtv"):
                is_clips = product_type_raw in ("clips", "reel", "reels")
                post_type = "reel" if is_clips else "video"
            else:
                # Fallback: infer from available signals
                has_video = bool(p.get("videoUrl") or p.get("videoViewCount") or p.get("videoPlayCount") or p.get("playCount"))
                if has_video:
                    is_clips = product_type_raw in ("clips", "reel", "reels", "feed_clip")
                    post_type = "reel" if is_clips else "video"
                else:
                    post_type = "image"
            
            # ── Extract comment texts (Action Plan #2) ─────────────────────
            raw_comments = p.get("latestComments") or p.get("comments_data") or p.get("topComments") or []
            latest_comments: List[str] = []
            if isinstance(raw_comments, list):
                for c in raw_comments:
                    if isinstance(c, dict):
                        text = c.get("text") or c.get("comment") or c.get("content") or ""
                        if text:
                            latest_comments.append(str(text).strip())
                    elif isinstance(c, str) and c.strip():
                        latest_comments.append(c.strip())

            parsed_posts.append({
                "post_id": p.get("id", "") or p.get("pk", ""),
                "shortcode": p.get("shortCode", "") or p.get("code", ""),
                "type": post_type,
                "caption": p.get("caption", "") or "",
                "hashtags": self._extract_hashtags(p.get("caption", "") or ""),
                "mentions": self._extract_mentions(p.get("caption", "") or ""),
                "likes": likes,
                "likesCount": likes,
                "comments": comments,
                "commentsCount": comments,
                "latest_comments": latest_comments,  # Sentiment engine için yorum metinleri
                "timestamp": p.get("timestamp", "") or p.get("takenAt", ""),
                "url": p.get("url", "") or f"https://instagram.com/p/{p.get('shortCode', '')}",
                "media_urls": p.get("displayUrl", []) if isinstance(p.get("displayUrl"), list) else [p.get("displayUrl", "")],
                "video_views": p.get("videoViewCount", 0) or p.get("videoPlayCount", 0) or p.get("playCount", 0),
            })
        
        # Log content type distribution for debugging
        type_counts = {}
        for post in parsed_posts:
            t = post.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
        logger.info(f"📊 Content type distribution: {type_counts}")
        
        # Calculate engagement metrics from posts
        follower_count = profile.get("followersCount", 0) or profile.get("followers", 0) or 1
        engagement_metrics = calculate_engagement_metrics(parsed_posts, follower_count)
        
        logger.info(f"Calculated engagement: avg_likes={engagement_metrics['avg_likes']}, "
                    f"avg_comments={engagement_metrics['avg_comments']}, "
                    f"engagement_rate={engagement_metrics['engagement_rate']}%")
        
        return {
            "profile": {
                "username": profile.get("username", ""),
                "full_name": profile.get("fullName", "") or profile.get("full_name", ""),
                "bio": profile.get("biography", "") or profile.get("bio", ""),
                "follower_count": follower_count,
                "following_count": profile.get("followsCount", 0) or profile.get("following", 0),
                "post_count": profile.get("postsCount", 0) or profile.get("posts", 0),
                "is_verified": profile.get("verified", False) or profile.get("is_verified", False),
                "is_business": profile.get("isBusinessAccount", False) or profile.get("is_business", False),
                "profile_pic_url": profile.get("profilePicUrl", "") or profile.get("profile_pic_url", ""),
                "external_url": profile.get("externalUrl") or profile.get("external_url"),
                # CRITICAL: Add calculated engagement metrics to profile
                "avg_likes": engagement_metrics["avg_likes"],
                "avg_comments": engagement_metrics["avg_comments"],
                "engagement_rate": engagement_metrics["engagement_rate"],
            },
            "posts": parsed_posts,
            "engagement_metrics": engagement_metrics,
        }
    
    def _extract_hashtags(self, caption: str) -> List[str]:
        """Extract hashtags from caption"""
        import re
        return re.findall(r'#(\w+)', caption)
    
    def _extract_mentions(self, caption: str) -> List[str]:
        """Extract mentions from caption"""
        import re
        return re.findall(r'@(\w+)', caption)
    
    async def _get_mock_data(self, username: str) -> Dict[str, Any]:
        """Get mock data for development/testing"""
        logger.info(f"Using mock data for @{username}")
        
        return {
            "profile": {
                "username": username,
                "full_name": f"{username.title()} User",
                "bio": "📍 Location | 🎯 Niche content creator | 💼 DM for collabs",
                "follower_count": random.randint(5000, 50000),
                "following_count": random.randint(200, 2000),
                "post_count": random.randint(50, 500),
                "is_verified": random.random() > 0.9,
                "is_business": random.random() > 0.3,
                "profile_pic_url": f"https://instagram.com/{username}/profile_pic",
                "external_url": f"https://linktr.ee/{username}",
            },
            "posts": [
                {
                    "post_id": f"post_{i}",
                    "shortcode": f"ABC{i}xyz",
                    "type": random.choice(["image", "video", "carousel", "reel"]),
                    "caption": f"Post #{i} caption with #hashtag1 #hashtag2 @mention1",
                    "hashtags": ["hashtag1", "hashtag2", "trending"],
                    "mentions": ["mention1", "brand"],
                    "likes": random.randint(100, 5000),
                    "comments": random.randint(5, 200),
                    "timestamp": datetime.now().isoformat(),
                    "url": f"https://instagram.com/p/ABC{i}xyz",
                    "media_urls": [f"https://instagram.com/media/{i}.jpg"],
                }
                for i in range(30)
            ],
        }
    
    async def close(self):
        """Close HTTP client"""
        await self.http_client.aclose()


# =========================
# LOGIN SCRAPER (PLACEHOLDER)
# =========================

class LoginScraper:
    """
    Login scraper for private Instagram data.
    
    NOTE: This is a placeholder implementation.
    Real implementation would use Puppeteer/Playwright with stealth plugins.
    """
    
    def __init__(self):
        self.anti_detection = AntiDetectionConfig()
        self.session = None
    
    async def authenticate(
        self,
        username: str,
        password: str,
        two_fa_code: Optional[str] = None
    ) -> bool:
        """
        Authenticate with Instagram.
        
        In production, this would:
        1. Launch headless browser with stealth
        2. Navigate to Instagram login
        3. Enter credentials with human-like delays
        4. Handle 2FA if required
        5. Save session for reuse
        """
        logger.info(f"Login authentication requested for @{username}")
        
        # Placeholder - in production would actually authenticate
        # For now, simulate authentication delay
        await asyncio.sleep(random.uniform(2, 4))
        
        # Simulate occasional 2FA requirement
        if two_fa_code is None and random.random() > 0.8:
            raise Exception(AcquisitionError.TWO_FA_REQUIRED.value)
        
        return True
    
    async def scrape_private_insights(self, username: str) -> Dict[str, Any]:
        """
        Scrape private Instagram insights (requires business account).
        
        In production, this would navigate through Instagram UI to:
        - Professional Dashboard
        - Insights > Overview
        - Audience demographics
        - Content insights
        """
        logger.info(f"Scraping private insights for @{username}")
        
        # Simulate scraping delay
        await asyncio.sleep(random.uniform(3, 6))
        
        # Return mock private data
        return {
            "insights": {
                "reach": [{"date": f"2024-01-{i:02d}", "value": random.randint(1000, 10000)} for i in range(1, 31)],
                "impressions": [{"date": f"2024-01-{i:02d}", "value": random.randint(2000, 20000)} for i in range(1, 31)],
                "profile_visits": [{"date": f"2024-01-{i:02d}", "value": random.randint(50, 500)} for i in range(1, 31)],
                "website_clicks": [{"date": f"2024-01-{i:02d}", "value": random.randint(10, 100)} for i in range(1, 31)],
                "engagement": [{"date": f"2024-01-{i:02d}", "value": random.randint(100, 1000)} for i in range(1, 31)],
            },
            "audience": {
                "total_followers": random.randint(5000, 50000),
                "gender": {"male": 0.45, "female": 0.52, "other": 0.03},
                "age_groups": [
                    {"range": "13-17", "percentage": 0.05},
                    {"range": "18-24", "percentage": 0.25},
                    {"range": "25-34", "percentage": 0.35},
                    {"range": "35-44", "percentage": 0.20},
                    {"range": "45-54", "percentage": 0.10},
                    {"range": "55+", "percentage": 0.05},
                ],
                "top_cities": [
                    {"name": "Istanbul", "percentage": 0.25},
                    {"name": "Ankara", "percentage": 0.15},
                    {"name": "Izmir", "percentage": 0.10},
                    {"name": "Bursa", "percentage": 0.08},
                    {"name": "Antalya", "percentage": 0.07},
                ],
                "top_countries": [
                    {"name": "Turkey", "percentage": 0.75},
                    {"name": "Germany", "percentage": 0.08},
                    {"name": "USA", "percentage": 0.05},
                    {"name": "UK", "percentage": 0.04},
                    {"name": "Netherlands", "percentage": 0.03},
                ],
                "active_hours": [
                    {"hour": h, "day": d, "activity_level": random.random()}
                    for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                    for h in range(24)
                ],
            },
            "content_insights": [
                {
                    "post_id": f"post_{i}",
                    "reach": random.randint(1000, 10000),
                    "impressions": random.randint(2000, 20000),
                    "saves": random.randint(10, 500),
                    "shares": random.randint(5, 200),
                    "follows_from_post": random.randint(0, 50),
                    "discovery": {
                        "home": 0.45,
                        "profile": 0.20,
                        "explore": 0.15,
                        "hashtags": 0.10,
                        "other": 0.10,
                    },
                }
                for i in range(30)
            ],
            "story_insights": [
                {
                    "story_id": f"story_{i}",
                    "views": random.randint(500, 5000),
                    "replies": random.randint(0, 50),
                    "shares": random.randint(0, 30),
                    "link_clicks": random.randint(0, 100),
                    "navigation": {
                        "forward": random.randint(100, 1000),
                        "back": random.randint(10, 100),
                        "exit": random.randint(50, 500),
                    },
                }
                for i in range(7)
            ],
        }
    
    async def close(self):
        """Close browser session"""
        if self.session:
            # Close browser session
            pass


# =========================
# INSTAGRAM DATA ACQUISITION AGENT
# =========================

class InstagramDataAcquisitionAgent:
    """
    Instagram Data Acquisition Agent - PhD Level
    
    Orchestrates data collection from Instagram using:
    - Login scraping (for own account private data)
    - Apify public scraping (for any account)
    
    Modes:
    - Full Access: Own account with credentials - 100% data coverage
    - Public Only: Competitor analysis - 30% data coverage (estimated)
    """
    
    def __init__(self):
        self.name = "Instagram Data Acquisition"
        self.role = "Data Collection Orchestrator"
        self.apify_client = ApifyClient()
        self.login_scraper = LoginScraper()
        self.rate_limits = RateLimits()
    
    def determine_mode(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Determine analysis mode based on request"""
        analysis_type = request.get("analysis_type", "competitor")
        
        if analysis_type == "competitor":
            return {
                "mode": AnalysisMode.PUBLIC_ONLY,
                "sources": [DataSource.APIFY],
                "target": request.get("competitor", {}).get("username", ""),
            }
        
        own_account = request.get("own_account", {})
        if own_account.get("fetch_private") and own_account.get("password"):
            return {
                "mode": AnalysisMode.FULL_ACCESS,
                "sources": [DataSource.APIFY, DataSource.LOGIN_SCRAPE],
                "target": own_account.get("username", ""),
            }
        
        return {
            "mode": AnalysisMode.PUBLIC_ONLY,
            "sources": [DataSource.APIFY],
            "target": own_account.get("username", ""),
        }
    
    async def acquire_data(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for data acquisition.
        
        Args:
            request: Analysis request with type and credentials
            
        Returns:
            Unified dataset with metadata
        """
        start_time = time.time()
        mode_info = self.determine_mode(request)
        
        # Extract niche for competitor benchmarking
        niche = request.get("niche", "general")
        if not niche:
            niche = "general"
        
        logger.info(f"Starting data acquisition in {mode_info['mode'].value} mode for @{mode_info['target']} (niche: {niche})")
        
        try:
            if mode_info["mode"] == AnalysisMode.FULL_ACCESS:
                result = await self._acquire_full_access(request)
            else:
                result = await self._acquire_public_only(mode_info["target"], niche)
            
            duration = time.time() - start_time
            logger.info(f"Data acquisition completed in {duration:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Data acquisition failed: {e}")
            return await self._handle_acquisition_error(e, mode_info)
    
    async def _acquire_full_access(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Acquire data with full access (login scrape + Apify).
        
        Runs both scrapers in parallel for efficiency.
        """
        own_account = request.get("own_account", {})
        username = own_account.get("username", "")
        password = own_account.get("password", "")
        two_fa_code = own_account.get("two_fa_code")
        
        try:
            # Authenticate first
            await self.login_scraper.authenticate(username, password, two_fa_code)
            
            # Run both scrapers in parallel
            private_task = asyncio.create_task(
                self.login_scraper.scrape_private_insights(username)
            )
            public_task = asyncio.create_task(
                self.apify_client.scrape_profile(username)
            )
            
            private_data, public_data = await asyncio.gather(
                private_task,
                public_task,
                return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(private_data, Exception):
                logger.error(f"Private scrape failed: {private_data}")
                private_data = None
            
            if isinstance(public_data, Exception):
                logger.error(f"Public scrape failed: {public_data}")
                public_data = None
            
            if public_data is None and private_data is None:
                raise Exception("Both scrapers failed")
            
            # Merge data
            merged = self._merge_data(private_data, public_data)
            
            return {
                "success": True,
                "job_id": f"acq_{int(time.time())}",
                "mode": AnalysisMode.FULL_ACCESS.value,
                "target_account": username,
                "data": merged,
                "metadata": {
                    "sources_used": ["apify", "login_scrape"],
                    "data_coverage": "100%",
                    "scrape_timestamp": datetime.utcnow().isoformat(),
                    "data_freshness": {
                        "private": datetime.utcnow().isoformat(),
                        "public": datetime.utcnow().isoformat(),
                    },
                },
            }
            
        except Exception as e:
            # Fallback to public only
            logger.warning(f"Full access failed, falling back to public only: {e}")
            return await self._acquire_public_only_with_limitations(username, str(e))
    
    async def _acquire_public_only(self, username: str, niche: str = "general") -> Dict[str, Any]:
        """Acquire public data only using Apify with engagement metrics and competitor data"""
        public_data = await self.apify_client.scrape_profile(username)
        
        # Add estimated metrics
        estimated = self._estimate_private_metrics(public_data)
        
        # Get engagement metrics from public_data (already calculated in scrape_profile)
        engagement_metrics = public_data.get("engagement_metrics", {})
        
        # Scrape competitor data for benchmarking
        competitor_data = await self.scrape_competitors(niche)
        
        # Calculate gap analysis
        user_engagement_data = {
            "engagement_rate": engagement_metrics.get("engagement_rate", 0),
            "avg_likes": engagement_metrics.get("avg_likes", 0),
            "avg_comments": engagement_metrics.get("avg_comments", 0),
        }
        gap_analysis = self.calculate_competitor_gap(user_engagement_data, competitor_data)
        
        return {
            "success": True,
            "job_id": f"acq_{int(time.time())}",
            "mode": AnalysisMode.PUBLIC_ONLY.value,
            "target_account": username,
            "data": {
                "profile": public_data.get("profile", {}),
                "posts": public_data.get("posts", []),
                "estimated": estimated,
                "engagement_metrics": engagement_metrics,
                "competitor_benchmarks": competitor_data,
                "gap_analysis": gap_analysis,
            },
            "metadata": {
                "sources_used": ["apify"],
                "data_coverage": "60%" if competitor_data.get("comparison_ready") else "30%",
                "scrape_timestamp": datetime.utcnow().isoformat(),
                "data_freshness": {
                    "private": None,
                    "public": datetime.utcnow().isoformat(),
                },
                "competitors_analyzed": len(competitor_data.get("competitors", [])),
            },
            "limitations": {
                "unavailable_metrics": [
                    "reach", "impressions", "demographics", "saves",
                    "shares", "profile_visits", "follower_growth",
                    "story_insights", "website_clicks", "discovery_sources"
                ],
                "reason": "Public data only - competitor analysis mode",
            },
        }
    
    async def _acquire_public_only_with_limitations(
        self,
        username: str,
        error_reason: str
    ) -> Dict[str, Any]:
        """Acquire public data after full access failure"""
        result = await self._acquire_public_only(username)
        
        result["limitations"] = {
            "unavailable_metrics": [
                "reach", "impressions", "demographics", "saves",
                "shares", "profile_visits", "follower_growth",
                "story_insights", "website_clicks", "discovery_sources"
            ],
            "reason": f"Login scrape failed: {error_reason}",
        }
        
        return result
    
    def _merge_data(
        self,
        private_data: Optional[Dict[str, Any]],
        public_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Merge private and public data into unified dataset"""
        merged = {
            "profile": {},
            "posts": [],
            "stories": [],
            "audience": None,
            "insights_timeline": None,
        }
        
        # Merge profile
        if public_data:
            merged["profile"] = public_data.get("profile", {})
        
        if private_data:
            # Add private metrics to profile
            insights = private_data.get("insights", {})
            merged["profile"]["total_reach_30d"] = sum(
                m.get("value", 0) for m in insights.get("reach", [])
            )
            merged["profile"]["total_impressions_30d"] = sum(
                m.get("value", 0) for m in insights.get("impressions", [])
            )
            merged["profile"]["demographics"] = private_data.get("audience")
        
        # Merge posts
        if public_data:
            posts = public_data.get("posts", [])
            content_insights = {}
            
            if private_data:
                for insight in private_data.get("content_insights", []):
                    content_insights[insight.get("post_id")] = insight
            
            merged["posts"] = []
            for post in posts:
                post_id = post.get("post_id")
                private_insight = content_insights.get(post_id, {})
                
                merged["posts"].append({
                    **post,
                    "reach": private_insight.get("reach"),
                    "impressions": private_insight.get("impressions"),
                    "saves": private_insight.get("saves"),
                    "shares": private_insight.get("shares") or post.get("shares"),
                    "discovery": private_insight.get("discovery"),
                })
        
        # Add private-only data
        if private_data:
            merged["stories"] = private_data.get("story_insights", [])
            merged["audience"] = private_data.get("audience")
            merged["insights_timeline"] = private_data.get("insights")
        
        return merged
    
    def _estimate_private_metrics(self, public_data: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate private metrics from public data using calculated engagement"""
        posts = public_data.get("posts", [])
        profile = public_data.get("profile", {})
        engagement_metrics = public_data.get("engagement_metrics", {})
        
        # Use pre-calculated metrics if available
        if engagement_metrics:
            avg_likes = engagement_metrics.get("avg_likes", 0)
            avg_comments = engagement_metrics.get("avg_comments", 0)
            engagement_rate = engagement_metrics.get("engagement_rate", 0)
            data_quality = engagement_metrics.get("data_quality", "low")
        else:
            # Fallback to manual calculation
            metrics = calculate_engagement_metrics(posts, profile.get("follower_count", 1))
            avg_likes = metrics["avg_likes"]
            avg_comments = metrics["avg_comments"]
            engagement_rate = metrics["engagement_rate"]
            data_quality = metrics["data_quality"]
        
        followers = profile.get("follower_count", 1) or 1
        
        return {
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
            "estimated_engagement_rate": round(engagement_rate, 4),
            "estimated_reach_per_post": round(followers * 0.3, 0),  # ~30% typical reach
            "estimated_saves_per_post": round(avg_likes * 0.05, 0),  # ~5% of likes
            "estimated_shares_per_post": round(avg_likes * 0.02, 0),  # ~2% of likes
            "data_quality": data_quality,
            "confidence": "high" if data_quality == "high" else "medium" if data_quality == "medium" else "low",
            "disclaimer": "Engagement metrics calculated from post data" if data_quality != "no_data" else "No posts available for estimation",
        }
    
    async def scrape_competitors(self, niche: str, custom_competitors: list = None) -> Dict[str, Any]:
        """
        Scrape competitor data for benchmarking.
        
        Args:
            niche: The account's niche for competitor selection
            custom_competitors: Optional list of specific competitor usernames
        
        Returns:
            Dictionary with competitor benchmarks
        """
        competitor_config = CompetitorConfig()
        
        # Get competitor list
        if custom_competitors and len(custom_competitors) > 0:
            competitors = custom_competitors
        else:
            competitors = competitor_config.get_competitors_for_niche(niche)
        
        logger.info(f"Scraping {len(competitors)} competitors for {niche} niche: {competitors}")
        
        benchmarking_data = {
            "competitors": [],
            "aggregate": {
                "avg_followers": 0,
                "avg_engagement_rate": 0,
                "avg_likes": 0,
                "avg_comments": 0,
            },
            "comparison_ready": False,
        }
        
        # Scrape each competitor
        competitor_results = []
        for username in competitors:
            try:
                logger.info(f"Scraping competitor: @{username}")
                data = await self.apify_client.scrape_profile(username)
                
                profile = data.get("profile", {})
                engagement = data.get("engagement_metrics", {})
                
                competitor_results.append({
                    "username": username,
                    "followers": profile.get("follower_count", 0),
                    "following": profile.get("following_count", 0),
                    "posts": profile.get("post_count", 0),
                    "is_verified": profile.get("is_verified", False),
                    "avg_likes": engagement.get("avg_likes", 0),
                    "avg_comments": engagement.get("avg_comments", 0),
                    "engagement_rate": engagement.get("engagement_rate", 0),
                    "data_quality": engagement.get("data_quality", "unknown"),
                })
                
                # Small delay between requests
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.warning(f"Failed to scrape competitor @{username}: {e}")
                continue
        
        if competitor_results:
            benchmarking_data["competitors"] = competitor_results
            benchmarking_data["competitors_identified"] = len(competitor_results)
            
            # Calculate aggregates
            total_followers = sum(c["followers"] for c in competitor_results)
            total_engagement = sum(c["engagement_rate"] for c in competitor_results)
            total_likes = sum(c["avg_likes"] for c in competitor_results)
            total_comments = sum(c["avg_comments"] for c in competitor_results)
            count = len(competitor_results)
            
            benchmarking_data["aggregate"] = {
                "avg_followers": round(total_followers / count, 0),
                "avg_engagement_rate": round(total_engagement / count, 4),
                "avg_likes": round(total_likes / count, 2),
                "avg_comments": round(total_comments / count, 2),
            }
            benchmarking_data["comparison_ready"] = True
            
            logger.info(f"Competitor benchmarking complete: {count} competitors analyzed")
        else:
            logger.warning("No competitor data could be collected")
            benchmarking_data["error"] = "Failed to scrape any competitors"
        
        return benchmarking_data
    
    def calculate_competitor_gap(
        self, 
        user_metrics: Dict[str, Any], 
        competitor_benchmarks: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate gap between user and competitors.
        
        Args:
            user_metrics: User's engagement metrics
            competitor_benchmarks: Competitor aggregate benchmarks
        
        Returns:
            Gap analysis with scores and recommendations
        """
        if not competitor_benchmarks.get("comparison_ready"):
            return {
                "competitorGap": 0,
                "gap_valid": False,
                "warning": "Insufficient competitor data for gap analysis",
                "data_quality_warning": "Insufficient competitor data for gap analysis"
            }
        
        agg = competitor_benchmarks.get("aggregate", {})
        
        user_engagement = user_metrics.get("engagement_rate", 0)
        competitor_engagement = agg.get("avg_engagement_rate", 0)
        
        user_likes = user_metrics.get("avg_likes", 0)
        competitor_likes = agg.get("avg_likes", 0)
        
        # Calculate gaps (positive = user is behind, negative = user is ahead)
        engagement_gap = 0
        if competitor_engagement > 0:
            engagement_gap = ((competitor_engagement - user_engagement) / competitor_engagement) * 100
        
        likes_gap = 0
        if competitor_likes > 0:
            likes_gap = ((competitor_likes - user_likes) / competitor_likes) * 100
        
        # Overall gap score (0-10 scale, higher = bigger gap)
        overall_gap = min(10, max(0, (engagement_gap + likes_gap) / 20))
        
        # Position category
        if overall_gap <= 2:
            position = "market_leader"
        elif overall_gap <= 4:
            position = "strong"
        elif overall_gap <= 6:
            position = "average"
        elif overall_gap <= 8:
            position = "below_average"
        else:
            position = "lagging"
        
        return {
            "competitorGap": round(overall_gap, 1),
            "gap_valid": True,
            "engagement_gap_percent": round(engagement_gap, 2),
            "likes_gap_percent": round(likes_gap, 2),
            "position_category": position,
            "competitors_analyzed": len(competitor_benchmarks.get("competitors", [])),
            "benchmark_engagement": competitor_engagement,
            "benchmark_likes": competitor_likes,
            "user_engagement": user_engagement,
            "user_likes": user_likes,
        }
    
    async def _handle_acquisition_error(
        self,
        error: Exception,
        mode_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle acquisition error with graceful degradation"""
        error_msg = str(error)
        
        return {
            "success": False,
            "job_id": f"acq_err_{int(time.time())}",
            "mode": mode_info["mode"].value,
            "target_account": mode_info["target"],
            "error": error_msg,
            "data": None,
            "metadata": {
                "sources_used": [],
                "data_coverage": "0%",
                "scrape_timestamp": datetime.utcnow().isoformat(),
                "data_freshness": {
                    "private": None,
                    "public": None,
                },
            },
        }
    
    def get_agent_data_availability(self, mode: str) -> Dict[str, str]:
        """
        Get data availability matrix for downstream agents.
        
        Returns availability status for each agent:
        - "full": Full data available
        - "limited": Partial data available
        - "estimated": Only estimated metrics
        - "unavailable": No data available
        """
        if mode == AnalysisMode.FULL_ACCESS.value:
            return {
                "content_strategist": "full",
                "audience_dynamics": "full",
                "engagement_optimizer": "full",
                "visual_brand": "full",
                "growth_architect": "full",
                "domain_master": "full",
            }
        else:
            return {
                "content_strategist": "limited",
                "audience_dynamics": "estimated",
                "engagement_optimizer": "limited",
                "visual_brand": "full",
                "growth_architect": "limited",
                "domain_master": "full",
            }
    
    async def close(self):
        """Cleanup resources"""
        await self.apify_client.close()
        await self.login_scraper.close()


# =========================
# HELPER FUNCTIONS
# =========================

def adjust_analysis_depth(mode: str) -> Dict[str, Any]:
    """
    Adjust analysis depth based on data availability mode.
    
    Used by downstream agents to adapt their analysis.
    """
    if mode == AnalysisMode.PUBLIC_ONLY.value:
        return {
            "audience_dynamics": "use_estimates",
            "engagement_optimizer": "skip_private_metrics",
            "growth_architect": "limited_recommendations",
            "report_disclaimer": True,
            "confidence_adjustment": 0.7,  # Reduce confidence by 30%
        }
    
    return {
        "full_analysis": True,
        "report_disclaimer": False,
        "confidence_adjustment": 1.0,
    }


def create_agent_data_package(acquisition_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create data package for distribution to analysis agents.
    
    Maps acquisition data to agent-specific requirements.
    """
    mode = acquisition_result.get("mode", AnalysisMode.PUBLIC_ONLY.value)
    data = acquisition_result.get("data", {})
    
    return {
        "source": "instagram_acquisition",
        "mode": mode,
        "target_agents": [
            "content_strategist",
            "audience_dynamics",
            "engagement_optimizer",
            "visual_brand",
            "growth_architect",
            "domain_master",
        ],
        "payload": acquisition_result,
        "agent_data_map": {
            "content_strategist": ["posts", "insights", "estimated"],
            "audience_dynamics": ["audience", "profile", "estimated"],
            "engagement_optimizer": ["posts", "insights", "stories"],
            "visual_brand": ["posts", "profile"],
            "growth_architect": ["audience", "insights", "profile"],
            "domain_master": ["profile", "posts"],
        },
        "analysis_adjustments": adjust_analysis_depth(mode),
    }
