'use client';

import React from 'react';
import { HashtagIcon, TrendingUpIcon, TrendingDownIcon, TargetIcon, SparkIcon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

/**
 * CRITICAL: React Error #31 Fix
 * Bu fonksiyon objeleri güvenli bir şekilde string'e çevirir.
 */
function safeRenderValue(value: any): string {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  if (Array.isArray(value)) {
    return value.map(v => safeRenderValue(v)).filter(Boolean).join(', ');
  }
  if (typeof value === 'object') {
    const entries = Object.entries(value);
    if (entries.length === 0) return '';
    return entries
      .map(([k, v]) => `${k}: ${typeof v === 'object' ? JSON.stringify(v) : v}`)
      .join(' | ');
  }
  return String(value);
}

interface HashtagStrategy {
  current_strategy: {
    avg_hashtags: number;
    distribution: {
      mega: number;
      large: number;
      medium: number;
      small: number;
      micro: number;
    };
    effectiveness_score: number;
  };
  optimal_strategy: {
    total: number;
    mega: number;
    large: number;
    medium: number;
    small: number;
    micro: number;
  };
  effectiveness_score: number;
  issues: Array<{
    issue: string;
    impact: string;
    recommendation: string;
  }>;
  recommendations: {
    increase_to: number;
    add_micro_niche: boolean;
    reduce_mega: boolean;
    suggested_sets?: Array<{
      name: string;
      hashtags: string[];
      use_for: string;
    }>;
  };
}

interface HashtagStrategyCardProps {
  hashtagStrategy: HashtagStrategy;
}

const distributionColors: Record<string, string> = {
  mega: 'bg-purple-500',
  large: 'bg-blue-500',
  medium: 'bg-green-500',
  small: 'bg-yellow-500',
  micro: 'bg-orange-500',
};

const distributionLabels: Record<string, { tr: string; en: string; desc: { tr: string; en: string } }> = {
  mega: { tr: 'Mega', en: 'Mega', desc: { tr: '>10M post', en: '>10M posts' } },
  large: { tr: 'Büyük', en: 'Large', desc: { tr: '1-10M post', en: '1-10M posts' } },
  medium: { tr: 'Orta', en: 'Medium', desc: { tr: '100K-1M post', en: '100K-1M posts' } },
  small: { tr: 'Küçük', en: 'Small', desc: { tr: '10K-100K post', en: '10K-100K posts' } },
  micro: { tr: 'Mikro', en: 'Micro', desc: { tr: '<10K post', en: '<10K posts' } },
};

export const HashtagStrategyCard: React.FC<HashtagStrategyCardProps> = ({ hashtagStrategy }) => {
  const { locale } = useTranslation();
  
  const labels = {
    title: locale === 'tr' ? 'Hashtag Stratejisi' : 'Hashtag Strategy',
    subtitle: locale === 'tr' ? 'Mevcut vs Optimal dağılım' : 'Current vs Optimal distribution',
    current: locale === 'tr' ? 'Mevcut' : 'Current',
    optimal: locale === 'tr' ? 'Optimal' : 'Optimal',
    effectiveness: locale === 'tr' ? 'Etkinlik Skoru' : 'Effectiveness Score',
    avgHashtags: locale === 'tr' ? 'Ort. Hashtag' : 'Avg. Hashtags',
    issues: locale === 'tr' ? 'Sorunlar' : 'Issues',
    suggestedSets: locale === 'tr' ? 'Önerilen Hashtag Setleri' : 'Suggested Hashtag Sets',
    useFor: locale === 'tr' ? 'Kullanım' : 'Use for',
  };

  const getLabel = (key: string) => distributionLabels[key]?.[locale as 'tr' | 'en'] || key;
  const getDesc = (key: string) => distributionLabels[key]?.desc[locale as 'tr' | 'en'] || '';

  const effectivenessColor = hashtagStrategy.effectiveness_score >= 70 
    ? 'text-green-600' 
    : hashtagStrategy.effectiveness_score >= 40 
    ? 'text-yellow-600' 
    : 'text-red-600';

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-200 bg-gradient-to-r from-violet-50 to-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <HashtagIcon size={24} className="text-violet-500" />
            <div>
              <h3 className="text-lg font-semibold text-slate-900"># {labels.title}</h3>
              <p className="text-sm text-slate-500">{labels.subtitle}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-xs text-slate-500">{labels.effectiveness}</p>
            <p className={`text-2xl font-bold ${effectivenessColor}`}>
              {hashtagStrategy.effectiveness_score}/100
            </p>
          </div>
        </div>
      </div>

      <div className="p-6">
        {/* Distribution Comparison */}
        <div className="grid grid-cols-2 gap-6 mb-6">
          {/* Current Distribution */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-slate-700">{labels.current}</h4>
              <span className="text-xs text-slate-500">
                {labels.avgHashtags}: {hashtagStrategy.current_strategy.avg_hashtags}
              </span>
            </div>
            <div className="space-y-2">
              {Object.entries(hashtagStrategy.current_strategy.distribution).map(([key, value]) => (
                <div key={key} className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 w-16">{getLabel(key)}</span>
                  <div className="flex-1 bg-slate-100 rounded-full h-4 overflow-hidden">
                    <div 
                      className={`h-full ${distributionColors[key]} rounded-full transition-all`}
                      style={{ width: `${Math.min(100, value * 4)}%` }}
                    />
                  </div>
                  <span className="text-xs font-medium text-slate-700 w-6">{value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Optimal Distribution */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-slate-700">{labels.optimal}</h4>
              <span className="text-xs text-slate-500">
                {labels.avgHashtags}: {hashtagStrategy.optimal_strategy.total}
              </span>
            </div>
            <div className="space-y-2">
              {Object.entries(hashtagStrategy.optimal_strategy)
                .filter(([key]) => key !== 'total')
                .map(([key, value]) => (
                <div key={key} className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 w-16">{getLabel(key)}</span>
                  <div className="flex-1 bg-slate-100 rounded-full h-4 overflow-hidden">
                    <div 
                      className={`h-full ${distributionColors[key]} rounded-full transition-all`}
                      style={{ width: `${Math.min(100, (value as number) * 4)}%` }}
                    />
                  </div>
                  <span className="text-xs font-medium text-slate-700 w-6">{value as number}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Issues */}
        {hashtagStrategy.issues && hashtagStrategy.issues.length > 0 && (
          <div className="mb-6">
            <h4 className="text-sm font-semibold text-slate-700 mb-3">{labels.issues}</h4>
            <div className="space-y-2">
              {hashtagStrategy.issues.map((issue, idx) => (
                <div 
                  key={idx}
                  className="flex items-start gap-3 p-3 rounded-xl bg-amber-50 border border-amber-200"
                >
                  <TrendingDownIcon size={16} className="text-amber-600 mt-0.5 shrink-0" />
                  <div>
                    <p className="text-sm text-slate-700">{typeof issue.recommendation === 'string' ? issue.recommendation : safeRenderValue(issue.recommendation)}</p>
                    <p className="text-xs text-amber-600 mt-1">Impact: {typeof issue.impact === 'string' ? issue.impact : safeRenderValue(issue.impact)}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Suggested Sets */}
        {hashtagStrategy.recommendations.suggested_sets && hashtagStrategy.recommendations.suggested_sets.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <SparkIcon size={16} className="text-violet-500" />
              {labels.suggestedSets}
            </h4>
            <div className="space-y-4">
              {hashtagStrategy.recommendations.suggested_sets.map((set, idx) => (
                <div 
                  key={idx}
                  className="p-4 rounded-xl bg-violet-50 border border-violet-200"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h5 className="text-sm font-semibold text-violet-800">{set.name}</h5>
                    <span className="text-xs text-violet-600">{labels.useFor}: {set.use_for}</span>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {set.hashtags.slice(0, 10).map((tag, tagIdx) => (
                      <span 
                        key={tagIdx}
                        className="px-2 py-0.5 rounded-full bg-violet-100 text-violet-700 text-xs"
                      >
                        {tag}
                      </span>
                    ))}
                    {set.hashtags.length > 10 && (
                      <span className="px-2 py-0.5 text-xs text-violet-500">
                        +{set.hashtags.length - 10} more
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HashtagStrategyCard;
