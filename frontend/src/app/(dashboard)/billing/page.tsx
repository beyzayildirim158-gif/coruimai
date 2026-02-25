"use client";

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import api from '@/lib/api';
import { InvoiceTable } from '@/components/billing/InvoiceTable';
import { CheckIcon, LoaderIcon, CreditCardIcon, ShieldCheckIcon } from '@/components/icons';
import toast from 'react-hot-toast';
import clsx from 'clsx';

const plans = [
  {
    tier: 'STARTER',
    price: '$99',
    description: 'Solo creators validating ideas',
    features: ['10 analyses / month', '3 AI agents', 'Basic PDF reports', 'Email support'],
  },
  {
    tier: 'PROFESSIONAL',
    price: '$199',
    description: 'Growing creators needing scale',
    features: ['50 analyses / month', '5 AI agents', 'Advanced reports', 'Priority support', 'API access'],
    featured: true,
  },
  {
    tier: 'PREMIUM',
    price: '$299',
    description: 'Agencies and power users',
    features: ['200 analyses / month', 'All 7 agents', 'White-label exports', '24/7 support'],
  },
  {
    tier: 'ENTERPRISE',
    price: '$499',
    description: 'Custom workflows & SLAs',
    features: ['Unlimited analyses', 'Custom agents', 'Dedicated success', 'Multi-seat workspaces'],
  },
];

export default function BillingPage() {
  const queryClient = useQueryClient();

  const subscriptionQuery = useQuery({
    queryKey: ['payments', 'subscription'],
    queryFn: async () => {
      const response = await api.get('/payments/subscription');
      return response.data.data;
    },
  });

  const invoicesQuery = useQuery({
    queryKey: ['payments', 'invoices'],
    queryFn: async () => {
      const response = await api.get('/payments/invoices');
      return response.data.data;
    },
  });

  const checkoutMutation = useMutation({
    mutationFn: async (tier: string) => {
      const response = await api.post('/payments/create-checkout', { tier });
      return response.data.data;
    },
    onSuccess: (data) => {
      toast.success('Redirecting to Stripe checkout');
      window.location.href = data.checkoutUrl;
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.message || 'Unable to start checkout');
    },
  });

  const portalMutation = useMutation({
    mutationFn: async () => {
      const response = await api.get('/payments/portal');
      return response.data.data.portalUrl;
    },
    onSuccess: (url) => {
      window.location.href = url;
    },
    onError: () => toast.error('Unable to open billing portal'),
  });

  const cancelMutation = useMutation({
    mutationFn: async () => {
      await api.post('/payments/cancel');
    },
    onSuccess: () => {
      toast.success('Subscription will be cancelled at period end');
      queryClient.invalidateQueries({ queryKey: ['payments', 'subscription'] });
    },
    onError: () => toast.error('Unable to cancel subscription'),
  });

  const resumeMutation = useMutation({
    mutationFn: async () => {
      await api.post('/payments/resume');
    },
    onSuccess: () => {
      toast.success('Subscription resumed');
      queryClient.invalidateQueries({ queryKey: ['payments', 'subscription'] });
    },
    onError: () => toast.error('Unable to resume subscription'),
  });

  const activeTier = subscriptionQuery.data?.tier;
  const cancelAtPeriodEnd = subscriptionQuery.data?.subscription?.cancelAtPeriodEnd;

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 text-slate-900 shadow-sm">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Current subscription</p>
            <h1 className="text-3xl font-semibold text-slate-900">{activeTier ?? 'STARTER'} plan</h1>
            <p className="text-sm text-slate-500">
              Status: {subscriptionQuery.data?.status ?? 'TRIALING'} · Next invoice{' '}
              {subscriptionQuery.data?.subscription?.currentPeriodEnd
                ? new Date(subscriptionQuery.data.subscription.currentPeriodEnd).toLocaleDateString()
                : '—'}
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => portalMutation.mutate()}
              disabled={portalMutation.isPending}
              className="inline-flex items-center gap-2 rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 disabled:opacity-50"
            >
              {portalMutation.isPending ? <LoaderIcon size={16} /> : <CreditCardIcon size={16} />}
              Billing portal
            </button>
            {cancelAtPeriodEnd ? (
              <button
                onClick={() => resumeMutation.mutate()}
                disabled={resumeMutation.isPending}
                className="inline-flex items-center gap-2 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm text-emerald-700"
              >
                {resumeMutation.isPending ? <LoaderIcon size={16} /> : <ShieldCheckIcon size={16} />}
                Resume plan
              </button>
            ) : (
              <button
                onClick={() => cancelMutation.mutate()}
                disabled={cancelMutation.isPending}
                className="inline-flex items-center gap-2 rounded-2xl border border-red-200 bg-red-50 px-4 py-2 text-sm text-red-600"
              >
                {cancelMutation.isPending ? <LoaderIcon size={16} /> : null}
                Cancel at renewal
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {plans.map((plan) => (
          <div
            key={plan.tier}
            className={clsx(
              'rounded-3xl border p-6 text-slate-900 shadow-sm',
              plan.featured
                ? 'border-primary-300 bg-gradient-to-b from-primary-50 to-white'
                : 'border-slate-200 bg-white'
            )}
          >
            <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{plan.tier}</p>
            <div className="mt-1 text-4xl font-semibold text-slate-900">{plan.price}</div>
            <p className="text-sm text-slate-600">{plan.description}</p>
            <ul className="mt-4 space-y-2 text-sm text-slate-700">
              {plan.features.map((feature) => (
                <li key={feature} className="flex items-center gap-2">
                  <CheckIcon size={16} className="text-emerald-600" /> {feature}
                </li>
              ))}
            </ul>
            <button
              onClick={() => checkoutMutation.mutate(plan.tier)}
              disabled={checkoutMutation.isPending}
              className={clsx(
                'mt-5 w-full rounded-2xl px-4 py-3 text-sm font-semibold uppercase tracking-[0.2em]',
                activeTier === plan.tier
                  ? 'border border-emerald-300 bg-emerald-50 text-emerald-700'
                  : 'bg-primary-600 text-white hover:bg-primary-700'
              )}
            >
              {activeTier === plan.tier ? 'Active plan' : 'Upgrade'}
            </button>
          </div>
        ))}
      </div>

      <div>
        <h2 className="mb-3 text-xl font-semibold text-slate-900">Payment history</h2>
        <InvoiceTable invoices={invoicesQuery.data} />
      </div>
    </div>
  );
}
