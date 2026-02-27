"use client";

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import api from '@/lib/api';
import { useAnalysisStore } from '@/store/analysisStore';
import { LoaderIcon, RadarIcon, ShieldIcon, InfoIcon, ChevronDownIcon, ChevronUpIcon, KeyIcon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

const schema = z.object({
  username: z
    .string()
    .min(1, 'Username required')
    .regex(/^[A-Za-z0-9._]+$/, 'Only Instagram-safe characters'),
  mode: z.enum(['public', 'authenticated']).default('public'),
  instagramUsername: z.string().optional(),
  instagramPassword: z.string().optional(),
}).refine((data) => {
  // If authenticated mode, require both username and password
  if (data.mode === 'authenticated') {
    return data.instagramUsername && data.instagramPassword;
  }
  return true;
}, {
  message: 'Instagram kullanıcı adı ve şifre gerekli',
  path: ['instagramUsername'],
});

type AnalysisFormValues = z.infer<typeof schema>;

export function AnalysisForm() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const setCurrentAnalysis = useAnalysisStore((state) => state.setCurrentAnalysis);
  const setIsAnalyzing = useAnalysisStore((state) => state.setIsAnalyzing);
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    reset,
  } = useForm<AnalysisFormValues>({
    resolver: zodResolver(schema),
    defaultValues: { username: '', mode: 'public', instagramUsername: '', instagramPassword: '' },
  });

  const selectedMode = watch('mode');

  const mutation = useMutation({
    mutationFn: async (values: AnalysisFormValues) => {
      const payload: any = { 
        username: values.username,
        mode: values.mode,
      };
      
      // Add login credentials for authenticated mode
      if (values.mode === 'authenticated' && values.instagramUsername && values.instagramPassword) {
        payload.instagramCredentials = {
          username: values.instagramUsername,
          password: values.instagramPassword,
        };
      }
      
      const response = await api.post('/analyze/start', payload);
      return response.data.data;
    },
    onSuccess: (data) => {
      toast.success(`${t('analysis.analysisLaunched')} @${data.account.username}`);
      setCurrentAnalysis({
        id: data.analysisId,
        username: data.account.username,
        status: 'PENDING',
        progress: 0,
        currentAgent: data.agents[0],
        completedAgents: [],
        createdAt: new Date().toISOString(),
        account: data.account,
      });
      setIsAnalyzing(true);
      queryClient.invalidateQueries({ queryKey: ['analysis', 'history'] });
      reset();
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.message || t('analysis.unableToStart'));
    },
  });

  const onSubmit = (values: AnalysisFormValues) => mutation.mutate(values);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="rounded-2xl sm:rounded-3xl border border-slate-200 bg-white p-4 sm:p-6 shadow-sm">
      <div className="flex items-center gap-2 text-xs sm:text-sm uppercase tracking-[0.2em] sm:tracking-[0.3em] text-slate-500">
        <RadarIcon className="h-4 w-4 text-primary" /> {t('analysis.launchNew')}
      </div>
      <h3 className="mt-2 sm:mt-3 text-xl sm:text-2xl font-semibold text-slate-900">{t('analysis.targetHandle')}</h3>
      <p className="text-xs sm:text-sm text-slate-500">{t('analysis.pullRealtime')}</p>

      <div className="mt-4 sm:mt-5 space-y-3">
        <div>
          <label className="text-xs sm:text-sm text-slate-700">{t('analysis.instagramUsername')}</label>
          <div className="mt-1.5 sm:mt-2 flex gap-2">
            <span className="flex items-center rounded-xl sm:rounded-2xl border border-slate-200 bg-slate-50 px-3 sm:px-4 text-sm sm:text-base text-slate-500">@</span>
            <input
              type="text"
              {...register('username')}
              className="w-full rounded-xl sm:rounded-2xl border border-slate-200 bg-slate-50 px-3 sm:px-4 py-2.5 sm:py-3 text-sm sm:text-base text-slate-900 placeholder:text-slate-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder={t('analysis.usernamePlaceholder')}
            />
          </div>
          {errors.username && <p className="mt-1 text-xs text-warning">{errors.username.message}</p>}
        </div>

        {/* Advanced Options Toggle */}
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex w-full items-center justify-between rounded-xl sm:rounded-2xl border border-slate-200 bg-slate-50 px-3 sm:px-4 py-2.5 sm:py-3 text-xs sm:text-sm text-slate-600 hover:bg-slate-100 transition"
        >
          <span className="flex items-center gap-2">
            <KeyIcon className="h-4 w-4" />
            {t('analysis.advancedOptions') || 'Gelişmiş Seçenekler (Instagram Session)'}
          </span>
          {showAdvanced ? <ChevronUpIcon className="h-4 w-4" /> : <ChevronDownIcon className="h-4 w-4" />}
        </button>

        {/* Advanced Options Panel */}
        {showAdvanced && (
          <div className="space-y-4 rounded-2xl border border-slate-200 bg-slate-50 p-4">
            {/* Analysis Mode Selection */}
            <div>
              <label className="text-sm font-medium text-slate-700">{t('analysis.analysisMode') || 'Analiz Modu'}</label>
              <div className="mt-2 grid grid-cols-2 gap-2">
                <label className={`flex cursor-pointer items-center gap-2 rounded-xl border p-3 transition ${selectedMode === 'public' ? 'border-primary bg-primary/5' : 'border-slate-200 bg-white hover:bg-slate-50'}`}>
                  <input type="radio" value="public" {...register('mode')} className="hidden" />
                  <ShieldIcon className={`h-4 w-4 ${selectedMode === 'public' ? 'text-primary' : 'text-slate-400'}`} />
                  <div>
                    <p className="text-sm font-medium text-slate-900">{t('analysis.publicMode') || 'Herkese Açık'}</p>
                    <p className="text-xs text-slate-500">{t('analysis.publicModeDesc') || 'Sadece genel veriler'}</p>
                  </div>
                </label>
                <label className={`flex cursor-pointer items-center gap-2 rounded-xl border p-3 transition ${selectedMode === 'authenticated' ? 'border-primary bg-primary/5' : 'border-slate-200 bg-white hover:bg-slate-50'}`}>
                  <input type="radio" value="authenticated" {...register('mode')} className="hidden" />
                  <KeyIcon className={`h-4 w-4 ${selectedMode === 'authenticated' ? 'text-primary' : 'text-slate-400'}`} />
                  <div>
                    <p className="text-sm font-medium text-slate-900">{t('analysis.authenticatedMode') || 'Oturum ile'}</p>
                    <p className="text-xs text-slate-500">{t('analysis.authenticatedModeDesc') || 'Özel veriler dahil'}</p>
                  </div>
                </label>
              </div>
            </div>

            {/* Login Fields (shown only in authenticated mode) */}
            {selectedMode === 'authenticated' && (
              <div className="space-y-3">
                <div className="flex items-start gap-2 rounded-xl bg-amber-50 p-3 text-sm text-amber-800">
                  <InfoIcon className="mt-0.5 h-4 w-4 flex-shrink-0" />
                  <p>
                    {t('analysis.loginInfo') || 'Kendi Instagram hesabınızla giriş yaparak özel verilere erişebilir ve daha detaylı analiz alabilirsiniz. Şifreniz sadece giriş için kullanılır ve saklanmaz.'}
                  </p>
                </div>
                <div className="flex items-start gap-2 rounded-xl bg-blue-50 p-3 text-sm text-blue-800">
                  <ShieldIcon className="mt-0.5 h-4 w-4 flex-shrink-0" />
                  <p>
                    {t('analysis.securityNote') || 'Güvenliğiniz için: Şifreniz şifrelenerek gönderilir ve işlem sonrası hemen silinir.'}
                  </p>
                </div>
                <div>
                  <label className="text-sm text-slate-700">{t('analysis.instagramUsernameLabel') || 'Instagram Kullanıcı Adı'}</label>
                  <input
                    type="text"
                    {...register('instagramUsername')}
                    className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                    placeholder={t('analysis.instagramUsernamePlaceholder') || 'kullanici_adi'}
                  />
                  {errors.instagramUsername && <p className="mt-1 text-xs text-warning">{errors.instagramUsername.message}</p>}
                </div>
                <div>
                  <label className="text-sm text-slate-700">{t('analysis.instagramPasswordLabel') || 'Instagram Şifre'}</label>
                  <input
                    type="password"
                    {...register('instagramPassword')}
                    className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                    placeholder="••••••••"
                  />
                </div>
              </div>
            )}
          </div>
        )}

        <button
          type="submit"
          disabled={mutation.isPending}
          className="flex w-full items-center justify-center rounded-xl sm:rounded-2xl bg-primary px-4 py-2.5 sm:py-3 text-base sm:text-lg font-semibold text-white transition hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {mutation.isPending ? (
            <>
              <LoaderIcon className="mr-2 h-5 w-5 animate-spin" /> {t('analysis.contactingAgents')}
            </>
          ) : (
            t('analysis.launchMultiAgent')
          )}
        </button>
      </div>
    </form>
  );
}
