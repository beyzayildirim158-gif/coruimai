'use client';

import React from 'react';
import { 
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  MinusIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';
import { useTranslation } from '@/i18n/TranslationProvider';

export interface BenchmarkData {
  metric: string;
  value: string | number;
  nicheAverage: string | number;
  topPerformers: string | number;
  unit?: string;
  higherIsBetter?: boolean;
}

interface BenchmarkComparisonProps {
  data: BenchmarkData;
  showTrend?: boolean;
}

// Get verdict based on comparison
function getVerdict(
  value: number,
  nicheAverage: number,
  topPerformers: number,
  higherIsBetter: boolean = true,
  locale: string = 'tr'
): { label: string; emoji: string; color: string } {
  const labels = locale === 'en' ? {
    topLevel: 'Top level performance',
    aboveAverage: 'Above average',
    average: 'Around average',
    belowAverage: 'Below average',
  } : {
    topLevel: 'Üst düzey performans',
    aboveAverage: 'Ortalamanın üstünde',
    average: 'Ortalama civarı',
    belowAverage: 'Ortalamanın altında',
  };
  
  // Handle edge cases: if benchmarks are 0 or invalid
  if (nicheAverage <= 0 || topPerformers <= 0) {
    return { label: labels.average, emoji: '➡️', color: 'text-yellow-600' };
  }
  
  if (higherIsBetter) {
    // Higher value = better (e.g., engagement rate, followers)
    if (value >= topPerformers * 0.9) {
      return { label: labels.topLevel, emoji: '⭐', color: 'text-green-600' };
    }
    if (value >= nicheAverage) {
      return { label: labels.aboveAverage, emoji: '✅', color: 'text-green-600' };
    }
    if (value >= nicheAverage * 0.7) {
      return { label: labels.average, emoji: '➡️', color: 'text-yellow-600' };
    }
    return { label: labels.belowAverage, emoji: '⚠️', color: 'text-red-600' };
  } else {
    // Lower is better (e.g., bot score, churn rate)
    // For bot score: lower = better, so if value < topPerformers (best case), it's great
    if (value <= topPerformers) {
      return { label: labels.topLevel, emoji: '⭐', color: 'text-green-600' };
    }
    if (value <= nicheAverage) {
      return { label: labels.aboveAverage, emoji: '✅', color: 'text-green-600' };
    }
    if (value <= nicheAverage * 1.3) {
      return { label: labels.average, emoji: '➡️', color: 'text-yellow-600' };
    }
    return { label: labels.belowAverage, emoji: '⚠️', color: 'text-red-600' };
  }
}

// Parse numeric value from string
function parseNumeric(value: string | number): number {
  if (typeof value === 'number') return value;
  const cleaned = value.replace(/[%,KMB]/gi, '').trim();
  let num = parseFloat(cleaned);
  if (value.toLowerCase().includes('k')) num *= 1000;
  if (value.toLowerCase().includes('m')) num *= 1000000;
  if (value.toLowerCase().includes('b')) num *= 1000000000;
  return num || 0;
}

const BenchmarkComparison: React.FC<BenchmarkComparisonProps> = ({ data, showTrend = true }) => {
  const { t, locale } = useTranslation();
  const { metric, value, nicheAverage, topPerformers, unit = '', higherIsBetter = true } = data;
  
  const numValue = parseNumeric(value);
  const numAverage = parseNumeric(nicheAverage);
  const numTop = parseNumeric(topPerformers);
  
  const verdict = getVerdict(numValue, numAverage, numTop, higherIsBetter, locale);
  
  // Calculate bar widths (normalize to top performers = 100%)
  const maxValue = Math.max(numValue, numAverage, numTop) * 1.1;
  const valueWidth = (numValue / maxValue) * 100;
  const avgWidth = (numAverage / maxValue) * 100;
  const topWidth = (numTop / maxValue) * 100;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-semibold text-slate-900">{metric}</h4>
        <div className={`flex items-center gap-1 text-sm font-medium ${verdict.color}`}>
          <span>{verdict.emoji}</span>
          <span>{verdict.label}</span>
        </div>
      </div>

      {/* Visual Comparison */}
      <div className="space-y-2 mb-4">
        {/* Your Value */}
        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-500 w-20">{t('benchmark.yours')}</span>
          <div className="flex-1 h-6 bg-slate-100 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-primary-500 to-primary-400 rounded-full flex items-center justify-end pr-2 transition-all duration-500"
              style={{ width: `${valueWidth}%` }}
            >
              <span className="text-xs text-white font-medium whitespace-nowrap">
                {typeof value === 'number' ? value.toFixed(2) : value}{unit}
              </span>
            </div>
          </div>
        </div>

        {/* Niche Average */}
        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-500 w-20">{t('benchmark.nicheAvg')}</span>
          <div className="flex-1 h-6 bg-slate-100 rounded-full overflow-hidden">
            <div 
              className="h-full bg-slate-400 rounded-full flex items-center justify-end pr-2"
              style={{ width: `${avgWidth}%` }}
            >
              <span className="text-xs text-white font-medium whitespace-nowrap">
                {typeof nicheAverage === 'number' ? nicheAverage.toFixed(2) : nicheAverage}{unit}
              </span>
            </div>
          </div>
        </div>

        {/* Top Performers */}
        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-500 w-20">{t('benchmark.topPerformers')}</span>
          <div className="flex-1 h-6 bg-slate-100 rounded-full overflow-hidden">
            <div 
              className="h-full bg-green-500 rounded-full flex items-center justify-end pr-2"
              style={{ width: `${topWidth}%` }}
            >
              <span className="text-xs text-white font-medium whitespace-nowrap">
                {typeof topPerformers === 'number' ? topPerformers.toFixed(2) : topPerformers}{unit}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Trend Indicator */}
      {showTrend && (
        <div className="pt-3 border-t border-slate-100">
          <div className="flex items-center gap-2 text-sm">
            {numValue > numAverage ? (
              <>
                <ArrowTrendingUpIcon className="w-4 h-4 text-green-500" />
                <span className="text-green-600">
                  {locale === 'en' 
                    ? `You are ${Math.round(((numValue - numAverage) / numAverage) * 100)}% above average`
                    : `Ortalamanın %${Math.round(((numValue - numAverage) / numAverage) * 100)} üstündesiniz`}
                </span>
              </>
            ) : numValue < numAverage ? (
              <>
                <ArrowTrendingDownIcon className="w-4 h-4 text-red-500" />
                <span className="text-red-600">
                  {locale === 'en'
                    ? `You are ${Math.round(((numAverage - numValue) / numAverage) * 100)}% below average`
                    : `Ortalamanın %${Math.round(((numAverage - numValue) / numAverage) * 100)} altındasınız`}
                </span>
              </>
            ) : (
              <>
                <MinusIcon className="w-4 h-4 text-slate-500" />
                <span className="text-slate-600">{t('benchmark.exactAverage')}</span>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default BenchmarkComparison;

// Multi-metric comparison grid
interface BenchmarkGridProps {
  benchmarks: BenchmarkData[];
  title?: string;
}

export const BenchmarkGrid: React.FC<BenchmarkGridProps> = ({ benchmarks, title }) => {
  return (
    <div className="space-y-4">
      {title && (
        <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {benchmarks.map((benchmark, idx) => (
          <BenchmarkComparison key={idx} data={benchmark} />
        ))}
      </div>
    </div>
  );
};

// Helper to create benchmark data from analysis
export function createBenchmarkData(
  metric: string,
  value: string | number,
  nicheData: { average?: number; top?: number },
  options?: { unit?: string; higherIsBetter?: boolean }
): BenchmarkData {
  return {
    metric,
    value,
    nicheAverage: nicheData.average || 0,
    topPerformers: nicheData.top || 0,
    unit: options?.unit || '',
    higherIsBetter: options?.higherIsBetter ?? true,
  };
}
