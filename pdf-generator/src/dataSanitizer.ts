/**
 * 🧹 DATA SANITIZER - PDF için Veri Temizleme ve Dönüştürme
 * Frontend ile %100 uyumlu, aynı JSON payload'ı kullanır
 * 
 * GÖREV 1: Değişken adı filtreleme
 * GÖREV 2: Null/Zero değer işleme
 * GÖREV 3: [object Object] önleme
 * GÖREV 4: Impossible metrics gizleme
 */

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface SanitizedMetric {
  value: string | number;
  display: string;
  isAvailable: boolean;
  color: string;
  badge: 'success' | 'warning' | 'danger' | 'neutral';
}

export interface SanitizedFinding {
  text: string;
  type: 'strength' | 'weakness' | 'info' | 'warning' | 'critical';
  icon: string;
  color: string;
  isValid: boolean;
}

export interface SanitizedRecommendation {
  action: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  icon: string;
  priorityNumber: number;
  isValid: boolean;
}

// ============================================================================
// VARIABLE NAME PATTERNS (Yasaklı desenler)
// ============================================================================

const VARIABLE_PATTERNS = [
  /_NOTE$/i,
  /_DISPLAY$/i,
  /_MAX$/i,
  /_MIN$/i,
  /_RATE$/i,
  /_SCORE$/i,
  /_COUNT$/i,
  /_VALUE$/i,
  /_INTERNAL$/i,
  /^[A-Z][A-Z_]+[A-Z]$/,           // ALL_CAPS_VARIABLES
  /^[a-z]+[A-Z][a-zA-Z]*$/,         // camelCaseVariables
  /^[a-z]+_[a-z]+_[a-z]+$/,         // snake_case_variables
  /BRAND_DEAL_RATE/i,
  /ZERO_METRICS/i,
  /NULL_VALUE/i,
  /UNDEFINED/i,
  /\[object Object\]/i,
  /^undefined$/i,
  /^null$/i,
  /^NaN$/i,
];

// Banned generic phrases that add no value
const BANNED_PHRASES = [
  'daha fazla paylaşım yap',
  'içerik kalitesini artır',
  'tutarlı ol',
  'etkileşimi artır',
  'more posts',
  'increase engagement',
  'be consistent',
  'improve quality',
];

// ============================================================================
// CORE SANITIZATION FUNCTIONS
// ============================================================================

/**
 * Bir metnin değişken adı olup olmadığını kontrol et
 */
export function isVariableName(text: string | null | undefined): boolean {
  if (!text || typeof text !== 'string') return false;
  const trimmed = text.trim();
  if (trimmed.length === 0) return false;
  return VARIABLE_PATTERNS.some(pattern => pattern.test(trimmed));
}

/**
 * Banned/generic phrase kontrolü
 */
export function isBannedPhrase(text: string | null | undefined): boolean {
  if (!text || typeof text !== 'string') return false;
  const lower = text.toLowerCase().trim();
  return BANNED_PHRASES.some(phrase => lower.includes(phrase));
}

/**
 * Metin çok kısa mı? (Minimum 50 karakter olmalı)
 */
export function isTooShort(text: string | null | undefined, minLength: number = 50): boolean {
  if (!text || typeof text !== 'string') return true;
  return text.trim().length < minLength;
}

/**
 * [object Object] veya JSON string kontrolü
 */
export function isInvalidObject(text: string | null | undefined): boolean {
  if (!text || typeof text !== 'string') return false;
  const trimmed = text.trim();
  return (
    trimmed === '[object Object]' ||
    trimmed.startsWith('{') ||
    trimmed.startsWith('[') ||
    trimmed.includes('[object')
  );
}

/**
 * Değerin geçerli olup olmadığını kontrol et
 */
export function isValidValue(value: any): boolean {
  if (value === null || value === undefined) return false;
  if (typeof value === 'number' && (isNaN(value) || !isFinite(value))) return false;
  if (typeof value === 'string') {
    const trimmed = value.trim().toLowerCase();
    if (['null', 'undefined', 'nan', '', '[object object]'].includes(trimmed)) return false;
    if (isVariableName(value)) return false;
  }
  return true;
}

// ============================================================================
// VALUE FORMATTERS
// ============================================================================

/**
 * Sayıyı formatla - Zero/null için "Hesaplanamadı"
 */
export function formatNumber(
  num: number | null | undefined,
  placeholder: string = '--'
): string {
  if (num === null || num === undefined || isNaN(num)) return placeholder;
  if (num === 0) return placeholder;
  
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return num.toLocaleString('tr-TR');
}

/**
 * Yüzdeyi formatla
 */
export function formatPercent(
  num: number | null | undefined,
  placeholder: string = '--'
): string {
  if (num === null || num === undefined || isNaN(num)) return placeholder;
  if (num === 0) return placeholder;
  return `%${num.toFixed(2)}`;
}

/**
 * Skoru formatla - 0 için "Hesaplanamadı"
 */
export function formatScore(
  score: number | null | undefined,
  placeholder: string = 'Hesaplanamadı'
): string {
  if (score === null || score === undefined || isNaN(score)) return placeholder;
  if (score === 0) return placeholder;
  return score.toFixed(0);
}

/**
 * Para formatla - Impossible values için gizle
 */
export function formatCurrency(
  amount: number | null | undefined,
  isServiceProvider: boolean = false
): string {
  if (amount === null || amount === undefined || isNaN(amount)) return 'Hesaplanamadı';
  if (amount === 0) return 'Hesaplanamadı';
  
  // GÖREV 4: Service provider için story value gibi metrikleri gizle
  if (isServiceProvider && amount < 50) {
    return 'Bu metrik hesap türünüz için geçerli değil';
  }
  
  if (amount >= 1000) {
    return `$${(amount / 1000).toFixed(1)}K`;
  }
  return `$${amount.toFixed(0)}`;
}

// ============================================================================
// OBJECT EXTRACTORS (Deep extraction from nested objects)
// ============================================================================

/**
 * Obje veya string'den metin çıkar
 */
export function extractText(item: any): string {
  if (!item) return '';
  if (typeof item === 'string') return item;
  if (typeof item === 'number' || typeof item === 'boolean') return String(item);
  
  // Bilinen alanları kontrol et
  const textFields = [
    'finding', 'text', 'description', 'action', 'recommendation',
    'insight', 'observation', 'issue', 'message', 'content',
    'kusur', 'realite', 'neden_onemli', 'headline'
  ];
  
  for (const field of textFields) {
    if (item[field] && typeof item[field] === 'string') {
      return item[field];
    }
  }
  
  // Array ise birleştir
  if (Array.isArray(item)) {
    return item.map(extractText).filter(Boolean).join(', ');
  }
  
  // Son çare - stringify etme, boş döndür
  return '';
}

/**
 * Finding objesini sanitize et
 */
export function sanitizeFinding(item: any): SanitizedFinding | null {
  const text = extractText(item);
  
  // Validation - Less aggressive
  if (!text || isVariableName(text) || isInvalidObject(text)) {
    return null;
  }
  
  // Minimum 15 karakter (reduced from 30)
  if (text.length < 15) {
    return null;
  }
  
  // Type belirleme
  let type: SanitizedFinding['type'] = 'info';
  const lower = text.toLowerCase();
  
  if (item?.type) {
    const t = item.type.toLowerCase();
    if (t.includes('strength') || t.includes('güç') || t.includes('olumlu')) type = 'strength';
    else if (t.includes('weakness') || t.includes('zayıf') || t.includes('sorun')) type = 'weakness';
    else if (t.includes('critical') || t.includes('kritik')) type = 'critical';
    else if (t.includes('warning') || t.includes('uyarı')) type = 'warning';
  } else {
    // Text'ten tahmin et
    if (lower.includes('güçlü') || lower.includes('başarılı') || lower.includes('iyi')) type = 'strength';
    else if (lower.includes('zayıf') || lower.includes('düşük') || lower.includes('yetersiz')) type = 'weakness';
    else if (lower.includes('kritik') || lower.includes('acil')) type = 'critical';
  }
  
  // Icon ve renk
  const typeConfig = {
    strength: { icon: '✅', color: '#16a34a' },
    weakness: { icon: '⚠️', color: '#dc2626' },
    critical: { icon: '🚨', color: '#991b1b' },
    warning: { icon: '⚡', color: '#d97706' },
    info: { icon: 'ℹ️', color: '#2563eb' },
  };
  
  return {
    text,
    type,
    icon: typeConfig[type].icon,
    color: typeConfig[type].color,
    isValid: true,
  };
}

/**
 * Recommendation objesini sanitize et
 */
export function sanitizeRecommendation(item: any, index: number): SanitizedRecommendation | null {
  let text = '';
  
  if (typeof item === 'string') {
    text = item;
  } else if (item?.action) {
    text = item.action;
  } else if (item?.recommendation) {
    text = item.recommendation;
  } else if (item?.text) {
    text = item.text;
  } else {
    text = extractText(item);
  }
  
  // Validation - Less aggressive
  if (!text || isVariableName(text) || isInvalidObject(text)) {
    return null;
  }
  
  // Minimum 20 karakter (reduced from 50)
  if (text.length < 20) {
    return null;
  }
  
  // Priority belirleme
  let priority: SanitizedRecommendation['priority'] = 'medium';
  
  if (item?.priority) {
    const p = String(item.priority).toLowerCase();
    if (p === 'critical' || p === '1' || p === 'kritik') priority = 'critical';
    else if (p === 'high' || p === '2' || p === 'yüksek') priority = 'high';
    else if (p === 'low' || p === '4' || p === 'düşük') priority = 'low';
  } else {
    // İlk 2 öneri yüksek öncelikli
    priority = index < 2 ? 'high' : 'medium';
  }
  
  const priorityConfig = {
    critical: { icon: '🚨', number: 1 },
    high: { icon: '🔴', number: 2 },
    medium: { icon: '🟡', number: 3 },
    low: { icon: '🟢', number: 4 },
  };
  
  return {
    action: text,
    priority,
    icon: priorityConfig[priority].icon,
    priorityNumber: priorityConfig[priority].number,
    isValid: true,
  };
}

// ============================================================================
// METRIC SANITIZER
// ============================================================================

/**
 * Metriği sanitize et ve görüntüleme bilgisi döndür
 */
export function sanitizeMetric(
  value: any,
  metricName: string,
  options: {
    isServiceProvider?: boolean;
    overallScore?: number;
  } = {}
): SanitizedMetric {
  const { isServiceProvider = false, overallScore } = options;
  
  // Geçersiz değer
  if (!isValidValue(value)) {
    return {
      value: 0,
      display: 'Hesaplanamadı',
      isAvailable: false,
      color: '#9CA3AF',
      badge: 'neutral',
    };
  }
  
  const numValue = typeof value === 'number' ? value : parseFloat(value);
  
  // Zero değer
  if (numValue === 0 || isNaN(numValue)) {
    return {
      value: 0,
      display: 'Hesaplanamadı',
      isAvailable: false,
      color: '#9CA3AF',
      badge: 'neutral',
    };
  }
  
  // GÖREV 4: Impossible metrics kontrolü
  // Service provider için bazı metrikler mantıksız
  const impossibleForService = [
    'brandDealRate', 'storyValue', 'revenuePerFollower',
    'sponsorshipValue', 'influencerScore'
  ];
  
  if (isServiceProvider && impossibleForService.some(m => metricName.includes(m))) {
    return {
      value: numValue,
      display: 'Bu hesap türü için geçerli değil',
      isAvailable: false,
      color: '#9CA3AF',
      badge: 'neutral',
    };
  }
  
  // Score bazlı renklendirme
  // GÖREV: Genel skor düşükse yeşil renk kullanma
  let color = '#9CA3AF';
  let badge: SanitizedMetric['badge'] = 'neutral';
  
  if (numValue >= 80) {
    // Genel skor 50'nin altındaysa yeşil kullanma
    if (overallScore !== undefined && overallScore < 50) {
      color = '#F59E0B'; // Turuncu
      badge = 'warning';
    } else {
      color = '#10B981';
      badge = 'success';
    }
  } else if (numValue >= 60) {
    color = '#22C55E';
    badge = 'success';
  } else if (numValue >= 40) {
    color = '#F59E0B';
    badge = 'warning';
  } else {
    color = '#EF4444';
    badge = 'danger';
  }
  
  return {
    value: numValue,
    display: numValue.toFixed(0),
    isAvailable: true,
    color,
    badge,
  };
}

// ============================================================================
// FULL PAYLOAD SANITIZER
// ============================================================================

export interface SanitizedPayload {
  // Account
  username: string;
  displayName: string;
  followers: SanitizedMetric;
  following: SanitizedMetric;
  posts: SanitizedMetric;
  engagementRate: SanitizedMetric;
  avgLikes: SanitizedMetric;
  avgComments: SanitizedMetric;
  botScore: SanitizedMetric;
  isVerified: boolean;
  isBusiness: boolean;
  bio: string;
  profilePicUrl: string;
  
  // Scores
  overallScore: SanitizedMetric;
  scoreGrade: string;
  healthStatus: string;
  healthClass: 'good' | 'medium' | 'poor';
  
  // Business Identity
  isServiceProvider: boolean;
  accountType: string;
  accountTypeExplanation: string;
  correctMetrics: string[];
  wrongMetrics: string[];
  
  // Agent Results (sanitized)
  agents: Array<{
    key: string;
    name: string;
    role: string;
    color: string;
    icon: string;
    score: SanitizedMetric;
    findings: SanitizedFinding[];
    recommendations: SanitizedRecommendation[];
    metrics: Record<string, SanitizedMetric>;
    // Raw data for full display
    rawFindings?: any[];
    rawRecommendations?: any[];
  }>;
  
  // ELI5 - Full structure
  eli5?: {
    headline: string;
    grade: string;
    gradeExplanation: string;
    topStrengths: string[];
    criticalIssues: string[];
    quickWins: string[];
    // Additional ELI5 sections
    simplifiedMetrics?: any;
    rewrittenHooks?: any[];
    actionPlan?: {
      thisWeek: string[];
      thisMonth: string[];
      avoid: string[];
    };
    motivationalNote?: string;
  };
  
  // Final Verdict
  finalVerdict?: {
    situation: string;
    verdict: string;
    criticalIssues: string[];
    thisWeekActions: string[];
    warning: string;
  };
  
  // Content Plan
  contentPlan?: Array<{
    day: number;
    dayName: string;
    contentType: string;
    topic: string;
    hook: string;
    bestTime: string;
    icon: string;
    caption?: string;
    hashtags?: string[];
    objective?: string;
  }>;
  
  // Advanced Analysis - Full 11 modules
  advancedAnalysis?: {
    audience_deep_dive?: any;
    content_forensics?: any;
    engagement_quality?: any;
    hashtag_intelligence?: any;
    competitor_gap?: any;
    brand_perception?: any;
    viral_potential?: any;
    monetization_readiness?: any;
    growth_trajectory?: any;
    risk_assessment?: any;
    action_priority?: any;
    [key: string]: any;
  };
  
  // Sanitization Report
  sanitizationReport?: {
    corrections?: Record<string, any>;
    warnings?: string[];
    phase_info?: {
      determined_phase: string;
      phase_name: string;
      health_score: number;
      effective_score: number;
      focus_areas: string[];
      blocked_strategies: string[];
      duration: string;
      reasoning: string;
    };
    metrics_summary?: {
      overall_health: number;
      engagement_depth: number;
      trust_score: number;
      ghost_follower_percent: number;
    };
  };
  
  // Hard Validation
  hardValidation?: {
    violations?: Array<{
      rule: string;
      message: string;
    }>;
  };
  
  // Metadata
  analysisDate: string;
  reportId: string;
  tier?: string;
}

/**
 * Agent meta verileri
 */
const AGENT_META: Record<string, { name: string; role: string; color: string; icon: string }> = {
  domainMaster: {
    name: 'Sektör Analizi',
    role: 'Sektör ve Niş Analiz Uzmanı',
    color: 'purple',
    icon: '🎯',
  },
  growthVirality: {
    name: 'Büyüme Stratejisi',
    role: 'Büyüme ve Viral Strateji Uzmanı',
    color: 'green',
    icon: '📈',
  },
  salesConversion: {
    name: 'Monetizasyon',
    role: 'Monetizasyon ve Satış Uzmanı',
    color: 'amber',
    icon: '💰',
  },
  visualBrand: {
    name: 'Görsel Kimlik',
    role: 'Görsel Marka Kimliği Uzmanı',
    color: 'pink',
    icon: '🎨',
  },
  communityLoyalty: {
    name: 'Topluluk',
    role: 'Topluluk ve Sadakat Stratejisti',
    color: 'red',
    icon: '❤️',
  },
  attentionArchitect: {
    name: 'Hook Optimizasyonu',
    role: 'Dikkat ve Hook Optimizasyon Uzmanı',
    color: 'blue',
    icon: '👁️',
  },
  systemGovernor: {
    name: 'Veri Doğrulama',
    role: 'Veri Doğrulama ve Güvenlik Uzmanı',
    color: 'slate',
    icon: '🛡️',
  },
  contentStrategist: {
    name: 'İçerik Stratejisi',
    role: 'İçerik Strateji Uzmanı',
    color: 'indigo',
    icon: '📝',
  },
  audienceDynamics: {
    name: 'Kitle Analizi',
    role: 'Kitle Dinamikleri Uzmanı',
    color: 'cyan',
    icon: '👥',
  },
};

/**
 * Content type icon mapping
 */
const CONTENT_TYPE_ICONS: Record<string, string> = {
  'Reels': '🎬',
  'Carousel': '📱',
  'Image': '🖼️',
  'Video': '📹',
  'Story': '⏰',
  'IGTV': '📺',
  'Live': '🔴',
};

/**
 * Day name mapping
 */
const DAY_NAMES: Record<number, string> = {
  1: 'Pazartesi',
  2: 'Salı',
  3: 'Çarşamba',
  4: 'Perşembe',
  5: 'Cuma',
  6: 'Cumartesi',
  7: 'Pazar',
};

/**
 * Ana sanitize fonksiyonu - Frontend ile aynı payload'ı alır
 */
export function sanitizePayload(payload: any): SanitizedPayload {
  const accountData = payload.accountData || {};
  const agentResults = payload.agentResults || {};
  const eli5Report = payload.eli5Report || agentResults.eli5Report || {};
  const finalVerdict = payload.finalVerdict || agentResults.finalVerdict || {};
  const businessIdentity = payload.businessIdentity || agentResults.businessIdentity || {};
  const contentPlan = payload.contentPlan || agentResults.contentPlan || {};
  const advancedAnalysis = payload.advancedAnalysis || agentResults.advancedAnalysis || null;
  const sanitizationReport = payload.sanitizationReport || agentResults.sanitizationReport || null;
  const hardValidation = payload.hardValidation || agentResults.hardValidation || null;
  
  // Business identity kontrolü
  const isServiceProvider = 
    businessIdentity?.account_type?.toLowerCase().includes('service') ||
    businessIdentity?.is_service_provider === true;
  
  const overallScore = payload.overallScore ?? 0;
  
  // Health status
  let healthStatus = 'Bilinmiyor';
  let healthClass: 'good' | 'medium' | 'poor' = 'medium';
  
  if (overallScore >= 70) {
    healthStatus = '🟢 İyi Performans';
    healthClass = 'good';
  } else if (overallScore >= 40) {
    healthStatus = '🟡 Geliştirilmeli';
    healthClass = 'medium';
  } else if (overallScore > 0) {
    healthStatus = '🔴 Kritik - Aksiyon Gerekli';
    healthClass = 'poor';
  }
  
  // Sanitize agents - Less aggressive filtering
  const sanitizedAgents = Object.entries(agentResults)
    .filter(([key]) => !['eli5Report', 'finalVerdict', 'businessIdentity', 'advancedAnalysis', 'sanitizationReport', 'hardValidation', 'contentPlan'].includes(key))
    .map(([key, value]: [string, any]) => {
      const meta = AGENT_META[key] || {
        name: key.replace(/([A-Z])/g, ' $1').trim(),
        role: 'Analiz Uzmanı',
        color: 'blue',
        icon: '📊',
      };
      
      // Sanitize findings - Less aggressive, keep more data
      const rawFindings = value.findings || [];
      const findings = rawFindings
        .map((f: any) => sanitizeFinding(f))
        .filter((f: any): f is SanitizedFinding => f !== null)
        .slice(0, 10); // Increased from 5 to 10
      
      // Sanitize recommendations - Less aggressive
      const rawRecommendations = value.recommendations || [];
      const recommendations = rawRecommendations
        .map((r: any, i: number) => sanitizeRecommendation(r, i))
        .filter((r: any): r is SanitizedRecommendation => r !== null)
        .slice(0, 10); // Increased from 5 to 10
      
      // Sanitize metrics
      const metrics: Record<string, SanitizedMetric> = {};
      if (value.metrics) {
        for (const [mKey, mValue] of Object.entries(value.metrics)) {
          // Skip internal/variable-like keys
          if (isVariableName(mKey)) continue;
          metrics[mKey] = sanitizeMetric(mValue, mKey, { isServiceProvider, overallScore });
        }
      }
      
      return {
        key,
        name: meta.name,
        role: meta.role,
        color: meta.color,
        icon: meta.icon,
        score: sanitizeMetric(value.metrics?.overallScore || value.score, 'overallScore', { isServiceProvider, overallScore }),
        findings,
        recommendations,
        metrics,
        // Keep raw data for alternative rendering
        rawFindings,
        rawRecommendations,
      };
    })
    // Don't filter out agents with no findings - they may have other useful data
    .filter(agent => agent.findings.length > 0 || agent.recommendations.length > 0 || Object.keys(agent.metrics).length > 0);
  
  // Sanitize ELI5 - Full structure
  let sanitizedEli5: SanitizedPayload['eli5'];
  if (eli5Report?.executiveSummary || eli5Report?.headline) {
    const es = eli5Report.executiveSummary || eli5Report;
    sanitizedEli5 = {
      headline: extractText(es.headline) || '',
      grade: es.grade || '',
      gradeExplanation: extractText(es.gradeExplanation) || '',
      topStrengths: (es.topStrengths || [])
        .map(extractText)
        .filter((s: string) => s && !isVariableName(s) && s.length > 10),
      criticalIssues: (es.criticalIssues || [])
        .map(extractText)
        .filter((s: string) => s && !isVariableName(s) && s.length > 10),
      quickWins: (es.quickWins || [])
        .map(extractText)
        .filter((s: string) => s && !isVariableName(s) && s.length > 10),
      // Additional sections - Pass through with proper structure
      simplifiedMetrics: eli5Report.simplifiedMetrics || eli5Report.simplified_metrics || null,
      rewrittenHooks: Array.isArray(eli5Report.rewrittenHooks) 
        ? eli5Report.rewrittenHooks 
        : (Array.isArray(eli5Report.rewritten_hooks) ? eli5Report.rewritten_hooks : []),
      actionPlan: eli5Report.actionPlan || eli5Report.action_plan ? {
        thisWeek: ((eli5Report.actionPlan || eli5Report.action_plan)?.thisWeek || (eli5Report.actionPlan || eli5Report.action_plan)?.this_week || []).map(extractText).filter(Boolean),
        thisMonth: ((eli5Report.actionPlan || eli5Report.action_plan)?.thisMonth || (eli5Report.actionPlan || eli5Report.action_plan)?.this_month || []).map(extractText).filter(Boolean),
        avoid: ((eli5Report.actionPlan || eli5Report.action_plan)?.avoid || []).map(extractText).filter(Boolean),
      } : undefined,
      motivationalNote: eli5Report.motivationalNote || eli5Report.motivational_note || '',
    };
  }
  
  // Sanitize Final Verdict
  let sanitizedVerdict: SanitizedPayload['finalVerdict'];
  if (finalVerdict?.verdict || finalVerdict?.situation) {
    sanitizedVerdict = {
      situation: extractText(finalVerdict.situation) || '',
      verdict: extractText(finalVerdict.verdict) || '',
      criticalIssues: (finalVerdict.critical_issues || finalVerdict.criticalIssues || [])
        .map(extractText)
        .filter((s: string) => s && !isVariableName(s) && s.length > 5),
      thisWeekActions: (finalVerdict.this_week_actions || finalVerdict.thisWeekActions || [])
        .map(extractText)
        .filter((s: string) => s && !isVariableName(s) && s.length > 5),
      warning: extractText(finalVerdict.warning) || '',
    };
  }
  
  // Sanitize Content Plan - Full structure
  let sanitizedContentPlan: SanitizedPayload['contentPlan'];
  const weeklyPlan = contentPlan?.weeklyPlan || contentPlan?.weekly_plan || (Array.isArray(contentPlan) ? contentPlan : null);
  if (weeklyPlan && Array.isArray(weeklyPlan)) {
    sanitizedContentPlan = weeklyPlan
      .filter((day: any) => day && (day.topic || day.hook || day.content_type || day.contentType))
      .map((day: any, index: number) => ({
        day: day.day || index + 1,
        dayName: day.dayName || day.day_name || DAY_NAMES[day.day || index + 1] || `Gün ${index + 1}`,
        contentType: day.contentType || day.content_type || 'Gönderi',
        topic: extractText(day.topic) || 'Konu belirtilmedi',
        hook: extractText(day.hook) || '',
        bestTime: day.bestTime || day.best_time || '',
        icon: CONTENT_TYPE_ICONS[day.contentType || day.content_type] || '📝',
        caption: day.caption || '',
        hashtags: day.hashtags || [],
        objective: day.objective || '',
      }))
      .slice(0, 7); // Max 7 days
  }
  
  return {
    // Account
    username: accountData.username || 'unknown',
    displayName: accountData.fullName || accountData.full_name || accountData.username || 'Kullanıcı',
    followers: sanitizeMetric(accountData.followers, 'followers'),
    following: sanitizeMetric(accountData.following, 'following'),
    posts: sanitizeMetric(accountData.posts || accountData.mediaCount, 'posts'),
    engagementRate: sanitizeMetric(accountData.engagementRate || accountData.engagement_rate, 'engagementRate'),
    avgLikes: sanitizeMetric(accountData.avgLikes || accountData.avg_likes, 'avgLikes'),
    avgComments: sanitizeMetric(accountData.avgComments || accountData.avg_comments, 'avgComments'),
    botScore: sanitizeMetric(accountData.botScore || accountData.bot_score, 'botScore'),
    isVerified: accountData.verified === true || accountData.isVerified === true || accountData.is_verified === true,
    isBusiness: accountData.isBusiness === true || accountData.is_business === true,
    bio: accountData.bio || accountData.biography || '',
    profilePicUrl: accountData.profilePicUrl || accountData.profile_pic_url || '',
    
    // Scores
    overallScore: sanitizeMetric(overallScore, 'overallScore'),
    scoreGrade: payload.scoreGrade || 'N/A',
    healthStatus,
    healthClass,
    
    // Business Identity
    isServiceProvider,
    accountType: businessIdentity?.account_type || businessIdentity?.accountType || 'İçerik Üreticisi',
    accountTypeExplanation: extractText(businessIdentity?.account_type_explanation || businessIdentity?.explanation) || '',
    correctMetrics: (businessIdentity?.correct_success_metrics || businessIdentity?.correctMetrics || [])
      .filter((m: any) => typeof m === 'string' && !isVariableName(m)),
    wrongMetrics: (businessIdentity?.wrong_metrics_to_avoid || businessIdentity?.wrongMetrics || [])
      .filter((m: any) => typeof m === 'string' && !isVariableName(m)),
    
    // Agents
    agents: sanitizedAgents,
    
    // Reports
    eli5: sanitizedEli5,
    finalVerdict: sanitizedVerdict,
    contentPlan: sanitizedContentPlan,
    
    // Advanced Analysis - Pass through with minimal sanitization
    advancedAnalysis: advancedAnalysis ? {
      ...advancedAnalysis,
    } : undefined,
    
    // Sanitization Report
    sanitizationReport: sanitizationReport ? {
      corrections: sanitizationReport.corrections,
      warnings: sanitizationReport.warnings,
      phase_info: sanitizationReport.phase_info,
      metrics_summary: sanitizationReport.metrics_summary,
    } : undefined,
    
    // Hard Validation
    hardValidation: hardValidation ? {
      violations: hardValidation.violations,
    } : undefined,
    
    // Metadata
    analysisDate: new Date().toLocaleDateString('tr-TR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }),
    reportId: payload.reportId || 'N/A',
    tier: payload.tier,
  };
}
