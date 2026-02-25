"use client";

import { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon, AlertOctagonIcon, CheckCircle2Icon, TargetIcon, CalendarIcon, LightningIcon, TrendingDownIcon, TrendingUpIcon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

interface FinalVerdictData {
  agent?: string;
  error?: boolean;
  finalVerdict?: {
    situation?: string;
    critical_issues?: string[];
    this_week_actions?: string[];
    warning?: string;
  };
  timestamp?: string;
}

interface Props {
  data: FinalVerdictData;
}

export function FinalVerdict({ data }: Props) {
  const [expanded, setExpanded] = useState(true);
  const { locale } = useTranslation();
  
  if (!data || !data.finalVerdict || Object.keys(data.finalVerdict).length === 0) {
    return null;
  }

  const { finalVerdict } = data;
  const { situation, critical_issues, this_week_actions, warning } = finalVerdict;

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between bg-gradient-to-r from-indigo-50 to-violet-50 p-6"
      >
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-100">
            <AlertOctagonIcon className="text-indigo-600" size={20} />
          </div>
          <div className="text-left">
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">
              {locale === 'tr' ? 'Final Analiz' : 'Final Analysis'}
            </p>
            <p className="text-lg font-semibold text-slate-900">
              {locale === 'tr' ? 'Kapsamlı Son Değerlendirme' : 'Comprehensive Final Verdict'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-lg bg-indigo-100 px-3 py-1 text-xs font-medium text-indigo-700">
            AI Analysis
          </span>
          {expanded ? (
            <ChevronUpIcon className="text-slate-400" size={20} />
          ) : (
            <ChevronDownIcon className="text-slate-400" size={20} />
          )}
        </div>
      </button>

      {expanded && (
        <div className="p-6 space-y-6">
          {/* Situation Overview */}
          {situation && (
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-3">
                <TargetIcon className="text-slate-500" size={16} />
                {locale === 'tr' ? 'Mevcut Durum' : 'Current Situation'}
              </h4>
              <p className="text-sm text-slate-700 leading-relaxed">{situation}</p>
            </div>
          )}

          {/* Critical Issues */}
          {critical_issues && critical_issues.length > 0 && (
            <div>
              <h4 className="flex items-center gap-2 text-sm font-semibold text-red-700 mb-3">
                <TrendingDownIcon size={16} />
                {locale === 'tr' ? 'Kritik Sorunlar' : 'Critical Issues'}
              </h4>
              <div className="space-y-2">
                {critical_issues.map((issue, idx) => (
                  <div key={idx} className="flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-3">
                    <AlertOctagonIcon className="text-red-500 flex-shrink-0 mt-0.5" size={16} />
                    <p className="text-sm text-red-800">{issue}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* This Week Actions */}
          {this_week_actions && this_week_actions.length > 0 && (
            <div>
              <h4 className="flex items-center gap-2 text-sm font-semibold text-green-700 mb-3">
                <CalendarIcon size={16} />
                {locale === 'tr' ? 'Bu Hafta Yapılması Gerekenler' : 'This Week\'s Actions'}
              </h4>
              <div className="space-y-2">
                {this_week_actions.map((action, idx) => (
                  <div key={idx} className="flex items-start gap-3 rounded-xl border border-green-200 bg-green-50 p-3">
                    <div className="flex h-5 w-5 items-center justify-center rounded-full bg-green-200 text-xs font-bold text-green-700 flex-shrink-0">
                      {idx + 1}
                    </div>
                    <p className="text-sm text-green-800">{action}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Warning */}
          {warning && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
              <h4 className="flex items-center gap-2 text-sm font-semibold text-amber-700 mb-2">
                <LightningIcon size={16} />
                {locale === 'tr' ? 'Uyarı' : 'Warning'}
              </h4>
              <p className="text-sm text-amber-800">{warning}</p>
            </div>
          )}

          {/* Timestamp */}
          {data.timestamp && (
            <p className="text-xs text-slate-400 text-right">
              {locale === 'tr' ? 'Analiz zamanı' : 'Analysis time'}: {new Date(data.timestamp).toLocaleString(locale)}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default FinalVerdict;
