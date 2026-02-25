'use client';

import Link from 'next/link';
import { LoaderIcon, DownloadIcon, ExternalLinkIcon, FileTextIcon } from '@/components/icons';
import { formatDateTime } from '@/lib/formatters';
import { useTranslation } from '@/i18n/TranslationProvider';

interface ReportTableProps {
  reports?: Array<{
    id: string;
    reportType: string;
    pdfUrl?: string | null;
    generatedAt?: string | null;
    analysis?: {
      id: string;
      account?: {
        username: string;
        profilePicUrl?: string | null;
      };
    };
  }>;
  isLoading?: boolean;
  emptyCta?: React.ReactNode;
}

export function ReportTable({ reports = [], isLoading, emptyCta }: ReportTableProps) {
  const { t, locale } = useTranslation();

  const reportTypeCopy: Record<string, string> = {
    FULL: locale === 'tr' ? 'Tam dosya' : 'Full dossier',
    SUMMARY: locale === 'tr' ? 'Yönetici özeti' : 'Executive summary',
    EXECUTIVE: locale === 'tr' ? 'Yatırımcıya hazır' : 'Investor ready',
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center rounded-3xl border border-slate-200 bg-white p-10 text-slate-500 shadow-sm">
        <LoaderIcon className="mr-2 h-5 w-5 animate-spin" /> {locale === 'tr' ? 'Raporlar alınıyor...' : 'Fetching reports...'}
      </div>
    );
  }

  if (!reports.length) {
    return (
      <div className="rounded-3xl border border-dashed border-slate-200 bg-slate-50 p-10 text-center text-slate-500">
        <FileTextIcon className="mx-auto mb-3 h-8 w-8 text-primary-500" />
        <p>{locale === 'tr' ? 'Henüz PDF raporu yok.' : 'No PDF reports yet.'}</p>
        {emptyCta}
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
      <div className="grid grid-cols-[2fr_1fr_1fr_80px] gap-4 bg-slate-50 px-6 py-3 text-xs uppercase tracking-[0.2em] text-slate-500 max-sm:hidden">
        <span>{locale === 'tr' ? 'Hesap' : 'Account'}</span>
        <span>{locale === 'tr' ? 'Rapor' : 'Report'}</span>
        <span>{locale === 'tr' ? 'Oluşturuldu' : 'Generated'}</span>
        <span className="text-right">{locale === 'tr' ? 'İşlem' : 'Action'}</span>
      </div>
      <div className="divide-y divide-slate-100">
        {reports.map((report) => (
          <div key={report.id} className="grid grid-cols-1 gap-4 px-6 py-4 text-sm text-slate-900 sm:grid-cols-[2fr_1fr_1fr_80px]">
            <div>
              <p className="text-sm font-semibold text-slate-900">@{report.analysis?.account?.username ?? (locale === 'tr' ? 'bilinmiyor' : 'unknown')}</p>
              <p className="text-xs text-slate-500">#{report.analysis?.id ?? 'n/a'}</p>
            </div>
            <div>
              <p className="font-semibold text-primary-600">{reportTypeCopy[report.reportType] ?? report.reportType}</p>
              <p className="text-xs text-slate-500">ID: {report.id.slice(0, 8)}...</p>
            </div>
            <div className="text-slate-500">{formatDateTime(report.generatedAt)}</div>
            <div className="flex items-center justify-end gap-2 text-primary-600">
              {report.pdfUrl ? (
                <Link
                  href={report.pdfUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 rounded-2xl border border-slate-200 px-3 py-1 text-xs hover:bg-slate-50"
                >
                  <DownloadIcon className="h-4 w-4" />
                  PDF
                </Link>
              ) : (
                <span className="rounded-2xl border border-dashed border-slate-200 px-3 py-1 text-xs text-slate-400">
                  {locale === 'tr' ? 'İşleniyor' : 'Processing'}
                </span>
              )}
              {report.analysis?.id && (
                <Link
                  href={`/analysis/${report.analysis.id}`}
                  className="inline-flex items-center gap-1 rounded-2xl border border-slate-200 px-3 py-1 text-xs hover:bg-slate-50"
                >
                  {locale === 'tr' ? 'Görüntüle' : 'View'}
                  <ExternalLinkIcon className="h-3.5 w-3.5" />
                </Link>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
