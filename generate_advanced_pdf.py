#!/usr/bin/env python3
"""
Advanced Report PDF Generator

Bu script advanced analysis raporunu PDF formatına dönüştürür.
HTTP isteği ile pdf-generator servisine gönderir.

Usage:
    python generate_advanced_pdf.py advanced_report_2d778291.json
"""

import json
import os
import sys
import requests
from datetime import datetime


def convert_advanced_report_to_pdf_payload(advanced_report: dict) -> dict:
    """
    Advanced Analysis Engine raporunu PDF generator payload formatına dönüştürür
    """
    
    # Executive summary
    exec_summary = advanced_report.get("executiveSummary", {})
    
    # Risk assessments
    risk = advanced_report.get("riskAssessments", {})
    
    # Detailed findings
    findings = advanced_report.get("detailedFindings", {})
    
    # Recommendations
    recs = advanced_report.get("prioritizedRecommendations", {})
    all_recs = recs.get("allRecommendations", [])
    
    # Strategies
    strategies = advanced_report.get("strategies", {})
    
    # Monitoring
    monitoring = advanced_report.get("monitoringAndFollowUp", {})
    
    # Construct ELI5-like report for PDF
    eli5_report = {
        "executiveSummary": {
            "headline": exec_summary.get("summaryText", "Analiz raporu"),
            "grade": exec_summary.get("healthGrade", "F"),
            "gradeExplanation": f"Hesap sağlık skoru: {exec_summary.get('healthScore', 0)}/100 - {exec_summary.get('verdict', 'Değerlendirme')}",
            "topStrengths": exec_summary.get("keyStrengths", []),
            "criticalIssues": exec_summary.get("criticalIssues", []),
            "quickWins": [r.get("action", "") for r in recs.get("quickWins", [])]
        },
        "simplifiedMetrics": {
            "engagement": {
                "value": f"{findings.get('engagementBenchmarks', {}).get('current_engagement_rate', 0):.2f}%",
                "verdict": "Kritik" if findings.get('engagementBenchmarks', {}).get('is_critical') else ("Düşük" if findings.get('engagementBenchmarks', {}).get('is_below_average') else "Normal"),
                "explanation": f"Niche ortalamasının %{findings.get('engagementBenchmarks', {}).get('vs_average_pct', 0):.1f}'i",
                "benchmark": f"Niche ortalaması: {findings.get('engagementBenchmarks', {}).get('benchmarks', {}).get('avg', 2.5)}%"
            },
            "growth": {
                "value": f"Risk: {risk.get('shadowbanRisk', 'unknown').upper()}",
                "verdict": "Tehlikeli" if risk.get('shadowbanRisk') in ['high', 'critical'] else "Normal",
                "explanation": f"Shadowban risk skoru: {findings.get('shadowbanRisk', {}).get('risk_score', 0)}/100",
                "benchmark": "Risk skoru 50'nin altında olmalı"
            },
            "contentQuality": {
                "value": f"Reels: {findings.get('contentFormats', {}).get('current_mix', {}).get('reels', 0)}%",
                "verdict": "Kritik Eksik" if findings.get('contentFormats', {}).get('current_mix', {}).get('reels', 0) == 0 else "Geliştirilebilir",
                "explanation": f"Optimal: {findings.get('contentFormats', {}).get('optimal_mix', {}).get('reels', 45)}%",
                "benchmark": "Reels oranı min. %30-45 olmalı"
            },
            "audienceQuality": {
                "value": f"Gerçek: ~{findings.get('botAndAuthenticity', {}).get('follower_breakdown', {}).get('real', 'N/A')}%",
                "verdict": "Zayıf" if int(findings.get('botAndAuthenticity', {}).get('follower_breakdown', {}).get('real', '0') or '0') < 50 else "Kabul Edilebilir",
                "explanation": f"Bot skoru: {findings.get('botAndAuthenticity', {}).get('bot_score', 0)}/100",
                "benchmark": "Gerçek takipçi oranı min. %70 olmalı"
            }
        },
        "actionPlan": {
            "thisWeek": [
                r.get("action", "") 
                for r in all_recs 
                if r.get("timeframe") in ["immediate", "1-2 weeks"]
            ][:5],
            "thisMonth": [
                r.get("action", "") 
                for r in all_recs 
                if r.get("timeframe") == "1-3 months"
            ][:5],
            "avoid": findings.get('shadowbanRisk', {}).get('mitigation_strategies', [])[:3]
        },
        "motivationalNote": "Bu analiz raporunda belirtilen önerileri uygulayarak hesabınızın sağlığını iyileştirebilirsiniz. Önce quick-win aksiyonlardan başlayın!"
    }
    
    # Construct agent results for detailed section
    agent_results = {
        "advancedAnalysis": {
            "agentName": "Advanced Analysis Engine",
            "agentRole": "Kapsamlı hesap analizi ve öneri sistemi",
            "score": advanced_report.get("overallAssessment", {}).get("healthScore", 0),
            "findings": [
                {
                    "type": "issue" if f.get("severity") in ["high", "critical"] else "insight",
                    "finding": f.get("title", ""),
                    "severity": f.get("severity", "medium"),
                    "evidence": f.get("evidence", []),
                    "rationale": f.get("rationale", "")
                }
                for f in advanced_report.get("findings", [])
            ],
            "recommendations": [
                {
                    "priority": r.get("priority", 5),
                    "recommendation": r.get("action", ""),
                    "description": r.get("description", ""),
                    "impact": r.get("expectedImpact", ""),
                    "steps": r.get("implementationSteps", [])
                }
                for r in all_recs
            ],
            "metrics": {
                "botScore": findings.get("botAndAuthenticity", {}).get("bot_score", 0),
                "authenticityScore": findings.get("botAndAuthenticity", {}).get("authenticity_score", 0),
                "engagementRate": findings.get("engagementBenchmarks", {}).get("current_engagement_rate", 0),
                "vsNicheAverage": findings.get("engagementBenchmarks", {}).get("vs_average_pct", 0),
                "shadowbanRiskScore": findings.get("shadowbanRisk", {}).get("risk_score", 0),
                "hashtagEffectiveness": findings.get("hashtagStrategy", {}).get("effectiveness_score", 0),
                "contentBalanceScore": findings.get("contentDistribution", {}).get("balance_score", 0),
                "viralReadiness": findings.get("viralPotential", {}).get("viral_readiness_score", 0)
            }
        },
        "riskAssessment": {
            "agentName": "Risk Assessment",
            "agentRole": "Risk değerlendirmesi",
            "findings": [
                {"type": "risk", "finding": f"{rf.get('factor', '')} (Severity: {rf.get('severity', 'medium')}, Impact: {rf.get('impact', 0)}/100)"}
                for rf in risk.get("riskFactors", [])
            ],
            "metrics": {
                "overallRisk": risk.get("overallRiskLevel", "unknown"),
                "botRisk": risk.get("botRisk", "unknown"),
                "shadowbanRisk": risk.get("shadowbanRisk", "unknown"),
                "algorithmPenaltyRisk": risk.get("algorithmPenaltyRisk", "unknown")
            }
        }
    }
    
    # Content plan from strategies
    content_strategy = strategies.get("content", {})
    weekly_calendar = content_strategy.get("weeklyContentCalendar", {})
    
    content_plan = {
        "weeklyPlan": [
            {
                "day": i + 1,
                "dayName": day.capitalize(),
                "contentType": content.split(" - ")[0] if " - " in content else "İçerik",
                "topic": content.split(" - ")[1] if " - " in content else content,
                "hook": "Hook örneği",
                "caption": content,
                "hashtags": findings.get("hashtagStrategy", {}).get("recommendations", {}).get("suggested_sets", [{}])[0].get("hashtags", [])[:5],
                "bestTime": content_strategy.get("postingTimes", {}).get("optimal", ["20:00"])[0],
                "objective": "Engagement ve erişim artışı"
            }
            for i, (day, content) in enumerate(weekly_calendar.items())
        ] if weekly_calendar else [],
        "monthlyTheme": "Hesap sağlığını iyileştirme ve engagement artışı",
        "contentPillars": [p.get("pillar", "") for p in content_strategy.get("contentPillars", [])]
    }
    
    # Account data
    quick_stats = exec_summary.get("quickStats", {})
    account_data = {
        "username": exec_summary.get("account", "unknown"),
        "followers": findings.get("engagementBenchmarks", {}).get("followers", 0),
        "engagementRate": findings.get("engagementBenchmarks", {}).get("current_engagement_rate", 0),
        "avgLikes": findings.get("engagementBenchmarks", {}).get("avg_likes", 0),
        "avgComments": findings.get("engagementBenchmarks", {}).get("avg_comments", 0)
    }
    
    # Final payload
    payload = {
        "reportId": advanced_report.get("reportMetadata", {}).get("reportId", "advanced_report"),
        "analysisId": advanced_report.get("reportMetadata", {}).get("analysisId", "unknown"),
        "accountData": account_data,
        "agentResults": agent_results,
        "eli5Report": eli5_report,
        "contentPlan": content_plan,
        "overallScore": advanced_report.get("overallAssessment", {}).get("healthScore", 0),
        "scoreGrade": advanced_report.get("overallAssessment", {}).get("grade", "F"),
        "recommendations": [r.get("action", "") for r in all_recs[:10]],
        "tier": "premium"
    }
    
    return payload


def generate_pdf(payload: dict, output_path: str) -> bool:
    """
    PDF generator servisine istek gönderir ve PDF'i kaydeder
    """
    pdf_service_url = "http://localhost:3002/generate"
    
    try:
        response = requests.post(
            pdf_service_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success") and result.get("pdfBuffer"):
                import base64
                pdf_bytes = base64.b64decode(result["pdfBuffer"])
                with open(output_path, 'wb') as f:
                    f.write(pdf_bytes)
                return True
            else:
                print(f"PDF generation failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Error: PDF generator service is not running on port 3002")
        print("Start the service with: docker-compose up pdf-generator")
        return False
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_advanced_pdf.py <advanced_report.json>")
        print("\nExample:")
        print("  python generate_advanced_pdf.py advanced_report_2d778291.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    print("=" * 60)
    print("ADVANCED REPORT PDF GENERATOR")
    print("=" * 60)
    
    # Load advanced report
    print(f"\n📥 Loading: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        advanced_report = json.load(f)
    
    # Get username and analysis ID
    exec_summary = advanced_report.get("executiveSummary", {})
    username = exec_summary.get("account", "unknown")
    analysis_id = advanced_report.get("reportMetadata", {}).get("analysisId", "unknown")[:8]
    
    print(f"✓ Loaded report for @{username}")
    print(f"  - Health Score: {exec_summary.get('healthScore', 0)}/100 ({exec_summary.get('healthGrade', 'F')})")
    
    # Convert to PDF payload
    print("\n🔄 Converting to PDF format...")
    payload = convert_advanced_report_to_pdf_payload(advanced_report)
    
    # Save payload for debugging
    payload_file = f"pdf_payload_{analysis_id}.json"
    with open(payload_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"✓ Payload saved: {payload_file}")
    
    # Generate PDF
    output_pdf = f"advanced_report_{analysis_id}.pdf"
    print(f"\n📄 Generating PDF: {output_pdf}")
    
    success = generate_pdf(payload, output_pdf)
    
    if success:
        file_size = os.path.getsize(output_pdf)
        print(f"✅ PDF generated successfully!")
        print(f"   File: {output_pdf}")
        print(f"   Size: {file_size:,} bytes")
    else:
        print("❌ PDF generation failed")
        print("\nAlternative: You can manually send the payload to the PDF service")
        print(f"Payload file: {payload_file}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
