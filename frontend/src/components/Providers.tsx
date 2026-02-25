'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, ReactNode } from 'react';
import { Toaster } from 'react-hot-toast';
import { TranslationProvider } from '@/i18n/TranslationProvider';

export function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      <TranslationProvider>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            className: 'bg-white text-slate-900 border border-slate-200 shadow-lg',
            duration: 4000,
          }}
        />
      </TranslationProvider>
    </QueryClientProvider>
  );
}
