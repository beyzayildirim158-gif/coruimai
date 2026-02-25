"use client";

import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import { UsageOverview } from '@/components/dashboard/UsageOverview';
import { StatCard } from '@/components/common/StatCard';
import { formatNumber } from '@/lib/formatters';
import { ActivityIcon, GaugeIcon, RadarIcon, LightningIcon, ArrowUpRightIcon } from '@/components/icons';
import Link from 'next/link';

export default function UsagePage() {
  const historyQuery = useQuery({
    queryKey: ['usage', 'history', { months: 12 }],
    queryFn: async () => {
      const response = await api.get('/usage/history?months=12');
      return response.data.data;
    },
  });

  const currentQuery = useQuery({
    queryKey: ['usage', 'current'],
    queryFn: async () => {
      const response = await api.get('/usage/current');
      return response.data.data;
    },
  });

  const statsQuery = useQuery({
    queryKey: ['usage', 'stats'],
    queryFn: async () => {
      const response = await api.get('/usage/stats');
      return response.data.data;
    },
  });

  const usageRows = historyQuery.data?.usage ?? [];
  const totalRequests = usageRows.reduce((sum: number, row: any) => sum + (row.requestsCount ?? 0), 0);

  const statCards = useMemo(() => {
    const stats = statsQuery.data;
    return [
      {
        label: 'Total analyses',
        value: formatNumber(stats?.totalAnalyses),
        helper: `${formatNumber(stats?.completedAnalyses)} completed missions`,
        icon: <ActivityIcon className="h-5 w-5" />,
        href: '/analysis',
      },
      {
        label: 'API requests',
        value: formatNumber(totalRequests),
        helper: 'Last 12 months',
        icon: <RadarIcon className="h-5 w-5" />,
      },
      {
        label: 'Success rate',
        value: stats?.successRate ? `${stats.successRate}%` : '—',
        helper: `${stats?.failedAnalyses ?? 0} failed`,
        icon: <GaugeIcon className="h-5 w-5" />,
        tone: 'success' as const,
      },
      {
        label: 'Reports emitted',
        value: formatNumber(stats?.totalReports),
        helper: `${formatNumber(stats?.accountsAnalyzed)} accounts`,
        icon: <LightningIcon className="h-5 w-5" />,
        href: '/reports',
      },
    ];
  }, [statsQuery.data, totalRequests]);

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {statCards.map((card) => (
          <StatCard key={card.label} {...card} />
        ))}
      </div>

      <UsageOverview usage={usageRows} monthlyLimit={currentQuery.data?.analyses?.limit} />

      <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Quota intel</p>
            <h2 className="text-2xl font-semibold text-slate-900">Current tier ({currentQuery.data?.tier?.name ?? 'STARTER'})</h2>
            <p className="text-sm text-slate-500">
              {currentQuery.data?.analyses?.used ?? 0} of {currentQuery.data?.analyses?.limit ?? '—'} analyses used ·
              {currentQuery.data?.tier?.requestsPerHour ?? '—'} req/hr
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-xs text-slate-600">
              {currentQuery.data?.tier?.agentCount ?? 0} active agents
            </div>
            <Link
              href="/billing"
              className="flex items-center gap-2 rounded-full bg-primary-600 px-4 py-2 text-xs text-white hover:bg-primary-700"
            >
              Upgrade plan
              <ArrowUpRightIcon className="h-3 w-3" />
            </Link>
          </div>
        </div>

        <div className="mt-6 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-xs uppercase tracking-[0.3em] text-slate-500">
              <tr>
                <th className="pb-3">Month</th>
                <th className="pb-3">Analyses</th>
                <th className="pb-3">API requests</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {usageRows.map((row: any) => (
                <tr key={row.monthYear} className="text-slate-900">
                  <td className="py-3">
                    {new Date(`${row.monthYear}-01`).toLocaleString('en-US', { month: 'long', year: 'numeric' })}
                  </td>
                  <td className="py-3 text-slate-600">{row.analysesUsed}</td>
                  <td className="py-3 text-slate-600">{row.requestsCount}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
