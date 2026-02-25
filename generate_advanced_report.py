#!/usr/bin/env python3
"""
Advanced Analysis Report Generator

Bu script, mevcut analiz verilerini kullanarak gelişmiş analiz raporu üretir.
Promptta belirtilen 11 modülü uygular.

Usage:
    python generate_advanced_report.py <analysis_id>
    python generate_advanced_report.py <json_file>
"""

import json
import os
import sys
from datetime import datetime

# Add agent-orchestrator to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent-orchestrator'))

from agents.advanced_analysis_engine import AdvancedAnalysisEngine, run_advanced_analysis  # type: ignore


def load_analysis_from_json(json_path: str) -> dict:
    """Load analysis data from JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_analysis_from_database(analysis_id: str) -> dict:
    """Load analysis data from PostgreSQL database"""
    import psycopg2  # type: ignore
    
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="instagram_analyzer",
        user="postgres",
        password="postgres123"
    )
    
    cursor = conn.cursor()
    
    # Get analysis data
    cursor.execute("""
        SELECT a.id, a.status, a.overall_score, a.health_grade, 
               a.agent_results, a.eli5_report, a.created_at,
               ia.username, ia.followers, ia.following, ia.posts_count,
               ia.bio, ia.engagement_rate, ia.avg_likes, ia.avg_comments,
               ia.is_verified, ia.is_business, ia.category
        FROM analyses a
        JOIN instagram_accounts ia ON a.account_id = ia.id
        WHERE a.id = %s
    """, (analysis_id,))
    
    row = cursor.fetchone()
    
    if not row:
        raise ValueError(f"Analysis not found: {analysis_id}")
    
    (analysis_id, status, overall_score, health_grade, agent_results,
     eli5_report, created_at, username, followers, following, posts_count,
     bio, engagement_rate, avg_likes, avg_comments, is_verified, 
     is_business, category) = row
    
    cursor.close()
    conn.close()
    
    return {
        "analysisId": analysis_id,
        "accountOverview": {
            "username": username,
            "bio": bio or "",
            "statistics": {
                "followers": followers,
                "following": following,
                "posts": posts_count,
                "engagementRate": float(engagement_rate or 0),
                "avgLikes": float(avg_likes or 0),
                "avgComments": float(avg_comments or 0),
            },
            "isVerified": is_verified,
            "isBusiness": is_business,
            "category": category
        },
        "overallAssessment": {
            "healthScore": overall_score,
            "grade": health_grade
        },
        "agentAnalyses": agent_results if isinstance(agent_results, dict) else {},
        "eli5Report": eli5_report if isinstance(eli5_report, dict) else {}
    }


def extract_account_data(data: dict) -> dict:
    """Extract account data from analysis data"""
    if "accountOverview" in data:
        overview = data["accountOverview"]
        stats = overview.get("statistics", {})
        return {
            "username": overview.get("username", "unknown"),
            "bio": overview.get("bio", ""),
            "followers": stats.get("followers", 0),
            "following": stats.get("following", 0),
            "posts": stats.get("posts", 0),
            "engagementRate": stats.get("engagementRate", 0),
            "avgLikes": stats.get("avgLikes", 0),
            "avgComments": stats.get("avgComments", 0),
            "isVerified": overview.get("isVerified", False),
            "isBusiness": overview.get("isBusiness", False),
            "category": overview.get("category", "unknown")
        }
    else:
        # Direct format
        return data


def extract_agent_results(data: dict) -> dict:
    """Extract agent results from analysis data"""
    if "agentAnalyses" in data:
        return data["agentAnalyses"]
    elif "agent_details" in data:
        return data["agent_details"]
    elif "agentResults" in data:
        return data["agentResults"]
    else:
        return data


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_advanced_report.py <analysis_id_or_json_file>")
        print("\nExamples:")
        print("  python generate_advanced_report.py 2d778291-16d0-41df-94c6-1e2716133bbc")
        print("  python generate_advanced_report.py full_report_2d778291.json")
        sys.exit(1)
    
    input_source = sys.argv[1]
    
    print("=" * 60)
    print("ADVANCED ANALYSIS REPORT GENERATOR")
    print("=" * 60)
    
    # Load data
    print(f"\n📥 Loading data from: {input_source}")
    
    if input_source.endswith('.json'):
        data = load_analysis_from_json(input_source)
        analysis_id = data.get("reportMetadata", {}).get("analysisId", input_source[:8])
    else:
        analysis_id = input_source
        data = load_analysis_from_database(analysis_id)
    
    # Extract components
    account_data = extract_account_data(data)
    agent_results = extract_agent_results(data)
    
    print(f"✓ Loaded data for @{account_data.get('username', 'unknown')}")
    print(f"  - Followers: {account_data.get('followers', 0):,}")
    print(f"  - Engagement Rate: {account_data.get('engagementRate', 0):.2f}%")
    print(f"  - Agent Results: {len(agent_results)} agents")
    
    # Run advanced analysis
    print("\n🔬 Running Advanced Analysis Engine...")
    print("   Analyzing 11 modules:")
    print("   1. Bot ve Fake Follower Tespiti")
    print("   2. Engagement Rate Benchmarking")
    print("   3. Bio/Profil Tutarlılık Kontrolü")
    print("   4. Hashtag Stratejisi Analizi")
    print("   5. İçerik Formatı Kullanımı")
    print("   6. İçerik Kalitesi Dağılımı")
    print("   7. Shadowban Risk Göstergeleri")
    print("   8. Öncelikli Eylem Önerileri")
    print("   9. Viral Potansiyel Analizi")
    print("   10. Açıklama ve Gerekçe")
    print("   11. Veri Kalitesi Skoru")
    
    report = run_advanced_analysis(analysis_id, account_data, agent_results)
    
    # Display summary
    print("\n" + "=" * 60)
    print("📊 ANALYSIS RESULTS")
    print("=" * 60)
    
    overall = report.get("overallAssessment", {})
    print(f"\n🎯 Overall Score: {overall.get('healthScore', 0)}/100 ({overall.get('grade', 'F')})")
    print(f"   Verdict: {overall.get('verdict', 'UNKNOWN')}")
    print(f"   Confidence: {overall.get('confidenceLevel', 0):.0%}")
    
    # Key issues
    key_issues = report.get("keyIssues", [])
    if key_issues:
        print(f"\n⚠️ Key Issues ({len(key_issues)}):")
        for i, issue in enumerate(key_issues[:5], 1):
            print(f"   {i}. {issue}")
    
    # Risk Assessment
    risk = report.get("riskAssessments", {})
    print(f"\n🔴 Risk Levels:")
    print(f"   - Overall Risk: {risk.get('overallRiskLevel', 'unknown').upper()}")
    print(f"   - Bot Risk: {risk.get('botRisk', 'unknown').upper()}")
    print(f"   - Shadowban Risk: {risk.get('shadowbanRisk', 'unknown').upper()}")
    print(f"   - Algorithm Penalty: {risk.get('algorithmPenaltyRisk', 'unknown').upper()}")
    
    # Top recommendations
    recs = report.get("prioritizedRecommendations", {})
    quick_wins = recs.get("quickWins", [])
    all_recs = recs.get("allRecommendations", [])
    
    if quick_wins:
        print(f"\n⚡ Quick Wins ({len(quick_wins)}):")
        for i, rec in enumerate(quick_wins[:3], 1):
            print(f"   {i}. {rec.get('action', rec)}")
    
    if all_recs:
        print(f"\n📋 Top Priority Actions:")
        for i, rec in enumerate(all_recs[:5], 1):
            print(f"   {i}. [{rec.get('priority', '?')}] {rec.get('action', rec)}")
            if rec.get('expectedImpact'):
                print(f"      Expected: {rec.get('expectedImpact')}")
    
    # Detailed findings summary
    findings = report.get("detailedFindings", {})
    
    print("\n📈 Detailed Analysis Summary:")
    
    # Bot Analysis
    bot = findings.get("botAndAuthenticity", {})
    if bot:
        print(f"   - Bot Score: {bot.get('bot_score', 0)}/100")
        print(f"   - Authenticity: {bot.get('authenticity_score', 0)}/100")
        fb = bot.get("follower_breakdown", {})
        print(f"   - Real Followers: ~{fb.get('real', 0)}%")
    
    # Engagement
    eng = findings.get("engagementBenchmarks", {})
    if eng:
        print(f"   - Engagement Rate: {eng.get('current_engagement_rate', 0):.2f}%")
        print(f"   - vs Average: {eng.get('vs_average_pct', 0):.1f}%")
        print(f"   - Percentile: {eng.get('percentile', 0):.0f}")
    
    # Content Formats
    fmt = findings.get("contentFormats", {})
    if fmt:
        mix = fmt.get("current_mix", {})
        print(f"   - Reels: {mix.get('reels', 0)}%")
        print(f"   - Carousel: {mix.get('carousel', 0)}%")
    
    # Save to file
    output_file = f"advanced_report_{analysis_id[:8]}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Advanced report saved to: {output_file}")
    print(f"   Size: {os.path.getsize(output_file):,} bytes")
    
    # Statistics
    total_findings = len(report.get("findings", []))
    total_recs = len(all_recs)
    
    print(f"\n📊 Report Statistics:")
    print(f"   - Total Findings: {total_findings}")
    print(f"   - Total Recommendations: {total_recs}")
    print(f"   - Analysis Modules: 11")
    
    print("\n" + "=" * 60)
    print("✨ ADVANCED ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
