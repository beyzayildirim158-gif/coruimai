'use client';

import React from 'react';
import { 
  ChartBarIcon,
  UserGroupIcon,
  ChatBubbleLeftRightIcon,
  SparklesIcon,
  LightBulbIcon,
  CheckCircleIcon,
  WrenchScrewdriverIcon,
} from '@heroicons/react/24/outline';
import { ContentPlan } from '@/store/contentPlanSlice';

interface ContentPlanOverviewProps {
  plan: ContentPlan;
}

const ContentPlanOverview: React.FC<ContentPlanOverviewProps> = ({ plan }) => {
  // Guard clause for undefined/null plan
  if (!plan) {
    return (
      <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
        <p className="text-gray-400 text-center">Content plan data not available</p>
      </div>
    );
  }

  // Extract with defaults for both old and new format - cast to any for union type compatibility
  const strategy = (plan.overallStrategy || plan.weeklyStrategy) as Record<string, unknown> | undefined;
  const weeklyTheme = (strategy?.weeklyTheme as string) || (strategy?.theme as string) || 'Content Strategy';
  const primaryGoal = (strategy?.primaryGoal as string) || ((strategy?.goals as string[])?.[0]) || 'Increase engagement';
  const secondaryGoals: string[] = (strategy?.secondaryGoals as string[]) || (strategy?.goals as string[])?.slice(1) || [];
  const targetAudience = (strategy?.targetAudience as string) || 'Target audience';
  const brandVoice = (strategy?.brandVoice as string) || 'Professional';
  const keyMessages: string[] = (strategy?.keyMessages as string[]) || [];
  
  const weeklyMetrics = plan.weeklyMetrics;
  const kpis = plan.kpis;
  
  const implementation = (plan.implementation || plan.implementationNotes) as Record<string, unknown> | undefined;
  const dataSourcesUsed = plan.dataSourcesUsed || [
    'Audience Dynamics',
    'Content Strategist', 
    'Attention Architect',
    'Visual Brand',
    'Growth Architect',
    'Domain Master'
  ];

  // Get content mix from either format
  const contentMixRatio = weeklyMetrics?.contentMixRatio || 
    plan.weeklyStrategy?.contentMixRatio || 
    { reels: 40, carousels: 30, staticPosts: 20, stories: 10 };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Strategy Overview */}
      <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <SparklesIcon className="w-5 h-5 text-purple-400" />
          Weekly Strategy
        </h3>
        
        <div className="space-y-4">
          <div>
            <span className="text-xs text-gray-500 uppercase tracking-wider block">Weekly Theme</span>
            <p className="text-white font-medium mt-1">{weeklyTheme}</p>
          </div>
          
          <div>
            <span className="text-xs text-gray-500 uppercase tracking-wider block">Primary Goal</span>
            <p className="text-white font-medium mt-1">{primaryGoal}</p>
          </div>

          {secondaryGoals.length > 0 && (
            <div>
              <span className="text-xs text-gray-500 uppercase tracking-wider block">Secondary Goals</span>
              <ul className="mt-1 space-y-1">
                {secondaryGoals.map((goal: string, idx: number) => (
                  <li key={idx} className="text-gray-300 flex items-start gap-2">
                    <CheckCircleIcon className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" />
                    {goal}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div>
            <span className="text-xs text-gray-500 uppercase tracking-wider block">Target Audience</span>
            <p className="text-gray-300 mt-1">{targetAudience}</p>
          </div>

          <div>
            <span className="text-xs text-gray-500 uppercase tracking-wider block">Brand Voice</span>
            <p className="text-gray-300 mt-1">{brandVoice}</p>
          </div>

          {keyMessages.length > 0 && (
            <div>
              <span className="text-xs text-gray-500 uppercase tracking-wider block">Key Messages</span>
              <div className="flex flex-wrap gap-2 mt-2">
                {keyMessages.map((message: string, idx: number) => (
                  <span key={idx} className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-sm">
                    {message}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Expected Metrics */}
      <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <ChartBarIcon className="w-5 h-5 text-blue-400" />
          Expected Results
        </h3>
        
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-gray-800/50 rounded-lg p-4">
            <p className="text-sm text-gray-400">Follower Growth</p>
            <p className="text-2xl font-bold text-green-400">
              {weeklyMetrics?.expectedFollowerGrowth || kpis?.weeklyTargets?.targetFollowerGrowth || '+2-5%'}
            </p>
          </div>
          <div className="bg-gray-800/50 rounded-lg p-4">
            <p className="text-sm text-gray-400">Engagement Rate</p>
            <p className="text-2xl font-bold text-blue-400">
              {weeklyMetrics?.expectedEngagementRate || kpis?.weeklyTargets?.targetEngagementRate || '4-6%'}
            </p>
          </div>
          <div className="bg-gray-800/50 rounded-lg p-4 col-span-2">
            <p className="text-sm text-gray-400">Expected Reach</p>
            <p className="text-2xl font-bold text-purple-400">
              {weeklyMetrics?.expectedReach || kpis?.weeklyTargets?.targetReach || '10K-50K'}
            </p>
          </div>
        </div>

        <div>
          <span className="text-xs text-gray-500 uppercase tracking-wider block">Content Mix</span>
          <div className="grid grid-cols-2 gap-3 mt-2">
            {Object.entries(contentMixRatio).map(([type, percentage]) => (
              <div key={type} className="flex items-center justify-between">
                <span className="text-gray-400 capitalize">{type}</span>
                <div className="flex items-center gap-2">
                  <div className="w-20 h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                  <span className="text-white text-sm font-medium w-8">{percentage}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Implementation Guide */}
      <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <WrenchScrewdriverIcon className="w-5 h-5 text-orange-400" />
          Implementation Guide
        </h3>
        
        <div className="space-y-4">
          {((implementation?.toolsNeeded as string[])?.length ?? 0) > 0 && (
            <div>
              <span className="text-xs text-gray-500 uppercase tracking-wider block">Tools Needed</span>
              <div className="flex flex-wrap gap-2 mt-2">
                {(implementation?.toolsNeeded as string[])?.map((tool: string, idx: number) => (
                  <span key={idx} className="px-3 py-1 bg-gray-800 text-gray-300 rounded-lg text-sm">
                    {tool}
                  </span>
                ))}
              </div>
            </div>
          )}

          {((implementation?.preparationChecklist as string[])?.length ?? 0) > 0 && (
            <div>
              <span className="text-xs text-gray-500 uppercase tracking-wider block">Preparation Checklist</span>
              <ul className="mt-2 space-y-2">
                {(implementation?.preparationChecklist as string[])?.map((item: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-2 text-gray-300">
                    <input 
                      type="checkbox" 
                      id={`prep-item-${idx}`}
                      name={`prep-item-${idx}`}
                      autoComplete="off"
                      className="mt-1 rounded border-gray-600 bg-gray-800 text-purple-500 focus:ring-purple-500"
                    />
                    <label htmlFor={`prep-item-${idx}`}>{item}</label>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {((implementation?.contentBatching as string[])?.length ?? 0) > 0 && (
            <div>
              <span className="text-xs text-gray-500 uppercase tracking-wider block">Content Batching Tips</span>
              <ul className="mt-2 space-y-2">
                {(implementation?.contentBatching as string[])?.map((tip: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-2 text-gray-300">
                    <LightBulbIcon className="w-4 h-4 text-yellow-400 mt-0.5 flex-shrink-0" />
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* New format: criticalSuccessFactors */}
          {((implementation?.criticalSuccessFactors as string[])?.length ?? 0) > 0 && (
            <div>
              <span className="text-xs text-gray-500 uppercase tracking-wider block">Critical Success Factors</span>
              <ul className="mt-2 space-y-2">
                {(implementation?.criticalSuccessFactors as string[])?.map((factor: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-2 text-gray-300">
                    <CheckCircleIcon className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" />
                    {factor}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* New format: potentialChallenges */}
          {((implementation?.potentialChallenges as string[])?.length ?? 0) > 0 && (
            <div>
              <span className="text-xs text-gray-500 uppercase tracking-wider block">Potential Challenges</span>
              <ul className="mt-2 space-y-2">
                {(implementation?.potentialChallenges as string[])?.map((challenge: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-2 text-gray-300">
                    <LightBulbIcon className="w-4 h-4 text-orange-400 mt-0.5 flex-shrink-0" />
                    {challenge}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Data Sources */}
      <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-800">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <ChatBubbleLeftRightIcon className="w-5 h-5 text-cyan-400" />
          Data Sources Used
        </h3>
        
        <p className="text-gray-400 text-sm mb-4">
          This content plan was generated using insights from the following AI agents:
        </p>
        
        <div className="grid grid-cols-2 gap-3">
          {dataSourcesUsed.map((source, idx) => (
            <div key={idx} className="flex items-center gap-2 bg-gray-800/50 rounded-lg p-3">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-lg flex items-center justify-center">
                <UserGroupIcon className="w-4 h-4 text-purple-400" />
              </div>
              <span className="text-gray-300 text-sm">{source}</span>
            </div>
          ))}
        </div>

        {/* Validation Report - New Format */}
        {plan.validationReport && (
          <div className="mt-6 pt-4 border-t border-gray-700">
            <span className="text-xs text-gray-500 uppercase tracking-wider mb-3 block">Data Validation</span>
            <div className="grid grid-cols-2 gap-2">
              {Object.entries(plan.validationReport).map(([key, value]) => {
                if (key === 'dataCompleteness') {
                  return (
                    <div key={key} className="col-span-2 flex items-center justify-between bg-gray-800/30 rounded p-2">
                      <span className="text-gray-400 text-sm">Data Completeness</span>
                      <span className="text-purple-400 font-medium">{typeof value === 'number' ? `${value}%` : value}</span>
                    </div>
                  );
                }
                return (
                  <div key={key} className="flex items-center gap-2 text-sm">
                    <span className={value ? 'text-green-400' : 'text-red-400'}>
                      {value ? '✓' : '✗'}
                    </span>
                    <span className="text-gray-400 capitalize">
                      {key.replace(/([A-Z])/g, ' $1').trim()}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ContentPlanOverview;
