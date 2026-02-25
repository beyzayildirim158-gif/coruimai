# Advanced Analysis Engine - Sistem Dokümantasyonu

## Genel Bakış

Advanced Analysis Engine, Instagram hesap analizinde kapsamlı ve yapılandırılmış bulgular, öncelikli öneriler ve stratejiler sunan yeni bir analiz modülüdür. Kullanıcının promptunda belirtilen 11 temel modülü uygular.

## Uygulanan Modüller

### 1. Bot ve Fake Follower Tespiti (`_analyze_bot_activity`)
- Bot skoru hesaplama
- Takipçi kalite değerlendirmesi
- Ghost follower tahmini
- Engagement pod tespiti
- Hesap askıya alma risk değerlendirmesi

### 2. Engagement Rate Benchmarking (`_analyze_engagement_benchmarks`)
- Niche bazlı benchmark karşılaştırması
- Percentile hesaplama
- Algoritma cezası risk değerlendirmesi
- Kritik düşük engagement tespiti

### 3. Bio ve İçerik Tutarlılık (`_analyze_profile_consistency`)
- Bio-içerik niche uyumu
- CTA eksikliği kontrolü
- Anahtar kelime analizi
- Profil optimizasyon önerileri

### 4. Hashtag Stratejisi (`_analyze_hashtag_strategy`)
- Mevcut vs optimal dağılım
- Mikro-niche hashtag eksikliği
- Mega hashtag fazlalığı
- Önerilen hashtag setleri

### 5. İçerik Formatı Kullanımı (`_analyze_content_formats`)
- Reels, Carousel, Single Post dağılımı
- Format boşlukları
- Büyüme kanalı potansiyelleri
- Haftalık hedefler

### 6. İçerik Kalitesi ve Dağılımı (`_analyze_content_distribution`)
- Eğitici, eğlence, tanıtım dengesi
- Content pillar analizi
- Dengesizlik tespiti
- Haftalık içerik mix önerisi

### 7. Shadowban ve Algoritma Riski (`_analyze_shadowban_risk`)
- Risk skoru hesaplama
- Göstergeler analizi
- Platform riski değerlendirmesi
- Azaltma stratejileri

### 8. Öncelikli Eylem Önerileri (`_prioritize_recommendations`)
- Priority bazlı sıralama
- Quick wins belirleme
- Timeframe kategorileme (immediate, short-term, medium-term)
- Implementation steps

### 9. Viral Potansiyel (`_analyze_viral_potential`)
- Viral katsayı hesaplama
- Hook etkinliği
- Paylaşılabilirlik skoru
- Viral içerik blueprint'leri

### 10. Açıklama ve Gerekçe
- Her bulgu için rationale
- Her öneri için expected impact
- Kanıt ve metrik destekli açıklamalar

### 11. Veri Kalitesi ve Güven (`_assess_data_quality`)
- Veri tamlığı kontrolü
- Agent kapsam değerlendirmesi
- Genel güven skoru

## Dosya Yapısı

```
instagram-ai-system/
├── agent-orchestrator/
│   └── agents/
│       ├── advanced_analysis_engine.py  # Ana modül (1700+ satır)
│       ├── orchestrator.py              # Entegrasyon noktası
│       └── __init__.py                  # Export'lar
├── generate_advanced_report.py          # CLI rapor üretici
├── generate_advanced_pdf.py             # PDF dönüştürücü
└── ADVANCED_ANALYSIS_README.md          # Bu dosya
```

## Kullanım

### Python API

```python
from agents.advanced_analysis_engine import run_advanced_analysis

# Analiz çalıştır
report = run_advanced_analysis(
    analysis_id="your-analysis-id",
    account_data={
        "username": "hesap_adi",
        "followers": 100000,
        "engagementRate": 2.5,
        # ...
    },
    agent_results={
        "systemGovernor": {...},
        "domainMaster": {...},
        # ...
    }
)

# Sonuç yapısı
print(report["executiveSummary"])
print(report["detailedFindings"])
print(report["prioritizedRecommendations"])
```

### CLI Kullanımı

```bash
# JSON'dan gelişmiş analiz raporu oluştur
python generate_advanced_report.py full_report_2d778291.json

# Veritabanından analiz ID ile
python generate_advanced_report.py 2d778291-16d0-41df-94c6-1e2716133bbc

# PDF oluştur
python generate_advanced_pdf.py advanced_report_2d778291.json
```

### Orchestrator Entegrasyonu

```python
from agents import AgentOrchestrator

orchestrator = AgentOrchestrator(redis_client=None)

# Gelişmiş analiz raporu oluştur
advanced_report = await orchestrator.generate_advanced_analysis(
    account_data=account_data,
    agent_results=agent_results,  # Opsiyonel
    analysis_id="custom-id",
    run_analysis_if_needed=True
)
```

## Rapor Yapısı

```json
{
  "reportMetadata": {
    "reportId": "advanced_analysis_xxx",
    "analysisId": "uuid",
    "version": "3.0",
    "reportType": "ADVANCED_COMPREHENSIVE_ANALYSIS"
  },
  
  "executiveSummary": {
    "account": "username",
    "healthScore": 35,
    "healthGrade": "F",
    "verdict": "KRİTİK",
    "summaryText": "...",
    "criticalIssues": [...],
    "keyStrengths": [...],
    "immediateActions": [...],
    "riskOverview": {...},
    "quickStats": {...}
  },
  
  "keyIssues": ["Issue 1", "Issue 2", ...],
  
  "overallAssessment": {
    "healthScore": 35,
    "grade": "F",
    "verdict": "KRİTİK",
    "confidenceLevel": 0.85
  },
  
  "detailedFindings": {
    "botAndAuthenticity": {...},
    "engagementBenchmarks": {...},
    "profileConsistency": {...},
    "hashtagStrategy": {...},
    "contentFormats": {...},
    "contentDistribution": {...},
    "shadowbanRisk": {...},
    "viralPotential": {...}
  },
  
  "riskAssessments": {
    "overallRiskLevel": "high",
    "botRisk": "medium",
    "shadowbanRisk": "high",
    "algorithmPenaltyRisk": "critical",
    "riskFactors": [...]
  },
  
  "prioritizedRecommendations": {
    "quickWins": [...],
    "shortTerm": [...],
    "mediumTerm": [...],
    "longTerm": [...],
    "allRecommendations": [...]
  },
  
  "strategies": {
    "content": {...},
    "growth": {...},
    "engagement": {...},
    "community": {...}
  },
  
  "monitoringAndFollowUp": {
    "keyMetricsToTrack": [...],
    "reviewSchedule": {...},
    "alertThresholds": {...}
  },
  
  "dataQuality": {
    "overall_confidence": 0.85,
    "data_completeness": 1.0,
    "agent_coverage": 0.875
  },
  
  "findings": [...],  // Tüm bulgular detaylı
  
  "actionPlan": {
    "immediate": {...},
    "shortTerm": {...},
    "mediumTerm": {...},
    "quickWins": [...]
  }
}
```

## Benchmark Değerleri

### Engagement Rate (Niche Bazlı)
| Niche | Ortalama | Top 25% | Top 10% |
|-------|----------|---------|---------|
| Default | 2.5% | 4.0% | 6.0% |
| Shopping/Deals | 2.5% | 3.5% | 5.0% |
| Lifestyle | 3.0% | 5.0% | 8.0% |

### İçerik Format Dağılımı (Optimal)
- Reels: 45%
- Carousel: 30%
- Single Post: 15%
- Stories: 10% (günlük ortalama)

### Hashtag Stratejisi (Optimal 25 adet)
- Mega (>10M): 2 adet
- Large (1-10M): 4 adet
- Medium (100K-1M): 10 adet
- Small (10K-100K): 6 adet
- Micro (<10K): 3 adet

### İçerik Ayakları (Content Pillars)
- Eğitici: 40%
- İlham verici: 20%
- Eğlence: 15%
- Tanıtım: 10%
- Topluluk: 15%

## Risk Seviyeleri

| Seviye | Kod | Açıklama |
|--------|-----|----------|
| LOW | low | Düşük risk, normal durum |
| MEDIUM | medium | Orta risk, iyileştirme gerekli |
| HIGH | high | Yüksek risk, acil aksiyon |
| CRITICAL | critical | Kritik risk, öncelikli müdahale |

## Versiyon Geçmişi

### v1.0 (2026-01-17)
- İlk sürüm
- 11 temel modül implementasyonu
- JSON ve PDF rapor desteği
- Orchestrator entegrasyonu
