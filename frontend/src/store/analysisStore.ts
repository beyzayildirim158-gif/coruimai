import { create } from 'zustand';

export interface AgentResult {
  findings?: string[] | string;
  recommendations?: string[] | string;
  metrics?: Record<string, any>;
  alerts?: string[];
  agentName?: string;
  agentRole?: string;
  // Extended fields from orchestrator
  error?: boolean;
  errorType?: string;
  errorMessage?: string;
  modelUsed?: string;
  timestamp?: string;
  fallback?: boolean;
  vetoed?: boolean;
  vetoReason?: string;
  // Agent-specific nested data
  niche_identification?: any;
  niche_analysis?: any;
  competitive_positioning?: any;
  growth_overview?: any;
  edge_cases?: any;
  edge_case_detection?: any;
  brand_overview?: any;
  recommendedPalette?: any;
  brand_guidelines_suggestion?: any;
  community_overview?: any;
  communityInsights?: any;
  retentionPrediction?: any;
  niche_specific_insights?: any;
  grade?: any;
  [key: string]: any; // Allow other dynamic fields
}

export interface Analysis {
  id: string;
  username?: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED' | 'CANCELLED';
  progress: number;
  currentAgent?: string;
  completedAgents: string[];
  agentResults?: Record<string, AgentResult>;
  createdAt: string;
  completedAt?: string;
  startedAt?: string;
  overallScore?: number | null;
  scoreGrade?: string | null;
  recommendations?: string[];
  account?: {
    username: string;
    profilePicUrl?: string | null;
    followers?: number;
    engagementRate?: number;
  };
}

interface AnalysisState {
  currentAnalysis: Analysis | null;
  analysisHistory: Analysis[];
  isAnalyzing: boolean;
  selectedAnalysis: Analysis | null;
  setCurrentAnalysis: (analysis: Analysis | null) => void;
  updateAnalysisProgress: (progress: Partial<Analysis>) => void;
  addToHistory: (analysis: Analysis) => void;
  setHistory: (analyses: Analysis[]) => void;
  setIsAnalyzing: (value: boolean) => void;
  setSelectedAnalysis: (analysis: Analysis | null) => void;
}

export const useAnalysisStore = create<AnalysisState>((set, get) => ({
  currentAnalysis: null,
  analysisHistory: [],
  isAnalyzing: false,
  selectedAnalysis: null,

  setCurrentAnalysis: (analysis) => set({ currentAnalysis: analysis }),

  updateAnalysisProgress: (progress) => {
    const current = get().currentAnalysis;
    if (current) {
      set({
        currentAnalysis: { ...current, ...progress },
      });
    }
  },

  addToHistory: (analysis) => {
    set((state) => ({
      analysisHistory: [analysis, ...state.analysisHistory].slice(0, 50),
    }));
  },

  setHistory: (analyses) => set({ analysisHistory: analyses }),

  setIsAnalyzing: (value) => set({ isAnalyzing: value }),

  setSelectedAnalysis: (analysis) => set({ selectedAnalysis: analysis }),
}));
