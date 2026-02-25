"use client";

import { useParams, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { 
  AgentResultAccordion,
  ExecutiveSummary,
  generateExecutiveSummary,
  ScoreExplainer,
  createScoreData,
  BenchmarkGrid,
  createBenchmarkData,
  PrioritizedActions,
  extractPriorityActions,
  ELI5Report,
  FinalVerdict,
  BusinessIdentity,
  AdvancedAnalysisSection,
  SanitizationReport,
  ComprehensiveMetricsDashboard,
  JargonGlossary,
} from '@/components/analysis';
import { formatNumber, formatDateTime } from '@/lib/formatters';
import { LoaderIcon, UsersIcon, UserIcon, BarChart3Icon, SparkIcon } from '@/components/icons';
import type { AgentResult } from '@/store/analysisStore';
import axios from 'axios';

/**
 * 📄 PDF PRINT VIEW - Unauthenticated
 * Bu sayfa PDF generator tarafından Puppeteer ile render edilir.
 * Auth gerektirmez - doğrudan internal API'den veri çeker.
 * Frontend'deki tüm chartlar ve componentler birebir PDF'e aktarılır.
 */

function resolveApiUrl(): string {
  const configured = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001/api';

  if (typeof window === 'undefined') return configured;

  // Puppeteer from docker network opens frontend as http://frontend:3000
  // In that case localhost would point to pdf-generator container, not backend.
  if (window.location.hostname === 'frontend') {
    return 'http://backend-api:3001/api';
  }

  return configured;
}

const PLACEHOLDER_REGEX = /\b(undefined|belirleniyor|loading\.\.\.|null|none|nan)\b/i;
const ALLOWED_TEXT_REGEX = /[^0-9A-Za-zÇĞİÖŞÜçğıöşü\s.,;:!?\-_'"%&/+#@*()\[\]{}=<>|]/g;

function sanitizeForPdf(input: any): any {
  if (input === undefined || input === null) return undefined;

  if (typeof input === 'string') {
    const trimmed = input.trim();
    if (!trimmed) return undefined;
    if (PLACEHOLDER_REGEX.test(trimmed)) return undefined;
    const cleaned = trimmed.replace(ALLOWED_TEXT_REGEX, '').replace(/\s{2,}/g, ' ').trim();
    if (!cleaned || PLACEHOLDER_REGEX.test(cleaned)) return undefined;
    return cleaned;
  }

  if (Array.isArray(input)) {
    const cleaned = input
      .map((item) => sanitizeForPdf(item))
      .filter((item) => item !== undefined);
    return cleaned.length > 0 ? cleaned : undefined;
  }

  if (typeof input === 'object') {
    const out: Record<string, any> = {};
    Object.entries(input).forEach(([key, value]) => {
      const cleaned = sanitizeForPdf(value);
      if (cleaned !== undefined) {
        out[key] = cleaned;
      }
    });
    return Object.keys(out).length > 0 ? out : undefined;
  }

  return input;
}

function ProfileAvatar({ src, username }: { src?: string; username: string }) {
  const [imgError, setImgError] = useState(false);
  const apiUrl = resolveApiUrl();
  
  if (!src || imgError) {
    return (
      <div className="flex h-20 w-20 items-center justify-center rounded-full border-4 border-white bg-gradient-to-br from-primary-400 to-primary-600 shadow-lg print:shadow-none">
        <UserIcon size={40} className="text-white" />
      </div>
    );
  }

  const imageSrc = src.startsWith('data:') 
    ? src 
    : `${apiUrl}/proxy/image?url=${encodeURIComponent(src)}`;
  
  return (
    <img 
      src={imageSrc} 
      alt={username}
      className="h-20 w-20 rounded-full border-4 border-white shadow-lg object-cover print:shadow-none"
      onError={() => setImgError(true)}
    />
  );
}

export default function PrintAnalysisPage() {
  const params = useParams<{ id: string }>();
  const searchParams = useSearchParams();
  const analysisId = params?.id;
  const agentSectionIds = ['domainMaster', 'growthVirality', 'salesConversion', 'visualBrand', 'communityLoyalty', 'attentionArchitect', 'systemGovernor'];
  
  // URL'den hangi bölümlerin dahil edileceğini al
  const sectionsParam = searchParams?.get('sections');
  const sections = sectionsParam ? sectionsParam.split(',') : null; // null = tümü
  const locale = searchParams?.get('locale') || 'tr';
  
  const [isReady, setIsReady] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const apiUrl = resolveApiUrl();

  // Fetch analysis data directly (no auth required for print view)
  useEffect(() => {
    if (!analysisId) return;
    
    const fetchAnalysis = async () => {
      try {
        // Internal API call - PDF generator container içinden geldiği için auth gerekmiyor
        // Backend'de bu endpoint'i public yapacağız
        const response = await axios.get(`${apiUrl}/analyze/print/${analysisId}`);
        setAnalysis(sanitizeForPdf(response.data.data) ?? response.data.data);
        setLoading(false);
      } catch (err: any) {
        console.error('Failed to fetch analysis:', err);
        setError(err.response?.data?.message || 'Analiz yüklenemedi');
        setLoading(false);
      }
    };
    
    fetchAnalysis();
  }, [analysisId, apiUrl]);

  // Sayfa yüklendikten sonra print-ready sinyali ver
  useEffect(() => {
    if (analysis && !loading) {
      // Chartların render olması için bekle
      const timer = setTimeout(() => {
        setIsReady(true);
        // Puppeteer'ın okuyacağı global değişken
        (window as any).__PRINT_READY__ = true;
        console.log('🖨️ Print ready signal sent');
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [analysis, loading]);

  // Bölüm gösterme kontrolü
  const showSection = (sectionId: string): boolean => !sections || sections.includes(sectionId);
  const showAnySection = (...sectionIds: string[]): boolean => !sections || sectionIds.some((id) => sections.includes(id));
  const showAgentSection = (agentKey: string): boolean => !sections || sections.includes(agentKey);

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <LoaderIcon size={32} className="animate-spin text-primary-500 mx-auto mb-4" />
          <p className="text-slate-500">Rapor hazırlanıyor...</p>
        </div>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center text-red-600">
          <p>{error || 'Analiz yüklenemedi'}</p>
        </div>
      </div>
    );
  }

  const { eli5Report, finalVerdict, businessIdentity, advancedAnalysis, sanitizationReport: sanitizationFromAgents, hardValidation: hardValidationFromAgents, ...otherAgentResults } = analysis.agentResults || {};
  const agentEntries = Object.entries(otherAgentResults || {});
  const filteredAgentEntries = agentEntries.filter(([agentKey]) => showAgentSection(agentKey));
  const sanitizationReport = sanitizationFromAgents || analysis.sanitizationReport;
  const hardValidation = hardValidationFromAgents || analysis.hardValidation;
  const contentPlan = analysis.contentPlan || analysis.agentResults?.contentPlan || null;

  return (
    <div 
      id="print-container"
      className="min-h-screen bg-white print:bg-white"
      data-print-ready={isReady}
    >
      {/* Print Styles */}
      <style jsx global>{`
        @media print {
          body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
          .page-break { page-break-before: always; break-before: page; }
          .avoid-break { page-break-inside: avoid; break-inside: avoid-page; }

          /* Başlık ile onu takip eden ilk kart ayrı sayfaya düşmesin */
          h1, h2, h3, h4, h5, h6 {
            page-break-after: avoid;
            break-after: avoid-page;
          }

          /* Yaygın kart/container blokları iki sayfaya bölünmesin */
          .rounded-3xl,
          .rounded-2xl,
          .rounded-xl,
          .stat-card,
          .finding-box,
          .hook-card,
          .verdict-card,
          .agent-card,
          .metric-card {
            page-break-inside: avoid;
            break-inside: avoid-page;
          }

          /* Grafik ve medya elemanları bölünmesin */
          canvas,
          svg,
          img,
          table,
          tr,
          pre,
          blockquote {
            page-break-inside: avoid;
            break-inside: avoid-page;
          }

          /* Flex/Grid parent'larda Chrome print bölünmesini stabilize et */
          .grid,
          [class*="grid-cols-"],
          .flex {
            break-inside: auto;
          }
        }
        @page {
          size: A4;
          margin: 8mm;
        }
        /* PDF için optimize */
        .print-section {
          page-break-inside: auto;
          break-inside: auto;
          margin-bottom: 20px;
        }

        /* Bölüm içindeki çocuklar mümkünse tek parça kalsın */
        .print-section > * {
          break-inside: avoid-page;
        }
        /* Tailwind primary color fix for print */
        .from-primary-400 { --tw-gradient-from: #60a5fa; }
        .to-primary-600 { --tw-gradient-to: #2563eb; }
        .text-primary-500 { color: #3b82f6; }
        .text-primary-600 { color: #2563eb; }
        .bg-primary-100 { background-color: #dbeafe; }
        .bg-primary-50 { background-color: #eff6ff; }
        .border-primary-600 { border-color: #2563eb; }
      `}</style>

      {/* Cover Page */}
      {showSection('coverPage') && (
        <div className="print-section bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white p-8 rounded-3xl mb-6 print:rounded-none print:mb-0">
          <div className="flex justify-between items-start mb-8">
            <div>
              <p className="text-blue-400 text-sm font-bold tracking-widest uppercase">Instagram AI</p>
              <p className="text-slate-400 text-xs mt-1">Profesyonel Analiz Raporu</p>
            </div>
            <p className="text-slate-400 text-sm">{formatDateTime(analysis.completedAt)}</p>
          </div>

          <div className="flex flex-col items-center text-center py-12">
            <ProfileAvatar src={analysis.account.profilePicUrl} username={analysis.account.username} />
            <h1 className="text-4xl font-bold mt-6">@{analysis.account.username}</h1>
            {analysis.account.fullName && (
              <p className="text-slate-400 mt-2">{analysis.account.fullName}</p>
            )}
            
            <div className="flex items-center gap-8 mt-8">
              <div className="text-center">
                <p className="text-3xl font-bold">{formatNumber(analysis.account.followers)}</p>
                <p className="text-slate-400 text-sm">Takipçi</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold">{formatNumber(analysis.account.following)}</p>
                <p className="text-slate-400 text-sm">Takip</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold">{formatNumber(analysis.account.posts)}</p>
                <p className="text-slate-400 text-sm">Gönderi</p>
              </div>
            </div>

            <div className="mt-12 bg-white/10 backdrop-blur rounded-2xl p-6">
              <p className="text-slate-300 text-sm mb-2">Genel Skor</p>
              <p className={`text-6xl font-bold ${
                (analysis.overallScore || 0) >= 70 ? 'text-green-400' :
                (analysis.overallScore || 0) >= 40 ? 'text-yellow-400' : 'text-red-400'
              }`}>
                {analysis.overallScore?.toFixed(0) ?? '--'}
              </p>
              <p className="text-slate-400 text-sm mt-2">Derece: {analysis.scoreGrade ?? '—'}</p>
            </div>
          </div>
        </div>
      )}

      {/* Content Sections */}
      <div className="space-y-6 p-4 print:p-0">
        
        {/* Executive Summary */}
        {showSection('executiveSummary') && (
          <div className="print-section">
            <ExecutiveSummary {...generateExecutiveSummary(analysis)} />
          </div>
        )}

        {/* Advanced Analysis */}
        {showAnySection('swotAnalysis', 'riskAssessment', 'contentStrategy') && advancedAnalysis && (
          <div className="print-section page-break">
            <AdvancedAnalysisSection data={advancedAnalysis} />
          </div>
        )}

        {/* Business Identity */}
        {showSection('businessIdentity') && businessIdentity && (
          <div className="print-section">
            <BusinessIdentity data={businessIdentity} />
          </div>
        )}

        {/* ELI5 Report */}
        {showSection('eli5Report') && eli5Report && (
          <div className="print-section page-break">
            <ELI5Report data={eli5Report} />
          </div>
        )}

        {/* Final Verdict */}
        {showSection('finalVerdict') && finalVerdict && (
          <div className="print-section">
            <FinalVerdict data={finalVerdict} />
          </div>
        )}

        {/* Comprehensive Metrics Dashboard */}
        {showAnySection(...agentSectionIds) && (
          <div className="print-section page-break">
            <ComprehensiveMetricsDashboard 
              agentResults={otherAgentResults} 
              businessIdentity={businessIdentity}
              hardValidation={hardValidation}
            />
          </div>
        )}

        {/* Sanitization Report */}
        {showAnySection('riskAssessment', 'contentStrategy') && sanitizationReport && (
          <div className="print-section">
            <SanitizationReport data={sanitizationReport} />
          </div>
        )}

        {/* Score Explainer */}
        {showSection('scoreExplainer') && (
          <div className="print-section rounded-3xl border border-slate-200 bg-white p-6 shadow-sm print:shadow-none print:border-slate-300">
            <div className="flex items-center gap-3 mb-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
                <BarChart3Icon size={20} className="text-blue-600" />
              </div>
              <div>
                <p className="text-sm uppercase tracking-widest text-slate-500">Skor Açıklaması</p>
                <p className="text-lg font-semibold text-slate-900">Neden bu puanı aldınız?</p>
              </div>
            </div>
            <ScoreExplainer scores={[
              createScoreData('Genel Performans', analysis.overallScore || 0, {
                explanation: 'Hesabınızın toplam performans puanı. Tüm metriklerin ağırlıklı ortalamasıdır.',
                nicheAverage: 55,
                topPerformers: 75
              }),
              createScoreData('Etkileşim Kalitesi', Math.min(100, (analysis.account?.engagementRate || 0) * 20), {
                explanation: 'Takipçilerinizin içeriklerinizle ne kadar aktif etkileşime girdiği.',
                nicheAverage: 35,
                topPerformers: 70
              }),
              createScoreData('Topluluk Sağlığı', 100 - (analysis.account?.botScore || 50), {
                explanation: 'Takipçi kitlesinizin gerçek ve aktif olma oranı.',
                nicheAverage: 50,
                topPerformers: 80
              }),
            ]} />
          </div>
        )}

        {/* Benchmarks */}
        {showSection('benchmarks') && (
          <div className="print-section rounded-3xl border border-slate-200 bg-white p-6 shadow-sm print:shadow-none print:border-slate-300">
            <div className="flex items-center gap-3 mb-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-amber-100">
                <UsersIcon className="h-5 w-5 text-amber-600" />
              </div>
              <div>
                <p className="text-sm uppercase tracking-widest text-slate-500">Karşılaştırma</p>
                <p className="text-lg font-semibold text-slate-900">Sektör ortalamalarına göre konumunuz</p>
              </div>
            </div>
            <BenchmarkGrid benchmarks={[
              createBenchmarkData('Etkileşim Oranı', analysis.account?.engagementRate || 0, { average: 2.5, top: 5.0 }, { unit: '%' }),
              createBenchmarkData('Post Başına Beğeni', analysis.account?.avgLikes || 0, { 
                average: Math.round((analysis.account?.followers || 1000) * 0.02),
                top: Math.round((analysis.account?.followers || 1000) * 0.05)
              }),
              createBenchmarkData('Bot Riski', 100 - (analysis.account?.botScore || 50), { average: 50, top: 80 }, { unit: '%', higherIsBetter: true }),
              createBenchmarkData('Takipçi/Takip Oranı', (analysis.account?.followers || 0) / Math.max(1, analysis.account?.following || 1), { average: 1.5, top: 3.0 }, { unit: 'x' }),
            ]} />
          </div>
        )}

        {/* Prioritized Actions */}
        {showAnySection('actionPlan') && (
          <div className="print-section page-break">
            <PrioritizedActions actions={extractPriorityActions(analysis)} />
          </div>
        )}

        {/* Agent Results */}
        {showAnySection(...agentSectionIds) && filteredAgentEntries.length > 0 && (
          <div className="print-section space-y-4">
            <div className="flex items-center gap-3 px-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-100">
                <SparkIcon size={16} className="text-slate-600" />
              </div>
              <p className="text-sm uppercase tracking-widest text-slate-500">Detaylı Ajan Analizleri</p>
            </div>
            {filteredAgentEntries.map(([agentKey, result]) => (
              <div key={agentKey} className="avoid-break">
                <AgentResultAccordion agentKey={agentKey} result={result as AgentResult} defaultOpen={true} />
              </div>
            ))}
          </div>
        )}

        {/* Hook Rewrites */}
        {showSection('hookRewrites') && eli5Report?.rewrittenHooks && Array.isArray(eli5Report.rewrittenHooks) && eli5Report.rewrittenHooks.length > 0 && (
          <div className="print-section rounded-3xl border border-slate-200 bg-white p-6 shadow-sm print:shadow-none print:border-slate-300">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Hook İyileştirmeleri</h3>
            <div className="space-y-3">
              {eli5Report.rewrittenHooks.slice(0, 10).map((item: any, idx: number) => (
                <div key={idx} className="rounded-xl border border-slate-200 p-4">
                  <p className="text-xs text-slate-500 mb-1">Orijinal</p>
                  <p className="text-sm text-slate-700 mb-2">{item?.originalHook || item?.originalPost || '-'}</p>
                  <p className="text-xs text-slate-500 mb-1">Yeni Hook</p>
                  <p className="text-sm font-medium text-slate-900">{item?.newHook || '-'}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Content Plan */}
        {showSection('contentCalendar') && contentPlan?.weeklyPlan && Array.isArray(contentPlan.weeklyPlan) && contentPlan.weeklyPlan.length > 0 && (
          <div className="print-section page-break rounded-3xl border border-slate-200 bg-white p-6 shadow-sm print:shadow-none print:border-slate-300">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">7 Günlük İçerik Planı</h3>
            <div className="space-y-3">
              {contentPlan.weeklyPlan.slice(0, 7).map((day: any, idx: number) => (
                <div key={idx} className="rounded-xl border border-slate-200 p-4">
                  <p className="text-sm font-semibold text-slate-900">{day?.dayName || `Gün ${day?.day || idx + 1}`}</p>
                  <p className="text-sm text-slate-700 mt-1">{day?.contentType || '-'} • {day?.topic || '-'}</p>
                  {day?.hook && <p className="text-sm text-slate-600 mt-1"><span className="font-medium">Hook:</span> {day.hook}</p>}
                  {day?.bestTime && <p className="text-xs text-slate-500 mt-1">En iyi saat: {day.bestTime}</p>}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Glossary */}
        {showSection('glossary') && (
          <div className="print-section page-break">
            <JargonGlossary />
          </div>
        )}

        {/* Footer */}
        <div className="print-section text-center py-8 border-t border-slate-200 mt-8">
          <p className="text-slate-400 text-sm">
            Bu rapor Instagram AI tarafından {formatDateTime(new Date())} tarihinde oluşturulmuştur.
          </p>
          <p className="text-slate-300 text-xs mt-2">
            © 2026 Instagram AI - Profesyonel Hesap Analiz Sistemi
          </p>
        </div>
      </div>
    </div>
  );
}
