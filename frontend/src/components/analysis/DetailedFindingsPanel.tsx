'use client';

import React, { useState } from 'react';
import { 
  ChevronDownIcon, 
  ChevronUpIcon,
  BarChart3Icon,
  UsersIcon,
  TargetIcon,
  PaletteIcon,
  HashtagIcon,
  FilmIcon,
  TrendingUpIcon,
  ShieldIcon,
  LightningIcon,
  CheckCircleIcon,
  AlertCircleIcon,
  AlertTriangleIcon
} from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface FindingSection {
  title: string;
  icon: string;
  status: 'good' | 'warning' | 'critical' | 'info';
  summary: string;
  details: string[];
  metrics?: Record<string, number | string>;
  recommendations?: string[];
}

interface DetailedFindingsPanelProps {
  findings: {
    botActivity?: FindingSection;
    engagementBenchmarks?: FindingSection;
    profileConsistency?: FindingSection;
    hashtagStrategy?: FindingSection;
    contentFormats?: FindingSection;
    contentDistribution?: FindingSection;
    shadowbanRisk?: FindingSection;
    viralPotential?: FindingSection;
    dataQuality?: FindingSection;
    [key: string]: FindingSection | undefined;
  };
}

const sectionIcons: Record<string, any> = {
  botActivity: UsersIcon,
  engagementBenchmarks: BarChart3Icon,
  profileConsistency: TargetIcon,
  hashtagStrategy: HashtagIcon,
  contentFormats: FilmIcon,
  contentDistribution: TrendingUpIcon,
  shadowbanRisk: ShieldIcon,
  viralPotential: LightningIcon,
  dataQuality: PaletteIcon,
};

const statusConfig = {
  good: { 
    bg: 'bg-green-50', 
    border: 'border-green-200', 
    text: 'text-green-700',
    icon: CheckCircleIcon,
    label: { tr: 'İyi', en: 'Good' }
  },
  warning: { 
    bg: 'bg-yellow-50', 
    border: 'border-yellow-200', 
    text: 'text-yellow-700',
    icon: AlertTriangleIcon,
    label: { tr: 'Uyarı', en: 'Warning' }
  },
  critical: { 
    bg: 'bg-red-50', 
    border: 'border-red-200', 
    text: 'text-red-700',
    icon: AlertCircleIcon,
    label: { tr: 'Kritik', en: 'Critical' }
  },
  info: { 
    bg: 'bg-blue-50', 
    border: 'border-blue-200', 
    text: 'text-blue-700',
    icon: BarChart3Icon,
    label: { tr: 'Bilgi', en: 'Info' }
  },
};

export const DetailedFindingsPanel: React.FC<DetailedFindingsPanelProps> = ({ findings }) => {
  const { locale } = useTranslation();
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());

  const labels = {
    title: locale === 'tr' ? 'Detaylı Bulgular' : 'Detailed Findings',
    subtitle: locale === 'tr' ? 'Tüm modüllerin ayrıntılı analiz sonuçları' : 'Detailed analysis results from all modules',
    metrics: locale === 'tr' ? 'Metrikler' : 'Metrics',
    recommendations: locale === 'tr' ? 'Öneriler' : 'Recommendations',
    expandAll: locale === 'tr' ? 'Tümünü Aç' : 'Expand All',
    collapseAll: locale === 'tr' ? 'Tümünü Kapat' : 'Collapse All',
    sectionTitles: {
      botActivity: locale === 'tr' ? 'Bot Aktivitesi Analizi' : 'Bot Activity Analysis',
      engagementBenchmarks: locale === 'tr' ? 'Etkileşim Karşılaştırması' : 'Engagement Benchmarks',
      profileConsistency: locale === 'tr' ? 'Profil Tutarlılığı' : 'Profile Consistency',
      hashtagStrategy: locale === 'tr' ? 'Hashtag Stratejisi' : 'Hashtag Strategy',
      contentFormats: locale === 'tr' ? 'İçerik Formatları' : 'Content Formats',
      contentDistribution: locale === 'tr' ? 'İçerik Dağılımı' : 'Content Distribution',
      shadowbanRisk: locale === 'tr' ? 'Shadowban Riski' : 'Shadowban Risk',
      viralPotential: locale === 'tr' ? 'Viral Potansiyel' : 'Viral Potential',
      dataQuality: locale === 'tr' ? 'Veri Kalitesi' : 'Data Quality',
    },
  };

  const getSectionTitle = (key: string) => 
    labels.sectionTitles[key as keyof typeof labels.sectionTitles] || key;

  const toggleSection = (key: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(key)) {
      newExpanded.delete(key);
    } else {
      newExpanded.add(key);
    }
    setExpandedSections(newExpanded);
  };

  const expandAll = () => {
    setExpandedSections(new Set(Object.keys(findings).filter(k => findings[k])));
  };

  const collapseAll = () => {
    setExpandedSections(new Set());
  };

  const validSections = Object.entries(findings).filter(([_, section]) => section);

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 bg-gradient-to-r from-slate-50 to-white border-b border-slate-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <BarChart3Icon size={24} className="text-slate-600" />
            <div>
              <h3 className="text-lg font-semibold text-slate-900">📋 {labels.title}</h3>
              <p className="text-sm text-slate-500">{labels.subtitle}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button 
              onClick={expandAll}
              className="px-3 py-1.5 text-xs rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors"
            >
              {labels.expandAll}
            </button>
            <button 
              onClick={collapseAll}
              className="px-3 py-1.5 text-xs rounded-lg bg-slate-100 text-slate-600 hover:bg-slate-200 transition-colors"
            >
              {labels.collapseAll}
            </button>
          </div>
        </div>
      </div>

      <div className="divide-y divide-slate-200">
        {validSections.map(([key, section]) => {
          if (!section) return null;
          const IconComp = sectionIcons[key] || BarChart3Icon;
          const config = statusConfig[section.status] || statusConfig.info;
          const StatusIcon = config.icon;
          const isExpanded = expandedSections.has(key);

          return (
            <div key={key} className={`${isExpanded ? config.bg : ''}`}>
              {/* Section Header */}
              <button
                onClick={() => toggleSection(key)}
                className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${config.bg}`}>
                    <IconComp size={20} className={config.text} />
                  </div>
                  <div className="text-left">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-slate-900">
                        {section.icon} {getSectionTitle(key)}
                      </span>
                      <span className={`px-2 py-0.5 text-xs rounded-full ${config.bg} ${config.text}`}>
                        {config.label[locale as 'tr' | 'en']}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">{section.summary}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <StatusIcon className={`h-5 w-5 ${config.text}`} />
                  {isExpanded ? (
                    <ChevronUpIcon size={20} className="text-slate-400" />
                  ) : (
                    <ChevronDownIcon size={20} className="text-slate-400" />
                  )}
                </div>
              </button>

              {/* Section Content */}
              {isExpanded && (
                <div className={`px-6 pb-4 ${config.bg}`}>
                  <div className="ml-11 space-y-4">
                    {/* Details */}
                    {section.details && section.details.length > 0 && (
                      <div className="space-y-2">
                        {section.details.map((detail, idx) => (
                          <div key={idx} className="flex items-start gap-2 text-sm text-slate-700">
                            <span className={`mt-0.5 ${config.text}`}>•</span>
                            <span>{detail}</span>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Metrics */}
                    {section.metrics && Object.keys(section.metrics).length > 0 && (
                      <div>
                        <h5 className="text-xs font-semibold text-slate-500 mb-2">{labels.metrics}</h5>
                        <div className="flex flex-wrap gap-2">
                          {Object.entries(section.metrics).map(([metricKey, value]) => (
                            <div 
                              key={metricKey}
                              className="px-3 py-1.5 rounded-lg bg-white/60 border border-slate-200"
                            >
                              <span className="text-xs text-slate-500">{metricKey}: </span>
                              <span className="text-sm font-medium text-slate-700">{String(value)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Recommendations */}
                    {section.recommendations && section.recommendations.length > 0 && (
                      <div>
                        <h5 className="text-xs font-semibold text-slate-500 mb-2">💡 {labels.recommendations}</h5>
                        <div className="p-3 rounded-xl bg-white/60 border border-slate-200">
                          <ul className="space-y-1">
                            {section.recommendations.map((rec, idx) => (
                              <li key={idx} className="flex items-start gap-2 text-sm text-slate-600">
                                <span className="text-primary-500">→</span>
                                <span>{rec}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DetailedFindingsPanel;
