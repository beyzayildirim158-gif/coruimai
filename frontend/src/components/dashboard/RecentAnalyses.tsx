import Link from 'next/link';
import { Analysis } from '@/store/analysisStore';
import { ArrowUpRightIcon, LoaderIcon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface RecentAnalysesProps {
  analyses?: Analysis[];
  isLoading?: boolean;
}

export function RecentAnalyses({ analyses = [], isLoading }: RecentAnalysesProps) {
  const { t, locale } = useTranslation();
  
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500">{t('dashboard.latestIntel')}</p>
          <h3 className="text-2xl font-semibold text-slate-900">{t('dashboard.recentAnalyses')}</h3>
        </div>
        <Link href="/analysis" className="text-sm text-primary-600 hover:text-primary-700">
          {t('common.viewAll')}
        </Link>
      </div>

      <div className="mt-4 divide-y divide-slate-100">
        {isLoading && (
          <div className="flex items-center justify-center py-10 text-slate-500">
            <LoaderIcon className="mr-2 h-5 w-5 animate-spin" /> {t('dashboard.fetchingTelemetry')}
          </div>
        )}

        {!isLoading && analyses.length === 0 && (
          <div className="flex flex-col items-center gap-2 py-8 text-center text-slate-500">
            <p>{t('dashboard.noAnalysesYet')}</p>
            <Link href="/analysis" className="text-primary-600 hover:text-primary-700">
              {t('dashboard.launchFirst')}
            </Link>
          </div>
        )}

        {analyses.slice(0, 5).map((analysis) => (
          <Link
            key={analysis.id}
            href={`/analysis/${analysis.id}`}
            className="flex items-center justify-between py-4 transition hover:bg-slate-50 rounded-xl px-2 -mx-2"
          >
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-slate-500">@{analysis.account?.username}</p>
              <p className="text-lg font-semibold text-slate-900">{analysis.status}</p>
              <p className="text-xs text-slate-500">
                {new Date(analysis.createdAt).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US', {
                  month: 'short',
                  day: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            </div>
            <div className="text-right">
              <p className="text-3xl font-semibold text-primary-600">
                {analysis.overallScore ? `${analysis.overallScore.toFixed(0)}` : '--'}
              </p>
              <p className="text-xs text-slate-500">{analysis.scoreGrade ?? '—'} {t('dashboard.grade')}</p>
            </div>
            <ArrowUpRightIcon className="h-5 w-5 text-primary-500" />
          </Link>
        ))}
      </div>
    </div>
  );
}
