'use client';

import React, { useState } from 'react';
import { 
  BarChart3Icon, 
  ChevronDownIcon, 
  ChevronUpIcon, 
  TrendingUpIcon,
  TrendingDownIcon,
  MinusIcon,
  LightningIcon,
  TargetIcon,
  UsersIcon,
  EyeIcon,
  DollarSignIcon,
  HeartIcon,
  PaletteIcon,
  ShieldIcon
} from '@/components/icons';
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
    // Obje içindeki değerleri düzgün formatta göster
    return entries
      .map(([k, v]) => `${k}: ${typeof v === 'object' ? JSON.stringify(v) : v}`)
      .join(' | ');
  }
  return String(value);
}

interface AgentMetrics {
  [key: string]: number | string | any;
}

interface AgentData {
  metrics?: AgentMetrics;
  findings?: any[];
  recommendations?: any[];
  error?: boolean;
  modelUsed?: string;
  vetoed?: boolean;
  vetoReason?: string;
  _strategic_phase?: any;
}

interface ComprehensiveMetricsDashboardProps {
  agentResults: Record<string, AgentData>;
  businessIdentity?: any;
  hardValidation?: any;
}

const agentIcons: Record<string, any> = {
  domainMaster: TargetIcon,
  growthVirality: TrendingUpIcon,
  salesConversion: DollarSignIcon,
  visualBrand: PaletteIcon,
  communityLoyalty: HeartIcon,
  attentionArchitect: EyeIcon,
  systemGovernor: ShieldIcon,
};

const agentColors: Record<string, string> = {
  domainMaster: 'purple',
  growthVirality: 'green',
  salesConversion: 'amber',
  visualBrand: 'pink',
  communityLoyalty: 'red',
  attentionArchitect: 'blue',
  systemGovernor: 'slate',
};

const getScoreColor = (score: number) => {
  if (score >= 80) return 'text-green-600 bg-green-100';
  if (score >= 60) return 'text-blue-600 bg-blue-100';
  if (score >= 40) return 'text-yellow-600 bg-yellow-100';
  if (score >= 20) return 'text-orange-600 bg-orange-100';
  return 'text-red-600 bg-red-100';
};

const getTrendIcon = (change?: number) => {
  if (!change || change === 0) return <MinusIcon size={12} className="text-slate-400" />;
  if (change > 0) return <TrendingUpIcon size={12} className="text-green-500" />;
  return <TrendingDownIcon size={12} className="text-red-500" />;
};

export const ComprehensiveMetricsDashboard: React.FC<ComprehensiveMetricsDashboardProps> = ({
  agentResults,
  businessIdentity,
  hardValidation,
}) => {
  const { locale } = useTranslation();
  const [expandedAgent, setExpandedAgent] = useState<string | null>(null);

  const labels = {
    title: locale === 'tr' ? 'Kapsamlı Metrik Panosu' : 'Comprehensive Metrics Dashboard',
    subtitle: locale === 'tr' ? 'Tüm ajan çıktıları ve skorları' : 'All agent outputs and scores',
    overallScore: locale === 'tr' ? 'Genel Skor' : 'Overall Score',
    findings: locale === 'tr' ? 'Bulgular' : 'Findings',
    recommendations: locale === 'tr' ? 'Öneriler' : 'Recommendations',
    metrics: locale === 'tr' ? 'Metrikler' : 'Metrics',
    modelUsed: locale === 'tr' ? 'Model' : 'Model Used',
    vetoed: locale === 'tr' ? 'Veto Edildi' : 'Vetoed',
    showDetails: locale === 'tr' ? 'Detayları Göster' : 'Show Details',
    hideDetails: locale === 'tr' ? 'Detayları Gizle' : 'Hide Details',
  };

  const agentNames: Record<string, { tr: string; en: string }> = {
    domainMaster: { tr: 'Sektör Uzmanı', en: 'Domain Master' },
    growthVirality: { tr: 'Büyüme Stratejisti', en: 'Growth & Virality' },
    salesConversion: { tr: 'Satış Uzmanı', en: 'Sales Conversion' },
    visualBrand: { tr: 'Görsel Marka', en: 'Visual Brand' },
    communityLoyalty: { tr: 'Topluluk Sadakati', en: 'Community Loyalty' },
    attentionArchitect: { tr: 'Dikkat Mimarı', en: 'Attention Architect' },
    systemGovernor: { tr: 'Sistem Denetçisi', en: 'System Governor' },
  };

  // Extract all metrics from all agents
  const extractAllMetrics = () => {
    const allMetrics: Record<string, { agent: string; value: number | string; key: string }[]> = {};
    
    Object.entries(agentResults || {}).forEach(([agentKey, agentData]) => {
      if (!agentData?.metrics || agentData.error) return;
      
      Object.entries(agentData.metrics).forEach(([metricKey, value]) => {
        if (typeof value === 'number' || typeof value === 'string') {
          if (!allMetrics[metricKey]) {
            allMetrics[metricKey] = [];
          }
          allMetrics[metricKey].push({
            agent: agentKey,
            value,
            key: metricKey,
          });
        }
      });
    });
    
    return allMetrics;
  };

  const allMetrics = extractAllMetrics();
  const agentEntries = Object.entries(agentResults || {}).filter(
    ([key]) => !['eli5Report', 'finalVerdict', 'businessIdentity', 'advancedAnalysis'].includes(key)
  );

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 bg-gradient-to-r from-slate-50 via-white to-blue-50 border-b border-slate-200">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-blue-100">
            <BarChart3Icon size={24} className="text-blue-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">📊 {labels.title}</h2>
            <p className="text-sm text-slate-500">{labels.subtitle}</p>
          </div>
        </div>
      </div>

      <div className="p-6">
        {/* Agent Score Cards Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-6">
          {agentEntries.map(([agentKey, agentData]) => {
            const IconComp = agentIcons[agentKey] || LightningIcon;
            const color = agentColors[agentKey] || 'slate';
            const overallScore = agentData?.metrics?.overallScore || 
                                 agentData?.metrics?.score || 
                                 agentData?.metrics?.totalScore || 0;
            const findingsCount = agentData?.findings?.length || 0;
            const recsCount = agentData?.recommendations?.length || 0;
            
            return (
              <div 
                key={agentKey}
                className={`p-4 rounded-xl border cursor-pointer transition-all hover:shadow-md ${
                  expandedAgent === agentKey ? 'ring-2 ring-primary-500' : ''
                } ${agentData?.vetoed ? 'border-red-200 bg-red-50' : 'border-slate-200 bg-white'}`}
                onClick={() => setExpandedAgent(expandedAgent === agentKey ? null : agentKey)}
              >
                <div className="flex items-center gap-2 mb-2">
                  <div className={`p-1.5 rounded-lg bg-${color}-100`}>
                    <IconComp size={16} className={`text-${color}-600`} />
                  </div>
                  <span className="text-xs font-medium text-slate-600 truncate">
                    {agentNames[agentKey]?.[locale === 'tr' ? 'tr' : 'en'] || agentKey}
                  </span>
                </div>
                
                <div className="flex items-end justify-between">
                  <div>
                    <div className={`text-2xl font-bold ${getScoreColor(Number(overallScore)).split(' ')[0]}`}>
                      {typeof overallScore === 'number' ? overallScore.toFixed(0) : overallScore || '--'}
                    </div>
                    <div className="text-xs text-slate-500">
                      {findingsCount} {locale === 'tr' ? 'bulgu' : 'findings'} • {recsCount} {locale === 'tr' ? 'öneri' : 'recs'}
                    </div>
                  </div>
                  
                  {agentData?.vetoed && (
                    <span className="text-xs px-2 py-0.5 rounded bg-red-200 text-red-700">
                      {labels.vetoed}
                    </span>
                  )}
                </div>
                

              </div>
            );
          })}
        </div>

        {/* Expanded Agent Details */}
        {expandedAgent && agentResults[expandedAgent] && (() => {
          const currentAgent = agentResults[expandedAgent];
          if (!currentAgent) return null;
          
          return (
          <div className="mt-6 p-4 rounded-xl border border-slate-200 bg-slate-50">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-lg text-slate-900">
                {agentNames[expandedAgent]?.[locale === 'tr' ? 'tr' : 'en'] || expandedAgent} - {labels.metrics}
              </h3>
              <button 
                onClick={() => setExpandedAgent(null)}
                className="text-sm text-slate-500 hover:text-slate-700"
              >
                {labels.hideDetails}
              </button>
            </div>
            
            {/* Metrics Grid */}
            {currentAgent?.metrics && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
                {Object.entries(currentAgent.metrics || {}).map(([key, value]) => {
                  // Skip internal keys
                  if (typeof value === 'object') return null;
                  if (key.startsWith('_') || key.endsWith('_note') || key.endsWith('_display')) return null;
                  
                  // Check if this is a zero metric that should show "Veri Yok"
                  const zeroMetrics = (currentAgent.metrics as any)?._zeroMetrics || [];
                  const isZeroMetric = zeroMetrics.includes(key) && value === 0;
                  
                  return (
                    <div key={key} className="p-3 rounded-lg bg-white border border-slate-200">
                      <div className="text-xs text-slate-500 truncate" title={key}>
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </div>
                      <div className={`text-lg font-semibold ${isZeroMetric ? 'text-slate-400' : 'text-slate-900'}`}>
                        {isZeroMetric ? 'Veri Yok' : (typeof value === 'number' ? value.toFixed(1) : String(value))}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
            
            {/* Findings Summary */}
            {currentAgent?.findings && currentAgent.findings.length > 0 && (
              <div className="mt-4">
                <h4 className="text-sm font-medium text-slate-700 mb-2">{labels.findings}</h4>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {currentAgent.findings.slice(0, 5).map((finding: any, idx: number) => {
                    // Extract meaningful text from finding - safely handle objects
                    let text = '';
                    if (typeof finding === 'string') {
                      text = finding;
                    } else if (finding?.text) {
                      text = typeof finding.text === 'string' ? finding.text : safeRenderValue(finding.text);
                    } else if (finding?.finding) {
                      text = typeof finding.finding === 'string' ? finding.finding : safeRenderValue(finding.finding);
                    } else if (finding?.description) {
                      text = typeof finding.description === 'string' ? finding.description : safeRenderValue(finding.description);
                    } else if (finding?.issue) {
                      text = finding.original || (typeof finding.issue === 'string' ? finding.issue : safeRenderValue(finding.issue));
                      if (finding.fix_action) {
                        const fixAction = typeof finding.fix_action === 'string' ? finding.fix_action : safeRenderValue(finding.fix_action);
                        text += ` → ${fixAction}`;
                      }
                    } else if (finding?.original) {
                      text = finding.original;
                    } else {
                      // Find any string property with meaningful content
                      const stringProps = Object.entries(finding || {})
                        .filter(([_, v]) => typeof v === 'string' && String(v).length > 15)
                        .map(([_, v]) => v);
                      text = stringProps[0] as string || safeRenderValue(finding) || `Bulgu ${idx + 1}`;
                    }
                    
                    return (
                      <div key={idx} className="p-2 rounded bg-white border border-slate-200 text-sm">
                        {text}
                      </div>
                    );
                  })}
                  {currentAgent.findings.length > 5 && (
                    <div className="text-xs text-slate-500 text-center">
                      +{currentAgent.findings.length - 5} {locale === 'tr' ? 'daha' : 'more'}
                    </div>
                  )}
                </div>
              </div>
            )}
            
            {/* Recommendations Summary */}
            {currentAgent?.recommendations && currentAgent.recommendations.length > 0 && (
              <div className="mt-4">
                <h4 className="text-sm font-medium text-slate-700 mb-2">{labels.recommendations}</h4>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {currentAgent.recommendations.slice(0, 5).map((rec: any, idx: number) => {
                    // Extract meaningful text from recommendation
                    let text = '';
                    if (typeof rec === 'string') {
                      text = rec;
                    } else if (rec?.action) {
                      text = typeof rec.action === 'string' ? rec.action : safeRenderValue(rec.action);
                    } else if (rec?.recommendation) {
                      text = typeof rec.recommendation === 'string' ? rec.recommendation : safeRenderValue(rec.recommendation);
                    } else if (rec?.text) {
                      text = typeof rec.text === 'string' ? rec.text : safeRenderValue(rec.text);
                    } else if (rec?.fix_action) {
                      text = typeof rec.fix_action === 'string' ? rec.fix_action : safeRenderValue(rec.fix_action);
                      if (rec.expected_impact) {
                        const impact = typeof rec.expected_impact === 'string' ? rec.expected_impact : safeRenderValue(rec.expected_impact);
                        text += ` (${impact})`;
                      }
                    } else if (rec?.issue) {
                      text = rec.original || (typeof rec.issue === 'string' ? rec.issue : safeRenderValue(rec.issue));
                      if (rec.fix_action) {
                        const fixAction = typeof rec.fix_action === 'string' ? rec.fix_action : safeRenderValue(rec.fix_action);
                        text += ` → ${fixAction}`;
                      }
                    } else {
                      // Find any string property with meaningful content
                      const stringProps = Object.entries(rec || {})
                        .filter(([_, v]) => typeof v === 'string' && String(v).length > 10)
                        .map(([_, v]) => v);
                      text = stringProps[0] as string || `Öneri ${idx + 1}`;
                    }
                    
                    return (
                      <div key={idx} className="p-2 rounded bg-green-50 border border-green-200 text-sm">
                        {text}
                      </div>
                    );
                  })}
                  {currentAgent.recommendations.length > 5 && (
                    <div className="text-xs text-slate-500 text-center">
                      +{currentAgent.recommendations.length - 5} {locale === 'tr' ? 'daha' : 'more'}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
          );
        })()}

        {/* Business Identity Summary */}
        {businessIdentity && (
          <div className="mt-6 p-4 rounded-xl border border-purple-200 bg-purple-50">
            <h3 className="font-semibold text-purple-900 mb-2 flex items-center gap-2">
              <UsersIcon size={16} />
              {locale === 'tr' ? 'İşletme Kimliği' : 'Business Identity'}
            </h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-purple-700 font-medium">
                  {locale === 'tr' ? 'Hesap Türü' : 'Account Type'}:
                </span>{' '}
                <span className="text-purple-900">{businessIdentity.account_type || 'N/A'}</span>
              </div>
              {businessIdentity.correct_success_metrics?.length > 0 && (
                <div>
                  <span className="text-purple-700 font-medium">
                    {locale === 'tr' ? 'Doğru Metrikler' : 'Correct Metrics'}:
                  </span>{' '}
                  <span className="text-purple-900">{businessIdentity.correct_success_metrics.join(', ')}</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Hard Validation Results */}
        {hardValidation?.violations?.length > 0 && (
          <div className="mt-6 p-4 rounded-xl border border-red-200 bg-red-50">
            <h3 className="font-semibold text-red-900 mb-2 flex items-center gap-2">
              <ShieldIcon size={16} />
              {locale === 'tr' ? 'Doğrulama İhlalleri' : 'Validation Violations'}
            </h3>
            <ul className="space-y-1">
              {hardValidation.violations.map((v: any, idx: number) => (
                <li key={idx} className="text-sm text-red-800">
                  • <strong>{v.rule}:</strong> {v.message}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ComprehensiveMetricsDashboard;
