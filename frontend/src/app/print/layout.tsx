import { ReactNode } from 'react';

/**
 * Print Layout - Auth gerektirmeyen, minimal layout
 * PDF generator bu sayfayı Puppeteer ile render eder
 */
export default function PrintLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-white">
      {children}
    </div>
  );
}
