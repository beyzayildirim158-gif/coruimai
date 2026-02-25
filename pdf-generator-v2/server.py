"""
Instagram AI PDF Generator v2.0 - WeasyPrint Based
==================================================

Optimal PDF Generation Stack:
- WeasyPrint: HTML/CSS → PDF (CSS Paged Media)
- Jinja2: Template Engine
- Pillow: Image Processing
- Matplotlib/Plotly: Chart Generation
- CairoSVG: SVG Support

Architecture:
1. Data Layer: Pydantic models for validation
2. Chart Layer: Matplotlib/Plotly for visualizations
3. Template Layer: Jinja2 for HTML generation
4. Render Layer: WeasyPrint for PDF output
5. Storage Layer: Local + S3 compatible
"""

import asyncio
import base64
import io
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from contextlib import asynccontextmanager

import httpx
import orjson
import structlog
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# PDF Generation
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Image & Chart Processing
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import numpy as np

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)
logger = structlog.get_logger()


# =============================================================================
# CONFIGURATION
# =============================================================================

class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Instagram AI PDF Generator v2"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 3006
    
    # Paths
    storage_path: str = "/app/storage/reports"
    fonts_path: str = "/app/fonts"
    templates_path: str = "/app/templates"
    
    # External
    redis_url: str = "redis://redis:6379"
    
    # Limits
    max_file_size_mb: int = 50
    report_retention_days: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()


# =============================================================================
# PYDANTIC MODELS (Data Validation Layer)
# =============================================================================

class AccountData(BaseModel):
    """Instagram account data"""
    username: str
    followers: int = 0
    following: int = 0
    posts: int = 0
    engagementRate: float = 0.0
    avgLikes: int = 0
    avgComments: int = 0
    profilePicUrl: Optional[str] = None
    fullName: Optional[str] = None
    bio: Optional[str] = None
    verified: bool = False
    isBusiness: bool = False
    botScore: Optional[float] = None


class ExecutiveSummary(BaseModel):
    """ELI5 Executive Summary"""
    headline: Optional[str] = None
    grade: Optional[str] = None
    gradeExplanation: Optional[str] = None
    topStrengths: List[str] = []
    criticalIssues: List[str] = []
    quickWins: List[str] = []


class SimplifiedMetric(BaseModel):
    """Simplified metric for ELI5"""
    name: str
    value: str
    verdict: str
    explanation: str
    benchmark: Optional[str] = None


class RewrittenHook(BaseModel):
    """Rewritten hook improvement"""
    original: Optional[str] = None
    badHook: Optional[str] = None
    rewritten: Optional[str] = None
    newHook: Optional[str] = None
    reason: Optional[str] = None
    whyItWorks: Optional[str] = None


class ActionPlan(BaseModel):
    """Action plan with timeframes"""
    thisWeek: List[str] = []
    thisMonth: List[str] = []
    avoid: List[str] = []


class FinalVerdict(BaseModel):
    """DeepSeek final analysis"""
    situation: Optional[str] = None
    verdict: Optional[str] = None
    critical_issues: List[str] = []
    this_week_actions: List[str] = []
    warning: Optional[str] = None


class BusinessIdentity(BaseModel):
    """Business identity classification"""
    account_type: Optional[str] = None
    account_type_explanation: Optional[str] = None
    correct_success_metrics: List[str] = []
    wrong_metrics_to_avoid: List[str] = []


class PhaseInfo(BaseModel):
    """Strategic phase information"""
    determined_phase: str = "growth"
    phase_name: str = "Growth"
    health_score: float = 50.0
    effective_score: float = 50.0
    focus_areas: List[str] = []
    blocked_strategies: List[str] = []
    duration: str = "8-12 weeks"
    reasoning: Optional[str] = None


class MetricsSummary(BaseModel):
    """Sanitization metrics summary"""
    overall_health: float = 50.0
    engagement_depth: float = 50.0
    trust_score: float = 50.0
    ghost_follower_percent: float = 0.0


class SanitizationReport(BaseModel):
    """Data sanitization report"""
    corrections: Dict[str, Any] = {}
    warnings: List[str] = []
    phase_info: Optional[PhaseInfo] = None
    metrics_summary: Optional[MetricsSummary] = None


class RiskAssessments(BaseModel):
    """Risk assessment data"""
    overall: str = "medium"
    bot_risk: str = "low"
    shadowban_risk: str = "low"
    algorithm_penalty: str = "low"
    risk_factors: List[str] = []


class AdvancedAnalysis(BaseModel):
    """Advanced analysis data"""
    executiveSummary: Optional[Dict[str, Any]] = None
    riskAssessments: Optional[RiskAssessments] = None
    strategies: Optional[Dict[str, Any]] = None
    detailedFindings: Optional[Dict[str, Any]] = None
    prioritizedRecommendations: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class ContentPlanDay(BaseModel):
    """Single day content plan"""
    day: int = 1
    dayName: str = ""
    contentType: str = ""
    topic: str = ""
    hook: Optional[str] = None
    caption: Optional[str] = None
    hashtags: List[str] = []
    bestTime: Optional[str] = None
    objective: Optional[str] = None


class ContentPlan(BaseModel):
    """Weekly content plan"""
    weeklyPlan: List[ContentPlanDay] = []
    monthlyTheme: Optional[str] = None
    contentPillars: List[str] = []


class ELI5Report(BaseModel):
    """Simplified ELI5 report"""
    executiveSummary: Optional[ExecutiveSummary] = None
    simplifiedMetrics: Optional[Dict[str, SimplifiedMetric]] = None
    rewrittenHooks: List[RewrittenHook] = []
    actionPlan: Optional[ActionPlan] = None
    motivationalNote: Optional[str] = None
    findings: List[Dict[str, Any]] = []
    finalVerdict: Optional[FinalVerdict] = None
    businessIdentity: Optional[BusinessIdentity] = None
    swotAnalysis: Optional[Dict[str, List[str]]] = None
    whatHappensIfNothing: Optional[str] = None
    motivationalKick: Optional[str] = None


class AgentResult(BaseModel):
    """Single agent result"""
    agentName: Optional[str] = None
    agentRole: Optional[str] = None
    findings: List[Any] = []
    recommendations: List[Any] = []
    metrics: Dict[str, Any] = {}
    parseError: bool = False


class GeneratePayload(BaseModel):
    """Main PDF generation payload"""
    reportId: str
    analysisId: str
    accountData: AccountData
    overallScore: Optional[float] = None
    scoreGrade: Optional[str] = None
    tier: str = "standard"  # free, standard, premium
    
    # Reports
    eli5Report: Optional[ELI5Report] = None
    advancedAnalysis: Optional[AdvancedAnalysis] = None
    contentPlan: Optional[ContentPlan] = None
    sanitizationReport: Optional[SanitizationReport] = None
    
    # Agent results
    agentResults: Dict[str, AgentResult] = {}
    
    # Actions
    prioritizedActions: List[Dict[str, Any]] = []
    recommendations: List[str] = []


class GenerateResponse(BaseModel):
    """PDF generation response"""
    success: bool
    pdfUrl: str
    fileSize: int
    pageCount: int
    generatedAt: str
    processingTime: float


# =============================================================================
# CHART GENERATOR (Visualization Layer)
# =============================================================================

class ChartGenerator:
    """
    Generates charts and visualizations using Matplotlib
    Returns base64 encoded images for embedding in HTML
    """
    
    # Color palette (consistent with brand)
    COLORS = {
        'primary': '#1e3a8a',
        'secondary': '#3b82f6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'info': '#06b6d4',
        'purple': '#8b5cf6',
        'pink': '#ec4899',
        'slate': '#64748b',
        'background': '#f8fafc',
    }
    
    @classmethod
    def _fig_to_base64(cls, fig: Figure, dpi: int = 150) -> str:
        """Convert matplotlib figure to base64 PNG"""
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', transparent=False)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_base64}"
    
    @classmethod
    def create_score_gauge(cls, score: float, grade: str, size: tuple = (4, 2.5)) -> str:
        """
        Create a professional gauge chart for overall score
        """
        fig, ax = plt.subplots(figsize=size)
        
        # Score ranges and colors
        ranges = [
            (0, 30, cls.COLORS['danger'], 'F'),
            (30, 50, '#f97316', 'D'),
            (50, 70, cls.COLORS['warning'], 'C'),
            (70, 85, '#22c55e', 'B'),
            (85, 100, cls.COLORS['success'], 'A'),
        ]
        
        # Draw arc segments
        theta_start = 180
        theta_range = 180
        
        for start, end, color, _ in ranges:
            start_angle = theta_start - (start / 100) * theta_range
            end_angle = theta_start - (end / 100) * theta_range
            wedge = mpatches.Wedge(
                center=(0.5, 0),
                r=0.45,
                theta1=end_angle,
                theta2=start_angle,
                width=0.12,
                facecolor=color,
                edgecolor='white',
                linewidth=2
            )
            ax.add_patch(wedge)
        
        # Draw needle
        needle_angle = np.radians(180 - (score / 100) * 180)
        needle_length = 0.35
        ax.arrow(
            0.5, 0,
            needle_length * np.cos(needle_angle),
            needle_length * np.sin(needle_angle),
            head_width=0.03,
            head_length=0.02,
            fc=cls.COLORS['primary'],
            ec=cls.COLORS['primary'],
            linewidth=2
        )
        
        # Center circle
        center_circle = plt.Circle((0.5, 0), 0.06, color=cls.COLORS['primary'], zorder=5)
        ax.add_patch(center_circle)
        
        # Score text
        ax.text(0.5, -0.15, f"{score:.0f}", fontsize=28, fontweight='bold',
                ha='center', va='center', color=cls.COLORS['primary'])
        ax.text(0.5, -0.28, grade, fontsize=18, fontweight='bold',
                ha='center', va='center', 
                color=cls.COLORS['success'] if score >= 70 else 
                      cls.COLORS['warning'] if score >= 50 else cls.COLORS['danger'])
        
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.4, 0.55)
        ax.set_aspect('equal')
        ax.axis('off')
        
        return cls._fig_to_base64(fig)
    
    @classmethod
    def create_metrics_radar(cls, metrics: Dict[str, float], size: tuple = (5, 5)) -> str:
        """
        Create radar/spider chart for metric comparison
        """
        fig, ax = plt.subplots(figsize=size, subplot_kw=dict(polar=True))
        
        # Data
        categories = list(metrics.keys())
        values = list(metrics.values())
        N = len(categories)
        
        if N < 3:
            # Need at least 3 points for radar
            return ""
        
        # Compute angles
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        values += values[:1]  # Close the polygon
        angles += angles[:1]
        
        # Draw
        ax.plot(angles, values, 'o-', linewidth=2, color=cls.COLORS['primary'])
        ax.fill(angles, values, alpha=0.25, color=cls.COLORS['secondary'])
        
        # Labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=9)
        ax.set_ylim(0, 100)
        
        # Grid styling
        ax.set_facecolor(cls.COLORS['background'])
        ax.spines['polar'].set_color(cls.COLORS['slate'])
        
        return cls._fig_to_base64(fig)
    
    @classmethod
    def create_risk_bars(cls, risks: Dict[str, str], size: tuple = (5, 2)) -> str:
        """
        Create horizontal bar chart for risk assessment
        """
        fig, ax = plt.subplots(figsize=size)
        
        risk_values = {'low': 25, 'medium': 50, 'high': 75, 'critical': 100}
        risk_colors = {
            'low': cls.COLORS['success'],
            'medium': cls.COLORS['warning'],
            'high': '#f97316',
            'critical': cls.COLORS['danger']
        }
        
        categories = list(risks.keys())
        values = [risk_values.get(v.lower(), 50) for v in risks.values()]
        colors = [risk_colors.get(v.lower(), cls.COLORS['slate']) for v in risks.values()]
        
        y_pos = np.arange(len(categories))
        bars = ax.barh(y_pos, values, color=colors, height=0.6, edgecolor='white')
        
        # Labels
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categories, fontsize=9)
        ax.set_xlim(0, 100)
        ax.set_xlabel('Risk Level', fontsize=9)
        
        # Add value labels
        for bar, val, risk in zip(bars, values, risks.values()):
            ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                   risk.capitalize(), va='center', fontsize=8, color=cls.COLORS['slate'])
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        return cls._fig_to_base64(fig)
    
    @classmethod
    def create_content_mix_pie(cls, mix: Dict[str, float], size: tuple = (4, 4)) -> str:
        """
        Create pie chart for content format mix
        """
        fig, ax = plt.subplots(figsize=size)
        
        format_colors = {
            'reels': cls.COLORS['pink'],
            'carousel': cls.COLORS['secondary'],
            'single_post': cls.COLORS['slate'],
            'stories': cls.COLORS['warning'],
        }
        
        labels = list(mix.keys())
        values = list(mix.values())
        colors = [format_colors.get(k.lower(), cls.COLORS['info']) for k in labels]
        
        # Format labels
        label_map = {
            'reels': 'Reels',
            'carousel': 'Carousel',
            'single_post': 'Tek Post',
            'stories': 'Stories',
        }
        labels = [label_map.get(l.lower(), l) for l in labels]
        
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, colors=colors,
            autopct='%1.0f%%', startangle=90,
            wedgeprops=dict(width=0.7, edgecolor='white'),
            textprops=dict(fontsize=9)
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('İçerik Format Dağılımı', fontsize=11, fontweight='bold', pad=10)
        
        return cls._fig_to_base64(fig)
    
    @classmethod
    def create_growth_trend(cls, data: List[Dict], size: tuple = (6, 3)) -> str:
        """
        Create line chart for growth trend
        """
        if not data:
            return ""
            
        fig, ax = plt.subplots(figsize=size)
        
        dates = [d.get('date', '') for d in data]
        values = [d.get('value', 0) for d in data]
        
        ax.plot(dates, values, 'o-', color=cls.COLORS['primary'], linewidth=2, markersize=6)
        ax.fill_between(dates, values, alpha=0.1, color=cls.COLORS['secondary'])
        
        ax.set_ylabel('Takipçi', fontsize=9)
        ax.tick_params(axis='x', rotation=45)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        return cls._fig_to_base64(fig)


# =============================================================================
# TEMPLATE FILTERS (Jinja2 Helpers)
# =============================================================================

def format_number(num: Union[int, float, None]) -> str:
    """Format number with K/M suffix"""
    if num is None or (isinstance(num, float) and np.isnan(num)):
        return '--'
    if num == 0:
        return '--'
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num/1_000:.1f}K"
    return f"{num:,.0f}".replace(',', '.')


def format_percent(num: Union[float, None]) -> str:
    """Format percentage"""
    if num is None or (isinstance(num, float) and np.isnan(num)):
        return '--'
    if num == 0:
        return '--'
    return f"{num:.2f}%"


def format_growth(num: Union[float, None]) -> str:
    """Format growth with sign"""
    if num is None or (isinstance(num, float) and np.isnan(num)):
        return 'N/A'
    sign = '+' if num >= 0 else ''
    return f"{sign}{num:.1f}%"


def format_date(date: Union[str, datetime, None]) -> str:
    """Format date to Turkish locale"""
    if date is None:
        return datetime.now().strftime("%d %B %Y")
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        except:
            return date
    months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
              'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    return f"{date.day} {months[date.month-1]} {date.year}"


def get_grade_color(grade: Optional[str]) -> str:
    """Get color for grade"""
    colors = {
        'A': '#10b981', 'A+': '#10b981',
        'B': '#22c55e', 'B+': '#22c55e',
        'C': '#f59e0b', 'C+': '#f59e0b',
        'D': '#f97316', 'D+': '#f97316',
        'F': '#ef4444',
    }
    return colors.get(grade.upper() if grade else '', '#6b7280')


def get_score_color(score: Union[float, None]) -> str:
    """Get color based on score"""
    if score is None:
        return '#64748b'
    if score >= 80:
        return '#10b981'
    if score >= 60:
        return '#22c55e'
    if score >= 40:
        return '#f59e0b'
    return '#ef4444'


def get_risk_color(level: Optional[str]) -> str:
    """Get color for risk level"""
    colors = {
        'low': '#10b981', 'düşük': '#10b981',
        'medium': '#f59e0b', 'orta': '#f59e0b',
        'high': '#f97316', 'yüksek': '#f97316',
        'critical': '#ef4444', 'kritik': '#ef4444',
    }
    return colors.get(level.lower() if level else '', '#64748b')


def format_risk_level(level: Optional[str]) -> str:
    """Format risk level to Turkish"""
    levels = {
        'low': 'Düşük', 'medium': 'Orta',
        'high': 'Yüksek', 'critical': 'Kritik',
    }
    return levels.get(level.lower() if level else '', level or 'Bilinmiyor')


def get_phase_info(phase: Optional[str]) -> Dict[str, str]:
    """Get phase display info"""
    phases = {
        'rescue': {'icon': '🚨', 'color': '#ef4444', 'name': 'Kurtarma Fazı'},
        'growth': {'icon': '📈', 'color': '#f59e0b', 'name': 'Büyüme Fazı'},
        'monetization': {'icon': '💰', 'color': '#10b981', 'name': 'Monetizasyon Fazı'},
    }
    return phases.get(phase.lower() if phase else '', 
                     {'icon': '📊', 'color': '#64748b', 'name': 'Analiz Fazı'})


def get_confidence_info(score: Union[float, None]) -> Dict[str, str]:
    """Get confidence level info"""
    if score is None or score < 60:
        return {'level': 'low', 'text': 'Düşük Güvenilirlik', 'color': '#ef4444', 'icon': '🔴'}
    if score < 80:
        return {'level': 'medium', 'text': 'Orta Güvenilirlik', 'color': '#f59e0b', 'icon': '🟡'}
    return {'level': 'high', 'text': 'Yüksek Güvenilirlik', 'color': '#10b981', 'icon': '🟢'}


def is_tier_allowed(tier: str, required: str) -> bool:
    """Check if tier allows feature"""
    levels = {'free': 0, 'standard': 1, 'premium': 2}
    return levels.get(tier.lower(), 0) >= levels.get(required.lower(), 0)


# =============================================================================
# PDF GENERATOR (Render Layer)
# =============================================================================

class PDFGenerator:
    """
    WeasyPrint-based PDF Generator
    
    Features:
    - CSS Paged Media support
    - Custom fonts
    - Embedded charts
    - Professional layout
    """
    
    def __init__(self):
        # Setup Jinja2 environment
        templates_dir = Path(settings.templates_path)
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # Register filters
        self.jinja_env.filters['format_number'] = format_number
        self.jinja_env.filters['format_percent'] = format_percent
        self.jinja_env.filters['format_growth'] = format_growth
        self.jinja_env.filters['format_date'] = format_date
        self.jinja_env.filters['get_grade_color'] = get_grade_color
        self.jinja_env.filters['get_score_color'] = get_score_color
        self.jinja_env.filters['get_risk_color'] = get_risk_color
        self.jinja_env.filters['format_risk_level'] = format_risk_level
        
        # Register globals
        self.jinja_env.globals['get_phase_info'] = get_phase_info
        self.jinja_env.globals['get_confidence_info'] = get_confidence_info
        self.jinja_env.globals['is_tier_allowed'] = is_tier_allowed
        self.jinja_env.globals['now'] = datetime.now
        
        # Font configuration
        self.font_config = FontConfiguration()
        
        # Storage
        self.storage_path = Path(settings.storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("PDFGenerator initialized", 
                   templates_dir=str(templates_dir),
                   storage_path=str(self.storage_path))
    
    async def fetch_profile_image(self, url: Optional[str]) -> Optional[str]:
        """Fetch profile image and convert to base64"""
        if not url:
            return None
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Process image with Pillow
                img = Image.open(io.BytesIO(response.content))
                img = img.convert('RGB')
                
                # Resize for PDF
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                buffer.seek(0)
                
                return f"data:image/jpeg;base64,{base64.b64encode(buffer.read()).decode()}"
        except Exception as e:
            logger.warning("Failed to fetch profile image", url=url, error=str(e))
            return None
    
    def generate_charts(self, payload: GeneratePayload) -> Dict[str, str]:
        """Generate all charts for the report"""
        charts = {}
        
        # 1. Score gauge
        if payload.overallScore is not None:
            charts['score_gauge'] = ChartGenerator.create_score_gauge(
                payload.overallScore,
                payload.scoreGrade or 'C'
            )
        
        # 2. Metrics radar
        agent_scores = {}
        for key, agent in payload.agentResults.items():
            if agent.metrics and 'overallScore' in agent.metrics:
                # Clean agent name
                name_map = {
                    'domainMaster': 'Sektör',
                    'growthVirality': 'Büyüme',
                    'salesConversion': 'Satış',
                    'visualBrand': 'Görsel',
                    'communityLoyalty': 'Topluluk',
                    'attentionArchitect': 'Dikkat',
                }
                name = name_map.get(key, key[:8])
                score = agent.metrics.get('overallScore', 0)
                if isinstance(score, (int, float)) and score > 0:
                    agent_scores[name] = min(100, max(0, score))
        
        if len(agent_scores) >= 3:
            charts['metrics_radar'] = ChartGenerator.create_metrics_radar(agent_scores)
        
        # 3. Risk bars
        if payload.advancedAnalysis and payload.advancedAnalysis.riskAssessments:
            risks = payload.advancedAnalysis.riskAssessments
            risk_data = {
                'Genel': risks.overall,
                'Bot': risks.bot_risk,
                'Shadowban': risks.shadowban_risk,
                'Algoritma': risks.algorithm_penalty,
            }
            charts['risk_bars'] = ChartGenerator.create_risk_bars(risk_data)
        
        # 4. Content mix pie
        if payload.advancedAnalysis and payload.advancedAnalysis.strategies:
            strategies = payload.advancedAnalysis.strategies
            if 'contentFormats' in strategies and strategies['contentFormats']:
                current_mix = strategies['contentFormats'].get('current_mix', {})
                if current_mix:
                    charts['content_mix'] = ChartGenerator.create_content_mix_pie(current_mix)
        
        return charts
    
    async def generate(self, payload: GeneratePayload) -> tuple[bytes, int]:
        """
        Generate PDF from payload
        
        Returns:
            Tuple of (pdf_bytes, page_count)
        """
        start_time = datetime.now()
        
        # Fetch profile image
        profile_image = await self.fetch_profile_image(
            payload.accountData.profilePicUrl
        )
        
        # Generate charts
        charts = self.generate_charts(payload)
        
        # Prepare template context
        context = {
            'report_id': payload.reportId,
            'analysis_id': payload.analysisId,
            'account': payload.accountData,
            'profile_image': profile_image,
            'overall_score': payload.overallScore,
            'score_grade': payload.scoreGrade,
            'tier': payload.tier,
            'eli5': payload.eli5Report,
            'advanced': payload.advancedAnalysis,
            'content_plan': payload.contentPlan,
            'sanitization': payload.sanitizationReport,
            'agents': payload.agentResults,
            'actions': payload.prioritizedActions,
            'charts': charts,
            'generated_at': datetime.now(),
        }
        
        # Render HTML
        template = self.jinja_env.get_template('report.html')
        html_content = template.render(**context)
        
        # Generate PDF with WeasyPrint
        html_doc = HTML(string=html_content, base_url=str(settings.templates_path))
        
        # Load CSS
        css_path = Path(settings.templates_path) / 'styles.css'
        stylesheets = []
        if css_path.exists():
            stylesheets.append(CSS(filename=str(css_path), font_config=self.font_config))
        
        # Render PDF
        pdf_doc = html_doc.render(stylesheets=stylesheets, font_config=self.font_config)
        pdf_bytes = pdf_doc.write_pdf()
        page_count = len(pdf_doc.pages)
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info("PDF generated",
                   report_id=payload.reportId,
                   pages=page_count,
                   size_kb=len(pdf_bytes) // 1024,
                   duration_s=duration)
        
        return pdf_bytes, page_count
    
    async def save_and_generate(self, payload: GeneratePayload) -> GenerateResponse:
        """Generate PDF and save to storage"""
        start_time = datetime.now()
        
        # Generate PDF
        pdf_bytes, page_count = await self.generate(payload)
        
        # Save to file
        filename = f"report-{int(datetime.now().timestamp() * 1000)}.pdf"
        filepath = self.storage_path / filename
        
        with open(filepath, 'wb') as f:
            f.write(pdf_bytes)
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return GenerateResponse(
            success=True,
            pdfUrl=f"http://localhost:{settings.port}/reports/{filename}",
            fileSize=len(pdf_bytes),
            pageCount=page_count,
            generatedAt=datetime.now().isoformat(),
            processingTime=duration
        )


# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting PDF Generator v2 (WeasyPrint)")
    app.state.generator = PDFGenerator()
    yield
    # Shutdown
    logger.info("Shutting down PDF Generator v2")


# Create app
app = FastAPI(
    title=settings.app_name,
    description="Professional PDF Generation with WeasyPrint",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for generated reports
reports_path = Path(settings.storage_path)
reports_path.mkdir(parents=True, exist_ok=True)
app.mount("/reports", StaticFiles(directory=str(reports_path)), name="reports")


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "pdf-generator-v2",
        "engine": "weasyprint",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate_pdf(payload: GeneratePayload):
    """
    Generate PDF report from analysis data
    """
    try:
        generator: PDFGenerator = app.state.generator
        response = await generator.save_and_generate(payload)
        return response
    except Exception as e:
        logger.error("PDF generation failed", error=str(e), report_id=payload.reportId)
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@app.post("/generate/preview")
async def generate_preview(payload: GeneratePayload):
    """
    Generate PDF and return as binary response
    """
    try:
        generator: PDFGenerator = app.state.generator
        pdf_bytes, page_count = await generator.generate(payload)
        
        return FileResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            filename=f"instagram-ai-report-{payload.accountData.username}.pdf",
            headers={
                "X-Page-Count": str(page_count),
                "X-File-Size": str(len(pdf_bytes))
            }
        )
    except Exception as e:
        logger.error("Preview generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reports/{filename}")
async def get_report(filename: str):
    """Download generated report"""
    filepath = reports_path / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(filepath, media_type="application/pdf")


@app.delete("/reports/{filename}")
async def delete_report(filename: str):
    """Delete generated report"""
    filepath = reports_path / filename
    if filepath.exists():
        filepath.unlink()
        return {"deleted": True, "filename": filename}
    raise HTTPException(status_code=404, detail="Report not found")


# =============================================================================
# MAIN ENTRY
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
