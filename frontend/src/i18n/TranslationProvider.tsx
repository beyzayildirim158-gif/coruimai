'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

type Locale = 'en' | 'tr';

interface TranslationContextType {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: string) => string;
  messages: Record<string, any>;
}

const TranslationContext = createContext<TranslationContextType | null>(null);

// Flatten nested object keys
function flattenMessages(obj: Record<string, any>, prefix = ''): Record<string, string> {
  return Object.keys(obj).reduce((acc: Record<string, string>, key) => {
    const value = obj[key];
    const newKey = prefix ? `${prefix}.${key}` : key;
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      Object.assign(acc, flattenMessages(value, newKey));
    } else {
      acc[newKey] = value;
    }
    return acc;
  }, {});
}

export function TranslationProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>('tr');
  const [messages, setMessages] = useState<Record<string, any>>({});
  const [flatMessages, setFlatMessages] = useState<Record<string, string>>({});

  useEffect(() => {
    // Get locale from cookie
    const cookieLocale = document.cookie
      .split('; ')
      .find(row => row.startsWith('locale='))
      ?.split('=')[1] as Locale | undefined;
    
    if (cookieLocale && (cookieLocale === 'en' || cookieLocale === 'tr')) {
      setLocaleState(cookieLocale);
    }
  }, []);

  useEffect(() => {
    // Load messages for current locale
    const loadMessages = async () => {
      try {
        const msgs = await import(`@/i18n/locales/${locale}.json`);
        setMessages(msgs.default);
        setFlatMessages(flattenMessages(msgs.default));
      } catch (error) {
        console.error('Failed to load messages:', error);
      }
    };
    loadMessages();
  }, [locale]);

  const setLocale = (newLocale: Locale) => {
    document.cookie = `locale=${newLocale};path=/;max-age=31536000`;
    setLocaleState(newLocale);
  };

  const t = (key: string): string => {
    return flatMessages[key] || key;
  };

  return (
    <TranslationContext.Provider value={{ locale, setLocale, t, messages }}>
      {children}
    </TranslationContext.Provider>
  );
}

export function useTranslation() {
  const context = useContext(TranslationContext);
  if (!context) {
    throw new Error('useTranslation must be used within a TranslationProvider');
  }
  return context;
}
