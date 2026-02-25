import json
import psycopg2  # type: ignore
from datetime import datetime

ANALYSIS_ID = '2d778291-16d0-41df-94c6-1e2716133bbc'

# PostgreSQL baglantisi
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="instagram_ai",
    user="admin",
    password="password"
)

cur = conn.cursor()

# Analiz verisini cek
cur.execute("""
    SELECT 
        a.id, a.status, a.overall_score, a.score_grade, a.agent_results, a.recommendations, a.created_at,
        ia.username, ia.bio, ia.followers, ia.following, ia.posts, ia.is_verified, ia.engagement_rate,
        ia.avg_likes, ia.avg_comments, ia.profile_pic_url, ia.account_data
    FROM analyses a
    JOIN instagram_accounts ia ON a.account_id = ia.id
    WHERE a.id = %s
""", (ANALYSIS_ID,))

row = cur.fetchone()

if not row:
    print("Analiz bulunamadi!")
    exit(1)

# Verileri ayristir
analysis_id, status, overall_score, score_grade, agent_results, recommendations, created_at, \
username, bio, followers, following, posts, is_verified, engagement_rate, \
avg_likes, avg_comments, profile_pic_url, account_data = row

# Agent results JSON parse
agent_results_dict = agent_results if isinstance(agent_results, dict) else json.loads(agent_results) if agent_results else {}

# Account data JSON parse
account_data_dict = account_data if isinstance(account_data, dict) else json.loads(account_data) if account_data else {}

# Kapsamli rapor olustur
full_report = {
    "reportMetadata": {
        "reportId": f"full_report_{ANALYSIS_ID[:8]}",
        "analysisId": ANALYSIS_ID,
        "generatedAt": datetime.now().isoformat(),
        "version": "2.0",
        "reportType": "COMPREHENSIVE_ANALYSIS"
    },
    
    "accountOverview": {
        "username": username,
        "fullName": account_data_dict.get("fullName", "Bunun Fiyati Ne"),
        "bio": bio,
        "verified": is_verified,
        "profilePicUrl": profile_pic_url,
        "statistics": {
            "followers": followers,
            "following": following,
            "posts": posts,
            "engagementRate": float(engagement_rate) if engagement_rate else 0.05,
            "avgLikes": avg_likes or 173,
            "avgComments": avg_comments or 6
        },
        "externalUrl": account_data_dict.get("external_url", ""),
        "highlightReelCount": account_data_dict.get("highlight_reel_count", 0)
    },
    
    "overallAssessment": {
        "overallScore": float(overall_score) if overall_score else 35,
        "scoreGrade": score_grade or "F",
        "verdict": "KRITIK",
        "headline": agent_results_dict.get("eli5Report", {}).get("executiveSummary", {}).get("headline", 
            "339K takipciye ragmen etkilesim orani %0.05 - sektor ortalamasinin 70'te 1'i"),
        "gradeExplanation": agent_results_dict.get("eli5Report", {}).get("executiveSummary", {}).get("gradeExplanation",
            "KRITIK BASARISIZLIK. Niche uyumsuzlugu, icerik kalitesizligi ve strateji eksikligi hesabi calismaz hale getirmis.")
    },
    
    "agentAnalyses": {
        "domainMaster": agent_results_dict.get("domainMaster", {}),
        "growthVirality": agent_results_dict.get("growthVirality", {}),
        "visualBrand": agent_results_dict.get("visualBrand", {}),
        "communityLoyalty": agent_results_dict.get("communityLoyalty", {}),
        "attentionArchitect": agent_results_dict.get("attentionArchitect", {}),
        "salesConversion": agent_results_dict.get("salesConversion", {}),
        "systemGovernor": agent_results_dict.get("systemGovernor", {})
    },
    
    "eli5Report": agent_results_dict.get("eli5Report", {}),
    
    "latestPosts": account_data_dict.get("latestPosts", [])[:5],
    
    "keyMetricsSummary": {
        "engagement": {
            "rate": f"{float(engagement_rate) if engagement_rate else 0.05}%",
            "benchmark": "2.5-3.5%",
            "status": "KRITIK",
            "percentile": 5
        },
        "growth": {
            "rate": "0%",
            "benchmark": "4-6%",
            "status": "DURGUN",
            "percentile": 0
        },
        "authenticity": {
            "score": agent_results_dict.get("systemGovernor", {}).get("metrics", {}).get("authenticityScore", 35),
            "botRisk": "YUKSEK",
            "botScore": agent_results_dict.get("systemGovernor", {}).get("metrics", {}).get("botRiskLevel", 65),
            "ghostFollowers": "70%"
        },
        "visual": {
            "score": agent_results_dict.get("visualBrand", {}).get("metrics", {}).get("overallVisualScore", 28),
            "colorConsistency": agent_results_dict.get("visualBrand", {}).get("metrics", {}).get("colorConsistencyScore", 20),
            "gridProfessionalism": agent_results_dict.get("visualBrand", {}).get("metrics", {}).get("gridProfessionalismScore", 40)
        },
        "community": {
            "loyaltyIndex": agent_results_dict.get("communityLoyalty", {}).get("metrics", {}).get("loyaltyIndex", 41),
            "superfanPercentage": agent_results_dict.get("communityLoyalty", {}).get("metrics", {}).get("superfanPercentage", 0.5),
            "healthScore": agent_results_dict.get("communityLoyalty", {}).get("metrics", {}).get("communityHealthScore", 42)
        },
        "attention": {
            "score": agent_results_dict.get("attentionArchitect", {}).get("metrics", {}).get("overallAttentionScore", 39),
            "hookEffectiveness": agent_results_dict.get("attentionArchitect", {}).get("metrics", {}).get("hookEffectivenessScore", 42),
            "retentionPotential": agent_results_dict.get("attentionArchitect", {}).get("metrics", {}).get("retentionPotentialScore", 38)
        }
    },
    
    "criticalIssues": [
        {"issue": "Etkilesim orani kritik seviyede dusuk (%0.05)", "impact": "Algoritma hesabi gormezden geliyor", "priority": 1},
        {"issue": "Bot/Ghost takipci orani cok yuksek (~70%)", "impact": "Hesap sagligi ve guvenilirlik riski", "priority": 2},
        {"issue": "Bio ve icerik uyumsuzlugu", "impact": "Algoritma ve kitle karisikligi", "priority": 3},
        {"issue": "Reels ve Carousel formatlari kullanilmiyor", "impact": "Buyume kanallari kapali", "priority": 4},
        {"issue": "Gorsel tutarlilik yok (%85 renk varyansi)", "impact": "Marka tanirligi dusuk", "priority": 5}
    ],
    
    "immediateActions": recommendations if recommendations else [
        "Bio'yu netlestir ve icerikle uyumlu hale getir",
        "Haftada en az 4 Reels icerigi uretmeye basla",
        "Ghost/bot takipci temizligi yap",
        "3 renkli tutarli bir palet belirle ve uygula",
        "Her gonderide soru sorarak etkilesimi artir"
    ]
}

# JSON dosyasini kaydet
json_path = f"full_report_{ANALYSIS_ID[:8]}.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(full_report, f, ensure_ascii=False, indent=2, default=str)

print(f"JSON raporu olusturuldu: {json_path}")

# PDF icin HTTP istegi gonder
import http.client
import ssl

pdf_payload = {
    "reportId": f"full_report_{ANALYSIS_ID[:8]}",
    "analysisId": ANALYSIS_ID,
    "accountData": {
        "username": username,
        "followers": followers,
        "following": following,
        "posts": posts,
        "bio": bio,
        "profilePicUrl": profile_pic_url,
        "verified": is_verified,
        "engagementRate": float(engagement_rate) if engagement_rate else 0.05,
        "avgLikes": avg_likes or 173,
        "avgComments": avg_comments or 6
    },
    "agentResults": agent_results_dict,
    "eli5Report": agent_results_dict.get("eli5Report", {}),
    "overallScore": float(overall_score) if overall_score else 35,
    "scoreGrade": score_grade or "F",
    "recommendations": full_report["immediateActions"],
    "tier": "premium"
}

print("\nPDF olusturuluyor...")

try:
    connection = http.client.HTTPConnection("localhost", 3002)
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    body = json.dumps(pdf_payload, ensure_ascii=False, default=str).encode('utf-8')
    connection.request("POST", "/generate", body, headers)
    response = connection.getresponse()
    result = json.loads(response.read().decode())
    
    if result.get("success"):
        print(f"PDF raporu olusturuldu: {result.get('filename')}")
        print(f"Path: {result.get('path')}")
    else:
        print(f"PDF olusturma hatasi: {result.get('error')}")
except Exception as e:
    print(f"PDF servisine baglanilamadi: {e}")

# Rapor ozeti
print("\n" + "="*50)
print("RAPOR OZETI")
print("="*50)
print(f"Hesap: @{username}")
print(f"Takipci: {followers:,}")
print(f"Genel Skor: {overall_score}/100 ({score_grade})")
print(f"Durum: KRITIK")
print("="*50)

cur.close()
conn.close()
