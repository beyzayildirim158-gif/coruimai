'use client';

import React, { useState } from 'react';
import { 
  ClockIcon,
  ChatBubbleLeftIcon,
  SparklesIcon,
  GiftIcon,
  HeartIcon,
  UserIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  QuestionMarkCircleIcon,
  ShareIcon,
  EyeIcon,
} from '@heroicons/react/24/outline';
import { DayPlan, StorySlot } from '@/store/contentPlanSlice';

interface StoryScheduleProps {
  days: DayPlan[];
}

// Map story types (both old and new formats)
const getStoryTypeKey = (type: string): string => {
  const typeMap: Record<string, string> = {
    'Poll': 'engagement',
    'poll': 'engagement',
    'engagement': 'engagement',
    'Question': 'engagement',
    'Quiz': 'engagement',
    'Teaser': 'teaser',
    'teaser': 'teaser',
    'preview': 'teaser',
    'Post Share': 'promotion',
    'post_share': 'promotion',
    'promotion': 'promotion',
    'Behind Scenes': 'personal',
    'behind_scenes': 'personal',
    'personal': 'personal',
    'BTS': 'personal',
    'Q&A': 'value',
    'value': 'value',
    'tip': 'value',
  };
  return typeMap[type] || 'value';
};

const storyTypeIcons: Record<string, React.ElementType> = {
  engagement: ChatBubbleLeftIcon,
  value: SparklesIcon,
  teaser: GiftIcon,
  promotion: HeartIcon,
  personal: UserIcon,
};

const storyTypeColors: Record<string, string> = {
  engagement: 'text-green-400 bg-green-500/10 border-green-500/30',
  value: 'text-blue-400 bg-blue-500/10 border-blue-500/30',
  teaser: 'text-purple-400 bg-purple-500/10 border-purple-500/30',
  promotion: 'text-pink-400 bg-pink-500/10 border-pink-500/30',
  personal: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30',
};

const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

const StorySchedule: React.FC<StoryScheduleProps> = ({ days }) => {
  const [expandedDays, setExpandedDays] = useState<Record<number, boolean>>({
    0: true, // Monday expanded by default
  });

  const toggleDay = (dayIndex: number) => {
    setExpandedDays(prev => ({ ...prev, [dayIndex]: !prev[dayIndex] }));
  };

  return (
    <div className="space-y-4">
      {/* Legend */}
      <div className="bg-gray-900/50 rounded-xl p-4 border border-gray-800">
        <h4 className="text-sm font-medium text-white mb-3">Story Types</h4>
        <div className="flex flex-wrap gap-3">
          {Object.entries(storyTypeColors).map(([type, colorClass]) => {
            const Icon = storyTypeIcons[type];
            return (
              <div 
                key={type}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border ${colorClass}`}
              >
                <Icon className="w-4 h-4" />
                <span className="text-sm capitalize">{type}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Weekly Schedule */}
      <div className="space-y-3">
        {days.map((day, dayIndex) => (
          <div 
            key={dayIndex}
            className="bg-gray-900/50 rounded-xl border border-gray-800 overflow-hidden"
          >
            {/* Day Header */}
            <button
              onClick={() => toggleDay(dayIndex)}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-800/50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-lg flex items-center justify-center">
                  <span className="text-lg font-bold text-white">{dayIndex + 1}</span>
                </div>
                <div className="text-left">
                  <h4 className="font-medium text-white">{dayNames[dayIndex]}</h4>
                  <p className="text-sm text-gray-400">{day.stories.length} story slots</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="hidden md:flex items-center gap-2">
                  {day.stories.slice(0, 5).map((story, idx) => {
                    const typeKey = getStoryTypeKey(story.type);
                    const Icon = storyTypeIcons[typeKey] || SparklesIcon;
                    const colorClass = storyTypeColors[typeKey] || storyTypeColors.value;
                    return (
                      <div
                        key={idx}
                        className={`w-8 h-8 rounded-lg flex items-center justify-center border ${colorClass}`}
                        title={`${story.type} at ${story.time}`}
                      >
                        <Icon className="w-4 h-4" />
                      </div>
                    );
                  })}
                </div>
                {expandedDays[dayIndex] ? (
                  <ChevronUpIcon className="w-5 h-5 text-gray-400" />
                ) : (
                  <ChevronDownIcon className="w-5 h-5 text-gray-400" />
                )}
              </div>
            </button>

            {/* Day Stories */}
            {expandedDays[dayIndex] && (
              <div className="px-4 pb-4">
                <div className="relative">
                  {/* Timeline */}
                  <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-700"></div>
                  
                  <div className="space-y-4">
                    {day.stories.map((story, storyIndex) => (
                      <StorySlotCard key={storyIndex} story={story} />
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

interface StorySlotCardProps {
  story: StorySlot;
}

const StorySlotCard: React.FC<StorySlotCardProps> = ({ story }) => {
  const typeKey = getStoryTypeKey(story.type);
  const Icon = storyTypeIcons[typeKey] || SparklesIcon;
  const colorClass = storyTypeColors[typeKey] || storyTypeColors.value;
  const [showStickers, setShowStickers] = useState(false);

  // Get slot number from either format
  const slotNumber = story.slot || story.slotNumber || 0;
  
  // Get stickers from either format
  const stickers = story.stickerSuggestions || (story.sticker ? [story.sticker] : []);
  
  // Get interactive element or poll options
  const hasOptions = story.options && story.options.length > 0;

  return (
    <div className="relative pl-10">
      {/* Timeline Dot */}
      <div className={`absolute left-2 w-5 h-5 rounded-full border-2 bg-gray-900 ${colorClass.split(' ')[2]}`}>
        <div className={`w-full h-full rounded-full flex items-center justify-center ${colorClass.split(' ')[1]}`}>
          <div className="w-2 h-2 rounded-full bg-current"></div>
        </div>
      </div>

      {/* Story Content */}
      <div className={`rounded-xl border p-4 ${colorClass}`}>
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <Icon className="w-5 h-5" />
            <span className="font-medium">{story.type}</span>
            <span className="text-sm opacity-70">Slot #{slotNumber}</span>
            {story.purpose && (
              <span className="text-xs px-2 py-0.5 bg-black/20 rounded-full">{story.purpose.replace(/_/g, ' ')}</span>
            )}
          </div>
          <div className="flex items-center gap-1 text-sm font-medium">
            <ClockIcon className="w-4 h-4" />
            {story.time}
          </div>
        </div>

        <p className="text-white/90 mb-3">{story.content}</p>

        {/* Poll Options - New Format */}
        {hasOptions && (
          <div className="bg-black/20 rounded-lg p-3 mb-3">
            <span className="text-xs opacity-70 block mb-2">Poll Options:</span>
            <div className="flex flex-wrap gap-2">
              {story.options!.map((option, idx) => (
                <span key={idx} className="px-3 py-1.5 bg-white/10 rounded-lg text-sm font-medium">
                  {option}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Visual Hint - New Format */}
        {story.visualHint && (
          <div className="bg-black/20 rounded-lg px-3 py-2 mb-3">
            <span className="text-xs opacity-70">Visual Style:</span>
            <p className="text-sm font-medium">{story.visualHint}</p>
          </div>
        )}

        {/* Engagement CTA - New Format */}
        {story.engagementCTA && (
          <div className="bg-black/20 rounded-lg px-3 py-2 mb-3">
            <span className="text-xs opacity-70">Engagement CTA:</span>
            <p className="text-sm font-medium text-purple-300">{story.engagementCTA}</p>
          </div>
        )}

        {story.interactiveElement && (
          <div className="bg-black/20 rounded-lg px-3 py-2 mb-3">
            <span className="text-xs opacity-70">Interactive Element:</span>
            <p className="text-sm font-medium">{story.interactiveElement}</p>
          </div>
        )}

        {stickers.length > 0 && (
          <div>
            <button
              onClick={() => setShowStickers(!showStickers)}
              className="text-sm opacity-70 hover:opacity-100 transition-opacity"
            >
              {showStickers ? 'Hide' : 'Show'} sticker{stickers.length > 1 ? 's' : ''} ({stickers.length})
            </button>
            {showStickers && (
              <div className="flex flex-wrap gap-2 mt-2">
                {stickers.map((sticker, idx) => (
                  <span 
                    key={idx}
                    className="px-2 py-1 bg-black/20 rounded text-xs"
                  >
                    {sticker}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default StorySchedule;
