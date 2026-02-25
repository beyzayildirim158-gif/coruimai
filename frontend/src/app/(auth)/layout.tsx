import type { ReactNode } from 'react';

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-primary/5 text-slate-900">
      <div className="mx-auto flex max-w-7xl flex-col items-center px-4 py-10 sm:px-6 lg:px-8">
        {children}
      </div>
    </div>
  );
}
