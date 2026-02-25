'use client';

import React, { useState } from 'react';
import { 
  ClockIcon,
  LightningIcon,
  CalendarDaysIcon,
  CalendarRangeIcon,
  TimerIcon,
  CheckCircle2Icon,
  CircleIcon,
  ChevronRightIcon
} from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface ActionItem {
  id: string;
  title: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  category: string;
  estimatedImpact: string;
  effort: string;
  status?: 'pending' | 'in_progress' | 'completed';
}

interface ActionPlan {
  immediate: ActionItem[];
  short_term: ActionItem[];
  medium_term: ActionItem[];
  long_term: ActionItem[];
}

interface ActionPlanTimelineProps {
  actionPlan: ActionPlan;
}

const timeframeConfig = {
  immediate: {
    icon: LightningIcon,
    color: 'text-red-600',
    bgLight: 'bg-red-50',
    bgDark: 'bg-red-500',
    border: 'border-red-200',
    label: { tr: 'Acil (Bu Hafta)', en: 'Immediate (This Week)' },
    dot: 'bg-red-500',
  },
  short_term: {
    icon: ClockIcon,
    color: 'text-orange-600',
    bgLight: 'bg-orange-50',
    bgDark: 'bg-orange-500',
    border: 'border-orange-200',
    label: { tr: 'Kısa Vadeli (2-4 Hafta)', en: 'Short Term (2-4 Weeks)' },
    dot: 'bg-orange-500',
  },
  medium_term: {
    icon: CalendarDaysIcon,
    color: 'text-blue-600',
    bgLight: 'bg-blue-50',
    bgDark: 'bg-blue-500',
    border: 'border-blue-200',
    label: { tr: 'Orta Vadeli (1-3 Ay)', en: 'Medium Term (1-3 Months)' },
    dot: 'bg-blue-500',
  },
  long_term: {
    icon: CalendarRangeIcon,
    color: 'text-purple-600',
    bgLight: 'bg-purple-50',
    bgDark: 'bg-purple-500',
    border: 'border-purple-200',
    label: { tr: 'Uzun Vadeli (3+ Ay)', en: 'Long Term (3+ Months)' },
    dot: 'bg-purple-500',
  },
};

const priorityConfig = {
  critical: { bg: 'bg-red-100', text: 'text-red-700', label: { tr: 'Kritik', en: 'Critical' } },
  high: { bg: 'bg-orange-100', text: 'text-orange-700', label: { tr: 'Yüksek', en: 'High' } },
  medium: { bg: 'bg-yellow-100', text: 'text-yellow-700', label: { tr: 'Orta', en: 'Medium' } },
  low: { bg: 'bg-green-100', text: 'text-green-700', label: { tr: 'Düşük', en: 'Low' } },
};

export const ActionPlanTimeline: React.FC<ActionPlanTimelineProps> = ({ actionPlan }) => {
  const { locale } = useTranslation();
  const [expandedTimeframes, setExpandedTimeframes] = useState<Set<string>>(new Set(['immediate', 'short_term']));

  const labels = {
    title: locale === 'tr' ? 'Aksiyon Planı' : 'Action Plan',
    subtitle: locale === 'tr' ? 'Önceliklendirilmiş büyüme stratejisi' : 'Prioritized growth strategy',
    impact: locale === 'tr' ? 'Etki' : 'Impact',
    effort: locale === 'tr' ? 'Efor' : 'Effort',
    category: locale === 'tr' ? 'Kategori' : 'Category',
    noActions: locale === 'tr' ? 'Bu dönem için aksiyon yok' : 'No actions for this period',
    totalActions: locale === 'tr' ? 'toplam aksiyon' : 'total actions',
  };

  const toggleTimeframe = (timeframe: string) => {
    const newExpanded = new Set(expandedTimeframes);
    if (newExpanded.has(timeframe)) {
      newExpanded.delete(timeframe);
    } else {
      newExpanded.add(timeframe);
    }
    setExpandedTimeframes(newExpanded);
  };

  // Count total actions
  const totalActions = Object.values(actionPlan).reduce((sum, actions) => sum + (actions?.length || 0), 0);

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 bg-gradient-to-r from-emerald-50 to-white border-b border-slate-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <TimerIcon className="text-emerald-500" size={24} />
            <div>
              <h3 className="text-lg font-semibold text-slate-900">🎯 {labels.title}</h3>
              <p className="text-sm text-slate-500">{labels.subtitle}</p>
            </div>
          </div>
          <div className="px-3 py-1.5 rounded-xl bg-emerald-100 text-emerald-700 text-sm font-medium">
            {totalActions} {labels.totalActions}
          </div>
        </div>
      </div>

      <div className="p-6">
        {/* Timeline */}
        <div className="relative">
          {/* Vertical Line */}
          <div className="absolute left-[19px] top-0 bottom-0 w-0.5 bg-slate-200" />

          {Object.entries(actionPlan).map(([timeframe, actions], index) => {
            const config = timeframeConfig[timeframe as keyof typeof timeframeConfig];
            if (!config) return null;
            
            const Icon = config.icon;
            const isExpanded = expandedTimeframes.has(timeframe);
            const hasActions = actions && actions.length > 0;

            return (
              <div key={timeframe} className="relative mb-6 last:mb-0">
                {/* Timeframe Header */}
                <button
                  onClick={() => toggleTimeframe(timeframe)}
                  className="relative flex items-center gap-4 w-full text-left group"
                >
                  {/* Dot */}
                  <div className={`relative z-10 w-10 h-10 rounded-full ${config.bgLight} ${config.border} border-2 flex items-center justify-center`}>
                    <Icon className={config.color} size={20} />
                  </div>

                  {/* Label */}
                  <div className="flex-1 flex items-center justify-between">
                    <div>
                      <h4 className={`text-sm font-semibold ${config.color}`}>
                        {config.label[locale as 'tr' | 'en']}
                      </h4>
                      {hasActions && (
                        <span className="text-xs text-slate-500">
                          {actions.length} {locale === 'tr' ? 'aksiyon' : 'actions'}
                        </span>
                      )}
                    </div>
                    <ChevronRightIcon 
                      className={`text-slate-400 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                      size={20}
                    />
                  </div>
                </button>

                {/* Actions */}
                {isExpanded && (
                  <div className="ml-14 mt-3 space-y-3">
                    {hasActions ? (
                      actions.map((action: ActionItem, idx: number) => {
                        const prConfig = priorityConfig[action.priority] || priorityConfig.medium;
                        return (
                          <div 
                            key={action.id || idx}
                            className={`p-4 rounded-xl ${config.bgLight} ${config.border} border`}
                          >
                            <div className="flex items-start justify-between mb-2">
                              <div className="flex items-center gap-2">
                                {action.status === 'completed' ? (
                                  <CheckCircle2Icon className="text-green-500" size={16} />
                                ) : (
                                  <CircleIcon className={config.color} size={16} />
                                )}
                                <h5 className="text-sm font-medium text-slate-900">{action.title}</h5>
                              </div>
                              <span className={`px-2 py-0.5 text-xs rounded-full ${prConfig.bg} ${prConfig.text}`}>
                                {prConfig.label[locale as 'tr' | 'en']}
                              </span>
                            </div>
                            
                            <p className="text-sm text-slate-600 mb-3">{action.description}</p>
                            
                            <div className="flex flex-wrap gap-2">
                              {action.category && (
                                <span className="px-2 py-1 text-xs rounded-lg bg-white/50 text-slate-600 border border-slate-200">
                                  {labels.category}: {action.category}
                                </span>
                              )}
                              {action.estimatedImpact && (
                                <span className="px-2 py-1 text-xs rounded-lg bg-green-50 text-green-700 border border-green-200">
                                  {labels.impact}: {action.estimatedImpact}
                                </span>
                              )}
                              {action.effort && (
                                <span className="px-2 py-1 text-xs rounded-lg bg-blue-50 text-blue-700 border border-blue-200">
                                  {labels.effort}: {action.effort}
                                </span>
                              )}
                            </div>
                          </div>
                        );
                      })
                    ) : (
                      <p className="text-sm text-slate-400 italic p-3">
                        {labels.noActions}
                      </p>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ActionPlanTimeline;
