/**
 * 🎨 INSTAGRAM AI - PROFESSIONAL PDF GENERATOR v2.0
 * HTML/CSS Template-Based System (Puppeteer + Handlebars)
 * McKinsey-Level Report Design
 */

import puppeteer, { Browser, PDFOptions } from 'puppeteer';
import Handlebars from 'handlebars';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { sanitizePayload, SanitizedPayload } from './dataSanitizer.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface AgentReport {
  agentName?: string;
  agentRole?: string;
  findings?: any[];
  recommendations?: any[];
  metrics?: Record<string, unknown>;
  [key: string]: any;
}

export interface AccountData {
  username: string;
  followers?: number;
  following?: number;
  engagementRate?: number;
  posts?: number;
  bio?: string;
  profilePicUrl?: string;
  avgLikes?: number;
  avgComments?: number;
  verified?: boolean;
  followersGrowth?: number;
}

export interface ELI5Report {
  executiveSummary?: {
    headline?: string;
    grade?: string;
    gradeExplanation?: string;
    topStrengths?: string[];
    criticalIssues?: string[];
    quickWins?: string[];
  };
  simplifiedMetrics?: {
    engagement?: { value?: string; verdict?: string; explanation?: string; benchmark?: string };
    growth?: { value?: string; verdict?: string; explanation?: string; benchmark?: string };
    contentQuality?: { value?: string; verdict?: string; explanation?: string; benchmark?: string };
    audienceQuality?: { value?: string; verdict?: string; explanation?: string; benchmark?: string };
  };
  rewrittenHooks?: Array<{
    originalPost?: string;
    originalHook?: string;
    newHook?: string;
    technique?: string;
    whyBetter?: string;
  }>;
  actionPlan?: {
    thisWeek?: string[];
    thisMonth?: string[];
    avoid?: string[];
  };
  motivationalNote?: string;
}

export interface ContentPlan {
  weeklyPlan?: Array<{
    day?: number;
    dayName?: string;
    contentType?: string;
    topic?: string;
    hook?: string;
    caption?: string;
    hashtags?: string[];
    bestTime?: string;
    objective?: string;
  }>;
  monthlyTheme?: string;
  contentPillars?: string[];
}

export interface FinalVerdict {
  situation?: string;
  verdict?: string;
  critical_issues?: string[];
  this_week_actions?: string[];
  warning?: string;
}

export interface BusinessIdentity {
  account_type?: string;
  account_type_explanation?: string;
  correct_success_metrics?: string[];
  wrong_metrics_to_avoid?: string[];
}

export interface AdvancedAnalysis {
  [key: string]: any;
}

export interface GeneratePayload {
  reportId: string;
  analysisId: string;
  accountData: AccountData;
  agentResults?: Record<string, AgentReport>;
  eli5Report?: ELI5Report;
  finalVerdict?: FinalVerdict;
  businessIdentity?: BusinessIdentity;
  advancedAnalysis?: AdvancedAnalysis;
  contentPlan?: ContentPlan;
  sanitizationReport?: SanitizationReport;
  hardValidation?: HardValidation;
  overallScore?: number | null;
  scoreGrade?: string | null;
  recommendations?: string[];
  tier?: string;
  // Custom sections - kullanıcı hangi bölümleri PDF'e dahil etmek istediğini belirler
  customSections?: string[];
}

export interface SanitizationReport {
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
}

export interface HardValidation {
  violations?: Array<{
    rule: string;
    message: string;
  }>;
}

// ============================================================================
// HANDLEBARS HELPERS (Format Functions)
// ============================================================================

function registerHandlebarsHelpers(): void {
  // ============================================================================
  // CUSTOM SECTIONS - Bölüm görünürlük kontrolü için helper
  // ============================================================================
  
  // showSection helper - belirli bir bölümün gösterilip gösterilmeyeceğini kontrol eder
  // Kullanım: {{#showSection "executiveSummary" showAllSections customSections}}...{{/showSection}}
  Handlebars.registerHelper('showSection', function(
    this: any,
    sectionId: string,
    showAllSections: boolean,
    customSections: string[],
    options: any
  ) {
    const shouldShow = showAllSections || (customSections && customSections.includes(sectionId));
    return shouldShow ? options.fn(this) : options.inverse(this);
  });
  
  // ============================================================================
  // GÖREV 1: PDF TEMİZLİK FİLTRESİ
  // ============================================================================
  
  /**
   * Değişken adı filtresi - Ham kod değişkenlerini tespit eder
   * _NOTE, _DISPLAY, camelCaseVariable gibi ham kodları filtreler
   */
  const isVariableNamePattern = (text: string): boolean => {
    if (!text || typeof text !== 'string') return false;
    const variablePatterns = [
      /_NOTE$/i,
      /_DISPLAY$/i,
      /_MAX$/i,
      /_MIN$/i,
      /_RATE$/i,
      /_SCORE$/i,
      /_COUNT$/i,
      /^[A-Z][A-Z_]+[A-Z]$/,  // ALL_CAPS_VARIABLES
      /^[a-z]+[A-Z][a-zA-Z]*$/,  // camelCaseVariables
      /^[a-z]+_[a-z]+/,  // snake_case_variables
      /BRAND_DEAL_RATE/i,
      /ZERO_METRICS/i,
      /NULL_VALUE/i,
    ];
    return variablePatterns.some(pattern => pattern.test(text.trim()));
  };

  /**
   * Zero/null değerler için güvenli format
   * 0, 0.0, null, undefined = "Hesaplanamadı" veya "--"
   */
  const formatZeroSafe = (value: any, placeholder: string = 'Hesaplanamadı'): string => {
    if (value === undefined || value === null) return placeholder;
    if (typeof value === 'number' && (value === 0 || isNaN(value))) return placeholder;
    if (typeof value === 'string' && (value === '0' || value === '0.0' || value === 'null' || value === 'undefined' || value.trim() === '')) return placeholder;
    return String(value);
  };

  // ifEquals helper - eşitlik kontrolü için (template'de kullanılıyor)
  Handlebars.registerHelper('ifEquals', function(this: any, arg1: any, arg2: any, options: any) {
    return (arg1 === arg2) ? options.fn(this) : options.inverse(this);
  });

  // getCategoryBorderColor helper - ELI5 findings kategorilerine göre renk
  Handlebars.registerHelper('getCategoryBorderColor', (category: string | undefined): string => {
    if (!category) return '#64748b';
    const cat = category.toLowerCase();
    if (cat.includes('etkile')) return '#f59e0b';       // Amber - Etkileşim
    if (cat.includes('içerik') || cat.includes('icerik')) return '#8b5cf6';  // Purple - İçerik Kalitesi
    if (cat.includes('büyüme') || cat.includes('buyume') || cat.includes('growth')) return '#10b981';  // Green - Büyüme
    if (cat.includes('görsel') || cat.includes('gorsel') || cat.includes('visual')) return '#3b82f6';  // Blue - Görsel Kimlik
    if (cat.includes('kitle') || cat.includes('audience')) return '#ef4444';  // Red - Kitle Kalitesi
    return '#64748b';  // Default slate
  });

  // Metin filtreleme helper - değişken isimli satırları siler
  Handlebars.registerHelper('filterVariableNames', (text: string): string => {
    if (!text || typeof text !== 'string') return '';
    if (isVariableNamePattern(text)) return '';
    return text;
  });

  // Zero metrics güvenli gösterim
  Handlebars.registerHelper('formatZeroSafe', (value: any, placeholder?: string): string => {
    return formatZeroSafe(value, typeof placeholder === 'string' ? placeholder : '--');
  });

  // Array filtresi - değişken isimli maddeleri siler
  Handlebars.registerHelper('filterVariableArray', (arr: any[]): any[] => {
    if (!arr || !Array.isArray(arr)) return [];
    return arr.filter(item => {
      if (typeof item === 'string') return !isVariableNamePattern(item);
      if (typeof item === 'object' && item !== null) {
        const text = item.finding || item.text || item.description || item.action || item.recommendation || '';
        return !isVariableNamePattern(text);
      }
      return true;
    });
  });

  // Değişken adı kontrolü
  Handlebars.registerHelper('isNotVariableName', (text: string): boolean => {
    return !isVariableNamePattern(text);
  });

  // Format numbers (1000 -> 1K, 1000000 -> 1M)
  Handlebars.registerHelper('formatNumber', (num: number | undefined | null): string => {
    if (num === undefined || num === null || isNaN(num)) return '--';
    if (num === 0) return '--';  // Zero değerler "--" olarak göster
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toLocaleString('tr-TR');
  });

  // Format percentage - Zero kontrolü
  Handlebars.registerHelper('formatPercent', (num: number | undefined | null): string => {
    if (num === undefined || num === null || isNaN(num)) return '--';
    if (num === 0) return '--';  // 0% değerler "--" olarak göster
    return `${num.toFixed(2)}%`;
  });

  // Format growth (+12% or -5%)
  Handlebars.registerHelper('formatGrowth', (num: number | undefined | null): string => {
    if (num === undefined || num === null || isNaN(num)) return 'N/A';
    const sign = num >= 0 ? '+' : '';
    return `${sign}${num.toFixed(1)}%`;
  });

  // GÖREV 1: Format score with "Hesaplanamadı" for zero/null
  Handlebars.registerHelper('formatScoreSafe', (score: any): string => {
    if (score === undefined || score === null) return 'Hesaplanamadı';
    if (typeof score === 'number') {
      if (score === 0 || isNaN(score)) return 'Hesaplanamadı';  // 0.0 değerler "Hesaplanamadı" olarak göster
      if (score > 100) return score.toFixed(0);
      if (score > 10) return score.toFixed(0);
      return score.toFixed(1);
    }
    return String(score);
  });

  // GÖREV 1: Renk senkronizasyonu - Zero değerler gri
  Handlebars.registerHelper('getMetricColorSync', (metricScore: number | undefined, overallScore: number | undefined): string => {
    if (metricScore === undefined || metricScore === null || isNaN(metricScore as number)) return '#9CA3AF';  // Gri - veri yok
    if (metricScore === 0) return '#9CA3AF';  // Gri - hesaplanamadı
    
    // Genel skor 50'nin altındaysa, hiçbir metrik yeşil olamaz
    if (overallScore !== undefined && overallScore < 50) {
      if (metricScore >= 70) return '#F59E0B';  // Yeşil yerine turuncu
      if (metricScore >= 50) return '#F97316';  // Sarı yerine koyu turuncu
      return '#EF4444';  // Kırmızı
    }
    
    // Normal renklendirme
    if (metricScore >= 80) return '#10B981';  // Yeşil
    if (metricScore >= 60) return '#22C55E';  // Açık yeşil
    if (metricScore >= 40) return '#F59E0B';  // Turuncu
    return '#EF4444';  // Kırmızı
  });

  // AŞAMA 4: Metric sınıfı senkronizasyonu
  Handlebars.registerHelper('getMetricClassSync', (metricScore: number | undefined, overallScore: number | undefined): string => {
    if (metricScore === undefined || metricScore === null || isNaN(metricScore as number) || metricScore === 0) return 'neutral';
    
    // Genel skor 50'nin altındaysa, hiçbir metrik success olamaz
    if (overallScore !== undefined && overallScore < 50) {
      if (metricScore >= 60) return 'warning';  // success yerine warning
      return 'danger';
    }
    
    // Normal sınıflandırma
    if (metricScore >= 70) return 'success';
    if (metricScore >= 40) return 'warning';
    return 'danger';
  });

  // Get grade color
  Handlebars.registerHelper('getGradeColor', (grade: string | null | undefined): string => {
    switch (grade?.toUpperCase()) {
      case 'A': case 'A+': return '#10B981';
      case 'B': case 'B+': return '#22C55E';
      case 'C': case 'C+': return '#F59E0B';
      case 'D': case 'D+': return '#F97316';
      case 'F': return '#EF4444';
      default: return '#6B7280';
    }
  });

  // Get metric card class (success/warning/danger)
  Handlebars.registerHelper('getMetricClass', (grade: string | null | undefined): string => {
    switch (grade?.toUpperCase()) {
      case 'A': case 'A+': case 'B': case 'B+': return 'success';
      case 'C': case 'C+': return 'warning';
      case 'D': case 'D+': case 'F': return 'danger';
      default: return '';
    }
  });

  // Get change class (positive/negative)
  Handlebars.registerHelper('getChangeClass', (num: number | undefined | null): string => {
    if (num === undefined || num === null || isNaN(num)) return '';
    return num >= 0 ? 'positive' : 'negative';
  });

  // Get risk class based on score (0-100)
  Handlebars.registerHelper('getRiskClass', (score: number | undefined | null): string => {
    if (score === undefined || score === null || isNaN(score)) return 'low';
    if (score <= 30) return 'low';
    if (score <= 60) return 'medium';
    return 'high';
  });

  // ============================================================================
  // ADVANCED ANALYSIS HELPERS
  // ============================================================================
  
  // Risk level background color
  Handlebars.registerHelper('getRiskBgColor', (level: string | undefined): string => {
    if (!level) return '#f1f5f9';
    const l = level.toLowerCase();
    if (l === 'low' || l === 'düşük') return '#dcfce7';  // Green
    if (l === 'medium' || l === 'orta') return '#fef3c7';  // Yellow
    if (l === 'high' || l === 'yüksek') return '#fed7aa';  // Orange
    if (l === 'critical' || l === 'kritik') return '#fee2e2';  // Red
    return '#f1f5f9';
  });

  // Risk level text color
  Handlebars.registerHelper('getRiskTextColor', (level: string | undefined): string => {
    if (!level) return '#475569';
    const l = level.toLowerCase();
    if (l === 'low' || l === 'düşük') return '#16a34a';
    if (l === 'medium' || l === 'orta') return '#d97706';
    if (l === 'high' || l === 'yüksek') return '#ea580c';
    if (l === 'critical' || l === 'kritik') return '#dc2626';
    return '#475569';
  });

  // Format risk level text
  Handlebars.registerHelper('formatRiskLevel', (level: string | undefined): string => {
    if (!level) return 'Bilinmiyor';
    const l = level.toLowerCase();
    if (l === 'low') return 'Düşük';
    if (l === 'medium') return 'Orta';
    if (l === 'high') return 'Yüksek';
    if (l === 'critical') return 'Kritik';
    if (l === 'unknown') return 'Bilinmiyor';
    return level;
  });

  // Hashtag distribution bar width
  Handlebars.registerHelper('getHashtagBarWidth', (count: number | undefined): number => {
    if (!count || typeof count !== 'number') return 0;
    return Math.min(100, count * 4);  // Max 25 hashtags = 100%
  });

  // Hashtag tier color
  Handlebars.registerHelper('getHashtagColor', (tier: string | undefined): string => {
    if (!tier) return '#64748b';
    const t = tier.toLowerCase();
    if (t === 'mega') return '#8b5cf6';  // Purple
    if (t === 'large') return '#3b82f6';  // Blue
    if (t === 'medium') return '#22c55e';  // Green
    if (t === 'small') return '#f59e0b';  // Yellow
    if (t === 'micro') return '#f97316';  // Orange
    return '#64748b';
  });

  // Content format key formatter
  Handlebars.registerHelper('formatContentKey', (key: string | undefined): string => {
    if (!key) return '';
    const keyMap: Record<string, string> = {
      'reels': 'Reels',
      'carousel': 'Carousel',
      'single_post': 'Tek Post',
      'stories': 'Stories',
    };
    return keyMap[key.toLowerCase()] || key;
  });

  // Content format color
  Handlebars.registerHelper('getContentColor', (format: string | undefined): string => {
    if (!format) return '#64748b';
    const f = format.toLowerCase();
    if (f === 'reels') return '#ec4899';  // Pink
    if (f === 'carousel') return '#3b82f6';  // Blue
    if (f === 'single_post') return '#64748b';  // Slate
    if (f === 'stories') return '#f59e0b';  // Amber
    return '#64748b';
  });

  // Viral factor label formatter
  Handlebars.registerHelper('formatViralFactor', (factor: string | undefined): string => {
    if (!factor) return '';
    const factorMap: Record<string, string> = {
      'content_quality': 'İçerik Kalitesi',
      'timing': 'Zamanlama',
      'hashtag_strategy': 'Hashtag',
      'engagement_rate': 'Etkileşim',
    };
    return factorMap[factor.toLowerCase()] || factor.replace(/_/g, ' ');
  });

  // Priority badge class
  Handlebars.registerHelper('getPriorityBadge', (priority: string | undefined): string => {
    if (!priority) return 'badge-slate';
    const p = priority.toLowerCase();
    if (p === 'critical' || p === 'kritik') return 'badge-red';
    if (p === 'high' || p === 'yüksek') return 'badge-amber';
    if (p === 'medium' || p === 'orta') return 'badge-blue';
    return 'badge-slate';
  });

  // Format priority text
  Handlebars.registerHelper('formatPriority', (priority: string | undefined): string => {
    if (!priority) return '';
    const p = priority.toLowerCase();
    if (p === 'critical') return 'Kritik';
    if (p === 'high') return 'Yüksek';
    if (p === 'medium') return 'Orta';
    if (p === 'low') return 'Düşük';
    return priority;
  });

  // Risk badge class (for risk levels)
  Handlebars.registerHelper('getRiskBadgeClass', (level: string | undefined): string => {
    if (!level) return 'badge-slate';
    const l = level.toLowerCase();
    if (l === 'low' || l === 'düşük') return 'badge-green';
    if (l === 'medium' || l === 'orta') return 'badge-amber';
    if (l === 'high' || l === 'yüksek') return 'badge-red';
    if (l === 'critical' || l === 'kritik') return 'badge-red';
    return 'badge-slate';
  });

  // Get ELI5 card class (issue/strength/neutral)
  Handlebars.registerHelper('getELI5Class', (verdict: string | undefined): string => {
    if (!verdict) return 'neutral';
    const lower = verdict.toLowerCase();
    if (lower.includes('mükemmel') || lower.includes('iyi') || lower.includes('güçlü')) return 'strength';
    if (lower.includes('zayıf') || lower.includes('kötü') || lower.includes('sorun')) return 'issue';
    return 'neutral';
  });

  // Extract text from object or string
  Handlebars.registerHelper('extractText', (item: any): string => {
    if (typeof item === 'string') return item;
    return item?.finding || item?.description || item?.text || item?.action || item?.recommendation || '';
  });

  // Join array with separator
  Handlebars.registerHelper('join', (arr: string[] | undefined, separator: string): string => {
    if (!arr || !Array.isArray(arr)) return '';
    return arr.join(separator);
  });

  // Format date
  Handlebars.registerHelper('formatDate', (date: Date | string | undefined): string => {
    if (!date) return new Date().toLocaleDateString('tr-TR');
    const d = typeof date === 'string' ? new Date(date) : date;
    return d.toLocaleDateString('tr-TR', { year: 'numeric', month: 'long', day: 'numeric' });
  });

  // Equality check
  Handlebars.registerHelper('eq', function(a: any, b: any) {
    return a === b;
  });

  // Get initial letter from username
  Handlebars.registerHelper('getInitial', (username: string | undefined): string => {
    if (!username) return '?';
    return username.charAt(0).toUpperCase();
  });

  // Get category class (critical/warning/success)
  Handlebars.registerHelper('getCategoryClass', (category: string | undefined): string => {
    if (!category) return '';
    const lower = category.toLowerCase();
    if (lower.includes('kritik') || lower.includes('sorun') || lower.includes('zayif') || lower.includes('hata')) return 'critical';
    if (lower.includes('uyari') || lower.includes('dikkat') || lower.includes('gelisim')) return 'warning';
    if (lower.includes('guclu') || lower.includes('basari') || lower.includes('iyi')) return 'success';
    return '';
  });

  // Get category icon
  Handlebars.registerHelper('getCategoryIcon', (category: string | undefined): string => {
    if (!category) return '📋';
    const lower = category.toLowerCase();
    if (lower.includes('hook') || lower.includes('icerik')) return '🎯';
    if (lower.includes('etkilesim') || lower.includes('engagement')) return '💬';
    if (lower.includes('takipci') || lower.includes('buyume') || lower.includes('growth')) return '📈';
    if (lower.includes('marka') || lower.includes('brand')) return '🏷️';
    if (lower.includes('gorsel') || lower.includes('visual')) return '🎨';
    if (lower.includes('strateji') || lower.includes('strategy')) return '📊';
    if (lower.includes('kitle') || lower.includes('audience')) return '👥';
    if (lower.includes('satis') || lower.includes('sales')) return '💰';
    if (lower.includes('kritik') || lower.includes('sorun')) return '⚠️';
    if (lower.includes('basari') || lower.includes('guclu')) return '✅';
    return '📌';
  });

  // Check if value is a number
  Handlebars.registerHelper('isNumber', (value: any): boolean => {
    return typeof value === 'number' && !isNaN(value);
  });

  // Format score (handle numbers)
  Handlebars.registerHelper('formatScore', (score: any): string => {
    if (score === undefined || score === null) return '-';
    if (typeof score === 'number') {
      if (score > 100) return score.toFixed(0);
      if (score > 10) return score.toFixed(0);
      return score.toFixed(1);
    }
    return String(score);
  });

  // Format metric key (camelCase to readable) - GÖREV 1: Değişken filtresi
  Handlebars.registerHelper('formatKey', (key: string | undefined): string => {
    if (!key) return '';
    
    // Değişken isim filtresi - _NOTE, _DISPLAY gibi son ekleri filtrele
    const filterPatterns = [/_NOTE$/i, /_DISPLAY$/i, /_MAX$/i, /_MIN$/i, /_RATE$/i, /_internal$/i];
    if (filterPatterns.some(p => p.test(key))) return '';
    
    // ALL_CAPS_VARIABLES filtresi
    if (/^[A-Z][A-Z_]+[A-Z]$/.test(key)) return '';
    
    // camelCase to "Camel Case"
    return key
      .replace(/([A-Z])/g, ' $1')
      .replace(/^./, str => str.toUpperCase())
      .trim();
  });

  // Extract finding text from various structures - GÖREV 1: Değişken filtresi
  Handlebars.registerHelper('extractFinding', (item: any): string => {
    let text = '';
    if (typeof item === 'string') text = item;
    else if (item?.finding) text = item.finding;
    else if (item?.issue) text = item.issue;
    else if (item?.description) text = item.description;
    else if (item?.text) text = item.text;
    else if (item?.recommendation) text = item.recommendation;
    else if (item?.action) text = item.action;
    else if (item?.insight) text = item.insight;
    else if (item?.observation) text = item.observation;
    
    // Değişken isim filtresi - _NOTE, _DISPLAY, camelCase vb.
    if (text) {
      const variablePatterns = [/_NOTE$/i, /_DISPLAY$/i, /_MAX$/i, /_MIN$/i, /^[A-Z][A-Z_]+[A-Z]$/, /BRAND_DEAL_RATE/i];
      if (variablePatterns.some(p => p.test(text.trim()))) return '';
    }
    return text;
  });

  // Check if string looks like unparsed JSON (to filter out)
  Handlebars.registerHelper('isJsonString', (str: any): boolean => {
    if (typeof str !== 'string') return false;
    const trimmed = str.trim();
    return trimmed.startsWith('{') || trimmed.startsWith('[') || trimmed.startsWith('"');
  });

  // Get health status text
  Handlebars.registerHelper('getHealthStatus', (score: number | undefined | null): string => {
    if (score === undefined || score === null || isNaN(score)) return 'Bilinmiyor';
    if (score >= 70) return '🟢 İyi Performans';
    if (score >= 40) return '🟡 Geliştirilmeli';
    return '🔴 Kritik - Aksiyon Gerekli';
  });

  // Get health class for CSS
  Handlebars.registerHelper('getHealthClass', (score: number | undefined | null): string => {
    if (score === undefined || score === null || isNaN(score)) return 'medium';
    if (score >= 70) return 'good';
    if (score >= 40) return 'medium';
    return 'poor';
  });

  // Greater than comparison
  Handlebars.registerHelper('gt', (a: any, b: any): boolean => {
    return Number(a) > Number(b);
  });

  // Get business card class
  Handlebars.registerHelper('getBusinessClass', (type: string | undefined): string => {
    if (!type) return 'personal';
    const t = type.toLowerCase();
    if (t.includes('service') || t.includes('business') || t.includes('hizmet')) return 'service';
    if (t.includes('creator') || t.includes('influencer') || t.includes('içerik')) return 'creator';
    return 'personal';
  });

  // Get verdict class (good/medium/bad)
  Handlebars.registerHelper('getVerdictClass', (verdict: string | undefined): string => {
    if (!verdict) return 'medium';
    const v = verdict.toLowerCase();
    if (v.includes('iyi') || v.includes('good') || v.includes('olumlu') || v.includes('mükemmel')) return 'good';
    if (v.includes('kötü') || v.includes('bad') || v.includes('kritik') || v.includes('zayıf')) return 'bad';
    return 'medium';
  });

  // Get verdict badge class
  Handlebars.registerHelper('getVerdictBadgeClass', (verdict: string | undefined): string => {
    if (!verdict) return 'badge-amber';
    const v = verdict.toLowerCase();
    if (v.includes('iyi') || v.includes('good') || v.includes('olumlu')) return 'badge-green';
    if (v.includes('kötü') || v.includes('bad') || v.includes('kritik')) return 'badge-red';
    return 'badge-amber';
  });

  // Get difficulty badge class
  Handlebars.registerHelper('getDifficultyBadge', (difficulty: string | undefined): string => {
    if (!difficulty) return 'badge-slate';
    const d = difficulty.toLowerCase();
    if (d.includes('kolay') || d.includes('easy')) return 'badge-green';
    if (d.includes('orta') || d.includes('medium')) return 'badge-amber';
    return 'badge-red';
  });

  // Math helper for index + 1
  Handlebars.registerHelper('math', (a: number, operator: string, b: number): number => {
    if (operator === '+') return a + b;
    if (operator === '-') return a - b;
    if (operator === '*') return a * b;
    if (operator === '/') return a / b;
    return a;
  });

  // Agent metadata helpers
  const agentTitles: Record<string, string> = {
    domainMaster: 'Sektör Analizi',
    growthVirality: 'Büyüme ve Viral Strateji',
    salesConversion: 'Monetizasyon ve Satış',
    visualBrand: 'Görsel Marka Kimliği',
    communityLoyalty: 'Topluluk ve Sadakat',
    attentionArchitect: 'Dikkat ve Hook Optimizasyonu',
    systemGovernor: 'Veri Doğrulama',
  };

  const agentRoles: Record<string, string> = {
    domainMaster: 'Sektör ve Niş Analiz Uzmanı',
    growthVirality: 'Büyüme ve Viral Strateji Uzmanı',
    salesConversion: 'Monetizasyon ve Satış Uzmanı',
    visualBrand: 'Görsel Marka Kimliği Uzmanı',
    communityLoyalty: 'Topluluk ve Sadakat Stratejisti',
    attentionArchitect: 'Dikkat ve Hook Optimizasyon Uzmanı',
    systemGovernor: 'Veri Doğrulama ve Güvenlik Uzmanı',
  };

  const agentColors: Record<string, string> = {
    domainMaster: 'purple',
    growthVirality: 'green',
    salesConversion: 'amber',
    visualBrand: 'pink',
    communityLoyalty: 'red',
    attentionArchitect: 'blue',
    systemGovernor: 'slate',
  };

  Handlebars.registerHelper('getAgentTitle', (key: string, fallback: string): string => {
    return agentTitles[key] || fallback || key;
  });

  Handlebars.registerHelper('getAgentRole', (key: string, fallback: string): string => {
    return agentRoles[key] || fallback || '';
  });

  Handlebars.registerHelper('getAgentColor', (key: string): string => {
    return agentColors[key] || 'blue';
  });

  // Format metric value
  Handlebars.registerHelper('formatMetricValue', (value: any): string => {
    if (value === undefined || value === null) return '-';
    if (typeof value === 'number') {
      if (value > 1000000) return `${(value / 1000000).toFixed(1)}M`;
      if (value > 1000) return `${(value / 1000).toFixed(1)}K`;
      if (value > 100) return value.toFixed(0);
      if (value > 10) return value.toFixed(0);
      return value.toFixed(1);
    }
    return String(value);
  });

  // Bot score color helper
  Handlebars.registerHelper('getBotScoreColor', (score: number | undefined | null): string => {
    if (score === undefined || score === null || isNaN(score)) return '#64748b';
    return score > 50 ? '#ef4444' : '#16a34a';
  });

  // Phase helpers for sanitization report
  Handlebars.registerHelper('getPhaseColor', (phase: string | undefined): string => {
    if (!phase) return '#64748b';
    const p = phase.toLowerCase();
    if (p.includes('rescue')) return '#ef4444';  // Red
    if (p.includes('growth')) return '#f59e0b';  // Amber
    if (p.includes('monetization')) return '#10b981';  // Green
    return '#64748b';
  });

  Handlebars.registerHelper('getPhaseTextColor', (phase: string | undefined): string => {
    if (!phase) return '#475569';
    const p = phase.toLowerCase();
    if (p.includes('rescue')) return '#991b1b';  // Dark red
    if (p.includes('growth')) return '#92400e';  // Dark amber
    if (p.includes('monetization')) return '#065f46';  // Dark green
    return '#475569';
  });

  Handlebars.registerHelper('getPhaseIcon', (phase: string | undefined): string => {
    if (!phase) return '📊';
    const p = phase.toLowerCase();
    if (p.includes('rescue')) return '🚨';
    if (p.includes('growth')) return '📈';
    if (p.includes('monetization')) return '💰';
    return '📊';
  });

  // Score color helper
  Handlebars.registerHelper('getScoreColor', (score: number | undefined | null): string => {
    if (score === undefined || score === null || isNaN(score)) return '#64748b';
    if (score >= 80) return '#10b981';  // Green
    if (score >= 60) return '#22c55e';  // Light green
    if (score >= 40) return '#f59e0b';  // Amber
    return '#ef4444';  // Red
  });

  // Ghost follower color
  Handlebars.registerHelper('getGhostColor', (percent: number | undefined | null): string => {
    if (percent === undefined || percent === null || isNaN(percent)) return '#64748b';
    if (percent <= 10) return '#10b981';  // Good - green
    if (percent <= 20) return '#f59e0b';  // Medium - amber
    return '#ef4444';  // Bad - red
  });

  // Score badge class
  Handlebars.registerHelper('getScoreBadgeClass', (score: number | undefined | null): string => {
    if (score === undefined || score === null || isNaN(score)) return 'badge-slate';
    if (score >= 80) return 'badge-green';
    if (score >= 60) return 'badge-blue';
    if (score >= 40) return 'badge-amber';
    return 'badge-red';
  });

  // ============================================================================
  // CORIUM-STYLE: CONFIDENCE-DRIVEN LANGUAGE HELPERS
  // ============================================================================
  
  /**
   * Confidence-Driven Language: Güvenilirlik skoruna göre dil tonu değişir
   * HIGH (≥0.80): Kesin, güçlü ifadeler
   * MEDIUM (0.60-0.79): Dengeli, dikkatli ifadeler
   * LOW (<0.60): Sınırlı veri uyarısı
   */
  Handlebars.registerHelper('getConfidenceLevel', (score: number | undefined | null): string => {
    if (score === undefined || score === null || isNaN(score)) return 'low';
    if (score >= 80) return 'high';
    if (score >= 60) return 'medium';
    return 'low';
  });

  Handlebars.registerHelper('getConfidenceText', (score: number | undefined | null): string => {
    if (score === undefined || score === null || isNaN(score)) return 'Sınırlı Veri';
    if (score >= 80) return 'Yüksek Güvenilirlik';
    if (score >= 60) return 'Orta Güvenilirlik';
    return 'Düşük Güvenilirlik';
  });

  Handlebars.registerHelper('getConfidenceBadge', (score: number | undefined | null): string => {
    if (score === undefined || score === null || isNaN(score)) return 'badge-slate';
    if (score >= 80) return 'badge-green';
    if (score >= 60) return 'badge-amber';
    return 'badge-red';
  });

  // Confidence-driven metric açıklaması
  Handlebars.registerHelper('getConfidencePhrase', (confidence: number | undefined, metricName: string): string => {
    const name = metricName || 'Bu metrik';
    if (confidence === undefined || confidence === null || isNaN(confidence)) {
      return `${name} için yeterli veri bulunamadı.`;
    }
    if (confidence >= 80) {
      return `${name} güvenilir verilerle doğrulanmıştır.`;
    }
    if (confidence >= 60) {
      return `${name} mevcut verilere göre hesaplanmıştır.`;
    }
    return `${name} sınırlı veriyle tahmin edilmiştir.`;
  });

  // Tier-based content control
  Handlebars.registerHelper('isTierAllowed', (tier: string | undefined, requiredTier: string): boolean => {
    const tierLevels: Record<string, number> = { 'free': 0, 'standard': 1, 'premium': 2 };
    const userTier = tierLevels[(tier || 'free').toLowerCase()] || 0;
    const required = tierLevels[requiredTier.toLowerCase()] || 0;
    return userTier >= required;
  });

  // SWOT item type helper
  Handlebars.registerHelper('getSwotClass', (type: string | undefined): string => {
    if (!type) return '';
    const t = type.toLowerCase();
    if (t.includes('strength') || t.includes('güç')) return 'success';
    if (t.includes('weakness') || t.includes('zayıf')) return 'danger';
    if (t.includes('opportunity') || t.includes('fırsat')) return 'info';
    if (t.includes('threat') || t.includes('tehdit')) return 'warning';
    return '';
  });

  Handlebars.registerHelper('getSwotIcon', (type: string | undefined): string => {
    if (!type) return '📋';
    const t = type.toLowerCase();
    if (t.includes('strength') || t.includes('güç')) return '💪';
    if (t.includes('weakness') || t.includes('zayıf')) return '⚠️';
    if (t.includes('opportunity') || t.includes('fırsat')) return '🚀';
    if (t.includes('threat') || t.includes('tehdit')) return '🛡️';
    return '📋';
  });

  // Format correction value (handle objects)
  Handlebars.registerHelper('formatCorrectionValue', (value: any): string => {
    if (value === undefined || value === null) return '-';
    if (typeof value === 'object') {
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  });

  // ============================================================================
  // V2 TEMPLATE HELPERS
  // ============================================================================

  // First letter helper for avatar fallback
  Handlebars.registerHelper('firstLetter', (text: string | undefined): string => {
    if (!text) return '?';
    return text.charAt(0).toUpperCase();
  });

  // toLowerCase helper
  Handlebars.registerHelper('toLowerCase', (text: string | undefined): string => {
    if (!text) return '';
    return text.toLowerCase();
  });

  // Truncate helper
  Handlebars.registerHelper('truncate', (text: string | undefined, length: number): string => {
    if (!text) return '';
    if (text.length <= length) return text;
    return text.substring(0, length) + '...';
  });

  // Format K helper (for thousands)
  Handlebars.registerHelper('formatK', (num: number | undefined | null): string => {
    if (num === undefined || num === null || isNaN(num)) return '--';
    if (num === 0) return '--';
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toLocaleString('tr-TR');
  });

  // Array length check helper
  Handlebars.registerHelper('hasItems', (arr: any[] | undefined): boolean => {
    return Array.isArray(arr) && arr.length > 0;
  });
}

// ============================================================================
// PDF GENERATOR CLASS
// ============================================================================

export class ModernPDFGenerator {
  private browser: Browser | null = null;
  private template: HandlebarsTemplateDelegate | null = null;
  private cssContent: string = '';

  constructor() {
    registerHandlebarsHelpers();
  }

  /**
   * Initialize Puppeteer browser and load template
   */
  async initialize(): Promise<void> {
    // Load Handlebars template - V2 template with modern design
    const templatePath = path.join(__dirname, '..', 'templates', 'report_template_v2.html');
    const templateContent = await fs.readFile(templatePath, 'utf-8');
    this.template = Handlebars.compile(templateContent);

    // Load CSS (for inline injection)
    const cssPath = path.join(__dirname, '..', 'styles', 'pdf_styles.css');
    this.cssContent = await fs.readFile(cssPath, 'utf-8');

    // Launch headless browser
    this.browser = await puppeteer.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-web-security',
      ],
    });
  }

  /**
   * Generate PDF from payload
   * 🔥 V2: dataSanitizer ile tam temizlik ve Frontend uyumu
   */
  async generatePDF(payload: GeneratePayload): Promise<Buffer> {
    if (!this.browser || !this.template) {
      await this.initialize();
    }

    // 🧹 V2: Sanitize payload with dataSanitizer - Frontend ile tam uyum
    const sanitized: SanitizedPayload = sanitizePayload(payload);
    
    // Custom sections - hangi bölümlerin gösterileceğini belirle
    const customSections = payload.customSections || [];
    const showAllSections = customSections.length === 0;
    
    // Section visibility helper
    const shouldShowSection = (sectionId: string): boolean => {
      return showAllSections || customSections.includes(sectionId);
    };
    
    // V2 Template'e gönderilecek temiz payload
    const processedPayload = {
      // Account data (sanitized)
      username: sanitized.username,
      displayName: sanitized.displayName,
      profilePicUrl: sanitized.profilePicUrl,
      bio: sanitized.bio,
      isVerified: sanitized.isVerified,
      isBusiness: sanitized.isBusiness,
      
      // Metrics (sanitized with display flags)
      followers: sanitized.followers,
      following: sanitized.following,
      posts: sanitized.posts,
      engagementRate: sanitized.engagementRate,
      avgLikes: sanitized.avgLikes,
      avgComments: sanitized.avgComments,
      botScore: sanitized.botScore,
      
      // Scores (sanitized)
      overallScore: sanitized.overallScore,
      scoreGrade: sanitized.scoreGrade,
      healthStatus: sanitized.healthStatus,
      healthClass: sanitized.healthClass,
      
      // Business Identity (sanitized)
      accountType: shouldShowSection('businessIdentity') ? sanitized.accountType : null,
      accountTypeExplanation: shouldShowSection('businessIdentity') ? sanitized.accountTypeExplanation : null,
      correctMetrics: shouldShowSection('businessIdentity') ? sanitized.correctMetrics : [],
      wrongMetrics: shouldShowSection('businessIdentity') ? sanitized.wrongMetrics : [],
      isServiceProvider: sanitized.isServiceProvider,
      
      // Agents (sanitized)
      agents: shouldShowSection('agents') ? sanitized.agents : [],
      
      // Reports (sanitized)
      eli5: shouldShowSection('eli5Report') ? sanitized.eli5 : null,
      finalVerdict: shouldShowSection('finalVerdict') ? sanitized.finalVerdict : null,
      contentPlan: shouldShowSection('contentPlan') || shouldShowSection('contentCalendar') ? sanitized.contentPlan : null,
      
      // Advanced Analysis (NEW)
      advancedAnalysis: shouldShowSection('advancedAnalysis') || shouldShowSection('contentStrategy') || shouldShowSection('riskAssessment') 
        ? sanitized.advancedAnalysis : null,
      
      // Sanitization Report (NEW)
      sanitizationReport: sanitized.sanitizationReport,
      
      // Hard Validation (NEW)
      hardValidation: sanitized.hardValidation,
      
      // Metadata
      analysisDate: sanitized.analysisDate,
      reportId: sanitized.reportId,
      tier: sanitized.tier,
      
      // Section visibility flags
      showAllSections,
      showExecutiveSummary: shouldShowSection('executiveSummary'),
      showOverallScore: shouldShowSection('overallScore'),
      showAccountMetrics: shouldShowSection('accountMetrics'),
      showBusinessIdentity: shouldShowSection('businessIdentity'),
      showFinalVerdict: shouldShowSection('finalVerdict'),
      showEli5Report: shouldShowSection('eli5Report'),
      showContentPlan: shouldShowSection('contentPlan') || shouldShowSection('contentCalendar'),
      showAgents: shouldShowSection('agents'),
      showAdvancedAnalysis: shouldShowSection('advancedAnalysis') || shouldShowSection('contentStrategy') || shouldShowSection('riskAssessment'),
    };

    // Render HTML from template
    const html = this.template!(processedPayload);

    // Inject CSS directly into HTML (avoid file path issues)
    const htmlWithCSS = html.replace(
      '<link rel="stylesheet" href="../styles/pdf_styles.css">',
      `<style>${this.cssContent}</style>`
    );

    // Create new page
    const page = await this.browser!.newPage();

    // Set content with longer timeout for profile images
    await page.setContent(htmlWithCSS, {
      waitUntil: ['networkidle0', 'load', 'domcontentloaded'],
      timeout: 30000,
    });

    // Wait for images to load
    await page.evaluate(() => {
      return new Promise<void>((resolve) => {
        const images = Array.from(document.querySelectorAll('img'));
        if (images.length === 0) {
          resolve();
          return;
        }
        let loadedCount = 0;
        const checkComplete = () => {
          loadedCount++;
          if (loadedCount >= images.length) resolve();
        };
        images.forEach(img => {
          if (img.complete) {
            checkComplete();
          } else {
            img.onload = checkComplete;
            img.onerror = checkComplete;
          }
        });
        setTimeout(resolve, 3000); // Max 3 second wait
      });
    });

    // PDF generation options
    const pdfOptions: PDFOptions = {
      format: 'A4',
      printBackground: true,
      margin: {
        top: '0mm',
        right: '0mm',
        bottom: '0mm',
        left: '0mm',
      },
      preferCSSPageSize: true,
    };

    // Generate PDF
    const pdfBuffer = await page.pdf(pdfOptions);

    // Close page
    await page.close();

    return Buffer.from(pdfBuffer);
  }

  /**
   * Close browser instance
   */
  async close(): Promise<void> {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }
}

// ============================================================================
// SINGLETON INSTANCE (For Reuse)
// ============================================================================

let generatorInstance: ModernPDFGenerator | null = null;

export async function getGeneratorInstance(): Promise<ModernPDFGenerator> {
  if (!generatorInstance) {
    generatorInstance = new ModernPDFGenerator();
    await generatorInstance.initialize();
  }
  return generatorInstance;
}

export async function cleanupGenerator(): Promise<void> {
  if (generatorInstance) {
    await generatorInstance.close();
    generatorInstance = null;
  }
}

// ============================================================================
// MAIN EXPORT FUNCTION (Backwards Compatible)
// ============================================================================

export async function generatePDF(payload: GeneratePayload): Promise<Buffer> {
  const generator = await getGeneratorInstance();
  return await generator.generatePDF(payload);
}
