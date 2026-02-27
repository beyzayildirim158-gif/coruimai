// =========================
// PERCENTAGE NORMALIZATION (Largest Remainder Method)
// =========================

interface PercentageData {
  [key: string]: number;
}

/**
 * Yüzdeleri tam 100'e normalize eder (Largest Remainder Method)
 * LLM'den gelen veriler %100'den fazla veya az toplayabilir
 * Bu fonksiyon matematiksel olarak doğru yuvarlama sağlar
 * 
 * @example
 * normalizePercentages({ superfan: 10, active: 94, passive: 5, ghost: 1 })
 * // Returns: { superfan: 9, active: 85, passive: 5, ghost: 1 } (toplam: 100)
 */
export function normalizePercentages<T extends PercentageData>(data: T): T {
  const keys = Object.keys(data);
  const values = keys.map(k => data[k]);
  const total = values.reduce((sum, v) => sum + v, 0);
  
  // Eğer toplam 0 ise, eşit dağıtım yap
  if (total === 0) {
    const equalShare = Math.floor(100 / keys.length);
    const remainder = 100 - (equalShare * keys.length);
    const result = {} as T;
    keys.forEach((key, i) => {
      (result as any)[key] = equalShare + (i < remainder ? 1 : 0);
    });
    return result;
  }
  
  // Her değeri 100 üzerinden hesapla
  const scaled = values.map(v => (v / total) * 100);
  
  // Floor değerleri al
  const floored = scaled.map(v => Math.floor(v));
  
  // Kalan miktarı hesapla
  let remainderTotal = 100 - floored.reduce((sum, v) => sum + v, 0);
  
  // Remainder'ları hesapla ve sırala (en büyük remainder önce)
  const remainders = scaled.map((v, i) => ({
    index: i,
    remainder: v - floored[i]
  })).sort((a, b) => b.remainder - a.remainder);
  
  // En büyük remainder'lara +1 ekle
  for (let i = 0; i < remainderTotal && i < remainders.length; i++) {
    floored[remainders[i].index] += 1;
  }
  
  // Sonucu oluştur
  const result = {} as T;
  keys.forEach((key, i) => {
    (result as any)[key] = floored[i];
  });
  
  return result;
}

// =========================
// EMPTY VALUE FILTERING
// =========================

type EmptyValue = 'Veri Yok' | 'N/A' | null | undefined | '';

/**
 * Boş, null, undefined veya 'Veri Yok' değerlerini filtreler
 * Tablo render'ı için kullanılır - boş satırlar gösterilmez
 * 
 * @example
 * filterEmptyMetrics({ er: 5.2, reach: 'Veri Yok', impressions: null })
 * // Returns: { er: 5.2 }
 */
export function filterEmptyMetrics<T extends Record<string, any>>(data: T): Partial<T> {
  const emptyValues: (string | null | undefined)[] = ['Veri Yok', 'N/A', null, undefined, '', 'undefined', 'null'];
  
  return Object.entries(data).reduce((acc, [key, value]) => {
    // Değer boş değilse ekle
    if (!emptyValues.includes(value) && value !== 0) {
      // 0 değeri geçerli bir veri olabilir, özel kontrol
      (acc as any)[key] = value;
    } else if (value === 0) {
      // 0 değerini koru (geçerli metrik)
      (acc as any)[key] = value;
    }
    return acc;
  }, {} as Partial<T>);
}

/**
 * Bir dizideki boş değerleri filtreler
 * Metrik listelerinden 'Veri Yok' satırlarını çıkarır
 * 
 * @example
 * filterEmptyRows([{ label: 'ER', value: 5.2 }, { label: 'Reach', value: 'Veri Yok' }])
 * // Returns: [{ label: 'ER', value: 5.2 }]
 */
export function filterEmptyRows<T extends { value?: any }>(rows: T[]): T[] {
  const emptyValues: (string | null | undefined)[] = ['Veri Yok', 'N/A', null, undefined, '', 'undefined', 'null'];
  
  return rows.filter(row => {
    const value = row.value;
    // Değer yoksa veya boş değer ise filtrele
    if (value === undefined) return false;
    if (emptyValues.includes(value)) return false;
    // String ise trim et ve kontrol et
    if (typeof value === 'string' && value.trim() === '') return false;
    return true;
  });
}

/**
 * Bir key-value map'inden render için filtrelenmiş entries döndürür
 * JSX map() için hazır
 * 
 * @example
 * getValidMetricEntries({ er: 5.2, reach: 'Veri Yok' })
 * // Returns: [['er', 5.2]]
 */
export function getValidMetricEntries<T extends Record<string, any>>(data: T): [string, any][] {
  const emptyValues: (string | null | undefined)[] = ['Veri Yok', 'N/A', null, undefined, '', 'undefined', 'null'];
  
  return Object.entries(data).filter(([_, value]) => {
    if (emptyValues.includes(value)) return false;
    if (typeof value === 'string' && value.trim() === '') return false;
    return true;
  });
}

// =========================
// NUMBER FORMATTING
// =========================

export const formatNumber = (value?: number | null, options: Intl.NumberFormatOptions = {}) => {
  if (value === undefined || value === null) return '—';
  return new Intl.NumberFormat('en-US', options).format(value);
};

export const formatPercentage = (value?: number | null, fractionDigits = 1) => {
  if (value === undefined || value === null) return '—';
  return `${value.toFixed(fractionDigits)}%`;
};

export const formatDateTime = (value?: string | Date | null) => {
  if (!value) return '—';
  const date = typeof value === 'string' ? new Date(value) : value;
  return date.toLocaleString('en-US', {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const gradeColor = (grade?: string | null) => {
  switch (grade) {
    case 'A':
      return 'text-emerald-300';
    case 'B':
      return 'text-lime-300';
    case 'C':
      return 'text-amber-300';
    case 'D':
      return 'text-orange-300';
    case 'F':
      return 'text-rose-400';
    default:
      return 'text-slate-400';
  }
};
