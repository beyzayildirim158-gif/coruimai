'use client';

import React, { useState } from 'react';
import { 
  ShieldIcon, 
  ChevronDownIcon, 
  ChevronUpIcon, 
  AlertTriangleIcon, 
  CheckCircleIcon, 
  InfoIcon,
  WrenchIcon,
  TargetIcon,
  TrendingUpIcon
} from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface SanitizationReportData {
  corrections?: Record<string, any>;
  warnings?: string[];
  phase_info?: {
    determined_phase: string;
    phase_name: string;
    health_score: number;
    effective_score: number;
    focus_areas: string[];
    blocked_strategies: string[];
    duration: string;
    reasoning: string;
  };
  metrics_summary?: {
    overall_health: number;
    engagement_depth: number;
    trust_score: number;
    ghost_follower_percent: number;
  };
}

interface SanitizationReportProps {
  data: SanitizationReportData;
}

const getPhaseColor = (phase: string) => {
  switch (phase?.toLowerCase()) {
    case 'rescue':
      return 'bg-red-100 text-red-700 border-red-200';
    case 'growth':
      return 'bg-yellow-100 text-yellow-700 border-yellow-200';
    case 'monetization':
      return 'bg-green-100 text-green-700 border-green-200';
    default:
      return 'bg-slate-100 text-slate-700 border-slate-200';
  }
};

const getPhaseIcon = (phase: string) => {
  switch (phase?.toLowerCase()) {
    case 'rescue':
      return '🚨';
    case 'growth':
      return '📈';
    case 'monetization':
      return '💰';
    default:
      return '📊';
  }
};

export const SanitizationReport: React.FC<SanitizationReportProps> = ({ data }) => {
  const { locale } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(false);

  const labels = {
    title: locale === 'tr' ? 'Veri Tutarlılık Raporu' : 'Data Consistency Report',
    subtitle: locale === 'tr' ? 'Metrik doğrulama ve düzeltmeler' : 'Metric validation and corrections',
    corrections: locale === 'tr' ? 'Yapılan Düzeltmeler' : 'Corrections Made',
    warnings: locale === 'tr' ? 'Uyarılar' : 'Warnings',
    phase: locale === 'tr' ? 'Stratejik Faz' : 'Strategic Phase',
    focusAreas: locale === 'tr' ? 'Odak Alanları' : 'Focus Areas',
    blockedStrategies: locale === 'tr' ? 'Engellenen Stratejiler' : 'Blocked Strategies',
    duration: locale === 'tr' ? 'Tahmini Süre' : 'Estimated Duration',
    reasoning: locale === 'tr' ? 'Gerekçe' : 'Reasoning',
    metricsUsed: locale === 'tr' ? 'Kullanılan Metrikler' : 'Metrics Used',
    noCorrections: locale === 'tr' ? 'Düzeltme gerekli değil' : 'No corrections needed',
    noWarnings: locale === 'tr' ? 'Uyarı yok' : 'No warnings',
  };

  const { corrections, warnings, phase_info, metrics_summary } = data || {};
  const correctionCount = corrections ? Object.keys(corrections).length : 0;
  const warningCount = warnings?.length || 0;

  // Don't render if no data
  if (!corrections && !warnings && !phase_info) {
    return null;
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div 
        className="px-6 py-4 bg-gradient-to-r from-indigo-50 via-white to-purple-50 border-b border-slate-200 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-indigo-100">
              <ShieldIcon className="text-indigo-600" size={24} />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900">🔧 {labels.title}</h2>
              <p className="text-sm text-slate-500">{labels.subtitle}</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            {/* Quick Stats */}
            <div className="flex items-center gap-3">
              {correctionCount > 0 && (
                <span className="flex items-center gap-1 px-3 py-1 rounded-full bg-amber-100 text-amber-700 text-sm font-medium">
                  <WrenchIcon size={12} />
                  {correctionCount}
                </span>
              )}
              {warningCount > 0 && (
                <span className="flex items-center gap-1 px-3 py-1 rounded-full bg-yellow-100 text-yellow-700 text-sm font-medium">
                  <AlertTriangleIcon size={12} />
                  {warningCount}
                </span>
              )}
              {phase_info && (
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getPhaseColor(phase_info.determined_phase)}`}>
                  {getPhaseIcon(phase_info.determined_phase)} {phase_info.phase_name}
                </span>
              )}
            </div>
            {isExpanded ? (
              <ChevronUpIcon className="text-slate-400" size={20} />
            ) : (
              <ChevronDownIcon className="text-slate-400" size={20} />
            )}
          </div>
        </div>
      </div>

      {isExpanded && (
        <div className="p-6 space-y-6">
          {/* Strategic Phase */}
          {phase_info && (
            <div className={`p-4 rounded-xl border ${getPhaseColor(phase_info.determined_phase)}`}>
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h4 className="font-semibold flex items-center gap-2">
                    <TargetIcon size={16} />
                    {labels.phase}: {phase_info.phase_name}
                  </h4>
                  <p className="text-sm mt-1 opacity-80">{phase_info.reasoning}</p>
                </div>
                <span className="text-sm font-medium">{labels.duration}: {phase_info.duration}</span>
              </div>
              
              <div className="grid grid-cols-2 gap-4 mt-4">
                {/* Focus Areas */}
                <div className="bg-white/50 rounded-lg p-3">
                  <h5 className="text-sm font-medium mb-2 flex items-center gap-1">
                    <CheckCircleIcon size={12} />
                    {labels.focusAreas}
                  </h5>
                  <ul className="text-sm space-y-1">
                    {phase_info.focus_areas?.map((area, idx) => (
                      <li key={idx} className="flex items-center gap-1">
                        <span className="text-green-500">✓</span>
                        {area.replace(/_/g, ' ')}
                      </li>
                    ))}
                  </ul>
                </div>
                
                {/* Blocked Strategies */}
                {phase_info.blocked_strategies?.length > 0 && (
                  <div className="bg-white/50 rounded-lg p-3">
                    <h5 className="text-sm font-medium mb-2 flex items-center gap-1">
                      <AlertTriangleIcon size={12} />
                      {labels.blockedStrategies}
                    </h5>
                    <ul className="text-sm space-y-1">
                      {phase_info.blocked_strategies.map((strategy, idx) => (
                        <li key={idx} className="flex items-center gap-1">
                          <span className="text-red-500">✗</span>
                          {strategy.replace(/_/g, ' ')}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              
              {/* Metrics Used */}
              {metrics_summary && (
                <div className="mt-4 pt-3 border-t border-current/20">
                  <h5 className="text-sm font-medium mb-2">{labels.metricsUsed}</h5>
                  <div className="grid grid-cols-4 gap-2">
                    <div className="text-center p-2 bg-white/50 rounded">
                      <div className="text-lg font-bold">{metrics_summary.overall_health}</div>
                      <div className="text-xs opacity-70">Health</div>
                    </div>
                    <div className="text-center p-2 bg-white/50 rounded">
                      <div className="text-lg font-bold">{metrics_summary.engagement_depth}</div>
                      <div className="text-xs opacity-70">Engagement</div>
                    </div>
                    <div className="text-center p-2 bg-white/50 rounded">
                      <div className="text-lg font-bold">{metrics_summary.trust_score}</div>
                      <div className="text-xs opacity-70">Trust</div>
                    </div>
                    <div className="text-center p-2 bg-white/50 rounded">
                      <div className="text-lg font-bold">{metrics_summary.ghost_follower_percent?.toFixed(1)}%</div>
                      <div className="text-xs opacity-70">Ghost</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Corrections */}
          <div className="space-y-3">
            <h4 className="font-semibold text-slate-900 flex items-center gap-2">
              <WrenchIcon size={16} className="text-amber-500" />
              {labels.corrections}
            </h4>
            {correctionCount > 0 ? (
              <div className="space-y-2">
                {Object.entries(corrections || {}).map(([key, value], idx) => (
                  <div key={idx} className="p-3 rounded-lg bg-amber-50 border border-amber-200">
                    <div className="font-medium text-amber-800 capitalize">
                      {key.replace(/_/g, ' ')}
                    </div>
                    <div className="text-sm text-amber-700 mt-1">
                      {typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-3 rounded-lg bg-green-50 border border-green-200 text-green-700 text-sm">
                <CheckCircleIcon size={16} className="inline mr-2" />
                {labels.noCorrections}
              </div>
            )}
          </div>

          {/* Warnings */}
          <div className="space-y-3">
            <h4 className="font-semibold text-slate-900 flex items-center gap-2">
              <AlertTriangleIcon size={16} className="text-yellow-500" />
              {labels.warnings}
            </h4>
            {warningCount > 0 ? (
              <div className="space-y-2">
                {warnings?.map((warning, idx) => (
                  <div key={idx} className="p-3 rounded-lg bg-yellow-50 border border-yellow-200 text-yellow-800 text-sm">
                    <InfoIcon size={16} className="inline mr-2" />
                    {warning}
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-3 rounded-lg bg-green-50 border border-green-200 text-green-700 text-sm">
                <CheckCircleIcon size={16} className="inline mr-2" />
                {labels.noWarnings}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SanitizationReport;
