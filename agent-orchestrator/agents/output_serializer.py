# =============================================================================
# Output Serializer - Frontend/PDF Tutarlılık Modülü
# Version 2.0 - Instagram AI Agent System
# =============================================================================
"""
Bu modül analiz sonuçlarını tutarlı formata dönüştürür:
1. Agent sonuçlarını normalize et
2. Frontend ve PDF için tek kaynak JSON üret
3. Eksik alanları doldur
4. Skor hesaplamalarını standardize et

Kullanım:
    from agents.output_serializer import OutputSerializer, serialize_analysis

    serializer = OutputSerializer()
    result = serializer.serialize(raw_results, account_data)
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

SCORE_GRADES = [
    (90, "A+", "Mükemmel", "#10B981"),
    (85, "A", "Harika", "#22C55E"),
    (80, "A-", "Çok İyi", "#34D399"),
    (75, "B+", "İyi", "#84CC16"),
    (70, "B", "İyi", "#A3E635"),
    (65, "B-", "Ortanın Üstü", "#BEF264"),
    (60, "C+", "Orta", "#FACC15"),
    (55, "C", "Orta", "#FCD34D"),
    (50, "C-", "Ortanın Altı", "#FBBF24"),
    (45, "D+", "Zayıf", "#F97316"),
    (40, "D", "Zayıf", "#FB923C"),
    (35, "D-", "Çok Zayıf", "#F87171"),
    (0, "F", "Başarısız", "#EF4444"),
]

AGENT_WEIGHT_MAP = {
    "domainMaster": 0.15,
    "growthVirality": 0.15,
    "salesConversion": 0.15,
    "visualBrand": 0.12,
    "communityLoyalty": 0.13,
    "attentionArchitect": 0.15,
    "systemGovernor": 0.10,
    "contentStrategist": 0.05,
}

CATEGORY_ICONS = {
    "growth": "📈",
    "engagement": "💬",
    "content": "📝",
    "visual": "🎨",
    "community": "👥",
    "sales": "💰",
    "technical": "⚙️",
    "strategy": "🎯",
    "warning": "⚠️",
    "success": "✅",
    "error": "❌",
    "info": "ℹ️",
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def score_to_grade(score: float) -> Tuple[str, str, str]:
    """
    Skoru nota çevir
    
    Returns:
        (grade, label, color_hex)
    """
    for threshold, grade, label, color in SCORE_GRADES:
        if score >= threshold:
            return grade, label, color
    return "F", "Başarısız", "#EF4444"


def get_category_icon(category: str) -> str:
    """Kategori için emoji al"""
    category_lower = category.lower()
    for key, icon in CATEGORY_ICONS.items():
        if key in category_lower:
            return icon
    return "📌"


def calculate_weighted_score(agent_results: Dict[str, Any]) -> float:
    """
    Ağırlıklı ortalama skor hesapla
    """
    total_weight = 0.0
    weighted_sum = 0.0
    
    for agent_name, result in agent_results.items():
        if isinstance(result, dict) and not result.get("error"):
            weight = AGENT_WEIGHT_MAP.get(agent_name, 0.1)
            metrics = result.get("metrics", {})
            score = metrics.get("overallScore", 50.0)
            
            weighted_sum += score * weight
            total_weight += weight
    
    if total_weight == 0:
        return 50.0
    
    return round(weighted_sum / total_weight, 1)


# =============================================================================
# OUTPUT SERIALIZER
# =============================================================================

class OutputSerializer:
    """
    Analiz sonuçlarını tutarlı formata dönüştürür
    """
    
    def __init__(self):
        self.default_finding = {
            "type": "info",
            "category": "general",
            "finding": "Analiz verisi mevcut değil",
            "evidence": "",
            "impact_score": 50
        }
        
        self.default_recommendation = {
            "priority": "medium",
            "category": "general",
            "action": "Analiz sonuçları detaylandırılmalı",
            "expected_impact": "İyileştirme bekleniyor",
            "implementation": "Yeniden analiz çalıştırın",
            "difficulty": "easy",
            "timeline": "1 week",
            "kpi": "N/A"
        }
    
    def serialize(
        self,
        raw_results: Dict[str, Any],
        account_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ham sonuçları tutarlı formata dönüştür
        
        Args:
            raw_results: Pipeline'dan gelen ham sonuçlar
            account_data: Hesap verileri
            
        Returns:
            Normalized, frontend/PDF ready JSON
        """
        # Extract components
        agent_results = raw_results.get("agentResults", {})
        eli5_report = raw_results.get("eli5Report", {})
        final_verdict = raw_results.get("finalVerdict", {})
        content_plan = raw_results.get("contentPlan", {})
        
        # Calculate overall score
        overall_score = calculate_weighted_score(agent_results)
        grade, label, color = score_to_grade(overall_score)
        
        # Build normalized output
        output = {
            # Metadata
            "metadata": self._build_metadata(raw_results, account_data),
            
            # Account info
            "account": self._normalize_account(account_data),
            
            # Overall score
            "overallScore": {
                "score": overall_score,
                "grade": grade,
                "label": label,
                "color": color,
                "confidence": self._calculate_confidence(agent_results)
            },
            
            # Agent results (normalized)
            "agentResults": self._normalize_agent_results(agent_results),
            
            # Summary sections
            "executiveSummary": self._build_executive_summary(eli5_report, agent_results, overall_score),
            
            # Key insights
            "keyStrengths": self._extract_strengths(agent_results),
            "keyWeaknesses": self._extract_weaknesses(agent_results),
            "quickWins": self._extract_quick_wins(agent_results),
            "topRecommendations": self._extract_top_recommendations(agent_results),
            
            # ELI5 Report
            "eli5Report": self._normalize_eli5(eli5_report),
            
            # Final verdict
            "finalVerdict": self._normalize_final_verdict(final_verdict),
            
            # Content plan
            "contentPlan": self._normalize_content_plan(content_plan),
            
            # Charts data
            "chartsData": self._build_charts_data(agent_results, overall_score),
            
            # Business identity
            "businessIdentity": raw_results.get("businessIdentity", {}),
            
            # Validation results
            "validationResults": {
                "hardValidation": raw_results.get("hardValidation", {}),
                "sanitizationReport": raw_results.get("sanitizationReport", {}),
            }
        }
        
        return output
    
    def _build_metadata(self, raw_results: Dict[str, Any], account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Metadata oluştur"""
        return {
            "analysisId": raw_results.get("analysisId", ""),
            "username": account_data.get("username", ""),
            "analysisStartedAt": raw_results.get("analysisStartedAt", datetime.utcnow().isoformat()),
            "analysisCompletedAt": raw_results.get("analysisCompletedAt", datetime.utcnow().isoformat()),
            "pipelineVersion": "2.0",
            "stagesCompleted": raw_results.get("stagesCompleted", []),
            "totalAgentsRun": len(raw_results.get("agentResults", {})),
            "dataSource": account_data.get("dataSource", "apify"),
        }
    
    def _normalize_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Hesap verilerini normalize et"""
        return {
            "username": account_data.get("username", ""),
            "fullName": account_data.get("fullName", ""),
            "followers": account_data.get("followers", account_data.get("followersCount", 0)),
            "following": account_data.get("following", account_data.get("followsCount", 0)),
            "posts": account_data.get("posts", account_data.get("postsCount", 0)),
            "bio": account_data.get("bio", ""),
            "profilePicUrl": account_data.get("profilePicUrl", ""),
            "isVerified": account_data.get("isVerified", False),
            "isPrivate": account_data.get("isPrivate", False),
            "isBusiness": account_data.get("isBusiness", False),
            "category": account_data.get("category", ""),
            "engagementRate": round(account_data.get("engagementRate", 0), 2),
            "avgLikes": account_data.get("avgLikes", 0),
            "avgComments": account_data.get("avgComments", 0),
        }
    
    def _normalize_agent_results(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Agent sonuçlarını normalize et"""
        normalized = {}
        
        for agent_name, result in agent_results.items():
            if not isinstance(result, dict):
                continue
            
            normalized[agent_name] = {
                "agentName": agent_name,
                "agentRole": result.get("agentRole", ""),
                
                # Findings
                "findings": self._normalize_findings(result.get("findings", [])),
                
                # Recommendations
                "recommendations": self._normalize_recommendations(result.get("recommendations", [])),
                
                # Metrics
                "metrics": self._normalize_metrics(result.get("metrics", {})),
                
                # Status
                "error": result.get("error", False),
                "errorMessage": result.get("errorMessage"),
                "vetoed": result.get("vetoed", False),
                "vetoReason": result.get("vetoReason"),
                "selfCorrected": result.get("selfCorrected", False),
                "modelUsed": result.get("modelUsed", ""),
                
                # Insights (if present)
                "insights": result.get("insights", []),
            }
        
        return normalized
    
    def _normalize_findings(self, findings: List[Any]) -> List[Dict[str, Any]]:
        """Findings'leri normalize et"""
        normalized = []
        
        for finding in findings:
            if isinstance(finding, str):
                normalized.append({
                    **self.default_finding,
                    "finding": finding if len(finding) >= 50 else finding + " " * (50 - len(finding))
                })
            elif isinstance(finding, dict):
                normalized.append({
                    "type": finding.get("type", "info"),
                    "category": finding.get("category", "general"),
                    "finding": finding.get("finding", finding.get("text", "N/A")),
                    "evidence": finding.get("evidence", ""),
                    "impact_score": finding.get("impact_score", finding.get("impactScore", 50)),
                    "icon": get_category_icon(finding.get("category", ""))
                })
        
        return normalized if normalized else [self.default_finding]
    
    def _normalize_recommendations(self, recommendations: List[Any]) -> List[Dict[str, Any]]:
        """Recommendations'ları normalize et"""
        normalized = []
        
        for i, rec in enumerate(recommendations):
            if isinstance(rec, str):
                normalized.append({
                    **self.default_recommendation,
                    "action": rec,
                    "priority": "high" if i < 2 else "medium"
                })
            elif isinstance(rec, dict):
                priority = rec.get("priority", "medium")
                if isinstance(priority, int):
                    priority = ["critical", "high", "medium", "low"][min(priority - 1, 3)] if priority > 0 else "medium"
                
                normalized.append({
                    "priority": priority,
                    "category": rec.get("category", "general"),
                    "action": rec.get("action", rec.get("recommendation", "N/A")),
                    "expected_impact": rec.get("expected_impact", rec.get("expectedImpact", "")),
                    "implementation": rec.get("implementation", ""),
                    "difficulty": rec.get("difficulty", "medium"),
                    "timeline": rec.get("timeline", "1-2 weeks"),
                    "kpi": rec.get("kpi", ""),
                    "icon": get_category_icon(rec.get("category", ""))
                })
        
        return normalized if normalized else [self.default_recommendation]
    
    def _normalize_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Metrics'leri normalize et"""
        return {
            "overallScore": round(metrics.get("overallScore", 50.0), 1),
            "confidence": round(metrics.get("confidence", 80.0), 1),
            "engagementScore": metrics.get("engagementScore"),
            "growthScore": metrics.get("growthScore"),
            "contentScore": metrics.get("contentScore"),
            "visualScore": metrics.get("visualScore"),
            "communityScore": metrics.get("communityScore"),
            "conversionScore": metrics.get("conversionScore"),
        }
    
    def _calculate_confidence(self, agent_results: Dict[str, Any]) -> float:
        """Genel güven skorunu hesapla"""
        confidences = []
        for result in agent_results.values():
            if isinstance(result, dict) and not result.get("error"):
                conf = result.get("metrics", {}).get("confidence", 80.0)
                confidences.append(conf)
        
        return round(sum(confidences) / len(confidences), 1) if confidences else 70.0
    
    def _build_executive_summary(
        self,
        eli5_report: Dict[str, Any],
        agent_results: Dict[str, Any],
        overall_score: float
    ) -> str:
        """Yönetici özeti oluştur"""
        # ELI5'ten al veya oluştur
        if eli5_report.get("executiveSummary"):
            return eli5_report["executiveSummary"]
        
        grade, label, _ = score_to_grade(overall_score)
        
        # Generate from agent results
        strengths = []
        weaknesses = []
        
        for agent_name, result in agent_results.items():
            if isinstance(result, dict) and not result.get("error"):
                findings = result.get("findings", [])
                for f in findings[:2]:
                    f_type = f.get("type", "info") if isinstance(f, dict) else "info"
                    f_text = f.get("finding", f) if isinstance(f, dict) else str(f)
                    
                    if f_type in ["strength", "opportunity"]:
                        strengths.append(f_text[:100])
                    elif f_type in ["weakness", "threat", "critical"]:
                        weaknesses.append(f_text[:100])
        
        summary = f"Hesap analizi tamamlandı. Genel performans: {label} ({grade}, {overall_score}/100). "
        
        if strengths:
            summary += f"Güçlü yönler: {'; '.join(strengths[:2])}. "
        if weaknesses:
            summary += f"İyileştirme alanları: {'; '.join(weaknesses[:2])}."
        
        return summary
    
    def _extract_strengths(self, agent_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Güçlü yönleri çıkar"""
        strengths = []
        
        for agent_name, result in agent_results.items():
            if isinstance(result, dict) and not result.get("error"):
                for finding in result.get("findings", []):
                    if isinstance(finding, dict):
                        if finding.get("type") in ["strength", "opportunity"]:
                            strengths.append({
                                "icon": "✅",
                                "label": finding.get("category", "Güçlü Yön"),
                                "content": finding.get("finding", ""),
                                "agent": agent_name
                            })
        
        return strengths[:5]  # Top 5
    
    def _extract_weaknesses(self, agent_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Zayıf yönleri çıkar"""
        weaknesses = []
        
        for agent_name, result in agent_results.items():
            if isinstance(result, dict) and not result.get("error"):
                for finding in result.get("findings", []):
                    if isinstance(finding, dict):
                        if finding.get("type") in ["weakness", "threat", "critical"]:
                            weaknesses.append({
                                "icon": "⚠️",
                                "label": finding.get("category", "İyileştirme Alanı"),
                                "content": finding.get("finding", ""),
                                "agent": agent_name,
                                "impact_score": finding.get("impact_score", 50)
                            })
        
        # Sort by impact score (higher first)
        weaknesses.sort(key=lambda x: x.get("impact_score", 50), reverse=True)
        return weaknesses[:5]
    
    def _extract_quick_wins(self, agent_results: Dict[str, Any]) -> List[str]:
        """Hızlı kazanımları çıkar"""
        quick_wins = []
        
        for result in agent_results.values():
            if isinstance(result, dict) and not result.get("error"):
                for rec in result.get("recommendations", []):
                    if isinstance(rec, dict):
                        difficulty = rec.get("difficulty", "medium")
                        if difficulty in ["easy", "kolay"]:
                            action = rec.get("action", "")
                            if action and len(action) > 20:
                                quick_wins.append(action[:200])
        
        return quick_wins[:3]
    
    def _extract_top_recommendations(self, agent_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """En önemli önerileri çıkar"""
        all_recs = []
        
        for agent_name, result in agent_results.items():
            if isinstance(result, dict) and not result.get("error"):
                for rec in result.get("recommendations", []):
                    if isinstance(rec, dict):
                        priority = rec.get("priority", "medium")
                        priority_score = {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(priority, 2)
                        
                        all_recs.append({
                            **rec,
                            "agent": agent_name,
                            "priority_score": priority_score
                        })
        
        # Sort by priority
        all_recs.sort(key=lambda x: x.get("priority_score", 2), reverse=True)
        return all_recs[:5]
    
    def _normalize_eli5(self, eli5_report: Dict[str, Any]) -> Dict[str, Any]:
        """ELI5 raporunu normalize et"""
        if not eli5_report:
            return {}
        
        return {
            "executiveSummary": eli5_report.get("executiveSummary", ""),
            "keyStrengths": eli5_report.get("keyStrengths", []),
            "keyWeaknesses": eli5_report.get("keyWeaknesses", []),
            "quickWins": eli5_report.get("quickWins", []),
            "longTermGoals": eli5_report.get("longTermGoals", []),
            "sections": eli5_report.get("sections", []),
            "attentionHooks": eli5_report.get("attentionHooks", []),
        }
    
    def _normalize_final_verdict(self, final_verdict: Dict[str, Any]) -> Dict[str, Any]:
        """Final verdict'i normalize et"""
        if not final_verdict:
            return {}
        
        return {
            "overallAssessment": final_verdict.get("overallAssessment", ""),
            "criticalIssues": final_verdict.get("criticalIssues", []),
            "strategicRecommendations": final_verdict.get("strategicRecommendations", []),
            "growthPotential": final_verdict.get("growthPotential", {}),
            "finalScore": final_verdict.get("finalScore", 0),
            "confidence": final_verdict.get("confidence", 80),
        }
    
    def _normalize_content_plan(self, content_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Content plan'ı normalize et"""
        if not content_plan:
            return {}
        
        return {
            "weeklyPlan": content_plan.get("weeklyPlan", content_plan.get("weekly_plan", [])),
            "contentThemes": content_plan.get("contentThemes", content_plan.get("themes", [])),
            "postingSchedule": content_plan.get("postingSchedule", {}),
            "contentMix": content_plan.get("contentMix", {}),
        }
    
    def _build_charts_data(self, agent_results: Dict[str, Any], overall_score: float) -> Dict[str, Any]:
        """Grafik verileri oluştur"""
        # Radar chart data
        radar_data = []
        for agent_name, result in agent_results.items():
            if isinstance(result, dict) and not result.get("error"):
                score = result.get("metrics", {}).get("overallScore", 50)
                radar_data.append({
                    "category": agent_name.replace("_", " ").title(),
                    "score": score,
                    "fullMark": 100
                })
        
        # Score distribution
        scores = [
            r.get("metrics", {}).get("overallScore", 50)
            for r in agent_results.values()
            if isinstance(r, dict) and not r.get("error")
        ]
        
        return {
            "radarChart": radar_data,
            "overallScore": overall_score,
            "scoreDistribution": {
                "min": min(scores) if scores else 0,
                "max": max(scores) if scores else 100,
                "avg": sum(scores) / len(scores) if scores else 50,
                "scores": scores
            }
        }


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def serialize_analysis(raw_results: Dict[str, Any], account_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function for serializing analysis results
    """
    serializer = OutputSerializer()
    return serializer.serialize(raw_results, account_data)
