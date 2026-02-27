"use client";

import { ReactNode, useState } from 'react';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
import { CloseIcon } from '@/components/icons';

interface DashboardShellProps {
  children: ReactNode;
}

export function DashboardShell({ children }: DashboardShellProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-white text-slate-900">
      {/* Desktop Sidebar */}
      <Sidebar />
      
      {/* Mobile Sidebar Overlay */}
      {isSidebarOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          {/* Backdrop */}
          <div 
            className="absolute inset-0 bg-black/40"
            onClick={() => setIsSidebarOpen(false)}
          />
          
          {/* Mobile Sidebar */}
          <div className="absolute left-0 top-0 h-full w-64 border-r border-slate-200 bg-white p-4">
            <div className="flex justify-end mb-4">
              <button 
                onClick={() => setIsSidebarOpen(false)}
                className="rounded-xl border border-slate-200 p-2 text-slate-600 hover:bg-slate-100"
              >
                <CloseIcon className="h-5 w-5" />
              </button>
            </div>
            <Sidebar isMobile onClose={() => setIsSidebarOpen(false)} />
          </div>
        </div>
      )}
      
      <div className="flex flex-1 flex-col">
        <TopBar onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
        <main className="flex-1 bg-slate-50 px-3 py-4 sm:px-6 sm:py-6 lg:px-8">
          <div className="mx-auto max-w-6xl space-y-4 sm:space-y-6">{children}</div>
        </main>
      </div>
    </div>
  );
}
