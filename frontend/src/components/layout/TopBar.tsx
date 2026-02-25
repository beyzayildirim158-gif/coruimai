"use client";

import { 
  MenuIcon, 
  SearchIcon, 
  BellIcon, 
  ShieldCheckIcon, 
  LogOutIcon, 
  CloseIcon, 
  SettingsIcon, 
  CreditCardIcon 
} from '@/components/icons';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { useState, useRef, useEffect } from 'react';
import toast from 'react-hot-toast';
import Link from 'next/link';
import { LanguageSwitcher } from '@/components/common/LanguageSwitcher';
import { useTranslation } from '@/i18n/TranslationProvider';

interface TopBarProps {
  onToggleSidebar?: () => void;
}

export function TopBar({ onToggleSidebar }: TopBarProps) {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const { t, locale } = useTranslation();
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearchResults, setShowSearchResults] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);
  const notifRef = useRef<HTMLDivElement>(null);
  const userMenuRef = useRef<HTMLDivElement>(null);

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setShowSearchResults(false);
      }
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) {
        setShowNotifications(false);
      }
      if (userMenuRef.current && !userMenuRef.current.contains(e.target as Node)) {
        setShowUserMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await logout();
      router.replace('/login');
    } catch (error) {
      toast.error('Failed to logout');
    } finally {
      setIsLoggingOut(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/analysis?search=${encodeURIComponent(searchQuery.trim())}`);
      setShowSearchResults(false);
      setSearchQuery('');
    }
  };

  const notifications = [
    { id: 1, title: t('common.analysisCompleted'), message: '@sample_creator ' + t('common.analysisReady'), time: '2m ago', read: false },
    { id: 2, title: t('common.pdfGenerated'), message: t('common.fullReportAvailable'), time: '1h ago', read: false },
    { id: 3, title: t('common.usageLimitWarning'), message: t('common.usedQuota'), time: '3h ago', read: true },
  ];

  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <header className="sticky top-0 z-40 flex items-center justify-between border-b border-slate-200 bg-white px-4 py-3">
      <div className="flex items-center gap-3">
        <button 
          onClick={onToggleSidebar}
          className="rounded-xl border border-slate-200 p-2 text-slate-600 hover:bg-slate-100 lg:hidden"
        >
          <MenuIcon className="h-5 w-5" />
        </button>
        
        {/* Search */}
        <div ref={searchRef} className="relative hidden md:block">
          <form onSubmit={handleSearch} className="flex items-center gap-3 rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm text-slate-600">
            <SearchIcon className="h-4 w-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setShowSearchResults(e.target.value.length > 0);
              }}
              placeholder={t('common.search')}
              className="w-64 bg-transparent text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none"
            />
            {searchQuery && (
              <button type="button" onClick={() => setSearchQuery('')} className="text-slate-400 hover:text-slate-600">
                <CloseIcon className="h-4 w-4" />
              </button>
            )}
          </form>
          
          {/* Search Results Dropdown */}
          {showSearchResults && searchQuery && (
            <div className="absolute top-full left-0 mt-2 w-80 rounded-2xl border border-slate-200 bg-white p-3 shadow-xl">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-400 mb-2">{t('common.quickActions')}</p>
              <Link
                href={`/analysis?search=${encodeURIComponent(searchQuery)}`}
                onClick={() => setShowSearchResults(false)}
                className="flex items-center gap-3 rounded-xl px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
              >
                <SearchIcon className="h-4 w-4 text-primary" />
                {t('common.searchFor')} "{searchQuery}"
              </Link>
              <button
                onClick={() => {
                  router.push('/analysis');
                  setShowSearchResults(false);
                }}
                className="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
              >
                <SearchIcon className="h-4 w-4 text-primary" />
                {t('common.analyze')} @{searchQuery.replace('@', '')}
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Language Switcher */}
        <LanguageSwitcher />

        {/* Subscription Badge */}
        <Link
          href="/billing"
          className="hidden rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-100 sm:flex"
        >
          <ShieldCheckIcon className="mr-2 h-4 w-4 text-trust" />
          {user?.subscriptionTier ?? 'STARTER'} · {user?.subscriptionStatus ?? 'TRIALING'}
        </Link>

        {/* Notifications */}
        <div ref={notifRef} className="relative">
          <button 
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative rounded-full border border-slate-200 p-2 text-slate-600 hover:bg-slate-100"
          >
            <BellIcon className="h-5 w-5" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-primary text-xs font-semibold text-white">
                {unreadCount}
              </span>
            )}
          </button>
          
          {/* Notifications Dropdown */}
          {showNotifications && (
            <div className="absolute top-full right-0 mt-2 w-80 rounded-2xl border border-slate-200 bg-white p-3 shadow-xl">
              <div className="flex items-center justify-between mb-3">
                <p className="text-sm font-semibold text-slate-900">{t('common.notifications')}</p>
                <button className="text-xs text-primary hover:text-primary/80">{t('common.markAllRead')}</button>
              </div>
              <div className="space-y-2 max-h-80 overflow-y-auto">
                {notifications.map((notif) => (
                  <div
                    key={notif.id}
                    className={`rounded-xl px-3 py-2 ${notif.read ? 'bg-slate-50' : 'bg-primary/5 border border-primary/20'}`}
                  >
                    <p className="text-sm font-medium text-slate-900">{notif.title}</p>
                    <p className="text-xs text-slate-500">{notif.message}</p>
                    <p className="text-xs text-slate-400 mt-1">{notif.time}</p>
                  </div>
                ))}
              </div>
              <Link
                href="/settings"
                onClick={() => setShowNotifications(false)}
                className="mt-3 block text-center text-xs text-primary hover:text-primary/80"
              >
                {t('settings.notifications')}
              </Link>
            </div>
          )}
        </div>

        {/* User Menu */}
        <div ref={userMenuRef} className="relative">
          <button 
            onClick={() => setShowUserMenu(!showUserMenu)}
            className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2 hover:bg-slate-100"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-lg font-semibold text-white">
              {user?.name?.[0]?.toUpperCase() ?? 'A'}
            </div>
            <div className="hidden sm:block">
              <p className="text-sm font-semibold text-slate-900">{user?.name ?? 'Agent'}</p>
              <p className="text-xs text-slate-500">{user?.email}</p>
            </div>
          </button>
          
          {/* User Menu Dropdown */}
          {showUserMenu && (
            <div className="absolute top-full right-0 mt-2 w-56 rounded-2xl border border-slate-200 bg-white p-2 shadow-xl">
              <div className="px-3 py-2 border-b border-slate-200 mb-2">
                <p className="text-sm font-semibold text-slate-900">{user?.name}</p>
                <p className="text-xs text-slate-500">{user?.email}</p>
              </div>
              <Link
                href="/settings"
                onClick={() => setShowUserMenu(false)}
                className="flex items-center gap-3 rounded-xl px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
              >
                <SettingsIcon className="h-4 w-4 text-slate-400" />
                {t('nav.settings')}
              </Link>
              <Link
                href="/billing"
                onClick={() => setShowUserMenu(false)}
                className="flex items-center gap-3 rounded-xl px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
              >
                <CreditCardIcon className="h-4 w-4 text-slate-400" />
                {t('nav.billing')}
              </Link>
              <button
                onClick={() => {
                  setShowUserMenu(false);
                  handleLogout();
                }}
                disabled={isLoggingOut}
                className="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-sm text-warning hover:bg-warning/5"
              >
                <LogOutIcon className="h-4 w-4" />
                {isLoggingOut ? t('common.loading') : t('auth.logout')}
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
