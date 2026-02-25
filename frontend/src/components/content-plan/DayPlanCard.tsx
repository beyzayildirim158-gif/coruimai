'use client';

import React, { useState } from 'react';
import { 
  DocumentDuplicateIcon,
  CheckIcon,
  HashtagIcon,
  PhotoIcon,
  ClockIcon,
  ChatBubbleBottomCenterTextIcon,
  SparklesIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  EyeIcon,
  HeartIcon,
  BookmarkIcon,
  ShareIcon,
  ExclamationCircleIcon,
  MapPinIcon,
} from '@heroicons/react/24/outline';
import { DayPlan, HashtagCategory } from '@/store/contentPlanSlice';

interface DayPlanCardProps {
  day: DayPlan;
  onCopy: (text: string, id: string) => void;
  copied: string | null;
}

const purposeColors: Record<string, { bg: string; text: string; border: string }> = {
  'HOOK_DAY': { bg: 'from-red-500/20 to-orange-500/20', text: 'text-red-400', border: 'border-red-500/30' },
  'VALUE_DAY': { bg: 'from-blue-500/20 to-cyan-500/20', text: 'text-blue-400', border: 'border-blue-500/30' },
  'ENGAGEMENT_DAY': { bg: 'from-green-500/20 to-emerald-500/20', text: 'text-green-400', border: 'border-green-500/30' },
  'AUTHORITY_DAY': { bg: 'from-purple-500/20 to-violet-500/20', text: 'text-purple-400', border: 'border-purple-500/30' },
  'VIRAL_ATTEMPT_DAY': { bg: 'from-pink-500/20 to-rose-500/20', text: 'text-pink-400', border: 'border-pink-500/30' },
  'COMMUNITY_DAY': { bg: 'from-yellow-500/20 to-amber-500/20', text: 'text-yellow-400', border: 'border-yellow-500/30' },
  'SOFT_SELL_DAY': { bg: 'from-teal-500/20 to-cyan-500/20', text: 'text-teal-400', border: 'border-teal-500/30' },
};

// Helper to extract hashtag tags from either new or old format
const getHashtagTags = (hashtags: any, category: string): string[] => {
  if (!hashtags || !hashtags[category]) return [];
  const value = hashtags[category];
  if (Array.isArray(value)) return value;
  if (value && typeof value === 'object' && 'tags' in value) return value.tags || [];
  return [];
};

// Helper to get all hashtags as a single string
const getAllHashtags = (hashtags: any): string => {
  const primary = getHashtagTags(hashtags, 'primary');
  const niche = getHashtagTags(hashtags, 'niche');
  const trending = getHashtagTags(hashtags, 'trending');
  const branded = hashtags?.branded || [];
  const secondary = getHashtagTags(hashtags, 'secondary');
  
  return [...primary, ...niche, ...trending, ...branded, ...secondary]
    .filter(Boolean)
    .map(t => `#${t}`)
    .join(' ');
};

const DayPlanCard: React.FC<DayPlanCardProps> = ({ day, onCopy, copied }) => {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    hook: true,
    caption: true,
    hashtags: false,
    visual: false,
    painPoint: false,
    stories: false,
  });

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  // Get purpose name from either new or old format
  const purposeName = day.dayPurpose?.name || day.purpose || 'VALUE_DAY';
  const purposeStyle = purposeColors[purposeName] || purposeColors['VALUE_DAY'];
  
  // Handle both old (mainPost) and new (direct) data formats
  const mainPost = day.mainPost;
  const hasNewFormat = !mainPost && day.content;
  
  // Extract data based on format
  const dayNumber = day.day || day.dayNumber || 1;
  const dayName = day.dayOfWeek || day.dayName || '';
  const topicRaw = hasNewFormat ? day.topic : mainPost?.topic;
  const topic = typeof topicRaw === 'string' ? topicRaw : (topicRaw?.title || '');
  const topicData = typeof day.topic === 'object' ? day.topic : null;
  
  // Get hook data
  const hook = hasNewFormat ? day.content?.hook : mainPost?.hook;
  
  // Get caption data
  const caption = hasNewFormat ? day.caption : mainPost?.caption;
  const fullCaptionText = caption?.fullText || caption?.fullCaption || '';
  const charCount = caption?.charCount || caption?.characterCount || 0;
  
  // Get hashtags
  const hashtags = hasNewFormat ? day.hashtags : mainPost?.hashtags;
  
  // Get visual guidelines
  const visual = hasNewFormat ? day.visualGuidelines : mainPost?.visualGuidelines;
  
  // Get posting time
  const postingTime = day.postingTime?.time || mainPost?.bestPostingTime || '';
  const timezone = day.postingTime?.timezone || '';
  
  // Get engagement metrics
  const engagement = hasNewFormat ? day.engagement?.expectedMetrics : mainPost?.estimatedEngagement;

  // Get daily stories
  const stories = day.stories || [];

  return (
    <div className={`bg-gradient-to-br ${purposeStyle.bg} rounded-2xl border ${purposeStyle.border} overflow-hidden`}>
      {/* Day Header */}
      <div className="p-6 border-b border-gray-800/50">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${purposeStyle.text} bg-gray-900/50`}>
                Day {dayNumber} - {dayName}
              </span>
              <span className={`text-sm ${purposeStyle.text}`}>{purposeName.replace(/_/g, ' ')}</span>
            </div>
            <h3 className="text-xl font-bold text-white">{topic}</h3>
            <p className="text-gray-400 mt-1">
              {day.dayPurpose?.objective || day.purposeDescription}
            </p>
          </div>
          <div className="flex flex-col items-end gap-2">
            <div className="flex items-center gap-2 text-gray-400 bg-gray-900/50 px-3 py-1.5 rounded-lg">
              <ClockIcon className="w-4 h-4" />
              <span className="text-sm font-medium">{postingTime}</span>
            </div>
            {timezone && (
              <span className="text-xs text-gray-500">{timezone}</span>
            )}
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Pain Point Mapping - NEW */}
        {topicData?.linkedPainPoint && (
          <div className="bg-gray-900/50 rounded-xl overflow-hidden">
            <button 
              onClick={() => toggleSection('painPoint')}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-800/50 transition-colors"
            >
              <div className="flex items-center gap-2">
                <ExclamationCircleIcon className="w-5 h-5 text-orange-400" />
                <span className="font-medium text-white">Pain Point Mapping</span>
              </div>
              {expandedSections.painPoint ? (
                <ChevronUpIcon className="w-5 h-5 text-gray-400" />
              ) : (
                <ChevronDownIcon className="w-5 h-5 text-gray-400" />
              )}
            </button>
            
            {expandedSections.painPoint && (
              <div className="px-4 pb-4 space-y-3">
                <div className="bg-gray-800/50 rounded-lg p-4">
                  <div className="mb-3">
                    <span className="text-xs text-gray-500 uppercase tracking-wider block">Linked Pain Point</span>
                    <p className="text-orange-300 mt-1 font-medium">{topicData.linkedPainPoint}</p>
                  </div>
                  {topicData.audienceRelevance && (
                    <div className="grid grid-cols-3 gap-4 pt-3 border-t border-gray-700">
                      <div>
                        <span className="text-xs text-gray-500 block">Relevance Score</span>
                        <p className="text-white font-semibold">{topicData.audienceRelevance.score}/10</p>
                      </div>
                      <div>
                        <span className="text-xs text-gray-500 block">Persona Match</span>
                        <p className="text-white text-sm">{topicData.audienceRelevance.primaryPersonaMatch}</p>
                      </div>
                      <div>
                        <span className="text-xs text-gray-500 block">Engagement Potential</span>
                        <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${
                          topicData.audienceRelevance.engagementPotential === 'high' 
                            ? 'bg-green-500/20 text-green-400'
                            : topicData.audienceRelevance.engagementPotential === 'medium'
                            ? 'bg-yellow-500/20 text-yellow-400'
                            : 'bg-gray-500/20 text-gray-400'
                        }`}>
                          {topicData.audienceRelevance.engagementPotential}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Hook Section */}
        {hook && (
          <div className="bg-gray-900/50 rounded-xl overflow-hidden">
            <button 
              onClick={() => toggleSection('hook')}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-800/50 transition-colors"
            >
              <div className="flex items-center gap-2">
                <SparklesIcon className="w-5 h-5 text-yellow-400" />
                <span className="font-medium text-white">Hook</span>
                <span className="text-xs text-gray-500 px-2 py-0.5 bg-gray-800 rounded-full">
                  {hook.type}
                </span>
              </div>
              {expandedSections.hook ? (
                <ChevronUpIcon className="w-5 h-5 text-gray-400" />
              ) : (
                <ChevronDownIcon className="w-5 h-5 text-gray-400" />
              )}
            </button>
            
            {expandedSections.hook && (
              <div className="px-4 pb-4 space-y-3">
                <div className="bg-gray-800/50 rounded-lg p-4">
                  <p className="text-white text-lg leading-relaxed">{hook.text}</p>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <span className="text-sm text-gray-400">
                      Target emotion: <span className="text-purple-400">{hook.targetEmotion}</span>
                    </span>
                    {hook.expectedRetention && (
                      <span className="text-sm text-gray-400">
                        Expected retention: <span className="text-green-400">{hook.expectedRetention}%</span>
                      </span>
                    )}
                  </div>
                  <button
                    onClick={() => onCopy(hook.text, `hook-${dayNumber}`)}
                    className="flex items-center gap-1 text-sm text-gray-400 hover:text-white transition-colors"
                  >
                    {copied === `hook-${dayNumber}` ? (
                      <>
                        <CheckIcon className="w-4 h-4 text-green-400" />
                        <span className="text-green-400">Copied!</span>
                      </>
                    ) : (
                      <>
                        <DocumentDuplicateIcon className="w-4 h-4" />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Caption Section */}
        {caption && (
          <div className="bg-gray-900/50 rounded-xl overflow-hidden">
            <button 
              onClick={() => toggleSection('caption')}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-800/50 transition-colors"
            >
              <div className="flex items-center gap-2">
                <ChatBubbleBottomCenterTextIcon className="w-5 h-5 text-blue-400" />
                <span className="font-medium text-white">Caption</span>
                <span className="text-xs text-gray-500 px-2 py-0.5 bg-gray-800 rounded-full">
                  {charCount} chars
                </span>
                {caption.emojiUsage && (
                  <span className="text-xs text-gray-500 px-2 py-0.5 bg-gray-800 rounded-full">
                    {caption.emojiUsage.count} emoji
                  </span>
                )}
              </div>
              {expandedSections.caption ? (
                <ChevronUpIcon className="w-5 h-5 text-gray-400" />
              ) : (
                <ChevronDownIcon className="w-5 h-5 text-gray-400" />
              )}
            </button>
            
            {expandedSections.caption && (
              <div className="px-4 pb-4 space-y-3">
                {/* Full Caption Text - New Format */}
                {fullCaptionText && (
                  <div className="bg-gray-800/50 rounded-lg p-4">
                    <span className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Full Caption</span>
                    <p className="text-white whitespace-pre-line">{fullCaptionText}</p>
                  </div>
                )}
                
                {/* Structured Caption - Old Format */}
                {!fullCaptionText && caption.hook && (
                  <div className="bg-gray-800/50 rounded-lg p-4 space-y-3">
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wider block">Hook</span>
                      <p className="text-white mt-1">{caption.hook}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wider block">Body</span>
                      <p className="text-gray-300 mt-1 whitespace-pre-line">{caption.body}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wider block">Call to Action</span>
                      <p className="text-purple-400 mt-1">{caption.callToAction}</p>
                    </div>
                  </div>
                )}
                
                {/* CTA Details - New Format */}
                {caption.cta && typeof caption.cta === 'object' && (
                  <div className="flex items-center gap-4 text-sm">
                    <span className="text-gray-400">
                      CTA: <span className="text-purple-400">{caption.cta.text}</span>
                    </span>
                    <span className="text-gray-500">
                      Type: {caption.cta.type}
                    </span>
                  </div>
                )}
                
                {/* Emoji Usage - New Format */}
                {caption.emojiUsage && caption.emojiUsage.emojis && caption.emojiUsage.emojis.length > 0 && (
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-500">Suggested emojis:</span>
                    <span className="text-lg">{caption.emojiUsage.emojis.join(' ')}</span>
                  </div>
                )}
                
                <div className="flex justify-end">
                  <button
                    onClick={() => onCopy(fullCaptionText || caption.fullCaption || '', `caption-${dayNumber}`)}
                    className="flex items-center gap-1 text-sm text-gray-400 hover:text-white transition-colors"
                  >
                    {copied === `caption-${dayNumber}` ? (
                      <>
                        <CheckIcon className="w-4 h-4 text-green-400" />
                        <span className="text-green-400">Copied!</span>
                      </>
                    ) : (
                      <>
                        <DocumentDuplicateIcon className="w-4 h-4" />
                        <span>Copy Full Caption</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Hashtags Section */}
        {hashtags && (
          <div className="bg-gray-900/50 rounded-xl overflow-hidden">
            <button 
              onClick={() => toggleSection('hashtags')}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-800/50 transition-colors"
            >
              <div className="flex items-center gap-2">
                <HashtagIcon className="w-5 h-5 text-green-400" />
                <span className="font-medium text-white">Hashtags</span>
                <span className="text-xs text-gray-500 px-2 py-0.5 bg-gray-800 rounded-full">
                  {hashtags.total || 15} tags
                </span>
                {hashtags.rotationSet && (
                  <span className="text-xs text-purple-400 px-2 py-0.5 bg-purple-500/10 rounded-full">
                    {hashtags.rotationSet}
                  </span>
                )}
              </div>
              {expandedSections.hashtags ? (
                <ChevronUpIcon className="w-5 h-5 text-gray-400" />
              ) : (
                <ChevronDownIcon className="w-5 h-5 text-gray-400" />
              )}
            </button>
            
            {expandedSections.hashtags && (
              <div className="px-4 pb-4 space-y-3">
                {/* Primary Hashtags */}
                {getHashtagTags(hashtags, 'primary').length > 0 && (
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs text-gray-500 uppercase tracking-wider">Primary (High Reach)</span>
                      {hashtags.primary && typeof hashtags.primary === 'object' && 'avgReach' in hashtags.primary && (
                        <span className="text-xs text-green-400">~{hashtags.primary.avgReach}</span>
                      )}
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {getHashtagTags(hashtags, 'primary').map((tag, idx) => (
                        <span 
                          key={idx}
                          className="px-2 py-1 bg-blue-500/20 text-blue-300 rounded text-sm cursor-pointer hover:bg-blue-500/30 transition-colors"
                          onClick={() => onCopy(tag, `tag-${dayNumber}-p-${idx}`)}
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Niche Hashtags */}
                {getHashtagTags(hashtags, 'niche').length > 0 && (
                  <div>
                    <span className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Niche</span>
                    <div className="flex flex-wrap gap-2">
                      {getHashtagTags(hashtags, 'niche').map((tag, idx) => (
                        <span 
                          key={idx}
                          className="px-2 py-1 bg-purple-500/20 text-purple-300 rounded text-sm cursor-pointer hover:bg-purple-500/30 transition-colors"
                          onClick={() => onCopy(tag, `tag-${dayNumber}-n-${idx}`)}
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Trending Hashtags */}
                {getHashtagTags(hashtags, 'trending').length > 0 && (
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs text-gray-500 uppercase tracking-wider">Trending</span>
                      {hashtags.trending && typeof hashtags.trending === 'object' && 'trendingUntil' in hashtags.trending && (
                        <span className="text-xs text-orange-400">until {hashtags.trending.trendingUntil}</span>
                      )}
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {getHashtagTags(hashtags, 'trending').map((tag, idx) => (
                        <span 
                          key={idx}
                          className="px-2 py-1 bg-orange-500/20 text-orange-300 rounded text-sm cursor-pointer hover:bg-orange-500/30 transition-colors"
                          onClick={() => onCopy(tag, `tag-${dayNumber}-t-${idx}`)}
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Branded & Secondary */}
                {(hashtags.branded?.length > 0 || getHashtagTags(hashtags, 'secondary').length > 0) && (
                  <div>
                    <span className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Branded / Other</span>
                    <div className="flex flex-wrap gap-2">
                      {[...hashtags.branded || [], ...getHashtagTags(hashtags, 'secondary')].map((tag, idx) => (
                        <span 
                          key={idx}
                          className="px-2 py-1 bg-gray-800 text-gray-300 rounded text-sm cursor-pointer hover:bg-gray-700 transition-colors"
                          onClick={() => onCopy(tag, `tag-${dayNumber}-b-${idx}`)}
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                <div className="flex justify-end">
                  <button
                    onClick={() => onCopy(getAllHashtags(hashtags), `all-hashtags-${dayNumber}`)}
                    className="flex items-center gap-1 text-sm text-gray-400 hover:text-white transition-colors"
                  >
                    {copied === `all-hashtags-${dayNumber}` ? (
                      <>
                        <CheckIcon className="w-4 h-4 text-green-400" />
                        <span className="text-green-400">Copied!</span>
                      </>
                    ) : (
                      <>
                        <DocumentDuplicateIcon className="w-4 h-4" />
                        <span>Copy All Hashtags</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Visual Guidelines Section */}
        {visual && (
          <div className="bg-gray-900/50 rounded-xl overflow-hidden">
            <button 
              onClick={() => toggleSection('visual')}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-800/50 transition-colors"
            >
              <div className="flex items-center gap-2">
                <PhotoIcon className="w-5 h-5 text-pink-400" />
                <span className="font-medium text-white">Visual Guidelines</span>
              </div>
              {expandedSections.visual ? (
                <ChevronUpIcon className="w-5 h-5 text-gray-400" />
              ) : (
                <ChevronDownIcon className="w-5 h-5 text-gray-400" />
              )}
            </button>
            
            {expandedSections.visual && (
              <div className="px-4 pb-4 space-y-4">
                {/* Color Palette */}
                <div>
                  <span className="text-xs text-gray-500 uppercase tracking-wider block">Color Palette</span>
                  <div className="flex gap-2 mt-2">
                    {Array.isArray(visual.colorPalette) ? (
                      // Old format: array of colors
                      visual.colorPalette.map((color: string, idx: number) => (
                        <div 
                          key={idx}
                          className="w-10 h-10 rounded-lg border border-gray-700 cursor-pointer flex items-center justify-center group relative"
                          style={{ backgroundColor: color }}
                          title={color}
                          onClick={() => onCopy(color, `color-${dayNumber}-${idx}`)}
                        >
                          <span className="hidden group-hover:block absolute -bottom-6 text-xs text-gray-400">{color}</span>
                        </div>
                      ))
                    ) : visual.colorPalette && typeof visual.colorPalette === 'object' ? (
                      // New format: object with primary/secondary/accent
                      (() => {
                        const palette = visual.colorPalette as { primary?: string; secondary?: string; accent?: string; background?: string };
                        return (
                          <>
                            {palette.primary && (
                              <div className="flex flex-col items-center">
                                <div 
                                  className="w-10 h-10 rounded-lg border border-gray-700 cursor-pointer"
                                  style={{ backgroundColor: palette.primary }}
                                  onClick={() => onCopy(palette.primary!, `color-${dayNumber}-primary`)}
                                />
                                <span className="text-xs text-gray-500 mt-1">Primary</span>
                              </div>
                            )}
                            {palette.secondary && (
                              <div className="flex flex-col items-center">
                                <div 
                                  className="w-10 h-10 rounded-lg border border-gray-700 cursor-pointer"
                                  style={{ backgroundColor: palette.secondary }}
                                  onClick={() => onCopy(palette.secondary!, `color-${dayNumber}-secondary`)}
                                />
                                <span className="text-xs text-gray-500 mt-1">Secondary</span>
                              </div>
                            )}
                            {palette.accent && (
                              <div className="flex flex-col items-center">
                                <div 
                                  className="w-10 h-10 rounded-lg border border-gray-700 cursor-pointer"
                                  style={{ backgroundColor: palette.accent }}
                                  onClick={() => onCopy(palette.accent!, `color-${dayNumber}-accent`)}
                                />
                                <span className="text-xs text-gray-500 mt-1">Accent</span>
                              </div>
                            )}
                            {palette.background && (
                              <div className="flex flex-col items-center">
                                <div 
                                  className="w-10 h-10 rounded-lg border border-gray-700 cursor-pointer"
                                  style={{ backgroundColor: palette.background }}
                                  onClick={() => onCopy(palette.background!, `color-${dayNumber}-bg`)}
                                />
                                <span className="text-xs text-gray-500 mt-1">Background</span>
                              </div>
                            )}
                          </>
                        );
                      })()
                    ) : null}
                  </div>
                </div>
                
                {/* Thumbnail Text - New Format */}
                {visual.thumbnailText && (
                  <div>
                    <span className="text-xs text-gray-500 uppercase tracking-wider block">Thumbnail Text</span>
                    <div className="bg-gray-800/50 rounded-lg p-3 mt-2">
                      <p className="text-white font-bold text-lg">
                        {typeof visual.thumbnailText === 'string' 
                          ? visual.thumbnailText 
                          : visual.thumbnailText.text || ''}
                      </p>
                      {typeof visual.thumbnailText === 'object' && visual.thumbnailText.position && (
                        <p className="text-xs text-gray-500 mt-1">Position: {visual.thumbnailText.position}</p>
                      )}
                    </div>
                  </div>
                )}
                
                {/* Style - New Format */}
                {visual.style && typeof visual.style === 'object' && (
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wider block">Style Archetype</span>
                      <p className="text-gray-300 mt-1">{visual.style.archetype}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wider block">Mood</span>
                      <p className="text-gray-300 mt-1">{visual.style.mood}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wider block">Composition</span>
                      <p className="text-gray-300 mt-1">{visual.style.composition}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500 uppercase tracking-wider block">Lighting</span>
                      <p className="text-gray-300 mt-1">{visual.style.lighting}</p>
                    </div>
                  </div>
                )}
                
                {/* Face Presence - New Format */}
                {visual.facePresence && (
                  <div className="bg-gray-800/50 rounded-lg p-3">
                    <span className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Face Presence</span>
                    <div className="flex items-center gap-4">
                      <span className={`px-2 py-1 rounded text-sm ${visual.facePresence.recommended ? 'bg-green-500/20 text-green-400' : 'bg-gray-500/20 text-gray-400'}`}>
                        {visual.facePresence.recommended ? 'Recommended' : 'Optional'}
                      </span>
                      {visual.facePresence.expression && (
                        <span className="text-gray-400 text-sm">
                          Expression: <span className="text-white">{visual.facePresence.expression}</span>
                        </span>
                      )}
                      {visual.facePresence.eyeContact && (
                        <span className="text-gray-400 text-sm">Eye contact: Yes</span>
                      )}
                    </div>
                  </div>
                )}
                
                {/* Old Format Fields */}
                {(visual.layoutStyle || visual.filterPreset) && (
                  <div className="grid grid-cols-2 gap-4">
                    {visual.layoutStyle && (
                      <div>
                        <span className="text-xs text-gray-500 uppercase tracking-wider block">Layout Style</span>
                        <p className="text-gray-300 mt-1">{visual.layoutStyle}</p>
                      </div>
                    )}
                    {visual.filterPreset && (
                      <div>
                        <span className="text-xs text-gray-500 uppercase tracking-wider block">Filter Preset</span>
                        <p className="text-gray-300 mt-1">{visual.filterPreset}</p>
                      </div>
                    )}
                  </div>
                )}

                {visual.visualElements && visual.visualElements.length > 0 && (
                  <div>
                    <span className="text-xs text-gray-500 uppercase tracking-wider block">Visual Elements</span>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {visual.visualElements.map((element: string, idx: number) => (
                        <span key={idx} className="px-3 py-1 bg-gray-800 text-gray-300 rounded-full text-sm">
                          {element}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Daily Stories Section - NEW */}
        {stories && stories.length > 0 && (
          <div className="bg-gray-900/50 rounded-xl overflow-hidden">
            <button 
              onClick={() => toggleSection('stories')}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-800/50 transition-colors"
            >
              <div className="flex items-center gap-2">
                <ClockIcon className="w-5 h-5 text-cyan-400" />
                <span className="font-medium text-white">Daily Stories</span>
                <span className="text-xs text-gray-500 px-2 py-0.5 bg-gray-800 rounded-full">
                  {stories.length} stories
                </span>
              </div>
              {expandedSections.stories ? (
                <ChevronUpIcon className="w-5 h-5 text-gray-400" />
              ) : (
                <ChevronDownIcon className="w-5 h-5 text-gray-400" />
              )}
            </button>
            
            {expandedSections.stories && (
              <div className="px-4 pb-4 space-y-3">
                <div className="grid gap-3">
                  {stories.map((story: any, idx: number) => (
                    <div 
                      key={idx} 
                      className="bg-gray-800/50 rounded-lg p-4 border-l-4"
                      style={{
                        borderLeftColor: story.type === 'Poll' ? '#06b6d4' :
                                         story.type === 'Teaser' ? '#f59e0b' :
                                         story.type === 'Post Share' ? '#8b5cf6' :
                                         story.type === 'Behind Scenes' ? '#ec4899' :
                                         story.type === 'Q&A' ? '#10b981' : '#6b7280'
                      }}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-gray-500 px-2 py-0.5 bg-gray-700 rounded">
                            Slot {story.slot || idx + 1}
                          </span>
                          <span className={`text-xs px-2 py-0.5 rounded font-medium ${
                            story.type === 'Poll' ? 'bg-cyan-500/20 text-cyan-400' :
                            story.type === 'Teaser' ? 'bg-amber-500/20 text-amber-400' :
                            story.type === 'Post Share' ? 'bg-purple-500/20 text-purple-400' :
                            story.type === 'Behind Scenes' ? 'bg-pink-500/20 text-pink-400' :
                            story.type === 'Q&A' ? 'bg-emerald-500/20 text-emerald-400' :
                            'bg-gray-500/20 text-gray-400'
                          }`}>
                            {story.type}
                          </span>
                        </div>
                        <div className="flex items-center gap-1 text-gray-400">
                          <ClockIcon className="w-4 h-4" />
                          <span className="text-sm font-medium">{story.time}</span>
                        </div>
                      </div>
                      
                      <p className="text-white text-sm mb-2">{story.content}</p>
                      
                      <div className="flex flex-wrap gap-2 text-xs">
                        {story.sticker && (
                          <span className="text-gray-400">
                            Sticker: <span className="text-purple-400">{story.sticker}</span>
                          </span>
                        )}
                        {story.options && story.options.length > 0 && (
                          <span className="text-gray-400">
                            Options: <span className="text-cyan-400">{story.options.join(' vs ')}</span>
                          </span>
                        )}
                        {story.engagementCTA && (
                          <span className="text-gray-400">
                            CTA: <span className="text-green-400">{story.engagementCTA}</span>
                          </span>
                        )}
                        {story.purpose && (
                          <span className="text-gray-500">
                            • {story.purpose.replace(/_/g, ' ')}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Expected Engagement */}
        {engagement && (
          <div className="bg-gray-900/50 rounded-xl p-4">
            <span className="text-xs text-gray-500 uppercase tracking-wider mb-3 block">Expected Engagement</span>
            <div className="grid grid-cols-5 gap-3">
              <div className="text-center">
                <HeartIcon className="w-5 h-5 text-red-400 mx-auto mb-1" />
                <p className="text-white font-semibold">{engagement.likes}</p>
                <p className="text-xs text-gray-500">Likes</p>
              </div>
              <div className="text-center">
                <ChatBubbleBottomCenterTextIcon className="w-5 h-5 text-blue-400 mx-auto mb-1" />
                <p className="text-white font-semibold">{engagement.comments}</p>
                <p className="text-xs text-gray-500">Comments</p>
              </div>
              <div className="text-center">
                <BookmarkIcon className="w-5 h-5 text-yellow-400 mx-auto mb-1" />
                <p className="text-white font-semibold">{engagement.saves}</p>
                <p className="text-xs text-gray-500">Saves</p>
              </div>
              <div className="text-center">
                <ShareIcon className="w-5 h-5 text-green-400 mx-auto mb-1" />
                <p className="text-white font-semibold">{engagement.shares}</p>
                <p className="text-xs text-gray-500">Shares</p>
              </div>
              {engagement.reach && (
                <div className="text-center">
                  <EyeIcon className="w-5 h-5 text-purple-400 mx-auto mb-1" />
                  <p className="text-white font-semibold">{engagement.reach}</p>
                  <p className="text-xs text-gray-500">Reach</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Daily Goals & Tasks - Legacy Support */}
        {((day.dailyGoals?.length ?? 0) > 0 || (day.engagementTasks?.length ?? 0) > 0) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {day.dailyGoals && day.dailyGoals.length > 0 && (
              <div className="bg-gray-900/50 rounded-xl p-4">
                <span className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Daily Goals</span>
                <ul className="space-y-2">
                  {day.dailyGoals.map((goal, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-gray-300 text-sm">
                      <input 
                        type="checkbox" 
                        id={`daily-goal-${dayNumber}-${idx}`}
                        name={`daily-goal-${dayNumber}-${idx}`}
                        autoComplete="off"
                        className="mt-0.5 rounded border-gray-600 bg-gray-800 text-purple-500 focus:ring-purple-500"
                      />
                      <label htmlFor={`daily-goal-${dayNumber}-${idx}`}>{goal}</label>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {day.engagementTasks && day.engagementTasks.length > 0 && (
              <div className="bg-gray-900/50 rounded-xl p-4">
                <span className="text-xs text-gray-500 uppercase tracking-wider mb-2 block">Engagement Tasks</span>
                <ul className="space-y-2">
                  {day.engagementTasks.map((task, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-gray-300 text-sm">
                      <input 
                        type="checkbox" 
                        id={`engagement-task-${dayNumber}-${idx}`}
                        name={`engagement-task-${dayNumber}-${idx}`}
                        autoComplete="off"
                        className="mt-0.5 rounded border-gray-600 bg-gray-800 text-purple-500 focus:ring-purple-500"
                      />
                      <label htmlFor={`engagement-task-${dayNumber}-${idx}`}>{task}</label>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default DayPlanCard;
