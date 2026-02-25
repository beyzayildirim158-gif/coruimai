'use client';

import React, { useState } from 'react';
import { 
  ArrowTrendingUpIcon,
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  SparklesIcon,
  ChevronDownIcon,
  ChevronUpIcon,
} from '@heroicons/react/24/outline';
import { useTranslation } from '@/i18n/TranslationProvider';
import { sanitizeDisplayText } from '@/lib/textSanitizer';

/**
 * CRITICAL: React Error #31 Fix
 * Bu fonksiyon objeleri güvenli bir şekilde string'e çevirir.
 */
function safeRenderValue(value: any): string {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  if (Array.isArray(value)) {
    return value.map(v => safeRenderValue(v)).filter(Boolean).join(', ');
  }
  if (typeof value === 'object') {
    const entries = Object.entries(value);
    if (entries.length === 0) return '';
    return entries
      .map(([k, v]) => `${k}: ${typeof v === 'object' ? JSON.stringify(v) : v}`)
      .join(' | ');
  }
  return String(value);
}

export interface PriorityAction {
  priority: number;
  action: string;
  description?: string;
  expectedImpact: string;
  impactMetric?: string;
  impactValue?: string;
  difficulty: 'Kolay' | 'Orta' | 'Zor' | 'Easy' | 'Medium' | 'Hard';
  timeToResult: string;
  category?: string;
  implementation?: string[];
}

interface PrioritizedActionsProps {
  actions: PriorityAction[];
  maxVisible?: number;
  title?: string;
}

const difficultyColors = {
  'Kolay': {
    bg: 'bg-green-100',
    text: 'text-green-700',
    border: 'border-green-200',
  },
  'Orta': {
    bg: 'bg-yellow-100',
    text: 'text-yellow-700',
    border: 'border-yellow-200',
  },
  'Zor': {
    bg: 'bg-red-100',
    text: 'text-red-700',
    border: 'border-red-200',
  },
};

const priorityColors = {
  1: 'bg-red-500',
  2: 'bg-orange-500',
  3: 'bg-yellow-500',
  4: 'bg-blue-500',
  5: 'bg-slate-500',
};

const PrioritizedActions: React.FC<PrioritizedActionsProps> = ({
  actions,
  maxVisible = 5,
  title,
}) => {
  const { t, locale } = useTranslation();
  const [showAll, setShowAll] = useState(false);
  const [expandedAction, setExpandedAction] = useState<number | null>(null);

  const sortedActions = [...actions].sort((a, b) => a.priority - b.priority);
  const visibleActions = showAll ? sortedActions : sortedActions.slice(0, maxVisible);
  
  // Map difficulty to locale
  const getDifficultyLabel = (difficulty: string) => {
    const map: Record<string, string> = {
      'Kolay': locale === 'en' ? 'Easy' : 'Kolay',
      'Easy': locale === 'en' ? 'Easy' : 'Kolay',
      'Orta': locale === 'en' ? 'Medium' : 'Orta',
      'Medium': locale === 'en' ? 'Medium' : 'Orta',
      'Zor': locale === 'en' ? 'Hard' : 'Zor',
      'Hard': locale === 'en' ? 'Hard' : 'Zor',
    };
    return map[difficulty] || difficulty;
  };
  
  // Normalize difficulty for color lookup
  const normalizeDifficulty = (difficulty: string): 'Kolay' | 'Orta' | 'Zor' => {
    if (difficulty === 'Easy' || difficulty === 'Kolay') return 'Kolay';
    if (difficulty === 'Medium' || difficulty === 'Orta') return 'Orta';
    return 'Zor';
  };

  return (
    <div className="rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-200 bg-gradient-to-r from-primary-50 to-white">
        <div className="flex items-center gap-3">
          <SparklesIcon className="h-6 w-6 text-primary-500" />
          <h3 className="text-lg font-semibold text-slate-900">{title || `🎯 ${t('actions.title')}`}</h3>
        </div>
        <p className="text-sm text-slate-500 mt-1">
          {t('actions.sortedByPriority')}
        </p>
      </div>

      {/* Actions List */}
      <div className="divide-y divide-slate-100">
        {visibleActions.map((action, idx) => {
          const isExpanded = expandedAction === action.priority;
          const normalizedDiff = normalizeDifficulty(action.difficulty);
          const difficultyStyle = difficultyColors[normalizedDiff];
          const priorityColor = priorityColors[action.priority as keyof typeof priorityColors] || 'bg-slate-500';
          const safeAction = sanitizeDisplayText(action.action, locale === 'tr' ? 'Genel Strateji' : 'General Strategy');
          const safeDescription = sanitizeDisplayText(action.description, '');
          const safeExpectedImpact = sanitizeDisplayText(action.expectedImpact, locale === 'tr' ? 'Genel Strateji' : 'General Strategy');
          const safeTimeToResult = sanitizeDisplayText(action.timeToResult, locale === 'tr' ? '2-4 hafta' : '2-4 weeks');
          const safeCategory = sanitizeDisplayText(action.category, '');

          return (
            <div 
              key={idx}
              className={`transition-colors ${isExpanded ? 'bg-slate-50' : 'hover:bg-slate-50/50'}`}
            >
              {/* Main Action Row */}
              <button
                onClick={() => setExpandedAction(isExpanded ? null : action.priority)}
                className="w-full px-6 py-4 text-left"
              >
                <div className="flex items-start gap-4">
                  {/* Priority Badge */}
                  <div className={`flex-shrink-0 w-8 h-8 ${priorityColor} rounded-full flex items-center justify-center`}>
                    <span className="text-white font-bold text-sm">#{action.priority}</span>
                  </div>

                  {/* Action Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h4 className="font-semibold text-slate-900">{safeAction}</h4>
                        {safeDescription && (
                          <p className="text-sm text-slate-600 mt-1">{safeDescription}</p>
                        )}
                      </div>
                      {isExpanded ? (
                        <ChevronUpIcon className="w-5 h-5 text-slate-400 flex-shrink-0" />
                      ) : (
                        <ChevronDownIcon className="w-5 h-5 text-slate-400 flex-shrink-0" />
                      )}
                    </div>

                    {/* Quick Stats */}
                    <div className="flex flex-wrap items-center gap-3 mt-3">
                      {/* Expected Impact */}
                      <div className="flex items-center gap-1.5 text-sm">
                        <ArrowTrendingUpIcon className="w-4 h-4 text-green-500" />
                        <span className="text-green-600 font-medium">{safeExpectedImpact}</span>
                      </div>

                      {/* Difficulty */}
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${difficultyStyle.bg} ${difficultyStyle.text}`}>
                        {getDifficultyLabel(action.difficulty)}
                      </span>

                      {/* Time to Result */}
                      <div className="flex items-center gap-1 text-sm text-slate-500">
                        <ClockIcon className="w-4 h-4" />
                        <span>{safeTimeToResult}</span>
                      </div>

                      {/* Category */}
                      {safeCategory && (
                        <span className="px-2 py-0.5 rounded-full text-xs bg-slate-100 text-slate-600">
                          {safeCategory}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </button>

              {/* Expanded Details */}
              {isExpanded && action.implementation && action.implementation.length > 0 && (
                <div className="px-6 pb-4 pl-18">
                  <div className="ml-12 p-4 bg-white rounded-xl border border-slate-200">
                    <h5 className="text-sm font-medium text-slate-700 mb-2">
                      📋 {t('actions.howToImplement')}
                    </h5>
                    <ol className="space-y-2">
                      {action.implementation.map((step, stepIdx) => (
                        <li key={stepIdx} className="flex items-start gap-2 text-sm text-slate-600">
                          <span className="flex-shrink-0 w-5 h-5 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-xs font-medium">
                            {stepIdx + 1}
                          </span>
                          <span>{sanitizeDisplayText(step, locale === 'tr' ? 'Genel Strateji' : 'General Strategy')}</span>
                        </li>
                      ))}
                    </ol>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Show More/Less */}
      {actions.length > maxVisible && (
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50">
          <button
            onClick={() => setShowAll(!showAll)}
            className="w-full text-center text-sm font-medium text-primary-600 hover:text-primary-700"
          >
            {showAll ? `${t('actions.showLess')} ▲` : `${actions.length - maxVisible} ${t('actions.showMore')} ▼`}
          </button>
        </div>
      )}

      {/* Summary Footer */}
      <div className="px-6 py-4 border-t border-slate-200 bg-gradient-to-r from-green-50 to-white">
        <div className="flex items-center gap-2 text-sm">
          <CheckCircleIcon className="w-5 h-5 text-green-500" />
          <span className="text-slate-700">
            <span className="font-medium text-green-600">
              {actions.filter(a => normalizeDifficulty(a.difficulty) === 'Kolay').length}
            </span> {t('actions.easyActions')}
          </span>
        </div>
      </div>
    </div>
  );
};

export default PrioritizedActions;

// TAGGING_PRECISION: infer category from action text when no explicit tag exists
function inferCategory(actionText: string, rawCategory?: string): string {
  // If backend already sent a meaningful non-generic tag, keep it
  if (
    rawCategory &&
    rawCategory.trim() !== '' &&
    rawCategory.toLowerCase() !== 'general strategy' &&
    rawCategory.toLowerCase() !== 'general' &&
    rawCategory.toLowerCase() !== 'genel strateji' &&
    rawCategory.toLowerCase() !== 'genel'
  ) {
    return rawCategory;
  }

  const lower = (actionText || '').toLowerCase();

  const VISIBILITY_KW = ['hashtag', '#', 'etiket', 'keşfet', 'reach', 'erişim', 'visibility', 'görünürlük', 'discovery', 'keşif', 'explore'];
  const CONTENT_KW    = ['content', 'içerik', 'reel', 'story', 'caption', 'gönderi', 'video', 'post', 'yayın', 'yazı', 'format', 'template', 'hook', 'senaryo', 'scenario'];
  const MONETIZATION_KW = ['money', 'sponsor', 'collab', 'gelir', 'kazanç', 'monetiz', 'brand deal', 'satış', 'sales', 'affiliate', 'paid', 'ücretli', 'işbirliği', 'reklam', 'revenue', 'income', 'conversion'];

  if (VISIBILITY_KW.some((kw) => lower.includes(kw))) return 'Visibility';
  if (MONETIZATION_KW.some((kw) => lower.includes(kw))) return 'Monetization';
  if (CONTENT_KW.some((kw) => lower.includes(kw))) return 'Content';

  return ''; // No generic fallback — omit the badge entirely
}

// Helper to create priority action from recommendation
export function createPriorityAction(
  priority: number,
  action: string,
  options: Partial<Omit<PriorityAction, 'priority' | 'action'>> = {}
): PriorityAction {
  const cleanAction = sanitizeDisplayText(action, '');
  return {
    priority,
    action: cleanAction,
    description: sanitizeDisplayText(options.description, ''),
    expectedImpact: sanitizeDisplayText(options.expectedImpact, ''),
    impactMetric: options.impactMetric,
    impactValue: options.impactValue,
    difficulty: options.difficulty || 'Orta',
    timeToResult: sanitizeDisplayText(options.timeToResult, '2-4 hafta'),
    // Apply tagging precision: infer category from action text if needed
    category: inferCategory(cleanAction, sanitizeDisplayText(options.category, '')),
    implementation: Array.isArray(options.implementation)
      ? options.implementation.map((step) => sanitizeDisplayText(step, '')).filter(Boolean)
      : options.implementation,
  };
}

// Extract actions from analysis recommendations
export function extractPriorityActions(analysis: any): PriorityAction[] {
  const actions: PriorityAction[] = [];
  const recommendations = analysis.recommendations || [];
  
  recommendations.forEach((rec: any, idx: number) => {
    if (typeof rec === 'string') {
      actions.push(createPriorityAction(idx + 1, rec));
    } else {
      // Safely convert action to string
      const actionText = typeof rec.action === 'string' ? rec.action :
                        typeof rec.recommendation === 'string' ? rec.recommendation :
                        typeof rec.title === 'string' ? rec.title :
                        safeRenderValue(rec.action || rec.recommendation || rec.title) || 'Aksiyon';
      
      // Safely convert expected_impact to string
      const impactText = typeof rec.expected_impact === 'string' ? rec.expected_impact :
                        typeof rec.impact === 'string' ? rec.impact :
                        safeRenderValue(rec.expected_impact || rec.impact) || 'Etkileşim artışı';
      
      actions.push(createPriorityAction(
        rec.priority || idx + 1,
        actionText,
        {
          description: rec.description || rec.details,
          expectedImpact: impactText,
          difficulty: rec.difficulty === 'easy' ? 'Kolay' : 
                      rec.difficulty === 'hard' ? 'Zor' : 'Orta',
          timeToResult: rec.time_to_result || rec.timeframe || '2-4 hafta',
          category: rec.category,
          implementation: rec.implementation_steps || rec.steps,
        }
      ));
    }
  });
  
  // Add agent-specific recommendations
  const agentResults = analysis.agentResults || {};
  
  // Content Strategist recommendations
  if (agentResults.contentStrategist?.recommendations) {
    agentResults.contentStrategist.recommendations.slice(0, 2).forEach((rec: any, idx: number) => {
      const recAction = typeof rec === 'string' ? rec : 
                       (typeof rec.action === 'string' ? rec.action : 
                        typeof rec.recommendation === 'string' ? rec.recommendation :
                        safeRenderValue(rec.action || rec.recommendation));
      if (!actions.find(a => a.action === recAction)) {
        const impactText = typeof rec.expected_impact === 'string' ? rec.expected_impact :
                          safeRenderValue(rec.expected_impact) || 'İçerik performansı artışı';
        actions.push(createPriorityAction(
          actions.length + 1,
          recAction,
          {
            category: 'İçerik Stratejisi',
            expectedImpact: impactText,
            difficulty: 'Orta',
            timeToResult: '2-3 hafta',
          }
        ));
      }
    });
  }
  
  // Growth recommendations
  if (agentResults.growthVirality?.recommendations) {
    agentResults.growthVirality.recommendations.slice(0, 2).forEach((rec: any, idx: number) => {
      const recAction = typeof rec === 'string' ? rec : 
                       (typeof rec.action === 'string' ? rec.action : 
                        typeof rec.recommendation === 'string' ? rec.recommendation :
                        safeRenderValue(rec.action || rec.recommendation));
      if (!actions.find(a => a.action === recAction)) {
        const impactText = typeof rec.expected_impact === 'string' ? rec.expected_impact :
                          safeRenderValue(rec.expected_impact) || 'Takipçi artışı';
        actions.push(createPriorityAction(
          actions.length + 1,
          recAction,
          {
            category: 'Büyüme',
            expectedImpact: impactText,
            difficulty: 'Orta',
            timeToResult: '4-6 hafta',
          }
        ));
      }
    });
  }
  
  return actions.slice(0, 10); // Max 10 actions
}
