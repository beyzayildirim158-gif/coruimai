// Types shared across the application
// Mirrors @instagram-ai/shared for Docker build compatibility

export type SubscriptionTier = 'STARTER' | 'PROFESSIONAL' | 'PREMIUM' | 'ENTERPRISE';

export type SubscriptionStatus = 'ACTIVE' | 'CANCELLED' | 'PAST_DUE' | 'TRIALING' | 'PAUSED';

export interface UsageSnapshot {
  monthYear: string;
  analysesUsed: number;
  requestsCount: number;
}

export interface AnalysisAccountSummary {
  username: string;
  followers?: number;
  posts?: number;
  engagementRate?: number;
  profilePicUrl?: string | null;
}

export interface AgentInsight {
  agentName: string;
  agentRole: string;
  findings?: string[];
  recommendations?: string[];
  metrics?: Record<string, unknown>;
}

export interface AnalysisSummary {
  id: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED' | 'CANCELLED';
  overallScore?: number | null;
  scoreGrade?: string | null;
  createdAt: string;
  completedAt?: string | null;
  account: AnalysisAccountSummary;
  agentResults?: Record<string, AgentInsight>;
}

export interface ReportSummary {
  id: string;
  reportType: 'FULL' | 'SUMMARY' | 'EXECUTIVE';
  generatedAt?: string | null;
  pdfUrl?: string | null;
  analysis?: AnalysisSummary;
}

export interface PaginatedResult<T> {
  items: T[];
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}
