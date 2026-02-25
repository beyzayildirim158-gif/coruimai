import { ReactNode } from 'react';
import Link from 'next/link';
import clsx from 'clsx';

interface StatCardProps {
  label: string;
  value: string;
  helper?: string;
  icon?: ReactNode;
  change?: string;
  tone?: 'default' | 'success' | 'warning' | 'danger';
  href?: string;
}

const toneClasses: Record<Required<StatCardProps>['tone'], string> = {
  default: 'bg-white border-slate-200',
  success: 'bg-emerald-50 border-emerald-200',
  warning: 'bg-amber-50 border-amber-200',
  danger: 'bg-red-50 border-red-200',
};

export function StatCard({ label, value, helper, icon, change, tone = 'default', href }: StatCardProps) {
  const content = (
    <>
      <div className="flex items-center justify-between">
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">{label}</p>
        {icon && <div className="text-primary-500">{icon}</div>}
      </div>
      <p className="mt-3 text-4xl font-semibold text-slate-900">{value}</p>
      {helper && <p className="mt-2 text-sm text-slate-500">{helper}</p>}
      {change && <p className="mt-3 text-xs text-emerald-600">{change}</p>}
    </>
  );

  const classes = clsx(
    'rounded-3xl border p-5 text-slate-900 shadow-sm transition-all',
    toneClasses[tone],
    href && 'hover:border-primary-300 hover:shadow-md cursor-pointer'
  );

  if (href) {
    return (
      <Link href={href} className={classes}>
        {content}
      </Link>
    );
  }

  return <div className={classes}>{content}</div>;
}
