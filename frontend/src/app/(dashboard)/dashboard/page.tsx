"use client";

import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ActivityIcon, TrophyIcon, TargetIcon, FileTextIcon, LoaderIcon } from '@/components/icons';
import api from '@/lib/api';
import { StatCard } from '@/components/common/StatCard';
import { UsageOverview } from '@/components/dashboard/UsageOverview';
import { PlanLimits } from '@/components/dashboard/PlanLimits';
import { RecentAnalyses } from '@/components/dashboard/RecentAnalyses';
import Link from 'next/link';
import { formatDateTime } from '@/lib/formatters';
import { useTranslation } from '@/i18n/TranslationProvider';

export default function DashboardPage() {
  const { t, locale } = useTranslation();

  const statsQuery = useQuery({
    queryKey: ['usage', 'stats'],
    queryFn: async () => {
      const response = await api.get('/usage/stats');
      return response.data.data;
    },
  });

  const currentUsageQuery = useQuery({
    queryKey: ['usage', 'current'],
    queryFn: async () => {
      const response = await api.get('/usage/current');
      return response.data.data;
    },
  });

  const usageHistoryQuery = useQuery({
    queryKey: ['usage', 'history', { months: 6 }],
    queryFn: async () => {
      const response = await api.get('/usage/history?months=6');
      return response.data.data;
    },
  });

  const reportsQuery = useQuery({
    queryKey: ['reports', 'recent'],
    queryFn: async () => {
      const response = await api.get('/reports', {
        params: { limit: 5 },
      });
      return response.data.data;
    },
  });

  const analysesQuery = useQuery({
    queryKey: ['analysis', 'history', { limit: 5 }],
    queryFn: async () => {
      const response = await api.get('/analyze/history?limit=5');
      return response.data.data;
    },
  });

  const statCards = useMemo(() => {
    const stats = statsQuery.data;
    return [
      {
        label: locale === 'tr' ? 'Toplam analiz' : 'Total analyses',
        value: stats?.totalAnalyses?.toString() ?? '0',
        helper: `${stats?.completedAnalyses ?? 0} ${locale === 'tr' ? 'tamamlandı' : 'completed'}`,
        icon: <ActivityIcon size={20} />,
        href: '/analysis',
      },
      {
        label: locale === 'tr' ? 'Başarı oranı' : 'Success rate',
        value: stats?.successRate ? `${stats.successRate}%` : '—',
        helper: `${stats?.failedAnalyses ?? 0} ${locale === 'tr' ? 'hata' : 'failures'}`,
        icon: <TargetIcon size={20} />,
        tone: 'success' as const,
        href: '/usage',
      },
      {
        label: locale === 'tr' ? 'Ortalama skor' : 'Average score',
        value: stats?.averageScore ? stats.averageScore : '—',
        helper: locale === 'tr' ? 'Tamamlanan analizlerde' : 'Across completed analyses',
        icon: <TrophyIcon size={20} />,
        href: '/analysis',
      },
      {
        label: locale === 'tr' ? 'Rapor sayısı' : 'Reports issued',
        value: stats?.totalReports?.toString() ?? '0',
        helper: `${stats?.accountsAnalyzed ?? 0} ${locale === 'tr' ? 'hesap analiz edildi' : 'accounts analyzed'}`,
        icon: <FileTextIcon size={20} />,
        href: '/reports',
      },
    ];
  }, [statsQuery.data, locale]);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-3 sm:gap-4 md:grid-cols-2 xl:grid-cols-4">
        {statCards.map((card) => (
          <StatCard key={card.label} {...card} />
        ))}
      </div>

      <div className="grid gap-4 sm:gap-6 lg:grid-cols-5">
        <div className="lg:col-span-3">
          {usageHistoryQuery.isLoading ? (
            <div className="flex h-56 sm:h-72 items-center justify-center rounded-2xl sm:rounded-3xl border border-slate-200 bg-white text-slate-500 shadow-sm text-sm sm:text-base">
              <LoaderIcon size={20} className="mr-2" /> {locale === 'tr' ? 'Kullanım trendleri yükleniyor...' : 'Loading usage trends...'}
            </div>
          ) : (
            <UsageOverview usage={usageHistoryQuery.data?.usage ?? []} monthlyLimit={currentUsageQuery.data?.analyses?.limit} />
          )}
        </div>
        <div className="lg:col-span-2">
          <PlanLimits
            tierName={currentUsageQuery.data?.tier?.name}
            limitUsed={currentUsageQuery.data?.analyses?.used}
            limitTotal={currentUsageQuery.data?.analyses?.limit}
            features={currentUsageQuery.data?.tier?.features}
          />
        </div>
      </div>

      <div className="grid gap-4 sm:gap-6 lg:grid-cols-5">
        <div className="lg:col-span-3">
          <RecentAnalyses analyses={analysesQuery.data} isLoading={analysesQuery.isLoading} />
        </div>
        <div className="space-y-3 rounded-2xl sm:rounded-3xl border border-slate-200 bg-white p-4 sm:p-6 lg:col-span-2 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs sm:text-sm uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500">
                {locale === 'tr' ? 'Son PDF\'ler' : 'Latest PDFs'}
              </p>
              <h3 className="text-lg sm:text-2xl font-semibold text-slate-900">
                {locale === 'tr' ? 'Rapor kuyruğu' : 'Report queue'}
              </h3>
            </div>
            <Link href="/reports" className="text-sm text-primary-600 hover:text-primary-700">
              {t('common.viewAll')}
            </Link>
          </div>

          {reportsQuery.isLoading && (
            <div className="flex items-center justify-center py-10 text-slate-500">
              <LoaderIcon size={16} className="mr-2" /> {locale === 'tr' ? 'Yazıcı kontrol ediliyor...' : 'Checking printer...'}
            </div>
          )}

          {!reportsQuery.isLoading && (reportsQuery.data?.reports?.length ?? 0) === 0 && (
            <p className="py-10 text-center text-sm text-slate-500">
              {locale === 'tr' ? 'Henüz PDF raporu oluşturulmadı.' : 'No PDF reports generated yet.'}
            </p>
          )}

          {reportsQuery.data?.reports?.map((report: any) => (
            <div key={report.id} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <div className="flex items-center justify-between text-sm">
                <div>
                  <p className="font-semibold text-slate-900">@{report.analysis?.account?.username}</p>
                  <p className="text-xs text-slate-500">{report.reportType} · {formatDateTime(report.generatedAt)}</p>
                </div>
                {report.pdfUrl ? (
                  <Link href={report.pdfUrl} target="_blank" rel="noreferrer" className="text-xs text-primary-600 hover:text-primary-700">
                    {locale === 'tr' ? 'İndir' : 'Download'}
                  </Link>
                ) : (
                  <span className="text-xs text-slate-400">{locale === 'tr' ? 'İşleniyor' : 'Processing'}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
