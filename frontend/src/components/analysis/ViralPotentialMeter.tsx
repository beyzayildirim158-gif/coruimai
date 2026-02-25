'use client';

import React from 'react';
import { 
  LightningIcon, 
  TrendingUpIcon, 
  ClockIcon, 
  ShareIcon, 
  CommentIcon,
  StarIcon,
  AlertCircleIcon,
  CheckCircleIcon
} from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface ViralPotential {
  readiness_score: number;
  strengths: string[];
  weaknesses: string[];
  viral_elements: {
    hook: string;
    share_trigger: string;
    engagement_bait: string;
  };
  viral_readiness: {
    overall: string;
    factors: {
      content_quality: number;
      timing: number;
      hashtag_strategy: number;
      engagement_rate: number;
    };
    missing_elements: string[];
    recommendations: string[];
  };
  immediate_opportunities: string[];
}

interface ViralPotentialMeterProps {
  viralPotential: ViralPotential;
}

const getScoreColor = (score: number) => {
  if (score >= 70) return { bg: 'bg-green-500', text: 'text-green-700', light: 'bg-green-50' };
  if (score >= 50) return { bg: 'bg-blue-500', text: 'text-blue-700', light: 'bg-blue-50' };
  if (score >= 30) return { bg: 'bg-yellow-500', text: 'text-yellow-700', light: 'bg-yellow-50' };
  return { bg: 'bg-red-500', text: 'text-red-700', light: 'bg-red-50' };
};

const getReadinessEmoji = (readiness: string) => {
  switch (readiness.toLowerCase()) {
    case 'high': return '🚀';
    case 'medium': return '📈';
    case 'low': return '⚠️';
    case 'very_low': return '🚨';
    default: return '📊';
  }
};

export const ViralPotentialMeter: React.FC<ViralPotentialMeterProps> = ({ viralPotential }) => {
  const { locale } = useTranslation();
  const scoreColor = getScoreColor(viralPotential.readiness_score);
  
  const labels = {
    title: locale === 'tr' ? 'Viral Potansiyel' : 'Viral Potential',
    subtitle: locale === 'tr' ? 'Viral hazırlık analizi' : 'Viral readiness analysis',
    readinessScore: locale === 'tr' ? 'Hazırlık Skoru' : 'Readiness Score',
    viralFactors: locale === 'tr' ? 'Viral Faktörler' : 'Viral Factors',
    strengths: locale === 'tr' ? 'Güçlü Yönler' : 'Strengths',
    weaknesses: locale === 'tr' ? 'Zayıf Yönler' : 'Weaknesses',
    viralElements: locale === 'tr' ? 'Viral Elementler' : 'Viral Elements',
    missingElements: locale === 'tr' ? 'Eksik Elementler' : 'Missing Elements',
    opportunities: locale === 'tr' ? 'Acil Fırsatlar' : 'Immediate Opportunities',
    recommendations: locale === 'tr' ? 'Öneriler' : 'Recommendations',
    factors: {
      content_quality: locale === 'tr' ? 'İçerik Kalitesi' : 'Content Quality',
      timing: locale === 'tr' ? 'Zamanlama' : 'Timing',
      hashtag_strategy: locale === 'tr' ? 'Hashtag Stratejisi' : 'Hashtag Strategy',
      engagement_rate: locale === 'tr' ? 'Etkileşim Oranı' : 'Engagement Rate',
    },
    elements: {
      hook: locale === 'tr' ? 'Hook (İlk 3 saniye)' : 'Hook (First 3 seconds)',
      share_trigger: locale === 'tr' ? 'Paylaşım Tetikleyici' : 'Share Trigger',
      engagement_bait: locale === 'tr' ? 'Etkileşim Çağrısı' : 'Engagement Bait',
    },
    readiness: {
      high: locale === 'tr' ? 'Yüksek' : 'High',
      medium: locale === 'tr' ? 'Orta' : 'Medium',
      low: locale === 'tr' ? 'Düşük' : 'Low',
      very_low: locale === 'tr' ? 'Çok Düşük' : 'Very Low',
    },
  };

  const getReadinessLabel = (readiness: string) => 
    labels.readiness[readiness as keyof typeof labels.readiness] || readiness;

  const factorIcons: Record<string, any> = {
    content_quality: StarIcon,
    timing: ClockIcon,
    hashtag_strategy: TrendingUpIcon,
    engagement_rate: CommentIcon,
  };

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 bg-gradient-to-r from-purple-50 to-white border-b border-slate-200">
        <div className="flex items-center gap-3">
          <LightningIcon size={24} className="text-purple-500" />
          <div>
            <h3 className="text-lg font-semibold text-slate-900">⚡ {labels.title}</h3>
            <p className="text-sm text-slate-500">{labels.subtitle}</p>
          </div>
        </div>
      </div>

      <div className="p-6">
        {/* Score Meter */}
        <div className="flex flex-col items-center mb-8">
          <div className="relative w-48 h-48">
            {/* Background circle */}
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="#e2e8f0"
                strokeWidth="10"
              />
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="currentColor"
                strokeWidth="10"
                strokeDasharray={`${viralPotential.readiness_score * 2.83} 283`}
                strokeLinecap="round"
                className={scoreColor.text}
              />
            </svg>
            {/* Center content */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-4xl font-bold text-slate-900">{viralPotential.readiness_score}</span>
              <span className="text-sm text-slate-500">/100</span>
              <div className="flex items-center gap-1 mt-1">
                <span className="text-lg">{getReadinessEmoji(viralPotential.viral_readiness.overall)}</span>
                <span className={`text-sm font-medium ${scoreColor.text}`}>
                  {getReadinessLabel(viralPotential.viral_readiness.overall)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Viral Factors Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          {Object.entries(viralPotential.viral_readiness.factors).map(([factor, score]) => {
            const IconComp = factorIcons[factor] || StarIcon;
            const color = getScoreColor(score);
            return (
              <div key={factor} className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div className="flex items-center gap-2 mb-2">
                  <IconComp size={16} className="text-slate-500" />
                  <span className="text-xs text-slate-600 truncate">
                    {labels.factors[factor as keyof typeof labels.factors]}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                    <div 
                      className={`h-full ${color.bg} rounded-full transition-all`}
                      style={{ width: `${score}%` }}
                    />
                  </div>
                  <span className={`text-xs font-medium ${color.text}`}>{score}%</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Viral Elements */}
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
            <ShareIcon size={16} className="text-purple-500" />
            {labels.viralElements}
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {Object.entries(viralPotential.viral_elements).map(([element, status]) => (
              <div 
                key={element}
                className={`p-3 rounded-xl border ${
                  status === 'present' || status === 'active'
                    ? 'bg-green-50 border-green-200'
                    : 'bg-red-50 border-red-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-700">
                    {labels.elements[element as keyof typeof labels.elements]}
                  </span>
                  {status === 'present' || status === 'active' ? (
                    <CheckCircleIcon size={16} className="text-green-500" />
                  ) : (
                    <AlertCircleIcon size={16} className="text-red-500" />
                  )}
                </div>
                <span className={`text-xs mt-1 ${
                  status === 'present' || status === 'active' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Strengths & Weaknesses */}
        <div className="grid grid-cols-2 gap-6 mb-6">
          {/* Strengths */}
          <div>
            <h4 className="text-sm font-semibold text-green-700 mb-3 flex items-center gap-2">
              <CheckCircleIcon size={16} />
              {labels.strengths}
            </h4>
            <div className="space-y-2">
              {viralPotential.strengths.length > 0 ? (
                viralPotential.strengths.map((strength, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-sm text-green-700">
                    <span className="text-green-500 mt-0.5">✓</span>
                    <span>{strength}</span>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-400 italic">
                  {locale === 'tr' ? 'Henüz güçlü yön bulunamadı' : 'No strengths identified yet'}
                </p>
              )}
            </div>
          </div>

          {/* Weaknesses */}
          <div>
            <h4 className="text-sm font-semibold text-red-700 mb-3 flex items-center gap-2">
              <AlertCircleIcon size={16} />
              {labels.weaknesses}
            </h4>
            <div className="space-y-2">
              {viralPotential.weaknesses.length > 0 ? (
                viralPotential.weaknesses.map((weakness, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-sm text-red-700">
                    <span className="text-red-500 mt-0.5">✗</span>
                    <span>{weakness}</span>
                  </div>
                ))
              ) : (
                <p className="text-sm text-slate-400 italic">
                  {locale === 'tr' ? 'Zayıf yön bulunamadı' : 'No weaknesses identified'}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Missing Elements */}
        {viralPotential.viral_readiness.missing_elements?.length > 0 && (
          <div className="mb-6">
            <h4 className="text-sm font-semibold text-amber-700 mb-3">{labels.missingElements}</h4>
            <div className="flex flex-wrap gap-2">
              {viralPotential.viral_readiness.missing_elements.map((element, idx) => (
                <span 
                  key={idx}
                  className="px-3 py-1 rounded-full text-xs bg-amber-100 text-amber-700 border border-amber-200"
                >
                  {element}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Immediate Opportunities */}
        {viralPotential.immediate_opportunities?.length > 0 && (
          <div className="p-4 rounded-xl bg-purple-50 border border-purple-200">
            <h4 className="text-sm font-semibold text-purple-700 mb-3 flex items-center gap-2">
              <LightningIcon size={16} />
              {labels.opportunities}
            </h4>
            <div className="space-y-2">
              {viralPotential.immediate_opportunities.map((opportunity, idx) => (
                <div key={idx} className="flex items-start gap-2 text-sm text-purple-700">
                  <span className="text-purple-500 mt-0.5">→</span>
                  <span>{opportunity}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ViralPotentialMeter;
