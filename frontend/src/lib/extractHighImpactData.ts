/**
 * 🎯 HIGH IMPACT DATA EXTRACTOR
 * 
 * Bu modül, agent sonuçlarından HighImpactDashboard için gerekli
 * "Vurucu Gerçekler" verilerini çıkarır.
 * 
 * Veri kaynakları:
 * - communityLoyalty → Audience Röntgen
 * - domainMaster → Benchmark Karşılaştırması
 * - attentionArchitect → Algoritmik Metrikler
 * - eli5Report → Hook İyileştirmeleri
 * - visualBrand → Marka Renk Paleti
 */

import {
  HighImpactData,
  AudienceSegment,
  BenchmarkComparison,
  AttentionMetrics,
  HookRewrite,
  BrandPalette,
  ColorSwatch,
} from '../components/analysis/HighImpactDashboard';

import { normalizePercentages } from './formatters';

// Safe accessor helper
function safeGet<T>(obj: any, path: string, defaultValue: T): T {
  try {
    const keys = path.split('.');
    let result = obj;
    for (const key of keys) {
      if (result === null || result === undefined) return defaultValue;
      result = result[key];
    }
    return result ?? defaultValue;
  } catch {
    return defaultValue;
  }
}

// Parse numeric value from various formats
function parseNumeric(value: any, defaultValue: number = 0): number {
  if (typeof value === 'number') return value;
  if (typeof value === 'string') {
    const parsed = parseFloat(value.replace(/[%,]/g, ''));
    return isNaN(parsed) ? defaultValue : parsed;
  }
  return defaultValue;
}

/**
 * Takipçi segmentasyonunu çıkarır
 */
function extractAudienceSegments(agentResults: any, totalFollowers: number): AudienceSegment[] {
  const communityLoyalty = agentResults?.communityLoyalty || {};
  const communityInsights = communityLoyalty?.communityInsights || {};
  const metrics = communityLoyalty?.metrics || {};

  // Get counts
  const superfans = parseNumeric(communityInsights.estimatedSuperfans) || parseNumeric(metrics.superfanPercentage);
  const activeEngagers = parseNumeric(communityInsights.activeEngagers) || parseNumeric(metrics.activeEngagersRatio);
  const passiveFollowers = parseNumeric(communityInsights.passiveFollowers) || parseNumeric(metrics.passiveFollowersRatio);
  const ghostFollowers = parseNumeric(communityInsights.ghostFollowers) || parseNumeric(metrics.ghostFollowersRatio);

  // Calculate percentages
  let superfanPct = 0;
  let activePct = 0;
  let passivePct = 0;
  let ghostPct = 0;

  // Try ratios first (0-1 range), then calculate from counts
  if (metrics.superfanPercentage !== undefined || metrics.activeEngagersRatio !== undefined) {
    superfanPct = parseNumeric(metrics.superfanPercentage) * 100 || parseNumeric(metrics.superfanPercentage);
    activePct = parseNumeric(metrics.activeEngagersRatio) * 100 || parseNumeric(metrics.activeEngagersRatio);
    passivePct = parseNumeric(metrics.passiveFollowersRatio) * 100 || parseNumeric(metrics.passiveFollowersRatio);
    ghostPct = parseNumeric(metrics.ghostFollowersRatio) * 100 || parseNumeric(metrics.ghostFollowersRatio);
  } else if (totalFollowers > 0) {
    superfanPct = (superfans / totalFollowers) * 100;
    activePct = (activeEngagers / totalFollowers) * 100;
    passivePct = (passiveFollowers / totalFollowers) * 100;
    ghostPct = (ghostFollowers / totalFollowers) * 100;
  }

  // Normalize if percentages are already in 0-100 range (e.g., ratio was 0.99 → 99%)
  const total = superfanPct + activePct + passivePct + ghostPct;
  if (total > 0 && total < 10) {
    // Values are in 0-1 range, multiply by 100
    superfanPct *= 100;
    activePct *= 100;
    passivePct *= 100;
    ghostPct *= 100;
  }

  // 🎯 CRITICAL: Normalize percentages to exactly 100% using Largest Remainder Method
  // This prevents math bugs where LLM-generated percentages don't sum to 100%
  const normalizedPcts = normalizePercentages({
    superfan: superfanPct,
    active: activePct,
    passive: passivePct,
    ghost: ghostPct,
  });

  // Use normalized percentages
  superfanPct = normalizedPcts.superfan;
  activePct = normalizedPcts.active;
  passivePct = normalizedPcts.passive;
  ghostPct = normalizedPcts.ghost;

  // Calculate counts from normalized percentages
  const superfanCount = totalFollowers > 0 ? Math.round((superfanPct / 100) * totalFollowers) : superfans;
  const activeCount = totalFollowers > 0 ? Math.round((activePct / 100) * totalFollowers) : activeEngagers;
  const passiveCount = totalFollowers > 0 ? Math.round((passivePct / 100) * totalFollowers) : passiveFollowers;
  const ghostCount = totalFollowers > 0 ? Math.round((ghostPct / 100) * totalFollowers) : ghostFollowers;

  return [
    {
      label: 'Süper Hayran',
      percentage: superfanPct || 0,
      count: superfanCount || 0,
      color: '#22c55e', // green-500
      description: 'Tüm içeriklerinizle aktif olarak etkileşime giren sadık takipçiler',
    },
    {
      label: 'Aktif Takipçi',
      percentage: activePct || 0,
      count: activeCount || 0,
      color: '#3b82f6', // blue-500
      description: 'Düzenli olarak içeriklerinizi gören ve ara sıra etkileşim kuran takipçiler',
    },
    {
      label: 'Pasif Takipçi',
      percentage: passivePct || 0,
      count: passiveCount || 0,
      color: '#f59e0b', // amber-500
      description: 'Sizi takip eden ama nadiren etkileşim kuran takipçiler',
    },
    {
      label: 'Hayalet Takipçi',
      percentage: ghostPct || 0,
      count: ghostCount || 0,
      color: '#94a3b8', // slate-400
      description: 'İnaktif veya bot hesaplar - etkileşim sağlamıyor',
    },
  ];
}

/**
 * Benchmark karşılaştırmasını çıkarır
 */
function extractBenchmarkComparison(agentResults: any): BenchmarkComparison {
  const domainMaster = agentResults?.domainMaster || {};
  const nicheBenchmarks = domainMaster?.nicheBenchmarks || {};
  const engagementBenchmarks = nicheBenchmarks?.engagementBenchmarks || {};

  // Try different field name patterns
  const yourER = parseNumeric(
    engagementBenchmarks.your_engagement_rate ??
    engagementBenchmarks.yourEngagementRate ??
    engagementBenchmarks.current ??
    domainMaster.currentEngagementRate ??
    0
  );

  const nicheAvg = parseNumeric(
    engagementBenchmarks.niche_average ??
    engagementBenchmarks.nicheAverage ??
    engagementBenchmarks.average ??
    domainMaster.nicheAverageER ??
    3.5 // Default niche average
  );

  const topPerformers = parseNumeric(
    engagementBenchmarks.top_performers ??
    engagementBenchmarks.topPerformers ??
    engagementBenchmarks.top_10_percent ??
    nicheAvg * 2 // Estimate top performers as 2x average
  );

  const gap = yourER - nicheAvg;
  
  // Calculate percentile (rough estimate)
  let percentile = 50;
  if (yourER >= topPerformers) percentile = 90;
  else if (yourER >= nicheAvg * 1.5) percentile = 75;
  else if (yourER >= nicheAvg) percentile = 50;
  else if (yourER >= nicheAvg * 0.5) percentile = 25;
  else percentile = 10;

  // Determine interpretation
  let interpretation: BenchmarkComparison['interpretation'] = 'average';
  const ratio = yourER / nicheAvg;
  if (ratio < 0.3) interpretation = 'critical';
  else if (ratio < 0.7) interpretation = 'below';
  else if (ratio < 1.1) interpretation = 'average';
  else if (ratio < 1.5) interpretation = 'above';
  else interpretation = 'excellent';

  return {
    yourValue: yourER,
    nicheAverage: nicheAvg,
    topPerformers,
    gap,
    percentile,
    interpretation,
  };
}

/**
 * Dikkat metriklerini çıkarır
 */
function extractAttentionMetrics(agentResults: any): AttentionMetrics {
  const attentionArchitect = agentResults?.attentionArchitect || {};
  const metrics = attentionArchitect?.metrics || {};
  const contentMetrics = attentionArchitect?.contentMetrics || {};
  const attentionScores = attentionArchitect?.attentionScores || {};

  return {
    scrollStopProbability: parseNumeric(
      metrics.scrollStopProbability ??
      metrics.scroll_stop_probability ??
      contentMetrics.scrollStopRate ??
      attentionScores.scrollStop ??
      0
    ),
    thumbnailImpact: parseNumeric(
      metrics.thumbnailImpactScore ??
      metrics.thumbnail_impact_score ??
      contentMetrics.thumbnailEffectiveness ??
      attentionScores.thumbnail ??
      0
    ),
    curiosityGap: parseNumeric(
      metrics.curiosityGapScore ??
      metrics.curiosity_gap_score ??
      contentMetrics.curiosityGap ??
      attentionScores.curiosity ??
      0
    ),
    hookEffectiveness: parseNumeric(
      metrics.hookEffectiveness ??
      metrics.hook_effectiveness ??
      contentMetrics.hookScore ??
      attentionScores.hook ??
      0
    ),
    first3SecondsRetention: parseNumeric(
      metrics.first3SecondsRetention ??
      metrics.first_3_seconds_retention ??
      contentMetrics.retentionRate ??
      attentionScores.retention ??
      0
    ),
  };
}

/**
 * Hook yeniden yazımlarını çıkarır
 */
function extractHookRewrites(agentResults: any): HookRewrite[] {
  const eli5Report = agentResults?.eli5Report || {};
  const rewrittenHooks = eli5Report?.rewrittenHooks || [];
  const attentionArchitect = agentResults?.attentionArchitect || {};
  const hookAnalysis = attentionArchitect?.hookAnalysis || [];

  // Trigger emoji mapping
  const triggerEmojis: Record<string, string> = {
    fear: '😨',
    curiosity: '🤔',
    controversy: '🔥',
    urgency: '⏰',
    exclusivity: '👑',
    social_proof: '👥',
    authority: '🏆',
    scarcity: '⚡',
    greed: '💰',
    vanity: '✨',
    default: '💡',
  };

  const results: HookRewrite[] = [];

  // Extract from eli5Report.rewrittenHooks
  for (const hook of rewrittenHooks) {
    if (hook.badHook || hook.original || hook.oldHook) {
      const trigger = (hook.triggerUsed || hook.trigger || hook.psychologicalTrigger || 'curiosity').toLowerCase();
      results.push({
        original: hook.badHook || hook.original || hook.oldHook || '',
        improved: hook.newHook || hook.improved || hook.rewritten || '',
        trigger: trigger.charAt(0).toUpperCase() + trigger.slice(1),
        triggerEmoji: triggerEmojis[trigger] || triggerEmojis.default,
        improvement: hook.whyItWorks || hook.explanation || hook.improvement || '',
      });
    }
  }

  // Extract from attentionArchitect.hookAnalysis as fallback
  if (results.length === 0 && hookAnalysis.length > 0) {
    for (const analysis of hookAnalysis) {
      if (analysis.current || analysis.original) {
        const trigger = (analysis.suggestedTrigger || analysis.trigger || 'curiosity').toLowerCase();
        results.push({
          original: analysis.current || analysis.original || '',
          improved: analysis.suggested || analysis.improved || analysis.optimized || '',
          trigger: trigger.charAt(0).toUpperCase() + trigger.slice(1),
          triggerEmoji: triggerEmojis[trigger] || triggerEmojis.default,
          improvement: analysis.rationale || analysis.reasoning || '',
        });
      }
    }
  }

  return results;
}

/**
 * Marka renk paletini çıkarır
 */
function extractBrandPalette(agentResults: any): BrandPalette {
  const visualBrand = agentResults?.visualBrand || {};
  const recommendedPalette = visualBrand?.recommendedPalette || {};
  const currentColors = visualBrand?.currentColors || visualBrand?.detectedColors || [];
  const colorAnalysis = visualBrand?.colorAnalysis || {};

  // Helper to create color swatch
  const createSwatch = (color: any, usage: string, defaultHex: string, defaultName: string): ColorSwatch => {
    if (typeof color === 'string') {
      return {
        hex: color,
        name: defaultName,
        usage,
        psychology: '',
      };
    }
    return {
      hex: color?.hex || color?.value || defaultHex,
      name: color?.name || color?.label || defaultName,
      usage,
      psychology: color?.psychology || color?.meaning || '',
    };
  };

  // Extract current palette (top 3 detected colors)
  const current: ColorSwatch[] = [];
  if (Array.isArray(currentColors)) {
    for (let i = 0; i < Math.min(3, currentColors.length); i++) {
      current.push(createSwatch(
        currentColors[i],
        i === 0 ? 'Primary' : i === 1 ? 'Secondary' : 'Accent',
        '#666666',
        `Mevcut Renk ${i + 1}`
      ));
    }
  }

  // Extract recommended palette
  const recommended = {
    primary: createSwatch(
      recommendedPalette?.primary,
      'Ana Renk - Logo ve başlıklar',
      '#3b82f6',
      'Ana Renk'
    ),
    secondary: createSwatch(
      recommendedPalette?.secondary,
      'İkincil Renk - Arka plan ve vurgular',
      '#6366f1',
      'İkincil Renk'
    ),
    accent: createSwatch(
      recommendedPalette?.accent,
      'Vurgu Renk - CTA ve önemli öğeler',
      '#ec4899',
      'Vurgu Renk'
    ),
    rationale: recommendedPalette?.rationale || 
               colorAnalysis?.recommendation || 
               visualBrand?.colorRecommendation ||
               'Bu renk paleti, hedef kitlenizle duygusal bağ kurmak için optimize edilmiştir.',
  };

  return { current, recommended };
}

/**
 * Genel sağlık notunu hesaplar
 */
function calculateOverallHealthGrade(
  benchmark: BenchmarkComparison,
  attention: AttentionMetrics
): string {
  // Weighted average of key metrics
  const erScore = Math.min((benchmark.yourValue / benchmark.nicheAverage) * 50, 50);
  const attentionScore = (
    attention.scrollStopProbability +
    attention.thumbnailImpact +
    attention.curiosityGap +
    attention.hookEffectiveness
  ) / 8; // Max 50 points

  const total = erScore + attentionScore;

  if (total >= 85) return 'A+';
  if (total >= 75) return 'A';
  if (total >= 65) return 'B+';
  if (total >= 55) return 'B';
  if (total >= 45) return 'C+';
  if (total >= 35) return 'C';
  if (total >= 25) return 'D';
  return 'F';
}

/**
 * Ana extraction fonksiyonu
 * 
 * @param reportData - Tam rapor verisi (analysis objesi)
 * @returns HighImpactDashboard için hazır veri
 */
export function extractHighImpactData(reportData: any): HighImpactData {
  // Support both direct agentResults and nested structure
  const agentResults = reportData?.agentResults || reportData || {};
  
  // Get basic profile info
  const profileData = reportData?.profile || reportData?.instagramProfile || {};
  const username = profileData?.username || reportData?.username || 'unknown';
  const totalFollowers = parseNumeric(profileData?.followers || profileData?.follower_count || 0);

  // Extract all sections
  const audienceSegments = extractAudienceSegments(agentResults, totalFollowers);
  const benchmark = extractBenchmarkComparison(agentResults);
  const attentionMetrics = extractAttentionMetrics(agentResults);
  const hookRewrites = extractHookRewrites(agentResults);
  const brandPalette = extractBrandPalette(agentResults);
  const overallHealthGrade = calculateOverallHealthGrade(benchmark, attentionMetrics);

  return {
    audienceSegments,
    benchmark,
    attentionMetrics,
    hookRewrites,
    brandPalette,
    overallHealthGrade,
    username,
  };
}

export default extractHighImpactData;
