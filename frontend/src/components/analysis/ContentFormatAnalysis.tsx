'use client';

import React from 'react';
import { 
  FilmIcon, 
  LayersIcon, 
  ImageIcon, 
  CommentIcon,
  TrendingUpIcon,
  AlertCircleIcon,
  TargetIcon
} from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface ContentFormats {
  current_mix: {
    reels: number;
    carousel: number;
    single_post: number;
  };
  optimal_mix: {
    reels: number;
    carousel: number;
    single_post: number;
    stories: number;
  };
  format_gaps: Array<{
    format: string;
    current: number;
    optimal: number;
    gap?: number;
    excess?: number;
    priority: string;
  }>;
  recommendations: {
    increase_reels: boolean;
    increase_carousel: boolean;
    reduce_single_post: boolean;
    weekly_targets: {
      reels: number;
      carousel: number;
      single_post: number;
    };
  };
  growth_channels?: Record<string, { status: string; potential: number }>;
}

interface ContentFormatAnalysisProps {
  contentFormats: ContentFormats;
}

const formatIcons: Record<string, any> = {
  reels: FilmIcon,
  carousel: LayersIcon,
  single_post: ImageIcon,
  stories: CommentIcon,
};

const formatColors: Record<string, { bg: string; text: string; bar: string }> = {
  reels: { bg: 'bg-pink-50', text: 'text-pink-700', bar: 'bg-pink-500' },
  carousel: { bg: 'bg-blue-50', text: 'text-blue-700', bar: 'bg-blue-500' },
  single_post: { bg: 'bg-slate-50', text: 'text-slate-700', bar: 'bg-slate-500' },
  stories: { bg: 'bg-amber-50', text: 'text-amber-700', bar: 'bg-amber-500' },
};

const priorityColors: Record<string, string> = {
  critical: 'bg-red-100 text-red-700 border-red-200',
  high: 'bg-orange-100 text-orange-700 border-orange-200',
  medium: 'bg-yellow-100 text-yellow-700 border-yellow-200',
  low: 'bg-green-100 text-green-700 border-green-200',
};

export const ContentFormatAnalysis: React.FC<ContentFormatAnalysisProps> = ({ contentFormats }) => {
  const { locale } = useTranslation();
  
  const labels = {
    title: locale === 'tr' ? 'İçerik Format Analizi' : 'Content Format Analysis',
    subtitle: locale === 'tr' ? 'Format dağılımı ve optimizasyon' : 'Format distribution and optimization',
    current: locale === 'tr' ? 'Mevcut Dağılım' : 'Current Distribution',
    optimal: locale === 'tr' ? 'Optimal Dağılım' : 'Optimal Distribution',
    formatGaps: locale === 'tr' ? 'Format Boşlukları' : 'Format Gaps',
    weeklyTargets: locale === 'tr' ? 'Haftalık Hedefler' : 'Weekly Targets',
    growthChannels: locale === 'tr' ? 'Büyüme Kanalları' : 'Growth Channels',
    formats: {
      reels: 'Reels',
      carousel: 'Carousel',
      single_post: locale === 'tr' ? 'Tek Post' : 'Single Post',
      stories: 'Stories',
    },
    statuses: {
      unused: locale === 'tr' ? 'Kullanılmıyor' : 'Unused',
      underutilized: locale === 'tr' ? 'Yetersiz Kullanım' : 'Underutilized',
      optimal: locale === 'tr' ? 'Optimal' : 'Optimal',
      suboptimal: locale === 'tr' ? 'Suboptimal' : 'Suboptimal',
    },
    priority: {
      critical: locale === 'tr' ? 'Kritik' : 'Critical',
      high: locale === 'tr' ? 'Yüksek' : 'High',
      medium: locale === 'tr' ? 'Orta' : 'Medium',
      low: locale === 'tr' ? 'Düşük' : 'Low',
    },
    perWeek: locale === 'tr' ? '/hafta' : '/week',
    potential: locale === 'tr' ? 'Potansiyel' : 'Potential',
  };

  const getFormatLabel = (format: string) => labels.formats[format as keyof typeof labels.formats] || format;
  const getPriorityLabel = (priority: string) => labels.priority[priority as keyof typeof labels.priority] || priority;
  const getStatusLabel = (status: string) => labels.statuses[status as keyof typeof labels.statuses] || status;

  // Check if Reels is at 0
  const reelsAtZero = contentFormats.current_mix.reels === 0;

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className={`px-6 py-4 border-b ${reelsAtZero ? 'bg-gradient-to-r from-red-50 to-white border-red-200' : 'bg-gradient-to-r from-pink-50 to-white border-slate-200'}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <FilmIcon className={reelsAtZero ? 'text-red-500' : 'text-pink-500'} size={24} />
            <div>
              <h3 className="text-lg font-semibold text-slate-900">📹 {labels.title}</h3>
              <p className="text-sm text-slate-500">{labels.subtitle}</p>
            </div>
          </div>
          {reelsAtZero && (
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-red-100 text-red-700 text-sm">
              <AlertCircleIcon size={16} />
              {locale === 'tr' ? 'Reels kullanılmıyor!' : 'No Reels!'}
            </div>
          )}
        </div>
      </div>

      <div className="p-6">
        {/* Format Distribution Comparison */}
        <div className="grid grid-cols-2 gap-6 mb-6">
          {/* Current Mix */}
          <div>
            <h4 className="text-sm font-semibold text-slate-700 mb-4">{labels.current}</h4>
            <div className="space-y-3">
              {Object.entries(contentFormats.current_mix).map(([format, percentage]) => {
                const Icon = formatIcons[format] || ImageIcon;
                const colors = formatColors[format] || formatColors.single_post;
                return (
                  <div key={format} className="flex items-center gap-3">
                    <div className={`p-1.5 rounded-lg ${colors.bg}`}>
                      <Icon className={colors.text} size={16} />
                    </div>
                    <div className="flex-1">
                      <div className="flex justify-between mb-1">
                        <span className="text-xs text-slate-600">{getFormatLabel(format)}</span>
                        <span className="text-xs font-medium text-slate-700">{percentage}%</span>
                      </div>
                      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                        <div 
                          className={`h-full ${colors.bar} rounded-full transition-all`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Optimal Mix */}
          <div>
            <h4 className="text-sm font-semibold text-slate-700 mb-4">{labels.optimal}</h4>
            <div className="space-y-3">
              {Object.entries(contentFormats.optimal_mix).map(([format, percentage]) => {
                const Icon = formatIcons[format] || ImageIcon;
                const colors = formatColors[format] || formatColors.single_post;
                return (
                  <div key={format} className="flex items-center gap-3">
                    <div className={`p-1.5 rounded-lg ${colors.bg}`}>
                      <Icon className={colors.text} size={16} />
                    </div>
                    <div className="flex-1">
                      <div className="flex justify-between mb-1">
                        <span className="text-xs text-slate-600">{getFormatLabel(format)}</span>
                        <span className="text-xs font-medium text-slate-700">{percentage}%</span>
                      </div>
                      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                        <div 
                          className={`h-full ${colors.bar} rounded-full transition-all`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Format Gaps */}
        {contentFormats.format_gaps && contentFormats.format_gaps.length > 0 && (
          <div className="mb-6">
            <h4 className="text-sm font-semibold text-slate-700 mb-3">{labels.formatGaps}</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {contentFormats.format_gaps.map((gap, idx) => (
                <div 
                  key={idx}
                  className={`p-3 rounded-xl border ${priorityColors[gap.priority]}`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">{getFormatLabel(gap.format)}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-white/50">
                      {getPriorityLabel(gap.priority)}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-xs">
                    <span>{gap.current}%</span>
                    <TrendingUpIcon size={12} />
                    <span>{gap.optimal}%</span>
                    {gap.gap && <span className="text-green-600">(+{gap.gap}%)</span>}
                    {gap.excess && <span className="text-red-600">(-{gap.excess}%)</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Weekly Targets */}
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
            <TargetIcon className="text-primary-500" size={16} />
            {labels.weeklyTargets}
          </h4>
          <div className="flex gap-4">
            {Object.entries(contentFormats.recommendations.weekly_targets).map(([format, count]) => {
              const Icon = formatIcons[format] || ImageIcon;
              const colors = formatColors[format] || formatColors.single_post;
              return (
                <div 
                  key={format}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl ${colors.bg} border border-opacity-50`}
                >
                  <Icon className={colors.text} size={16} />
                  <span className={`text-sm font-medium ${colors.text}`}>
                    {count} {getFormatLabel(format)}{labels.perWeek}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Growth Channels */}
        {contentFormats.growth_channels && (
          <div>
            <h4 className="text-sm font-semibold text-slate-700 mb-3">{labels.growthChannels}</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {Object.entries(contentFormats.growth_channels).map(([channel, data]) => (
                <div 
                  key={channel}
                  className="p-3 rounded-xl bg-slate-50 border border-slate-200"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-slate-700 capitalize">{channel}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-slate-200 text-slate-600">
                      {getStatusLabel(data.status)}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-500">{labels.potential}:</span>
                    <div className="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-green-500 rounded-full"
                        style={{ width: `${data.potential}%` }}
                      />
                    </div>
                    <span className="text-xs font-medium text-slate-700">{data.potential}%</span>
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

export default ContentFormatAnalysis;
