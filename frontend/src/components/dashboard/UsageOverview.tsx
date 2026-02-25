'use client';

import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { useTranslation } from '@/i18n/TranslationProvider';

interface UsagePoint {
  monthYear: string;
  analysesUsed: number;
  requestsCount: number;
}

interface UsageOverviewProps {
  usage: UsagePoint[];
  monthlyLimit?: number;
}

export function UsageOverview({ usage, monthlyLimit }: UsageOverviewProps) {
  const { t, locale } = useTranslation();
  
  const formatMonth = (input: string) => {
    const [year, month] = input.split('-');
    const date = new Date(Number(year), Number(month) - 1);
    return date.toLocaleDateString(locale === 'tr' ? 'tr-TR' : 'en-US', { month: 'short' });
  };

  const chartData = usage.map((point) => ({
    month: formatMonth(point.monthYear),
    analyses: point.analysesUsed,
    requests: point.requestsCount,
  }));

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500">
            {locale === 'tr' ? 'Kullanım nabzı' : 'Usage pulse'}
          </p>
          <h3 className="text-2xl font-semibold text-slate-900">
            {locale === 'tr' ? 'Analiz hızı' : 'Analysis velocity'}
          </h3>
        </div>
        {monthlyLimit !== undefined && monthlyLimit > 0 && (
          <div className="rounded-full border border-slate-200 bg-slate-50 px-4 py-1 text-xs text-slate-600">
            {locale === 'tr' ? 'Aylık kota' : 'Monthly quota'} · {monthlyLimit}
          </div>
        )}
      </div>
      <div className="mt-6 h-60">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ left: 0, right: 0 }}>
            <defs>
              <linearGradient id="colorAnalyses" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#FF4D00" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#FF4D00" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="month" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} allowDecimals={false} />
            <Tooltip
              contentStyle={{ background: '#ffffff', borderRadius: 16, border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
              labelStyle={{ color: '#0f172a' }}
              formatter={(value: number) => [`${value} ${locale === 'tr' ? 'analiz' : 'analyses'}`, locale === 'tr' ? 'Hacim' : 'Volume']}
            />
            <Area
              type="monotone"
              dataKey="analyses"
              stroke="#FF4D00"
              fillOpacity={1}
              fill="url(#colorAnalyses)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
