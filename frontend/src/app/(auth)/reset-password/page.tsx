"use client";

import { useState, Suspense } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { LoaderIcon, KeyRoundIcon, CheckCircle2Icon } from '@/components/icons';
import Link from 'next/link';
import { useSearchParams, useRouter } from 'next/navigation';

const resetSchema = z.object({
  password: z
    .string()
    .min(8, 'Password must be 8+ chars')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, 'Must include upper, lower, number'),
  confirmPassword: z.string().min(1, 'Confirm your password'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type ResetForm = z.infer<typeof resetSchema>;

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const [isSuccess, setIsSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ResetForm>({
    resolver: zodResolver(resetSchema),
    defaultValues: { password: '', confirmPassword: '' },
  });

  const onSubmit = async (values: ResetForm) => {
    if (!token) {
      toast.error('Invalid reset link');
      return;
    }
    
    try {
      await api.post('/auth/reset-password', {
        token,
        password: values.password,
      });
      setIsSuccess(true);
      toast.success('Password reset successful');
      setTimeout(() => router.push('/login'), 3000);
    } catch (error: any) {
      toast.error(error?.response?.data?.message || 'Failed to reset password');
    }
  };

  if (!token) {
    return (
      <div className="w-full max-w-3xl rounded-3xl border border-rose-400/30 bg-rose-500/10 p-10 text-white text-center">
        <h1 className="text-2xl font-semibold text-rose-200">Invalid Reset Link</h1>
        <p className="mt-2 text-sm text-rose-100">
          This password reset link is invalid or has expired.
        </p>
        <Link
          href="/forgot-password"
          className="mt-6 inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-purple-600 to-pink-500 px-6 py-3 text-sm font-semibold text-white"
        >
          Request a new link
        </Link>
      </div>
    );
  }

  if (isSuccess) {
    return (
      <div className="w-full max-w-3xl rounded-3xl border border-emerald-400/30 bg-emerald-500/10 p-10 text-white text-center">
        <CheckCircle2Icon size={48} className="mx-auto text-emerald-300" />
        <h1 className="mt-4 text-2xl font-semibold text-emerald-200">Password Reset Successful!</h1>
        <p className="mt-2 text-sm text-emerald-100">
          Your password has been changed. Redirecting to login...
        </p>
        <Link
          href="/login"
          className="mt-6 inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-purple-600 to-pink-500 px-6 py-3 text-sm font-semibold text-white"
        >
          Go to Login
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full max-w-3xl rounded-3xl border border-white/10 bg-slate-950/70 p-10 text-white">
      <div className="flex items-center gap-3 text-sm uppercase tracking-[0.3em] text-cyan-200">
        <KeyRoundIcon size={20} />
        New Password
      </div>
      <h1 className="mt-4 text-3xl font-semibold">Create a new password</h1>
      <p className="mt-2 text-sm text-slate-400">
        Enter your new password below. Make sure it's strong and unique.
      </p>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-4">
        <div>
          <label className="text-sm text-slate-200">New password</label>
          <input
            type="password"
            {...register('password')}
            className="mt-2 w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-slate-500 focus:border-purple-400 focus:outline-none"
            placeholder="••••••••"
          />
          {errors.password && <p className="mt-1 text-xs text-rose-400">{errors.password.message}</p>}
        </div>
        <div>
          <label className="text-sm text-slate-200">Confirm new password</label>
          <input
            type="password"
            {...register('confirmPassword')}
            className="mt-2 w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-slate-500 focus:border-purple-400 focus:outline-none"
            placeholder="••••••••"
          />
          {errors.confirmPassword && <p className="mt-1 text-xs text-rose-400">{errors.confirmPassword.message}</p>}
        </div>
        <button
          type="submit"
          disabled={isSubmitting}
          className="flex w-full items-center justify-center rounded-2xl bg-gradient-to-r from-purple-600 to-pink-500 px-4 py-3 font-semibold text-white transition hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? <LoaderIcon size={20} /> : 'Reset Password'}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate-400">
        Remembered your password? <Link href="/login" className="text-purple-300">Back to login</Link>
      </p>
    </div>
  );
}

function LoadingFallback() {
  return (
    <div className="w-full max-w-3xl rounded-3xl border border-white/10 bg-slate-950/70 p-10 text-white text-center">
      <LoaderIcon size={32} className="mx-auto text-purple-400" />
      <p className="mt-4 text-slate-400">Loading...</p>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <ResetPasswordForm />
    </Suspense>
  );
}
