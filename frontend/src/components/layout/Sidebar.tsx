"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  HomeIcon,
  ActivityIcon,
  FileTextIcon,
  BarChart3Icon,
  CreditCardIcon,
  SettingsIcon,
  MagicWandIcon,
} from '@/components/icons';
import clsx from 'clsx';
import { useTranslation } from '@/i18n/TranslationProvider';

interface SidebarProps {
  isMobile?: boolean;
  onClose?: () => void;
}

export function Sidebar({ isMobile, onClose }: SidebarProps) {
  const pathname = usePathname();
  const { t } = useTranslation();

  const navItems = [
    { href: '/dashboard', label: t('nav.dashboard'), icon: HomeIcon },
    { href: '/analysis', label: t('nav.analysis'), icon: ActivityIcon },
    { href: '/reports', label: t('nav.reports'), icon: FileTextIcon },
    { href: '/usage', label: t('nav.usage'), icon: BarChart3Icon },
    { href: '/billing', label: t('nav.billing'), icon: CreditCardIcon },
    { href: '/settings', label: t('nav.settings'), icon: SettingsIcon },
  ];

  const handleNavClick = () => {
    if (isMobile && onClose) {
      onClose();
    }
  };

  // Mobile sidebar is rendered inside DashboardShell overlay
  if (isMobile) {
    return (
      <div className="flex flex-col h-full">
        <div className="mb-6 flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-white">
            <MagicWandIcon className="h-6 w-6" />
          </div>
          <div>
            <p className="text-lg font-bold text-slate-900">corium.ai</p>
            <p className="text-xs text-slate-500">Instagram Intelligence</p>
          </div>
        </div>

        <nav className="flex flex-1 flex-col gap-1">
          {navItems.map((item) => {
            const isActive = pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={handleNavClick}
                className={clsx(
                  'group flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition-all',
                  isActive
                    ? 'bg-primary/10 text-primary'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                )}
              >
                <Icon className={clsx('h-5 w-5', isActive ? 'text-primary' : 'text-slate-400')} />
                {item.label}
                {isActive && <span className="ml-auto h-2 w-2 rounded-full bg-primary" />}
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto rounded-2xl border border-slate-200 bg-gradient-to-br from-primary/5 to-trust/5 p-4">
          <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{t('dashboard.live')}</p>
          <h3 className="mt-2 text-lg font-semibold text-slate-900">{t('dashboard.realtimeAgents')}</h3>
          <p className="mt-1 text-sm text-slate-600">
            {t('dashboard.agentsReady')}
          </p>
        </div>
      </div>
    );
  }

  return (
    <aside className="relative hidden w-64 flex-col border-r border-slate-200 bg-white p-4 lg:flex">
      <div className="mb-10 flex items-center gap-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-white">
          <MagicWandIcon className="h-6 w-6" />
        </div>
        <div>
          <p className="text-lg font-bold text-slate-900">corium.ai</p>
          <p className="text-xs text-slate-500">Instagram Intelligence</p>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-1">
        {navItems.map((item) => {
          const isActive = pathname.startsWith(item.href);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                'group flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition-all',
                isActive
                  ? 'bg-primary/10 text-primary'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              )}
            >
              <Icon className={clsx('h-5 w-5', isActive ? 'text-primary' : 'text-slate-400')} />
              {item.label}
              {isActive && <span className="ml-auto h-2 w-2 rounded-full bg-primary" />}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto rounded-2xl border border-slate-200 bg-gradient-to-br from-primary/5 to-trust/5 p-4">
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{t('dashboard.live')}</p>
        <h3 className="mt-2 text-xl font-semibold text-slate-900">{t('dashboard.realtimeAgents')}</h3>
        <p className="mt-1 text-sm text-slate-600">
          {t('dashboard.agentsReadyFull')}
        </p>
        <div className="mt-4 flex items-center gap-2 text-xs text-slate-500">
          <ActivityIcon className="h-4 w-4 text-trust" />
          {t('dashboard.lastSync')}
        </div>
      </div>
    </aside>
  );
}
