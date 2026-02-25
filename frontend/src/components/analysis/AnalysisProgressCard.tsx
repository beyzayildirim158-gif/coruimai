import { useAnalysisStore } from '@/store/analysisStore';
import { LoaderIcon, AtomIcon } from '@/components/icons';
import { useMutation } from '@tanstack/react-query';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { useTranslation } from '@/i18n/TranslationProvider';

export function AnalysisProgressCard() {
  const { t } = useTranslation();
  const { currentAnalysis, setCurrentAnalysis, setIsAnalyzing } = useAnalysisStore();

  const cancelMutation = useMutation({
    mutationFn: async (analysisId: string) => {
      await api.post(`/analyze/cancel/${analysisId}`);
    },
    onSuccess: () => {
      toast.success(t('analysis.analysisCancelled'));
      setIsAnalyzing(false);
      setCurrentAnalysis(null);
    },
    onError: () => {
      toast.error(t('analysis.unableToCancel'));
    },
  });

  if (!currentAnalysis) {
    return (
      <div className="rounded-3xl border border-dashed border-slate-200 bg-white p-6 text-center text-slate-500">
        {t('analysis.awaitingLaunch')}
      </div>
    );
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center gap-3">
        <AtomIcon className="h-6 w-6 text-primary" />
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500">{t('analysis.liveRun')}</p>
          <h3 className="text-2xl font-semibold text-slate-900">@{currentAnalysis.username}</h3>
        </div>
      </div>

      <div className="mt-6">
        <div className="flex items-center justify-between text-sm text-slate-600">
          <span>{currentAnalysis.currentAgent ? `${t('analysis.agent')}: ${currentAnalysis.currentAgent}` : currentAnalysis.status}</span>
          <span>{currentAnalysis.progress}%</span>
        </div>
        <div className="mt-2 h-3 rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-primary"
            style={{ width: `${currentAnalysis.progress}%` }}
          />
        </div>
      </div>

      <div className="mt-6 flex flex-wrap gap-2 text-xs text-slate-600">
        {currentAnalysis.completedAgents.map((agent) => (
          <span
            key={agent}
            className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-slate-700"
          >
            {agent}
          </span>
        ))}
      </div>

      <button
        onClick={() => cancelMutation.mutate(currentAnalysis.id)}
        disabled={cancelMutation.isPending}
        className="mt-6 flex w-full items-center justify-center rounded-2xl border border-slate-200 px-4 py-3 text-sm text-slate-600 hover:bg-slate-50 disabled:cursor-not-allowed"
      >
        {cancelMutation.isPending ? <LoaderIcon className="mr-2 h-4 w-4 animate-spin" /> : t('analysis.cancelAnalysis')}
      </button>
    </div>
  );
}
