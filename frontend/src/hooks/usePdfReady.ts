'use client';

import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * 📄 usePdfReady Hook
 * 
 * PDF generation için sayfa hazırlığını yönetir.
 * Tüm chart'ların ve critical element'lerin render olmasını bekler.
 * 
 * Özellikler:
 * 1. Chart render durumunu takip eder
 * 2. Global __PRINT_READY__ flag'i set eder (Puppeteer için)
 * 3. data-print-ready attribute'u günceller
 * 4. Configurable timeout ile fallback sağlar
 * 
 * Kullanım:
 * const { isReady, progress, markElementReady, waitForSelectors } = usePdfReady({
 *   chartIds: ['chart-1', 'chart-2'],
 *   timeout: 5000,
 *   onReady: () => console.log('PDF ready!')
 * });
 */

interface UsePdfReadyOptions {
  /** İzlenecek chart ID'leri */
  chartIds?: string[];
  /** Beklenecek CSS selector'lar */
  selectors?: string[];
  /** Minimum bekleme süresi (ms) */
  minWait?: number;
  /** Maximum bekleme süresi (ms) - timeout */
  timeout?: number;
  /** Data fetch tamamlandı mı? */
  dataLoaded?: boolean;
  /** Ready olduğunda çağrılacak callback */
  onReady?: () => void;
  /** Puppeteer için global flag set edilsin mi? */
  setPuppeteerFlag?: boolean;
}

interface UsePdfReadyReturn {
  /** Tüm elementler hazır mı? */
  isReady: boolean;
  /** Hazırlık yüzdesi (0-100) */
  progress: number;
  /** Belirli bir element'i hazır olarak işaretle */
  markElementReady: (id: string) => void;
  /** Hazır olan element sayısı */
  readyCount: number;
  /** Toplam beklenilen element sayısı */
  totalCount: number;
  /** Hazır olan element ID'leri */
  readyElements: string[];
  /** Manuel olarak ready tetikle */
  forceReady: () => void;
}

export function usePdfReady({
  chartIds = [],
  selectors = [],
  minWait = 1000,
  timeout = 10000,
  dataLoaded = true,
  onReady,
  setPuppeteerFlag = true,
}: UsePdfReadyOptions = {}): UsePdfReadyReturn {
  const [isReady, setIsReady] = useState(false);
  const [readyElements, setReadyElements] = useState<Set<string>>(new Set());
  const readyCalledRef = useRef(false);
  const startTimeRef = useRef<number>(Date.now());

  const totalCount = chartIds.length + selectors.length;

  // Element hazır işaretleme
  const markElementReady = useCallback((id: string) => {
    setReadyElements((prev) => {
      const next = new Set(prev);
      next.add(id);
      return next;
    });
  }, []);

  // Manuel ready tetikleme
  const forceReady = useCallback(() => {
    if (readyCalledRef.current) return;
    readyCalledRef.current = true;
    setIsReady(true);
    
    if (setPuppeteerFlag && typeof window !== 'undefined') {
      (window as any).__PRINT_READY__ = true;
    }
    
    onReady?.();
  }, [onReady, setPuppeteerFlag]);

  // Chart ve selector kontrolü
  useEffect(() => {
    if (readyCalledRef.current) return;
    if (!dataLoaded) return;

    const checkElements = () => {
      const ready = new Set<string>();
      
      // Chart'ları kontrol et
      chartIds.forEach((id) => {
        const element = document.querySelector(
          `[data-chart-id="${id}"][data-status="rendered"], [data-chart-id="${id}"][data-chart-rendered="true"]`
        );
        if (element) {
          ready.add(`chart:${id}`);
        }
      });

      // Selector'ları kontrol et
      selectors.forEach((selector) => {
        const element = document.querySelector(selector);
        if (element) {
          ready.add(`selector:${selector}`);
        }
      });

      return ready;
    };

    const evaluateReady = () => {
      const elapsed = Date.now() - startTimeRef.current;
      const currentReady = checkElements();
      
      setReadyElements(currentReady);

      // Minimum bekleme süresi kontrolü
      if (elapsed < minWait) {
        return false;
      }

      // Tüm elementler hazır mı?
      const allElementsReady = 
        chartIds.every((id) => currentReady.has(`chart:${id}`)) &&
        selectors.every((s) => currentReady.has(`selector:${s}`));

      // Timeout kontrolü
      const isTimedOut = elapsed >= timeout;

      if (allElementsReady || isTimedOut || totalCount === 0) {
        if (!readyCalledRef.current) {
          readyCalledRef.current = true;
          setIsReady(true);

          if (setPuppeteerFlag && typeof window !== 'undefined') {
            (window as any).__PRINT_READY__ = true;
            console.log('🖨️ PDF Ready signal sent', {
              elapsed,
              readyElements: Array.from(currentReady),
              timedOut: isTimedOut,
            });
          }

          onReady?.();
        }
        return true;
      }

      return false;
    };

    // İlk kontrol
    if (evaluateReady()) return;

    // Polling
    const interval = setInterval(() => {
      if (evaluateReady()) {
        clearInterval(interval);
      }
    }, 200);

    return () => {
      clearInterval(interval);
    };
  }, [chartIds, selectors, minWait, timeout, dataLoaded, onReady, setPuppeteerFlag, totalCount]);

  // Progress hesaplama
  const progress = totalCount === 0 
    ? 100 
    : Math.round((readyElements.size / totalCount) * 100);

  return {
    isReady,
    progress,
    markElementReady,
    readyCount: readyElements.size,
    totalCount,
    readyElements: Array.from(readyElements),
    forceReady,
  };
}

/**
 * 📊 useAllChartsReady Hook
 * 
 * Sayfadaki tüm chart wrapper'ların hazır olmasını bekler.
 * Otomatik olarak [data-status="rendered"] attribute'u ile kontrol eder.
 */
export function useAllChartsReady(timeout = 8000) {
  const [isReady, setIsReady] = useState(false);
  const [chartCount, setChartCount] = useState({ ready: 0, total: 0 });

  useEffect(() => {
    const startTime = Date.now();

    const checkCharts = () => {
      const allCharts = document.querySelectorAll('[data-chart-id]');
      const readyCharts = document.querySelectorAll('[data-chart-id][data-status="rendered"]');

      setChartCount({
        ready: readyCharts.length,
        total: allCharts.length,
      });

      const elapsed = Date.now() - startTime;
      
      // Tüm chart'lar hazır veya timeout
      if (readyCharts.length >= allCharts.length || elapsed >= timeout) {
        setIsReady(true);
        return true;
      }
      return false;
    };

    // İlk kontrol
    if (checkCharts()) return;

    const interval = setInterval(() => {
      if (checkCharts()) {
        clearInterval(interval);
      }
    }, 150);

    return () => clearInterval(interval);
  }, [timeout]);

  return { isReady, ...chartCount };
}

/**
 * 🖼️ waitForImages Hook
 * 
 * Sayfadaki tüm görsellerin yüklenmesini bekler.
 */
export function useWaitForImages(containerRef?: React.RefObject<HTMLElement>, timeout = 5000) {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const container = containerRef?.current || document.body;
    const images = container.querySelectorAll('img');
    
    if (images.length === 0) {
      setIsReady(true);
      return;
    }

    let loadedCount = 0;
    const totalImages = images.length;

    const checkReady = () => {
      loadedCount++;
      if (loadedCount >= totalImages) {
        setIsReady(true);
      }
    };

    images.forEach((img) => {
      if (img.complete) {
        checkReady();
      } else {
        img.addEventListener('load', checkReady);
        img.addEventListener('error', checkReady); // Error da ready sayılır
      }
    });

    // Timeout
    const timeoutId = setTimeout(() => {
      setIsReady(true);
    }, timeout);

    return () => {
      clearTimeout(timeoutId);
      images.forEach((img) => {
        img.removeEventListener('load', checkReady);
        img.removeEventListener('error', checkReady);
      });
    };
  }, [containerRef, timeout]);

  return isReady;
}

export default usePdfReady;
