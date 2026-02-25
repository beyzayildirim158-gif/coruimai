'use client';

import React from 'react';
import { 
  BookOpenIcon, 
  SmileIcon, 
  ShoppingBagIcon,
  HeartIcon,
  TrendingUpIcon,
  AlertTriangleIcon
} from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface ContentDistribution {
  current: {
    educational: number;
    entertainment: number;
    promotional: number;
    personal: number;
  };
  optimal: {
    educational: number;
    entertainment: number;
    promotional: number;
    personal: number;
  };
  balance_score: number;
  issues: string[];
  recommendations: string[];
}

interface ContentDistributionChartProps {
  contentDistribution: ContentDistribution;
}

const categoryConfig: Record<string, { icon: any; color: string; bgLight: string; bgDark: string }> = {
  educational: { 
    icon: BookOpenIcon, 
    color: 'text-blue-600', 
    bgLight: 'bg-blue-100', 
    bgDark: 'bg-blue-500' 
  },
  entertainment: { 
    icon: SmileIcon, 
    color: 'text-pink-600', 
    bgLight: 'bg-pink-100', 
    bgDark: 'bg-pink-500' 
  },
  promotional: { 
    icon: ShoppingBagIcon, 
    color: 'text-amber-600', 
    bgLight: 'bg-amber-100', 
    bgDark: 'bg-amber-500' 
  },
  personal: { 
    icon: HeartIcon, 
    color: 'text-red-600', 
    bgLight: 'bg-red-100', 
    bgDark: 'bg-red-500' 
  },
};

const getBalanceScoreColor = (score: number) => {
  if (score >= 80) return { text: 'text-green-700', bg: 'bg-green-50', border: 'border-green-200' };
  if (score >= 60) return { text: 'text-blue-700', bg: 'bg-blue-50', border: 'border-blue-200' };
  if (score >= 40) return { text: 'text-yellow-700', bg: 'bg-yellow-50', border: 'border-yellow-200' };
  return { text: 'text-red-700', bg: 'bg-red-50', border: 'border-red-200' };
};

export const ContentDistributionChart: React.FC<ContentDistributionChartProps> = ({ contentDistribution }) => {
  const { locale } = useTranslation();
  const balanceColor = getBalanceScoreColor(contentDistribution.balance_score);
  
  const labels = {
    title: locale === 'tr' ? 'İçerik Dağılımı' : 'Content Distribution',
    subtitle: locale === 'tr' ? 'Değer/eğlence dengesi analizi' : 'Value/entertainment balance analysis',
    balanceScore: locale === 'tr' ? 'Denge Skoru' : 'Balance Score',
    current: locale === 'tr' ? 'Mevcut' : 'Current',
    optimal: locale === 'tr' ? 'Optimal' : 'Optimal',
    issues: locale === 'tr' ? 'Tespit Edilen Sorunlar' : 'Identified Issues',
    recommendations: locale === 'tr' ? 'Öneriler' : 'Recommendations',
    categories: {
      educational: locale === 'tr' ? 'Eğitici' : 'Educational',
      entertainment: locale === 'tr' ? 'Eğlence' : 'Entertainment',
      promotional: locale === 'tr' ? 'Tanıtım' : 'Promotional',
      personal: locale === 'tr' ? 'Kişisel' : 'Personal',
    },
  };

  const getCategoryLabel = (category: string) => 
    labels.categories[category as keyof typeof labels.categories] || category;

  // Calculate max for scaling
  const allValues = [
    ...Object.values(contentDistribution.current),
    ...Object.values(contentDistribution.optimal),
  ];
  const maxValue = Math.max(...allValues, 50);

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 bg-gradient-to-r from-indigo-50 to-white border-b border-slate-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <TrendingUpIcon size={24} className="text-indigo-500" />
            <div>
              <h3 className="text-lg font-semibold text-slate-900">📊 {labels.title}</h3>
              <p className="text-sm text-slate-500">{labels.subtitle}</p>
            </div>
          </div>
          {/* Balance Score Badge */}
          <div className={`px-4 py-2 rounded-xl ${balanceColor.bg} ${balanceColor.border} border`}>
            <span className="text-xs text-slate-500">{labels.balanceScore}</span>
            <div className={`text-2xl font-bold ${balanceColor.text}`}>
              {contentDistribution.balance_score}%
            </div>
          </div>
        </div>
      </div>

      <div className="p-6">
        {/* Distribution Comparison */}
        <div className="mb-6">
          <div className="flex items-center justify-end gap-6 mb-4">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-slate-400" />
              <span className="text-xs text-slate-500">{labels.current}</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-indigo-400" />
              <span className="text-xs text-slate-500">{labels.optimal}</span>
            </div>
          </div>

          <div className="space-y-4">
            {Object.keys(contentDistribution.current).map((category) => {
              const config = categoryConfig[category] || categoryConfig.educational;
              const Icon = config.icon;
              const currentValue = contentDistribution.current[category as keyof typeof contentDistribution.current];
              const optimalValue = contentDistribution.optimal[category as keyof typeof contentDistribution.optimal];
              const diff = optimalValue - currentValue;

              return (
                <div key={category} className="group">
                  <div className="flex items-center gap-3 mb-2">
                    <div className={`p-2 rounded-lg ${config.bgLight}`}>
                      <Icon className={`h-4 w-4 ${config.color}`} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-700">
                          {getCategoryLabel(category)}
                        </span>
                        <div className="flex items-center gap-3 text-sm">
                          <span className="text-slate-500">{currentValue}%</span>
                          <span className="text-slate-300">→</span>
                          <span className="text-indigo-600 font-medium">{optimalValue}%</span>
                          {diff !== 0 && (
                            <span className={`text-xs px-2 py-0.5 rounded-full ${
                              diff > 0 
                                ? 'bg-green-100 text-green-700' 
                                : 'bg-red-100 text-red-700'
                            }`}>
                              {diff > 0 ? '+' : ''}{diff}%
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Bar comparison */}
                  <div className="ml-11 space-y-1">
                    {/* Current bar */}
                    <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-slate-400 rounded-full transition-all"
                        style={{ width: `${(currentValue / maxValue) * 100}%` }}
                      />
                    </div>
                    {/* Optimal bar */}
                    <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className={`h-full ${config.bgDark} rounded-full transition-all opacity-70`}
                        style={{ width: `${(optimalValue / maxValue) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Issues */}
        {contentDistribution.issues && contentDistribution.issues.length > 0 && (
          <div className="mb-6">
            <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <AlertTriangleIcon size={16} className="text-amber-500" />
              {labels.issues}
            </h4>
            <div className="p-4 rounded-xl bg-amber-50 border border-amber-200">
              <ul className="space-y-2">
                {contentDistribution.issues.map((issue, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-amber-700">
                    <span className="text-amber-500 mt-0.5">⚠</span>
                    <span>{issue}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Recommendations */}
        {contentDistribution.recommendations && contentDistribution.recommendations.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-slate-700 mb-3">💡 {labels.recommendations}</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {contentDistribution.recommendations.map((rec, idx) => (
                <div 
                  key={idx}
                  className="p-3 rounded-xl bg-indigo-50 border border-indigo-200 text-sm text-indigo-700"
                >
                  <span className="mr-2">→</span>
                  {rec}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ContentDistributionChart;
