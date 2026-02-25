"use client";

import { useState, useCallback, useEffect } from 'react';
import { 
  FileTextIcon, 
  ChevronDownIcon, 
  ChevronUpIcon,
  CheckCircleIcon,
  XCircleIcon,
  DownloadCloudIcon,
  LoaderIcon,
  SettingsIcon,
  BarChart3Icon,
  TargetIcon,
  TrendingUpIcon,
  DollarSignIcon,
  ShieldIcon,
  CalendarIcon,
  LightbulbIcon,
  AlertTriangleIcon,
  UsersIcon,
  PaletteIcon,
  HeartIcon,
  EyeIcon,
  SparkIcon,
} from '@/components/icons';
import { useTranslation } from '@/i18n/TranslationProvider';
import api from '@/lib/api';
import toast from 'react-hot-toast';

interface PdfSection {
  id: string;
  nameKey: string;
  descriptionKey: string;
  icon: React.ReactNode;
  category: 'core' | 'agents' | 'advanced' | 'extras';
  defaultEnabled: boolean;
  requiresTier?: 'standard' | 'premium';
}

const pdfSections: PdfSection[] = [
  // Core Sections
  {
    id: 'coverPage',
    nameKey: 'Kapak Sayfası',
    descriptionKey: 'Profil bilgileri ve genel skor',
    icon: <FileTextIcon size={18} />,
    category: 'core',
    defaultEnabled: true,
  },
  {
    id: 'executiveSummary',
    nameKey: 'Yönetici Özeti',
    descriptionKey: 'Hesap özeti ve kritik bulgular',
    icon: <TargetIcon size={18} />,
    category: 'core',
    defaultEnabled: true,
  },
  {
    id: 'scoreExplainer',
    nameKey: 'Skor Açıklaması',
    descriptionKey: 'Puan detayları ve karşılaştırma',
    icon: <BarChart3Icon size={18} />,
    category: 'core',
    defaultEnabled: true,
  },
  {
    id: 'businessIdentity',
    nameKey: 'İş Kimliği',
    descriptionKey: 'Hesap türü ve metrik önerileri',
    icon: <UsersIcon size={18} />,
    category: 'core',
    defaultEnabled: true,
  },
  
  // Agent Results
  {
    id: 'domainMaster',
    nameKey: 'Sektör Analizi',
    descriptionKey: 'Niş ve rekabet değerlendirmesi',
    icon: <TargetIcon size={18} className="text-purple-500" />,
    category: 'agents',
    defaultEnabled: true,
  },
  {
    id: 'growthVirality',
    nameKey: 'Büyüme Analizi',
    descriptionKey: 'Büyüme potansiyeli ve viral içerik',
    icon: <TrendingUpIcon size={18} className="text-green-500" />,
    category: 'agents',
    defaultEnabled: true,
  },
  {
    id: 'salesConversion',
    nameKey: 'Monetizasyon',
    descriptionKey: 'Gelir potansiyeli ve satış',
    icon: <DollarSignIcon size={18} className="text-amber-500" />,
    category: 'agents',
    defaultEnabled: true,
    requiresTier: 'standard',
  },
  {
    id: 'visualBrand',
    nameKey: 'Görsel Marka',
    descriptionKey: 'Görsel tutarlılık analizi',
    icon: <PaletteIcon size={18} className="text-pink-500" />,
    category: 'agents',
    defaultEnabled: true,
  },
  {
    id: 'communityLoyalty',
    nameKey: 'Topluluk Sadakati',
    descriptionKey: 'Takipçi etkileşimi ve bağlılık',
    icon: <HeartIcon size={18} className="text-red-500" />,
    category: 'agents',
    defaultEnabled: true,
  },
  {
    id: 'attentionArchitect',
    nameKey: 'Dikkat Mimarisi',
    descriptionKey: 'Hook ve içerik yapısı analizi',
    icon: <EyeIcon size={18} className="text-blue-500" />,
    category: 'agents',
    defaultEnabled: true,
  },
  {
    id: 'systemGovernor',
    nameKey: 'Sistem Denetimi',
    descriptionKey: 'Risk ve güvenlik analizi',
    icon: <ShieldIcon size={18} className="text-slate-500" />,
    category: 'agents',
    defaultEnabled: true,
  },
  
  // Advanced Sections
  {
    id: 'swotAnalysis',
    nameKey: 'SWOT Analizi',
    descriptionKey: 'Güçlü/zayıf yönler ve fırsatlar',
    icon: <AlertTriangleIcon size={18} className="text-indigo-500" />,
    category: 'advanced',
    defaultEnabled: true,
    requiresTier: 'standard',
  },
  {
    id: 'riskAssessment',
    nameKey: 'Risk Değerlendirmesi',
    descriptionKey: 'Bot, shadowban ve algoritma riskleri',
    icon: <ShieldIcon size={18} className="text-red-500" />,
    category: 'advanced',
    defaultEnabled: true,
  },
  {
    id: 'contentStrategy',
    nameKey: 'İçerik Stratejisi',
    descriptionKey: 'Format analizi ve hashtag stratejisi',
    icon: <BarChart3Icon size={18} className="text-purple-500" />,
    category: 'advanced',
    defaultEnabled: true,
    requiresTier: 'standard',
  },
  {
    id: 'actionPlan',
    nameKey: 'Aksiyon Planı',
    descriptionKey: 'Önceliklendirilmiş öneriler',
    icon: <TargetIcon size={18} className="text-green-500" />,
    category: 'advanced',
    defaultEnabled: true,
  },
  {
    id: 'benchmarks',
    nameKey: 'Kıyaslama',
    descriptionKey: 'Sektör ortalamaları ile karşılaştırma',
    icon: <BarChart3Icon size={18} className="text-blue-500" />,
    category: 'advanced',
    defaultEnabled: true,
    requiresTier: 'premium',
  },
  
  // Extras
  {
    id: 'eli5Report',
    nameKey: 'Detaylı Açıklamalar',
    descriptionKey: 'Anlaşılır metrik yorumları',
    icon: <LightbulbIcon size={18} className="text-amber-500" />,
    category: 'extras',
    defaultEnabled: true,
  },
  {
    id: 'hookRewrites',
    nameKey: 'Hook İyileştirmeleri',
    descriptionKey: 'İçerik başlığı önerileri',
    icon: <SparkIcon size={18} className="text-orange-500" />,
    category: 'extras',
    defaultEnabled: true,
    requiresTier: 'standard',
  },
  {
    id: 'contentCalendar',
    nameKey: 'İçerik Planı',
    descriptionKey: '7 günlük içerik takvimi',
    icon: <CalendarIcon size={18} className="text-green-500" />,
    category: 'extras',
    defaultEnabled: true,
    requiresTier: 'premium',
  },
  {
    id: 'finalVerdict',
    nameKey: 'Final Analiz',
    descriptionKey: 'Kapsamlı son değerlendirme',
    icon: <TargetIcon size={18} className="text-indigo-500" />,
    category: 'extras',
    defaultEnabled: true,
  },
  {
    id: 'glossary',
    nameKey: 'Terimler Sözlüğü',
    descriptionKey: 'Jargon açıklamaları',
    icon: <FileTextIcon size={18} className="text-slate-500" />,
    category: 'extras',
    defaultEnabled: false,
  },
];

interface PdfCustomizerProps {
  analysisId: string;
  userTier: 'STARTER' | 'PROFESSIONAL' | 'PREMIUM' | 'ENTERPRISE';
  onClose?: () => void;
}

interface PdfJobState {
  reportId: string;
  progress: number;
  status: 'idle' | 'starting' | 'processing' | 'done' | 'error';
  startedAt: number;
  pdfUrl?: string | null;
}

export function PdfCustomizer({ analysisId, userTier, onClose }: PdfCustomizerProps) {
  const { locale } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(false);
  const [pdfJob, setPdfJob] = useState<PdfJobState>({
    reportId: '',
    progress: 0,
    status: 'idle',
    startedAt: 0,
    pdfUrl: null,
  });
  const isGenerating = pdfJob.status === 'starting' || pdfJob.status === 'processing';
  
  // Map tier to simplified levels for access control
  const getTierLevel = (tier: string): 'basic' | 'standard' | 'premium' => {
    if (tier === 'PREMIUM' || tier === 'ENTERPRISE') return 'premium';
    if (tier === 'PROFESSIONAL') return 'standard';
    return 'basic';
  };
  const tierLevel = getTierLevel(userTier);
  
  const [selectedSections, setSelectedSections] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    pdfSections.forEach(section => {
      // Check tier requirements
      const tierAllowed = !section.requiresTier || 
        (section.requiresTier === 'standard' && (tierLevel === 'standard' || tierLevel === 'premium')) ||
        (section.requiresTier === 'premium' && tierLevel === 'premium');
      initial[section.id] = section.defaultEnabled && tierAllowed;
    });
    return initial;
  });

  const labels = {
    title: locale === 'tr' ? 'PDF Rapor Oluşturucu' : 'PDF Report Builder',
    subtitle: locale === 'tr' ? 'Raporunuza dahil edilecek bölümleri seçin' : 'Select sections to include in your report',
    coreTitle: locale === 'tr' ? 'Temel Bölümler' : 'Core Sections',
    agentsTitle: locale === 'tr' ? 'Ajan Analizleri' : 'Agent Analysis',
    advancedTitle: locale === 'tr' ? 'Gelişmiş Analizler' : 'Advanced Analysis',
    extrasTitle: locale === 'tr' ? 'Ek Bölümler' : 'Extra Sections',
    selectAll: locale === 'tr' ? 'Tümünü Seç' : 'Select All',
    deselectAll: locale === 'tr' ? 'Tümünü Kaldır' : 'Deselect All',
    generatePdf: locale === 'tr' ? 'PDF Oluştur' : 'Generate PDF',
    generating: locale === 'tr' ? 'Oluşturuluyor...' : 'Generating...',
    selectedCount: locale === 'tr' ? 'seçili bölüm' : 'sections selected',
    requiresPremium: locale === 'tr' ? 'Premium gerekli' : 'Premium required',
    requiresStandard: locale === 'tr' ? 'Standard gerekli' : 'Standard required',
    customize: locale === 'tr' ? 'Özelleştir' : 'Customize',
    quickExport: locale === 'tr' ? 'Hızlı Dışa Aktar' : 'Quick Export',
    processingPdf: locale === 'tr' ? 'PDF işleniyor' : 'Processing PDF',
    openPdf: locale === 'tr' ? 'PDF Aç' : 'Open PDF',
  };

  useEffect(() => {
    if (!pdfJob.reportId || !isGenerating) return;

    const interval = setInterval(async () => {
      try {
        const elapsedSec = (Date.now() - pdfJob.startedAt) / 1000;
        const syntheticProgress = Math.min(95, Math.max(8, Math.round(8 + elapsedSec * 2.2)));

        setPdfJob((prev) => {
          if (!prev.reportId || prev.status === 'done' || prev.status === 'error') return prev;
          return {
            ...prev,
            status: 'processing',
            progress: Math.max(prev.progress, syntheticProgress),
          };
        });

        const response = await api.get(`/reports/${pdfJob.reportId}`);
        const report = response?.data?.data;

        if (report?.pdfUrl) {
          setPdfJob((prev) => ({
            ...prev,
            status: 'done',
            progress: 100,
            pdfUrl: report.pdfUrl,
          }));
          toast.success(locale === 'tr' ? 'PDF hazır' : 'PDF is ready');
        }
      } catch {
        // Polling hatasında süreci kesmeden devam et
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [pdfJob.reportId, pdfJob.startedAt, isGenerating, locale]);

  const startPdfJob = (reportId: string) => {
    setPdfJob({
      reportId,
      progress: 8,
      status: 'starting',
      startedAt: Date.now(),
      pdfUrl: null,
    });
  };

  const isTierAllowed = (section: PdfSection): boolean => {
    if (!section.requiresTier) return true;
    if (section.requiresTier === 'standard') {
      return tierLevel === 'standard' || tierLevel === 'premium';
    }
    if (section.requiresTier === 'premium') {
      return tierLevel === 'premium';
    }
    return true;
  };

  const toggleSection = useCallback((sectionId: string) => {
    setSelectedSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId],
    }));
  }, []);

  const selectAllInCategory = useCallback((category: string) => {
    setSelectedSections(prev => {
      const updated = { ...prev };
      pdfSections
        .filter(s => s.category === category && isTierAllowed(s))
        .forEach(s => { updated[s.id] = true; });
      return updated;
    });
  }, [tierLevel]);

  const deselectAllInCategory = useCallback((category: string) => {
    setSelectedSections(prev => {
      const updated = { ...prev };
      pdfSections
        .filter(s => s.category === category)
        .forEach(s => { updated[s.id] = false; });
      return updated;
    });
  }, []);

  const selectedCount = Object.values(selectedSections).filter(Boolean).length;

  const handleGeneratePdf = async () => {
    const enabledSections = Object.entries(selectedSections)
      .filter(([_, enabled]) => enabled)
      .map(([id]) => id);

    if (enabledSections.length === 0) {
      toast.error(locale === 'tr' ? 'En az bir bölüm seçmelisiniz' : 'Select at least one section');
      return;
    }

    setPdfJob((prev) => ({
      ...prev,
      status: 'starting',
      progress: Math.max(prev.progress, 5),
      startedAt: Date.now(),
      pdfUrl: null,
    }));
    try {
      const response = await api.post('/reports/generate-custom', {
        analysisId,
        sections: enabledSections,
      });

      if (response.data.success) {
        toast.success(locale === 'tr' ? 'PDF oluşturma başlatıldı' : 'PDF generation started');
        const reportId = response?.data?.data?.reportId;
        if (reportId) {
          startPdfJob(reportId);
        }
        onClose?.();
      }
    } catch (error: any) {
      setPdfJob((prev) => ({ ...prev, status: 'error' }));
      toast.error(error?.response?.data?.message || (locale === 'tr' ? 'PDF oluşturulamadı' : 'Failed to generate PDF'));
    }
  };

  const handleQuickExport = async () => {
    setPdfJob((prev) => ({
      ...prev,
      status: 'starting',
      progress: Math.max(prev.progress, 5),
      startedAt: Date.now(),
      pdfUrl: null,
    }));
    try {
      const response = await api.post('/reports/generate', { analysisId });
      if (response.data.success) {
        toast.success(locale === 'tr' ? 'PDF oluşturma başlatıldı' : 'PDF generation started');
        const reportId = response?.data?.data?.reportId;
        if (reportId) {
          startPdfJob(reportId);
        }
      }
    } catch (error: any) {
      setPdfJob((prev) => ({ ...prev, status: 'error' }));
      toast.error(error?.response?.data?.message || (locale === 'tr' ? 'PDF oluşturulamadı' : 'Failed to generate PDF'));
    }
  };

  const renderCategory = (category: 'core' | 'agents' | 'advanced' | 'extras', title: string) => {
    const categorySections = pdfSections.filter(s => s.category === category);
    const selectedInCategory = categorySections.filter(s => selectedSections[s.id]).length;

    return (
      <div className="mb-6">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-semibold text-slate-700">{title}</h4>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">
              {selectedInCategory}/{categorySections.length}
            </span>
            <button
              onClick={() => selectAllInCategory(category)}
              className="text-xs text-primary-600 hover:text-primary-700"
            >
              {labels.selectAll}
            </button>
            <span className="text-slate-300">|</span>
            <button
              onClick={() => deselectAllInCategory(category)}
              className="text-xs text-slate-500 hover:text-slate-700"
            >
              {labels.deselectAll}
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {categorySections.map(section => {
            const tierAllowed = isTierAllowed(section);
            const isSelected = selectedSections[section.id];

            return (
              <button
                key={section.id}
                onClick={() => tierAllowed && toggleSection(section.id)}
                disabled={!tierAllowed}
                className={`
                  flex items-start gap-3 p-3 rounded-xl border text-left transition-all
                  ${isSelected && tierAllowed
                    ? 'border-primary-300 bg-primary-50 ring-1 ring-primary-200'
                    : tierAllowed
                      ? 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50'
                      : 'border-slate-100 bg-slate-50 opacity-50 cursor-not-allowed'
                  }
                `}
              >
                <div className={`
                  flex-shrink-0 p-2 rounded-lg
                  ${isSelected && tierAllowed ? 'bg-primary-100' : 'bg-slate-100'}
                `}>
                  {section.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`text-sm font-medium ${tierAllowed ? 'text-slate-900' : 'text-slate-400'}`}>
                      {section.nameKey}
                    </span>
                    {section.requiresTier && !tierAllowed && (
                      <span className="text-xs px-1.5 py-0.5 rounded bg-amber-100 text-amber-700">
                        {section.requiresTier === 'premium' ? labels.requiresPremium : labels.requiresStandard}
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-500 truncate">{section.descriptionKey}</p>
                </div>
                <div className="flex-shrink-0">
                  {isSelected && tierAllowed ? (
                    <CheckCircleIcon size={20} className="text-primary-600" />
                  ) : (
                    <div className={`w-5 h-5 rounded-full border-2 ${tierAllowed ? 'border-slate-300' : 'border-slate-200'}`} />
                  )}
                </div>
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="relative">
      {/* Compact Trigger Buttons - Always Visible */}
      <div className="flex items-center gap-2">
        {/* Quick Export Button */}
        {isGenerating ? (
          <div className="w-52 rounded-2xl border border-slate-200 bg-white px-3 py-2 shadow-sm">
            <div className="mb-1 flex items-center justify-between text-[11px] text-slate-600">
              <span>{labels.processingPdf}</span>
              <span className="font-semibold text-primary-700">{pdfJob.progress}%</span>
            </div>
            <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-gradient-to-r from-primary-500 to-indigo-600 transition-all duration-500"
                style={{ width: `${pdfJob.progress}%` }}
              />
            </div>
          </div>
        ) : pdfJob.status === 'done' && pdfJob.pdfUrl ? (
          <button
            onClick={() => window.open(pdfJob.pdfUrl || '', '_blank', 'noopener,noreferrer')}
            className="flex items-center gap-2 px-4 py-3 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-700 hover:bg-emerald-100 transition-colors text-sm font-semibold shadow-sm"
          >
            <CheckCircleIcon size={16} />
            {labels.openPdf}
          </button>
        ) : (
          <button
            onClick={handleQuickExport}
            disabled={isGenerating}
            className="flex items-center gap-2 px-4 py-3 rounded-2xl bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition-colors text-sm font-semibold shadow-sm"
          >
            <DownloadCloudIcon size={16} />
            {locale === 'tr' ? 'PDF' : 'PDF'}
          </button>
        )}
        
        {/* Customize Button */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-2 px-3 py-3 rounded-2xl bg-indigo-600 text-white hover:bg-indigo-700 transition-colors text-sm font-semibold shadow-sm"
          title={labels.customize}
        >
          <SettingsIcon size={16} />
          {isExpanded ? <ChevronUpIcon size={14} /> : <ChevronDownIcon size={14} />}
        </button>
      </div>

      {/* Expandable Dropdown Panel */}
      {isExpanded && (
        <div className="absolute right-0 top-full mt-2 w-[600px] max-h-[70vh] overflow-y-auto rounded-2xl border border-slate-200 bg-white shadow-xl z-50">
          {/* Header */}
          <div className="sticky top-0 px-5 py-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-slate-200">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-indigo-100">
                <FileTextIcon size={20} className="text-indigo-600" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">{labels.title}</h3>
                <p className="text-xs text-slate-500">{labels.subtitle}</p>
              </div>
            </div>
          </div>

          {/* Section Selection */}
          <div className="p-5">
            {renderCategory('core', labels.coreTitle)}
            {renderCategory('agents', labels.agentsTitle)}
            {renderCategory('advanced', labels.advancedTitle)}
            {renderCategory('extras', labels.extrasTitle)}
          </div>

          {/* Footer Actions */}
          <div className="sticky bottom-0 flex items-center justify-between px-5 py-4 bg-white border-t border-slate-200">
            <div className="text-sm text-slate-500">
              <span className="font-semibold text-slate-900">{selectedCount}</span> {labels.selectedCount}
            </div>
            
            <button
              onClick={handleGeneratePdf}
              disabled={isGenerating || selectedCount === 0}
              className={`
                flex items-center gap-2 px-5 py-2.5 rounded-xl text-white font-semibold transition-all text-sm
                ${isGenerating || selectedCount === 0
                  ? 'bg-slate-300 cursor-not-allowed'
                  : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg hover:shadow-xl'
                }
              `}
            >
              {isGenerating ? (
                <>
                  <LoaderIcon size={16} className="animate-spin" />
                  {labels.processingPdf} ({pdfJob.progress}%)
                </>
              ) : (
                <>
                  <DownloadCloudIcon size={16} />
                  {labels.generatePdf}
                </>
              )}
            </button>
          </div>
        </div>
      )}
      
      {/* Overlay to close dropdown */}
      {isExpanded && (
        <div 
          className="fixed inset-0 z-40" 
          onClick={() => setIsExpanded(false)}
        />
      )}
    </div>
  );
}

export default PdfCustomizer;
