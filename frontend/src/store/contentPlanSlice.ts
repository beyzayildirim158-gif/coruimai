import { create } from 'zustand';
import api from '../lib/api';

// Types for 7-Day Content Plan - Enhanced with all required fields

export interface PostingTime {
  time: string;       // e.g., "18:30"
  timezone: string;   // e.g., "Europe/Istanbul"
  reason: string;     // Why this time was chosen
}

export interface TopicData {
  title: string;
  angle: string;
  source: string;
  linkedPainPoint: string;  // REQUIRED: from audience_dynamics.pain_points
  audienceRelevance: {
    score: number;
    primaryPersonaMatch: string;
    engagementPotential: 'high' | 'medium' | 'low';
  };
}

export interface HookData {
  type: 'question' | 'statement' | 'story' | 'shock' | 'curiosity' | 'pain_solution';
  text: string;
  formula?: string;
  targetEmotion: string;
  expectedRetention?: number;
}

export interface CaptionCTA {
  text: string;
  type: 'comment' | 'save' | 'share' | 'link';
  placement: 'end' | 'middle';
}

export interface EmojiUsage {
  count: number;
  emojis: string[];
  density: 'low' | 'medium' | 'high';
}

export interface CaptionData {
  fullText: string;           // REQUIRED: 200-600 chars complete caption
  charCount: number;
  structure: string;
  cta: CaptionCTA;
  emojiUsage: EmojiUsage;
  lineBreaks: number;
  // Legacy fields for backward compatibility
  hook?: string;
  body?: string;
  callToAction?: string;
  fullCaption?: string;
  characterCount?: number;
}

export interface HashtagCategory {
  tags: string[];
  avgReach?: string;
  relevanceScore?: number;
  trendingUntil?: string;
}

export interface HashtagSet {
  primary: HashtagCategory | string[];
  niche: HashtagCategory | string[];
  trending?: HashtagCategory;
  branded: string[];
  total: number;
  rotationSet: string;
  // Legacy fields
  secondary?: string[];
}

export interface ColorPalette {
  primary: string;
  secondary: string;
  accent: string;
  background?: string;
}

export interface ThumbnailText {
  text: string;
  font?: string;
  position: 'center' | 'top' | 'bottom';
}

export interface VisualStyle {
  archetype: string;
  mood: string;
  composition: string;
  lighting: string;
}

export interface FacePresence {
  recommended: boolean;
  expression?: string;
  eyeContact: boolean;
}

export interface VisualGuidelines {
  colorPalette: ColorPalette | string[];
  thumbnailText: ThumbnailText;
  style: VisualStyle | string;
  facePresence?: FacePresence;
  // Legacy fields
  fontRecommendations?: string[];
  layoutStyle?: string;
  filterPreset?: string;
  visualElements?: string[];
}

export interface StorySlot {
  slot: number;
  time: string;             // REQUIRED: specific time from audience_active_times
  type: string;             // Poll, Teaser, Post Share, Behind Scenes, Q&A
  content: string;          // REQUIRED: related to daily_topic
  sticker?: string;
  options?: string[];       // For polls
  visualHint?: string;
  engagementCTA?: string;
  purpose: string;
  // Legacy fields
  slotNumber?: number;
  stickerSuggestions?: string[];
  interactiveElement?: string;
}

export interface ContentData {
  type: string;             // reel, carousel, static
  hook: HookData;
  script?: {
    intro: string;
    body: string[];
    cta: string;
    duration: string;
    pacing: string;
  };
}

export interface ContentPost {
  postNumber?: number;
  topic: string | TopicData;
  contentPillar?: string;
  hook: HookData;
  script?: string | {
    intro: string;
    body: string[];
    cta: string;
    duration: string;
    pacing: string;
  };
  caption: CaptionData;
  hashtags: HashtagSet;
  visualGuidelines: VisualGuidelines;
  bestPostingTime?: string;
  alternateTime?: string;
  estimatedEngagement?: {
    likes: string | number;
    comments: string | number;
    saves: string | number;
    shares: string | number;
    reach?: number;
  };
}

export interface DayPlan {
  day: number;
  dayNumber?: number;       // Legacy
  dayName?: string;
  dayOfWeek?: string;
  date?: string;
  postingTime: PostingTime;
  dayPurpose: {
    name: string;
    objective: string;
    primaryMetric: string;
  };
  topic: TopicData;
  content: ContentData;
  caption: CaptionData;
  hashtags: HashtagSet;
  stories: StorySlot[];
  visualGuidelines: VisualGuidelines;
  engagement: {
    commentPrompt: string;
    replyStrategy: string;
    expectedMetrics: {
      likes: number;
      comments: number;
      saves: number;
      shares: number;
      reach: number;
    };
  };
  // Legacy fields
  purpose?: string;
  purposeDescription?: string;
  mainPost?: ContentPost;
  dailyGoals?: string[];
  engagementTasks?: string[];
  audienceInteractionFocus?: string;
}

export interface ContentPlanMetrics {
  expectedFollowerGrowth: string;
  expectedEngagementRate: string;
  expectedReach: string;
  contentMixRatio: {
    reels?: number;
    carousels?: number;
    staticPosts?: number;
    stories?: number;
    educational?: number;
    entertainment?: number;
    promotional?: number;
    personal?: number;
  };
}

export interface ContentPlan {
  planId: string;
  analysisId: string;
  username: string;
  generatedAt: string;
  weekStartDate?: string;
  weekEndDate?: string;
  generatedFor?: {
    handle: string;
    niche: string;
    subNiche?: string;
    analysisId: string;
    generatedDate: string;
    planPeriod: {
      startDate: string;
      endDate: string;
    };
  };
  dataSourcesSummary?: Record<string, any>;
  overallStrategy?: {
    weeklyTheme?: string;
    theme?: string;
    primaryGoal?: string;
    goals?: string[];
    secondaryGoals?: string[];
    targetAudience?: string;
    brandVoice?: string;
    keyMessages?: string[];
    contentMixRatio?: Record<string, number>;
    focusAreas?: string[];
    avoidAreas?: string[];
  };
  weeklyStrategy?: {
    theme: string;
    goals: string[];
    contentMixRatio: Record<string, number>;
    focusAreas: string[];
    avoidAreas: string[];
  };
  days: DayPlan[];
  dailyPlan?: DayPlan[];    // Alternative key from backend
  weeklyHashtagRotation?: {
    set1: { days: number[]; hashtags: string[]; focus: string; totalReach: string };
    set2: { days: number[]; hashtags: string[]; focus: string; totalReach: string };
    set3: { days: number[]; hashtags: string[]; focus: string; totalReach: string };
    avoidHashtags: string[];
    rotationRationale: string;
  };
  contentPillars?: {
    identified: string[];
    weeklyDistribution: Record<string, number>;
    recommendations: string[];
  };
  kpis?: {
    currentMetrics: Record<string, number>;
    weeklyTargets: Record<string, number>;
    improvementPercentages: Record<string, string>;
    trackingRecommendations: string[];
  };
  weeklyMetrics?: ContentPlanMetrics;
  implementation?: {
    toolsNeeded?: string[];
    preparationChecklist?: string[];
    contentBatching?: string[];
    criticalSuccessFactors?: string[];
    potentialChallenges?: string[];
    adaptationGuidelines?: string;
    reviewSchedule?: string;
  };
  implementationNotes?: {
    criticalSuccessFactors: string[];
    potentialChallenges: string[];
    adaptationGuidelines: string;
    reviewSchedule: string;
  };
  validationReport?: {
    allTopicsFromAnalysis: boolean;
    hooksMatchAudienceLanguage: boolean;
    hashtagsFromAnalyzedClusters: boolean;
    postingTimesMatchActivity: boolean;
    visualsMatchBrandPalette: boolean;
    ctasAlignedWithOffer: boolean;
    noHardcodedContent: boolean;
    dataCompleteness: number;
  };
  dataSourcesUsed?: string[];
}

export interface ValidationResult {
  isValid: boolean;
  completenessScore: number;
  missingData: string[];
  availableData: string[];
  recommendation: string;
}

interface ContentPlanState {
  currentPlan: ContentPlan | null;
  validation: ValidationResult | null;
  isLoading: boolean;
  isGenerating: boolean;
  isValidating: boolean;
  error: string | null;
  generationProgress: number;

  // Actions
  generateContentPlan: (analysisId: string) => Promise<void>;
  fetchContentPlan: (analysisId: string) => Promise<void>;
  validateAnalysisForPlan: (analysisId: string) => Promise<void>;
  deleteContentPlan: (analysisId: string) => Promise<void>;
  clearContentPlan: () => void;
  setGenerationProgress: (progress: number) => void;
  clearError: () => void;
}

export const useContentPlanStore = create<ContentPlanState>((set) => ({
  currentPlan: null,
  validation: null,
  isLoading: false,
  isGenerating: false,
  isValidating: false,
  error: null,
  generationProgress: 0,

  generateContentPlan: async (analysisId: string) => {
    try {
      set({ isGenerating: true, error: null, generationProgress: 10 });
      
      const response = await api.post(`/analyze/${analysisId}/content-plan`);
      
      set({
        isGenerating: false,
        currentPlan: response.data.contentPlan,
        generationProgress: 100,
      });
    } catch (error: any) {
      // Extract error message, ensuring it's a string
      const errorMessage = typeof error.response?.data?.error === 'string' 
        ? error.response.data.error 
        : error.response?.data?.message || 'Failed to generate content plan';
      
      set({
        isGenerating: false,
        error: errorMessage,
        generationProgress: 0,
      });
      throw error;
    }
  },

  fetchContentPlan: async (analysisId: string) => {
    try {
      set({ isLoading: true, error: null });
      
      const response = await api.get(`/analyze/${analysisId}/content-plan`);
      
      set({
        isLoading: false,
        currentPlan: response.data.contentPlan,
      });
    } catch (error: any) {
      // 404 means plan doesn't exist yet - not an error condition
      const status = error.response?.status;
      if (status === 404) {
        set({ isLoading: false });
        return; // Don't throw, just return - no plan exists yet
      }
      
      // Extract error message, ensuring it's a string
      const errorMessage = typeof error.response?.data?.error === 'string' 
        ? error.response.data.error 
        : error.response?.data?.message || 'Failed to fetch content plan';
      
      set({
        isLoading: false,
        error: errorMessage,
      });
      throw error;
    }
  },

  validateAnalysisForPlan: async (analysisId: string) => {
    try {
      set({ isValidating: true, error: null });
      
      const response = await api.get(`/analyze/${analysisId}/content-plan/validate`);
      
      set({
        isValidating: false,
        validation: response.data.validation,
      });
    } catch (error: any) {
      const errorMessage = typeof error.response?.data?.error === 'string' 
        ? error.response.data.error 
        : error.response?.data?.message || 'Failed to validate analysis data';
      
      set({
        isValidating: false,
        error: errorMessage,
      });
      throw error;
    }
  },

  deleteContentPlan: async (analysisId: string) => {
    try {
      set({ isLoading: true });
      
      await api.delete(`/analyze/${analysisId}/content-plan`);
      
      set({
        isLoading: false,
        currentPlan: null,
      });
    } catch (error: any) {
      const errorMessage = typeof error.response?.data?.error === 'string' 
        ? error.response.data.error 
        : error.response?.data?.message || 'Failed to delete content plan';
      
      set({
        isLoading: false,
        error: errorMessage,
      });
      throw error;
    }
  },

  clearContentPlan: () => {
    set({
      currentPlan: null,
      validation: null,
      error: null,
      generationProgress: 0,
    });
  },

  setGenerationProgress: (progress: number) => {
    set({ generationProgress: progress });
  },

  clearError: () => {
    set({ error: null });
  },
}));

