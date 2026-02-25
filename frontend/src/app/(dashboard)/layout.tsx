import { ReactNode } from 'react';
import { AuthGuard } from '@/components/layout/AuthGuard';
import { DashboardShell } from '@/components/layout/DashboardShell';

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <AuthGuard>
      <DashboardShell>{children}</DashboardShell>
    </AuthGuard>
  );
}
