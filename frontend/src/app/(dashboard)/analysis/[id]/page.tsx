"use client";

import { useState } from 'react';
import { useParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import { 
  AgentResultAccordion,
  ExecutiveSummary,
  generateExecutiveSummary,
  ScoreExplainer,
  createScoreData,
  JargonGlossary,
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
  PdfCustomizer,
  AdvancedIntelligenceDashboard,
  DataQualityBadge,
  HighImpactDashboard,
} from '@/components/analysis';
import { extractHighImpactData } from '@/lib/extractHighImpactData';
import { gradeColor, formatNumber, formatPercentage, formatDateTime } from '@/lib/formatters';
import { LoaderIcon, DownloadCloudIcon, FileTextIcon, SparkIcon, CheckCircleIcon, UsersIcon, UserPlusIcon, Grid3X3Icon, LinkIcon, UserIcon, CalendarIcon, BarChart3Icon } from '@/components/icons';
import type { AgentResult } from '@/store/analysisStore';
import { ContentPlanViewer } from '@/components/content-plan';
import { useTranslation } from '@/i18n/TranslationProvider';
import { useAuthStore } from '@/store/authStore';

// Avatar component with fallback - uses base64 data or backend proxy for CORS
function ProfileAvatar({ src, username }: { src?: string; username: string }) {
  const [imgError, setImgError] = useState(false);
  
  if (!src || imgError) {
    return (
      <div className="flex h-16 w-16 items-center justify-center rounded-full border-2 border-white bg-gradient-to-br from-primary-400 to-primary-600 shadow-lg">
        <UserIcon size={32} className="text-white" />
      </div>
    );
  }

  // If it's already a data URI (base64), use directly - no CORS issues
  // Otherwise use backend proxy to bypass Instagram CORS restrictions
  // Note: NEXT_PUBLIC_API_URL already includes /api, so we just add /proxy/image
  const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001/api';
  const imageSrc = src.startsWith('data:') 
    ? src 
    : `${apiBase}/proxy/image?url=${encodeURIComponent(src)}`;
  
  return (
    <img 
      src={imageSrc} 
      alt={username}
      className="h-16 w-16 rounded-full border-2 border-white shadow-lg object-cover"
      onError={() => setImgError(true)}
    />
  );
}

type TabType = 'analysis' | 'content-plan';

export default function AnalysisDetailPage() {
  const params = useParams<{ id: string }>();
  const analysisId = params?.id;
  const [activeTab, setActiveTab] = useState<TabType>('analysis');
  const { t, locale } = useTranslation();
  const { user } = useAuthStore();
  const userTier = user?.subscriptionTier || 'STARTER';

  const analysisQuery = useQuery({
    queryKey: ['analysis', analysisId],
    queryFn: async () => {
      const response = await api.get(`/analyze/result/${analysisId}`);
      return response.data.data;
    },
    enabled: Boolean(analysisId),
    retry: false,
  });

  if (analysisQuery.isLoading) {
    return (
      <div className="rounded-2xl sm:rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 text-center text-slate-500 shadow-sm text-sm sm:text-base">
        <LoaderIcon size={20} className="mr-2 inline" /> {locale === 'tr' ? 'Analiz yükleniyor...' : 'Fetching analysis...'}
      </div>
    );
  }

  if (analysisQuery.isError) {
    return (
      <div className="rounded-2xl sm:rounded-3xl border border-red-200 bg-red-50 p-6 sm:p-8 text-center text-red-600 text-sm sm:text-base">
        {locale === 'tr' ? 'Analiz yüklenemedi. Analizin tamamlandığından emin olun.' : 'Unable to load analysis. Make sure it is completed.'}
      </div>
    );
  }

  const analysis = analysisQuery.data;
  
  // Extract ELI5, FinalVerdict, BusinessIdentity, AdvancedAnalysis from agentResults
  const { eli5Report, finalVerdict, businessIdentity, advancedAnalysis, sanitizationReport: sanitizationFromAgents, hardValidation: hardValidationFromAgents, dataQualityReport, ...otherAgentResults } = analysis.agentResults || {};
  const agentEntries = Object.entries(otherAgentResults || {});
  
  // Extract sanitization report and hard validation from analysis (can be in agentResults or root level)
  const sanitizationReport = sanitizationFromAgents || analysis.sanitizationReport;
  const hardValidation = hardValidationFromAgents || analysis.hardValidation;
  const governorResult = (analysis.agentResults || {}).systemGovernor;
  const rawConfidence = governorResult?.confidence_metrics?.overall_confidence
    ?? governorResult?.validation_summary?.analysis_confidence
    ?? governorResult?.quality_assurance?.qa_score
    ?? 1;
  const confidenceScore = Number(rawConfidence) <= 1 ? Number(rawConfidence) * 100 : Number(rawConfidence);
  const exportLocked = !Number.isNaN(confidenceScore) && confidenceScore < 50;

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="rounded-2xl sm:rounded-3xl border border-slate-200 bg-gradient-to-br from-primary-50 to-white p-4 sm:p-6 text-slate-900 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:flex-wrap items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3 sm:gap-4">
            <ProfileAvatar src={analysis.account.profilePicUrl} username={analysis.account.username} />
            <div>
              <p className="text-xs sm:text-sm uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500">
                {locale === 'tr' ? 'Instagram hesabı' : 'Instagram account'}
              </p>
              <div className="mt-1 flex items-center gap-2">
                <h1 className="text-xl sm:text-3xl font-bold text-slate-900">@{analysis.account.username}</h1>
                {analysis.account.isVerified && (
                  <CheckCircleIcon size={20} className="text-blue-500 sm:hidden" />
                )}
                {analysis.account.isVerified && (
                  <CheckCircleIcon size={24} className="text-blue-500 hidden sm:block" />
                )}
              </div>
              <p className="text-xs sm:text-sm text-slate-500">
                {locale === 'tr' ? 'Tamamlandı' : 'Completed'} {formatDateTime(analysis.completedAt)}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 sm:gap-4 w-full sm:w-auto">
            <div className="text-left sm:text-right flex-1 sm:flex-none">
              <p className="text-xs uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500">{locale === 'tr' ? 'Skor' : 'Score'}</p>
              <p className={`text-2xl sm:text-4xl font-semibold ${gradeColor(analysis.scoreGrade)}`}>
                {analysis.overallScore?.toFixed(0) ?? '--'}
              </p>
              <p className="text-xs text-slate-500">{locale === 'tr' ? 'Derece' : 'Grade'} {analysis.scoreGrade ?? '—'}</p>
            </div>
            {/* PDF Customizer - Özelleştirilebilir PDF Aktarma */}
            {!exportLocked ? (
              <PdfCustomizer 
                analysisId={analysisId || ''} 
                userTier={userTier}
              />
            ) : (
              <div className="rounded-lg sm:rounded-xl border border-rose-200 bg-rose-50 px-2 sm:px-3 py-1.5 sm:py-2 text-xs font-medium text-rose-700">
                {locale === 'tr' ? 'Needs More Data: Düşük güven skoru nedeniyle export geçici olarak devre dışı.' : 'Needs More Data: Export is temporarily disabled due to low confidence score.'}
              </div>
            )}
          </div>
        </div>

        {/* Bio Section */}
        {analysis.account.bio && (
          <div className="mt-3 sm:mt-4 rounded-xl sm:rounded-2xl border border-slate-200 bg-white/50 px-3 sm:px-4 py-2 sm:py-3">
            <p className="text-xs sm:text-sm text-slate-700 whitespace-pre-line">{analysis.account.bio}</p>
          </div>
        )}

        {/* Data Quality Badge — hidden (eksik veriler kullanıcıya gösterilmiyor) */}

        {/* Stats Grid */}
        <div className="mt-4 sm:mt-6 grid gap-2 sm:gap-4 grid-cols-2 md:grid-cols-5">
          <div className="rounded-xl sm:rounded-2xl border border-slate-200 bg-slate-50 px-3 sm:px-4 py-2 sm:py-3">
            <div className="flex items-center gap-1.5 sm:gap-2">
              <UsersIcon size={14} className="text-slate-400 sm:hidden" />
              <UsersIcon size={16} className="text-slate-400 hidden sm:block" />
              <p className="text-xs uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500 truncate">{t('results.followers')}</p>
            </div>
            <p className="text-lg sm:text-2xl font-semibold text-slate-900">{formatNumber(analysis.account.followers)}</p>
          </div>
          <div className="rounded-xl sm:rounded-2xl border border-slate-200 bg-slate-50 px-3 sm:px-4 py-2 sm:py-3">
            <div className="flex items-center gap-1.5 sm:gap-2">
              <UserPlusIcon size={14} className="text-slate-400 sm:hidden" />
              <UserPlusIcon size={16} className="text-slate-400 hidden sm:block" />
              <p className="text-xs uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500 truncate">{t('results.following')}</p>
            </div>
            <p className="text-lg sm:text-2xl font-semibold text-slate-900">{formatNumber(analysis.account.following)}</p>
          </div>
          <div className="rounded-xl sm:rounded-2xl border border-slate-200 bg-slate-50 px-3 sm:px-4 py-2 sm:py-3">
            <div className="flex items-center gap-1.5 sm:gap-2">
              <Grid3X3Icon size={14} className="text-slate-400 sm:hidden" />
              <Grid3X3Icon size={16} className="text-slate-400 hidden sm:block" />
              <p className="text-xs uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500 truncate">{t('results.posts')}</p>
            </div>
            <p className="text-lg sm:text-2xl font-semibold text-slate-900">{formatNumber(analysis.account.posts)}</p>
          </div>
          <div className="rounded-xl sm:rounded-2xl border border-slate-200 bg-slate-50 px-3 sm:px-4 py-2 sm:py-3">
            <p className="text-xs uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500 truncate">{t('results.engagement')}</p>
            <p className="text-lg sm:text-2xl font-semibold text-slate-900">{formatPercentage(analysis.account.engagementRate)}</p>
          </div>
          <div className="rounded-xl sm:rounded-2xl border border-slate-200 bg-slate-50 px-3 sm:px-4 py-2 sm:py-3">
            <p className="text-xs uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500 truncate">{t('results.botScore')}</p>
            <p className={`text-2xl font-semibold ${(analysis.account.botScore || 0) > 50 ? 'text-red-500' : 'text-green-600'}`}>
              {analysis.account.botScore?.toFixed(0) ?? '--'}
            </p>
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-3 sm:mt-4 flex flex-wrap gap-1.5 sm:gap-2">
          {analysis.account.isBusiness && (
            <span className="inline-flex items-center rounded-full bg-purple-100 px-2 sm:px-3 py-0.5 sm:py-1 text-xs font-medium text-purple-700">
              {locale === 'tr' ? 'İşletme Hesabı' : 'Business Account'}
            </span>
          )}
          {analysis.account.isVerified && (
            <span className="inline-flex items-center rounded-full bg-blue-100 px-2 sm:px-3 py-0.5 sm:py-1 text-xs font-medium text-blue-700">
              {locale === 'tr' ? 'Doğrulanmış' : 'Verified'}
            </span>
          )}
          {analysis.account.avgLikes > 0 && (
            <span className="inline-flex items-center rounded-full bg-pink-100 px-2 sm:px-3 py-0.5 sm:py-1 text-xs font-medium text-pink-700">
              {locale === 'tr' ? `Ort. ${formatNumber(analysis.account.avgLikes)} beğeni` : `Avg. ${formatNumber(analysis.account.avgLikes)} likes`}
            </span>
          )}
          {analysis.account.avgComments > 0 && (
            <span className="inline-flex items-center rounded-full bg-amber-100 px-2 sm:px-3 py-0.5 sm:py-1 text-xs font-medium text-amber-700">
              {locale === 'tr' ? `Ort. ${formatNumber(analysis.account.avgComments)} yorum` : `Avg. ${formatNumber(analysis.account.avgComments)} comments`}
            </span>
          )}
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="rounded-2xl sm:rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
        <div className="flex border-b border-slate-200 overflow-x-auto">
          <button
            onClick={() => setActiveTab('analysis')}
            className={`flex items-center gap-1.5 sm:gap-2 px-3 sm:px-6 py-3 sm:py-4 text-xs sm:text-sm font-medium transition-colors border-b-2 -mb-px whitespace-nowrap flex-shrink-0 ${
              activeTab === 'analysis'
                ? 'text-primary-600 border-primary-600 bg-primary-50/50'
                : 'text-slate-500 border-transparent hover:text-slate-700 hover:bg-slate-50'
            }`}
          >
            <BarChart3Icon size={14} className="sm:hidden" />
            <BarChart3Icon size={16} className="hidden sm:block" />
            {locale === 'tr' ? 'Analiz Sonuçları' : 'Analysis Results'}
          </button>
          <button
            onClick={() => setActiveTab('content-plan')}
            className={`flex items-center gap-1.5 sm:gap-2 px-3 sm:px-6 py-3 sm:py-4 text-xs sm:text-sm font-medium transition-colors border-b-2 -mb-px whitespace-nowrap flex-shrink-0 ${
              activeTab === 'content-plan'
                ? 'text-primary-600 border-primary-600 bg-primary-50/50'
                : 'text-slate-500 border-transparent hover:text-slate-700 hover:bg-slate-50'
            }`}
          >
            <CalendarIcon size={14} className="sm:hidden" />
            <CalendarIcon size={16} className="hidden sm:block" />
            {locale === 'tr' ? '7 Günlük İçerik Planı' : '7-Day Content Plan'}
          </button>
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'analysis' && (
        <>
          {/* Executive Summary - Quick overview at the top */}
          <ExecutiveSummary {...generateExecutiveSummary(analysis)} />

          {/* 🎯 HIGH IMPACT DASHBOARD - Vurucu Gerçekler */}
          <HighImpactDashboard 
            data={extractHighImpactData({
              agentResults: analysis.agentResults,
              profile: analysis.account,
              username: analysis.account?.username,
            })} 
            locale={locale === 'tr' ? 'tr' : 'en'} 
          />

          {/* Advanced Analysis Section - 11 Module Deep Analysis (if available) */}
          {advancedAnalysis && (
            <AdvancedAnalysisSection data={advancedAnalysis} />
          )}

          {/* Business Identity - Account type detection */}
          {businessIdentity && <BusinessIdentity data={businessIdentity} />}

          {/* ELI5 Report - Simplified explanation */}
          {eli5Report && <ELI5Report data={eli5Report} />}

          {/* Final Verdict - DeepSeek's final analysis */}
          {finalVerdict && <FinalVerdict data={finalVerdict} />}

          {/* Comprehensive Metrics Dashboard - All agent metrics in one view */}
          <ComprehensiveMetricsDashboard 
            agentResults={otherAgentResults} 
            businessIdentity={businessIdentity}
            hardValidation={hardValidation}
          />

          {/* Advanced Intelligence Dashboard - Heatmap, Sentiment, Benchmark, Polarity */}
          <AdvancedIntelligenceDashboard
            systemGovernor={governorResult}
            locale={locale === 'tr' ? 'tr' : 'en'}
          />

          {/* Sanitization Report - Data consistency checks */}
          {sanitizationReport && <SanitizationReport data={sanitizationReport} />}

          {/* Score Explanation - WHY this score */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100">
                <BarChart3Icon size={20} className="text-primary-600" />
              </div>
              <div>
                <p className="text-sm uppercase tracking-[0.3em] text-slate-500">
                  {locale === 'tr' ? 'Skor Açıklaması' : 'Score Explanation'}
                </p>
                <p className="text-lg font-semibold text-slate-900">
                  {locale === 'tr' ? 'Neden bu puanı aldınız?' : 'Why did you get this score?'}
                </p>
              </div>
            </div>
            <ScoreExplainer scores={[
              createScoreData(
                locale === 'tr' ? 'Genel Performans' : 'Overall Performance',
                analysis.overallScore || 0,
                {
                  explanation: locale === 'tr' 
                    ? ('Hesabınızın toplam performans puanı. Tüm metriklerin ağırlıklı ortalamasıdır. ' + 
                      (analysis.overallScore >= 70 
                        ? 'İçerik kalitesi ve etkileşim oranlarınız iyi seviyede.'
                        : analysis.overallScore >= 50
                        ? 'Bazı alanlarda iyileştirme potansiyeli var.'
                        : 'Ciddi optimizasyon gerekiyor. Önerileri takip edin.'))
                    : ('Your account\'s total performance score. A weighted average of all metrics. ' +
                      (analysis.overallScore >= 70
                        ? 'Your content quality and engagement rates are at a good level.'
                        : analysis.overallScore >= 50
                        ? 'There is potential for improvement in some areas.'
                        : 'Serious optimization needed. Follow the recommendations.')),
                  nicheAverage: 55,
                  topPerformers: 75
                }
              ),
              createScoreData(
                locale === 'tr' ? 'Etkileşim Kalitesi' : 'Engagement Quality',
                Math.min(100, (analysis.account?.engagementRate || 0) * 20),
                {
                  explanation: locale === 'tr'
                    ? ('Takipçilerinizin içeriklerinizle ne kadar aktif etkileşime girdiği. ' +
                      ((analysis.account?.engagementRate || 0) >= 3.5
                        ? 'Takipçileriniz içeriklerinizi seviyor ve aktif olarak etkileşime giriyor.'
                        : (analysis.account?.engagementRate || 0) >= 1.5
                        ? 'Ortalama bir etkileşim oranınız var. Hook ve CTA\'larınızı güçlendirin.'
                        : 'Etkileşim oranı düşük. İçerik stratejinizi gözden geçirin.'))
                    : ('How actively your followers engage with your content. ' +
                      ((analysis.account?.engagementRate || 0) >= 3.5
                        ? 'Your followers love your content and actively engage.'
                        : (analysis.account?.engagementRate || 0) >= 1.5
                        ? 'You have an average engagement rate. Strengthen your hooks and CTAs.'
                        : 'Engagement rate is low. Review your content strategy.')),
                  nicheAverage: 35,
                  topPerformers: 70
                }
              ),
              createScoreData(
                locale === 'tr' ? 'Topluluk Sağlığı' : 'Community Health',
                100 - (analysis.account?.botScore || 50),
                {
                  explanation: locale === 'tr'
                    ? ('Takipçi kitlesinizin gerçek ve aktif olma oranı. ' +
                      ((analysis.account?.botScore || 50) <= 30
                        ? 'Takipçi kitleniz gerçek ve kaliteli görünüyor.'
                        : (analysis.account?.botScore || 50) <= 50
                        ? 'Bazı şüpheli takipçiler var. Temizlik yapılabilir.'
                        : 'Bot/fake takipçi oranı yüksek. Organik büyümeye odaklanın.'))
                    : ('The ratio of your audience being real and active. ' +
                      ((analysis.account?.botScore || 50) <= 30
                        ? 'Your follower base looks real and quality.'
                        : (analysis.account?.botScore || 50) <= 50
                        ? 'There are some suspicious followers. Cleanup may help.'
                        : 'Bot/fake follower ratio is high. Focus on organic growth.')),
                  nicheAverage: 50,
                  topPerformers: 80
                }
              ),
            ]} />
          </div>

          {/* Benchmark Comparisons - How you compare to others */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-amber-100">
                <UsersIcon className="h-5 w-5 text-amber-600" />
              </div>
              <div>
                <p className="text-sm uppercase tracking-[0.3em] text-slate-500">
                  {locale === 'tr' ? 'Karşılaştırma' : 'Comparison'}
                </p>
                <p className="text-lg font-semibold text-slate-900">
                  {locale === 'tr' ? 'Sektör ortalamalarına göre konumunuz' : 'Your position compared to industry averages'}
                </p>
              </div>
            </div>
            <BenchmarkGrid benchmarks={[
              createBenchmarkData(
                locale === 'tr' ? 'Etkileşim Oranı' : 'Engagement Rate',
                analysis.account?.engagementRate || 0,
                { average: 2.5, top: 5.0 },
                { unit: '%' }
              ),
              createBenchmarkData(
                locale === 'tr' ? 'Post Başına Beğeni' : 'Likes per Post',
                analysis.account?.avgLikes || 0,
                { 
                  average: Math.round((analysis.account?.followers || 1000) * 0.02),
                  top: Math.round((analysis.account?.followers || 1000) * 0.05)
                }
              ),
              createBenchmarkData(
                locale === 'tr' ? 'Bot Riski' : 'Bot Risk',
                100 - (analysis.account?.botScore || 50),
                { average: 50, top: 80 },
                { unit: '%', higherIsBetter: true }
              ),
              createBenchmarkData(
                locale === 'tr' ? 'Takipçi/Takip Oranı' : 'Follower/Following Ratio',
                (analysis.account?.followers || 0) / Math.max(1, analysis.account?.following || 1),
                { average: 1.5, top: 3.0 },
                { unit: 'x' }
              ),
            ]} />
          </div>

          {/* Prioritized Actions - What to do, in order */}
          <PrioritizedActions 
            actions={extractPriorityActions(analysis)} 
          />

          {/* Agent Results - Detailed analysis */}
          <div className="space-y-4">
            <div className="flex items-center gap-3 px-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-100">
                <SparkIcon size={16} className="text-slate-600" />
              </div>
              <p className="text-sm uppercase tracking-[0.3em] text-slate-500">
                {locale === 'tr' ? 'Detaylı Ajan Analizleri' : 'Detailed Agent Analyses'}
              </p>
            </div>
            {agentEntries.map(([agentKey, result]) => (
              <AgentResultAccordion key={agentKey} agentKey={agentKey} result={result as AgentResult} />
            ))}
            {agentEntries.length === 0 && (
              <div className="rounded-3xl border border-slate-200 bg-white p-6 text-center text-slate-500 shadow-sm">
                {t('results.awaitingOutput')}
              </div>
            )}
          </div>

          {/* Jargon Glossary - Technical terms explained */}
          <JargonGlossary />

          {analysis.reports?.length > 0 && (
            <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
              <div className="flex items-center gap-3">
                <FileTextIcon size={20} className="text-primary-500" />
                <div>
                  <p className="text-sm uppercase tracking-[0.3em] text-slate-500">{t('reports.title')}</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {locale === 'tr' ? 'Hazır PDF\'ler' : 'Available PDFs'}
                  </p>
                </div>
              </div>
              <div className="mt-4 divide-y divide-slate-100 text-sm text-slate-700">
                {analysis.reports.map((report: any) => (
                  <a
                    key={report.id}
                    href={report.pdfUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center justify-between py-3 hover:text-primary-600"
                  >
                    <div>
                      <p className="font-semibold text-slate-900">{report.reportType} {locale === 'tr' ? 'raporu' : 'report'}</p>
                      <p className="text-xs text-slate-500">
                        {locale === 'tr' ? 'Oluşturuldu' : 'Generated'} {formatDateTime(report.generatedAt)}
                      </p>
                    </div>
                    <DownloadCloudIcon size={16} />
                  </a>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {activeTab === 'content-plan' && analysisId && (
        <ContentPlanViewer analysisId={analysisId} />
      )}
    </div>
  );
}
