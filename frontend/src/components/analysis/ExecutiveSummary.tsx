'use client';

import React from 'react';
import { 
  ChartBarIcon, 
  CheckCircleIcon, 
  ExclamationTriangleIcon,
  ArrowTrendingUpIcon,
  ClockIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';
import { useTranslation } from '@/i18n/TranslationProvider';

interface ExecutiveSummaryProps {
  overallScore: number;
  accountHealth: 'iyi' | 'orta' | 'zayıf' | 'good' | 'medium' | 'poor';
  topStrength: string;
  mainIssue: string;
  topAction: string;
  expectedImprovement: string;
  timeframe: string;
  niche?: string;
  nicheAverage?: number;
}

// Utility to determine health status from score
export function getHealthStatus(score: number): 'iyi' | 'orta' | 'zayıf' {
  if (score >= 70) return 'iyi';
  if (score >= 40) return 'orta';
  return 'zayıf';
}

// Get visual indicator emoji based on score
export function getScoreIndicator(score: number): string {
  if (score >= 80) return '🟢';
  if (score >= 60) return '🟡';
  if (score >= 40) return '🟠';
  return '🔴';
}

// Get score label based on locale
export function getScoreLabel(score: number, locale: string = 'tr'): string {
  if (locale === 'en') {
    if (score >= 70) return 'Good';
    if (score >= 40) return 'Needs Improvement';
    return 'Critical';
  }
  if (score >= 70) return 'İyi Seviyede';
  if (score >= 40) return 'Geliştirilmeli';
  return 'Kritik Seviyede';
}

const ExecutiveSummary: React.FC<ExecutiveSummaryProps> = ({
  overallScore,
  accountHealth,
  topStrength,
  mainIssue,
  topAction,
  expectedImprovement,
  timeframe,
  niche,
  nicheAverage,
}) => {
  const { t, locale } = useTranslation();
  
  // Map health status based on locale
  const healthKey = accountHealth === 'good' || accountHealth === 'iyi' ? 'iyi' 
    : accountHealth === 'medium' || accountHealth === 'orta' ? 'orta' : 'zayıf';
  
  const healthColors = {
    'iyi': 'text-green-500 bg-green-500/10 border-green-500/30',
    'orta': 'text-yellow-500 bg-yellow-500/10 border-yellow-500/30',
    'zayıf': 'text-red-500 bg-red-500/10 border-red-500/30',
  };

  const healthIcons = {
    'iyi': '🟢',
    'orta': '🟡',
    'zayıf': '🔴',
  };
  
  const healthLabels = {
    'iyi': locale === 'en' ? 'Good Performance' : 'İyi Performans',
    'orta': locale === 'en' ? 'Needs Improvement' : 'Geliştirilmeli',
    'zayıf': locale === 'en' ? 'Critical - Action Required' : 'Kritik - Aksiyon Gerekli',
  };

  return (
    <div className="rounded-3xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <SparklesIcon className="h-6 w-6 text-primary-500" />
        <h2 className="text-xl font-bold text-slate-900">📊 {t('results.summary')}</h2>
      </div>

      <div className="space-y-4">
        {/* Account Health Score */}
        <div className="flex items-center justify-between p-4 rounded-2xl border border-slate-200 bg-white">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-full ${healthColors[healthKey]}`}>
              <ChartBarIcon className="h-5 w-5" />
            </div>
            <div>
              <span className="text-sm text-slate-500">{t('results.accountHealth')}</span>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-bold text-slate-900">{overallScore}/100</span>
                <span className={`text-sm font-medium px-2 py-0.5 rounded-full ${healthColors[healthKey]}`}>
                  {healthIcons[healthKey]} {healthLabels[healthKey]}
                </span>
              </div>
            </div>
          </div>
          {nicheAverage && (
            <div className="text-right">
              <span className="text-xs text-slate-500 block">{t('results.nicheAverage')}</span>
              <span className="text-lg font-semibold text-slate-600">{nicheAverage}/100</span>
            </div>
          )}
        </div>

        {/* Key Insights Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {/* Top Strength */}
          <div className="p-4 rounded-2xl border border-green-200 bg-green-50/50">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircleIcon className="h-5 w-5 text-green-500" />
              <span className="text-sm font-medium text-green-700">{t('results.topStrength')}</span>
            </div>
            <p className="text-slate-700">{topStrength}</p>
          </div>

          {/* Main Issue */}
          <div className="p-4 rounded-2xl border border-red-200 bg-red-50/50">
            <div className="flex items-center gap-2 mb-2">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
              <span className="text-sm font-medium text-red-700">{t('results.mainIssue')}</span>
            </div>
            <p className="text-slate-700">{mainIssue}</p>
          </div>
        </div>

        {/* Priority Action */}
        <div className="p-4 rounded-2xl border border-primary-200 bg-primary-50/50">
          <div className="flex items-center gap-2 mb-2">
            <ArrowTrendingUpIcon className="h-5 w-5 text-primary-500" />
            <span className="text-sm font-medium text-primary-700">{t('results.priorityAction')}</span>
          </div>
          <p className="text-slate-700 font-medium">{topAction}</p>
        </div>

        {/* Expected Improvement */}
        <div className="p-4 rounded-2xl border border-slate-200 bg-white">
          <div className="flex items-center gap-2 mb-2">
            <ClockIcon className="h-5 w-5 text-slate-500" />
            <span className="text-sm font-medium text-slate-700">{t('results.expectedImprovement')}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-semibold text-green-600">{expectedImprovement}</span>
            <span className="text-sm text-slate-500">({timeframe})</span>
          </div>
        </div>

        {/* Niche Context */}
        {niche && (
          <div className="text-xs text-slate-500 text-center pt-2 border-t border-slate-100">
            📊 {t('results.nicheComparison')} - <span className="font-medium text-slate-700">{niche}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExecutiveSummary;

// Helper function to generate executive summary from analysis data
export function generateExecutiveSummary(analysis: any): ExecutiveSummaryProps {
  const score = analysis.overallScore || 0;
  const accountHealth = getHealthStatus(score);
  
  // Extract top strength from agent results
  let topStrength = 'Analiz verileri değerlendiriliyor...';
  let mainIssue = 'Detaylı analiz sonuçları bekleniyor';
  let topAction = 'Analiz tamamlandıktan sonra öncelikli aksiyonlar belirlenecek';
  
  const agentResults = analysis.agentResults || {};
  
  // Find strengths
  const strengths: string[] = [];
  const issues: string[] = [];
  
  // Check Engagement Rate
  const engagementRate = analysis.account?.engagementRate || 0;
  if (engagementRate > 5) {
    strengths.push(`Olağanüstü etkileşim oranı (%${engagementRate.toFixed(2)}) - sektör ortalamasının çok üzerinde`);
  } else if (engagementRate > 3) {
    strengths.push(`Güçlü etkileşim oranı (%${engagementRate.toFixed(2)}) - takipçileriniz içeriklerinize aktif tepki veriyor`);
  } else if (engagementRate < 1) {
    issues.push(`Düşük etkileşim oranı (%${engagementRate.toFixed(2)}) - içerik stratejisi ve hook'lar gözden geçirilmeli`);
  } else if (engagementRate < 2) {
    issues.push(`Ortalamanın altında etkileşim - caption CTA'ları ve içerik zamanlaması optimize edilmeli`);
  }
  
  // Check Follower/Following Ratio
  const followers = analysis.account?.followers || 0;
  const following = analysis.account?.following || 1;
  const ratio = followers / following;
  if (ratio > 10) {
    strengths.push(`Yüksek takipçi/takip oranı (${ratio.toFixed(1)}x) - güçlü otorite sinyali`);
  } else if (ratio < 0.5) {
    issues.push(`Düşük takipçi/takip oranı - takip stratejinizi gözden geçirin`);
  }
  
  // Check Visual Brand
  if (agentResults.visualBrand) {
    const visualScore = agentResults.visualBrand.metrics?.colorConsistencyScore || agentResults.visualBrand.metrics?.overallVisualScore;
    if (visualScore > 70) {
      strengths.push('Tutarlı görsel marka kimliği - profesyonel grid estetiği');
    } else if (visualScore < 40) {
      issues.push('Görsel tutarlılık eksik - renk paleti ve grid düzeni standardize edilmeli');
    }
  }
  
  // Check Growth
  if (agentResults.growthVirality) {
    const viralScore = agentResults.growthVirality.metrics?.viralPotential;
    if (viralScore > 70) {
      strengths.push('Yüksek viral potansiyel - içerikleriniz paylaşılabilir formatta');
    } else if (viralScore < 40) {
      issues.push('Viral içerik stratejisi geliştirilmeli - paylaşılabilirlik düşük');
    }
  }
  
  // Check Community
  if (agentResults.communityLoyalty) {
    const loyaltyScore = agentResults.communityLoyalty.metrics?.loyaltyIndex;
    if (loyaltyScore > 70) {
      strengths.push('Güçlü topluluk bağlılığı - sadık takipçi kitlesi');
    } else if (loyaltyScore < 40) {
      issues.push('Topluluk bağlılığı düşük - etkileşim artırıcı aktiviteler yapılmalı');
    }
  }
  
  // Check Bot Score
  const botScore = analysis.account?.botScore || 0;
  if (botScore > 40) {
    issues.push(`Yüksek bot riski (%${botScore.toFixed(0)}) - sahte/inaktif takipçiler tespit edildi`);
  } else if (botScore < 20) {
    strengths.push('Düşük bot oranı - organik ve gerçek takipçi kitlesi');
  }
  
  // Set top strength and main issue
  if (strengths.length > 0) {
    topStrength = strengths[0];
  } else if (score >= 50) {
    topStrength = 'Hesabınız genel olarak iyi durumda, optimizasyon fırsatları mevcut';
  }
  
  if (issues.length > 0) {
    mainIssue = issues[0];
  } else if (score >= 70) {
    mainIssue = 'Kritik sorun tespit edilmedi - ince ayar optimizasyonları önerilir';
  }
  
  // Get top action from recommendations
  const recommendations = analysis.recommendations || [];
  if (recommendations.length > 0) {
    const firstRec = recommendations[0];
    topAction = typeof firstRec === 'string' ? firstRec : (firstRec.action || firstRec.recommendation || 'Önerilen aksiyonlar hazırlanıyor...');
  } else if (issues.length > 0) {
    topAction = `"${mainIssue}" sorununu çözmek için stratejik plan oluşturun`;
  }
  
  // Calculate expected improvement based on current score and issues
  let expectedImprovement = '+10-15% etkileşim artışı';
  let timeframe = '4 hafta';
  
  if (score < 30) {
    expectedImprovement = '+100-200% büyüme potansiyeli';
    timeframe = '8-12 hafta yoğun çalışmayla';
  } else if (score < 50) {
    expectedImprovement = '+50-80% etkileşim artışı';
    timeframe = '6-8 hafta';
  } else if (score < 70) {
    expectedImprovement = '+25-40% performans artışı';
    timeframe = '4-6 hafta';
  } else {
    expectedImprovement = '+10-20% optimizasyon';
    timeframe = '2-4 hafta ince ayarla';
  }
  
  return {
    overallScore: Math.round(score),
    accountHealth,
    topStrength,
    mainIssue,
    topAction,
    expectedImprovement,
    timeframe,
    niche: agentResults.domainMaster?.niche_identification?.primary_niche || analysis.account?.niche,
    nicheAverage: agentResults.domainMaster?.metrics?.nicheAverageScore || agentResults.domainMaster?.benchmark_comparison?.overall_benchmark_score,
  };
}
