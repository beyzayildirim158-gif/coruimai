"use client";

import { useParams, useSearchParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
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
} from '@/components/analysis';
import { gradeColor, formatNumber, formatPercentage, formatDateTime } from '@/lib/formatters';
import { LoaderIcon, CheckCircleIcon, UsersIcon, UserPlusIcon, Grid3X3Icon, UserIcon, BarChart3Icon, SparkIcon } from '@/components/icons';
import type { AgentResult } from '@/store/analysisStore';
import { ContentPlanViewer } from '@/components/content-plan';
import { useEffect, useState } from 'react';

/**
 * 📄 PDF PRINT VIEW
 * Bu sayfa PDF generator tarafından Puppeteer ile render edilir.
 * Frontend'deki tüm chartlar ve componentler birebir PDF'e aktarılır.
 */

function ProfileAvatar({ src, username }: { src?: string; username: string }) {
  const [imgError, setImgError] = useState(false);
  
  if (!src || imgError) {
    return (
      <div className="flex h-20 w-20 items-center justify-center rounded-full border-4 border-white bg-gradient-to-br from-primary-400 to-primary-600 shadow-lg print:shadow-none">
        <UserIcon size={40} className="text-white" />
      </div>
    );
  }

  const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001/api';
  const imageSrc = src.startsWith('data:') 
    ? src 
    : `${apiBase}/proxy/image?url=${encodeURIComponent(src)}`;
  
  return (
    <img 
      src={imageSrc} 
      alt={username}
      className="h-20 w-20 rounded-full border-4 border-white shadow-lg object-cover print:shadow-none"
      onError={() => setImgError(true)}
    />
  );
}

export default function PrintViewPage() {
  const params = useParams<{ id: string }>();
  const searchParams = useSearchParams();
  const analysisId = params?.id;
  
  // URL'den hangi bölümlerin dahil edileceğini al
  const sectionsParam = searchParams?.get('sections');
  const sections = sectionsParam ? sectionsParam.split(',') : null; // null = tümü
  const locale = searchParams?.get('locale') || 'tr';
  
  const [isReady, setIsReady] = useState(false);

  const analysisQuery = useQuery({
    queryKey: ['analysis', analysisId],
    queryFn: async () => {
      const response = await api.get(`/analyze/result/${analysisId}`);
      return response.data.data;
    },
    enabled: Boolean(analysisId),
    retry: false,
  });

  // Sayfa yüklendikten sonra print-ready sinyali ver
  useEffect(() => {
    if (analysisQuery.data && !analysisQuery.isLoading) {
      // Chartların render olması için biraz bekle
      const timer = setTimeout(() => {
        setIsReady(true);
        // Puppeteer'ın okuyacağı global değişken
        (window as any).__PRINT_READY__ = true;
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [analysisQuery.data, analysisQuery.isLoading]);

  // Bölüm gösterme kontrolü
  const showSection = (sectionId: string): boolean => {
    if (!sections) return true; // sections null ise tümünü göster
    return sections.includes(sectionId);
  };

  if (analysisQuery.isLoading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <LoaderIcon size={32} className="animate-spin text-primary-500 mx-auto mb-4" />
          <p className="text-slate-500">Rapor hazırlanıyor...</p>
        </div>
      </div>
    );
  }

  if (analysisQuery.isError || !analysisQuery.data) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center text-red-600">
          <p>Analiz yüklenemedi</p>
        </div>
      </div>
    );
  }

  const analysis = analysisQuery.data;
  const { eli5Report, finalVerdict, businessIdentity, advancedAnalysis, sanitizationReport: sanitizationFromAgents, hardValidation: hardValidationFromAgents, ...otherAgentResults } = analysis.agentResults || {};
  const agentEntries = Object.entries(otherAgentResults || {});
  const sanitizationReport = sanitizationFromAgents || analysis.sanitizationReport;
  const hardValidation = hardValidationFromAgents || analysis.hardValidation;

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
          .page-break { page-break-before: always; }
          .avoid-break { page-break-inside: avoid; }
        }
        @page {
          size: A4;
          margin: 10mm;
        }
        /* PDF için optimize */
        .print-section {
          page-break-inside: avoid;
          margin-bottom: 20px;
        }
      `}</style>

      {/* Cover Page */}
      {showSection('coverPage') && (
        <div className="print-section bg-gradient-to-br from-slate-900 via-primary-900 to-slate-900 text-white p-8 rounded-3xl mb-6 print:rounded-none print:mb-0">
          <div className="flex justify-between items-start mb-8">
            <div>
              <p className="text-primary-400 text-sm font-bold tracking-widest uppercase">Instagram AI</p>
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
        {showSection('advancedAnalysis') && advancedAnalysis && (
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
        {showSection('metricsDashboard') && (
          <div className="print-section page-break">
            <ComprehensiveMetricsDashboard 
              agentResults={otherAgentResults} 
              businessIdentity={businessIdentity}
              hardValidation={hardValidation}
            />
          </div>
        )}

        {/* Sanitization Report */}
        {showSection('sanitizationReport') && sanitizationReport && (
          <div className="print-section">
            <SanitizationReport data={sanitizationReport} />
          </div>
        )}

        {/* Score Explainer */}
        {showSection('scoreExplainer') && (
          <div className="print-section rounded-3xl border border-slate-200 bg-white p-6 shadow-sm print:shadow-none print:border-slate-300">
            <div className="flex items-center gap-3 mb-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100">
                <BarChart3Icon size={20} className="text-primary-600" />
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
        {showSection('actionPlan') && (
          <div className="print-section page-break">
            <PrioritizedActions actions={extractPriorityActions(analysis)} />
          </div>
        )}

        {/* Agent Results */}
        {showSection('agentResults') && agentEntries.length > 0 && (
          <div className="print-section space-y-4">
            <div className="flex items-center gap-3 px-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-100">
                <SparkIcon size={16} className="text-slate-600" />
              </div>
              <p className="text-sm uppercase tracking-widest text-slate-500">Detaylı Ajan Analizleri</p>
            </div>
            {agentEntries.map(([agentKey, result]) => (
              <div key={agentKey} className="avoid-break">
                <AgentResultAccordion agentKey={agentKey} result={result as AgentResult} defaultOpen={true} />
              </div>
            ))}
          </div>
        )}

        {/* Content Plan */}
        {showSection('contentPlan') && analysisId && (
          <div className="print-section page-break">
            <ContentPlanViewer analysisId={analysisId} />
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
