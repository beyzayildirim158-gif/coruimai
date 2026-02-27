"use client";

import { useEffect } from 'react';
import { useAnalysisStore } from '@/store/analysisStore';
import { useAnalysisWebSocket } from '@/hooks/useAnalysisWebSocket';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import { AnalysisForm } from '@/components/analysis/AnalysisForm';
import { AnalysisProgressCard } from '@/components/analysis/AnalysisProgressCard';
import { RecentAnalyses } from '@/components/dashboard/RecentAnalyses';
import { LoaderIcon } from '@/components/icons';
import { useQueryClient } from '@tanstack/react-query';
import { useTranslation } from '@/i18n/TranslationProvider';

export default function AnalysisPage() {
  const queryClient = useQueryClient();
  const { currentAnalysis, setHistory, analysisHistory } = useAnalysisStore();
  const { locale } = useTranslation();
  
  // WebSocket with auto-navigate enabled
  useAnalysisWebSocket(currentAnalysis?.id, {
    autoNavigate: true,
    onComplete: () => {
      // Refresh history when analysis completes
      queryClient.invalidateQueries({ queryKey: ['analysis', 'history'] });
    },
  });

  const historyQuery = useQuery({
    queryKey: ['analysis', 'history'],
    queryFn: async () => {
      const response = await api.get('/analyze/history?limit=10');
      return response.data.data;
    },
  });

  // Update store when data is fetched (replaces onSuccess)
  useEffect(() => {
    if (historyQuery.data) {
      setHistory(historyQuery.data);
    }
  }, [historyQuery.data, setHistory]);

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="grid gap-4 sm:gap-6 lg:grid-cols-2">
        <AnalysisForm />
        <AnalysisProgressCard />
      </div>

      {historyQuery.isLoading ? (
        <div className="rounded-2xl sm:rounded-3xl border border-slate-200 bg-white p-4 sm:p-6 text-center text-slate-500 text-sm sm:text-base">
          <LoaderIcon size={20} className="mr-2 inline" /> {locale === 'tr' ? 'Geçmiş yükleniyor...' : 'Fetching history...'}
        </div>
      ) : (
        <RecentAnalyses analyses={analysisHistory} />
      )}
    </div>
  );
}
