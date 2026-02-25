"use client";

import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import { useAuthStore } from '@/store/authStore';
import { LoaderIcon, SaveIcon, InstagramIcon, TrashIcon, KeyIcon, EyeIcon, EyeOffIcon, RefreshIcon, GlobeIcon } from '@/components/icons';
import toast from 'react-hot-toast';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useTranslation } from '@/i18n/TranslationProvider';

const schema = z.object({
  name: z.string().min(2, 'Name required'),
  avatarUrl: z
    .string()
    .url('Must be a valid URL')
    .or(z.literal(''))
    .optional(),
});

const passwordSchema = z.object({
  currentPassword: z.string().min(1, 'Current password required'),
  newPassword: z
    .string()
    .min(8, 'Password must be 8+ chars')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, 'Must include upper, lower, number'),
  confirmPassword: z.string().min(1, 'Confirm your new password'),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type ProfileFormValues = z.infer<typeof schema>;
type PasswordFormValues = z.infer<typeof passwordSchema>;

export default function SettingsPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user, setUser, logout } = useAuthStore();
  const { t, locale, setLocale } = useTranslation();
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);

  const profileQuery = useQuery({
    queryKey: ['user', 'profile'],
    queryFn: async () => {
      const response = await api.get('/users/profile');
      return response.data.data;
    },
    initialData: user ?? undefined,
  });

  const accountsQuery = useQuery({
    queryKey: ['user', 'accounts'],
    queryFn: async () => {
      const response = await api.get('/users/accounts');
      return response.data.data;
    },
  });

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<ProfileFormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      name: profileQuery.data?.name ?? '',
      avatarUrl: profileQuery.data?.avatarUrl ?? '',
    },
  });

  useEffect(() => {
    if (profileQuery.data) {
      reset({
        name: profileQuery.data.name ?? '',
        avatarUrl: profileQuery.data.avatarUrl ?? '',
      });
    }
  }, [profileQuery.data, reset]);

  const updateMutation = useMutation({
    mutationFn: async (values: ProfileFormValues) => {
      const payload = { ...values, avatarUrl: values.avatarUrl || null };
      const response = await api.patch('/users/profile', payload);
      return response.data.data;
    },
    onSuccess: (data) => {
      toast.success('Profile updated');
      setUser(data);
      queryClient.invalidateQueries({ queryKey: ['user', 'profile'] });
    },
    onError: () => toast.error('Unable to update profile'),
  });

  // Password change form
  const {
    register: registerPassword,
    handleSubmit: handlePasswordSubmit,
    formState: { errors: passwordErrors },
    reset: resetPassword,
  } = useForm<PasswordFormValues>({
    resolver: zodResolver(passwordSchema),
    defaultValues: {
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
    },
  });

  const passwordMutation = useMutation({
    mutationFn: async (values: PasswordFormValues) => {
      await api.post('/auth/change-password', {
        currentPassword: values.currentPassword,
        newPassword: values.newPassword,
      });
    },
    onSuccess: () => {
      toast.success('Password changed successfully');
      resetPassword();
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.message || 'Failed to change password');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async () => {
      await api.delete('/users/delete');
    },
    onSuccess: async () => {
      toast.success('Account deleted');
      await logout();
      router.replace('/register');
    },
    onError: () => toast.error('Failed to delete account'),
  });

  const onSubmit = (values: ProfileFormValues) => updateMutation.mutate(values);

  return (
    <div className="space-y-6">
      {/* Language Settings */}
      <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
        <div className="flex items-center gap-3">
          <GlobeIcon size={20} className="text-primary-500" />
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">{t('settings.language')}</p>
            <h2 className="text-2xl font-semibold text-slate-900">{t('settings.selectLanguage')}</h2>
          </div>
        </div>
        <div className="mt-6 flex gap-4">
          <button
            onClick={() => setLocale('en')}
            className={`flex items-center gap-3 rounded-2xl border px-6 py-4 transition-all ${
              locale === 'en'
                ? 'border-primary-500 bg-primary-50 text-slate-900'
                : 'border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100'
            }`}
          >
            <span className="text-2xl">🇬🇧</span>
            <div className="text-left">
              <p className="font-semibold">English</p>
              <p className="text-xs text-slate-500">English (US)</p>
            </div>
          </button>
          <button
            onClick={() => setLocale('tr')}
            className={`flex items-center gap-3 rounded-2xl border px-6 py-4 transition-all ${
              locale === 'tr'
                ? 'border-primary-500 bg-primary-50 text-slate-900'
                : 'border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100'
            }`}
          >
            <span className="text-2xl">🇹🇷</span>
            <div className="text-left">
              <p className="font-semibold">Türkçe</p>
              <p className="text-xs text-slate-500">Turkish</p>
            </div>
          </button>
        </div>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">{t('common.profile')}</p>
        <h1 className="text-3xl font-semibold text-slate-900">Command center settings</h1>
        <form onSubmit={handleSubmit(onSubmit)} className="mt-6 space-y-4">
          <div>
            <label className="text-sm text-slate-600">Name</label>
            <input
              {...register('name')}
              className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 focus:border-primary-400 focus:outline-none focus:ring-2 focus:ring-primary-100"
              placeholder="Agent name"
            />
            {errors.name && <p className="mt-1 text-xs text-red-600">{errors.name.message}</p>}
          </div>
          <div>
            <label className="text-sm text-slate-300">Avatar URL</label>
            <input
              {...register('avatarUrl')}
              className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white focus:border-purple-400 focus:outline-none"
              placeholder="https://..."
            />
            {errors.avatarUrl && <p className="mt-1 text-xs text-rose-300">{errors.avatarUrl.message}</p>}
          </div>
          <button
            type="submit"
            disabled={isSubmitting || updateMutation.isPending}
            className="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-purple-600 to-pink-500 px-6 py-3 text-sm font-semibold uppercase tracking-[0.2em] disabled:opacity-50"
          >
            {updateMutation.isPending ? <LoaderIcon size={16} /> : <SaveIcon size={16} />}
            Save profile
          </button>
        </form>
      </div>

      {/* Password Change Section */}
      <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
        <div className="flex items-center gap-3">
          <KeyIcon size={20} className="text-primary-500" />
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Security</p>
            <h2 className="text-2xl font-semibold text-slate-900">Change password</h2>
          </div>
        </div>
        <form onSubmit={handlePasswordSubmit((values) => passwordMutation.mutate(values))} className="mt-6 space-y-4">
          <div>
            <label className="text-sm text-slate-600">Current password</label>
            <div className="relative mt-2">
              <input
                type={showCurrentPassword ? 'text' : 'password'}
                {...registerPassword('currentPassword')}
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 pr-12 text-slate-900 focus:border-primary-400 focus:outline-none focus:ring-2 focus:ring-primary-100"
                placeholder="••••••••"
              />
              <button
                type="button"
                onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                {showCurrentPassword ? <EyeOffIcon size={16} /> : <EyeIcon size={16} />}
              </button>
            </div>
            {passwordErrors.currentPassword && <p className="mt-1 text-xs text-red-600">{passwordErrors.currentPassword.message}</p>}
          </div>
          <div>
            <label className="text-sm text-slate-600">New password</label>
            <div className="relative mt-2">
              <input
                type={showNewPassword ? 'text' : 'password'}
                {...registerPassword('newPassword')}
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 pr-12 text-slate-900 focus:border-primary-400 focus:outline-none focus:ring-2 focus:ring-primary-100"
                placeholder="••••••••"
              />
              <button
                type="button"
                onClick={() => setShowNewPassword(!showNewPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                {showNewPassword ? <EyeOffIcon size={16} /> : <EyeIcon size={16} />}
              </button>
            </div>
            {passwordErrors.newPassword && <p className="mt-1 text-xs text-red-600">{passwordErrors.newPassword.message}</p>}
          </div>
          <div>
            <label className="text-sm text-slate-600">Confirm new password</label>
            <input
              type="password"
              {...registerPassword('confirmPassword')}
              className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 focus:border-primary-400 focus:outline-none focus:ring-2 focus:ring-primary-100"
              placeholder="••••••••"
            />
            {passwordErrors.confirmPassword && <p className="mt-1 text-xs text-red-600">{passwordErrors.confirmPassword.message}</p>}
          </div>
          <button
            type="submit"
            disabled={passwordMutation.isPending}
            className="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-slate-50 px-6 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-100 disabled:opacity-50"
          >
            {passwordMutation.isPending ? <LoaderIcon size={16} /> : <RefreshIcon size={16} />}
            Update password
          </button>
        </form>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Instagram accounts</p>
            <h2 className="text-2xl font-semibold text-slate-900">Connected targets</h2>
          </div>
          <span className="rounded-full border border-slate-200 bg-slate-50 px-4 py-1 text-xs text-slate-600">
            {accountsQuery.data?.length ?? 0} tracked
          </span>
        </div>
        <div className="mt-4 space-y-3">
          {accountsQuery.isLoading && (
            <div className="flex items-center gap-2 text-slate-500">
              <LoaderIcon size={16} /> Loading accounts...
            </div>
          )}
          {!accountsQuery.isLoading && (accountsQuery.data?.length ?? 0) === 0 && (
            <div className="text-center py-6">
              <p className="text-sm text-slate-500 mb-3">No Instagram accounts analyzed yet.</p>
              <Link 
                href="/analysis"
                className="inline-flex items-center gap-2 rounded-2xl border border-primary-200 bg-primary-50 px-4 py-2 text-sm text-primary-700 hover:bg-primary-100"
              >
                Launch your first analysis
              </Link>
            </div>
          )}
          {accountsQuery.data?.map((account: any) => (
            <div key={account.id} className="flex items-center justify-between rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-primary-500 to-primary-600 text-white">
                  <InstagramIcon size={20} />
                </div>
                <div>
                  <p className="font-semibold text-slate-900">@{account.username}</p>
                  <p className="text-xs text-slate-500">{account.followers?.toLocaleString()} followers</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-slate-500">
                  {account.lastAnalyzedAt
                    ? new Date(account.lastAnalyzedAt).toLocaleDateString()
                    : 'never'}
                </span>
                <Link
                  href={`/analysis?username=${account.username}`}
                  className="rounded-xl border border-slate-200 bg-white px-3 py-1 text-xs text-primary-600 hover:bg-slate-50"
                >
                  Re-analyze
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-3xl border border-red-200 bg-red-50 p-6 text-slate-900">
        <p className="text-sm uppercase tracking-[0.3em] text-red-600">Danger zone</p>
        <h2 className="mt-2 text-2xl font-semibold text-slate-900">Delete workspace</h2>
        <p className="text-sm text-red-700">
          This will permanently delete your account, analyses, and reports. This action cannot be undone.
        </p>
        <button
          onClick={() => {
            if (confirm('This will permanently delete your account. Continue?')) {
              deleteMutation.mutate();
            }
          }}
          className="mt-4 inline-flex items-center gap-2 rounded-2xl border border-red-300 bg-red-100 px-6 py-3 text-sm text-red-700 hover:bg-red-200"
          disabled={deleteMutation.isPending}
        >
          {deleteMutation.isPending ? <LoaderIcon size={16} /> : <TrashIcon size={16} />}
          Delete account
        </button>
      </div>
    </div>
  );
}
