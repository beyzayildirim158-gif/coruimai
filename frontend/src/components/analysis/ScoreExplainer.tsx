'use client';

import React, { useState } from 'react';
import { 
  ChevronDownIcon,
  ChevronUpIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline';
import { useTranslation } from '@/i18n/TranslationProvider';

export interface ScoreData {
  score: number;
  label: string;
  explanation: string;
  mainIssues?: string[];
  improvements?: string[];
  benchmark?: {
    nicheAverage: number;
    topPerformers: number;
  };
}

interface ScoreExplainerProps {
  scoreData?: ScoreData;
  scores?: ScoreData[];
  showDetails?: boolean;
}

// Get visual indicator based on score
export function getScoreEmoji(score: number): string {
  if (score >= 70) return '🟢';
  if (score >= 40) return '🟡';
  return '🔴';
}

export function getScoreStatus(score: number): 'good' | 'medium' | 'critical' {
  if (score >= 70) return 'good';
  if (score >= 40) return 'medium';
  return 'critical';
}

export function getScoreStatusLabel(score: number, locale: string = 'tr'): string {
  if (locale === 'en') {
    if (score >= 70) return 'Good';
    if (score >= 40) return 'Needs Improvement';
    return 'Critical';
  }
  if (score >= 70) return 'İyi';
  if (score >= 40) return 'Geliştirilmeli';
  return 'Kritik';
}

const statusColors = {
  good: {
    bg: 'bg-green-500/10',
    border: 'border-green-500/30',
    text: 'text-green-600',
    bar: 'bg-gradient-to-r from-green-500 to-emerald-400',
  },
  medium: {
    bg: 'bg-yellow-500/10',
    border: 'border-yellow-500/30',
    text: 'text-yellow-600',
    bar: 'bg-gradient-to-r from-yellow-500 to-amber-400',
  },
  critical: {
    bg: 'bg-red-500/10',
    border: 'border-red-500/30',
    text: 'text-red-600',
    bar: 'bg-gradient-to-r from-red-500 to-rose-400',
  },
};

const ScoreExplainer: React.FC<ScoreExplainerProps> = ({ scoreData, scores, showDetails = true }) => {
  // If scores array is provided, render multiple score items
  if (scores && scores.length > 0) {
    return (
      <div className="space-y-4">
        {scores.map((data, idx) => (
          <ScoreExplainerItem key={idx} scoreData={data} showDetails={showDetails} />
        ))}
      </div>
    );
  }
  
  // Single scoreData
  if (!scoreData) return null;
  return <ScoreExplainerItem scoreData={scoreData} showDetails={showDetails} />;
};

const ScoreExplainerItem: React.FC<{ scoreData: ScoreData; showDetails: boolean }> = ({ scoreData, showDetails }) => {
  const { t, locale } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(false);
  const { score, label, explanation, mainIssues, improvements, benchmark } = scoreData;
  
  const status = getScoreStatus(score);
  const colors = statusColors[status];
  const emoji = getScoreEmoji(score);
  const statusLabel = getScoreStatusLabel(score, locale);
  
  // Calculate position relative to benchmarks
  const benchmarkPosition = benchmark ? {
    belowAverage: score < benchmark.nicheAverage,
    nearTop: score >= benchmark.topPerformers * 0.8,
  } : null;

  return (
    <div className={`rounded-2xl border ${colors.border} ${colors.bg} overflow-hidden`}>
      {/* Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 flex items-center justify-between hover:bg-white/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{emoji}</span>
          <div className="text-left">
            <p className="font-semibold text-slate-900">{label}</p>
            <p className={`text-sm ${colors.text}`}>{statusLabel}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <span className={`text-3xl font-bold ${colors.text}`}>{score}</span>
            <span className="text-slate-400 text-lg">/100</span>
          </div>
          {showDetails && (
            isExpanded ? (
              <ChevronUpIcon className="w-5 h-5 text-slate-400" />
            ) : (
              <ChevronDownIcon className="w-5 h-5 text-slate-400" />
            )
          )}
        </div>
      </button>

      {/* Score Bar */}
      <div className="px-4 pb-3">
        <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
          <div 
            className={`h-full ${colors.bar} rounded-full transition-all duration-500`}
            style={{ width: `${score}%` }}
          />
        </div>
        
        {/* Benchmark Markers */}
        {benchmark && (
          <div className="relative h-6 mt-1">
            {/* Niche Average Marker */}
            <div 
              className="absolute -top-1 flex flex-col items-center"
              style={{ left: `${benchmark.nicheAverage}%`, transform: 'translateX(-50%)' }}
            >
              <div className="w-0.5 h-3 bg-slate-400" />
              <span className="text-[10px] text-slate-500 whitespace-nowrap">
                {t('scores.niche')}: {benchmark.nicheAverage}
              </span>
            </div>
            
            {/* Top Performers Marker */}
            <div 
              className="absolute -top-1 flex flex-col items-center"
              style={{ left: `${benchmark.topPerformers}%`, transform: 'translateX(-50%)' }}
            >
              <div className="w-0.5 h-3 bg-green-500" />
              <span className="text-[10px] text-green-600 whitespace-nowrap">
                {t('scores.best')}: {benchmark.topPerformers}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Expanded Details */}
      {showDetails && isExpanded && (
        <div className="px-4 pb-4 space-y-3 border-t border-slate-200/50 pt-3">
          {/* Explanation */}
          <div className="flex items-start gap-2">
            <InformationCircleIcon className="w-5 h-5 text-slate-400 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-sm font-medium text-slate-700">{t('scores.whyThisScore')}</p>
              <p className="text-sm text-slate-600 mt-1">{explanation}</p>
            </div>
          </div>

          {/* Main Issues */}
          {mainIssues && mainIssues.length > 0 && (
            <div className="flex items-start gap-2">
              <ExclamationTriangleIcon className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-slate-700">{t('scores.mainIssues')}</p>
                <ul className="text-sm text-slate-600 mt-1 space-y-1">
                  {mainIssues.map((issue, idx) => (
                    <li key={idx} className="flex items-start gap-1">
                      <span className="text-red-400">•</span> {issue}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Improvements */}
          {improvements && improvements.length > 0 && (
            <div className="flex items-start gap-2">
              <ArrowTrendingUpIcon className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-slate-700">{t('scores.howToImprove')}</p>
                <ul className="text-sm text-slate-600 mt-1 space-y-1">
                  {improvements.map((imp, idx) => (
                    <li key={idx} className="flex items-start gap-1">
                      <span className="text-green-400">•</span> {imp}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Benchmark Comparison */}
          {benchmark && (
            <div className="bg-white/50 rounded-xl p-3 mt-2">
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2">{t('scores.benchmarkComparison')}</p>
              <div className="grid grid-cols-3 gap-3 text-center">
                <div>
                  <p className="text-lg font-bold text-slate-900">{score}</p>
                  <p className="text-xs text-slate-500">{t('scores.yourScore')}</p>
                </div>
                <div>
                  <p className="text-lg font-bold text-slate-600">{benchmark.nicheAverage}</p>
                  <p className="text-xs text-slate-500">{t('scores.nicheAverage')}</p>
                </div>
                <div>
                  <p className="text-lg font-bold text-green-600">{benchmark.topPerformers}</p>
                  <p className="text-xs text-slate-500">{t('scores.topPerformers')}</p>
                </div>
              </div>
              
              {/* Verdict */}
              <div className="mt-3 pt-2 border-t border-slate-200/50">
                {benchmarkPosition?.belowAverage ? (
                  <div className="flex items-center gap-2 text-sm">
                    <ArrowTrendingDownIcon className="w-4 h-4 text-red-500" />
                    <span className="text-red-600 font-medium">{t('scores.belowAverage')}</span>
                  </div>
                ) : benchmarkPosition?.nearTop ? (
                  <div className="flex items-center gap-2 text-sm">
                    <ArrowTrendingUpIcon className="w-4 h-4 text-green-500" />
                    <span className="text-green-600 font-medium">{t('scores.topLevelPerformance')}</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-2 text-sm">
                    <span className="text-yellow-600 font-medium">{t('scores.aroundAverage')}</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ScoreExplainer;

// Helper to create score data from agent metrics
export function createScoreData(
  label: string,
  score: number,
  context: {
    explanation?: string;
    mainIssues?: string[];
    improvements?: string[];
    nicheAverage?: number;
    topPerformers?: number;
  }
): ScoreData {
  // Generate detailed automatic explanation based on score and label
  let explanation = context.explanation || '';
  
  if (!explanation) {
    // Score-based detailed explanations
    if (score >= 85) {
      explanation = `${label} performansınız mükemmel seviyede! Sektördeki en iyi hesaplarla aynı ligdesiniz. Bu başarıyı sürdürmek için mevcut stratejinize sadık kalın ve küçük optimizasyonlarla daha da ileriye taşıyın.`;
    } else if (score >= 70) {
      explanation = `${label} performansınız iyi seviyede ve sektör ortalamasının üzerinde. Birkaç stratejik iyileştirmeyle üst lige çıkabilirsiniz. Güçlü yönlerinizi korurken zayıf noktaları tespit edin.`;
    } else if (score >= 55) {
      explanation = `${label} performansınız ortalama civarında. Rekabette öne çıkmak için bu alanda ciddi çalışma gerekiyor. Aşağıdaki önerileri uygulayarak 2-4 hafta içinde gözle görülür iyileşme sağlayabilirsiniz.`;
    } else if (score >= 40) {
      explanation = `${label} performansınız sektör ortalamasının altında ve acil iyileştirme gerektiriyor. Bu durum büyüme potansiyelinizi sınırlıyor. Stratejik değişiklikler yapılmazsa rakiplerinizin gerisinde kalma riski yüksek.`;
    } else {
      explanation = `${label} performansınız kritik seviyede ve hesabınızın en zayıf noktalarından biri. Bu alan öncelikli olarak ele alınmalı. İyileştirme yapılmazsa diğer alanlardaki çabalarınız da verimsiz kalacaktır.`;
    }
  }

  return {
    score,
    label,
    explanation,
    mainIssues: context.mainIssues,
    improvements: context.improvements,
    benchmark: context.nicheAverage && context.topPerformers ? {
      nicheAverage: context.nicheAverage,
      topPerformers: context.topPerformers,
    } : undefined,
  };
}

// Enhanced helper to generate contextual score explanations
export function generateScoreInsights(
  category: string,
  score: number,
  metrics?: Record<string, number>
): { issues: string[]; improvements: string[] } {
  const issues: string[] = [];
  const improvements: string[] = [];

  // Category-specific insights
  switch (category.toLowerCase()) {
    case 'engagement':
    case 'etkileşim':
      if (score < 50) {
        issues.push('Etkileşim oranları düşük, içerikler yeterli tepki almıyor');
        issues.push('Hook\'lar yeterince dikkat çekici değil');
        improvements.push('Her içeriğe güçlü CTA (Call to Action) ekleyin');
        improvements.push('Soru soran, tartışma başlatan içerikler üretin');
        improvements.push('Story\'lerde poll, quiz gibi interaktif öğeler kullanın');
      }
      break;
    
    case 'growth':
    case 'büyüme':
      if (score < 50) {
        issues.push('Organik büyüme durağan veya yavaş');
        issues.push('Viral loop oluşmuyor');
        improvements.push('Reels formatına ağırlık verin (algoritma önceliklendiriyor)');
        improvements.push('Trend audio ve formatları takip edin');
        improvements.push('Collaboration içerikleri ile çapraz kitle kazanın');
      }
      break;

    case 'visual':
    case 'görsel':
      if (score < 50) {
        issues.push('Görsel tutarlılık eksik');
        issues.push('Profesyonel marka algısı oluşmuyor');
        improvements.push('3-5 renklik tutarlı bir palet belirleyin');
        improvements.push('Canva/Figma şablonları ile tutarlılık sağlayın');
        improvements.push('Grid estetiğine dikkat edin (9-12 post uyumu)');
      }
      break;

    case 'community':
    case 'topluluk':
      if (score < 50) {
        issues.push('Topluluk bağlılığı zayıf');
        issues.push('Super fan kitlesi oluşmamış');
        improvements.push('Yorumlara hızlı ve anlamlı cevaplar verin');
        improvements.push('DM\'lere gelen sorulara özen gösterin');
        improvements.push('Kullanıcı içeriklerini (UGC) öne çıkarın');
      }
      break;

    case 'sales':
    case 'satış':
      if (score < 50) {
        issues.push('Monetizasyon stratejisi belirsiz');
        issues.push('Satış dönüşümleri düşük');
        improvements.push('Net bir sales funnel oluşturun');
        improvements.push('Sosyal kanıt (testimonial, rakamlar) paylaşın');
        improvements.push('Bio\'daki linki optimize edin, CTA netleştirin');
      }
      break;
  }

  return { issues, improvements };
}
