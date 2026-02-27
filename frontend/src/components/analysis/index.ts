// Analysis components for user-friendly report display
export { default as ExecutiveSummary, generateExecutiveSummary, getHealthStatus, getScoreIndicator, getScoreLabel } from './ExecutiveSummary';
export { default as ScoreExplainer, createScoreData, getScoreEmoji, getScoreStatus, getScoreStatusLabel } from './ScoreExplainer';
export type { ScoreData } from './ScoreExplainer';
export { default as JargonGlossary, defaultGlossaryTerms, extractTechnicalTerms } from './JargonGlossary';
export type { GlossaryTerm } from './JargonGlossary';
export { default as BenchmarkComparison, BenchmarkGrid, createBenchmarkData } from './BenchmarkComparison';
export type { BenchmarkData } from './BenchmarkComparison';
export { default as PrioritizedActions, createPriorityAction, extractPriorityActions } from './PrioritizedActions';
export type { PriorityAction } from './PrioritizedActions';
export { AgentResultAccordion } from './AgentResultAccordion';
export { default as ELI5Report } from './ELI5Report';
export { default as FinalVerdict } from './FinalVerdict';
export { default as BusinessIdentity } from './BusinessIdentity';

// Advanced Analysis Components (11-Module Deep Analysis)
export { AdvancedRiskDashboard } from './AdvancedRiskDashboard';
export { HashtagStrategyCard } from './HashtagStrategyCard';
export { ContentFormatAnalysis } from './ContentFormatAnalysis';
export { ContentDistributionChart } from './ContentDistributionChart';
export { ViralPotentialMeter } from './ViralPotentialMeter';
export { DetailedFindingsPanel } from './DetailedFindingsPanel';
export { ActionPlanTimeline } from './ActionPlanTimeline';
export { AdvancedAnalysisSection } from './AdvancedAnalysisSection';

// New: Comprehensive Data Display Components
export { SanitizationReport } from './SanitizationReport';
export { ComprehensiveMetricsDashboard } from './ComprehensiveMetricsDashboard';
export { AdvancedIntelligenceDashboard } from './AdvancedIntelligenceDashboard';

// PDF Export Components & Utilities
export { 
  ChartPdfWrapper, 
  useChartPdfReady, 
  preparePdfExport, 
  cleanupPdfExport,
  setPdfExportMode,
  isPdfExportMode 
} from './ChartPdfWrapper';
export { PrintableAdvancedIntelligence } from './PrintableAdvancedIntelligence';

// High Impact Dashboard (Vurucu Gerçekler)
export { HighImpactDashboard } from './HighImpactDashboard';
export type {
  HighImpactData,
  AudienceSegment,
  BenchmarkComparison as HighImpactBenchmark,
  AttentionMetrics,
  HookRewrite,
  BrandPalette,
  ColorSwatch,
} from './HighImpactDashboard';

// Data Quality
export { DataQualityBadge } from './DataQualityBadge';

// PDF Customization
export { PdfCustomizer } from './PdfCustomizer';
