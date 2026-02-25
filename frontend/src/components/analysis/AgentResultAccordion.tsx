import { 
  ChevronDownIcon, 
  ShieldIcon, 
  TargetIcon, 
  LightningIcon, 
  TrendingUpIcon, 
  UsersIcon, 
  EyeIcon, 
  PaletteIcon, 
  HeartIcon, 
  DollarSignIcon, 
  AlertTriangleIcon, 
  CheckCircleIcon, 
  InfoIcon, 
  BarChart3Icon, 
  LightbulbIcon, 
  ArrowRightIcon 
} from '@/components/icons';
import { useState, useMemo } from 'react';
import { useTranslation } from '@/i18n/TranslationProvider';
import { ReelsScenarioCard } from './ReelsScenarioCard';  // 🎬 GÖREV 2: Import scenario card

/**
 * CRITICAL: React Error #31 Fix
 * Bu fonksiyon objeleri güvenli bir şekilde string'e çevirir.
 * Objects are not valid as React children hatası için gerekli.
 */
function safeRenderValue(value: any): string {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  if (Array.isArray(value)) {
    return value.map(v => safeRenderValue(v)).filter(Boolean).join(', ');
  }
  if (typeof value === 'object') {
    // Obje ise anlamlı bir şekilde formatla
    const entries = Object.entries(value);
    if (entries.length === 0) return '';
    
    // Bazı özel alanları kontrol et
    if ('format' in value && 'examples' in value) {
      // Template objesi - format, examples, technique, cta_placement içerir
      const parts: string[] = [];
      if (value.technique) parts.push(`Teknik: ${typeof value.technique === 'string' ? value.technique : safeRenderValue(value.technique)}`);
      if (value.format) parts.push(`Format: ${typeof value.format === 'string' ? value.format : safeRenderValue(value.format)}`);
      if (value.examples && Array.isArray(value.examples)) {
        const examplesStr = value.examples.map((ex: any) => typeof ex === 'string' ? ex : safeRenderValue(ex)).join(', ');
        parts.push(`Örnekler: ${examplesStr}`);
      }
      if (value.cta_placement) parts.push(`CTA Konumu: ${typeof value.cta_placement === 'string' ? value.cta_placement : safeRenderValue(value.cta_placement)}`);
      return parts.join(' | ');
    }
    
    if ('soft_cta' in value || 'growth_cta' in value) {
      // CTA template objesi
      const parts: string[] = [];
      if (value.soft_cta) parts.push(`💾 ${typeof value.soft_cta === 'string' ? value.soft_cta : safeRenderValue(value.soft_cta)}`);
      if (value.engagement_cta) parts.push(`💬 ${typeof value.engagement_cta === 'string' ? value.engagement_cta : safeRenderValue(value.engagement_cta)}`);
      if (value.growth_cta) parts.push(`📈 ${typeof value.growth_cta === 'string' ? value.growth_cta : safeRenderValue(value.growth_cta)}`);
      if (value.conversion_cta) parts.push(`🎯 ${typeof value.conversion_cta === 'string' ? value.conversion_cta : safeRenderValue(value.conversion_cta)}`);
      if (value.placement) parts.push(`📍 Konum: ${typeof value.placement === 'string' ? value.placement : safeRenderValue(value.placement)}`);
      return parts.join(' | ');
    }
    
    // Genel obje - key=value formatında döndür
    return entries
      .map(([k, v]) => `${k}: ${typeof v === 'object' ? JSON.stringify(v) : v}`)
      .join(' | ');
  }
  return String(value);
}

// Extended AgentResult type to handle all possible fields from orchestrator
interface ExtendedAgentResult {
  findings?: string[] | string | any;
  recommendations?: string[] | string | any;
  metrics?: Record<string, any>;
  alerts?: string[];
  agentName?: string;
  agentRole?: string;
  error?: boolean;
  errorType?: string;
  errorMessage?: string;
  modelUsed?: string;
  timestamp?: string;
  fallback?: boolean;
  vetoed?: boolean;
  vetoReason?: string;
  [key: string]: any;
}

interface AgentResultAccordionProps {
  agentKey: string;
  result: ExtendedAgentResult;
  defaultOpen?: boolean;
}

// Agent metadata with detailed Turkish descriptions
const agentMeta: Record<string, { icon: any; color: string; bgGradient: string; description: string; role: string }> = {
  domainMaster: {
    icon: TargetIcon,
    color: 'bg-purple-100 text-purple-600 border-purple-200',
    bgGradient: 'from-purple-50 to-violet-50',
    description: 'Sektör pozisyonunuzu, niş pazar fırsatlarını, rekabet dinamiklerini ve içerik stratejinizi derinlemesine analiz ederek pazar konumlandırmanızı optimize etmenizi sağlar. Rakiplerinizi inceleyerek sizi farklı kılacak benzersiz değer önerileri sunar.',
    role: 'Sektör ve Niş Analiz Uzmanı'
  },
  growthVirality: {
    icon: TrendingUpIcon,
    color: 'bg-green-100 text-green-600 border-green-200',
    bgGradient: 'from-green-50 to-emerald-50',
    description: 'Organik büyüme potansiyelinizi, viral içerik fırsatlarını, takipçi kazanma stratejilerini ve algoritma uyumunuzu analiz eder. Rakiplerinizle büyüme oranı karşılaştırması yapar ve 6 aylık projeksiyon sunar.',
    role: 'Büyüme ve Viral Strateji Uzmanı'
  },
  salesConversion: {
    icon: DollarSignIcon,
    color: 'bg-amber-100 text-amber-600 border-amber-200',
    bgGradient: 'from-amber-50 to-orange-50',
    description: 'Monetizasyon hazırlığınızı, marka anlaşması potansiyelinizi, affiliate marketing fırsatlarını ve gelir akışlarınızı analiz eder. Fiyatlandırma önerileri ve satış hunisi optimizasyonları sunar.',
    role: 'Monetizasyon ve Satış Uzmanı'
  },
  visualBrand: {
    icon: PaletteIcon,
    color: 'bg-pink-100 text-pink-600 border-pink-200',
    bgGradient: 'from-pink-50 to-rose-50',
    description: 'Görsel tutarlılığınızı, renk paletinizi, tipografi kullanımınızı, grid estetiğinizi ve marka kimliği algısını değerlendirir. Profesyonel görsel standartlara ulaşmanız için somut öneriler sunar.',
    role: 'Görsel Marka Kimliği Uzmanı'
  },
  communityLoyalty: {
    icon: HeartIcon,
    color: 'bg-red-100 text-red-600 border-red-200',
    bgGradient: 'from-red-50 to-rose-50',
    description: 'Topluluk sağlığınızı, takipçi sadakatini, etkileşim kalitesini ve superfan oranınızı ölçer. Ambassador programı önerileri ve topluluk ritüelleri ile sadakati artırma stratejileri sunar.',
    role: 'Topluluk ve Sadakat Stratejisti'
  },
  attentionArchitect: {
    icon: EyeIcon,
    color: 'bg-blue-100 text-blue-600 border-blue-200',
    bgGradient: 'from-blue-50 to-sky-50',
    description: 'Hook etkinliğinizi, ilk 3 saniye performansını, dikkat çekme gücünüzü, scroll durdurucu elementleri ve içerik tutma oranlarını analiz eder. Viral hook formülleri ve caption şablonları sunar.',
    role: 'Dikkat ve Hook Optimizasyon Uzmanı'
  },
  systemGovernor: {
    icon: ShieldIcon,
    color: 'bg-slate-100 text-slate-600 border-slate-200',
    bgGradient: 'from-slate-50 to-gray-50',
    description: 'Hesap güvenilirliğini, bot/sahte takipçi oranını, veri tutarlılığını ve diğer agent çıktılarının doğruluğunu denetler. Çelişkili verileri tespit eder ve düzeltir.',
    role: 'Veri Doğrulama ve Güvenlik Uzmanı'
  },
};

const defaultMeta = {
  icon: LightningIcon,
  color: 'bg-primary-100 text-primary-600 border-primary-200',
  bgGradient: 'from-primary-50 to-blue-50',
  description: 'Detaylı analiz sonuçları ve öneriler',
  role: 'AI Analiz Uzmanı'
};

// Helper function to parse nested object strings like "@{key=value; key2=value2}"
function parseNestedString(value: any): Record<string, any> | any {
  if (typeof value !== 'string') return value;
  
  // Check if it's a nested object string
  if (value.startsWith('@{') && value.endsWith('}')) {
    try {
      const inner = value.slice(2, -1);
      const pairs = inner.split('; ');
      const result: Record<string, any> = {};
      
      for (const pair of pairs) {
        const eqIndex = pair.indexOf('=');
        if (eqIndex > 0) {
          const key = pair.slice(0, eqIndex).trim();
          let val: any = pair.slice(eqIndex + 1).trim();
          
          // Try to parse nested values recursively
          if (val.startsWith('@{')) {
            val = parseNestedString(val);
          } else if (val.startsWith('System.Object[]')) {
            val = [];
          } else if (val === '' || val === 'null' || val === 'None') {
            val = null;
          } else if (!isNaN(Number(val)) && val !== '') {
            val = Number(val);
          }
          
          result[key] = val;
        }
      }
      return result;
    } catch {
      return value;
    }
  }
  return value;
}

// Format a complex finding object to human-readable text
function formatFindingObject(obj: any): { text: string; type: string; category?: string; impact_score?: number; evidence?: string } {
  // Handle specificity-enhanced findings from ELI5 formatter
  if (obj.issue && obj.fix_action) {
    const text = obj.original || obj.issue;
    const type = obj.type === 'phase_enforcement' ? 'warning' : 'finding';
    // Template objesi varsa güvenli şekilde render et
    const templateEvidence = obj.template ? safeRenderValue(obj.template) : undefined;
    return {
      text: `${text}${obj.expected_impact ? ` (Beklenen: ${typeof obj.expected_impact === 'string' ? obj.expected_impact : safeRenderValue(obj.expected_impact)})` : ''}`,
      type,
      category: typeof obj.fix_action === 'string' ? obj.fix_action : safeRenderValue(obj.fix_action),
      evidence: templateEvidence
    };
  }
  
  // Handle phase enforcement findings
  if (obj.type === 'phase_enforcement') {
    return {
      text: `${obj.issue || 'Faz Uyarısı'}: ${safeRenderValue(obj.fix_action) || ''}${obj.estimated_timeline ? ` (Süre: ${obj.estimated_timeline})` : ''}`,
      type: 'warning',
      category: obj.current_phase || 'Phase',
    };
  }
  
  // Handle regular finding objects
  if (obj.finding || obj.text || obj.description) {
    return {
      text: obj.finding || obj.text || obj.description,
      type: obj.type || 'finding',
      category: obj.category,
      impact_score: obj.impact_score,
      evidence: obj.evidence
    };
  }
  
  // Fallback: just return the object as text
  return {
    text: typeof obj === 'string' ? obj : JSON.stringify(obj),
    type: 'finding'
  };
}

// Parse findings that might be string or array
function parseFindings(findings: any): any[] {
  if (!findings) return [];
  
  if (Array.isArray(findings)) {
    return findings.map(f => {
      if (typeof f === 'string') {
        // Check if it's a JSON string
        if (f.startsWith('{') && f.endsWith('}')) {
          try {
            const parsed = JSON.parse(f);
            return formatFindingObject(parsed);
          } catch {
            // Not valid JSON, treat as plain text
          }
        }
        if (f.startsWith('@{')) {
          return parseNestedString(f);
        }
        return { text: f, type: 'finding' };
      }
      if (typeof f === 'object' && f !== null) {
        return formatFindingObject(f);
      }
      return { text: String(f), type: 'finding' };
    });
  }
  
  if (typeof findings === 'string') {
    // Try to split by "Bulgu X:" pattern
    const bulguPattern = findings.split(/Bulgu \d+:/i).filter(Boolean).map(s => s.trim());
    if (bulguPattern.length > 0) {
      return bulguPattern.map(p => ({ text: p, type: 'finding' }));
    }
    
    // Try splitting by numbered list
    const numberedPattern = findings.split(/\d+\.\s+/).filter(s => s.trim().length > 15);
    if (numberedPattern.length > 1) {
      return numberedPattern.map(p => ({ text: p.trim(), type: 'finding' }));
    }
    
    // Split by paragraph/sentence
    const paragraphs = findings.split(/\n\n|\.\s+(?=[A-Z])/).filter(s => s.trim().length > 15);
    if (paragraphs.length > 1) {
      return paragraphs.map(p => ({ text: p.trim(), type: 'finding' }));
    }
    
    // Just return as single finding
    if (findings.trim().length > 10) {
      return [{ text: findings.trim(), type: 'finding' }];
    }
  }
  
  return [];
}

// Parse recommendations
function parseRecommendations(recommendations: any): any[] {
  if (!recommendations) return [];
  
  if (Array.isArray(recommendations)) {
    return recommendations.map(r => {
      if (typeof r === 'string' && r.startsWith('@{')) {
        return parseNestedString(r);
      }
      return r;
    });
  }
  
  if (typeof recommendations === 'string') {
    // Try to split by "Öneri X:" pattern
    const oneriPattern = recommendations.split(/Öneri \d+:/i).filter(Boolean).map(s => s.trim());
    if (oneriPattern.length > 0) {
      return oneriPattern.map((p, i) => ({ action: p, priority: i + 1 }));
    }
    
    // Split by numbered list
    const numbered = recommendations.split(/\d+\.\s+/).filter(Boolean);
    if (numbered.length > 1) {
      return numbered.map((p, i) => ({ action: p.trim(), priority: i + 1 }));
    }
    
    // Split by paragraphs
    const paragraphs = recommendations.split(/\n\n|\.\s+(?=[A-Z])/).filter(s => s.trim().length > 20);
    if (paragraphs.length > 1) {
      return paragraphs.map((s, i) => ({ action: s.trim(), priority: i + 1 }));
    }
    
    if (recommendations.trim().length > 15) {
      return [{ action: recommendations.trim(), priority: 1 }];
    }
  }
  
  return [];
}

// Extract numeric metrics from nested objects - Enhanced to support deep nesting
function extractMetrics(metrics: any, fullResult?: any): Record<string, number | string> {
  if (!metrics || typeof metrics !== 'object') return {};
  
  const result: Record<string, number | string> = {};
  
  // Skip meta keys and zero metrics tracking
  const skipKeys = ['overallScore', 'overall_score', 'errorOccurred', '_zeroMetrics'];
  const zeroMetrics = metrics._zeroMetrics || [];
  
  // First extract from direct metrics object
  for (const [key, value] of Object.entries(metrics)) {
    // Skip meta keys
    if (skipKeys.includes(key)) continue;
    // Skip keys ending with _note or _display
    if (key.endsWith('_note') || key.endsWith('_display')) continue;
    
    if (typeof value === 'number') {
      // Check if this metric is in zeroMetrics list (means data was not available)
      if (zeroMetrics.includes(key) && value === 0) {
        // Show as "Veri yok" instead of 0
        result[key] = 'N/A';
      } else {
        result[key] = value;
      }
    } else if (typeof value === 'string') {
      // Try to parse nested object
      const parsed = parseNestedString(value);
      if (typeof parsed === 'object' && parsed !== null) {
        // Extract numeric values from parsed object
        for (const [k, v] of Object.entries(parsed)) {
          if (typeof v === 'number') {
            result[k] = v;
          }
        }
      } else if (!isNaN(Number(value)) && value !== '') {
        result[key] = Number(value);
      }
    } else if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      // Nested object, extract numeric values recursively
      extractNestedScores(value, key, result);
    }
  }
  
  // Then extract from analysis objects if fullResult is provided
  if (fullResult) {
    // Grid analysis
    if (fullResult.grid_analysis) {
      const grid = fullResult.grid_analysis;
      if (grid.visual_flow?.score != null) result['Grid Visual Flow'] = grid.visual_flow.score;
      if (grid.color_distribution?.score != null) result['Grid Color Harmony'] = grid.color_distribution.score;
      if (grid.content_variety?.score != null) result['Grid Content Balance'] = grid.content_variety.score;
      if (grid.first_impression?.score != null) result['Grid First Impression'] = grid.first_impression.score;
    }
    
    // Color analysis
    if (fullResult.color_analysis) {
      const color = fullResult.color_analysis;
      if (color.color_consistency?.score != null) result['Color Consistency'] = color.color_consistency.score;
      if (color.palette_harmony?.score != null) result['Palette Harmony'] = color.palette_harmony.score;
      if (color.niche_color_fit?.score != null) result['Niche Color Fit'] = color.niche_color_fit.score;
    }
    
    // Typography analysis
    if (fullResult.typography_analysis) {
      const typo = fullResult.typography_analysis;
      if (typo.font_consistency?.score != null) result['Font Consistency'] = typo.font_consistency.score;
      if (typo.readability_score != null) result['Readability'] = typo.readability_score;
      if (typo.hierarchy_clarity != null) result['Hierarchy Clarity'] = typo.hierarchy_clarity;
    }
    
    // Consistency analysis
    if (fullResult.consistency_analysis) {
      const consistency = fullResult.consistency_analysis;
      if (consistency.visual_consistency_score != null) result['Visual Consistency'] = consistency.visual_consistency_score;
      if (consistency.brand_recognition_score != null) result['Brand Recognition'] = consistency.brand_recognition_score;
    }
    
    // Quality analysis
    if (fullResult.quality_analysis) {
      const quality = fullResult.quality_analysis;
      if (quality.image_quality?.score != null) result['Image Quality'] = quality.image_quality.score;
      if (quality.video_quality?.score != null) result['Video Quality'] = quality.video_quality.score;
      if (quality.reels_quality?.score != null) result['Reels Quality'] = quality.reels_quality.score;
      if (quality.carousel_quality?.score != null) result['Carousel Quality'] = quality.carousel_quality.score;
    }
    
    // Format analysis
    if (fullResult.format_analysis) {
      const format = fullResult.format_analysis;
      if (format.deviation_score != null) result['Format Optimization'] = 100 - format.deviation_score;
    }
    
    // Thumbnail analysis
    if (fullResult.thumbnailAnalysis) {
      const thumb = fullResult.thumbnailAnalysis;
      if (thumb.overall_score != null) result['Thumbnail Score'] = thumb.overall_score;
      if (thumb.average_thumbnail_score != null) result['Avg Thumbnail'] = thumb.average_thumbnail_score;
    }
    
    // Grid professionalism
    if (fullResult.gridProfessionalism) {
      const gp = fullResult.gridProfessionalism;
      if (gp.score != null) result['Grid Professionalism'] = gp.score;
    }
    
    // Color consistency analysis
    if (fullResult.colorConsistencyAnalysis) {
      const cca = fullResult.colorConsistencyAnalysis;
      if (cca.score != null) result['Color Consistency Score'] = cca.score;
    }
  }
  
  return result;
}

// Helper to extract nested scores recursively
function extractNestedScores(obj: any, prefix: string, result: Record<string, number | string>, depth: number = 0): void {
  if (depth > 2 || !obj || typeof obj !== 'object') return;
  
  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === 'number' && key.toLowerCase().includes('score')) {
      // Create readable key name
      const readableKey = `${prefix} ${key}`.replace(/_/g, ' ').replace(/([A-Z])/g, ' $1').trim();
      result[readableKey] = value;
    } else if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      extractNestedScores(value, key, result, depth + 1);
    }
  }
}

// Insight type with optional color palette
interface InsightItem {
  title: string;
  content: string;
  type: 'info' | 'warning' | 'success';
  colorPalette?: { primary?: string; secondary?: string; accent?: string };
}

// Get additional insights from agent data
function extractInsights(result: any, agentKey: string): InsightItem[] {
  const insights: InsightItem[] = [];
  
  // Extract niche identification for domainMaster
  if (agentKey === 'domainMaster') {
    const nicheId = parseNestedString(result.niche_identification);
    if (nicheId && typeof nicheId === 'object') {
      if (nicheId.primary_niche) {
        insights.push({
          title: 'Birincil Niş',
          content: `${nicheId.primary_niche}${nicheId.sub_niche ? ' > ' + nicheId.sub_niche : ''}${nicheId.micro_niche ? ' > ' + nicheId.micro_niche : ''}`,
          type: 'info'
        });
      }
      if (nicheId.positioning_clarity) {
        insights.push({
          title: 'Konumlandırma Analizi',
          content: nicheId.positioning_clarity,
          type: 'info'
        });
      }
    }
    
    const nicheAnalysis = parseNestedString(result.niche_analysis);
    if (nicheAnalysis && typeof nicheAnalysis === 'object') {
      if (nicheAnalysis.differentiation_opportunity) {
        insights.push({
          title: 'Farklılaşma Fırsatı',
          content: nicheAnalysis.differentiation_opportunity,
          type: 'success'
        });
      }
    }
    
    const competitive = parseNestedString(result.competitive_positioning);
    if (competitive && typeof competitive === 'object') {
      if (competitive.unique_value_proposition) {
        insights.push({
          title: 'Benzersiz Değer Önerisi',
          content: competitive.unique_value_proposition,
          type: 'success'
        });
      }
      if (competitive.differentiation_strategy) {
        insights.push({
          title: 'Farklılaşma Stratejisi',
          content: competitive.differentiation_strategy,
          type: 'info'
        });
      }
    }
  }
  
  // Growth Virality insights
  if (agentKey === 'growthVirality') {
    const overview = parseNestedString(result.growth_overview);
    if (overview && typeof overview === 'object') {
      if (overview.growth_category) {
        insights.push({
          title: 'Büyüme Kategorisi',
          content: `${overview.growth_category === 'stagnant' ? '📉 Durağan' : overview.growth_category === 'growing' ? '📈 Büyüyor' : overview.growth_category}${overview.projected_followers_6mo ? ` • 6 aylık projeksiyon: ${overview.projected_followers_6mo.toLocaleString()}` : ''}`,
          type: overview.growth_category === 'stagnant' ? 'warning' : 'success'
        });
      }
    }
    
    const edgeCases = parseNestedString(result.edge_cases);
    if (edgeCases && typeof edgeCases === 'object' && edgeCases.special_notes) {
      insights.push({
        title: 'Özel Durum Tespiti',
        content: edgeCases.special_notes,
        type: 'warning'
      });
    }
  }
  
  // Visual Brand insights  
  if (agentKey === 'visualBrand') {
    const palette = parseNestedString(result.recommendedPalette);
    if (palette && typeof palette === 'object') {
      if (palette.rationale) {
        insights.push({
          title: 'Renk Önerisi Gerekçesi',
          content: palette.rationale,
          type: 'info'
        });
      }
    }
    
    const brand = parseNestedString(result.brand_overview);
    if (brand && typeof brand === 'object') {
      if (brand.visual_identity_strength) {
        insights.push({
          title: 'Görsel Kimlik Gücü',
          content: `${brand.visual_identity_strength === 'low' ? '⚠️ Düşük - İyileştirme gerekli' : brand.visual_identity_strength === 'medium' ? '📊 Orta - Geliştirilmeli' : '✅ Güçlü'}`,
          type: brand.visual_identity_strength === 'low' ? 'warning' : 'info'
        });
      }
      if (brand.visualArchetype) {
        const archetypeNames: Record<string, string> = {
          'minimalist_clean': '🎯 Minimalist & Temiz',
          'bold_vibrant': '🔥 Cesur & Canlı',
          'elegant_luxury': '✨ Zarif & Lüks',
          'casual_friendly': '😊 Samimi & Dostça',
          'professional_corporate': '💼 Profesyonel & Kurumsal',
          'artistic_creative': '🎨 Sanatsal & Yaratıcı',
          'nature_organic': '🌿 Doğal & Organik',
          'tech_modern': '💻 Teknoloji & Modern'
        };
        insights.push({
          title: 'Görsel Arketip',
          content: archetypeNames[brand.visualArchetype] || brand.visualArchetype,
          type: 'info'
        });
      }
    }
    
    // Grid analysis insights
    const gridAnalysis = parseNestedString(result.grid_analysis);
    if (gridAnalysis && typeof gridAnalysis === 'object') {
      if (gridAnalysis.pattern_detected) {
        const patternNames: Record<string, string> = {
          'checkerboard': '⬛⬜ Checkerboard (Dama Tahtası)',
          'row_by_row': '📊 Satır Bazlı Tema',
          'column': '📏 Dikey Tutarlılık',
          'puzzle': '🧩 Puzzle (Yapboz)',
          'rainbow': '🌈 Gökkuşağı Gradyan',
          'borders': '🖼️ Çerçeveli Stil',
          'tiles': '🔲 Tekrarlayan Pattern',
          'no_pattern': '❌ Pattern Yok'
        };
        insights.push({
          title: 'Grid Pattern',
          content: patternNames[gridAnalysis.pattern_detected] || gridAnalysis.pattern_detected,
          type: gridAnalysis.pattern_detected === 'no_pattern' ? 'warning' : 'info'
        });
      }
      if (gridAnalysis.grid_recommendation) {
        insights.push({
          title: 'Grid Önerisi',
          content: gridAnalysis.grid_recommendation,
          type: 'info'
        });
      }
    }
    
    // Color analysis insights
    const colorAnalysis = parseNestedString(result.color_analysis);
    if (colorAnalysis && typeof colorAnalysis === 'object') {
      if (colorAnalysis.palette_harmony?.type) {
        const harmonyNames: Record<string, string> = {
          'complementary': '🎯 Tamamlayıcı (Zıt Renkler)',
          'analogous': '🌊 Analog (Komşu Renkler)',
          'triadic': '🔺 Üçlü Uyum',
          'split_complementary': '✂️ Ayrık Tamamlayıcı',
          'monochromatic': '⚪ Monokromatik (Tek Renk)',
          'none': '❌ Uyum Yok'
        };
        insights.push({
          title: 'Renk Uyumu',
          content: harmonyNames[colorAnalysis.palette_harmony.type] || colorAnalysis.palette_harmony.type,
          type: colorAnalysis.palette_harmony.type === 'none' ? 'warning' : 'success'
        });
      }
    }
    
    const guidelines = parseNestedString(result.brand_guidelines_suggestion);
    if (guidelines && typeof guidelines === 'object') {
      if (guidelines.primary_color && guidelines.secondary_color) {
        insights.push({
          title: 'Önerilen Renk Paleti',
          content: `Ana: ${guidelines.primary_color} | İkincil: ${guidelines.secondary_color} | Aksan: ${guidelines.accent_color || 'Belirtilmemiş'}`,
          type: 'success',
          colorPalette: {
            primary: guidelines.primary_color,
            secondary: guidelines.secondary_color,
            accent: guidelines.accent_color
          }
        });
      }
      if (guidelines.grid_strategy) {
        insights.push({
          title: 'Grid Stratejisi',
          content: guidelines.grid_strategy,
          type: 'info'
        });
      }
      if (guidelines.visual_style_keywords && guidelines.visual_style_keywords.length > 0) {
        insights.push({
          title: 'Görsel Stil Anahtar Kelimeleri',
          content: guidelines.visual_style_keywords.join(' • '),
          type: 'info'
        });
      }
    }
    
    // Format analysis insights
    const formatAnalysis = parseNestedString(result.format_analysis);
    if (formatAnalysis && typeof formatAnalysis === 'object') {
      if (formatAnalysis.current_mix) {
        const mix = formatAnalysis.current_mix;
        insights.push({
          title: 'Mevcut Format Dağılımı',
          content: `Reels: %${mix.reels || 0} | Carousel: %${mix.carousel || 0} | Tek Post: %${mix.single_post || 0}`,
          type: 'info'
        });
      }
    }
  }
  
  // Community Loyalty insights
  if (agentKey === 'communityLoyalty') {
    const overview = parseNestedString(result.community_overview);
    if (overview && typeof overview === 'object') {
      if (overview.health_status) {
        insights.push({
          title: 'Topluluk Sağlığı',
          content: `${overview.health_status === 'at_risk' ? '⚠️ Risk altında' : overview.health_status === 'healthy' ? '✅ Sağlıklı' : overview.health_status}${overview.loyalty_level ? ` • Sadakat: ${overview.loyalty_level}` : ''}`,
          type: overview.health_status === 'at_risk' ? 'warning' : 'success'
        });
      }
    }
    
    const communityInsights = parseNestedString(result.communityInsights);
    if (communityInsights && typeof communityInsights === 'object') {
      if (communityInsights.estimatedSuperfans) {
        insights.push({
          title: 'Kitle Dağılımı',
          content: `Superfan: ${communityInsights.estimatedSuperfans?.toLocaleString() || '?'} | Aktif: ${communityInsights.activeEngagers?.toLocaleString() || '?'} | Pasif: ${communityInsights.passiveFollowers?.toLocaleString() || '?'} | Hayalet: ${communityInsights.ghostFollowers?.toLocaleString() || '?'}`,
          type: 'info'
        });
      }
    }
  }
  
  // Attention Architect insights
  if (agentKey === 'attentionArchitect') {
    const retention = parseNestedString(result.retentionPrediction);
    if (retention && typeof retention === 'object') {
      if (retention.scrollStopProbability !== undefined) {
        insights.push({
          title: 'Scroll Durdurucu Etkisi',
          content: `%${retention.scrollStopProbability} olasılıkla kullanıcılar içeriğinizde durur${retention.curiosityGapPresent ? ' • ✅ Merak boşluğu mevcut' : ' • ⚠️ Merak boşluğu eksik'}`,
          type: retention.scrollStopProbability > 30 ? 'success' : 'warning'
        });
      }
    }
    
    const nicheInsights = parseNestedString(result.niche_specific_insights);
    if (nicheInsights && typeof nicheInsights === 'object') {
      if (nicheInsights.optimal_content_length) {
        insights.push({
          title: 'Optimal İçerik Uzunluğu',
          content: nicheInsights.optimal_content_length,
          type: 'info'
        });
      }
      if (nicheInsights.viral_threshold_for_niche) {
        insights.push({
          title: 'Viral Eşiği',
          content: nicheInsights.viral_threshold_for_niche,
          type: 'info'
        });
      }
    }
    
    const grade = parseNestedString(result.grade);
    if (grade && typeof grade === 'object' && grade.description) {
      insights.push({
        title: 'Genel Değerlendirme',
        content: grade.description,
        type: grade.overall === 'A' || grade.overall === 'B' ? 'success' : 'warning'
      });
    }
  }
  
  // Growth Virality insights
  if (agentKey === 'growthVirality') {
    const growthMetrics = parseNestedString(result.growth_metrics);
    if (growthMetrics && typeof growthMetrics === 'object') {
      insights.push({
        title: 'Büyüme Metrikleri',
        content: `Net Büyüme: %${growthMetrics.net_growth_rate?.toFixed(1) || '?'} | Churn: %${growthMetrics.churn_rate?.toFixed(1) || '?'} | CMGR: %${growthMetrics.cmgr?.toFixed(2) || '?'}`,
        type: growthMetrics.net_growth_rate > 0 ? 'success' : 'warning'
      });
    }
    
    const growthAnalysis = parseNestedString(result.growth_analysis);
    if (growthAnalysis && typeof growthAnalysis === 'object') {
      if (growthAnalysis.growth_sources) {
        const sources = growthAnalysis.growth_sources;
        insights.push({
          title: 'Büyüme Kaynakları',
          content: `Explore: %${sources.explore_page || 0} | Reels: %${sources.reels || 0} | Hashtags: %${sources.hashtags || 0} | Paylaşımlar: %${sources.shares || 0}`,
          type: 'info'
        });
      }
      if (growthAnalysis.pattern_analysis) {
        const pattern = growthAnalysis.pattern_analysis;
        const sustainabilityEmoji = pattern.sustainability === 'high' ? '🟢' : pattern.sustainability === 'medium' ? '🟡' : '🔴';
        insights.push({
          title: 'Büyüme Patterni',
          content: `${pattern.detected_pattern || 'Bilinmiyor'} - ${sustainabilityEmoji} Sürdürülebilirlik: ${pattern.sustainability || '?'}`,
          type: pattern.sustainability === 'high' ? 'success' : 'warning'
        });
      }
    }
    
    const viralityAnalysis = parseNestedString(result.virality_analysis);
    if (viralityAnalysis && typeof viralityAnalysis === 'object') {
      if (viralityAnalysis.viral_potential) {
        insights.push({
          title: 'Viral Potansiyel',
          content: viralityAnalysis.viral_potential,
          type: 'info'
        });
      }
    }
  }
  
  // Sales Conversion insights
  if (agentKey === 'salesConversion') {
    const monthlyRevenue = parseNestedString(result.monthlyRevenuePotential);
    if (monthlyRevenue && typeof monthlyRevenue === 'object') {
      insights.push({
        title: 'Aylık Gelir Potansiyeli',
        content: `Muhafazakar: $${monthlyRevenue.conservative?.toLocaleString() || '?'} | Gerçekçi: $${monthlyRevenue.moderate?.toLocaleString() || '?'} | Agresif: $${monthlyRevenue.aggressive?.toLocaleString() || '?'}`,
        type: 'success'
      });
    }
    
    const brandDealGuidelines = parseNestedString(result.brandDealGuidelines);
    if (brandDealGuidelines && typeof brandDealGuidelines === 'object') {
      if (brandDealGuidelines.storyRate) {
        insights.push({
          title: 'Story Ücret Önerileri',
          content: `Tekli: $${brandDealGuidelines.storyRate.single || '?'} | Seri: $${brandDealGuidelines.storyRate.series || '?'} | Swipe Up ile: $${brandDealGuidelines.storyRate.withSwipeUp || '?'}`,
          type: 'info'
        });
      }
      if (brandDealGuidelines.reelRate) {
        insights.push({
          title: 'Reel Ücret Önerileri',
          content: `Kısa: $${brandDealGuidelines.reelRate.short || '?'} | Uzun: $${brandDealGuidelines.reelRate.long || '?'}`,
          type: 'info'
        });
      }
    }
    
    if (result.revenueStreams && Array.isArray(result.revenueStreams)) {
      const highPotentialStreams = result.revenueStreams.filter((s: any) => s.potential === 'high');
      if (highPotentialStreams.length > 0) {
        insights.push({
          title: 'Yüksek Potansiyelli Gelir Kanalları',
          content: highPotentialStreams.map((s: any) => `${s.type}: $${s.estimatedMonthly?.toLocaleString() || '?'}/ay`).join(' | '),
          type: 'success'
        });
      }
    }
  }
  
  // Domain Master insights
  if (agentKey === 'domainMaster') {
    const nicheAnalysis = parseNestedString(result.niche_analysis);
    if (nicheAnalysis && typeof nicheAnalysis === 'object') {
      const marketSizeEmoji = { large: '🏢', medium: '🏠', small: '🏘️', micro: '🏚️' }[nicheAnalysis.market_size as string] || '📊';
      const competitionEmoji = { very_high: '🔴', high: '🟠', medium: '🟡', low: '🟢' }[nicheAnalysis.competition_level as string] || '⚪';
      insights.push({
        title: 'Niş Analizi',
        content: `${marketSizeEmoji} Pazar: ${nicheAnalysis.market_size || '?'} | ${competitionEmoji} Rekabet: ${nicheAnalysis.competition_level || '?'} | 📈 Büyüme Potansiyeli: ${nicheAnalysis.growth_potential || '?'}`,
        type: 'info'
      });
      if (nicheAnalysis.differentiation_opportunity) {
        insights.push({
          title: 'Farklılaşma Fırsatı',
          content: nicheAnalysis.differentiation_opportunity,
          type: 'success'
        });
      }
    }
    
    const benchmarkComparison = parseNestedString(result.benchmark_comparison);
    if (benchmarkComparison && typeof benchmarkComparison === 'object') {
      if (benchmarkComparison.engagement_rate) {
        const er = benchmarkComparison.engagement_rate;
        insights.push({
          title: 'Engagement Benchmark',
          content: `Sizin: %${er.account?.toFixed(2) || '?'} | Niş Ort: %${er.niche_avg?.toFixed(2) || '?'} | Yüzdelik: ${er.percentile || '?'}%`,
          type: er.percentile > 50 ? 'success' : 'warning'
        });
      }
      if (benchmarkComparison.growth_rate) {
        const gr = benchmarkComparison.growth_rate;
        insights.push({
          title: 'Büyüme Benchmark',
          content: `Sizin: %${gr.account?.toFixed(2) || '?'} | Niş Ort: %${gr.niche_avg?.toFixed(2) || '?'} | Yüzdelik: ${gr.percentile || '?'}%`,
          type: gr.percentile > 50 ? 'success' : 'warning'
        });
      }
    }
    
    const positioning = parseNestedString(result.positioning);
    if (positioning && typeof positioning === 'object') {
      if (positioning.primary_niche) {
        insights.push({
          title: 'Niş Konumlandırması',
          content: `Ana: ${positioning.primary_niche}${positioning.secondary_niches?.length > 0 ? ` | İkincil: ${positioning.secondary_niches.join(', ')}` : ''}`,
          type: 'info'
        });
      }
    }
  }
  
  // Content Strategist insights
  if (agentKey === 'contentStrategist') {
    const postingAnalysis = parseNestedString(result.posting_analysis);
    if (postingAnalysis && typeof postingAnalysis === 'object') {
      insights.push({
        title: 'Paylaşım Analizi',
        content: `Haftalık: ${postingAnalysis.posts_per_week || '?'} post | Tutarlılık: ${postingAnalysis.consistency === 'high' ? '✅ Yüksek' : postingAnalysis.consistency === 'medium' ? '🟡 Orta' : '⚠️ Düşük'}`,
        type: postingAnalysis.consistency === 'high' ? 'success' : 'warning'
      });
    }
    
    const formatBreakdown = parseNestedString(result.format_breakdown);
    if (formatBreakdown && typeof formatBreakdown === 'object') {
      const total = (formatBreakdown.reels || 0) + (formatBreakdown.carousel || 0) + (formatBreakdown.single || 0);
      if (total > 0) {
        insights.push({
          title: 'Format Dağılımı',
          content: `Reels: %${Math.round((formatBreakdown.reels || 0) / total * 100)} | Carousel: %${Math.round((formatBreakdown.carousel || 0) / total * 100)} | Tek Post: %${Math.round((formatBreakdown.single || 0) / total * 100)}`,
          type: 'info'
        });
      }
    }
    
    const hashtagAnalysis = parseNestedString(result.hashtag_analysis);
    if (hashtagAnalysis && typeof hashtagAnalysis === 'object') {
      if (hashtagAnalysis.effectiveness_score !== undefined) {
        insights.push({
          title: 'Hashtag Etkinliği',
          content: `Skor: ${hashtagAnalysis.effectiveness_score}/100${hashtagAnalysis.top_performing?.length > 0 ? ` | En İyi: ${hashtagAnalysis.top_performing.slice(0, 3).join(', ')}` : ''}`,
          type: hashtagAnalysis.effectiveness_score > 60 ? 'success' : 'warning'
        });
      }
    }
    
    const contentMix = parseNestedString(result.content_mix);
    if (contentMix && typeof contentMix === 'object' && contentMix.optimal_mix) {
      insights.push({
        title: 'Önerilen İçerik Karışımı',
        content: `Eğitici: %${contentMix.optimal_mix.educational || '?'} | Eğlenceli: %${contentMix.optimal_mix.entertaining || '?'} | İlham Verici: %${contentMix.optimal_mix.inspiring || '?'} | Promosyon: %${contentMix.optimal_mix.promotional || '?'}`,
        type: 'info'
      });
    }
  }
  
  // Audience Dynamics insights
  if (agentKey === 'audienceDynamics') {
    const audienceSegments = result.audience_segments;
    if (audienceSegments && Array.isArray(audienceSegments) && audienceSegments.length > 0) {
      const topSegments = audienceSegments.slice(0, 3);
      insights.push({
        title: 'Top Kitle Segmentleri',
        content: topSegments.map((s: any) => `${s.name || s.segment_name}: %${s.percentage || '?'}`).join(' | '),
        type: 'info'
      });
    }
    
    const engagementPatterns = parseNestedString(result.engagement_patterns);
    if (engagementPatterns && typeof engagementPatterns === 'object') {
      if (engagementPatterns.peak_times && engagementPatterns.peak_times.length > 0) {
        insights.push({
          title: 'En İyi Paylaşım Saatleri',
          content: engagementPatterns.peak_times.slice(0, 4).join(' • '),
          type: 'success'
        });
      }
      if (engagementPatterns.best_days && engagementPatterns.best_days.length > 0) {
        insights.push({
          title: 'En İyi Günler',
          content: engagementPatterns.best_days.join(' • '),
          type: 'success'
        });
      }
    }
    
    const fakeFollowerAnalysis = parseNestedString(result.fake_follower_analysis);
    if (fakeFollowerAnalysis && typeof fakeFollowerAnalysis === 'object') {
      const riskLevel = fakeFollowerAnalysis.risk_level || fakeFollowerAnalysis.assessment;
      const riskEmoji = riskLevel === 'low' ? '🟢' : riskLevel === 'medium' ? '🟡' : '🔴';
      insights.push({
        title: 'Sahte Takipçi Riski',
        content: `${riskEmoji} ${riskLevel === 'low' ? 'Düşük Risk' : riskLevel === 'medium' ? 'Orta Risk' : 'Yüksek Risk'}${fakeFollowerAnalysis.estimated_percentage ? ` - Tahmini %${fakeFollowerAnalysis.estimated_percentage}` : ''}`,
        type: riskLevel === 'low' ? 'success' : 'warning'
      });
    }
  }
  
  // Edge case detection (common to many agents)
  const edgeCase = parseNestedString(result.edge_case_detection);
  if (edgeCase && typeof edgeCase === 'object') {
    if (edgeCase.detected_case && edgeCase.detected_case !== 'none') {
      insights.push({
        title: 'Tespit Edilen Özel Durum',
        content: `${edgeCase.detected_case}${edgeCase.adjusted_approach ? ': ' + edgeCase.adjusted_approach : ''}`,
        type: 'warning'
      });
    }
  }
  
  return insights;
}

// Metric progress bar component
function MetricBar({ label, value, max = 100, color }: { label: string; value: number | string; max?: number; color: string }) {
  const isNA = value === 'N/A' || value === null || value === undefined;
  const numValue = isNA ? 0 : typeof value === 'number' ? value : parseFloat(String(value)) || 0;
  const percentage = Math.min(100, (numValue / max) * 100);
  
  return (
    <div className="space-y-1">
      <div className="flex justify-between items-center">
        <span className="text-xs text-slate-600">{label}</span>
        <span className={`text-sm font-bold ${isNA ? 'text-slate-400' : 'text-slate-900'}`}>
          {isNA ? 'Veri Yok' : numValue.toFixed(0)}
        </span>
      </div>
      <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
        {isNA ? (
          <div className="h-full w-full bg-slate-300 opacity-50" />
        ) : (
          <div 
            className={`h-full rounded-full transition-all duration-500 ${color}`}
            style={{ width: `${percentage}%` }}
          />
        )}
      </div>
    </div>
  );
}

export function AgentResultAccordion({ agentKey, result, defaultOpen = false }: AgentResultAccordionProps) {
  const [open, setOpen] = useState(defaultOpen);
  const { t, locale } = useTranslation();
  const meta = agentMeta[agentKey] || defaultMeta;
  const Icon = meta.icon;

  // Get overall score from various possible locations
  const overallScore = result.metrics?.overallScore || result.metrics?.overall_score || 
    result.metrics?.overall_domain_score || result.metrics?.overall_growth_score ||
    result.metrics?.overallVisualScore || result.metrics?.communityHealthScore ||
    result.metrics?.overallAttentionScore;

  // Parse data with memoization - pass full result for nested metric extraction
  const parsedFindings = useMemo(() => parseFindings(result.findings), [result.findings]);
  const parsedRecommendations = useMemo(() => parseRecommendations(result.recommendations), [result.recommendations]);
  const extractedMetrics = useMemo(() => extractMetrics(result.metrics, result), [result.metrics, result]);
  const insights = useMemo(() => extractInsights(result, agentKey), [result, agentKey]);

  // Get score color
  const scoreColor = typeof overallScore === 'number' 
    ? overallScore >= 70 ? 'text-green-600' 
      : overallScore >= 40 ? 'text-amber-600' 
      : 'text-red-600'
    : 'text-slate-600';

  // Check if there's an error
  const hasError = result.error || result.errorType;
  
  // Check if there's meaningful content - DAHA ESNEK KONTROL
  const hasContent = parsedFindings.length > 0 || parsedRecommendations.length > 0 || 
    Object.keys(extractedMetrics).length > 0 || insights.length > 0 ||
    (result.metrics && Object.keys(result.metrics).length > 0) ||
    (result && typeof result === 'object' && Object.keys(result).length > 3); // En az 3 alan varsa (agentName, agentRole, metrics gibi)

  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      <button
        onClick={() => setOpen((prev) => !prev)}
        className={`flex w-full items-center justify-between px-5 py-4 text-left transition-colors bg-gradient-to-r ${meta.bgGradient} hover:opacity-90`}
      >
        <div className="flex items-center gap-4 flex-1 min-w-0">
          <div className={`rounded-xl border p-3 flex-shrink-0 ${meta.color}`}>
            <Icon className="h-5 w-5" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs uppercase tracking-[0.2em] text-slate-500 font-medium">{result.agentRole || meta.role}</p>
            <p className="text-lg font-semibold text-slate-900">{result.agentName ?? agentKey}</p>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed line-clamp-2">{meta.description}</p>
          </div>
        </div>
        <div className="flex items-center gap-4 flex-shrink-0 ml-4">
          {hasError ? (
            <div className="text-right">
              <AlertTriangleIcon className="h-6 w-6 text-red-500" />
              <p className="text-xs text-red-500 mt-1">Hata</p>
            </div>
          ) : overallScore !== undefined ? (
            <div className="text-right">
              <p className={`text-3xl font-bold ${scoreColor}`}>
                {typeof overallScore === 'number' ? overallScore.toFixed(0) : overallScore}
              </p>
              <p className="text-xs text-slate-500">{locale === 'tr' ? 'Skor' : 'Score'}</p>
            </div>
          ) : null}
          <ChevronDownIcon className={`h-5 w-5 text-slate-400 transition-transform duration-200 ${open ? 'rotate-180' : ''}`} />
        </div>
      </button>
      
      {open && (
        <div className="space-y-5 border-t border-slate-100 px-5 py-5 bg-slate-50/50">
          
          {/* Error Display */}
          {hasError && (
            <div className="bg-red-50 rounded-xl border border-red-200 p-4">
              <div className="flex items-start gap-3">
                <AlertTriangleIcon className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium text-red-800">{result.errorType || 'Hata'}</p>
                  <p className="text-sm text-red-700 mt-1">{result.errorMessage || 'Analiz tamamlanamadı'}</p>
                </div>
              </div>
            </div>
          )}

          {/* No Content Warning */}
          {!hasError && !hasContent && (
            <div className="bg-amber-50 rounded-xl border border-amber-200 p-4 text-center">
              <InfoIcon className="h-8 w-8 text-amber-500 mx-auto mb-2" />
              <p className="text-amber-800 font-medium">Bu agent için detaylı veri bulunamadı</p>
              <p className="text-sm text-amber-600 mt-1">Analiz tamamlanmış olabilir ancak detaylar kaydedilmemiş.</p>
              {/* Debug: Show raw data structure */}
              {process.env.NODE_ENV === 'development' && result && (
                <details className="mt-4 text-left">
                  <summary className="text-xs text-slate-500 cursor-pointer hover:text-slate-700">
                    🔍 Raw Data (Debug)
                  </summary>
                  <pre className="text-xs bg-slate-900 text-green-400 p-3 rounded mt-2 overflow-auto max-h-60">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </details>
              )}
            </div>
          )}

          {/* Key Insights Section */}
          {insights.length > 0 && (
            <div className="bg-white rounded-xl border border-slate-200 p-4">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-600 mb-4 flex items-center gap-2">
                <LightbulbIcon className="h-4 w-4 text-amber-500" />
                {locale === 'tr' ? 'Önemli Bilgiler' : 'Key Insights'}
              </p>
              <div className="space-y-3">
                {insights.map((insight, idx) => (
                  <div 
                    key={idx} 
                    className={`p-3 rounded-lg border ${
                      insight.type === 'warning' ? 'bg-amber-50 border-amber-200' :
                      insight.type === 'success' ? 'bg-green-50 border-green-200' :
                      'bg-blue-50 border-blue-200'
                    }`}
                  >
                    <p className={`text-xs font-semibold uppercase tracking-wider mb-1 ${
                      insight.type === 'warning' ? 'text-amber-700' :
                      insight.type === 'success' ? 'text-green-700' :
                      'text-blue-700'
                    }`}>
                      {insight.title}
                    </p>
                    {/* Color Palette with visual swatches */}
                    {insight.colorPalette ? (
                      <div className="flex flex-wrap items-center gap-3 mt-2">
                        {insight.colorPalette.primary && (
                          <div className="flex items-center gap-2">
                            <div 
                              className="w-8 h-8 rounded-lg border-2 border-white shadow-md" 
                              style={{ backgroundColor: insight.colorPalette.primary }}
                              title={insight.colorPalette.primary}
                            />
                            <div className="text-xs">
                              <span className="text-slate-500 block">Ana</span>
                              <span className="font-mono text-slate-700">{insight.colorPalette.primary}</span>
                            </div>
                          </div>
                        )}
                        {insight.colorPalette.secondary && (
                          <div className="flex items-center gap-2">
                            <div 
                              className="w-8 h-8 rounded-lg border-2 border-white shadow-md" 
                              style={{ backgroundColor: insight.colorPalette.secondary }}
                              title={insight.colorPalette.secondary}
                            />
                            <div className="text-xs">
                              <span className="text-slate-500 block">İkincil</span>
                              <span className="font-mono text-slate-700">{insight.colorPalette.secondary}</span>
                            </div>
                          </div>
                        )}
                        {insight.colorPalette.accent && (
                          <div className="flex items-center gap-2">
                            <div 
                              className="w-8 h-8 rounded-lg border-2 border-white shadow-md" 
                              style={{ backgroundColor: insight.colorPalette.accent }}
                              title={insight.colorPalette.accent}
                            />
                            <div className="text-xs">
                              <span className="text-slate-500 block">Aksan</span>
                              <span className="font-mono text-slate-700">{insight.colorPalette.accent}</span>
                            </div>
                          </div>
                        )}
                      </div>
                    ) : (
                      <p className="text-sm text-slate-800 leading-relaxed">{insight.content}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Metrics Section with Progress Bars */}
          {Object.keys(extractedMetrics).length > 0 && (
            <div className="bg-white rounded-xl border border-slate-200 p-4">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-600 mb-4 flex items-center gap-2">
                <BarChart3Icon className="h-4 w-4 text-purple-500" />
                {t('results.metrics')}
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(extractedMetrics)
                  .filter(([_, value]) => typeof value === 'number' || value === 'N/A')
                  .slice(0, 10)
                  .map(([key, value]) => {
                    const isNA = value === 'N/A';
                    const numValue = isNA ? 0 : typeof value === 'number' ? value : 0;
                    const color = isNA ? 'bg-slate-300' : numValue >= 70 ? 'bg-green-500' : numValue >= 40 ? 'bg-amber-500' : 'bg-red-500';
                    const label = key
                      .replace(/([A-Z])/g, ' $1')
                      .replace(/^./, s => s.toUpperCase())
                      .replace(/_/g, ' ')
                      .trim();
                    
                    return (
                      <MetricBar 
                        key={key}
                        label={label}
                        value={isNA ? 'N/A' : numValue}
                        color={color}
                      />
                    );
                  })}
              </div>
            </div>
          )}

          {/* Findings Section */}
          {parsedFindings.length > 0 && (
            <div className="bg-white rounded-xl border border-slate-200 p-4">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-600 mb-4 flex items-center gap-2">
                <InfoIcon className="h-4 w-4 text-blue-500" />
                {t('results.findings')}
              </p>
              <ul className="space-y-3">
                {parsedFindings.map((finding: any, idx: number) => {
                  // Handle both formatted objects and raw objects
                  let text = '';
                  let type = 'finding';
                  let category = finding?.category;
                  
                  // Category'yi güvenli şekilde string'e çevir
                  if (category && typeof category !== 'string') {
                    category = safeRenderValue(category);
                  }
                  
                  if (typeof finding === 'string') {
                    text = finding;
                  } else if (finding?.text) {
                    text = typeof finding.text === 'string' ? finding.text : safeRenderValue(finding.text);
                    type = finding.type || 'finding';
                    category = finding.category ? (typeof finding.category === 'string' ? finding.category : safeRenderValue(finding.category)) : category;
                  } else if (finding?.finding) {
                    text = typeof finding.finding === 'string' ? finding.finding : safeRenderValue(finding.finding);
                  } else if (finding?.description) {
                    text = typeof finding.description === 'string' ? finding.description : safeRenderValue(finding.description);
                  } else if (finding?.issue) {
                    // Handle issue-based findings
                    text = finding.original || (typeof finding.issue === 'string' ? finding.issue : safeRenderValue(finding.issue));
                    if (finding.fix_action) {
                      category = typeof finding.fix_action === 'string' ? finding.fix_action : safeRenderValue(finding.fix_action);
                    }
                    if (finding.expected_impact) {
                      const impact = typeof finding.expected_impact === 'string' ? finding.expected_impact : safeRenderValue(finding.expected_impact);
                      text += ` (Beklenen etki: ${impact})`;
                    }
                  } else {
                    // Avoid showing raw JSON - extract meaningful info
                    const keys = Object.keys(finding || {});
                    const meaningfulKey = keys.find(k => typeof finding[k] === 'string' && finding[k].length > 20);
                    text = meaningfulKey ? finding[meaningfulKey] : safeRenderValue(finding) || `Bulgu ${idx + 1}`;
                  }
                  
                  // Güvenli şekilde evidence çıkar
                  let evidence = finding?.evidence;
                  if (evidence && typeof evidence !== 'string') {
                    evidence = safeRenderValue(evidence);
                  }
                  
                  return (
                    <li key={idx} className="text-sm">
                      <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
                        <div className="flex items-start gap-2 flex-wrap mb-2">
                          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                            type === 'strength' ? 'bg-green-100 text-green-700' :
                            type === 'weakness' ? 'bg-red-100 text-red-700' :
                            type === 'opportunity' ? 'bg-blue-100 text-blue-700' :
                            type === 'threat' ? 'bg-amber-100 text-amber-700' :
                            'bg-slate-100 text-slate-700'
                          }`}>
                            {type === 'strength' ? '💪 Güçlü Yön' :
                             type === 'weakness' ? '⚠️ Zayıf Yön' :
                             type === 'opportunity' ? '🎯 Fırsat' :
                             type === 'threat' ? '⚡ Tehdit' : 
                             category || `Bulgu ${idx + 1}`}
                          </span>
                          {finding?.impact_score && (
                            <span className="text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">
                              Etki: {finding.impact_score}/10
                            </span>
                          )}
                        </div>
                        <p className="text-slate-800 leading-relaxed">{text}</p>
                        {evidence && (
                          <p className="text-xs text-slate-500 mt-2 italic bg-slate-100 p-2 rounded">
                            📊 {evidence}
                          </p>
                        )}
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
          )}

          {/* Recommendations Section */}
          {parsedRecommendations.length > 0 && (
            <div className="bg-white rounded-xl border border-slate-200 p-4">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-600 mb-4 flex items-center gap-2">
                <CheckCircleIcon className="h-4 w-4 text-green-500" />
                {t('results.recommendations')}
              </p>
              
              {/* 🎬 GÖREV 2: Reels Scenario Card (eğer varsa) */}
              {result.reelsScenario && (
                <div className="mb-4">
                  <ReelsScenarioCard scenario={result.reelsScenario} compact={false} />
                </div>
              )}
              
              {/* 🎬 GÖREV 2: Niche Detection Scenario (alternatif konum) */}
              {result.nicheDetection?.reels_scenario && !result.reelsScenario && (
                <div className="mb-4">
                  <ReelsScenarioCard scenario={result.nicheDetection.reels_scenario} compact={false} />
                </div>
              )}
              
              <ul className="space-y-3">{parsedRecommendations.map((rec: any, idx: number) => {
                  // Extract meaningful text from recommendation object
                  let action = '';
                  let expectedImpact = rec?.expected_impact;
                  let difficulty = rec?.difficulty;
                  let timeline = rec?.timeline;
                  
                  if (typeof rec === 'string') {
                    action = rec;
                  } else if (rec?.action) {
                    action = typeof rec.action === 'string' ? rec.action : safeRenderValue(rec.action);
                  } else if (rec?.recommendation) {
                    action = typeof rec.recommendation === 'string' ? rec.recommendation : safeRenderValue(rec.recommendation);
                  } else if (rec?.text) {
                    action = typeof rec.text === 'string' ? rec.text : safeRenderValue(rec.text);
                  } else if (rec?.fix_action) {
                    // Handle fix_action format from ELI5
                    action = typeof rec.fix_action === 'string' ? rec.fix_action : safeRenderValue(rec.fix_action);
                    if (rec.original) {
                      action = `${rec.original} → ${action}`;
                    }
                    expectedImpact = rec.expected_impact;
                  } else if (rec?.issue) {
                    // Handle issue-based recommendations
                    action = rec.original || (typeof rec.issue === 'string' ? rec.issue : safeRenderValue(rec.issue));
                    if (rec.fix_action) {
                      const fixAction = typeof rec.fix_action === 'string' ? rec.fix_action : safeRenderValue(rec.fix_action);
                      action += ` → ${fixAction}`;
                    }
                    expectedImpact = rec.expected_impact;
                  } else if (rec?.template) {
                    // Handle template-based recommendations (CTA, format vs.)
                    action = safeRenderValue(rec.template);
                    expectedImpact = rec.expected_impact;
                  } else {
                    // Avoid JSON - find meaningful string property or convert
                    const keys = Object.keys(rec || {});
                    const textKey = keys.find(k => typeof rec[k] === 'string' && rec[k].length > 10);
                    if (textKey) {
                      action = rec[textKey];
                    } else {
                      // Son çare: objeyi güvenli şekilde render et
                      action = safeRenderValue(rec) || `Öneri ${idx + 1}`;
                    }
                  }
                  
                  // Eğer action hala obje ise, güvenli şekilde dönüştür
                  if (typeof action !== 'string') {
                    action = safeRenderValue(action);
                  }
                  
                  // expected_impact obje olabilir
                  if (expectedImpact && typeof expectedImpact !== 'string') {
                    expectedImpact = safeRenderValue(expectedImpact);
                  }
                  
                  // 🎬 GÖREV 2: "Senaryo" içeren önerileri özel işaretle
                  const isScenario = action.toLowerCase().includes('senaryo') || 
                                    action.toLowerCase().includes('hook:') ||
                                    action.toLowerCase().includes('script:');
                  
                  return (
                    <li key={idx} className="text-sm">
                      <div className={`p-3 rounded-lg border ${
                        isScenario 
                          ? 'bg-gradient-to-r from-purple-50 to-pink-50 border-purple-200' 
                          : 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200'
                      }`}>
                        <div className="flex items-center gap-2 flex-wrap mb-2">
                          {(rec?.priority || idx + 1) && (
                            <span className={`text-xs px-2 py-0.5 rounded-full font-bold text-white ${
                              (rec?.priority || idx + 1) === 1 ? 'bg-red-500' :
                              (rec?.priority || idx + 1) === 2 ? 'bg-orange-500' :
                              (rec?.priority || idx + 1) === 3 ? 'bg-amber-500' :
                              'bg-slate-500'
                            }`}>
                              #{rec?.priority || idx + 1}
                            </span>
                          )}
                          {rec?.difficulty && (
                            <span className={`text-xs px-2 py-0.5 rounded-full ${
                              rec.difficulty === 'easy' || rec.difficulty === 'low' ? 'bg-green-200 text-green-800' :
                              rec.difficulty === 'medium' ? 'bg-yellow-200 text-yellow-800' :
                              'bg-red-200 text-red-800'
                            }`}>
                              {rec.difficulty === 'easy' || rec.difficulty === 'low' ? 'Kolay' : 
                               rec.difficulty === 'medium' ? 'Orta' : 
                               rec.difficulty === 'hard' || rec.difficulty === 'high' ? 'Zor' : rec.difficulty}
                            </span>
                          )}
                          {rec?.timeline && (
                            <span className="text-xs text-slate-600 bg-white px-2 py-0.5 rounded-full">
                              ⏱️ {rec.timeline}
                            </span>
                          )}
                        </div>
                        <p className="text-slate-800 leading-relaxed flex items-start gap-2">
                          <ArrowRightIcon className="h-4 w-4 text-green-500 flex-shrink-0 mt-0.5" />
                          <span>{action}</span>
                        </p>
                        {rec?.expected_impact && (
                          <p className="text-xs text-green-700 mt-2 font-medium">
                            ✨ Beklenen Etki: {typeof rec.expected_impact === 'string' ? rec.expected_impact : safeRenderValue(rec.expected_impact)}
                          </p>
                        )}
                        {rec?.implementation && (
                          <p className="text-xs text-slate-600 mt-1 bg-white/50 p-2 rounded">
                            📋 Uygulama: {typeof rec.implementation === 'string' ? rec.implementation : safeRenderValue(rec.implementation)}
                          </p>
                        )}
                        {rec?.actionRequired && (
                          <p className="text-xs text-slate-600 mt-1 bg-white/50 p-2 rounded">
                            📋 Aksiyon: {typeof rec.actionRequired === 'string' ? rec.actionRequired : safeRenderValue(rec.actionRequired)}
                          </p>
                        )}
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
          )}

          {/* Model Info - Kullanıcıya gösterilmiyor */}
        </div>
      )}
    </div>
  );
}
