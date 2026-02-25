'use client';

import { useState } from 'react';
import { AlertTriangleIcon, CheckCircleIcon, InfoIcon, ShieldCheckIcon } from '@/components/icons';

interface MissingDetail {
  field: string;
  label: string;
  reason: string;
  impact: string;
  severity: 'high' | 'medium' | 'low';
}

interface DataQualityReport {
  missing_fields: string[];
  missing_details?: MissingDetail[];
  confidence_score: number;
  total_missing: number;
  has_critical_gaps: boolean;
  summary: string;
}

interface DataQualityBadgeProps {
  report?: DataQualityReport | null;
  locale?: 'tr' | 'en';
}

const SEVERITY_STYLES: Record<string, string> = {
  high:   'border-rose-200 bg-rose-50 text-rose-700',
  medium: 'border-amber-200 bg-amber-50 text-amber-700',
  low:    'border-slate-200 bg-slate-50 text-slate-600',
};

const SEVERITY_LABEL: Record<string, string> = {
  high:   'Kritik',
  medium: 'Orta',
  low:    'Düşük',
};

export function DataQualityBadge({ report, locale = 'tr' }: DataQualityBadgeProps) {
  const [expanded, setExpanded] = useState(false);

  if (!report) return null;

  const { missing_details = [], confidence_score, has_critical_gaps, summary, total_missing } = report;
  const isTr = locale === 'tr';

  // All data collected — show green pill
  if (total_missing === 0) {
    return (
      <div className="flex items-center gap-2 rounded-2xl bg-emerald-50 border border-emerald-200 px-4 py-2 text-sm text-emerald-700">
        <ShieldCheckIcon size={16} />
        <span>{isTr ? 'Tüm veriler eksiksiz toplandı' : 'All data collected successfully'}</span>
        <span className="ml-auto rounded-full bg-emerald-200 px-2 py-0.5 text-xs font-semibold">
          %{confidence_score}
        </span>
      </div>
    );
  }

  const borderColor = has_critical_gaps ? 'border-rose-200' : 'border-amber-200';
  const bgColor     = has_critical_gaps ? 'bg-rose-50'     : 'bg-amber-50';
  const textColor   = has_critical_gaps ? 'text-rose-800'  : 'text-amber-800';
  const badgeBg     = has_critical_gaps ? 'bg-rose-200'    : 'bg-amber-200';

  return (
    <div className={`rounded-3xl border ${borderColor} ${bgColor} p-4`}>
      {/* Header row */}
      <div className="flex items-center gap-2">
        <AlertTriangleIcon size={16} className={textColor} />
        <span className={`text-sm font-semibold ${textColor}`}>
          {isTr
            ? `Veri Kalitesi — ${total_missing} alan toplanamadı`
            : `Data Quality — ${total_missing} field(s) unavailable`}
        </span>
        <span className={`ml-auto rounded-full ${badgeBg} px-2 py-0.5 text-xs font-semibold ${textColor}`}>
          {isTr ? 'Güven' : 'Confidence'}: %{confidence_score}
        </span>
        <button
          onClick={() => setExpanded((v) => !v)}
          className={`rounded-full border ${borderColor} bg-white px-3 py-0.5 text-xs ${textColor} hover:bg-white/80 transition-colors`}
        >
          {expanded
            ? (isTr ? 'Gizle' : 'Hide')
            : (isTr ? 'Detaylar' : 'Details')}
        </button>
      </div>

      {/* Summary pill row */}
      {!expanded && (
        <div className="mt-3 flex flex-wrap gap-2">
          {missing_details.map((item) => (
            <span
              key={item.field}
              className={`inline-flex items-center gap-1 rounded-full border px-3 py-1 text-xs ${SEVERITY_STYLES[item.severity]}`}
            >
              <InfoIcon size={10} />
              {item.label}
            </span>
          ))}
        </div>
      )}

      {/* Expanded detail cards */}
      {expanded && (
        <div className="mt-3 space-y-2">
          {missing_details.map((item) => (
            <div
              key={item.field}
              className={`rounded-2xl border p-3 ${SEVERITY_STYLES[item.severity]}`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold">{item.label}</span>
                <span className={`rounded-full border px-2 py-0.5 text-xs ${SEVERITY_STYLES[item.severity]}`}>
                  {SEVERITY_LABEL[item.severity]}
                </span>
              </div>
              <p className="mt-1 text-xs opacity-80">
                <strong>{isTr ? 'Neden:' : 'Reason:'}</strong> {item.reason}
              </p>
              <p className="mt-0.5 text-xs opacity-80">
                <strong>{isTr ? 'Etki:' : 'Impact:'}</strong> {item.impact}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Footer note */}
      <p className={`mt-3 text-xs opacity-70 ${textColor}`}>
        {isTr
          ? 'Bu alanlar Instagram API kısıtlamaları nedeniyle toplanamadı. Analiz yalnızca mevcut verilerle oluşturuldu.'
          : 'These fields could not be collected due to Instagram API limitations. Analysis was built from available data only.'}
      </p>
    </div>
  );
}
