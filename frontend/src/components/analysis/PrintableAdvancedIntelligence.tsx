'use client';

import React, { useEffect, useState, useRef, useCallback } from 'react';
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

/**
 * 📊 PrintableAdvancedIntelligence
 * 
 * PDF export için optimize edilmiş Advanced Intelligence Dashboard.
 * 
 * Özellikler:
 * 1. SVG chart'ları otomatik olarak PNG'ye çevirir
 * 2. Animasyonları devre dışı bırakır
 * 3. Print-safe CSS uygular
 * 4. Word cloud için fallback sunar
 * 5. data-status attribute'ları ile render durumunu bildirir
 */

interface PrintableAdvancedIntelligenceProps {
  systemGovernor?: any;
  locale?: 'tr' | 'en';
  /** Chart'ları image'a çevir (Puppeteer için önerilen) */
  convertChartsToImages?: boolean;
  /** Render tamamlandığında çağrılır */
  onRenderComplete?: () => void;
}

const dayOrder = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'];

// Recharts animasyon config - PDF için disabled
const ANIMATION_CONFIG = {
  isAnimationActive: false,
  animationDuration: 0,
  animationBegin: 0,
};

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

type ConfidenceState = 'high' | 'partial' | 'low';

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
      text: 'Verified',
      classes: 'bg-emerald-100 text-emerald-700 border-emerald-300',
    };
  }
  if (state === 'partial') {
    return {
      state,
      text: 'Estimated',
      classes: 'bg-amber-100 text-amber-700 border-amber-300',
    };
  }
  return {
    state,
    text: locale === 'tr' ? 'Daha Fazla Veri Gerekli' : 'Needs More Data',
    classes: 'bg-rose-100 text-rose-700 border-rose-300',
  };
}

/**
 * SVG'yi Canvas'a çevirip base64 PNG olarak döndüren yardımcı fonksiyon
 */
async function svgToBase64Image(svgElement: SVGElement): Promise<string | null> {
  try {
    const svgRect = svgElement.getBoundingClientRect();
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    if (!ctx) return null;

    // 2x resolution
    canvas.width = svgRect.width * 2 || 400;
    canvas.height = svgRect.height * 2 || 300;

    // Clone SVG and add white background
    const clonedSvg = svgElement.cloneNode(true) as SVGElement;
    clonedSvg.setAttribute('width', String(canvas.width));
    clonedSvg.setAttribute('height', String(canvas.height));
    
    // Add background rect
    const bgRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    bgRect.setAttribute('width', '100%');
    bgRect.setAttribute('height', '100%');
    bgRect.setAttribute('fill', '#ffffff');
    clonedSvg.insertBefore(bgRect, clonedSvg.firstChild);

    const svgData = new XMLSerializer().serializeToString(clonedSvg);
    const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(svgBlob);

    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(url);
        resolve(canvas.toDataURL('image/png', 1.0));
      };
      img.onerror = () => {
        URL.revokeObjectURL(url);
        resolve(null);
      };
      img.src = url;
    });
  } catch (e) {
    console.error('SVG to image conversion failed:', e);
    return null;
  }
}

/**
 * 📈 ChartWithImageFallback
 * Chart'ı render eder, sonra PNG'ye çevirir ve gösterir
 */
function ChartWithImageFallback({
  chartId,
  children,
  height = 176,
  convertToImage = false,
}: {
  chartId: string;
  children: React.ReactNode;
  height?: number;
  convertToImage?: boolean;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [imageData, setImageData] = useState<string | null>(null);
  const [isRendered, setIsRendered] = useState(false);

  useEffect(() => {
    const timer = setTimeout(async () => {
      if (convertToImage && containerRef.current) {
        const svg = containerRef.current.querySelector('svg');
        if (svg) {
          const imgData = await svgToBase64Image(svg);
          if (imgData) {
            setImageData(imgData);
          }
        }
      }
      setIsRendered(true);
    }, 800);

    return () => clearTimeout(timer);
  }, [convertToImage]);

  return (
    <div
      ref={containerRef}
      className="chart-container"
      data-chart-id={chartId}
      data-status={isRendered ? 'rendered' : 'loading'}
      style={{ 
        height, 
        overflow: 'visible',
        pageBreakInside: 'avoid',
        breakInside: 'avoid',
      }}
    >
      {imageData ? (
        <img 
          src={imageData} 
          alt={`Chart ${chartId}`} 
          className="w-full h-full object-contain"
          style={{ maxHeight: height }}
        />
      ) : (
        children
      )}
    </div>
  );
}

/**
 * 🏷️ WordCloudFallback
 * Word cloud için print-safe fallback bileşeni
 */
function WordCloudFallback({
  keywords,
  sentimentSplit,
  locale,
}: {
  keywords: string[];
  sentimentSplit?: { positive_pct?: number; negative_pct?: number; neutral_pct?: number };
  locale: 'tr' | 'en';
}) {
  return (
    <div 
      className="word-cloud-fallback" 
      data-chart-id="sentiment-cloud"
      data-status="rendered"
      style={{ pageBreakInside: 'avoid', breakInside: 'avoid' }}
    >
      <div className="mb-3 flex flex-wrap gap-2">
        {keywords.slice(0, 12).map((word, i) => {
          const size = Math.max(11, 16 - i);
          const bgColor = i < 3 ? 'bg-emerald-100 text-emerald-700' 
            : i > 8 ? 'bg-rose-100 text-rose-700' 
            : 'bg-slate-100 text-slate-700';
          
          return (
            <span
              key={`${word}-${i}`}
              className={`rounded-full px-3 py-1 ${bgColor} print:border print:border-current`}
              style={{ fontSize: `${size}px` }}
            >
              {sanitizeDisplayText(word, 'keyword')}
            </span>
          );
        })}
      </div>
      <div className="text-xs text-slate-600 print:text-slate-800">
        <span className="inline-block mr-3">
          ✅ {locale === 'tr' ? 'Pozitif' : 'Positive'}: {(sentimentSplit?.positive_pct ?? 0).toFixed(1)}%
        </span>
        <span className="inline-block mr-3">
          ❌ {locale === 'tr' ? 'Negatif' : 'Negative'}: {(sentimentSplit?.negative_pct ?? 0).toFixed(1)}%
        </span>
        <span className="inline-block">
          ➖ {locale === 'tr' ? 'Nötr' : 'Neutral'}: {(sentimentSplit?.neutral_pct ?? 0).toFixed(1)}%
        </span>
      </div>
    </div>
  );
}

export function PrintableAdvancedIntelligence({
  systemGovernor,
  locale = 'tr',
  convertChartsToImages = true,
  onRenderComplete,
}: PrintableAdvancedIntelligenceProps) {
  const [allChartsRendered, setAllChartsRendered] = useState(false);
  const sectionRef = useRef<HTMLElement>(null);

  const advanced = systemGovernor?.advancedAnalytics;

  // Render complete callback
  useEffect(() => {
    if (allChartsRendered && onRenderComplete) {
      onRenderComplete();
    }
  }, [allChartsRendered, onRenderComplete]);

  // Chart render durumunu takip et
  useEffect(() => {
    const timer = setTimeout(() => {
      setAllChartsRendered(true);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

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
        { name: locale === 'tr' ? 'En Düşük' : 'Worst', value: Number((polarity.bottom_posts || []).reduce((s: number, p: any) => s + Number(p.engagement_rate || 0), 0) / Math.max(1, (polarity.bottom_posts || []).length)) },
        { name: locale === 'tr' ? 'En İyi' : 'Best', value: Number((polarity.top_posts || []).reduce((s: number, p: any) => s + Number(p.engagement_rate || 0), 0) / Math.max(1, (polarity.top_posts || []).length)) },
      ]
    : [];

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
    <section 
      ref={sectionRef}
      className="printable-advanced-intelligence rounded-3xl border border-slate-200 bg-white p-6 shadow-sm print:shadow-none print:border-slate-300"
      data-section="advanced-intelligence"
      data-status={allChartsRendered ? 'rendered' : 'loading'}
      style={{
        pageBreakInside: 'avoid',
        breakInside: 'avoid',
        overflow: 'visible',
      }}
    >
      {/* Print-specific styles */}
      <style jsx>{`
        .printable-advanced-intelligence {
          overflow: visible !important;
        }

        @media print {
          .printable-advanced-intelligence {
            page-break-inside: avoid !important;
            break-inside: avoid-page !important;
            overflow: visible !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }

          .printable-advanced-intelligence .chart-container {
            page-break-inside: avoid !important;
            break-inside: avoid-page !important;
            overflow: visible !important;
          }

          .printable-advanced-intelligence svg {
            overflow: visible !important;
          }

          /* Recharts animasyonlarını devre dışı bırak */
          .printable-advanced-intelligence .recharts-wrapper,
          .printable-advanced-intelligence .recharts-surface {
            overflow: visible !important;
          }

          .printable-advanced-intelligence .recharts-cartesian-grid,
          .printable-advanced-intelligence .recharts-cartesian-axis {
            opacity: 1 !important;
          }
        }
      `}</style>

      {/* Header */}
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3 print:mb-4">
        <div className="flex items-center gap-2">
          <BarChart3Icon size={20} className="text-indigo-600 print:text-indigo-700" />
          <h3 className="text-xl font-semibold text-slate-900">
            {locale === 'tr' ? 'Gelişmiş Analiz' : 'Advanced Intelligence'}
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${badge.classes}`}>
            {badge.text}
          </span>
          <span className="text-xs text-slate-500">{confidence}%</span>
        </div>
      </div>

      {badge.state === 'low' && (
        <div className="mb-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700 print:bg-rose-100">
          {locale === 'tr' 
            ? 'Bazı metrikler düşük güven seviyesinde; sonuçlar tahmini olabilir.' 
            : 'Some metrics are low-confidence; results may be estimated.'}
        </div>
      )}

      <div className={badge.state === 'low' ? 'opacity-70' : ''}>
        <div className="grid gap-4 lg:grid-cols-2 print:grid-cols-2">
          
          {/* Performance Polarity */}
          {canRenderPolarity && (
            <div 
              className="rounded-2xl border border-slate-200 p-4 print:border-slate-300"
              style={{ pageBreakInside: 'avoid', breakInside: 'avoid' }}
            >
              <h4 className="mb-3 text-sm font-semibold text-slate-700">
                {locale === 'tr' ? 'PERFORMANS POLARİTESİ' : 'PERFORMANCE POLARITY'}
              </h4>
              <div className="grid gap-3 md:grid-cols-2 print:grid-cols-2">
                <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 print:bg-emerald-100">
                  <p className="mb-2 text-xs font-semibold text-emerald-700">
                    {locale === 'tr' ? 'En İyi 3' : 'Top 3 (Best)'}
                  </p>
                  {(polarity.top_posts || []).slice(0, 3).map((p: any, i: number) => (
                    <div key={i} className="mb-1 text-xs text-slate-700">
                      #{p.post_id || i + 1} • ER {Number(p.engagement_rate || 0).toFixed(2)}%
                    </div>
                  ))}
                </div>
                <div className="rounded-xl border border-rose-200 bg-rose-50 p-3 print:bg-rose-100">
                  <p className="mb-2 text-xs font-semibold text-rose-700">
                    {locale === 'tr' ? 'En Düşük 3' : 'Bottom 3 (Worst)'}
                  </p>
                  {(polarity.bottom_posts || []).slice(0, 3).map((p: any, i: number) => (
                    <div key={i} className="mb-1 text-xs text-slate-700">
                      #{p.post_id || i + 1} • ER {Number(p.engagement_rate || 0).toFixed(2)}%
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Audience Chronobiology - Scatter Chart */}
          {canRenderChronobio && (
            <div 
              className="rounded-2xl border border-slate-200 p-4 print:border-slate-300"
              style={{ pageBreakInside: 'avoid', breakInside: 'avoid' }}
            >
              <h4 className="mb-3 text-sm font-semibold text-slate-700">
                {locale === 'tr' ? 'HEDEFLİ ZAMAN DİLİMİ' : 'AUDIENCE CHRONOBIOLOGY'}
              </h4>
              <p className="mb-2 text-xs text-slate-600">
                {sanitizeDisplayText(chronobio.golden_window?.visual_description, '')}
              </p>
              <ChartWithImageFallback chartId="chronobiology-scatter" height={176} convertToImage={convertChartsToImages}>
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 10, right: 10, bottom: 0, left: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      type="number" 
                      dataKey="x" 
                      domain={[0, 23]} 
                      tick={{ fontSize: 11 }}
                      {...ANIMATION_CONFIG}
                    />
                    <YAxis 
                      type="number" 
                      dataKey="y" 
                      domain={[0, 6]} 
                      tickFormatter={(v) => dayOrder[v] || ''} 
                      tick={{ fontSize: 10 }}
                      {...ANIMATION_CONFIG}
                    />
                    <ZAxis type="number" dataKey="z" range={[120, 420]} />
                    <Tooltip formatter={(value: any) => [`${Number(value).toFixed(2)}%`, 'Avg ER']} />
                    <Scatter 
                      data={heatmapData} 
                      fill="#4f46e5" 
                      {...ANIMATION_CONFIG}
                    />
                  </ScatterChart>
                </ResponsiveContainer>
              </ChartWithImageFallback>
            </div>
          )}

          {/* Sentiment Cloud - Word Cloud Fallback */}
          {canRenderSentiment && (
            <div 
              className="rounded-2xl border border-slate-200 p-4 print:border-slate-300"
              style={{ pageBreakInside: 'avoid', breakInside: 'avoid' }}
            >
              <h4 className="mb-3 text-sm font-semibold text-slate-700">
                {locale === 'tr' ? 'DUYGU ANALİZİ' : 'SENTIMENT CLOUD ENGINE'}
              </h4>
              <WordCloudFallback
                keywords={sentiment.top_keywords || []}
                sentimentSplit={sentiment.sentiment_split}
                locale={locale}
              />
            </div>
          )}

          {/* Competitive Benchmark - Bar Chart */}
          {canRenderBenchmark && (
            <div 
              className="rounded-2xl border border-slate-200 p-4 print:border-slate-300"
              style={{ pageBreakInside: 'avoid', breakInside: 'avoid' }}
            >
              <h4 className="mb-3 text-sm font-semibold text-slate-700">
                {locale === 'tr' ? 'REKABETÇİ KARŞILAŞTIRMA' : 'COMPETITIVE BENCHMARK'}
              </h4>
              <ChartWithImageFallback chartId="benchmark-bar" height={176} convertToImage={convertChartsToImages}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={benchmarkData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="metric" tick={{ fontSize: 11 }} {...ANIMATION_CONFIG} />
                    <YAxis tick={{ fontSize: 11 }} {...ANIMATION_CONFIG} />
                    <Tooltip />
                    <Legend />
                    <Bar 
                      dataKey="user" 
                      name={locale === 'tr' ? 'Kullanıcı' : 'User'} 
                      fill="#2563eb" 
                      radius={[6, 6, 0, 0]}
                      {...ANIMATION_CONFIG}
                    />
                    <Bar 
                      dataKey="competitor" 
                      name={locale === 'tr' ? 'Rakip' : 'Competitor'} 
                      fill="#9ca3af" 
                      radius={[6, 6, 0, 0]}
                      {...ANIMATION_CONFIG}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </ChartWithImageFallback>
            </div>
          )}
        </div>

        {/* Trend Trajectory - Line Chart */}
        {trendData.length > 0 && (
          <div 
            className="mt-4 rounded-2xl border border-slate-200 p-4 print:border-slate-300"
            style={{ pageBreakInside: 'avoid', breakInside: 'avoid' }}
          >
            <div className="mb-2 flex items-center justify-between">
              <h4 className="text-sm font-semibold text-slate-700">
                {locale === 'tr' ? 'TREND TRAJEKTÖRİSİ' : 'TREND TRAJECTORY'}
              </h4>
              <div className="flex items-center gap-1 text-xs">
                {trendUp ? (
                  <TrendingUpIcon size={14} className="text-emerald-600" />
                ) : (
                  <TrendingDownIcon size={14} className="text-rose-600" />
                )}
                <span className={trendUp ? 'text-emerald-700' : 'text-rose-700'}>
                  {trendUp ? (locale === 'tr' ? 'Yükseliş' : 'Rising') : (locale === 'tr' ? 'Düşüş' : 'Declining')}
                </span>
              </div>
            </div>
            <ChartWithImageFallback chartId="trend-line" height={96} convertToImage={convertChartsToImages}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} {...ANIMATION_CONFIG} />
                  <YAxis tick={{ fontSize: 11 }} {...ANIMATION_CONFIG} />
                  <Tooltip />
                  <Line 
                    type="monotone" 
                    dataKey="value" 
                    stroke="#4f46e5" 
                    strokeWidth={2} 
                    dot={{ r: 4 }}
                    {...ANIMATION_CONFIG}
                  />
                </LineChart>
              </ResponsiveContainer>
            </ChartWithImageFallback>
          </div>
        )}
      </div>

      {badge.state === 'partial' && (
        <div className="mt-4 flex items-start gap-2 rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-700 print:bg-amber-100">
          <ShieldIcon size={14} className="mt-0.5" />
          <p>
            {locale === 'tr' 
              ? 'Tahmini: Bu katmandaki metriklerde varyans olabilir; yöntem ve örneklem sınırlarını dikkate alınız.' 
              : 'Estimated: Metrics may vary; consider methodology and sampling boundaries.'}
          </p>
        </div>
      )}
    </section>
  );
}

export default PrintableAdvancedIntelligence;
