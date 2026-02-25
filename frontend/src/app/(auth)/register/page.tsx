"use client";

import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { LoaderIcon, RadarIcon } from '@/components/icons';

const registerSchema = z.object({
  name: z.string().min(2, 'Name required'),
  email: z.string().email('Valid email required'),
  password: z
    .string()
    .min(8, 'Password must be 8+ chars')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, 'Must include upper, lower, number'),
});

type RegisterForm = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const router = useRouter();
  const { register: registerUser, isLoading } = useAuthStore();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: '',
      email: '',
      password: '',
    },
  });

  const onSubmit = async (values: RegisterForm) => {
    try {
      await registerUser(values);
      toast.success('Workspace initialized. Verify your email.');
      router.replace('/dashboard');
    } catch (error: any) {
      toast.error(error?.response?.data?.message || 'Registration failed');
    }
  };

  return (
    <div className="flex w-full max-w-5xl flex-col gap-10 lg:flex-row">
      <div className="flex flex-1 flex-col gap-6 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex items-center gap-3 text-sm uppercase tracking-[0.3em] text-primary">
          <RadarIcon size={20} />
          corium.ai Platform
        </div>
        <h1 className="text-4xl font-bold text-slate-900">Launch your AI analytics stack</h1>
        <p className="max-w-md text-slate-600">
          Deploy a multi-agent Instagram intelligence suite with authenticated API access, billing integration, and comprehensive PDF reporting.
        </p>
        <ul className="space-y-3 text-sm text-slate-700">
          <li className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-primary" /> 7 AI specialists orchestrated via FastAPI
          </li>
          <li className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-trust" /> Live Instagram data via Apify + bot detection
          </li>
          <li className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-primary" /> Stripe-native billing with tiered plans
          </li>
        </ul>
        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
          <p className="text-xs uppercase tracking-[0.2em] text-trust">What you get</p>
          <p className="mt-2 text-slate-900">
            Real-time analysis dashboard, PDF intelligence reports, and API/webhook access out of the box.
          </p>
        </div>
      </div>

      <div className="flex flex-1 flex-col gap-5 rounded-3xl border border-slate-200 bg-white p-8 shadow-lg">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Create access</p>
          <h2 className="mt-2 text-3xl font-semibold text-slate-900">Get started with corium.ai</h2>
        </div>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="text-sm text-slate-700">Full name</label>
            <input
              type="text"
              autoComplete="name"
              {...register('name')}
              className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="Your name"
            />
            {errors.name && <p className="mt-1 text-xs text-warning">{errors.name.message}</p>}
          </div>
          <div>
            <label className="text-sm text-slate-700">Email</label>
            <input
              type="email"
              autoComplete="email"
              {...register('email')}
              className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="you@company.com"
            />
            {errors.email && <p className="mt-1 text-xs text-warning">{errors.email.message}</p>}
          </div>
          <div>
            <label className="text-sm text-slate-700">Password</label>
            <input
              type="password"
              autoComplete="new-password"
              {...register('password')}
              className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              placeholder="••••••••"
            />
            {errors.password && <p className="mt-1 text-xs text-warning">{errors.password.message}</p>}
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="flex w-full items-center justify-center rounded-2xl bg-primary px-4 py-3 text-lg font-semibold text-white transition-all hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? (
              <>
                <LoaderIcon size={20} className="mr-2" /> Creating account...
              </>
            ) : (
              'Create Account'
            )}
          </button>
        </form>
        <p className="text-center text-sm text-slate-500">
          Already have an account?{' '}
          <Link href="/login" className="text-primary font-medium">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
