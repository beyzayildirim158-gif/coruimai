// Simple i18n configuration for client-side only
export const locales = ['en', 'tr'] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = 'tr';
