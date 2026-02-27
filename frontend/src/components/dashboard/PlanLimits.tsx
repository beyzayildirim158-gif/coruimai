'use client';

import Link from 'next/link';
import { ArrowUpRightIcon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface PlanLimitsProps {
  tierName?: string;
  limitUsed?: number;
  limitTotal?: number;
  features?: Record<string, boolean>;
}

export function PlanLimits({ tierName, limitUsed, limitTotal, features = {} }: PlanLimitsProps) {
  const { t, locale } = useTranslation();
  
  const featureLabels: Record<string, string> = {
    pdfReports: locale === 'tr' ? 'PDF istihbarat raporları' : 'PDF intelligence reports',
    brandedReports: locale === 'tr' ? 'Markalı dışa aktarımlar' : 'Branded exports',
    whiteLabelReports: locale === 'tr' ? 'Beyaz etiket modu' : 'White-label mode',
    apiAccess: locale === 'tr' ? 'API erişimi' : 'API access',
    botDetection: locale === 'tr' ? 'Gelişmiş bot tespiti' : 'Advanced bot detection',
    customAgents: locale === 'tr' ? 'Özel AI ajanları' : 'Custom AI agents',
    multiUser: locale === 'tr' ? 'Çoklu kullanıcı çalışma alanı' : 'Multi-seat workspace',
  };

  const limitPercent = limitTotal && limitTotal > 0 ? Math.min(100, Math.round(((limitUsed ?? 0) / limitTotal) * 100)) : 0;
  const isNearLimit = limitPercent >= 80;

  return (
    <div className="rounded-2xl sm:rounded-3xl border border-slate-200 bg-gradient-to-b from-primary-50 to-white p-4 sm:p-6 text-slate-900 shadow-sm">
      <p className="text-xs sm:text-sm uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500">
        {locale === 'tr' ? 'Plan telemetrisi' : 'Plan telemetry'}
      </p>
      <h3 className="text-lg sm:text-2xl font-semibold text-slate-900">
        {tierName ?? 'STARTER'} {locale === 'tr' ? 'seviyesi' : 'tier'}
      </h3>
      {limitTotal && limitTotal > 0 && (
        <div className="mt-4">
          <div className="flex items-center justify-between text-sm text-slate-600">
            <span>{t('usage.analysesUsed')}</span>
            <span className={isNearLimit ? 'text-amber-600' : ''}>
              {limitUsed ?? 0} / {limitTotal}
            </span>
          </div>
          <div className="mt-2 h-2 rounded-full bg-slate-200">
            <div 
              className={`h-full rounded-full ${isNearLimit ? 'bg-gradient-to-r from-amber-500 to-red-500' : 'bg-gradient-to-r from-primary-500 to-primary-400'}`} 
              style={{ width: `${limitPercent}%` }} 
            />
          </div>
          {isNearLimit && (
            <p className="mt-2 text-xs text-amber-600">
              {locale === 'tr' 
                ? 'Analiz kotanız azalıyor. Planınızı yükseltmeyi düşünün.'
                : 'Running low on analyses. Consider upgrading your plan.'}
            </p>
          )}
        </div>
      )}
      <div className="mt-4 sm:mt-5 space-y-2 sm:space-y-3 text-xs sm:text-sm text-slate-700">
        {Object.entries(features).map(([key, value]) => (
          <div key={key} className="flex items-center justify-between rounded-xl sm:rounded-2xl border border-slate-200 bg-slate-50 px-3 sm:px-4 py-2">
            <span className="truncate mr-2">{featureLabels[key] ?? key}</span>
            <span className={`flex-shrink-0 ${value ? 'text-emerald-600' : 'text-slate-400'}`}>
              {value 
                ? (locale === 'tr' ? 'Dahil' : 'Included')
                : (locale === 'tr' ? 'Kilitli' : 'Locked')}
            </span>
          </div>
        ))}
      </div>
      
      {/* Upgrade CTA */}
      {tierName !== 'ENTERPRISE' && (
        <Link
          href="/billing"
          className="mt-4 sm:mt-5 flex items-center justify-center gap-2 rounded-xl sm:rounded-2xl bg-primary-600 px-4 py-2.5 sm:py-3 text-xs sm:text-sm font-semibold text-white hover:bg-primary-700 transition-colors"
        >
          {locale === 'tr' ? 'Planı yükselt' : 'Upgrade plan'}
          <ArrowUpRightIcon className="h-4 w-4" />
        </Link>
      )}
    </div>
  );
}
