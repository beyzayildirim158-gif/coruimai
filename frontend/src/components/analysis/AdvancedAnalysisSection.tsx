'use client';

import React, { useState } from 'react';
import { 
  BarChart3Icon, 
  ChevronDownIcon,
  ChevronUpIcon,
  SparkIcon,
  AlertTriangleIcon,
  TrendingUpIcon,
  ShieldIcon
} from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

// Import all Advanced Analysis components
import { AdvancedRiskDashboard } from './AdvancedRiskDashboard';
import { HashtagStrategyCard } from './HashtagStrategyCard';
import { ContentFormatAnalysis } from './ContentFormatAnalysis';
import { ContentDistributionChart } from './ContentDistributionChart';
import { ViralPotentialMeter } from './ViralPotentialMeter';
import { DetailedFindingsPanel } from './DetailedFindingsPanel';
import { ActionPlanTimeline } from './ActionPlanTimeline';

interface AdvancedAnalysisData {
  executiveSummary: {
    score: number;
    grade: string;
    status: string;
    headline: string;
    subheadline: string;
    criticalAlerts: string[];
    quickWins: string[];
    topPriorities: string[];
  };
  detailedFindings: {
    botActivity?: any;
    engagementBenchmarks?: any;
    profileConsistency?: any;
    hashtagStrategy?: any;
    contentFormats?: any;
    contentDistribution?: any;
    shadowbanRisk?: any;
    viralPotential?: any;
    dataQuality?: any;
  };
  riskAssessments: {
    overall: string;
    bot_risk: string;
    shadowban_risk: string;
    algorithm_penalty: string;
    suspension_risk?: string;
    risk_factors?: string[];
  };
  prioritizedRecommendations: {
    immediate: any[];
    short_term: any[];
    medium_term: any[];
    long_term: any[];
  };
  strategies: {
    hashtagStrategy?: any;
    contentFormats?: any;
    contentDistribution?: any;
    viralPotential?: any;
  };
  metadata?: {
    analysis_timestamp: string;
    data_quality_score: number;
    confidence_level: string;
  };
}

interface AdvancedAnalysisSectionProps {
  data: AdvancedAnalysisData;
}

const getGradeColor = (grade: string) => {
  switch (grade.toUpperCase()) {
    case 'A': return 'text-green-600 bg-green-100';
    case 'B': return 'text-blue-600 bg-blue-100';
    case 'C': return 'text-yellow-600 bg-yellow-100';
    case 'D': return 'text-orange-600 bg-orange-100';
    case 'F': return 'text-red-600 bg-red-100';
    default: return 'text-slate-600 bg-slate-100';
  }
};

const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'excellent':
    case 'mükemmel':
      return 'bg-green-50 border-green-200 text-green-700';
    case 'good':
    case 'iyi':
      return 'bg-blue-50 border-blue-200 text-blue-700';
    case 'needs_improvement':
    case 'geliştirilmeli':
      return 'bg-yellow-50 border-yellow-200 text-yellow-700';
    case 'concerning':
    case 'endişe_verici':
      return 'bg-orange-50 border-orange-200 text-orange-700';
    case 'critical':
    case 'kritik':
      return 'bg-red-50 border-red-200 text-red-700';
    default:
      return 'bg-slate-50 border-slate-200 text-slate-700';
  }
};

export const AdvancedAnalysisSection: React.FC<AdvancedAnalysisSectionProps> = ({ data }) => {
  const { locale } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'details' | 'actions'>('overview');

  const labels = {
    title: locale === 'tr' ? 'Gelişmiş Analiz' : 'Advanced Analysis',
    subtitle: locale === 'tr' ? '11 modüllü derin Instagram analizi' : '11-module deep Instagram analysis',
    overview: locale === 'tr' ? 'Genel Bakış' : 'Overview',
    details: locale === 'tr' ? 'Detaylar' : 'Details',
    actions: locale === 'tr' ? 'Aksiyon Planı' : 'Action Plan',
    criticalAlerts: locale === 'tr' ? 'Kritik Uyarılar' : 'Critical Alerts',
    quickWins: locale === 'tr' ? 'Hızlı Kazanımlar' : 'Quick Wins',
    topPriorities: locale === 'tr' ? 'Öncelikler' : 'Top Priorities',
    score: locale === 'tr' ? 'Skor' : 'Score',
    grade: locale === 'tr' ? 'Not' : 'Grade',
    status: locale === 'tr' ? 'Durum' : 'Status',
    dataQuality: locale === 'tr' ? 'Veri Kalitesi' : 'Data Quality',
    confidence: locale === 'tr' ? 'Güven' : 'Confidence',
  };

  const { executiveSummary, detailedFindings, riskAssessments, prioritizedRecommendations, strategies, metadata } = data;

  // Transform riskAssessments to match AdvancedRiskDashboard expected props
  const transformedRiskAssessments = {
    overallRiskLevel: riskAssessments.overall || 'medium',
    botRisk: riskAssessments.bot_risk || 'medium',
    shadowbanRisk: riskAssessments.shadowban_risk || 'medium',
    algorithmPenaltyRisk: riskAssessments.algorithm_penalty || 'medium',
    accountSuspensionRisk: riskAssessments.suspension_risk,
    riskFactors: riskAssessments.risk_factors?.map((factor: string) => ({
      factor,
      severity: 'medium',
      impact: 50,
    })),
  };

  // Prepare bot analysis data for risk dashboard (matching expected interface)
  const botAnalysis = detailedFindings?.botActivity ? {
    bot_score: detailedFindings.botActivity.botPercentage || detailedFindings.botActivity.bot_score || 0,
    authenticity_score: detailedFindings.botActivity.authenticityScore || detailedFindings.botActivity.authenticity_score || (100 - (detailedFindings.botActivity.botPercentage || 0)),
    follower_breakdown: {
      real: detailedFindings.botActivity.breakdown?.real || detailedFindings.botActivity.realFollowers || 0,
      ghost: detailedFindings.botActivity.breakdown?.ghost || detailedFindings.botActivity.suspiciousFollowers || 0,
      bot: detailedFindings.botActivity.breakdown?.bot || detailedFindings.botActivity.confirmedBots || 0,
    },
  } : undefined;

  // Prepare shadowban analysis data (matching expected interface)
  const shadowbanAnalysis = detailedFindings?.shadowbanRisk ? {
    risk_score: detailedFindings.shadowbanRisk.riskScore || detailedFindings.shadowbanRisk.risk_score || 50,
    risk_level: detailedFindings.shadowbanRisk.riskLevel || detailedFindings.shadowbanRisk.risk_level || 'unknown',
    indicators: detailedFindings.shadowbanRisk.indicators || [],
  } : undefined;

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Main Header */}
      <div 
        className="px-6 py-4 bg-gradient-to-r from-primary-50 via-white to-purple-50 border-b border-slate-200 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-primary-100">
              <SparkIcon size={24} className="text-primary-600" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900">✨ {labels.title}</h2>
              <p className="text-sm text-slate-500">{labels.subtitle}</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            {/* Score Badge */}
            <div className="flex items-center gap-3">
              <div className="text-center">
                <div className="text-3xl font-bold text-slate-900">{executiveSummary.score}</div>
                <div className="text-xs text-slate-500">/100</div>
              </div>
              <div className={`px-4 py-2 rounded-xl ${getGradeColor(executiveSummary.grade)}`}>
                <span className="text-2xl font-bold">{executiveSummary.grade}</span>
              </div>
            </div>
            {isExpanded ? (
              <ChevronUpIcon size={20} className="text-slate-400" />
            ) : (
              <ChevronDownIcon size={20} className="text-slate-400" />
            )}
          </div>
        </div>

        {/* Status and Headline */}
        {isExpanded && (
          <div className="mt-4">
            <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm ${getStatusColor(executiveSummary.status)}`}>
              {executiveSummary.status === 'critical' || executiveSummary.status === 'kritik' ? (
                <AlertTriangleIcon size={16} />
              ) : (
                <TrendingUpIcon size={16} />
              )}
              {executiveSummary.status.toUpperCase()}
            </div>
            <h3 className="text-lg font-semibold text-slate-900 mt-2">{executiveSummary.headline}</h3>
            <p className="text-sm text-slate-600">{executiveSummary.subheadline}</p>
          </div>
        )}
      </div>

      {isExpanded && (
        <>
          {/* Tabs */}
          <div className="flex border-b border-slate-200">
            {(['overview', 'details', 'actions'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === tab
                    ? 'text-primary-600 border-b-2 border-primary-600 bg-primary-50/50'
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
              >
                {labels[tab]}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* Critical Alerts */}
                {executiveSummary.criticalAlerts && executiveSummary.criticalAlerts.length > 0 && (
                  <div className="p-4 rounded-xl bg-red-50 border border-red-200">
                    <h4 className="text-sm font-semibold text-red-700 mb-2 flex items-center gap-2">
                      <AlertTriangleIcon size={16} />
                      🚨 {labels.criticalAlerts}
                    </h4>
                    <ul className="space-y-1">
                      {executiveSummary.criticalAlerts.map((alert, idx) => (
                        <li key={idx} className="text-sm text-red-700 flex items-start gap-2">
                          <span>•</span>
                          <span>{alert}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Quick Wins & Priorities Grid */}
                <div className="grid grid-cols-2 gap-4">
                  {/* Quick Wins */}
                  {executiveSummary.quickWins && executiveSummary.quickWins.length > 0 && (
                    <div className="p-4 rounded-xl bg-green-50 border border-green-200">
                      <h4 className="text-sm font-semibold text-green-700 mb-2">⚡ {labels.quickWins}</h4>
                      <ul className="space-y-1">
                        {executiveSummary.quickWins.map((win, idx) => (
                          <li key={idx} className="text-sm text-green-700 flex items-start gap-2">
                            <span>✓</span>
                            <span>{win}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Top Priorities */}
                  {executiveSummary.topPriorities && executiveSummary.topPriorities.length > 0 && (
                    <div className="p-4 rounded-xl bg-blue-50 border border-blue-200">
                      <h4 className="text-sm font-semibold text-blue-700 mb-2">🎯 {labels.topPriorities}</h4>
                      <ol className="space-y-1">
                        {executiveSummary.topPriorities.map((priority, idx) => (
                          <li key={idx} className="text-sm text-blue-700 flex items-start gap-2">
                            <span className="font-medium">{idx + 1}.</span>
                            <span>{priority}</span>
                          </li>
                        ))}
                      </ol>
                    </div>
                  )}
                </div>

                {/* Risk Dashboard */}
                <AdvancedRiskDashboard 
                  riskAssessments={transformedRiskAssessments}
                  botAnalysis={botAnalysis}
                  shadowbanAnalysis={shadowbanAnalysis}
                />

                {/* Hashtag Strategy */}
                {strategies?.hashtagStrategy && (
                  <HashtagStrategyCard hashtagStrategy={strategies.hashtagStrategy} />
                )}

                {/* Content Format Analysis */}
                {strategies?.contentFormats && (
                  <ContentFormatAnalysis contentFormats={strategies.contentFormats} />
                )}

                {/* Content Distribution */}
                {strategies?.contentDistribution && (
                  <ContentDistributionChart contentDistribution={strategies.contentDistribution} />
                )}

                {/* Viral Potential */}
                {strategies?.viralPotential && (
                  <ViralPotentialMeter viralPotential={strategies.viralPotential} />
                )}
              </div>
            )}

            {activeTab === 'details' && (
              <DetailedFindingsPanel findings={detailedFindings} />
            )}

            {activeTab === 'actions' && (
              <ActionPlanTimeline actionPlan={prioritizedRecommendations} />
            )}
          </div>

          {/* Footer with Metadata */}
          {metadata && (
            <div className="px-6 py-3 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
              <div className="flex items-center gap-4">
                <span>{labels.dataQuality}: {metadata.data_quality_score}%</span>
                <span>{labels.confidence}: {metadata.confidence_level}</span>
              </div>
              <span>
                {new Date(metadata.analysis_timestamp).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US')}
              </span>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default AdvancedAnalysisSection;
