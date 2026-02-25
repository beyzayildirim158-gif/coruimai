"use client";

import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { LoaderIcon, MailCheckIcon } from '@/components/icons';
import Link from 'next/link';

const forgotSchema = z.object({
  email: z.string().email('Valid email required'),
});

type ForgotForm = z.infer<typeof forgotSchema>;

export default function ForgotPasswordPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<ForgotForm>({
    resolver: zodResolver(forgotSchema),
    defaultValues: { email: '' },
  });

  const onSubmit = async (values: ForgotForm) => {
    try {
      await api.post('/auth/forgot-password', values);
      toast.success('If the account exists, a reset link is on its way.');
      reset();
    } catch (error: any) {
      toast.error(error?.response?.data?.message || 'Failed to send reset email');
    }
  };

  return (
    <div className="w-full max-w-3xl rounded-3xl border border-white/10 bg-slate-950/70 p-10 text-white">
      <div className="flex items-center gap-3 text-sm uppercase tracking-[0.3em] text-cyan-200">
        <MailCheckIcon size={20} />
        Reset Credentials
      </div>
      <h1 className="mt-4 text-3xl font-semibold">Send a secure reset link</h1>
      <p className="mt-2 text-sm text-slate-400">
        We will email you a time-limited link to create a new password. For security, the system never reveals if an email exists.
      </p>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-4">
        <div>
          <label className="text-sm text-slate-200">Email address</label>
          <input
            type="email"
            {...register('email')}
            className="mt-2 w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder:text-slate-500 focus:border-purple-400 focus:outline-none"
            placeholder="you@agency.com"
          />
          {errors.email && <p className="mt-1 text-xs text-rose-400">{errors.email.message}</p>}
        </div>
        <button
          type="submit"
          disabled={isSubmitting}
          className="flex items-center justify-center rounded-2xl bg-gradient-to-r from-purple-600 to-pink-500 px-4 py-3 font-semibold text-white transition hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? <LoaderIcon size={20} /> : 'Send reset link'}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate-400">
        Remembered it? <Link href="/login" className="text-purple-300">Back to login</Link>
      </p>
    </div>
  );
}
