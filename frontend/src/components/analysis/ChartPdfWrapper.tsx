'use client';

import React, { useRef, useState, useEffect, useCallback, ReactNode } from 'react';

/**
 * 📊 ChartPdfWrapper - PDF Export için Chart Sarmalayıcısı
 * 
 * Bu bileşen Recharts SVG grafiklerini PDF'e doğru şekilde aktarır.
 * 
 * Özellikler:
 * 1. SVG'yi canvas'a çevirip base64 image olarak render eder (opsiyonel)
 * 2. Animasyonları devre dışı bırakır
 * 3. PDF ready sinyali için data-status attribute'u kullanır
 * 4. Print media için özel stiller uygular
 * 
 * Kullanım:
 * <ChartPdfWrapper chartId="engagement-chart">
 *   <ResponsiveContainer>
 *     <BarChart data={data}>...</BarChart>
 *   </ResponsiveContainer>
 * </ChartPdfWrapper>
 */

interface ChartPdfWrapperProps {
  children: ReactNode;
  chartId: string;
  height?: number | string;
  width?: number | string;
  className?: string;
  /** SVG'yi canvas'a çevirip image olarak göster (bazı PDF kütüphaneleri için gerekli) */
  convertToImage?: boolean;
  /** Render bekle süresi (ms) - chart animasyonlarının bitmesini bekler */
  renderDelay?: number;
  /** Fallback mesajı */
  fallbackMessage?: string;
}

// Global PDF export modu kontrolü
let globalPdfExportMode = false;

export const setPdfExportMode = (enabled: boolean) => {
  globalPdfExportMode = enabled;
  // CSS class ile animasyonları kontrol et
  if (typeof document !== 'undefined') {
    if (enabled) {
      document.documentElement.classList.add('pdf-export-mode');
    } else {
      document.documentElement.classList.remove('pdf-export-mode');
    }
  }
};

export const isPdfExportMode = () => globalPdfExportMode;

export function ChartPdfWrapper({
  children,
  chartId,
  height = '100%',
  width = '100%',
  className = '',
  convertToImage = false,
  renderDelay = 500,
  fallbackMessage = 'Grafik yükleniyor...',
}: ChartPdfWrapperProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isRendered, setIsRendered] = useState(false);
  const [imageDataUrl, setImageDataUrl] = useState<string | null>(null);
  const [renderError, setRenderError] = useState(false);

  // SVG'yi canvas'a çevirip base64 image olarak döndür
  const convertSvgToImage = useCallback(async (): Promise<string | null> => {
    if (!containerRef.current) return null;

    const svgElement = containerRef.current.querySelector('svg');
    if (!svgElement) return null;

    try {
      // SVG'yi string'e çevir
      const svgData = new XMLSerializer().serializeToString(svgElement);
      const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
      const svgUrl = URL.createObjectURL(svgBlob);

      // Canvas oluştur
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      if (!ctx) return null;

      const img = new Image();
      
      return new Promise((resolve) => {
        img.onload = () => {
          // Canvas boyutlarını SVG'ye göre ayarla
          const svgRect = svgElement.getBoundingClientRect();
          canvas.width = svgRect.width * 2; // 2x resolution for better quality
          canvas.height = svgRect.height * 2;
          
          // Beyaz arka plan
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          
          // SVG'yi canvas'a çiz
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          
          URL.revokeObjectURL(svgUrl);
          resolve(canvas.toDataURL('image/png', 1.0));
        };

        img.onerror = () => {
          URL.revokeObjectURL(svgUrl);
          resolve(null);
        };

        img.src = svgUrl;
      });
    } catch (error) {
      console.error('SVG to image conversion failed:', error);
      return null;
    }
  }, []);

  // Chart render kontrolü
  useEffect(() => {
    const checkRenderStatus = async () => {
      // İlk render beklemesi
      await new Promise((resolve) => setTimeout(resolve, renderDelay));

      if (!containerRef.current) {
        setRenderError(true);
        setIsRendered(true);
        return;
      }

      const svgElement = containerRef.current.querySelector('svg');
      
      if (!svgElement) {
        setRenderError(true);
        setIsRendered(true);
        return;
      }

      // Eğer image'a çevirme istenmişse
      if (convertToImage && globalPdfExportMode) {
        const dataUrl = await convertSvgToImage();
        if (dataUrl) {
          setImageDataUrl(dataUrl);
        }
      }

      setIsRendered(true);
    };

    checkRenderStatus();
  }, [convertToImage, renderDelay, convertSvgToImage]);

  // Print modu için SVG dışa aktarma data attribute'u
  useEffect(() => {
    if (isRendered && containerRef.current) {
      containerRef.current.setAttribute('data-chart-rendered', 'true');
      containerRef.current.setAttribute('data-chart-id', chartId);
    }
  }, [isRendered, chartId]);

  return (
    <div
      ref={containerRef}
      className={`chart-pdf-wrapper ${className}`}
      data-status={isRendered ? 'rendered' : 'loading'}
      data-chart-id={chartId}
      style={{
        width,
        height,
        position: 'relative',
        overflow: 'visible',
      }}
    >
      {/* CSS Styles for PDF Export */}
      <style jsx>{`
        .chart-pdf-wrapper {
          /* Print/PDF için görünürlük garantisi */
          overflow: visible !important;
          page-break-inside: avoid;
          break-inside: avoid;
        }

        .chart-pdf-wrapper svg {
          overflow: visible !important;
        }

        /* PDF export modunda animasyonları devre dışı bırak */
        :global(.pdf-export-mode) .chart-pdf-wrapper svg * {
          animation: none !important;
          transition: none !important;
        }

        :global(.pdf-export-mode) .chart-pdf-wrapper .recharts-animation-wrapper {
          animation: none !important;
        }

        @media print {
          .chart-pdf-wrapper {
            overflow: visible !important;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
          }

          .chart-pdf-wrapper svg {
            overflow: visible !important;
            width: 100% !important;
            height: 100% !important;
          }

          /* Recharts animasyonlarını print'de devre dışı bırak */
          .chart-pdf-wrapper .recharts-animation-wrapper {
            animation: none !important;
          }
        }
      `}</style>

      {/* Render Error Fallback */}
      {renderError && (
        <div className="flex items-center justify-center h-full text-slate-400 text-sm">
          {fallbackMessage}
        </div>
      )}

      {/* Image mode: Canvas'tan oluşturulan görsel */}
      {imageDataUrl && convertToImage && globalPdfExportMode ? (
        <img
          src={imageDataUrl}
          alt={`Chart: ${chartId}`}
          className="w-full h-full object-contain"
          style={{ maxWidth: '100%', maxHeight: '100%' }}
        />
      ) : (
        // Normal SVG mode
        <div 
          className="chart-content" 
          style={{ width: '100%', height: '100%', overflow: 'visible' }}
        >
          {children}
        </div>
      )}
    </div>
  );
}

/**
 * 🎯 useChartPdfReady Hook
 * 
 * Tüm chart'ların render olmasını bekler ve PDF ready sinyali verir.
 * 
 * Kullanım:
 * const { isReady, readyCount, totalCount } = useChartPdfReady(['chart-1', 'chart-2']);
 */
export function useChartPdfReady(chartIds: string[], timeout = 5000) {
  const [readyCharts, setReadyCharts] = useState<Set<string>>(new Set());
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (chartIds.length === 0) {
      setIsReady(true);
      return;
    }

    const checkCharts = () => {
      const ready = new Set<string>();
      
      chartIds.forEach((id) => {
        const element = document.querySelector(`[data-chart-id="${id}"][data-status="rendered"]`);
        if (element) {
          ready.add(id);
        }
      });

      setReadyCharts(ready);

      if (ready.size === chartIds.length) {
        setIsReady(true);
        return true;
      }
      return false;
    };

    // İlk kontrol
    if (checkCharts()) return;

    // Polling ile kontrol
    const interval = setInterval(() => {
      if (checkCharts()) {
        clearInterval(interval);
      }
    }, 100);

    // Timeout
    const timeoutId = setTimeout(() => {
      clearInterval(interval);
      setIsReady(true); // Timeout olsa bile ready ver
    }, timeout);

    return () => {
      clearInterval(interval);
      clearTimeout(timeoutId);
    };
  }, [chartIds, timeout]);

  return {
    isReady,
    readyCount: readyCharts.size,
    totalCount: chartIds.length,
    readyCharts: Array.from(readyCharts),
  };
}

/**
 * 🚀 preparePdfExport - PDF export öncesi hazırlık fonksiyonu
 * 
 * Chart animasyonlarını devre dışı bırakır ve render bekler
 */
export async function preparePdfExport(chartIds: string[], timeout = 5000): Promise<boolean> {
  // PDF export modunu aktif et
  setPdfExportMode(true);

  return new Promise((resolve) => {
    const startTime = Date.now();

    const checkReady = () => {
      const allReady = chartIds.every((id) => {
        const element = document.querySelector(`[data-chart-id="${id}"][data-status="rendered"]`);
        return element !== null;
      });

      if (allReady || Date.now() - startTime > timeout) {
        resolve(allReady);
        return;
      }

      requestAnimationFrame(checkReady);
    };

    // İlk çerçevede başla
    requestAnimationFrame(checkReady);
  });
}

/**
 * 🧹 cleanupPdfExport - PDF export sonrası temizlik
 */
export function cleanupPdfExport() {
  setPdfExportMode(false);
}

export default ChartPdfWrapper;
