"use client";

import { BriefcaseIcon, UserIcon, SparkIcon, BarChart3Icon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface BusinessIdentityData {
  is_service_provider?: boolean;
  account_type?: string;
  category?: string;
  confidence?: number;
  indicators_found?: string[];
  service_signals_in_bio?: number;
  correct_success_metrics?: string[];
  wrong_metrics_to_avoid?: string[];
  benchmark_engagement?: number;
  analysis_note?: string;
}

interface Props {
  data: BusinessIdentityData;
}

function getAccountTypeIcon(type: string | undefined) {
  if (!type) return <UserIcon size={20} />;
  const t = type.toLowerCase();
  if (t.includes('service') || t.includes('business')) return <BriefcaseIcon size={20} />;
  if (t.includes('creator') || t.includes('influencer')) return <SparkIcon size={20} />;
  return <UserIcon size={20} />;
}

function getAccountTypeColor(type: string | undefined): { bg: string; text: string; border: string } {
  if (!type) return { bg: 'bg-slate-100', text: 'text-slate-700', border: 'border-slate-200' };
  const t = type.toLowerCase();
  if (t.includes('service') || t.includes('business')) {
    return { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' };
  }
  if (t.includes('creator') || t.includes('influencer')) {
    return { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200' };
  }
  return { bg: 'bg-slate-100', text: 'text-slate-700', border: 'border-slate-200' };
}

export function BusinessIdentity({ data }: Props) {
  const { locale } = useTranslation();
  
  if (!data || Object.keys(data).length === 0) {
    return null;
  }

  const colors = getAccountTypeColor(data.account_type);
  const confidencePercent = data.confidence ? Math.round(data.confidence * 100) : 0;

  return (
    <div className={`rounded-3xl border ${colors.border} ${colors.bg} p-6 shadow-sm`}>
      <div className="flex items-start gap-4">
        <div className={`flex h-12 w-12 items-center justify-center rounded-xl ${colors.bg} ${colors.text} border ${colors.border}`}>
          {getAccountTypeIcon(data.account_type)}
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">
              {locale === 'tr' ? 'Hesap Türü' : 'Account Type'}
            </p>
            {confidencePercent > 0 && (
              <span className="rounded-full bg-white px-2 py-0.5 text-xs text-slate-500">
                {confidencePercent}% {locale === 'tr' ? 'güvenilirlik' : 'confidence'}
              </span>
            )}
          </div>
          <h3 className={`text-xl font-bold ${colors.text} mb-2`}>
            {data.account_type?.replace(/_/g, ' ') || (locale === 'tr' ? 'Bilinmiyor' : 'Unknown')}
          </h3>
          
          {data.analysis_note && (
            <p className="text-sm text-slate-700 mb-4">{data.analysis_note}</p>
          )}

          {/* Success Metrics */}
          {data.correct_success_metrics && data.correct_success_metrics.length > 0 && (
            <div className="mb-4">
              <p className="text-xs uppercase tracking-wider text-slate-500 mb-2">
                {locale === 'tr' ? 'Takip Edilmesi Gereken Metrikler' : 'Metrics to Track'}
              </p>
              <div className="flex flex-wrap gap-2">
                {data.correct_success_metrics.map((metric, idx) => (
                  <span key={idx} className="inline-flex items-center rounded-full bg-white px-3 py-1 text-xs font-medium text-green-700 border border-green-200">
                    <BarChart3Icon className="mr-1" size={12} />
                    {metric.replace(/_/g, ' ')}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Wrong Metrics */}
          {data.wrong_metrics_to_avoid && data.wrong_metrics_to_avoid.length > 0 && (
            <div className="mb-4">
              <p className="text-xs uppercase tracking-wider text-slate-500 mb-2">
                {locale === 'tr' ? 'Yanıltıcı Metrikler' : 'Misleading Metrics'}
              </p>
              <div className="flex flex-wrap gap-2">
                {data.wrong_metrics_to_avoid.map((metric, idx) => (
                  <span key={idx} className="inline-flex items-center rounded-full bg-white px-3 py-1 text-xs font-medium text-red-600 border border-red-200 line-through">
                    {metric.replace(/_/g, ' ')}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Benchmark */}
          {data.benchmark_engagement !== undefined && (
            <div className="rounded-xl bg-white/80 border border-slate-200 p-3">
              <p className="text-xs text-slate-500 mb-1">
                {locale === 'tr' ? 'Sektör Benchmark Etkileşim Oranı' : 'Industry Benchmark Engagement Rate'}
              </p>
              <p className="text-lg font-bold text-slate-900">
                %{data.benchmark_engagement.toFixed(1)}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default BusinessIdentity;
