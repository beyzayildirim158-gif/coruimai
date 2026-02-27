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
    <div className="rounded-2xl sm:rounded-3xl border border-slate-200 bg-white p-4 sm:p-6 text-slate-900 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs sm:text-sm uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500">{t('dashboard.latestIntel')}</p>
          <h3 className="text-lg sm:text-2xl font-semibold text-slate-900">{t('dashboard.recentAnalyses')}</h3>
        </div>
        <Link href="/analysis" className="text-xs sm:text-sm text-primary-600 hover:text-primary-700">
          {t('common.viewAll')}
        </Link>
      </div>

      <div className="mt-3 sm:mt-4 divide-y divide-slate-100">
        {isLoading && (
          <div className="flex items-center justify-center py-8 sm:py-10 text-slate-500 text-sm">
            <LoaderIcon className="mr-2 h-4 sm:h-5 w-4 sm:w-5 animate-spin" /> {t('dashboard.fetchingTelemetry')}
          </div>
        )}

        {!isLoading && analyses.length === 0 && (
          <div className="flex flex-col items-center gap-2 py-6 sm:py-8 text-center text-slate-500 text-sm">
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
            className="flex items-center justify-between py-3 sm:py-4 transition hover:bg-slate-50 rounded-lg sm:rounded-xl px-2 -mx-2 gap-2"
          >
            <div className="min-w-0 flex-1">
              <p className="text-xs sm:text-sm uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500 truncate">@{analysis.account?.username}</p>
              <p className="text-sm sm:text-lg font-semibold text-slate-900">{analysis.status}</p>
              <p className="text-xs text-slate-500">
                {new Date(analysis.createdAt).toLocaleString(locale === 'tr' ? 'tr-TR' : 'en-US', {
                  month: 'short',
                  day: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            </div>
            <div className="text-right flex-shrink-0">
              <p className="text-xl sm:text-3xl font-semibold text-primary-600">
                {analysis.overallScore ? `${analysis.overallScore.toFixed(0)}` : '--'}
              </p>
              <p className="text-xs text-slate-500">{analysis.scoreGrade ?? '—'} {t('dashboard.grade')}</p>
            </div>
            <ArrowUpRightIcon className="h-4 w-4 sm:h-5 sm:w-5 text-primary-500 flex-shrink-0" />
          </Link>
        ))}
      </div>
    </div>
  );
}
