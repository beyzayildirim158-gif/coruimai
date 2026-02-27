# Metric Sanity Gates - Critical Consistency Enforcement
# Fixes contradictory metrics, vague advice, data hallucinations, and phase prioritization
"""
Metric Sanity Gates - PhD Level Post-Processing

Bu modül analiz çıktılarındaki mantıksal tutarsızlıkları düzeltir:
1. Metric Sanity Gates: Çelişkili metrikleri clamp eder
2. Specificity Enforcement: Genel tavsiyeleri spesifik şablonlara dönüştürür  
3. Competitor Data Validation: Boş veriye dayalı hallüsinasyonları önler
4. Phase Prioritization: Health score'a göre stratejik faz belirler
"""

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class MetricSanityGates:
    """
    Post-processor that enforces logical consistency across all agent outputs.
    
    This class runs AFTER all agents complete and BEFORE report generation.
    It validates and corrects contradictory metrics.
    """
    
    def __init__(self):
        # Sanity gate thresholds
        self.gates = {
            "monetization_requires_engagement": {
                "engagement_depth_min": 30,
                "trust_score_min": 50,
                "monetization_cap": 40,
            },
            "ghost_follower_penalty": {
                "ghost_threshold_percent": 20,
                "algorithm_health_penalty": 50,
            },
            "competitor_data_validation": {
                "min_competitors_for_gap": 1,
                "min_data_points": 3,
            },
        }
        
        # Phase definitions based on health score
        self.strategic_phases = {
            "rescue": {
                "health_range": (0, 49),
                "focus_areas": ["ghost_removal", "bio_fix", "content_formatting", "profile_optimization"],
                "blocked_strategies": ["influencer_collaboration", "monetization", "brand_deals", "paid_promotion"],
                "phase_name": "Foundation & Cleanup",
                "duration": "4-8 weeks",
            },
            "growth": {
                "health_range": (50, 70),
                "focus_areas": ["viral_hooks", "reach_optimization", "content_pillars", "engagement_boost"],
                "blocked_strategies": ["aggressive_monetization", "high_ticket_sales"],
                "phase_name": "Growth & Reach",
                "duration": "8-12 weeks",
            },
            "monetization": {
                "health_range": (71, 100),
                "focus_areas": ["cta_optimization", "funnel_building", "collaboration", "revenue_streams"],
                "blocked_strategies": [],
                "phase_name": "Monetization & Scale",
                "duration": "Ongoing",
            },
        }
        
        # Specific action templates for common issues
        self.action_templates = {
            "weak_hook": {
                "issue": "Weak Hook Retention",
                "fix_action": "Use the 'Stop-Scroll' Pattern",
                "template": {
                    "visual": "Hand gesture stopping the camera OR dramatic zoom-in",
                    "text_overlay": "Stop scrolling if you are a [Target Audience]",
                    "caption_start": "Read this before you swipe...",
                    "timing": "Hook must hit within 0.5-1 second"
                },
                "examples": [
                    "POV: Your [Niche] journey just changed",
                    "Nobody talks about this [Niche] secret",
                    "Wait... did you know this about [Topic]?"
                ]
            },
            "low_engagement": {
                "issue": "Low Engagement Rate",
                "fix_action": "Implement 'Comment Magnet' Strategy",
                "template": {
                    "technique": "End posts with binary choice questions",
                    "format": "A or B? Comment below 👇",
                    "examples": ["Haftanın en verimli içerik saati sizce kaç?", "İlk bakışta en değerli metrik sizce hangisi?"],
                    "cta_placement": "Last line of caption + pinned comment"
                },
                "expected_impact": "+50-100% comment rate within 2 weeks"
            },
            "ghost_followers": {
                "issue": "High Ghost Follower Percentage",
                "fix_action": "Run 'Follower Cleanse' Protocol",
                "template": {
                    "step_1": "Post Story asking 'Still interested in [Niche]? React with 🔥'",
                    "step_2": "Wait 48 hours, identify non-reactors",
                    "step_3": "Soft-block inactive followers (500-1000/week max)",
                    "step_4": "Post re-engagement content with 'For my real ones' angle"
                },
                "warning": "Do NOT remove more than 5% of followers per week"
            },
            "poor_bio": {
                "issue": "Unclear Bio/Value Proposition",
                "fix_action": "Implement 'WHO-WHAT-WHY' Bio Formula",
                "template": {
                    "line_1": "[WHO] Your specific target audience identifier",
                    "line_2": "[WHAT] The transformation/value you provide",
                    "line_3": "[WHY] Social proof or unique differentiator",
                    "line_4": "[CTA] Clear next step with link",
                    "max_length": "150 characters total"
                },
                "example": "Helping busy moms 👩‍👧 | Lose 10kg without dieting 🏃‍♀️ | 50K+ transformed ✨ | Free guide ⬇️"
            },
            "inconsistent_posting": {
                "issue": "Inconsistent Posting Schedule",
                "fix_action": "Establish 'Content Rhythm' System",
                "template": {
                    "minimum_frequency": "4 posts/week (non-negotiable)",
                    "optimal_frequency": "1-2 posts/day",
                    "content_mix": {
                        "educational": "40%",
                        "entertaining": "30%",
                        "promotional": "20%",
                        "personal": "10%"
                    },
                    "best_times": "Check your insights, typically 9AM, 12PM, 7PM local"
                }
            },
            "no_cta": {
                "issue": "Missing or Weak Call-to-Action",
                "fix_action": "Add 'Micro-CTA' to Every Post",
                "template": {
                    "soft_cta": "Save this for later 📌",
                    "engagement_cta": "Tag someone who needs this 👇",
                    "growth_cta": "Follow for more [Niche] tips",
                    "conversion_cta": "DM me 'START' for free guide",
                    "placement": "Last line of caption + first comment"
                }
            },
            "poor_hashtags": {
                "issue": "Ineffective Hashtag Strategy",
                "fix_action": "Use '3-3-3' Hashtag Formula",
                "template": {
                    "small_hashtags": "3 hashtags with <50K posts (high visibility chance)",
                    "medium_hashtags": "3 hashtags with 50K-500K posts (moderate competition)",
                    "large_hashtags": "3 hashtags with 500K-2M posts (discovery potential)",
                    "placement": "Caption (not comments) for maximum reach",
                    "total": "9-15 hashtags maximum"
                }
            },
            "low_saves": {
                "issue": "Low Save Rate on Content",
                "fix_action": "Create 'Reference Content' Format",
                "template": {
                    "format_type": "Carousel with actionable steps",
                    "structure": [
                        "Slide 1: Hook + Promise",
                        "Slides 2-8: Numbered actionable tips",
                        "Final Slide: Summary + CTA to save"
                    ],
                    "text_prompt": "Add 'SAVE this for when you need it 📌' in caption",
                    "design_tip": "Use consistent template for brand recognition"
                }
            }
        }

        # Principal System Auditor lexicon guard
        self.prohibited_lexicon_map = {
            "çöp": "Critical Underperformance",
            "sıfır": "Insufficient Data",
            "alarm": "Priority Risk Signal",
            "felaket": "Critical Underperformance",
            "bad": "Critical Underperformance",
            "very bad": "Critical Underperformance",
            "you need to fix this": "This presents a Strategic Opportunity for improvement",
            "morning workout or evening": "İkili tercih odaklı yorum CTA örneği",
            "coffee or tea": "İkili tercih odaklı yorum CTA örneği",
        }

        # Strategy registry for diversity enforcement
        self.strategy_library = [
            "Comment Magnet",
            "Story Sticker",
            "DM Automation",
            "Carousel Value",
            "Micro-CTA",
            "Retention Loop",
            "UGC Trigger",
            "Hook Ladder",
            "Lead Magnet",
            "Community Ritual",
        ]

        # Context Integrity Protocol (niche/sub-niche aware)
        self.context_integrity = {
            "spirituality_forbidden": [
                "workout", "abs", "fitness", "gym", "diet", "reps", "sets",
                "antrenman", "karın", "diyet"
            ],
            "spirituality_forced": [
                "meditation", "energy", "healing", "routine"
            ],
            # Travel / City Guide niche guardrails
            "travel_forbidden": [
                "tech", "iphone", "apps", "application", "technology", "gadget",
                "smartphone", "uygulama", "teknoloji", "akillı", "yazilim", "software"
            ],
            "travel_forced_hint": (
                "Yerel yemek kültürü, gizli mekânlar ve seyahat ipucu odaklı "
                "içerik önerileri kullanın (Hidden Gems, Local Food, Travel Hacks)."
            ),
            # Retro / Vintage / Nostalgia niche guardrails
            "retro_forbidden": [
                "iphone", "ios", "android", "app store", "5g",
                "modern tech", "software update", "uygulama mağazası",
                "yeni güncelleme", "smartphone", "akillı telefon"
            ],
            "retro_forced": [
                "nokia", "snake game", "battery life", "collection",
                "history", "classic", "vintage", "koleksiyon", "tarih",
                "klasik", "nostalji"
            ],
            "retro_forced_hint": (
                "Retro/Vintage içeriği için: Nokia, Snake Game, pil ömrü, koleksiyon, "
                "tarihî önemli anlar ve klasik tasarım odaklı öneriler kullanın."
            ),
            # Fashion / Clothing / Style niche guardrails
            "fashion_forbidden": [
                "tech", "iphone", "apps", "application", "software", "gadget",
                "smartphone", "teknoloji", "uygulama", "yazılım", "donanım"
            ],
            "fashion_forced": [
                "outfit", "fabric", "styling", "wardrobe", "kıyafet",
                "giyim", "stil", "moda", "kombinasyon"
            ],
            "fashion_forced_hint": (
                "Moda/Giyim nişi için: Outfit Hacks, Fabric Care, Styling Tips ve "
                "Wardrobe Essentials odaklı içerik önerileri kullanın."
            ),
            # Food / Cooking niche guardrails
            "food_forced": [
                "recipe", "taste", "kitchen", "tarif", "lezzet",
                "yemek", "mutfak", "pişirme", "malzeme"
            ],
            "food_forced_hint": (
                "Yemek/Mutfak nişi için: Recipe, Taste Test ve Kitchen Hacks "
                "odaklı içerik önerileri kullanın."
            ),
            # Local Business niche guardrails
            "local_business_forced": [
                "visit us", "location", "local", "ziyaret", "konum",
                "yerel", "etkinlik", "event", "maps", "harita"
            ],
            "local_business_forced_hint": (
                "Yerel işletme nişi için: Location tag, 'Bizi ziyaret edin', "
                "yerel etkinlikler ve müşteri buluşması odaklı içerik önerileri kullanın."
            ),
        }

        # Logic Override Protocol thresholds
        self.logic_override = {
            "engagement_high_threshold": 5.0,   # >5% → forbid 'Low Engagement'
            "dashboard_score_growth_threshold": 80,  # >80 → redirect crit to Growth
        }

        # Tagging keyword maps for TAGGING_PRECISION gate
        self.tag_keyword_map = {
            "Visibility": [
                "hashtag", "#", "etiket", "keşfet", "reach", "erişim",
                "visibility", "görünürlük", "discovery", "keşif", "explore"
            ],
            "Content": [
                "content", "içerik", "reel", "story", "caption", "gönderi",
                "video", "post", "yayın", "yazı", "format", "template", "hook",
                "scenario", "senaryo"
            ],
            "Monetization": [
                "money", "sponsor", "collab", "gelir", "kazanç", "monetiz",
                "brand deal", "satış", "sales", "affiliate", "paid", "ücretli",
                "işbirliği", "reklam", "revenue", "income", "conversion"
            ],
        }
    
    def apply_all_gates(
        self,
        agent_results: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Apply all sanity gates and return corrected results + gate report.
        
        Returns:
            Tuple of (corrected_results, gate_report)
        """
        corrections = []
        warnings = []

        # Gate 0: Mathematical Immutability Protocol
        agent_results, math_corrections, math_warnings = self._apply_mathematical_immutability(
            agent_results, account_data
        )
        corrections.extend(math_corrections)
        warnings.extend(math_warnings)
        
        # Extract key metrics from various agents
        metrics = self._extract_cross_agent_metrics(agent_results)

        # Gate 0.5: Logic Synchronization Lock
        agent_results, sync_corrections, sync_warnings = self._apply_logic_synchronization_lock(
            agent_results, metrics, account_data
        )
        corrections.extend(sync_corrections)
        warnings.extend(sync_warnings)
        
        # Gate 1: Monetization-Engagement Consistency
        agent_results, gate1_corrections = self._apply_monetization_gate(
            agent_results, metrics
        )
        corrections.extend(gate1_corrections)
        
        # Gate 2: Ghost Follower Algorithm Penalty  
        agent_results, gate2_corrections = self._apply_ghost_follower_gate(
            agent_results, metrics, account_data
        )
        corrections.extend(gate2_corrections)
        
        # Gate 3: Competitor Data Validation
        agent_results, gate3_corrections, gate3_warnings = self._apply_competitor_data_gate(
            agent_results
        )
        corrections.extend(gate3_corrections)
        warnings.extend(gate3_warnings)
        
        # Gate 4: Strategic Phase Enforcement
        agent_results, phase_info = self._apply_phase_enforcement(
            agent_results, metrics
        )
        
        # Gate 5: Specificity Enforcement
        agent_results = self._apply_specificity_enforcement(agent_results, metrics)

        # Gate 6: Deduplication & Loop Prevention
        agent_results, dedup_warnings = self._apply_deduplication_loop_prevention(agent_results)
        warnings.extend(dedup_warnings)

        # Gate 7: Hallucination Containment
        agent_results, hallucination_warnings = self._apply_hallucination_containment(agent_results)
        warnings.extend(hallucination_warnings)

        # Gate 8: Tone & Language Standardization
        agent_results = self._apply_tone_language_standard(agent_results)

        # Gate 8.5: Dashboard metric sync for textual statements
        agent_results, data_sync_warnings = self._apply_data_sync_with_dashboard(agent_results, account_data)
        warnings.extend(data_sync_warnings)

        # Gate 8.6: Benchmark-commentary synchronization (math/text alignment)
        agent_results, benchmark_sync_warnings = self._apply_benchmark_commentary_sync(
            agent_results, metrics, account_data
        )
        warnings.extend(benchmark_sync_warnings)

        # Gate 8.65: Logic Override Protocol (engagement/dashboard score enforcement)
        agent_results, logic_override_warnings = self._apply_logic_override_protocol(
            agent_results, metrics, account_data
        )
        warnings.extend(logic_override_warnings)

        # Gate 8.66: Estimation Fallback Logic (brand deal estimate when API returns null/0)
        agent_results, estimation_warnings = self._apply_estimation_fallback_gate(
            agent_results, account_data
        )
        warnings.extend(estimation_warnings)

        # Gate 8.7: Context-aware recommendation filter (niche relevance)
        agent_results, context_warnings = self._apply_context_awareness_fix(agent_results, account_data)
        warnings.extend(context_warnings)

        # Gate 9: Section-specific constraints
        agent_results, section_warnings = self._apply_section_specific_constraints(agent_results, metrics, account_data)
        warnings.extend(section_warnings)

        # Gate 10: Advanced Analytics Modules (Heatmap / Sentiment / Polarity / Benchmark)
        advanced_analytics, advanced_warnings = self._run_advanced_analytics_modules(account_data, agent_results)
        warnings.extend(advanced_warnings)
        self._attach_advanced_analytics(agent_results, advanced_analytics)

        # Gate 11: Output Sanitization (remove internal logs/prompt residues)
        agent_results = self._apply_output_sanitization(agent_results)

        # Gate 11.5: Tagging Precision (hashtag→Visibility, content→Content, money→Monetization)
        agent_results = self._apply_tagging_precision(agent_results)

        # Gate 11.75: Action Plan Cleanup — suppress action items for null-metric agents
        agent_results = self._apply_action_plan_cleanup(agent_results)
        
        gate_report = {
            "gates_applied": [
                "mathematical_immutability_protocol",
                "data_sanity_protocol",
                "logic_synchronization_lock",
                "monetization_engagement_consistency",
                "ghost_follower_penalty",
                "competitor_data_validation",
                "phase_enforcement",
                "specificity_enforcement",
                "deduplication_loop_prevention",
                "hallucination_containment",
                "tone_language_standard",
                "dashboard_data_sync",
                "benchmark_commentary_sync",
                "logic_override_protocol",
                "estimation_fallback_logic",
                "context_awareness_fix",
                "section_specific_constraints",
                "advanced_analytics_modules",
                "output_sanitization",
                "tagging_precision",
                "action_plan_cleanup"
            ],
            "corrections_made": len(corrections),
            "corrections": corrections,
            "warnings": warnings,
            "advanced_analytics": advanced_analytics,
            "strategic_phase": phase_info,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Sanity gates applied: {len(corrections)} corrections, {len(warnings)} warnings")
        return agent_results, gate_report

    def _to_number(self, value: Any) -> Optional[float]:
        """Safely cast value to float."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            v = value.strip().replace('%', '').replace(',', '.')
            if v in ("", "null", "None", "N/A", "Insufficient Data"):
                return None
            try:
                return float(v)
            except ValueError:
                return None
        return None

    def _apply_mathematical_immutability(
        self,
        results: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[str]]:
        """
        Enforce immutable core formulas and missing-data handling.
        """
        corrections: List[Dict[str, Any]] = []
        warnings: List[str] = []

        followers = self._to_number(account_data.get("followers"))
        following = self._to_number(account_data.get("following"))
        avg_likes = self._to_number(account_data.get("avgLikes")) or 0.0
        avg_comments = self._to_number(account_data.get("avgComments")) or 0.0
        total_posts = self._to_number(account_data.get("posts")) or 0.0

        # ── DATA_SANITY_PROTOCOL ───────────────────────────────────────────────
        # IF followers > 10,000 AND avg_likes < 10 → almost certainly a parse error.
        # Attempt to recalculate from engagement_rate; otherwise mark 'Veri hesaplanamadı'.
        if followers is not None and followers > 10_000 and avg_likes < 10:
            eng_rate_raw = self._to_number(
                account_data.get("engagementRate") or account_data.get("engagement_rate")
            )
            if eng_rate_raw is not None and eng_rate_raw > 0 and followers > 0:
                # avg_likes ≈ (followers * engagement_rate) / 100
                recalc_avg_likes = (followers * eng_rate_raw) / 100
                avg_likes = recalc_avg_likes
                account_data = dict(account_data)  # avoid mutating caller's dict
                account_data["avgLikes"] = round(recalc_avg_likes, 2)
                corrections.append({
                    "gate": "data_sanity_protocol",
                    "field": "avgLikes",
                    "action": "recalculated_from_engagement_rate",
                    "new_value": round(recalc_avg_likes, 2),
                    "reason": (
                        f"DATA_PARSING_ERROR detected: followers={followers}, "
                        f"avgLikes<10 — recalculated from engagementRate={eng_rate_raw}"
                    ),
                })
            else:
                # Engagement rate also unavailable — mark as uncalculable
                account_data = dict(account_data)
                account_data["avgLikes"] = "Veri hesaplanamadı"
                avg_likes = 0.0  # keep downstream arithmetic safe
                corrections.append({
                    "gate": "data_sanity_protocol",
                    "field": "avgLikes",
                    "action": "set_veri_hesaplanamadi",
                    "reason": (
                        f"DATA_PARSING_ERROR detected: followers={followers}, "
                        "avgLikes<10 AND engagementRate unavailable"
                    ),
                })
                warnings.append(
                    "DATA_SANITY_PROTOCOL: avgLikes suspiciously low for large account; "
                    "engagementRate also missing — printed 'Veri hesaplanamadı'"
                )
        # ─────────────────────────────────────────────────────────────────────

        ratio = None
        if following and following > 0 and followers is not None:
            ratio = followers / following

        engagement_rate = None
        if followers and followers > 0:
            engagement_rate = ((avg_likes + avg_comments) / followers) * 100

        # Write canonical outputs to systemGovernor metrics for downstream consistency
        if "systemGovernor" in results and not results["systemGovernor"].get("error_flag"):
            sg_metrics = results["systemGovernor"].setdefault("metrics", {})
            sg_metrics["followerFollowingRatio"] = round(ratio, 4) if ratio is not None else "Insufficient Data"
            sg_metrics["engagementRate"] = round(engagement_rate, 4) if engagement_rate is not None else "Insufficient Data"

        # Net growth cannot be calculated without churn rate
        growth = results.get("growthVirality", {})
        if growth and not growth.get("error_flag"):
            g_metrics = growth.setdefault("metrics", {})
            net_growth = g_metrics.get("netGrowth") or g_metrics.get("netGrowthRate")
            churn_rate = g_metrics.get("churnRate") or g_metrics.get("churn_rate")

            if net_growth is not None and self._to_number(churn_rate) is None:
                if "netGrowth" in g_metrics:
                    g_metrics["netGrowth"] = "Insufficient Data"
                if "netGrowthRate" in g_metrics:
                    g_metrics["netGrowthRate"] = "Insufficient Data"
                corrections.append({
                    "gate": "mathematical_immutability",
                    "field": "netGrowth",
                    "action": "set_insufficient_data",
                    "reason": "Churn rate is null; net growth cannot be computed reliably"
                })

            # If posts exist, all-zero format distribution is invalid
            format_keys = ["reelsShare", "carouselShare", "imageShare", "reelsPercent", "carouselPercent", "imagePercent"]
            found_values = [self._to_number(g_metrics.get(k)) for k in format_keys if k in g_metrics]
            if total_posts > 0 and found_values and all((v is None or v == 0) for v in found_values):
                for k in format_keys:
                    if k in g_metrics:
                        g_metrics[k] = "Hesaplanamadı"
                warnings.append(
                    "Content Format Distribution invalid: posts exist but Reels/Carousel/Image distribution is all zero"
                )
                corrections.append({
                    "gate": "mathematical_immutability",
                    "field": "content_format_distribution",
                    "action": "set_hesaplanamadi",
                    "reason": "Posts exist but format distribution values are all zero"
                })

        return results, corrections, warnings

    def _apply_logic_synchronization_lock(
        self,
        results: Dict[str, Any],
        metrics: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[str]]:
        """
        Ensure micro-metrics and macro status are logically aligned.
        """
        corrections: List[Dict[str, Any]] = []
        warnings: List[str] = []

        # Rule: Critical engagement cannot coexist with high overall health
        engagement_rate = self._to_number(metrics.get("engagement_rate"))
        if engagement_rate is None:
            engagement_rate = self._to_number(account_data.get("engagementRate"))

        if engagement_rate is not None and engagement_rate < 0.5:
            sg = results.get("systemGovernor", {})
            if sg and not sg.get("error_flag"):
                sg_metrics = sg.setdefault("metrics", {})
                current_health = self._to_number(sg_metrics.get("overallHealthScore") or sg_metrics.get("overallScore"))
                if current_health is not None and current_health > 69:
                    capped = 55.0
                    sg_metrics["overallHealthScore"] = capped
                    sg_metrics["overallHealthGrade"] = "D"
                    corrections.append({
                        "gate": "logic_synchronization",
                        "field": "overallHealthScore",
                        "old": current_health,
                        "new": capped,
                        "reason": f"Engagement rate is critical ({engagement_rate:.2f}%)"
                    })

        # Rule: passive follower ratio > 90% => community health capped at 50
        community = results.get("communityLoyalty", {})
        if community and not community.get("error_flag"):
            insights = community.get("communityInsights", {}) or {}
            passive = self._to_number(insights.get("passiveFollowers")) or 0.0
            superfans = self._to_number(insights.get("estimatedSuperfans")) or 0.0
            active = self._to_number(insights.get("activeEngagers")) or 0.0
            ghost = self._to_number(insights.get("ghostFollowers")) or 0.0
            total = passive + superfans + active + ghost

            if total > 0:
                passive_ratio = (passive / total) * 100
                if passive_ratio > 90:
                    c_metrics = community.setdefault("metrics", {})
                    health_key = "communityHealthScore"
                    current_ch = self._to_number(c_metrics.get(health_key))
                    if current_ch is not None and current_ch > 50:
                        c_metrics[health_key] = 50
                        corrections.append({
                            "gate": "logic_synchronization",
                            "field": health_key,
                            "old": current_ch,
                            "new": 50,
                            "reason": f"Passive follower ratio is {passive_ratio:.1f}% (>90%)"
                        })

        # Rule: bot-risk conflict should be flagged and lower-confidence signal suppressed
        sg = results.get("systemGovernor", {})
        sg_risk = None
        if sg and not sg.get("error_flag"):
            sg_risk = (sg.get("metrics", {}) or {}).get("botRiskLevel")

        external_bot_score = self._to_number(account_data.get("botScore"))
        external_risk = None
        if external_bot_score is not None:
            if external_bot_score > 60:
                external_risk = "high"
            elif external_bot_score > 30:
                external_risk = "medium"
            else:
                external_risk = "low"

        if sg_risk and external_risk and sg_risk != external_risk:
            warnings.append(
                f"INTEGRITY CONFLICT: bot risk mismatch (systemGovernor={sg_risk}, account.botScore={external_risk})"
            )
            audience = results.get("audienceDynamics", {})
            if audience and not audience.get("error_flag"):
                audience["_suppressed_by_integrity_conflict"] = True
                if "botDetectionScore" in audience:
                    audience.pop("botDetectionScore", None)

        # LOGIC_SYNCHRONIZATION_LAYER: Dashboard Score > 75 → enforce positive language
        sg_data = results.get("systemGovernor", {})
        dashboard_score_sync = None
        if sg_data and not sg_data.get("error_flag"):
            sg_m = sg_data.get("metrics", {}) or {}
            dashboard_score_sync = self._to_number(
                sg_m.get("overallHealthScore") or sg_m.get("overallScore")
            )
        if dashboard_score_sync is None:
            dashboard_score_sync = metrics.get("overall_health")

        if dashboard_score_sync is not None and dashboard_score_sync > 75:
            # Negative/neutral adjectives that contradict a high-score dashboard
            positive_rewrites: List[Tuple[re.Pattern, str]] = [
                (re.compile(r"\b(struggling|poor performance|weak performance)\b", re.IGNORECASE), "high-performing"),
                (re.compile(r"\bpoor engagement\b", re.IGNORECASE), "High Engagement"),
                (re.compile(r"\bweak engagement\b", re.IGNORECASE), "Strong Engagement"),
                (re.compile(r"\b(low performance|underperform\w*)\b", re.IGNORECASE), "High Performance"),
                (re.compile(r"\b(düşük performans|zayıf performans)\b", re.IGNORECASE), "Güçlü Performans"),
                (re.compile(r"\b(at risk|risk at\w*)\b", re.IGNORECASE), "with optimization opportunity"),
            ]

            positive_fields = {
                "verdict", "summary", "commentary", "analysis",
                "situation", "overview", "conclusion"
            }

            def enforce_positive(obj: Any) -> Any:
                if isinstance(obj, str):
                    result_text = obj
                    for pattern, replacement in positive_rewrites:
                        result_text = pattern.sub(replacement, result_text)
                    return result_text
                if isinstance(obj, list):
                    return [enforce_positive(v) for v in obj]
                if isinstance(obj, dict):
                    out = {}
                    for k, v in obj.items():
                        if k.lower() in positive_fields:
                            out[k] = enforce_positive(v)
                        else:
                            out[k] = v
                    return out
                return obj

            for agent_name, agent_result in results.items():
                if isinstance(agent_result, dict) and not agent_result.get("error_flag"):
                    results[agent_name] = enforce_positive(agent_result)

            corrections.append({
                "gate": "logic_synchronization",
                "field": "textual_commentary",
                "action": "positive_language_enforced",
                "reason": f"Dashboard score={dashboard_score_sync:.0f} > 75; negative language rewritten"
            })

        return results, corrections, warnings

    def _extract_text(self, item: Any) -> str:
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            for key in ("finding", "recommendation", "action", "description", "issue", "text", "label"):
                if item.get(key):
                    return str(item.get(key))
        return str(item)

    def _apply_deduplication_loop_prevention(
        self,
        results: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        Remove repeated strategy loops and force cross-references.
        """
        warnings: List[str] = []
        seen_global_actions: set = set()
        used_strategies: set = set()

        def normalize(text: str) -> str:
            return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", text.lower())).strip()

        def detect_strategy(text: str) -> Optional[str]:
            low = text.lower()
            for s in self.strategy_library:
                if s.lower() in low:
                    return s
            return None

        def next_available_strategy(exclude: Optional[str] = None) -> Optional[str]:
            for s in self.strategy_library:
                if s != exclude and s not in used_strategies:
                    return s
            return None

        for agent_name, agent_result in results.items():
            if agent_result.get("error_flag"):
                continue

            recommendations = agent_result.get("recommendations", [])
            if isinstance(recommendations, list) and recommendations:
                deduped = []
                for rec in recommendations:
                    text = self._extract_text(rec)
                    norm = normalize(text)
                    if not norm:
                        continue

                    strategy = detect_strategy(text)
                    if strategy:
                        if strategy in used_strategies:
                            alternative = next_available_strategy(exclude=strategy)
                            if alternative:
                                rec = {
                                    "recommendation": f"Strateji çeşitliliği için '{alternative}' yaklaşımını uygulayın.",
                                    "strategy_diversity_applied": True,
                                }
                                text = self._extract_text(rec)
                                norm = normalize(text)
                                warnings.append(f"Strategy diversity enforced in {agent_name}: {strategy} -> {alternative}")
                                used_strategies.add(alternative)
                            else:
                                warnings.append(f"No available alternative strategy left for {agent_name}")
                        else:
                            used_strategies.add(strategy)

                    if norm in seen_global_actions:
                        cross_ref = "(Bkz: Büyüme Stratejileri Bölümü - Comment Magnet Detayı)"
                        if "comment magnet" not in norm:
                            cross_ref = "(Bkz: Büyüme Stratejileri Bölümü - İlgili Strateji Detayı)"
                        deduped.append({
                            "recommendation": cross_ref,
                            "cross_reference": True
                        })
                        warnings.append(f"Deduplicated repetitive recommendation in {agent_name}")
                    else:
                        seen_global_actions.add(norm)
                        deduped.append(rec)
                agent_result["recommendations"] = deduped

        return results, warnings

    def _apply_data_sync_with_dashboard(
        self,
        results: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Ensure textual bot-risk statement syncs with dashboard metrics source."""
        warnings: List[str] = []

        dashboard_bot = self._to_number(account_data.get("botScore"))
        if dashboard_bot is None:
            return results, warnings

        if dashboard_bot >= 80:
            expected_level = "Yüksek Risk"
        elif dashboard_bot >= 50:
            expected_level = "Orta Risk"
        else:
            expected_level = "Düşük Risk"

        governor = results.get("systemGovernor", {})
        if governor and not governor.get("error_flag"):
            findings = governor.get("findings", [])
            if not isinstance(findings, list):
                findings = []

            # Remove contradictory direct text snippets
            synced = []
            for f in findings:
                text = self._extract_text(f)
                low = text.lower()
                if expected_level == "Yüksek Risk" and ("düşük risk" in low or "low risk" in low):
                    continue
                synced.append(f)

            synced.insert(0, f"Dashboard senkronizasyonu: Bot Risk seviyesi {expected_level} olarak doğrulandı.")
            governor["findings"] = synced
            warnings.append(f"Data sync applied: dashboard bot risk => {expected_level}")

        return results, warnings

    def _benchmark_state(self, results: Dict[str, Any], metrics: Dict[str, Any], account_data: Dict[str, Any]) -> str:
        """Classify engagement state against benchmark for text synchronization."""
        engagement_rate = self._to_number(metrics.get("engagement_rate"))
        if engagement_rate is None:
            engagement_rate = self._to_number(account_data.get("engagementRate"))

        benchmark = self._to_number(account_data.get("benchmark_engagement"))
        if benchmark is None:
            benchmark = self._to_number(account_data.get("industryBenchmarkEngagement"))

        domain = results.get("domainMaster", {})
        if benchmark is None and isinstance(domain, dict) and not domain.get("error_flag"):
            benchmark = self._to_number((domain.get("niche_identification", {}) or {}).get("benchmark_engagement"))
            if benchmark is None:
                benchmark = self._to_number((domain.get("metrics", {}) or {}).get("benchmarkEngagement"))

        if engagement_rate is not None and benchmark is not None and benchmark > 0:
            return "above_average" if engagement_rate >= benchmark else "below_average"

        comp_verdict = (((results.get("systemGovernor", {}) or {}).get("advancedAnalytics", {}) or {})
                        .get("competitive_benchmark", {})
                        .get("engagement_rate", {})
                        .get("verdict"))
        if isinstance(comp_verdict, str):
            low = comp_verdict.lower()
            if low == "win":
                return "above_average"
            if low == "loss":
                return "below_average"

        return "insufficient"

    def _sync_claim_text(self, text: str, benchmark_state: str) -> str:
        """Normalize contradictory engagement claims according to benchmark state."""
        if not isinstance(text, str):
            return text

        synced = text
        if benchmark_state == "above_average":
            synced = re.sub(r"\blow engagement\b", "good performance", synced, flags=re.IGNORECASE)
            synced = re.sub(r"\bbelow average engagement\b", "above average engagement", synced, flags=re.IGNORECASE)
            synced = re.sub(r"\bzayıf etkileşim\b", "iyi performans", synced, flags=re.IGNORECASE)
            synced = re.sub(r"\bdüşük etkileşim\b", "iyi performans", synced, flags=re.IGNORECASE)
        elif benchmark_state == "below_average":
            synced = re.sub(r"\bhigh engagement\b", "developing engagement", synced, flags=re.IGNORECASE)
            synced = re.sub(r"\bstrong performance\b", "geliştirme fırsatı", synced, flags=re.IGNORECASE)
            synced = re.sub(r"\bgood performance\b", "geliştirme fırsatı", synced, flags=re.IGNORECASE)
            synced = re.sub(r"\byüksek etkileşim\b", "gelişmekte olan etkileşim", synced, flags=re.IGNORECASE)
            synced = re.sub(r"\bçok iyi performans\b", "geliştirme fırsatı", synced, flags=re.IGNORECASE)

        return synced

    def _apply_benchmark_commentary_sync(
        self,
        results: Dict[str, Any],
        metrics: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Force engagement commentary to follow dashboard benchmark mathematics."""
        warnings: List[str] = []
        state = self._benchmark_state(results, metrics, account_data)

        if state == "insufficient":
            return results, warnings

        updated_fields = 0

        def sync_obj(obj: Any) -> Any:
            nonlocal updated_fields
            if isinstance(obj, str):
                synced = self._sync_claim_text(obj, state)
                if synced != obj:
                    updated_fields += 1
                return synced
            if isinstance(obj, list):
                return [sync_obj(v) for v in obj]
            if isinstance(obj, dict):
                out = {}
                for k, v in obj.items():
                    if k in {"findings", "recommendations", "verdict", "situation", "summary", "commentary", "analysis"}:
                        out[k] = sync_obj(v)
                    else:
                        out[k] = v
                return out
            return obj

        for agent_name, agent_result in results.items():
            if isinstance(agent_result, dict) and not agent_result.get("error_flag"):
                results[agent_name] = sync_obj(agent_result)

        if updated_fields > 0:
            human_state = "Above Average" if state == "above_average" else "Below Average"
            warnings.append(f"Benchmark commentary sync applied ({human_state}): {updated_fields} text field(s) normalized")

        return results, warnings

    def _extract_detected_niche(self, results: Dict[str, Any], account_data: Dict[str, Any]) -> str:
        """Best-effort niche extraction across pipeline outputs."""
        candidates: List[Any] = [
            account_data.get("niche"),
            account_data.get("accountNiche"),
            account_data.get("detectedNiche"),
            results.get("detectedNiche"),
            ((results.get("domainMaster", {}) or {}).get("niche_identification", {}) or {}).get("primary_niche"),
            ((results.get("domainMaster", {}) or {}).get("niche_identification", {}) or {}).get("detected_niche"),
            (((results.get("crossAgentInsights", {}) or {}).get("domainMaster", {}) or {}).get("detectedNiche")),
        ]
        for c in candidates:
            if isinstance(c, str) and c.strip():
                return c.strip()
        return ""

    def _extract_sub_niche(self, results: Dict[str, Any], account_data: Dict[str, Any]) -> str:
        """Best-effort sub-niche extraction across pipeline outputs."""
        domain_niche = (results.get("domainMaster", {}) or {}).get("niche_identification", {}) or {}
        candidates: List[Any] = [
            account_data.get("sub_niche"),
            account_data.get("subNiche"),
            account_data.get("micro_niche"),
            account_data.get("microNiche"),
            domain_niche.get("sub_niche"),
            domain_niche.get("micro_niche"),
            domain_niche.get("secondary_niche"),
            domain_niche.get("secondaryNiche"),
            results.get("sub_niche"),
            results.get("micro_niche"),
        ]
        for c in candidates:
            if isinstance(c, str) and c.strip():
                return c.strip()
        return ""

    def _apply_estimation_fallback_gate(
        self,
        results: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        ESTIMATION_FALLBACK_LOGIC:
        brandDealRateMin/Max sıfır veya null ise
        followers + engagement_rate üzerinden tahmini sektör aralığı hesaplar.
        Formula: base = (followers / 1000) * (engagement_rate * coeff)
        coeff: eng < 1% → 0.5 | 1-3% → 1.0 | 3-5% → 1.3 | >5% → 1.6
        """
        warnings: List[str] = []
        sc = results.get("salesConversion", {})
        if not sc or sc.get("error_flag"):
            return results, warnings

        metrics = sc.get("metrics", {})
        if not isinstance(metrics, dict):
            return results, warnings

        rate_min = self._to_number(metrics.get("brandDealRateMin"))
        rate_max = self._to_number(metrics.get("brandDealRateMax"))

        if (rate_min is None or rate_min == 0) and (rate_max is None or rate_max == 0):
            followers = self._to_number(account_data.get("followers")) or 0
            eng_rate = (
                self._to_number(account_data.get("engagementRate"))
                or self._to_number(account_data.get("engagement_rate"))
                or 0
            )
            if followers > 0:
                coeff = 0.5
                if eng_rate >= 5:
                    coeff = 1.6
                elif eng_rate >= 3:
                    coeff = 1.3
                elif eng_rate >= 1:
                    coeff = 1.0

                base = (followers / 1000) * (eng_rate * coeff)
                est_min = round(base * 0.7, 2)
                est_max = round(base * 1.5, 2)

                # Sıfır tahmini gösterme — minimum sektör eşiği uygula
                if est_min == 0:
                    est_min = round(followers / 10000, 2)
                if est_max == 0:
                    est_max = round(followers / 5000, 2)

                metrics["brandDealRateMin"] = est_min
                metrics["brandDealRateMax"] = est_max
                metrics["brandDealRateIsEstimate"] = True
                metrics["brandDealRateNote"] = (
                    f"Tahmini Sektör Aralığı: ${est_min:.0f} - ${est_max:.0f} "
                    f"(Kesin veri oluşana kadar bu aralık referans alınmıştır)."
                )
                results["salesConversion"]["metrics"] = metrics
                warnings.append(
                    f"Estimation fallback: brand deal rate calculated from "
                    f"followers={followers}, engagement={eng_rate}% → ${est_min:.0f}-${est_max:.0f}"
                )

        return results, warnings

    def _apply_context_awareness_fix(
        self,
        results: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Prevent niche-irrelevant recommendations with niche/sub-niche specific constraints."""
        warnings: List[str] = []

        niche_raw = self._extract_detected_niche(results, account_data)
        sub_niche_raw = self._extract_sub_niche(results, account_data)
        niche = niche_raw.lower()
        sub_niche = sub_niche_raw.lower()

        is_fitness = "fitness" in niche

        # ── Spirituality sub-niche ──────────────────────────────────────────
        is_spirituality_sub_niche = (
            any(token in niche for token in ["health", "wellness", "sağlık"]) and
            any(token in sub_niche for token in ["spiritual", "spirituality", "crystal", "kristal", "energy", "enerji"])
        )

        forbidden_tokens = self.context_integrity["spirituality_forbidden"]
        forced_tokens = self.context_integrity["spirituality_forced"]
        forbidden_re = re.compile(
            r"\b(" + "|".join(re.escape(t) for t in forbidden_tokens) + r")\b",
            re.IGNORECASE,
        )
        forced_hint = "Meditation, energy, healing ve günlük routine odaklı içerik önerileri kullanın."
        sub_niche_context_applied = 0

        def apply_sub_niche_context(text: str) -> str:
            nonlocal sub_niche_context_applied
            if not isinstance(text, str) or not text.strip():
                return text
            if not is_spirituality_sub_niche or is_fitness:
                return text

            cleaned = text
            had_forbidden = bool(forbidden_re.search(cleaned))
            if had_forbidden:
                cleaned = forbidden_re.sub("", cleaned)
                cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" ,.-")

            low = cleaned.lower()
            has_forced = any(t in low for t in forced_tokens)

            if had_forbidden or not has_forced:
                if cleaned and not cleaned.endswith((".", "!", "?")):
                    cleaned += "."
                cleaned = f"{cleaned} {forced_hint}".strip()
                sub_niche_context_applied += 1

            return cleaned

        # ── Travel / City Guide niche guardrail ────────────────────────────
        is_travel = any(
            token in niche or token in sub_niche
            for token in ["travel", "seyahat", "city guide", "şehir rehberi", "tourism", "turizm", "kahramanmaraş"]
        )
        travel_forbidden_tokens = self.context_integrity["travel_forbidden"]
        travel_forbidden_re = re.compile(
            r"\b(" + "|".join(re.escape(t) for t in travel_forbidden_tokens) + r")\b",
            re.IGNORECASE,
        )
        travel_hint = self.context_integrity["travel_forced_hint"]
        travel_context_applied = 0

        def apply_travel_context(text: str) -> str:
            nonlocal travel_context_applied
            if not isinstance(text, str) or not text.strip() or not is_travel:
                return text

            had_forbidden = bool(travel_forbidden_re.search(text))
            cleaned = text
            if had_forbidden:
                cleaned = travel_forbidden_re.sub("", cleaned)
                cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" ,.-")

            low = cleaned.lower()
            has_travel_kw = any(
                kw in low for kw in ["hidden gems", "local food", "travel hack", "yerel yemek",
                                      "gizli mekân", "seyahat ipucu", "kahramanmaraş"]
            )
            if had_forbidden or not has_travel_kw:
                if cleaned and not cleaned.endswith((".", "!", "?")):
                    cleaned += "."
                cleaned = f"{cleaned} {travel_hint}".strip()
                travel_context_applied += 1

            return cleaned

        # ── Football niche ─────────────────────────────────────────────────
        is_football = any(token in niche for token in ["football", "soccer", "futbol", "kulüp", "club"])
        conflict_re = re.compile(r"home\s*fitness|workout|gym\s*tips|meal\s*plan|diyet|evde\s*antrenman", re.IGNORECASE)
        football_replacement = (
            "Niş uyumlu öneri: Match Day analizi, oyuncu röportajı kısa klipleri, "
            "antrenman arkası sahne içerikleri ve taraftar etkileşim anketleri üretin."
        )

        # ── Retro / Vintage / Nostalgia niche guardrail ────────────────────
        is_retro = any(
            token in niche or token in sub_niche
            for token in ["retro", "vintage", "nostalgia", "nostalji", "klasik", "classic"]
        )
        retro_forbidden_tokens = self.context_integrity["retro_forbidden"]
        retro_forbidden_re = re.compile(
            r"\b(" + "|".join(re.escape(t) for t in retro_forbidden_tokens) + r")\b",
            re.IGNORECASE,
        )
        retro_forced_tokens = self.context_integrity["retro_forced"]
        retro_hint = self.context_integrity["retro_forced_hint"]
        retro_context_applied = 0

        def apply_retro_context(text: str) -> str:
            nonlocal retro_context_applied
            if not isinstance(text, str) or not text.strip() or not is_retro:
                return text

            had_forbidden = bool(retro_forbidden_re.search(text))
            cleaned = text
            if had_forbidden:
                cleaned = retro_forbidden_re.sub("", cleaned)
                cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" ,.-")

            low = cleaned.lower()
            has_retro_kw = any(kw in low for kw in retro_forced_tokens)
            if had_forbidden or not has_retro_kw:
                if cleaned and not cleaned.endswith((".", "!", "?")):
                    cleaned += "."
                cleaned = f"{cleaned} {retro_hint}".strip()
                retro_context_applied += 1

            return cleaned

        # ── Fashion / Clothing / Style niche guardrail ─────────────────────
        is_fashion = any(
            token in niche or token in sub_niche
            for token in ["fashion", "clothing", "style", "moda", "giyim", "kıyafet", "stil"]
        )
        fashion_forbidden_tokens = self.context_integrity["fashion_forbidden"]
        fashion_forbidden_re = re.compile(
            r"\b(" + "|".join(re.escape(t) for t in fashion_forbidden_tokens) + r")\b",
            re.IGNORECASE,
        )
        fashion_forced_tokens = self.context_integrity["fashion_forced"]
        fashion_hint = self.context_integrity["fashion_forced_hint"]
        fashion_context_applied = 0

        def apply_fashion_context(text: str) -> str:
            nonlocal fashion_context_applied
            if not isinstance(text, str) or not text.strip() or not is_fashion:
                return text

            had_forbidden = bool(fashion_forbidden_re.search(text))
            cleaned = text
            if had_forbidden:
                cleaned = fashion_forbidden_re.sub("", cleaned)
                cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" ,.-")

            low = cleaned.lower()
            has_fashion_kw = any(kw in low for kw in fashion_forced_tokens)
            if had_forbidden or not has_fashion_kw:
                if cleaned and not cleaned.endswith((".", "!", "?")):
                    cleaned += "."
                cleaned = f"{cleaned} {fashion_hint}".strip()
                fashion_context_applied += 1

            return cleaned

        # ── Food / Cooking niche guardrail ─────────────────────────────────
        is_food = any(
            token in niche or token in sub_niche
            for token in ["food", "cooking", "yemek", "mutfak", "cuisine", "recipe", "gastronomy", "gastronomi"]
        )
        food_forced_tokens = self.context_integrity["food_forced"]
        food_hint = self.context_integrity["food_forced_hint"]
        food_context_applied = 0

        def apply_food_context(text: str) -> str:
            nonlocal food_context_applied
            if not isinstance(text, str) or not text.strip() or not is_food:
                return text

            low = text.lower()
            has_food_kw = any(kw in low for kw in food_forced_tokens)
            if not has_food_kw:
                cleaned = text
                if cleaned and not cleaned.endswith((".", "!", "?")):
                    cleaned += "."
                cleaned = f"{cleaned} {food_hint}".strip()
                food_context_applied += 1
                return cleaned
            return text

        # ── Local Business niche guardrail ─────────────────────────────────────
        is_local_business = any(
            token in niche or token in sub_niche
            for token in [
                "local business", "local", "yerel işletme", "yerel",
                "shop", "store", "restaurant", "cafe", "restoran",
                "kafe", "dükkan", "mağaza"
            ]
        )
        local_business_forced_tokens = self.context_integrity.get("local_business_forced", [])
        local_business_hint = self.context_integrity.get(
            "local_business_forced_hint",
            "Yerel işletme nişi için: Location tag, 'Bizi ziyaret edin', yerel etkinlikler ve müşteri buluşması odaklı içerik önerileri kullanın."
        )
        local_business_context_applied = 0

        def apply_local_business_context(text: str) -> str:
            nonlocal local_business_context_applied
            if not isinstance(text, str) or not text.strip() or not is_local_business:
                return text
            low = text.lower()
            has_local_kw = any(kw in low for kw in local_business_forced_tokens)
            if not has_local_kw:
                cleaned = text
                if cleaned and not cleaned.endswith((".", "!", "?")):
                    cleaned += "."
                cleaned = f"{cleaned} {local_business_hint}".strip()
                local_business_context_applied += 1
                return cleaned
            return text

        fixed = 0

        def rewrite(obj: Any) -> Any:
            nonlocal fixed
            if isinstance(obj, str):
                updated = apply_sub_niche_context(obj)
                updated = apply_travel_context(updated)
                updated = apply_retro_context(updated)
                updated = apply_fashion_context(updated)
                updated = apply_food_context(updated)
                updated = apply_local_business_context(updated)
                if is_football and conflict_re.search(updated):
                    fixed += 1
                    return football_replacement
                return updated
            if isinstance(obj, list):
                return [rewrite(v) for v in obj]
            if isinstance(obj, dict):
                out = {}
                for k, v in obj.items():
                    if k in {"findings", "recommendations", "action", "recommendation",
                             "finding", "issue", "template", "caption", "script",
                             "suggestion", "advice", "strategy"}:
                        out[k] = rewrite(v)
                    else:
                        out[k] = v
                return out
            return obj

        for agent_name, agent_result in results.items():
            if isinstance(agent_result, dict) and not agent_result.get("error_flag"):
                results[agent_name] = rewrite(agent_result)

        if fixed > 0:
            warnings.append(f"Context awareness fix applied for football niche: {fixed} irrelevant item(s) replaced")
        if sub_niche_context_applied > 0:
            warnings.append(
                f"Context integrity protocol applied ({niche_raw}/{sub_niche_raw}): "
                f"{sub_niche_context_applied} recommendation text(s) aligned"
            )
        if travel_context_applied > 0:
            warnings.append(
                f"Travel/City Guide guardrail applied ({niche_raw}): "
                f"{travel_context_applied} tech-irrelevant item(s) redirected to travel content"
            )
        if retro_context_applied > 0:
            warnings.append(
                f"Retro/Vintage guardrail applied ({niche_raw}): "
                f"{retro_context_applied} modern-tech item(s) replaced with retro-aligned content"
            )
        if fashion_context_applied > 0:
            warnings.append(
                f"Fashion/Clothing/Style guardrail applied ({niche_raw}): "
                f"{fashion_context_applied} tech-irrelevant item(s) replaced with fashion-aligned content"
            )
        if food_context_applied > 0:
            warnings.append(
                f"Food/Cooking guardrail applied ({niche_raw}): "
                f"{food_context_applied} item(s) enriched with recipe/kitchen-oriented hints"
            )
        if local_business_context_applied > 0:
            warnings.append(
                f"Local Business guardrail applied ({niche_raw}): "
                f"{local_business_context_applied} item(s) enriched with location/event-oriented hints"
            )

        return results, warnings

    def _apply_logic_override_protocol(
        self,
        results: Dict[str, Any],
        metrics: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        LOGIC_OVERRIDE_PROTOCOL:
        - IF engagement_rate > 5% → replace 'Low Engagement' with 'High Engagement but Unoptimized'
        - IF dashboard_score > 80 → redirect engagement criticism to Growth focus
        """
        warnings: List[str] = []

        # ── 1. Resolve engagement rate ─────────────────────────────────────
        engagement_rate = self._to_number(metrics.get("engagement_rate"))
        if engagement_rate is None:
            followers = self._to_number(account_data.get("followers"))
            avg_likes = self._to_number(account_data.get("avgLikes")) or 0.0
            avg_comments = self._to_number(account_data.get("avgComments")) or 0.0
            if followers and followers > 0:
                engagement_rate = ((avg_likes + avg_comments) / followers) * 100

        high_engagement = (
            engagement_rate is not None
            and engagement_rate > self.logic_override["engagement_high_threshold"]
        )

        # ── 2. Resolve dashboard / overall health score ────────────────────
        sg = results.get("systemGovernor", {})
        dashboard_score = None
        if sg and not sg.get("error_flag"):
            sg_m = sg.get("metrics", {})
            dashboard_score = self._to_number(
                sg_m.get("overallHealthScore") or sg_m.get("overallScore")
            )
        if dashboard_score is None:
            dashboard_score = metrics.get("overall_health")

        high_dashboard = (
            dashboard_score is not None
            and dashboard_score > self.logic_override["dashboard_score_growth_threshold"]
        )

        if not high_engagement and not high_dashboard:
            return results, warnings

        # ── 3. Build replacement regexes ───────────────────────────────────
        low_eng_re = re.compile(
            r"\b(low\s+engagement|düşük\s+etkileşim|etkileşim\s+düşük|engagement\s+sorunu|"
            r"engagement\s+is\s+low|poor\s+engagement)\b",
            re.IGNORECASE,
        )
        high_eng_label = "High Engagement but Unoptimized"

        # Patterns that criticise engagement (used when dashboard_score > 80)
        eng_criticism_re = re.compile(
            r"\b(artır\s+etkileşim|improve\s+your\s+engagement|boost\s+engagement|"
            r"focus\s+on\s+engagement|etkileşim\s+odakl[ıi]|engagement-focused)\b",
            re.IGNORECASE,
        )
        growth_redirect = "Growth ve içerik optimizasyonuna odaklanın"

        lo_fixed = 0
        dash_fixed = 0

        def override_text(text: str) -> str:
            nonlocal lo_fixed, dash_fixed
            if not isinstance(text, str):
                return text
            updated = text
            if high_engagement and low_eng_re.search(updated):
                updated = low_eng_re.sub(high_eng_label, updated)
                lo_fixed += 1
            if high_dashboard and eng_criticism_re.search(updated):
                updated = eng_criticism_re.sub(growth_redirect, updated)
                dash_fixed += 1
            return updated

        def override_obj(obj: Any) -> Any:
            if isinstance(obj, str):
                return override_text(obj)
            if isinstance(obj, list):
                return [override_obj(v) for v in obj]
            if isinstance(obj, dict):
                out = {}
                for k, v in obj.items():
                    if k in {"findings", "recommendations", "action", "recommendation",
                             "finding", "issue", "summary", "verdict", "commentary",
                             "analysis", "suggestion", "strategy", "advice"}:
                        out[k] = override_obj(v)
                    else:
                        out[k] = v
                return out
            return obj

        for agent_name, agent_result in results.items():
            if isinstance(agent_result, dict) and not agent_result.get("error_flag"):
                results[agent_name] = override_obj(agent_result)

        if lo_fixed > 0:
            warnings.append(
                f"Logic Override: engagement_rate={engagement_rate:.2f}% > 5% — "
                f"'Low Engagement' replaced with 'High Engagement but Unoptimized' "
                f"in {lo_fixed} field(s)"
            )
        if dash_fixed > 0:
            warnings.append(
                f"Logic Override: dashboard_score={dashboard_score:.0f} > 80 — "
                f"engagement criticism redirected to Growth in {dash_fixed} field(s)"
            )

        return results, warnings

    def _apply_tagging_precision(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        TAGGING_PRECISION gate:
        Auto-assign category tags based on action/recommendation text.
        hashtag/reach → 'Visibility' | content/reel → 'Content' | money/monetiz → 'Monetization'
        Never emit bare 'General Strategy'.
        """

        def infer_tag(text: str) -> Optional[str]:
            if not isinstance(text, str) or not text.strip():
                return None
            lower = text.lower()
            for tag, keywords in self.tag_keyword_map.items():
                if any(kw in lower for kw in keywords):
                    return tag
            return None

        def tag_obj(obj: Any) -> Any:
            if isinstance(obj, dict):
                cat = obj.get("category", "")
                # Sanitise bare 'General Strategy' placeholder
                if isinstance(cat, str) and cat.strip().lower() in {
                    "general strategy", "general", "genel strateji", "genel", ""
                }:
                    # Try to infer from action/recommendation text
                    text_for_inference = (
                        obj.get("action") or obj.get("recommendation") or
                        obj.get("finding") or obj.get("strategy") or ""
                    )
                    inferred = infer_tag(str(text_for_inference))
                    if inferred:
                        obj = dict(obj)
                        obj["category"] = inferred
                # Recurse into sub-fields
                out = {}
                for k, v in obj.items():
                    if k in {"recommendations", "findings", "actions", "prioritized_actions"}:
                        out[k] = tag_obj(v)
                    else:
                        out[k] = v
                return out
            if isinstance(obj, list):
                return [tag_obj(v) for v in obj]
            return obj

        for agent_name, agent_result in results.items():
            if isinstance(agent_result, dict) and not agent_result.get("error_flag"):
                results[agent_name] = tag_obj(agent_result)

        return results

    def _apply_action_plan_cleanup(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        ACTION_PLAN_CLEANUP gate:
        If an agent's findings/metrics contain the null-data sentinel
        ('Bu metrik için yeterli veri toplanamadı'), remove its recommendations
        from the executive summary / prioritized actions so that we never
        suggest a fix for a metric we don't actually have.

        Strategy:
        - Walk every agent result.
        - If the agent is already flagged via hallucination containment sentinel,
          strip its 'recommendations' and 'prioritized_actions' lists.
        - Also strip any cross-agent executive_summary items whose source_agent
          matches a null-data agent.
        """
        NULL_SENTINEL = "Bu metrik için yeterli veri toplanamadı"
        null_agents: List[str] = []

        def _is_null_agent(agent_result: Dict[str, Any]) -> bool:
            """Return True if this agent output is entirely null-data."""
            # Check findings list
            findings = agent_result.get("findings", [])
            if isinstance(findings, list) and findings:
                for f in findings:
                    text = ""
                    if isinstance(f, str):
                        text = f
                    elif isinstance(f, dict):
                        text = str(f.get("finding", ""))
                    if NULL_SENTINEL in text:
                        return True
            # Check recommendations list
            recs = agent_result.get("recommendations", [])
            if isinstance(recs, list) and recs:
                for r in recs:
                    text = ""
                    if isinstance(r, str):
                        text = r
                    elif isinstance(r, dict):
                        text = str(r.get("recommendation", ""))
                    if NULL_SENTINEL in text:
                        return True
            return False

        # First pass: identify null agents
        for agent_name, agent_result in results.items():
            if isinstance(agent_result, dict) and not agent_result.get("error_flag"):
                if _is_null_agent(agent_result):
                    null_agents.append(agent_name)
                    # Clear recommendations and prioritized_actions for this agent
                    agent_result["recommendations"] = []
                    agent_result["prioritized_actions"] = []
                    agent_result["_action_plan_suppressed"] = True

        # Second pass: strip from cross-agent executive summary if present
        for key in ("executiveSummary", "executive_summary", "crossAgentInsights"):
            summary = results.get(key)
            if not isinstance(summary, dict):
                continue
            for sub_key in ("action_items", "actionItems", "recommendations", "prioritized_actions"):
                items = summary.get(sub_key)
                if not isinstance(items, list):
                    continue
                filtered = [
                    item for item in items
                    if not (
                        isinstance(item, dict) and
                        item.get("source_agent", item.get("agent", "")) in null_agents
                    )
                ]
                if len(filtered) < len(items):
                    summary[sub_key] = filtered

        if null_agents:
            logger.info(
                f"ACTION_PLAN_CLEANUP: suppressed action items for {len(null_agents)} "
                f"null-data agent(s): {', '.join(null_agents)}"
            )

        return results

    def _apply_hallucination_containment(
        self,
        results: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        If agent has zero/null-only metrics, block qualitative hallucinations.
        """
        warnings: List[str] = []

        for agent_name, agent_result in results.items():
            if agent_result.get("error_flag"):
                continue

            metrics = agent_result.get("metrics", {})
            if not isinstance(metrics, dict):
                continue

            numeric_values = [self._to_number(v) for v in metrics.values()]
            valid_numeric = [v for v in numeric_values if v is not None]

            # Rule: ALL numeric metrics are 0 → hallucination containment
            has_only_zero_or_missing = bool(valid_numeric) and all(v == 0 for v in valid_numeric)

            # Rule: MAJORITY (>50%) of metric values are null/missing → containment
            # Single null value is normal (e.g. competitor data); don't suppress entire agent
            total_metric_count = len(metrics)
            missing_count = sum(
                1 for v in metrics.values()
                if (v is None) or (isinstance(v, str) and v.strip().lower() in {
                    "veri yok", "hesaplanamadı", "n/a", "insufficient data"
                })
            )
            has_mostly_missing = (
                total_metric_count > 0 and
                (missing_count / total_metric_count) > 0.5
            )

            if has_only_zero_or_missing or has_mostly_missing:
                agent_result["findings"] = [
                    {
                        "finding": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı.",
                        "source_citation": "zero_or_null_metric_table"
                    }
                ]
                agent_result["recommendations"] = [
                    {
                        "recommendation": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı.",
                        "source_citation": "zero_or_null_metric_table"
                    }
                ]
                warnings.append(f"Hallucination containment activated for {agent_name}")

        return results, warnings

    def _apply_tone_language_standard(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Map prohibited lexicon to board-ready language recursively."""

        def sanitize_text(text: str) -> str:
            cleaned = text
            for bad, good in self.prohibited_lexicon_map.items():
                cleaned = re.sub(rf"\b{re.escape(bad)}\b", good, cleaned, flags=re.IGNORECASE)
            return cleaned

        def sanitize(obj: Any) -> Any:
            if isinstance(obj, str):
                return sanitize_text(obj)
            if isinstance(obj, list):
                return [sanitize(v) for v in obj]
            if isinstance(obj, dict):
                return {k: sanitize(v) for k, v in obj.items()}
            return obj

        return sanitize(results)

    def _apply_section_specific_constraints(
        self,
        results: Dict[str, Any],
        metrics: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Apply section-scoped constraints from strict audit protocol."""
        warnings: List[str] = []

        # Visual_Brand_Expert constraint: no color/font critique without explicit evidence
        visual = results.get("visualBrand", {})
        if visual and not visual.get("error_flag"):
            blob = str(visual).lower()
            has_hex = bool(re.search(r"#[0-9a-f]{3,8}\b", blob))
            has_font_signal = any(k in blob for k in ["font", "typography", "typeface"])

            if not has_hex and not has_font_signal:
                filtered_findings = []
                for f in visual.get("findings", []):
                    txt = self._extract_text(f).lower()
                    if any(w in txt for w in ["renk", "color", "font", "tipografi", "palette", "palet"]):
                        continue
                    filtered_findings.append(f)

                if not filtered_findings:
                    filtered_findings = [{
                        "finding": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı.",
                        "source_citation": "missing_hex_or_font_data"
                    }]

                visual["findings"] = filtered_findings
                warnings.append("Visual Brand constraints applied: color/font critique suppressed due to missing explicit evidence")

        # Community_Manager constraint: no Comment Magnet when ER > 3%, focus retention
        engagement_rate = self._to_number(metrics.get("engagement_rate"))
        if engagement_rate is None:
            engagement_rate = self._to_number(account_data.get("engagementRate"))

        if engagement_rate is not None and engagement_rate > 3:
            community = results.get("communityLoyalty", {})
            if community and not community.get("error_flag"):
                recs = community.get("recommendations", [])
                cleaned = []
                removed = False
                for rec in recs:
                    txt = self._extract_text(rec).lower()
                    if "comment magnet" in txt:
                        removed = True
                        continue
                    cleaned.append(rec)

                if removed:
                    cleaned.append({
                        "recommendation": "Retention odaklı stratejiye geçin: tekrar ziyaret/saklama/seri içerik tamamlama metriklerini artırın.",
                        "source_citation": f"engagement_rate={engagement_rate:.2f}%"
                    })
                    warnings.append("Community constraint applied: Comment Magnet removed for ER > 3%")

                community["recommendations"] = cleaned

        return results, warnings

    def _run_advanced_analytics_modules(
        self,
        account_data: Dict[str, Any],
        results: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Run board-ready advanced analytics modules with strict zero-data handling."""
        warnings: List[str] = []

        media_list = account_data.get("media_list") or account_data.get("recentPosts") or []
        comments_list = account_data.get("comments_list") or account_data.get("recentComments") or []
        competitor_data = account_data.get("competitor_data") or account_data.get("competitors") or None
        followers = self._to_number(account_data.get("followers"))

        # Fallback: derive sentiment corpus from media captions and embedded comments
        if not comments_list and isinstance(media_list, list):
            synthesized_comments: List[Any] = []
            for post in media_list[:40]:
                if not isinstance(post, dict):
                    continue

                caption = post.get("caption") or post.get("text")
                if isinstance(caption, str) and caption.strip():
                    synthesized_comments.append(caption)

                embedded = (
                    post.get("latestComments")
                    or post.get("comments")
                    or post.get("topComments")
                    or []
                )
                if isinstance(embedded, list):
                    synthesized_comments.extend(embedded[:10])

            comments_list = synthesized_comments

        polarity = self._module_performance_polarity(media_list, followers)
        chronobio = self._module_audience_chronobiology(media_list, followers)
        sentiment = self._module_sentiment_cloud_engine(comments_list)
        benchmark = self._module_competitive_benchmark(account_data, competitor_data, results)

        # Collect warnings for insufficient datasets
        for name, module in {
            "PERFORMANCE_POLARITY": polarity,
            "AUDIENCE_CHRONOBIOLOGY": chronobio,
            "SENTIMENT_CLOUD_ENGINE": sentiment,
            "COMPETITIVE_BENCHMARK": benchmark,
        }.items():
            if module.get("status") == "Insufficient Data":
                warnings.append(f"{name}: Insufficient Data")

        return {
            "performance_polarity": polarity,
            "audience_chronobiology": chronobio,
            "sentiment_cloud_engine": sentiment,
            "competitive_benchmark": benchmark,
        }, warnings

    def _module_performance_polarity(self, media_list: List[Any], followers: Optional[float]) -> Dict[str, Any]:
        if not isinstance(media_list, list) or not media_list:
            return {
                "status": "Insufficient Data",
                "message": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı."
            }

        if not followers or followers <= 0:
            return {
                "status": "Insufficient Data",
                "message": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı."
            }

        scored = []
        for p in media_list[:24]:
            if not isinstance(p, dict):
                continue
            likes = self._to_number(p.get("likes") or p.get("likeCount")) or 0
            comments = self._to_number(p.get("comments") or p.get("commentCount")) or 0
            post_id = p.get("id") or p.get("shortCode") or p.get("code") or "unknown"
            er = ((likes + comments) / followers) * 100 if followers > 0 else None
            if er is None:
                continue
            caption = str(p.get("caption") or "")
            scored.append({
                "post_id": post_id,
                "engagement_rate": round(er, 4),
                "caption_length": len(caption),
                "likes": likes,
                "comments": comments,
            })

        if len(scored) < 3:
            return {
                "status": "Insufficient Data",
                "message": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı."
            }

        sorted_posts = sorted(scored, key=lambda x: x["engagement_rate"], reverse=True)
        top3 = sorted_posts[:3]
        bottom3 = sorted_posts[-3:]

        return {
            "status": "OK",
            "top_posts": top3,
            "bottom_posts": bottom3,
            "insight": "Yüksek performanslı gönderiler, ortalamanın üzerinde etkileşim oranı ile öne çıkıyor; düşük performanslı gönderilerde etkileşim derinliği zayıf."
        }

    def _module_audience_chronobiology(self, media_list: List[Any], followers: Optional[float]) -> Dict[str, Any]:
        if not isinstance(media_list, list) or not media_list or not followers or followers <= 0:
            return {
                "status": "Insufficient Data",
                "message": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı."
            }

        bins: Dict[Tuple[str, int], List[float]] = {}
        day_map = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

        for p in media_list[:24]:
            if not isinstance(p, dict):
                continue
            ts = p.get("timestamp") or p.get("createdAt") or p.get("takenAt")
            if not ts:
                continue
            try:
                dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            except Exception:
                continue

            likes = self._to_number(p.get("likes") or p.get("likeCount")) or 0
            comments = self._to_number(p.get("comments") or p.get("commentCount")) or 0
            er = ((likes + comments) / followers) * 100

            key = (day_map[dt.weekday()], dt.hour)
            bins.setdefault(key, []).append(er)

        if not bins:
            return {
                "status": "Insufficient Data",
                "message": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı."
            }

        best_key, values = max(bins.items(), key=lambda x: sum(x[1]) / max(1, len(x[1])))
        avg_er = sum(values) / len(values)

        return {
            "status": "OK",
            "golden_window": {
                "day": best_key[0],
                "hour": best_key[1],
                "avg_er": round(avg_er, 4),
                "visual_description": f"Best Time: {best_key[0]} at {best_key[1]:02d}:00 (Avg ER: {avg_er:.2f}%)"
            }
        }

    def _module_sentiment_cloud_engine(self, comments_list: List[Any]) -> Dict[str, Any]:
        if not isinstance(comments_list, list) or not comments_list:
            return {
                "status": "Insufficient Data",
                "message": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı."
            }

        stopwords = {
            "ve", "ile", "ama", "çok", "bir", "bu", "şu", "için", "the", "and", "to", "of", "is", "it", "a", "an"
        }
        pos_words = {"harika", "mükemmel", "güzel", "iyi", "love", "great", "amazing", "super"}
        neg_words = {"kötü", "berbat", "zayıf", "bad", "poor", "awful", "hate"}

        token_freq: Dict[str, int] = {}
        pos = 0
        neg = 0
        neu = 0

        for c in comments_list[:100]:
            text = c.get("text") if isinstance(c, dict) else str(c)
            if not text:
                continue
            words = re.findall(r"[\wçğıöşüÇĞİÖŞÜ]{2,}", str(text).lower())
            filtered = [w for w in words if w not in stopwords]
            for w in filtered:
                token_freq[w] = token_freq.get(w, 0) + 1

            wset = set(filtered)
            if wset & pos_words:
                pos += 1
            elif wset & neg_words:
                neg += 1
            else:
                neu += 1

        total = pos + neg + neu
        if total == 0:
            return {
                "status": "Insufficient Data",
                "message": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı."
            }

        top5 = [k for k, _ in sorted(token_freq.items(), key=lambda x: x[1], reverse=True)[:5]]

        return {
            "status": "OK",
            "top_keywords": top5,
            "sentiment_split": {
                "positive_pct": round((pos / total) * 100, 2),
                "negative_pct": round((neg / total) * 100, 2),
                "neutral_pct": round((neu / total) * 100, 2),
            }
        }

    def _module_competitive_benchmark(
        self,
        account_data: Dict[str, Any],
        competitor_data: Any,
        results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        # normalize competitor source
        if isinstance(competitor_data, list) and competitor_data:
            comp = competitor_data[0] if isinstance(competitor_data[0], dict) else {}
        elif isinstance(competitor_data, dict):
            comp = competitor_data
        else:
            comp = {}

        my_er = self._to_number(account_data.get("engagementRate"))
        comp_er = self._to_number(comp.get("engagementRate") or comp.get("er"))

        my_growth = self._to_number(account_data.get("followersGrowth") or account_data.get("growthRate"))
        comp_growth = self._to_number(comp.get("followersGrowth") or comp.get("growthRate"))

        my_freq = self._to_number(account_data.get("postsPerWeek") or account_data.get("postingFrequency"))
        comp_freq = self._to_number(comp.get("postsPerWeek") or comp.get("postingFrequency"))

        # Fallback: if competitor payload missing, use domain/niche proxy benchmarks
        source = "competitor_data"
        if not comp:
            source = "niche_proxy"

            dm = (results or {}).get("domainMaster", {}) if isinstance(results, dict) else {}
            niche_info = (dm.get("niche_identification", {}) or {}) if isinstance(dm, dict) else {}
            dm_metrics = (dm.get("metrics", {}) or {}) if isinstance(dm, dict) else {}

            proxy_er = (
                self._to_number(account_data.get("benchmark_engagement"))
                or self._to_number(account_data.get("industryBenchmarkEngagement"))
                or self._to_number(niche_info.get("benchmark_engagement"))
                or self._to_number(dm_metrics.get("benchmarkEngagement"))
                or 2.5
            )
            proxy_growth = (
                self._to_number(account_data.get("benchmark_growth"))
                or self._to_number(dm_metrics.get("nicheGrowthBenchmark"))
                or 5.0
            )
            proxy_freq = (
                self._to_number(account_data.get("benchmark_posts_per_week"))
                or self._to_number(dm_metrics.get("benchmarkPostingFrequency"))
                or 4.0
            )

            comp_er = comp_er if comp_er is not None else proxy_er
            comp_growth = comp_growth if comp_growth is not None else proxy_growth
            comp_freq = comp_freq if comp_freq is not None else proxy_freq

        def verdict(a: Optional[float], b: Optional[float]) -> str:
            if a is None or b is None:
                return "Insufficient Data"
            return "WIN" if a >= b else "LOSS"

        status = "OK" if any(v is not None for v in [my_er, my_growth, my_freq]) else "Insufficient Data"
        if status == "Insufficient Data":
            return {
                "status": "Insufficient Data",
                "message": "Bu metrik için yeterli veri toplanamadı, bu nedenle yapay zeka analizi devre dışı bırakıldı."
            }

        return {
            "status": "OK",
            "source": source,
            "growth_rate": {
                "user": my_growth if my_growth is not None else "Insufficient Data",
                "competitor": comp_growth if comp_growth is not None else "Insufficient Data",
                "verdict": verdict(my_growth, comp_growth),
            },
            "engagement_rate": {
                "user": my_er if my_er is not None else "Insufficient Data",
                "competitor": comp_er if comp_er is not None else "Insufficient Data",
                "verdict": verdict(my_er, comp_er),
            },
            "posting_frequency": {
                "user": my_freq if my_freq is not None else "Insufficient Data",
                "competitor": comp_freq if comp_freq is not None else "Insufficient Data",
                "verdict": verdict(my_freq, comp_freq),
            }
        }

    def _attach_advanced_analytics(self, results: Dict[str, Any], analytics: Dict[str, Any]) -> None:
        """Attach advanced analytics to system governor output for report builder."""
        if "systemGovernor" not in results or not isinstance(results.get("systemGovernor"), dict):
            results["systemGovernor"] = {}
        results["systemGovernor"]["advancedAnalytics"] = analytics

    def _apply_output_sanitization(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Remove internal logs and prompt residue from final output."""
        remove_phrases = [
            # Internal system artifacts
            "json parsing failed",
            "manual review required",
            "mismatch detected",
            "integrity_conflict",
            "integrity conflict",
            "_action_plan_suppressed",
            "_suppressed_by_integrity_conflict",
            "line_1: [who]",
            "line_2: [what]",
            "line_3: [why]",
            "belirleniyor",
            "undefined",
            "loading...",
            "veto edildi",
            # ERROR_SUPPRESSION_PROTOCOL: hide API/system errors from client
            "resource_exhausted",
            "quota exceeded",
            "clienterror",
            "internal server error",
            "429",
            "rate limit",
            "api key",
            "apify run failed",
            "apify run timed out",
            "timeout",
        ]

        # TONE_POLICE_PROTOCOL: Maintain Professional Corporate Tone
        tone_police_rewrites = [
            (re.compile(r"\bÖlümcül\b", re.IGNORECASE), "Kritik"),
            (re.compile(r"\bİntihar\b", re.IGNORECASE), "Yüksek Riskli Strateji"),
            (re.compile(r"\bRezalet\b", re.IGNORECASE), "Yetersiz"),
            (re.compile(r"\bÇöp\b", re.IGNORECASE), "Verimsiz"),
            (re.compile(r"\bBerbat\b", re.IGNORECASE), "Zayıf"),
            (re.compile(r"\bSürünüyor\b", re.IGNORECASE), "Beklentinin Altında"),
        ]

        def to_report_string(entry: Any) -> str:
            if isinstance(entry, str):
                return entry
            if isinstance(entry, dict):
                for key in ("recommendation", "finding", "action", "description", "issue", "text"):
                    if entry.get(key):
                        return str(entry.get(key))
                compact = [f"{k}: {v}" for k, v in entry.items() if isinstance(v, (str, int, float))]
                return " | ".join(compact) if compact else ""
            return str(entry)

        def sanitize(obj: Any) -> Any:
            if isinstance(obj, str):
                lowered = obj.lower()
                if lowered.strip().startswith("{"):
                    return ""
                if lowered.strip() in {"undefined", "belirleniyor", "null", "none", "nan", "veto edildi"}:
                    return ""
                for p in remove_phrases:
                    if p in lowered:
                        return ""
                # VARIABLE_HANDLING: Remove sentences that expose 'reelsScenario' as a literal variable name
                if "reelsscenario" in lowered and ("alanında" in lowered or "alaninda" in lowered):
                    obj = re.sub(
                        r"\.?\s*Detaylı senaryo '?reelsScenario'? alanında\.?",
                        "",
                        obj,
                        flags=re.IGNORECASE
                    ).strip().rstrip(".")
                    if not obj:
                        return ""
                # TONE_POLICE_PROTOCOL: Replace banned words with corporate-safe alternatives
                for pattern, replacement in tone_police_rewrites:
                    obj = pattern.sub(replacement, obj)
                # FRONTEND-SAFE ENCODING: keep Latin/Turkish chars and common punctuation only
                cleaned = re.sub(r"[^0-9A-Za-zÇĞİÖŞÜçğıöşü\s\.,;:!?\-_'\"%&/\+\(\)\[\]#@*=]", "", obj)
                return re.sub(r"\s{2,}", " ", cleaned).strip()
            if isinstance(obj, list):
                cleaned = [sanitize(v) for v in obj]
                return [v for v in cleaned if not (isinstance(v, str) and v == "")]
            if isinstance(obj, dict):
                out = {}
                for k, v in obj.items():
                    sv = sanitize(v)
                    if isinstance(sv, str) and sv == "":
                        continue
                    out[k] = sv

                # ZERO_DATA_UX_STRATEGY: collapse visual/growth sections that are entirely zero/null
                # so the client never sees a table full of empty cells
                numeric_score_keys = {
                    "contentQuality", "visualConsistency", "brandRecognition",
                    "colorConsistencyScore", "gridProfessionalism",
                }
                score_values = [
                    out.get(k) for k in numeric_score_keys
                    if k in out and self._to_number(out.get(k)) is not None
                ]
                if score_values and all((self._to_number(v) or 0) == 0 for v in score_values):
                    # Replace all-zero visual section with processing placeholder
                    for k in numeric_score_keys:
                        out.pop(k, None)
                    out["_visual_placeholder"] = (
                        "Görsel veri analizi işleniyor. "
                        "(Yeterli veri toplanınca rapor güncellenecektir)."
                    )

                # ZERO_DATA_UX_STRATEGY: collapse growth section if all null / 'Veri Yok'
                growth_keys = {"netGrowthRate", "churnRate", "growthVelocity"}
                growth_values = [
                    out.get(k) for k in growth_keys if k in out
                ]
                if growth_values and all(
                    (v is None or str(v).lower() in {"veri yok", "null", "0", "none", ""})
                    for v in growth_values
                ):
                    for k in growth_keys:
                        out.pop(k, None)

                # FINAL_OUTPUT_CHECK step_1: remove any remaining raw JSON strings
                for k, v in list(out.items()):
                    if isinstance(v, str) and v.strip().startswith("{") and v.strip().endswith("}"):
                        out.pop(k, None)

                # CRITICAL_OUTPUT_SANITIZATION: user-facing arrays should be plain text, not raw JSON objects
                for list_key in ("findings", "recommendations", "alerts"):
                    if isinstance(out.get(list_key), list):
                        normalized = []
                        for item in out[list_key]:
                            s = to_report_string(item)
                            if s and not s.strip().startswith("{"):
                                normalized.append(s)
                        out[list_key] = normalized

                # Never expose internal conflict tag in final text
                if isinstance(out.get("findings"), list):
                    out["findings"] = [
                        f for f in out["findings"]
                        if "integrity_conflict" not in str(f).lower() and "integrity conflict" not in str(f).lower()
                    ]

                return out
            return obj

        return sanitize(results)
    
    def _extract_cross_agent_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and normalize metrics from all agents for cross-validation."""
        metrics = {
            "engagement_depth": 50,  # Default
            "trust_score": 50,
            "monetization_readiness": 0,
            "ghost_follower_percent": 0,
            "algorithm_health": 50,
            "competitor_gap": 0,
            "competitors_identified": 0,
            "overall_health": 50,
            "funnel_efficiency": 0,
            "engagement_rate": 0,
        }
        
        # From Community Loyalty Agent
        community = results.get("communityLoyalty", {})
        if community and not community.get("error_flag"):
            community_metrics = community.get("metrics", {})
            # Convert avgEngagementDepth to numeric
            depth_map = {"surface": 20, "light": 35, "medium": 50, "deep": 70, "advocacy": 90}
            depth_str = community_metrics.get("avgEngagementDepth", "surface")
            metrics["engagement_depth"] = depth_map.get(depth_str, 30)
            metrics["trust_score"] = community_metrics.get("loyaltyIndex", 50)
            
            # Ghost follower estimation from community insights
            insights = community.get("communityInsights", {})
            followers = insights.get("passiveFollowers", 0) + insights.get("ghostFollowers", 0)
            total = (insights.get("estimatedSuperfans", 0) + insights.get("activeEngagers", 0) + 
                    insights.get("passiveFollowers", 0) + insights.get("ghostFollowers", 0))
            if total > 0:
                metrics["ghost_follower_percent"] = (insights.get("ghostFollowers", 0) / total) * 100
        
        # From Sales Conversion Agent
        sales = results.get("salesConversion", {})
        if sales and not sales.get("error_flag"):
            sales_metrics = sales.get("metrics", {})
            metrics["monetization_readiness"] = sales_metrics.get("monetizationReadinessScore", 0)
            metrics["funnel_efficiency"] = sales_metrics.get("conversionPotentialScore", 0) * 100
        
        # From Growth Virality Agent
        growth = results.get("growthVirality", {})
        if growth and not growth.get("error_flag"):
            growth_metrics = growth.get("metrics", {})
            metrics["competitor_gap"] = growth_metrics.get("competitorGap", 0)
            
            comp_analysis = growth.get("competitor_analysis", {})
            metrics["competitors_identified"] = comp_analysis.get("competitors_identified", 0)
            metrics["algorithm_health"] = growth_metrics.get("strategyEffectiveness", 50) * 20
        
        # From Audience Dynamics Agent  
        audience = results.get("audienceDynamics", {})
        if audience and not audience.get("error_flag"):
            audience_metrics = audience.get("metrics", {})
            metrics["engagement_rate"] = audience_metrics.get("engagementRate", 0)
            
            # Better ghost follower detection from audience
            bot_detection = audience.get("botDetectionScore", {})
            if bot_detection:
                ghost_estimate = bot_detection.get("estimated_fake_percentage", 0)
                if ghost_estimate > metrics["ghost_follower_percent"]:
                    metrics["ghost_follower_percent"] = ghost_estimate
        
        # From System Governor - overall health
        governor = results.get("systemGovernor", {})
        if governor and not governor.get("error_flag"):
            metrics["overall_health"] = self._calculate_health_from_governor(governor)
        
        return metrics
    
    def _calculate_health_from_governor(self, governor_result: Dict[str, Any]) -> float:
        """Calculate overall health score from system governor validation."""
        # Try to get from validation results
        validation = governor_result.get("validation", {})
        if validation:
            confidence = validation.get("confidence", 0.5)
            issues = len(validation.get("issues", []))
            base_health = confidence * 100
            penalty = min(30, issues * 5)
            return max(0, base_health - penalty)
        
        # Fallback to metrics
        metrics = governor_result.get("metrics", {})
        return metrics.get("overallScore", 50)
    
    def _apply_monetization_gate(
        self,
        results: Dict[str, Any],
        metrics: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Gate 1: If engagement_depth < 30 OR trust_score < 50,
        monetization_readiness MUST NOT exceed 40.
        """
        corrections = []
        gate = self.gates["monetization_requires_engagement"]
        
        engagement_depth = metrics["engagement_depth"]
        trust_score = metrics["trust_score"]
        current_monetization = metrics["monetization_readiness"]
        funnel_efficiency = metrics["funnel_efficiency"]
        
        needs_cap = (
            engagement_depth < gate["engagement_depth_min"] or 
            trust_score < gate["trust_score_min"]
        )
        
        if needs_cap and current_monetization > gate["monetization_cap"]:
            # Apply correction to salesConversion agent
            if "salesConversion" in results and not results["salesConversion"].get("error_flag"):
                old_value = current_monetization
                new_value = gate["monetization_cap"]
                
                results["salesConversion"]["metrics"]["monetizationReadinessScore"] = new_value
                
                # Add correction notice to findings
                correction_finding = {
                    "type": "sanity_gate_correction",
                    "issue": "Monetization Score Overclaim",
                    "original_value": old_value,
                    "corrected_value": new_value,
                    "reason": f"Engagement depth ({engagement_depth}) and/or trust score ({trust_score}) "
                             f"do not support monetization readiness above {gate['monetization_cap']}",
                    "fix_action": "Build engagement foundation before monetization",
                    "template": self.action_templates["low_engagement"]
                }
                
                results["salesConversion"]["_sanity_corrections"] = [correction_finding]
                
                corrections.append({
                    "gate": "monetization_engagement_consistency",
                    "agent": "salesConversion",
                    "field": "monetizationReadinessScore",
                    "old_value": old_value,
                    "new_value": new_value,
                    "reason": correction_finding["reason"]
                })
                
                logger.warning(
                    f"Sanity Gate: Capped monetizationReadinessScore from {old_value} to {new_value} "
                    f"(engagement_depth={engagement_depth}, trust_score={trust_score})"
                )
        
        return results, corrections
    
    def _apply_ghost_follower_gate(
        self,
        results: Dict[str, Any],
        metrics: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Gate 2: If ghost_followers > 20%, apply -50 penalty to algorithm_health.
        """
        corrections = []
        gate = self.gates["ghost_follower_penalty"]
        
        ghost_percent = metrics["ghost_follower_percent"]
        
        if ghost_percent > gate["ghost_threshold_percent"]:
            penalty = gate["algorithm_health_penalty"]
            
            # Apply to growthVirality agent
            if "growthVirality" in results and not results["growthVirality"].get("error_flag"):
                growth_metrics = results["growthVirality"].get("metrics", {})
                old_effectiveness = growth_metrics.get("strategyEffectiveness", 5)
                # Convert to 0-100 scale, apply penalty, convert back
                old_score = old_effectiveness * 20
                new_score = max(0, old_score - penalty)
                new_effectiveness = new_score / 20
                
                results["growthVirality"]["metrics"]["strategyEffectiveness"] = new_effectiveness
                
                # Add warning finding
                ghost_warning = {
                    "type": "sanity_gate_penalty",
                    "issue": "High Ghost Follower Impact",
                    "ghost_percentage": round(ghost_percent, 1),
                    "penalty_applied": penalty,
                    "impact": "Algorithm health significantly reduced",
                    "fix_action": "Prioritize ghost follower removal before growth tactics",
                    "template": self.action_templates["ghost_followers"]
                }
                
                if "_sanity_corrections" not in results["growthVirality"]:
                    results["growthVirality"]["_sanity_corrections"] = []
                results["growthVirality"]["_sanity_corrections"].append(ghost_warning)
                
                corrections.append({
                    "gate": "ghost_follower_penalty",
                    "agent": "growthVirality",
                    "field": "strategyEffectiveness",
                    "old_value": old_effectiveness,
                    "new_value": new_effectiveness,
                    "penalty": penalty,
                    "reason": f"Ghost follower percentage ({ghost_percent:.1f}%) exceeds threshold ({gate['ghost_threshold_percent']}%)"
                })
                
                logger.warning(
                    f"Sanity Gate: Applied {penalty} penalty to algorithm health "
                    f"(ghost_followers={ghost_percent:.1f}%)"
                )
        
        return results, corrections
    
    def _apply_competitor_data_gate(
        self,
        results: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Gate 3: If competitor data is 0 or null, set competitorGap to null/0
        and add data quality warning.
        """
        corrections = []
        warnings = []
        gate = self.gates["competitor_data_validation"]
        
        if "growthVirality" in results and not results["growthVirality"].get("error_flag"):
            growth = results["growthVirality"]
            
            # Check competitor analysis
            comp_analysis = growth.get("competitor_analysis", {})
            competitors_identified = comp_analysis.get("competitors_identified", 0)
            
            # Check competitorGapAnalysis
            gap_analysis = growth.get("competitorGapAnalysis", {})
            competitors_list = gap_analysis.get("competitors", [])
            
            has_valid_competitor_data = (
                competitors_identified >= gate["min_competitors_for_gap"] and
                len(competitors_list) >= gate["min_competitors_for_gap"]
            )
            
            current_gap = growth.get("metrics", {}).get("competitorGap", 0)
            
            if not has_valid_competitor_data:
                # Reset competitorGap to 0
                if current_gap != 0:
                    results["growthVirality"]["metrics"]["competitorGap"] = 0
                    
                    corrections.append({
                        "gate": "competitor_data_validation",
                        "agent": "growthVirality",
                        "field": "competitorGap",
                        "old_value": current_gap,
                        "new_value": 0,
                        "reason": "Insufficient competitor data for valid gap analysis"
                    })
                
                # Add data quality warning
                warning = {
                    "type": "data_quality_warning",
                    "field": "competitor_analysis",
                    "message": "Insufficient competitor data for gap analysis",
                    "competitors_found": competitors_identified,
                    "minimum_required": gate["min_competitors_for_gap"],
                    "impact": "Competitor-based strategies may not be accurate",
                    "recommendation": "Run competitor discovery or manually input competitor usernames"
                }
                
                warnings.append(warning)
                
                # Add flag to results
                if "_data_quality_warnings" not in results["growthVirality"]:
                    results["growthVirality"]["_data_quality_warnings"] = []
                results["growthVirality"]["_data_quality_warnings"].append(warning)
                
                # Remove competitor-based recommendations
                recommendations = growth.get("recommendations", [])
                filtered_recs = []
                competitor_keywords = ["competitor", "rakip", "benchmark", "market leader", "industry leader"]
                
                for rec in recommendations:
                    rec_text = rec.get("action", "") if isinstance(rec, dict) else str(rec)
                    if not any(kw in rec_text.lower() for kw in competitor_keywords):
                        filtered_recs.append(rec)
                    else:
                        logger.info(f"Removed competitor-based recommendation due to missing data: {rec_text[:50]}")
                
                results["growthVirality"]["recommendations"] = filtered_recs
                
                logger.warning(
                    f"Sanity Gate: Invalidated competitor gap analysis "
                    f"(competitors_found={competitors_identified}, required={gate['min_competitors_for_gap']})"
                )
        
        return results, corrections, warnings
    
    def _apply_phase_enforcement(
        self,
        results: Dict[str, Any],
        metrics: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Gate 4: Enforce strategic phase based on overall health score.
        Block inappropriate strategies for current phase.
        """
        health_score = metrics["overall_health"]
        engagement_depth = metrics["engagement_depth"]
        trust_score = metrics["trust_score"]
        
        # Determine phase (use worst indicator)
        effective_score = min(health_score, engagement_depth, trust_score)
        
        current_phase = None
        for phase_name, phase_config in self.strategic_phases.items():
            low, high = phase_config["health_range"]
            if low <= effective_score <= high:
                current_phase = phase_name
                break
        
        if current_phase is None:
            current_phase = "rescue"  # Default to most conservative
        
        phase_config = self.strategic_phases[current_phase]
        
        phase_info = {
            "determined_phase": current_phase,
            "phase_name": phase_config["phase_name"],
            "health_score": health_score,
            "effective_score": effective_score,
            "focus_areas": phase_config["focus_areas"],
            "blocked_strategies": phase_config["blocked_strategies"],
            "duration": phase_config["duration"],
            "reasoning": self._generate_phase_reasoning(current_phase, metrics)
        }
        
        # Update strategy recommendations in salesConversion
        if "salesConversion" in results and not results["salesConversion"].get("error_flag"):
            sales = results["salesConversion"]
            
            # Override phase 1 strategy if in rescue mode
            if current_phase == "rescue":
                action_plan = sales.get("actionPlan", {})
                
                # Replace immediate actions with foundation tasks
                action_plan["immediate"] = [
                    "Profile optimization: Bio'yu WHO-WHAT-WHY formatına çevir",
                    "Ghost follower temizliği başlat (Story poll ile tespit)",
                    "İçerik formatlarını standartlaştır (tutarlı template kullan)"
                ]
                action_plan["thirtyDay"] = [
                    "Engagement depth artırma: Her paylaşımda soru sor",
                    "Topluluk ritüelleri oluştur (haftalık Q&A, günlük tip)",
                    "Hashtag stratejisini 3-3-3 formatına geçir"
                ]
                action_plan["ninetyDay"] = [
                    "Trust sinyalleri güçlendir (testimonial, UGC paylaş)",
                    "Email listesi oluşturmaya başla (lead magnet)",
                    "Mikro-influencer networking'e başla"
                ]
                
                sales["actionPlan"] = action_plan
                sales["_phase_override"] = {
                    "original_phase": sales.get("monetization_overview", {}).get("revenue_stage", "unknown"),
                    "enforced_phase": "foundation",
                    "reason": "Health score requires foundation building before monetization"
                }
                
                # Update findings
                if isinstance(sales.get("findings"), list):
                    sales["findings"].insert(0, {
                        "type": "phase_enforcement",
                        "issue": "Account Not Ready for Monetization",
                        "current_phase": "Foundation & Cleanup",
                        "blocked_actions": phase_config["blocked_strategies"],
                        "fix_action": "Complete foundation phase before monetization",
                        "estimated_timeline": phase_config["duration"]
                    })
            
            results["salesConversion"] = sales
        
        # Add phase info to all agents
        for agent_name in results:
            if not results[agent_name].get("error_flag"):
                results[agent_name]["_strategic_phase"] = phase_info
        
        return results, phase_info
    
    def _generate_phase_reasoning(
        self,
        phase: str,
        metrics: Dict[str, Any]
    ) -> str:
        """Generate human-readable reasoning for phase determination."""
        if phase == "rescue":
            issues = []
            if metrics["engagement_depth"] < 30:
                issues.append(f"Low engagement depth ({metrics['engagement_depth']})")
            if metrics["trust_score"] < 50:
                issues.append(f"Low trust score ({metrics['trust_score']})")
            if metrics["ghost_follower_percent"] > 20:
                issues.append(f"High ghost followers ({metrics['ghost_follower_percent']:.1f}%)")
            if metrics["overall_health"] < 50:
                issues.append(f"Low overall health ({metrics['overall_health']})")
            
            return f"Account requires foundation work due to: {', '.join(issues) if issues else 'multiple health indicators below threshold'}"
        
        elif phase == "growth":
            return (f"Account has solid foundation (health={metrics['overall_health']}) "
                   f"but needs engagement boost before monetization")
        
        else:  # monetization
            return (f"Account is ready for monetization "
                   f"(health={metrics['overall_health']}, engagement={metrics['engagement_depth']}, "
                   f"trust={metrics['trust_score']})")
    
    def _apply_specificity_enforcement(
        self,
        results: Dict[str, Any],
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Gate 5: Convert generic findings to specific, actionable templates.
        """
        # Define generic patterns and their specific replacements
        generic_patterns = {
            r"improve.*(hook|başlık|dikkat)": "weak_hook",
            r"(engagement|etkileşim).*(low|düşük|artır)": "low_engagement",
            r"(ghost|hayalet|inaktif).*(follower|takipçi)": "ghost_followers",
            r"(bio|profil).*(unclear|belirsiz|optimize|geliştir)": "poor_bio",
            r"(inconsistent|düzensiz).*(post|paylaşım|içerik)": "inconsistent_posting",
            r"(cta|call.to.action|harekete geçir)": "no_cta",
            r"(hashtag).*(ineffective|etkisiz|geliştir)": "poor_hashtags",
            r"(save|kaydet).*(low|düşük|artır)": "low_saves",
            r"(create|oluştur).*(content|içerik).*(emotion|duygu)": "weak_hook",  # Catch generic advice
        }
        
        for agent_name, agent_result in results.items():
            if agent_result.get("error_flag"):
                continue
            
            # Process findings
            findings = agent_result.get("findings", [])
            enhanced_findings = []
            
            for finding in findings:
                finding_text = finding if isinstance(finding, str) else finding.get("finding", str(finding))
                finding_lower = finding_text.lower()
                
                matched_template = None
                for pattern, template_key in generic_patterns.items():
                    if re.search(pattern, finding_lower):
                        matched_template = self.action_templates.get(template_key)
                        break
                
                if matched_template:
                    # Replace generic finding with specific template
                    enhanced_finding = {
                        "original": finding_text,
                        "issue": matched_template["issue"],
                        "fix_action": matched_template["fix_action"],
                        "template": matched_template["template"],
                        "specificity_enhanced": True
                    }
                    if "examples" in matched_template:
                        enhanced_finding["examples"] = matched_template["examples"]
                    if "expected_impact" in matched_template:
                        enhanced_finding["expected_impact"] = matched_template["expected_impact"]
                    
                    enhanced_findings.append(enhanced_finding)
                else:
                    # Keep original if no match
                    if isinstance(finding, dict):
                        enhanced_findings.append(finding)
                    else:
                        enhanced_findings.append({"finding": finding_text, "specificity_enhanced": False})
            
            if enhanced_findings:
                results[agent_name]["findings"] = enhanced_findings
            
            # Process recommendations similarly
            recommendations = agent_result.get("recommendations", [])
            enhanced_recs = []
            
            for rec in recommendations:
                rec_text = rec if isinstance(rec, str) else rec.get("action", rec.get("recommendation", str(rec)))
                rec_lower = rec_text.lower()
                
                matched_template = None
                for pattern, template_key in generic_patterns.items():
                    if re.search(pattern, rec_lower):
                        matched_template = self.action_templates.get(template_key)
                        break
                
                if matched_template:
                    enhanced_rec = {
                        "original": rec_text,
                        "action": matched_template["fix_action"],
                        "implementation": matched_template["template"],
                        "specificity_enhanced": True
                    }
                    if isinstance(rec, dict):
                        enhanced_rec.update({k: v for k, v in rec.items() if k not in ["action", "recommendation"]})
                    enhanced_recs.append(enhanced_rec)
                else:
                    if isinstance(rec, dict):
                        enhanced_recs.append(rec)
                    else:
                        enhanced_recs.append({"recommendation": rec_text, "specificity_enhanced": False})
            
            if enhanced_recs:
                results[agent_name]["recommendations"] = enhanced_recs
        
        return results


# Singleton instance for import
_sanity_gates = None

def get_sanity_gates() -> MetricSanityGates:
    """Get or create singleton MetricSanityGates instance."""
    global _sanity_gates
    if _sanity_gates is None:
        _sanity_gates = MetricSanityGates()
    return _sanity_gates


__all__ = ["MetricSanityGates", "get_sanity_gates"]
