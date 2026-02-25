'use client';

import { GlobeIcon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

const languageNames = {
  en: 'English',
  tr: 'Türkçe',
} as const;

type Locale = keyof typeof languageNames;

const locales: Locale[] = ['en', 'tr'];

export function LanguageSwitcher() {
  const { locale, setLocale } = useTranslation();

  return (
    <div className="relative group">
      <button
        className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-colors"
      >
        <GlobeIcon className="h-4 w-4" />
        <span>{languageNames[locale as Locale] || 'English'}</span>
      </button>
      <div className="absolute right-0 mt-2 w-40 rounded-xl border border-slate-200 bg-white py-1 shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
        {locales.map((loc) => (
          <button
            key={loc}
            onClick={() => setLocale(loc)}
            className={`w-full px-4 py-2 text-left text-sm hover:bg-slate-50 transition-colors ${
              loc === locale
                ? 'text-primary bg-primary/5'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            {languageNames[loc]}
          </button>
        ))}
      </div>
    </div>
  );
}
