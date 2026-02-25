'use client';

import React, { useState } from 'react';
import { VideoIcon, CopyIcon, CheckCircleIcon, ChevronDownIcon, ChevronUpIcon } from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';

/**
 * 🎬 GÖREV 2: TELEPROMPTER KART TASARIMI
 * 
 * Bu component "Senaryo" formatındaki önerileri özel bir kart olarak gösterir:
 * - Terminal/kod havası
 * - Monospace font
 * - KOPYALA butonu
 */

interface ReelsScenario {
  title?: string;
  duration?: string;
  sections?: Array<{
    name: string;
    instruction?: string;
    overlay_text?: string;
    script?: string;
    audio?: string;
    visual_tip?: string;
  }>;
  pro_tips?: string[];
}

interface ReelsScenarioCardProps {
  scenario: ReelsScenario;
  compact?: boolean;
}

export const ReelsScenarioCard: React.FC<ReelsScenarioCardProps> = ({ 
  scenario, 
  compact = false 
}) => {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(!compact);
  const { locale } = useTranslation();

  if (!scenario || !scenario.sections || scenario.sections.length === 0) {
    return null;
  }

  const handleCopy = () => {
    // Senaryoyu kopyalanabilir metne çevir
    let text = `${scenario.title || 'Reels Senaryosu'}\n`;
    text += `Süre: ${scenario.duration || '15-30 saniye'}\n\n`;
    
    scenario.sections?.forEach((section, idx) => {
      text += `${idx + 1}. ${section.name}\n`;
      if (section.instruction) text += `   📝 ${section.instruction}\n`;
      if (section.overlay_text) text += `   💬 Metin: ${section.overlay_text}\n`;
      if (section.script) text += `   🎙️ Konuşma: ${section.script}\n`;
      if (section.audio) text += `   🎵 Ses: ${section.audio}\n`;
      if (section.visual_tip) text += `   💡 İpucu: ${section.visual_tip}\n`;
      text += '\n';
    });

    if (scenario.pro_tips && scenario.pro_tips.length > 0) {
      text += '\n✨ PRO İPUÇLARI:\n';
      scenario.pro_tips.forEach((tip, idx) => {
        text += `  ${idx + 1}. ${tip}\n`;
      });
    }

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-2xl border border-slate-700 bg-gradient-to-br from-slate-900 to-slate-800 shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-slate-800 border-b border-slate-700 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-purple-600">
            <VideoIcon className="text-white" size={16} />
          </div>
          <div>
            <p className="text-sm font-semibold text-white">
              {scenario.title || 'Reels Senaryosu'}
            </p>
            {scenario.duration && (
              <p className="text-xs text-slate-400">
                ⏱️ {scenario.duration}
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-2 px-3 py-1.5 bg-purple-600 hover:bg-purple-700 text-white text-sm rounded-lg transition-colors"
          >
            {copied ? (
              <>
                <CheckCircleIcon size={16} />
                <span>{locale === 'tr' ? 'Kopyalandı!' : 'Copied!'}</span>
              </>
            ) : (
              <>
                <CopyIcon size={16} />
                <span>{locale === 'tr' ? 'Kopyala' : 'Copy'}</span>
              </>
            )}
          </button>
          {compact && (
            <button
              onClick={() => setExpanded(!expanded)}
              className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
            >
              {expanded ? (
                <ChevronUpIcon className="text-slate-400" size={16} />
              ) : (
                <ChevronDownIcon className="text-slate-400" size={16} />
              )}
            </button>
          )}
        </div>
      </div>

      {/* Content */}
      {expanded && (
        <div className="p-4 space-y-4 font-mono text-sm">
          {/* Sections */}
          {scenario.sections.map((section, idx) => (
            <div key={idx} className="space-y-2">
              {/* Section Header */}
              <div className="flex items-center gap-2">
                <span className="flex h-6 w-6 items-center justify-center rounded bg-purple-600 text-white text-xs font-bold">
                  {idx + 1}
                </span>
                <span className="text-yellow-400 font-bold">{section.name}</span>
              </div>

              {/* Section Details */}
              <div className="ml-8 space-y-1.5">
                {section.instruction && (
                  <div className="flex items-start gap-2">
                    <span className="text-slate-500">📝</span>
                    <span className="text-slate-300">{section.instruction}</span>
                  </div>
                )}
                
                {section.overlay_text && (
                  <div className="flex items-start gap-2">
                    <span className="text-slate-500">💬</span>
                    <span className="text-green-400">&quot;{section.overlay_text}&quot;</span>
                  </div>
                )}
                
                {section.script && (
                  <div className="flex items-start gap-2">
                    <span className="text-slate-500">🎙️</span>
                    <span className="text-blue-400">{section.script}</span>
                  </div>
                )}
                
                {section.audio && (
                  <div className="flex items-start gap-2">
                    <span className="text-slate-500">🎵</span>
                    <span className="text-purple-400">{section.audio}</span>
                  </div>
                )}
                
                {section.visual_tip && (
                  <div className="flex items-start gap-2">
                    <span className="text-slate-500">💡</span>
                    <span className="text-orange-400 italic">{section.visual_tip}</span>
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Pro Tips */}
          {scenario.pro_tips && scenario.pro_tips.length > 0 && (
            <div className="mt-4 pt-4 border-t border-slate-700">
              <p className="text-yellow-400 font-bold mb-2">✨ PRO İPUÇLARI</p>
              <ul className="ml-4 space-y-1.5 text-slate-300">
                {scenario.pro_tips.map((tip, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-slate-500">{idx + 1}.</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
