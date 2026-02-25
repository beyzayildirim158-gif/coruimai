"use client";

import { useMemo, useState } from 'react';
import { useQuery, keepPreviousData } from '@tanstack/react-query';
import api from '@/lib/api';
import { ReportTable } from '@/components/reports/ReportTable';
import { LoaderIcon, FilterIcon, DownloadCloudIcon } from '@/components/icons';
import clsx from 'clsx';

const reportFilters = ['ALL', 'FULL', 'SUMMARY', 'EXECUTIVE'] as const;

type ReportFilter = (typeof reportFilters)[number];

export default function ReportsPage() {
  const [page, setPage] = useState(1);
  const [filter, setFilter] = useState<ReportFilter>('ALL');
  const limit = 10;

  const reportsQuery = useQuery({
    queryKey: ['reports', page, filter],
    queryFn: async () => {
      const response = await api.get('/reports', {
        params: { page, limit },
      });
      return response.data.data;
    },
    placeholderData: keepPreviousData,
  });

  const filteredReports = useMemo(() => {
    if (!reportsQuery.data?.reports) return [];
    if (filter === 'ALL') return reportsQuery.data.reports;
    return reportsQuery.data.reports.filter((report: any) => report.reportType === filter);
  }, [filter, reportsQuery.data]);

  const totalPages = reportsQuery.data?.pagination?.totalPages ?? 1;

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Mission exports</p>
            <h1 className="text-3xl font-semibold text-slate-900">PDF intelligence reports</h1>
            <p className="text-sm text-slate-500">Every report is white-glove formatted for stakeholders, investors, or clients.</p>
          </div>
          <button
            onClick={() => window.open('/analysis', '_self')}
            className="flex items-center gap-2 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-2 text-sm text-primary-600 hover:bg-slate-100"
          >
            <DownloadCloudIcon size={16} />
            Generate from analysis
          </button>
        </div>
        <div className="mt-4 flex flex-wrap gap-2 text-xs text-slate-700">
          {reportFilters.map((option) => (
            <button
              key={option}
              onClick={() => setFilter(option)}
              className={clsx(
                'inline-flex items-center gap-1 rounded-full border px-3 py-1',
                filter === option ? 'border-primary-300 bg-primary-50 text-primary-700' : 'border-slate-200 text-slate-600 hover:bg-slate-50'
              )}
            >
              {option === 'ALL' && <FilterIcon size={12} />}
              {option}
            </button>
          ))}
        </div>
      </div>

      <ReportTable
        reports={filteredReports}
        isLoading={reportsQuery.isLoading}
        emptyCta={
          <button
            onClick={() => (window.location.href = '/analysis')}
            className="mt-4 inline-flex items-center justify-center rounded-full bg-primary-600 px-6 py-2 text-xs text-white hover:bg-primary-700"
          >
            Launch an analysis
          </button>
        }
      />

      <div className="flex items-center justify-between text-sm text-slate-500">
        <div>
          Page {page} of {totalPages}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage((prev) => Math.max(1, prev - 1))}
            disabled={page === 1 || reportsQuery.isFetching}
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 px-4 py-2 text-slate-700 hover:bg-slate-50 disabled:opacity-40"
          >
            {reportsQuery.isFetching && <LoaderIcon size={16} />}
            Previous
          </button>
          <button
            onClick={() => setPage((prev) => Math.min(totalPages, prev + 1))}
            disabled={page === totalPages || reportsQuery.isFetching}
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 px-4 py-2 text-slate-700 hover:bg-slate-50 disabled:opacity-40"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
