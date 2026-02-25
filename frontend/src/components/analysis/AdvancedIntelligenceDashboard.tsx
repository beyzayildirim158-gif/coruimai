"use client";

import React from 'react';
import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  Legend,
  LineChart,
  Line,
} from 'recharts';
import { BarChart3Icon, TrendingUpIcon, TrendingDownIcon, ShieldIcon } from '@/components/icons';
import { sanitizeDisplayText } from '@/lib/textSanitizer';

type ConfidenceState = 'high' | 'partial' | 'low';

interface AdvancedIntelligenceDashboardProps {
  systemGovernor?: any;
  locale?: 'tr' | 'en';
}

const EMPTY_TR = 'Bu veri seti için yeterli sinyal toplanamadı.';
const EMPTY_MIN_TR = 'Veri yetersiz.';

function EmptyStateCard({ message = EMPTY_TR }: { message?: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center text-slate-600">
      <p className="text-sm">{message}</p>
    </div>
  );
}

function hasSuppressedText(value: any): boolean {
  const banned = [
    'json parsing failed',
    'manual review required',
    'mismatch detected',
    'integrity_conflict',
    'integrity conflict',
  ];

  const scan = (v: any): boolean => {
    if (v == null) return false;
    if (typeof v === 'string') {
      const low = v.toLowerCase();
      return banned.some((b) => low.includes(b));
    }
    if (Array.isArray(v)) return v.some(scan);
    if (typeof v === 'object') return Object.values(v).some(scan);
    return false;
  };

  return scan(value);
}

function getConfidence(systemGovernor: any): number {
  const fromConfidenceMetrics = Number(systemGovernor?.confidence_metrics?.overall_confidence ?? NaN);
  if (!Number.isNaN(fromConfidenceMetrics)) {
    return fromConfidenceMetrics <= 1 ? Math.round(fromConfidenceMetrics * 100) : Math.round(fromConfidenceMetrics);
  }

  const fromValidationSummary = Number(systemGovernor?.validation_summary?.analysis_confidence ?? NaN);
  if (!Number.isNaN(fromValidationSummary)) {
    return fromValidationSummary <= 1 ? Math.round(fromValidationSummary * 100) : Math.round(fromValidationSummary);
  }

  const fromQa = Number(systemGovernor?.quality_assurance?.qa_score ?? NaN);
  if (!Number.isNaN(fromQa)) return Math.round(fromQa);

  return 50;
}

function getConfidenceState(score: number): ConfidenceState {
  if (score > 80) return 'high';
  if (score >= 50) return 'partial';
  return 'low';
}

function getBadge(confidence: number, locale: 'tr' | 'en') {
  const state = getConfidenceState(confidence);
  if (state === 'high') {
    return {
      state,
      text: locale === 'tr' ? 'Verified' : 'Verified',
      classes: 'bg-emerald-100 text-emerald-700 border-emerald-300',
    };
  }
  if (state === 'partial') {
    return {
      state,
      text: locale === 'tr' ? 'Estimated' : 'Estimated',
      classes: 'bg-amber-100 text-amber-700 border-amber-300',
    };
  }
  return {
    state,
    text: locale === 'tr' ? 'Needs More Data' : 'Needs More Data',
    classes: 'bg-rose-100 text-rose-700 border-rose-300',
  };
}

const dayOrder = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'];

export function AdvancedIntelligenceDashboard({ systemGovernor, locale = 'tr' }: AdvancedIntelligenceDashboardProps) {
  const advanced = systemGovernor?.advancedAnalytics;

  if (!advanced || hasSuppressedText(advanced)) {
    return null;
  }

  const confidence = getConfidence(systemGovernor);
  const badge = getBadge(confidence, locale);

  const polarity = advanced?.performance_polarity;
  const chronobio = advanced?.audience_chronobiology;
  const sentiment = advanced?.sentiment_cloud_engine;
  const benchmark = advanced?.competitive_benchmark;

  const canRenderPolarity = polarity?.status === 'OK' && Array.isArray(polarity?.top_posts) && Array.isArray(polarity?.bottom_posts);
  const canRenderChronobio = chronobio?.status === 'OK' && chronobio?.golden_window;
  const canRenderSentiment = sentiment?.status === 'OK';
  const canRenderBenchmark = benchmark?.status === 'OK';

  const trendData = canRenderPolarity
    ? [
        { name: 'Worst', value: Number((polarity.bottom_posts || []).reduce((s: number, p: any) => s + Number(p.engagement_rate || 0), 0) / Math.max(1, (polarity.bottom_posts || []).length)) },
        { name: 'Best', value: Number((polarity.top_posts || []).reduce((s: number, p: any) => s + Number(p.engagement_rate || 0), 0) / Math.max(1, (polarity.top_posts || []).length)) },
      ]
    : [];

  // EMPTY_SECTION_HANDLER: if ALL panels are empty, silently hide the entire section
  const anyPanelRenderable = canRenderPolarity || canRenderChronobio || canRenderSentiment || canRenderBenchmark || trendData.length > 0;
  if (!anyPanelRenderable) return null;

  const heatmapData = canRenderChronobio
    ? [{
        x: Number(chronobio.golden_window.hour ?? 0),
        y: dayOrder.indexOf(String(chronobio.golden_window.day || 'Pazartesi')),
        z: Number(chronobio.golden_window.avg_er ?? 0),
      }]
    : [];

  const benchmarkData = canRenderBenchmark
    ? [
        {
          metric: locale === 'tr' ? 'Büyüme' : 'Growth',
          user: Number(benchmark.growth_rate?.user ?? 0),
          competitor: Number(benchmark.growth_rate?.competitor ?? 0),
        },
        {
          metric: locale === 'tr' ? 'Etkileşim' : 'Engagement',
          user: Number(benchmark.engagement_rate?.user ?? 0),
          competitor: Number(benchmark.engagement_rate?.competitor ?? 0),
        },
        {
          metric: locale === 'tr' ? 'Sıklık' : 'Frequency',
          user: Number(benchmark.posting_frequency?.user ?? 0),
          competitor: Number(benchmark.posting_frequency?.competitor ?? 0),
        },
      ]
    : [];

  const trendUp = trendData.length === 2 && trendData[1].value >= trendData[0].value;

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <BarChart3Icon size={20} className="text-indigo-600" />
          <h3 className="text-xl font-semibold text-slate-900">{locale === 'tr' ? 'Advanced Intelligence' : 'Advanced Intelligence'}</h3>
        </div>
        <div className="flex items-center gap-2">
          <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${badge.classes}`}>{badge.text}</span>
          <span className="text-xs text-slate-500">{confidence}%</span>
        </div>
      </div>

      {badge.state === 'low' && (
        <div className="mb-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {locale === 'tr' ? 'Needs More Data: Bazı metrikler düşük güven seviyesinde; export katmanı kısıtlı çalışabilir.' : 'Needs More Data: Some metrics are low-confidence; export layer may be restricted.'}
        </div>
      )}

      <div className={badge.state === 'low' ? 'pointer-events-none opacity-60 blur-[1px]' : ''}>
        <div className="grid gap-4 lg:grid-cols-2">
          {canRenderPolarity && (
          <div className="rounded-2xl border border-slate-200 p-4">
            <h4 className="mb-3 text-sm font-semibold text-slate-700">PERFORMANCE POLARITY</h4>
              <div className="grid gap-3 md:grid-cols-2">
                <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3">
                  <p className="mb-2 text-xs font-semibold text-emerald-700">{locale === 'tr' ? 'Top 3 (Best)' : 'Top 3 (Best)'}</p>
                  {(polarity.top_posts || []).slice(0, 3).map((p: any) => (
                    <div key={String(p.post_id)} className="mb-1 text-xs text-slate-700">
                      #{p.post_id} • ER {Number(p.engagement_rate || 0).toFixed(2)}%
                    </div>
                  ))}
                </div>
                <div className="rounded-xl border border-rose-200 bg-rose-50 p-3">
                  <p className="mb-2 text-xs font-semibold text-rose-700">{locale === 'tr' ? 'Bottom 3 (Worst)' : 'Bottom 3 (Worst)'}</p>
                  {(polarity.bottom_posts || []).slice(0, 3).map((p: any) => (
                    <div key={String(p.post_id)} className="mb-1 text-xs text-slate-700">
                      #{p.post_id} • ER {Number(p.engagement_rate || 0).toFixed(2)}%
                    </div>
                  ))}
                </div>
              </div>
          </div>
          )}

          {canRenderChronobio && (
          <div className="rounded-2xl border border-slate-200 p-4">
            <h4 className="mb-3 text-sm font-semibold text-slate-700">AUDIENCE CHRONOBIOLOGY</h4>
              <>
                <p className="mb-2 text-xs text-slate-600">{sanitizeDisplayText(chronobio.golden_window?.visual_description, '')}</p>
                <div className="h-44">
                  <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart margin={{ top: 10, right: 10, bottom: 0, left: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" dataKey="x" domain={[0, 23]} tick={{ fontSize: 11 }} />
                      <YAxis type="number" dataKey="y" domain={[0, 6]} tickFormatter={(v) => dayOrder[v] || ''} tick={{ fontSize: 10 }} />
                      <ZAxis type="number" dataKey="z" range={[120, 420]} />
                      <Tooltip formatter={(value: any) => [`${Number(value).toFixed(2)}%`, 'Avg ER']} />
                      <Scatter data={heatmapData} fill="#4f46e5" />
                    </ScatterChart>
                  </ResponsiveContainer>
                </div>
              </>
          </div>
          )}

          {canRenderSentiment && (
          <div className="rounded-2xl border border-slate-200 p-4">
            <h4 className="mb-3 text-sm font-semibold text-slate-700">SENTIMENT CLOUD ENGINE</h4>
              <>
                <div className="mb-3 flex flex-wrap gap-2">
                  {Array.isArray(sentiment.top_keywords) && sentiment.top_keywords.length > 0 ? (
                    sentiment.top_keywords.slice(0, 10).map((w: string, i: number) => (
                      <span
                        key={`${w}-${i}`}
                        className={`rounded-full px-3 py-1 ${i < 3 ? 'bg-emerald-100 text-emerald-700' : i > 7 ? 'bg-rose-100 text-rose-700' : 'bg-slate-100 text-slate-700'}`}
                        style={{ fontSize: `${14 + Math.max(0, 8 - i)}px` }}
                      >
                        {sanitizeDisplayText(w, 'keyword')}
                      </span>
                    ))
                  ) : null}
                </div>
                <p className="text-xs text-slate-600">
                  Pos: {Number(sentiment.sentiment_split?.positive_pct || 0).toFixed(1)}% • Neg: {Number(sentiment.sentiment_split?.negative_pct || 0).toFixed(1)}% • Neu: {Number(sentiment.sentiment_split?.neutral_pct || 0).toFixed(1)}%
                </p>
              </>
          </div>
          )}

          {canRenderBenchmark && (
          <div className="rounded-2xl border border-slate-200 p-4">
            <h4 className="mb-3 text-sm font-semibold text-slate-700">COMPETITIVE BENCHMARK</h4>
              <div className="h-44">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={benchmarkData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="metric" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="user" name={locale === 'tr' ? 'Kullanıcı' : 'User'} fill="#2563eb" radius={[6, 6, 0, 0]} />
                    <Bar dataKey="competitor" name={locale === 'tr' ? 'Rakip' : 'Competitor'} fill="#9ca3af" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
          </div>
          )}
        </div>

        {trendData.length > 0 && (
        <div className="mt-4 rounded-2xl border border-slate-200 p-4">
          <div className="mb-2 flex items-center justify-between">
            <h4 className="text-sm font-semibold text-slate-700">TREND TRAJECTORY</h4>
            <div className="flex items-center gap-1 text-xs">
              {trendUp ? <TrendingUpIcon size={14} className="text-emerald-600" /> : <TrendingDownIcon size={14} className="text-rose-600" />}
              <span className={trendUp ? 'text-emerald-700' : 'text-rose-700'}>
                {trendUp ? (locale === 'tr' ? 'Yükseliş' : 'Rising') : (locale === 'tr' ? 'Düşüş' : 'Declining')}
              </span>
            </div>
          </div>
            <div className="h-24">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="value" stroke="#4f46e5" strokeWidth={2} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
        </div>
        )}
      </div>

      {badge.state === 'partial' && (
        <div className="mt-4 flex items-start gap-2 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-700">
          <ShieldIcon size={14} className="mt-0.5" />
          <p>{locale === 'tr' ? 'Estimated: Bu katmandaki metriklerde varyans olabilir; yöntem ve örneklem sınırlarını dikkate alınız.' : 'Estimated: Metrics may vary; consider methodology and sampling boundaries.'}</p>
        </div>
      )}
    </section>
  );
}

export default AdvancedIntelligenceDashboard;
