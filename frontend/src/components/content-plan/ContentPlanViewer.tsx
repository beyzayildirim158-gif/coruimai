'use client';

import React, { useState, useEffect } from 'react';
import { 
  CalendarIcon, 
  SparklesIcon, 
  ClockIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  DocumentDuplicateIcon,
  CheckIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon,
} from '@heroicons/react/24/outline';
import { useContentPlanStore, DayPlan, ContentPlan } from '@/store/contentPlanSlice';
import DayPlanCard from './DayPlanCard';
import ContentPlanOverview from './ContentPlanOverview';
import StorySchedule from './StorySchedule';

interface ContentPlanViewerProps {
  analysisId: string;
}

const ContentPlanViewer: React.FC<ContentPlanViewerProps> = ({ analysisId }) => {
  const [selectedDay, setSelectedDay] = useState(0);
  const [activeTab, setActiveTab] = useState<'overview' | 'days' | 'stories'>('overview');
  const [copied, setCopied] = useState<string | null>(null);

  const {
    currentPlan,
    isLoading,
    isGenerating,
    error,
    generationProgress,
    generateContentPlan,
    fetchContentPlan,
    clearError,
  } = useContentPlanStore();

  useEffect(() => {
    // Try to fetch existing plan first
    fetchContentPlan(analysisId).catch(() => {
      // Plan doesn't exist, that's fine
    });
  }, [analysisId, fetchContentPlan]);

  const handleGenerate = async () => {
    try {
      await generateContentPlan(analysisId);
    } catch (err) {
      // Error handled by store
    }
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  // Handle both 'days' and 'dailyPlan' keys from backend
  const planDays = currentPlan?.days || currentPlan?.dailyPlan || [];
  
  // Get week dates from either new or old format
  const weekStart = currentPlan?.generatedFor?.planPeriod?.startDate || currentPlan?.weekStartDate || 'Current Week';
  const planUsername = currentPlan?.generatedFor?.handle?.replace('@', '') || currentPlan?.username || '';

  if (isGenerating) {
    return (
      <div className="bg-gradient-to-br from-gray-900 via-purple-900/20 to-gray-900 rounded-2xl p-8 border border-purple-500/20">
        <div className="flex flex-col items-center justify-center py-12">
          <div className="relative mb-6">
            <div className="w-20 h-20 border-4 border-purple-500/30 rounded-full animate-pulse"></div>
            <SparklesIcon className="w-10 h-10 text-purple-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-bounce" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">
            Generating Your 7-Day Content Plan
          </h3>
          <p className="text-gray-400 text-center mb-6 max-w-md">
            Our AI agents are synthesizing insights from your analysis to create
            a personalized content strategy...
          </p>
          <div className="w-full max-w-md">
            <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full transition-all duration-500"
                style={{ width: `${generationProgress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-500 mt-2 text-center">
              {generationProgress}% complete
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (error && !currentPlan) {
    return (
      <div className="bg-gradient-to-br from-gray-900 via-red-900/10 to-gray-900 rounded-2xl p-8 border border-red-500/20">
        <div className="flex flex-col items-center justify-center py-12">
          <ExclamationTriangleIcon className="w-16 h-16 text-red-400 mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">
            Generation Failed
          </h3>
          <p className="text-gray-400 text-center mb-6 max-w-md">{error}</p>
          <div className="flex gap-4">
            <button
              onClick={clearError}
              className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
            >
              Dismiss
            </button>
            <button
              onClick={handleGenerate}
              className="px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:opacity-90 transition-opacity flex items-center gap-2"
            >
              <ArrowPathIcon className="w-5 h-5" />
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!currentPlan) {
    return (
      <div className="bg-gradient-to-br from-gray-900 via-purple-900/20 to-gray-900 rounded-2xl p-8 border border-purple-500/20">
        <div className="flex flex-col items-center justify-center py-12">
          <div className="w-20 h-20 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-full flex items-center justify-center mb-6">
            <CalendarIcon className="w-10 h-10 text-purple-400" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">
            Generate Your 7-Day Content Plan
          </h3>
          <p className="text-gray-400 text-center mb-6 max-w-md">
            Create a personalized week of content based on your analysis results.
            Includes hooks, captions, hashtags, and story schedules.
          </p>
          <button
            onClick={handleGenerate}
            disabled={isLoading}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-medium hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center gap-2"
          >
            <SparklesIcon className="w-5 h-5" />
            Generate Content Plan
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-br from-gray-900 via-purple-900/20 to-gray-900 rounded-2xl p-6 border border-purple-500/20">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <CalendarIcon className="w-7 h-7 text-purple-400" />
              7-Day Content Plan
            </h2>
            <p className="text-gray-400 mt-1">
              Week of {weekStart} • @{planUsername}
            </p>
          </div>
          <button
            onClick={handleGenerate}
            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <ArrowPathIcon className="w-4 h-4" />
            Regenerate
          </button>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 border-b border-gray-700 -mb-px">
          {[
            { id: 'overview', label: 'Overview', icon: SparklesIcon },
            { id: 'days', label: 'Daily Plans', icon: CalendarIcon },
            { id: 'stories', label: 'Story Schedule', icon: ClockIcon },
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id as any)}
              className={`px-4 py-3 flex items-center gap-2 text-sm font-medium transition-colors border-b-2 -mb-px ${
                activeTab === id
                  ? 'text-purple-400 border-purple-400'
                  : 'text-gray-400 border-transparent hover:text-white'
              }`}
            >
              <Icon className="w-4 h-4" />
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <ContentPlanOverview plan={currentPlan} />
      )}

      {activeTab === 'days' && (
        <div className="space-y-4">
          {/* Day Navigation */}
          <div className="flex items-center justify-between bg-gray-900/50 rounded-xl p-4 border border-gray-800">
            <button
              onClick={() => setSelectedDay(Math.max(0, selectedDay - 1))}
              disabled={selectedDay === 0}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeftIcon className="w-5 h-5 text-gray-400" />
            </button>

            <div className="flex gap-2">
              {planDays.map((day, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedDay(idx)}
                  className={`w-12 h-12 rounded-lg flex flex-col items-center justify-center transition-all ${
                    selectedDay === idx
                      ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white scale-110'
                      : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}
                >
                  <span className="text-xs font-medium">{dayNames[idx]}</span>
                  <span className="text-lg font-bold">{idx + 1}</span>
                </button>
              ))}
            </div>

            <button
              onClick={() => setSelectedDay(Math.min(6, selectedDay + 1))}
              disabled={selectedDay === 6}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRightIcon className="w-5 h-5 text-gray-400" />
            </button>
          </div>

          {/* Selected Day Content */}
          {planDays[selectedDay] && (
            <DayPlanCard 
              day={planDays[selectedDay]} 
              onCopy={copyToClipboard}
              copied={copied}
            />
          )}
        </div>
      )}

      {activeTab === 'stories' && (
        <StorySchedule days={planDays} />
      )}
    </div>
  );
};

export default ContentPlanViewer;
