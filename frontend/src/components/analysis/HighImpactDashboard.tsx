'use client';

import React from 'react';
import {
  UsersIcon,
  TargetIcon,
  EyeIcon,
  LightbulbIcon,
  PaletteIcon,
  TrendingUpIcon,
  TrendingDownIcon,
  AlertTriangleIcon,
  SparkIcon,
} from '@/components/icons';

/**
 * 🚀 HIGH IMPACT DASHBOARD
 * 
 * "Vurucu Gerçekler" bölümü - Executive Summary'den hemen sonra gösterilir.
 * En değerli ve psikolojik etkisi yüksek verileri görselleştirir.
 * 
 * İçerir:
 * 1. Audience Röntgen (Community Agent) - Takipçi segmentasyonu
 * 2. Slap in the Face Benchmark (Domain Master) - ER karşılaştırması
 * 3. Algorithmic Reality Check (Attention Architect) - Dikkat metrikleri
 * 4. Copywriting Reverse-Engineering (Attention Architect) - Hook iyileştirme
 * 5. Grid & Brand Math (Visual Brand) - Renk paleti önerileri
 */

// =============================================
// TYPES
// =============================================

export interface AudienceSegment {
  label: string;
  percentage: number;
  count: number;
  color: string;
  description: string;
}

export interface BenchmarkComparison {
  yourValue: number;
  nicheAverage: number;
  topPerformers: number;
  gap: number;
  percentile: number;
  interpretation: 'critical' | 'below' | 'average' | 'above' | 'excellent';
}

export interface AttentionMetrics {
  scrollStopProbability: number;
  thumbnailImpact: number;
  curiosityGap: number;
  hookEffectiveness: number;
  first3SecondsRetention: number;
}

export interface HookRewrite {
  original: string;
  improved: string;
  trigger: string;
  triggerEmoji: string;
  improvement: string;
}

export interface ColorSwatch {
  hex: string;
  name: string;
  usage: string;
  psychology: string;
}

export interface BrandPalette {
  current: ColorSwatch[];
  recommended: {
    primary: ColorSwatch;
    secondary: ColorSwatch;
    accent: ColorSwatch;
    rationale: string;
  };
}

export interface HighImpactData {
  audienceSegments: AudienceSegment[];
  benchmark: BenchmarkComparison;
  attentionMetrics: AttentionMetrics;
  hookRewrites: HookRewrite[];
  brandPalette: BrandPalette;
  overallHealthGrade: string;
  username: string;
}

interface HighImpactDashboardProps {
  data: HighImpactData;
  locale?: 'tr' | 'en';
}

// =============================================
// HELPER COMPONENTS
// =============================================

function CircularGauge({ 
  value, 
  maxValue = 100, 
  label, 
  color,
  size = 'md'
}: { 
  value: number; 
  maxValue?: number; 
  label: string; 
  color: string;
  size?: 'sm' | 'md' | 'lg';
}) {
  const percentage = Math.min((value / maxValue) * 100, 100);
  const circumference = 2 * Math.PI * 40;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;
  
  const sizeClasses = {
    sm: 'w-20 h-20',
    md: 'w-28 h-28',
    lg: 'w-36 h-36',
  };

  const textSizes = {
    sm: 'text-lg',
    md: 'text-2xl',
    lg: 'text-3xl',
  };

  return (
    <div className="flex flex-col items-center">
      <div className={`relative ${sizeClasses[size]}`}>
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r="40"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
            className="text-slate-200"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r="40"
            stroke={color}
            strokeWidth="8"
            fill="none"
            strokeLinecap="round"
            style={{
              strokeDasharray: circumference,
              strokeDashoffset,
              transition: 'stroke-dashoffset 0.5s ease-in-out',
            }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`${textSizes[size]} font-bold text-slate-900`}>
            {Math.round(value)}
          </span>
        </div>
      </div>
      <p className="mt-2 text-sm font-medium text-slate-600 text-center">{label}</p>
    </div>
  );
}

function SegmentedProgressBar({ segments }: { segments: AudienceSegment[] }) {
  return (
    <div className="w-full">
      {/* Progress bar */}
      <div className="h-8 rounded-full overflow-hidden flex bg-slate-100">
        {segments.map((segment, idx) => (
          <div
            key={idx}
            className="h-full transition-all duration-500 relative group"
            style={{
              width: `${segment.percentage}%`,
              backgroundColor: segment.color,
              minWidth: segment.percentage > 0 ? '2%' : '0',
            }}
          >
            {/* Tooltip on hover */}
            <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-slate-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10 pointer-events-none">
              {segment.label}: {segment.percentage.toFixed(1)}%
              <br />
              ({segment.count.toLocaleString()} kişi)
            </div>
          </div>
        ))}
      </div>
      
      {/* Legend */}
      <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
        {segments.map((segment, idx) => (
          <div key={idx} className="flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full flex-shrink-0"
              style={{ backgroundColor: segment.color }}
            />
            <div className="min-w-0">
              <p className="text-sm font-medium text-slate-900 truncate">{segment.label}</p>
              <p className="text-xs text-slate-500">{segment.percentage.toFixed(1)}%</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ColorSwatchDisplay({ swatch, showDetails = true }: { swatch: ColorSwatch; showDetails?: boolean }) {
  return (
    <div className="flex items-center gap-3">
      <div
        className="w-12 h-12 rounded-xl shadow-inner border border-slate-200 flex-shrink-0"
        style={{ 
          backgroundColor: swatch.hex,
          printColorAdjust: 'exact',
          WebkitPrintColorAdjust: 'exact',
        }}
      />
      {showDetails && (
        <div className="min-w-0">
          <p className="text-sm font-semibold text-slate-900">{swatch.name}</p>
          <p className="text-xs font-mono text-slate-500">{swatch.hex}</p>
          <p className="text-xs text-slate-400">{swatch.usage}</p>
        </div>
      )}
    </div>
  );
}

// =============================================
// MAIN COMPONENT
// =============================================

export function HighImpactDashboard({ data, locale = 'tr' }: HighImpactDashboardProps) {
  const labels = {
    title: locale === 'tr' ? '🎯 Vurucu Gerçekler' : '🎯 Eye-Opening Insights',
    subtitle: locale === 'tr' 
      ? 'Hesabınızın kritik durumu bir bakışta' 
      : 'Your account\'s critical status at a glance',
    audienceTitle: locale === 'tr' ? '👥 Takipçi Röntgeni' : '👥 Audience X-Ray',
    audienceSubtitle: locale === 'tr' 
      ? 'Takipçilerinizin %kaçı gerçekten aktif?' 
      : 'What percentage of your followers are actually active?',
    benchmarkTitle: locale === 'tr' ? '📊 Sektör Karşılaştırması' : '📊 Industry Benchmark',
    benchmarkSubtitle: locale === 'tr' 
      ? 'Niş ortalamasına göre konumunuz' 
      : 'Your position vs. niche average',
    attentionTitle: locale === 'tr' ? '🧠 Algoritmik Gerçeklik' : '🧠 Algorithmic Reality',
    attentionSubtitle: locale === 'tr' 
      ? 'İçerikleriniz kaydırmayı durduruyor mu?' 
      : 'Does your content stop the scroll?',
    hookTitle: locale === 'tr' ? '✍️ Hook Mühendisliği' : '✍️ Hook Engineering',
    hookSubtitle: locale === 'tr' 
      ? 'Orijinal vs. İyileştirilmiş' 
      : 'Original vs. Improved',
    brandTitle: locale === 'tr' ? '🎨 Marka Renk Matematiği' : '🎨 Brand Color Math',
    brandSubtitle: locale === 'tr' 
      ? 'Önerilen HEX renk paleti' 
      : 'Recommended HEX color palette',
    yourER: locale === 'tr' ? 'Sizin ER' : 'Your ER',
    nicheAvg: locale === 'tr' ? 'Niş Ort.' : 'Niche Avg',
    topPerformers: locale === 'tr' ? 'Top %10' : 'Top 10%',
    gap: locale === 'tr' ? 'Fark' : 'Gap',
    original: locale === 'tr' ? 'Orijinal' : 'Original',
    improved: locale === 'tr' ? 'İyileştirilmiş' : 'Improved',
    trigger: locale === 'tr' ? 'Psikolojik Tetikleyici' : 'Psychological Trigger',
    currentPalette: locale === 'tr' ? 'Mevcut' : 'Current',
    recommendedPalette: locale === 'tr' ? 'Önerilen' : 'Recommended',
  };

  const getInterpretationColor = (interpretation: string) => {
    switch (interpretation) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'below': return 'text-orange-600 bg-orange-100';
      case 'average': return 'text-yellow-600 bg-yellow-100';
      case 'above': return 'text-blue-600 bg-blue-100';
      case 'excellent': return 'text-green-600 bg-green-100';
      default: return 'text-slate-600 bg-slate-100';
    }
  };

  const getInterpretationLabel = (interpretation: string) => {
    const labels: Record<string, { tr: string; en: string }> = {
      critical: { tr: 'Kritik', en: 'Critical' },
      below: { tr: 'Ortalamanın Altı', en: 'Below Average' },
      average: { tr: 'Ortalama', en: 'Average' },
      above: { tr: 'Ortalamanın Üstü', en: 'Above Average' },
      excellent: { tr: 'Mükemmel', en: 'Excellent' },
    };
    return labels[interpretation]?.[locale] || interpretation;
  };

  const getGaugeColor = (value: number) => {
    if (value >= 70) return '#22c55e'; // green-500
    if (value >= 50) return '#3b82f6'; // blue-500
    if (value >= 30) return '#f59e0b'; // amber-500
    return '#ef4444'; // red-500
  };

  return (
    <div className="high-impact-dashboard print-section space-y-6">
      {/* Header */}
      <div className="rounded-3xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 p-6 text-white shadow-xl">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-white/20 rounded-2xl backdrop-blur">
            <SparkIcon size={32} className="text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold">{labels.title}</h2>
            <p className="text-white/80 mt-1">{labels.subtitle}</p>
          </div>
          <div className="ml-auto">
            <div className="px-4 py-2 bg-white/20 rounded-xl backdrop-blur">
              <span className="text-sm">@{data.username}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* 1. Audience Röntgen */}
        <div className="avoid-break rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2.5 rounded-xl bg-blue-100">
              <UsersIcon size={20} className="text-blue-600" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900">{labels.audienceTitle}</h3>
              <p className="text-xs text-slate-500">{labels.audienceSubtitle}</p>
            </div>
          </div>
          
          <SegmentedProgressBar segments={data.audienceSegments} />
          
          {/* Warning if ghost followers > 30% */}
          {(data.audienceSegments.find(s => s.label.toLowerCase().includes('ghost') || s.label.toLowerCase().includes('hayalet'))?.percentage ?? 0) > 30 && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl flex items-start gap-2">
              <AlertTriangleIcon size={16} className="text-red-500 flex-shrink-0 mt-0.5" />
              <p className="text-xs text-red-700">
                {locale === 'tr' 
                  ? 'Takipçilerinizin büyük çoğunluğu pasif! Bu, etkileşim oranınızı düşürüyor ve algoritma tarafından cezalandırılmanıza neden oluyor.'
                  : 'Most of your followers are passive! This lowers your engagement rate and causes algorithm penalties.'}
              </p>
            </div>
          )}
        </div>

        {/* 2. Slap in the Face Benchmark */}
        <div className="avoid-break rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2.5 rounded-xl bg-amber-100">
              <TargetIcon size={20} className="text-amber-600" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900">{labels.benchmarkTitle}</h3>
              <p className="text-xs text-slate-500">{labels.benchmarkSubtitle}</p>
            </div>
          </div>

          {/* Big Comparison Card */}
          <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-2xl p-5">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-xs text-slate-500 mb-1">{labels.yourER}</p>
                <p className={`text-3xl font-bold ${data.benchmark.yourValue < data.benchmark.nicheAverage ? 'text-red-600' : 'text-green-600'}`}>
                  {data.benchmark.yourValue.toFixed(2)}%
                </p>
              </div>
              <div className="flex items-center justify-center">
                <div className="text-2xl">vs</div>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">{labels.nicheAvg}</p>
                <p className="text-3xl font-bold text-slate-700">
                  {data.benchmark.nicheAverage.toFixed(2)}%
                </p>
              </div>
            </div>

            {/* Gap indicator */}
            <div className="mt-4 pt-4 border-t border-slate-200">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-600">{labels.gap}:</span>
                <span className={`text-lg font-bold flex items-center gap-1 ${data.benchmark.gap < 0 ? 'text-red-600' : 'text-green-600'}`}>
                  {data.benchmark.gap < 0 ? <TrendingDownIcon size={18} /> : <TrendingUpIcon size={18} />}
                  {data.benchmark.gap > 0 ? '+' : ''}{data.benchmark.gap.toFixed(1)}%
                </span>
              </div>
              <div className="mt-2">
                <span className={`inline-flex px-3 py-1 rounded-full text-xs font-medium ${getInterpretationColor(data.benchmark.interpretation)}`}>
                  {getInterpretationLabel(data.benchmark.interpretation)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* 3. Algorithmic Reality Check - Full width */}
        <div className="avoid-break lg:col-span-2 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2.5 rounded-xl bg-purple-100">
              <EyeIcon size={20} className="text-purple-600" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900">{labels.attentionTitle}</h3>
              <p className="text-xs text-slate-500">{labels.attentionSubtitle}</p>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
            <CircularGauge
              value={data.attentionMetrics.scrollStopProbability}
              label={locale === 'tr' ? 'Scroll Durma' : 'Scroll Stop'}
              color={getGaugeColor(data.attentionMetrics.scrollStopProbability)}
              size="md"
            />
            <CircularGauge
              value={data.attentionMetrics.thumbnailImpact}
              label={locale === 'tr' ? 'Thumbnail Etkisi' : 'Thumbnail Impact'}
              color={getGaugeColor(data.attentionMetrics.thumbnailImpact)}
              size="md"
            />
            <CircularGauge
              value={data.attentionMetrics.curiosityGap}
              label={locale === 'tr' ? 'Merak Boşluğu' : 'Curiosity Gap'}
              color={getGaugeColor(data.attentionMetrics.curiosityGap)}
              size="md"
            />
            <CircularGauge
              value={data.attentionMetrics.hookEffectiveness}
              label={locale === 'tr' ? 'Hook Etkinliği' : 'Hook Effectiveness'}
              color={getGaugeColor(data.attentionMetrics.hookEffectiveness)}
              size="md"
            />
            <CircularGauge
              value={data.attentionMetrics.first3SecondsRetention}
              label={locale === 'tr' ? 'İlk 3sn Tutma' : 'First 3s Retention'}
              color={getGaugeColor(data.attentionMetrics.first3SecondsRetention)}
              size="md"
            />
          </div>
        </div>

        {/* 4. Hook Engineering */}
        {data.hookRewrites.length > 0 && (
          <div className="avoid-break rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2.5 rounded-xl bg-green-100">
                <LightbulbIcon size={20} className="text-green-600" />
              </div>
              <div>
                <h3 className="font-bold text-slate-900">{labels.hookTitle}</h3>
                <p className="text-xs text-slate-500">{labels.hookSubtitle}</p>
              </div>
            </div>

            {data.hookRewrites.slice(0, 1).map((hook, idx) => (
              <div key={idx} className="space-y-3">
                {/* Original */}
                <div className="p-3 bg-red-50 border border-red-200 rounded-xl">
                  <p className="text-xs font-medium text-red-600 mb-1">❌ {labels.original}</p>
                  <p className="text-sm text-red-800">{hook.original}</p>
                </div>
                
                {/* Improved */}
                <div className="p-3 bg-green-50 border border-green-200 rounded-xl">
                  <p className="text-xs font-medium text-green-600 mb-1">✅ {labels.improved}</p>
                  <p className="text-sm text-green-800 font-medium">{hook.improved}</p>
                </div>

                {/* Trigger Badge */}
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500">{labels.trigger}:</span>
                  <span className="inline-flex items-center gap-1 px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                    {hook.triggerEmoji} {hook.trigger}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* 5. Brand Color Math */}
        <div className="avoid-break rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2.5 rounded-xl bg-pink-100">
              <PaletteIcon size={20} className="text-pink-600" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900">{labels.brandTitle}</h3>
              <p className="text-xs text-slate-500">{labels.brandSubtitle}</p>
            </div>
          </div>

          {/* Recommended Palette */}
          <div className="space-y-4">
            <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">
              {labels.recommendedPalette}
            </p>
            
            <div className="grid grid-cols-1 gap-3">
              <ColorSwatchDisplay swatch={data.brandPalette.recommended.primary} />
              <ColorSwatchDisplay swatch={data.brandPalette.recommended.secondary} />
              <ColorSwatchDisplay swatch={data.brandPalette.recommended.accent} />
            </div>

            {data.brandPalette.recommended.rationale && (
              <div className="mt-3 p-3 bg-slate-50 rounded-xl">
                <p className="text-xs text-slate-600 italic">
                  💡 {data.brandPalette.recommended.rationale}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default HighImpactDashboard;
