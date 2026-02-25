'use client';

import React from 'react';
import { 
  ShieldAlertIcon, 
  BotIcon, 
  EyeIcon, 
  AlertTriangleIcon,
  TrendingDownIcon,
  CheckCircleIcon,
  XCircleIcon,
  AlertCircleIcon
} from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface RiskAssessment {
  overallRiskLevel: string;
  botRisk: string;
  shadowbanRisk: string;
  algorithmPenaltyRisk: string;
  accountSuspensionRisk?: string;
  riskFactors?: Array<{
    factor: string;
    severity: string;
    impact: number;
  }>;
}

interface AdvancedRiskDashboardProps {
  riskAssessments: RiskAssessment;
  botAnalysis?: {
    bot_score: number;
    authenticity_score: number;
    follower_breakdown: {
      real: string | number;
      ghost: string | number;
      bot: string | number;
    };
  };
  shadowbanAnalysis?: {
    risk_score: number | null;  // 🛡️ GÖREV 1: null desteği
    risk_level: string;
    indicators: string[];
    description?: string;  // 🛡️ GÖREV 1: description field eklendi
  };
}

const riskColors: Record<string, { bg: string; text: string; border: string; icon: string }> = {
  low: { bg: 'bg-green-50', text: 'text-green-700', border: 'border-green-200', icon: 'text-green-500' },
  medium: { bg: 'bg-yellow-50', text: 'text-yellow-700', border: 'border-yellow-200', icon: 'text-yellow-500' },
  high: { bg: 'bg-orange-50', text: 'text-orange-700', border: 'border-orange-200', icon: 'text-orange-500' },
  critical: { bg: 'bg-red-50', text: 'text-red-700', border: 'border-red-200', icon: 'text-red-500' },
};

const getRiskColor = (level: string) => riskColors[level?.toLowerCase()] || riskColors.medium;

const RiskIcon = ({ level }: { level: string }) => {
  const normalizedLevel = level?.toLowerCase();
  if (normalizedLevel === 'low') return <CheckCircleIcon size={20} />;
  if (normalizedLevel === 'medium') return <AlertCircleIcon size={20} />;
  if (normalizedLevel === 'high') return <AlertTriangleIcon size={20} />;
  return <XCircleIcon size={20} />;
};

export const AdvancedRiskDashboard: React.FC<AdvancedRiskDashboardProps> = ({
  riskAssessments,
  botAnalysis,
  shadowbanAnalysis,
}) => {
  const { t, locale } = useTranslation();

  const labels = {
    title: locale === 'tr' ? 'Risk Değerlendirmesi' : 'Risk Assessment',
    subtitle: locale === 'tr' ? 'Hesap sağlığı ve güvenlik durumu' : 'Account health and security status',
    overallRisk: locale === 'tr' ? 'Genel Risk' : 'Overall Risk',
    botRisk: locale === 'tr' ? 'Bot/Fake Riski' : 'Bot/Fake Risk',
    shadowbanRisk: locale === 'tr' ? 'Shadowban Riski' : 'Shadowban Risk',
    algorithmRisk: locale === 'tr' ? 'Algoritma Cezası' : 'Algorithm Penalty',
    followerBreakdown: locale === 'tr' ? 'Takipçi Dağılımı' : 'Follower Breakdown',
    real: locale === 'tr' ? 'Gerçek' : 'Real',
    ghost: locale === 'tr' ? 'Ghost' : 'Ghost',
    bot: locale === 'tr' ? 'Bot' : 'Bot',
    riskFactors: locale === 'tr' ? 'Risk Faktörleri' : 'Risk Factors',
    indicators: locale === 'tr' ? 'Göstergeler' : 'Indicators',
    riskLevels: {
      low: locale === 'tr' ? 'Düşük' : 'Low',
      medium: locale === 'tr' ? 'Orta' : 'Medium',
      high: locale === 'tr' ? 'Yüksek' : 'High',
      critical: locale === 'tr' ? 'Kritik' : 'Critical',
    }
  };

  const getRiskLabel = (level: string) => {
    return labels.riskLevels[level?.toLowerCase() as keyof typeof labels.riskLevels] || level;
  };

  const overallColor = getRiskColor(riskAssessments.overallRiskLevel);

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className={`px-6 py-4 border-b ${overallColor.bg} ${overallColor.border}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <ShieldAlertIcon size={24} className={overallColor.icon} />
            <div>
              <h3 className="text-lg font-semibold text-slate-900">🛡️ {labels.title}</h3>
              <p className="text-sm text-slate-500">{labels.subtitle}</p>
            </div>
          </div>
          <div className={`px-4 py-2 rounded-full ${overallColor.bg} ${overallColor.text} ${overallColor.border} border font-semibold`}>
            {labels.overallRisk}: {getRiskLabel(riskAssessments.overallRiskLevel)}
          </div>
        </div>
      </div>

      <div className="p-6">
        {/* Risk Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {/* Bot Risk */}
          <div className={`rounded-2xl border p-4 ${getRiskColor(riskAssessments.botRisk).bg} ${getRiskColor(riskAssessments.botRisk).border}`}>
            <div className="flex items-center gap-2 mb-2">
              <BotIcon size={20} className={getRiskColor(riskAssessments.botRisk).icon} />
              <span className="text-sm font-medium text-slate-700">{labels.botRisk}</span>
            </div>
            <div className="flex items-center gap-2">
              <RiskIcon level={riskAssessments.botRisk} />
              <span className={`text-lg font-bold ${getRiskColor(riskAssessments.botRisk).text}`}>
                {getRiskLabel(riskAssessments.botRisk)}
              </span>
            </div>
            {botAnalysis && (
              <div className="mt-2 text-xs text-slate-500">
                Bot Skoru: {botAnalysis.bot_score}/100
              </div>
            )}
          </div>

          {/* Shadowban Risk */}
          {/* 🛡️ GÖREV 1: DATA FETCH ERROR YÖNETİMİ */}
          {riskAssessments.shadowbanRisk === 'UNKNOWN' || shadowbanAnalysis?.risk_level === 'UNKNOWN' ? (
            // Veri yoksa UNKNOWN durumu göster
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 mb-2">
                <EyeIcon size={20} className="text-slate-400" />
                <span className="text-sm font-medium text-slate-700">{labels.shadowbanRisk}</span>
              </div>
              <div className="flex items-center gap-2 mb-2">
                <AlertCircleIcon size={20} className="text-slate-400" />
                <span className="text-sm font-medium text-slate-600">
                  {locale === 'tr' ? 'Veri Yok' : 'No Data'}
                </span>
              </div>
              <div className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-xs text-blue-800 flex items-start gap-2">
                  <AlertCircleIcon size={16} className="mt-0.5 flex-shrink-0" />
                  <span>
                    {locale === 'tr' 
                      ? '⚠️ Veri Sağlayıcı Hatası: Bu metrik şu an hesaplanamıyor. Hesabınızda sorun olmayabilir.' 
                      : 'ℹ️ Data Provider Error: This metric cannot be calculated right now. Your account may not have issues.'}
                  </span>
                </p>
              </div>
              {shadowbanAnalysis?.description && (
                <div className="mt-2 text-xs text-slate-500">
                  {shadowbanAnalysis.description}
                </div>
              )}
            </div>
          ) : (
            // Normal Shadowban risk gösterimi
            <div className={`rounded-2xl border p-4 ${getRiskColor(riskAssessments.shadowbanRisk).bg} ${getRiskColor(riskAssessments.shadowbanRisk).border}`}>
              <div className="flex items-center gap-2 mb-2">
                <EyeIcon size={20} className={getRiskColor(riskAssessments.shadowbanRisk).icon} />
                <span className="text-sm font-medium text-slate-700">{labels.shadowbanRisk}</span>
              </div>
              <div className="flex items-center gap-2">
                <RiskIcon level={riskAssessments.shadowbanRisk} />
                <span className={`text-lg font-bold ${getRiskColor(riskAssessments.shadowbanRisk).text}`}>
                  {getRiskLabel(riskAssessments.shadowbanRisk)}
                </span>
              </div>
              {shadowbanAnalysis && shadowbanAnalysis.risk_score !== null && (
                <div className="mt-2 text-xs text-slate-500">
                  Risk Skoru: {shadowbanAnalysis.risk_score}/100
                </div>
              )}
            </div>
          )}

          {/* Algorithm Penalty Risk */}
          <div className={`rounded-2xl border p-4 ${getRiskColor(riskAssessments.algorithmPenaltyRisk).bg} ${getRiskColor(riskAssessments.algorithmPenaltyRisk).border}`}>
            <div className="flex items-center gap-2 mb-2">
              <TrendingDownIcon size={20} className={getRiskColor(riskAssessments.algorithmPenaltyRisk).icon} />
              <span className="text-sm font-medium text-slate-700">{labels.algorithmRisk}</span>
            </div>
            <div className="flex items-center gap-2">
              <RiskIcon level={riskAssessments.algorithmPenaltyRisk} />
              <span className={`text-lg font-bold ${getRiskColor(riskAssessments.algorithmPenaltyRisk).text}`}>
                {getRiskLabel(riskAssessments.algorithmPenaltyRisk)}
              </span>
            </div>
          </div>

          {/* Account Suspension Risk */}
          {riskAssessments.accountSuspensionRisk && (
            <div className={`rounded-2xl border p-4 ${getRiskColor(riskAssessments.accountSuspensionRisk).bg} ${getRiskColor(riskAssessments.accountSuspensionRisk).border}`}>
              <div className="flex items-center gap-2 mb-2">
                <AlertTriangleIcon size={20} className={getRiskColor(riskAssessments.accountSuspensionRisk).icon} />
                <span className="text-sm font-medium text-slate-700">
                  {locale === 'tr' ? 'Askıya Alma' : 'Suspension'}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <RiskIcon level={riskAssessments.accountSuspensionRisk} />
                <span className={`text-lg font-bold ${getRiskColor(riskAssessments.accountSuspensionRisk).text}`}>
                  {getRiskLabel(riskAssessments.accountSuspensionRisk)}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Follower Breakdown */}
        {botAnalysis?.follower_breakdown && (
          <div className="mb-6">
            <h4 className="text-sm font-semibold text-slate-700 mb-3">{labels.followerBreakdown}</h4>
            <div className="flex rounded-full overflow-hidden h-6 bg-slate-100">
              <div 
                className="bg-green-500 flex items-center justify-center text-xs text-white font-medium"
                style={{ width: `${botAnalysis.follower_breakdown.real}%` }}
              >
                {Number(botAnalysis.follower_breakdown.real) > 10 && `${botAnalysis.follower_breakdown.real}%`}
              </div>
              <div 
                className="bg-yellow-500 flex items-center justify-center text-xs text-white font-medium"
                style={{ width: `${botAnalysis.follower_breakdown.ghost}%` }}
              >
                {Number(botAnalysis.follower_breakdown.ghost) > 10 && `${botAnalysis.follower_breakdown.ghost}%`}
              </div>
              <div 
                className="bg-red-500 flex items-center justify-center text-xs text-white font-medium"
                style={{ width: `${botAnalysis.follower_breakdown.bot}%` }}
              >
                {Number(botAnalysis.follower_breakdown.bot) > 10 && `${botAnalysis.follower_breakdown.bot}%`}
              </div>
            </div>
            <div className="flex gap-4 mt-2 text-xs">
              <span className="flex items-center gap-1">
                <span className="w-3 h-3 rounded-full bg-green-500"></span>
                {labels.real}: {botAnalysis.follower_breakdown.real}%
              </span>
              <span className="flex items-center gap-1">
                <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
                {labels.ghost}: {botAnalysis.follower_breakdown.ghost}%
              </span>
              <span className="flex items-center gap-1">
                <span className="w-3 h-3 rounded-full bg-red-500"></span>
                {labels.bot}: {botAnalysis.follower_breakdown.bot}%
              </span>
            </div>
          </div>
        )}

        {/* Shadowban Indicators */}
        {shadowbanAnalysis?.indicators && shadowbanAnalysis.indicators.length > 0 && (
          <div className="mb-6">
            <h4 className="text-sm font-semibold text-slate-700 mb-3">{labels.indicators}</h4>
            <div className="flex flex-wrap gap-2">
              {shadowbanAnalysis.indicators.slice(0, 5).map((indicator, idx) => (
                <span 
                  key={idx}
                  className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-orange-100 text-orange-700 text-xs"
                >
                  <AlertCircleIcon size={12} />
                  {indicator}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Risk Factors */}
        {riskAssessments.riskFactors && riskAssessments.riskFactors.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-slate-700 mb-3">{labels.riskFactors}</h4>
            <div className="space-y-2">
              {riskAssessments.riskFactors.slice(0, 5).map((factor, idx) => (
                <div 
                  key={idx}
                  className={`flex items-center justify-between p-3 rounded-xl border ${getRiskColor(factor.severity).bg} ${getRiskColor(factor.severity).border}`}
                >
                  <div className="flex items-center gap-2">
                    <RiskIcon level={factor.severity} />
                    <span className="text-sm text-slate-700">{factor.factor}</span>
                  </div>
                  <span className={`text-sm font-medium ${getRiskColor(factor.severity).text}`}>
                    Impact: {factor.impact}/100
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdvancedRiskDashboard;
