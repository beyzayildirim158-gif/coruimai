"use client";

import { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon, AlertTriangleIcon, CheckCircleIcon, InfoIcon, StarIcon, TargetIcon, TrendingUpIcon, CommentIcon, LightbulbIcon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

/**
 * CRITICAL: React Error #31 Fix
 * Bu fonksiyon objeleri güvenli bir şekilde string'e çevirir.
 */
function safeRenderValue(value: any): string {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  if (Array.isArray(value)) {
    return value.map(v => safeRenderValue(v)).filter(Boolean).join(', ');
  }
  if (typeof value === 'object') {
    const entries = Object.entries(value);
    if (entries.length === 0) return '';
    return entries
      .map(([k, v]) => `${k}: ${typeof v === 'object' ? JSON.stringify(v) : v}`)
      .join(' | ');
  }
  return String(value);
}

interface ELI5Finding {
  category: string;
  kusur?: string;
  realite?: string;
  neden_onemli?: string;
}

interface SimplifiedMetric {
  name: string;
  value: string;
  explanation: string;
  verdict: string;
}

interface RewrittenHook {
  original: string;
  rewritten: string;
  reason: string;
}

interface ELI5ReportData {
  executiveSummary?: {
    headline?: string;
    grade?: string;
    gradeExplanation?: string;
    overallVerdict?: string;
  };
  findings?: ELI5Finding[];
  simplifiedMetrics?: SimplifiedMetric[];
  rewrittenHooks?: RewrittenHook[];
  whatHappensIfNothing?: string;
  motivationalKick?: string;
}

interface Props {
  data: ELI5ReportData;
}

function getGradeColor(grade: string | undefined): string {
  if (!grade) return 'text-slate-500';
  switch (grade.toUpperCase()) {
    case 'A': return 'text-green-600';
    case 'B': return 'text-blue-600';
    case 'C': return 'text-yellow-600';
    case 'D': return 'text-orange-600';
    case 'F': return 'text-red-600';
    default: return 'text-slate-500';
  }
}

function getGradeBgColor(grade: string | undefined): string {
  if (!grade) return 'bg-slate-100';
  switch (grade.toUpperCase()) {
    case 'A': return 'bg-green-100 border-green-200';
    case 'B': return 'bg-blue-100 border-blue-200';
    case 'C': return 'bg-yellow-100 border-yellow-200';
    case 'D': return 'bg-orange-100 border-orange-200';
    case 'F': return 'bg-red-100 border-red-200';
    default: return 'bg-slate-100 border-slate-200';
  }
}

function getVerdictColor(verdict: string | undefined): string {
  if (!verdict) return 'text-slate-500';
  const v = verdict.toLowerCase();
  if (v.includes('iyi') || v.includes('good') || v.includes('olumlu')) return 'text-green-600';
  if (v.includes('kötü') || v.includes('bad') || v.includes('kritik') || v.includes('critical')) return 'text-red-600';
  return 'text-amber-600';
}

export function ELI5Report({ data }: Props) {
  const [expanded, setExpanded] = useState(true);
  const { locale } = useTranslation();
  
  if (!data || Object.keys(data).length === 0) {
    return null;
  }

  const { executiveSummary, findings, simplifiedMetrics, rewrittenHooks, whatHappensIfNothing, motivationalKick } = data;

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between bg-gradient-to-r from-purple-50 to-pink-50 p-6"
      >
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100">
            <CommentIcon size={20} className="text-purple-600" />
          </div>
          <div className="text-left">
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">
              {locale === 'tr' ? 'Detaylı Analiz' : 'Detailed Analysis'}
            </p>
            <p className="text-lg font-semibold text-slate-900">
              {locale === 'tr' ? 'Anlaşılır Açıklamalar' : 'Clear Explanations'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {executiveSummary?.grade && (
            <span className={`rounded-lg px-3 py-1 text-xl font-bold ${getGradeColor(executiveSummary.grade)} ${getGradeBgColor(executiveSummary.grade)}`}>
              {executiveSummary.grade}
            </span>
          )}
          {expanded ? (
            <ChevronUpIcon size={20} className="text-slate-400" />
          ) : (
            <ChevronDownIcon size={20} className="text-slate-400" />
          )}
        </div>
      </button>

      {expanded && (
        <div className="p-6 space-y-6">
          {/* Executive Summary */}
          {executiveSummary && (
            <div className={`rounded-2xl border p-4 ${getGradeBgColor(executiveSummary.grade)}`}>
              {executiveSummary.headline && (
                <h3 className="text-lg font-bold text-slate-900 mb-2">
                  {executiveSummary.headline}
                </h3>
              )}
              {executiveSummary.gradeExplanation && (
                <p className="text-sm text-slate-700 mb-2">
                  {executiveSummary.gradeExplanation}
                </p>
              )}
              {executiveSummary.overallVerdict && (
                <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${getVerdictColor(executiveSummary.overallVerdict)} bg-white/80`}>
                  {executiveSummary.overallVerdict}
                </span>
              )}
            </div>
          )}

          {/* Findings */}
          {findings && findings.length > 0 && (
            <div>
              <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-3">
                <AlertTriangleIcon size={16} className="text-amber-500" />
                {locale === 'tr' ? 'Temel Bulgular' : 'Key Findings'}
              </h4>
              <div className="space-y-3">
                {findings.map((finding, idx) => (
                  <div key={idx} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 mt-0.5">
                        {finding.kusur ? (
                          <AlertTriangleIcon size={16} className="text-red-500" />
                        ) : (
                          <InfoIcon size={16} className="text-blue-500" />
                        )}
                      </div>
                      <div>
                        <p className="text-xs uppercase tracking-wider text-slate-500 mb-1">{typeof finding.category === 'string' ? finding.category : safeRenderValue(finding.category)}</p>
                        {finding.kusur && (
                          <p className="text-sm font-medium text-red-700 mb-1">{typeof finding.kusur === 'string' ? finding.kusur : safeRenderValue(finding.kusur)}</p>
                        )}
                        {finding.realite && (
                          <p className="text-sm text-slate-700 mb-1">{typeof finding.realite === 'string' ? finding.realite : safeRenderValue(finding.realite)}</p>
                        )}
                        {finding.neden_onemli && (
                          <p className="text-xs text-slate-500 italic">{typeof finding.neden_onemli === 'string' ? finding.neden_onemli : safeRenderValue(finding.neden_onemli)}</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Simplified Metrics */}
          {simplifiedMetrics && simplifiedMetrics.length > 0 && (
            <div>
              <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-3">
                <TargetIcon size={16} className="text-primary-500" />
                {locale === 'tr' ? 'Metrik Yorumları' : 'Metric Interpretations'}
              </h4>
              <div className="grid gap-3 md:grid-cols-2">
                {simplifiedMetrics.map((metric, idx) => (
                  <div key={idx} className="rounded-xl border border-slate-200 bg-white p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-slate-900">{metric.name}</span>
                      <span className={`text-sm font-bold ${getVerdictColor(metric.verdict)}`}>{metric.value}</span>
                    </div>
                    <p className="text-xs text-slate-600">{metric.explanation}</p>
                    <span className={`mt-2 inline-flex items-center rounded-full px-2 py-0.5 text-xs ${getVerdictColor(metric.verdict)} bg-slate-100`}>
                      {metric.verdict}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Rewritten Hooks */}
          {rewrittenHooks && rewrittenHooks.length > 0 && (
            <div>
              <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-3">
                <LightbulbIcon size={16} className="text-yellow-500" />
                {locale === 'tr' ? 'İyileştirilmiş Hook\'lar' : 'Improved Hooks'}
              </h4>
              <div className="space-y-3">
                {rewrittenHooks.map((hook, idx) => (
                  <div key={idx} className="rounded-xl border border-slate-200 bg-gradient-to-r from-green-50 to-emerald-50 p-4">
                    <div className="mb-2">
                      <p className="text-xs uppercase tracking-wider text-slate-500 mb-1">{locale === 'tr' ? 'Orijinal' : 'Original'}</p>
                      <p className="text-sm text-slate-600 line-through">{hook.original}</p>
                    </div>
                    <div className="mb-2">
                      <p className="text-xs uppercase tracking-wider text-green-600 mb-1">{locale === 'tr' ? 'İyileştirilmiş' : 'Improved'}</p>
                      <p className="text-sm font-medium text-slate-900">{hook.rewritten}</p>
                    </div>
                    <p className="text-xs text-slate-500 italic">{hook.reason}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* What Happens If Nothing */}
          {whatHappensIfNothing && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4">
              <h4 className="flex items-center gap-2 text-sm font-semibold text-red-700 mb-2">
                <AlertTriangleIcon size={16} />
                {locale === 'tr' ? 'Hiçbir Şey Yapmazsan Ne Olur?' : 'What Happens If You Do Nothing?'}
              </h4>
              <p className="text-sm text-red-700">{whatHappensIfNothing}</p>
            </div>
          )}

          {/* Motivational Kick */}
          {motivationalKick && (
            <div className="rounded-xl border border-green-200 bg-gradient-to-r from-green-50 to-emerald-50 p-4">
              <h4 className="flex items-center gap-2 text-sm font-semibold text-green-700 mb-2">
                <StarIcon size={16} />
                {locale === 'tr' ? 'Motivasyon' : 'Motivation'}
              </h4>
              <p className="text-sm text-green-800 font-medium">{motivationalKick}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ELI5Report;
