"use client";

import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { LoaderIcon, SparkIcon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

const loginSchema = z.object({
  email: z.string().email('Valid email required'),
  password: z.string().min(1, 'Password required'),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const { login, isLoading } = useAuthStore();
  const { t, locale } = useTranslation();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = async (values: LoginForm) => {
    try {
      await login(values.email, values.password);
      toast.success(locale === 'tr' ? 'Tekrar hoş geldiniz, stratejist' : 'Welcome back, strategist');
      router.replace('/dashboard');
    } catch (error: any) {
      toast.error(error?.response?.data?.message || (locale === 'tr' ? 'Giriş başarısız' : 'Login failed'));
    }
  };

  return (
    <div className="flex w-full max-w-5xl flex-col gap-10 lg:flex-row">
      <div className="flex flex-1 flex-col justify-center rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex items-center gap-3 text-sm uppercase tracking-[0.3em] text-primary">
          <SparkIcon size={20} />
          corium.ai {locale === 'tr' ? 'İstihbarat Platformu' : 'Intelligence Platform'}
        </div>
        <h1 className="mt-6 text-4xl font-bold text-slate-900">
          {locale === 'tr' ? 'Analiz panonuza giriş yapın' : 'Sign in to your analytics dashboard'}
        </h1>
        <p className="mt-3 max-w-md text-slate-600">
          {locale === 'tr'
            ? '7 ajanlı komuta merkezine erişin, canlı analizleri izleyin ve kapsamlı PDF istihbarat raporları oluşturun.'
            : 'Access the 7-agent command center, monitor live analyses, and generate comprehensive PDF intelligence reports.'}
        </p>
        <div className="mt-10 grid gap-4 text-sm text-slate-600">
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-trust">{locale === 'tr' ? 'Canlı sinyal' : 'Live signal'}</p>
            <p className="mt-2 text-lg text-slate-900">
              {locale === 'tr' ? 'AI çoklu ajan grafiği hazır bekliyor.' : 'AI multi-agent graph standing by.'}
            </p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-trust">{locale === 'tr' ? 'Güvenlik' : 'Security'}</p>
            <p className="mt-2 text-lg text-slate-900">
              {locale === 'tr'
                ? 'Sıfır güven erişimi · Şifrelenmiş tokenlar · Denetim hazır.'
                : 'Zero-trust access · Encrypted tokens · Audit-ready.'}
            </p>
          </div>
        </div>
      </div>

      <div className="flex flex-1 flex-col gap-6 rounded-3xl border border-slate-200 bg-white p-8 shadow-lg">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">{locale === 'tr' ? 'Kimlik doğrula' : 'Authenticate'}</p>
          <h2 className="mt-2 text-3xl font-semibold text-slate-900">{t('dashboard.welcome')}</h2>
          <p className="text-sm text-slate-500">
            {locale === 'tr' ? 'E-posta ve şifrenizle giriş yapın.' : 'Use your email and password to sign in.'}
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
          <div>
            <label htmlFor="email" className="text-sm text-slate-700">{t('auth.email')}</label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              {...register('email')}
              className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="you@company.com"
            />
            {errors.email && <p className="mt-1 text-xs text-warning">{errors.email.message}</p>}
          </div>
          <div>
            <label htmlFor="password" className="text-sm text-slate-700">{t('auth.password')}</label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              {...register('password')}
              className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="••••••••"
            />
            {errors.password && <p className="mt-1 text-xs text-warning">{errors.password.message}</p>}
          </div>

          <div className="flex items-center justify-between text-sm">
            <label htmlFor="remember-device" className="flex items-center gap-2 text-slate-500">
              <input id="remember-device" type="checkbox" className="rounded border-slate-300 bg-white text-primary focus:ring-primary" />
              {locale === 'tr' ? 'Cihazı hatırla' : 'Remember device'}
            </label>
            <Link href="/forgot-password" className="text-primary hover:text-primary/80">
              {t('auth.forgotPassword')}
            </Link>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="flex w-full items-center justify-center rounded-2xl bg-primary px-4 py-3 text-lg font-semibold text-white transition-all hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? (
              <>
                <LoaderIcon size={20} className="mr-2" /> {locale === 'tr' ? 'Doğrulanıyor...' : 'Authenticating...'}
              </>
            ) : (
              t('auth.login')
            )}
          </button>
        </form>

        <p className="text-center text-sm text-slate-500">
          {t('auth.noAccount')}{' '}
          <Link href="/register" className="text-primary font-medium">
            {t('auth.register')}
          </Link>
        </p>
      </div>
    </div>
  );
}
