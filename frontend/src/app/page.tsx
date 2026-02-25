'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  MagicWandIcon,
  BarChart3Icon,
  ShieldIcon,
  LightningIcon,
  TrendingUpIcon,
  UsersIcon,
  DollarSignIcon,
  ArrowRightIcon,
  CheckIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from '@/components/icons';
import { useAuthStore } from '@/store/authStore';
import { useState, useEffect } from 'react';
import { useTranslation } from '@/i18n/TranslationProvider';

const features = [
  {
    icon: ShieldIcon,
    title: { en: 'Bot Detection', tr: 'Bot Tespiti' },
    description: {
      en: 'Advanced AI identifies fake followers and engagement bots',
      tr: 'Gelişmiş AI, sahte takipçi ve bot etkileşimi tespit eder',
    },
  },
  {
    icon: TrendingUpIcon,
    title: { en: 'Growth Strategy', tr: 'Büyüme Stratejisi' },
    description: {
      en: 'Data-driven recommendations to accelerate your growth',
      tr: 'Büyümenizi hızlandıran veri odaklı öneriler üretir',
    },
  },
  {
    icon: BarChart3Icon,
    title: { en: 'Deep Analytics', tr: 'Derin Analitik' },
    description: {
      en: 'Specialized AI agents analyze every aspect of your account',
      tr: 'Uzman AI ajanları hesabınızın her yönünü analiz eder',
    },
  },
  {
    icon: UsersIcon,
    title: { en: 'Community Insights', tr: 'Topluluk İçgörüleri' },
    description: {
      en: 'Understand your audience and build loyal followers',
      tr: 'Kitlenizi anlayın, sadık bir topluluk inşa edin',
    },
  },
  {
    icon: LightningIcon,
    title: { en: 'Viral Potential', tr: 'Viral Potansiyel' },
    description: {
      en: 'Identify content opportunities with high viral probability',
      tr: 'Yüksek viral olasılığa sahip içerik fırsatlarını bulun',
    },
  },
  {
    icon: DollarSignIcon,
    title: { en: 'Monetization', tr: 'Monetizasyon' },
    description: {
      en: 'Unlock revenue streams and brand deal opportunities',
      tr: 'Gelir kanallarını ve marka iş birliği fırsatlarını açığa çıkarın',
    },
  },
];

const allAgents = [
  {
    name: { en: 'System Governor', tr: 'System Governor' },
    role: { en: 'Data Validation & Bot Detection', tr: 'Veri Doğrulama & Bot Tespiti' },
  },
  {
    name: { en: 'Growth Specialist', tr: 'Growth Specialist' },
    role: { en: 'Growth Strategy & Viral Potential', tr: 'Büyüme Stratejisi & Viral Potansiyel' },
  },
  {
    name: { en: 'Attention Architect', tr: 'Attention Architect' },
    role: { en: 'Content Retention Optimization', tr: 'İçerik Tutma Optimizasyonu' },
  },
  {
    name: { en: 'Sales Conversion', tr: 'Sales Conversion' },
    role: { en: 'Monetization Strategy', tr: 'Monetizasyon Stratejisi' },
  },
  {
    name: { en: 'Community Loyalty', tr: 'Community Loyalty' },
    role: { en: 'Engagement & Community Building', tr: 'Etkileşim & Topluluk İnşası' },
  },
  {
    name: { en: 'Visual Brand', tr: 'Visual Brand' },
    role: { en: 'Brand Identity & Consistency', tr: 'Marka Kimliği & Tutarlılık' },
  },
  {
    name: { en: 'Domain Master', tr: 'Domain Master' },
    role: { en: 'Niche Positioning & Competition', tr: 'Niş Konumlandırma & Rekabet' },
  },
] as const;

const pricingPlans = [
  {
    name: 'Starter' as const,
    price: '100 TL',
    period: '/month',
    description: {
      en: 'Perfect for new creators',
      tr: 'Yeni başlayan üreticiler için ideal',
    },
    features: {
      en: ['10 analyses per month', '3 AI agents', 'Basic PDF reports', 'Email support'],
      tr: ['Aylık 10 analiz', '3 AI ajanı', 'Temel PDF raporları', 'E-posta desteği'],
    },
    agentCount: 3,
    popular: false,
  },
  {
    name: 'Professional' as const,
    price: '200 TL',
    period: '/month',
    description: {
      en: 'For serious content creators',
      tr: 'Büyümeye odaklı içerik üreticileri için',
    },
    features: {
      en: ['50 analyses per month', '5 AI agents', 'Advanced PDF reports', 'Priority support', 'API access'],
      tr: ['Aylık 50 analiz', '5 AI ajanı', 'Gelişmiş PDF raporları', 'Öncelikli destek', 'API erişimi'],
    },
    agentCount: 5,
    popular: true,
  },
  {
    name: 'Premium' as const,
    price: '1000 TL',
    period: '/month',
    description: {
      en: 'For established influencers',
      tr: 'Yerleşik influencer profilleri için',
    },
    features: {
      en: ['200 analyses per month', 'All 7 AI agents', 'Premium PDF reports', '24/7 support', 'Full API access', 'White-label reports'],
      tr: ['Aylık 200 analiz', 'Tüm 7 AI ajanı', 'Premium PDF raporları', '7/24 destek', 'Tam API erişimi', 'White-label raporlar'],
    },
    agentCount: 7,
    popular: false,
  },
  {
    name: 'Enterprise' as const,
    price: '5000 TL',
    period: '/month',
    description: {
      en: 'For agencies and teams',
      tr: 'Ajanslar ve ekipler için',
    },
    features: {
      en: ['Unlimited analyses', 'All 7 AI agents', 'Custom integrations', 'Dedicated account manager', 'Team collaboration', 'Priority processing'],
      tr: ['Sınırsız analiz', 'Tüm 7 AI ajanı', 'Özel entegrasyonlar', 'Özel müşteri yöneticisi', 'Ekip iş birliği', 'Öncelikli işleme'],
    },
    agentCount: 7,
    popular: false,
  },
];

const slides = [
  {
    title: {
      en: 'How the system works: Data ingestion & cleanup',
      tr: 'Sistem nasıl çalışır: Veri toplama ve temizleme',
    },
    description: {
      en: 'Public Instagram signals are collected, validated, and standardized before analysis starts.',
      tr: 'Analiz başlamadan önce herkese açık Instagram sinyalleri toplanır, doğrulanır ve standardize edilir.',
    },
    badge: { en: 'Step 1', tr: 'Adım 1' },
    image: '/landing-slider/step-1.svg',
    imageAlt: {
      en: 'Data ingestion and cleanup visual',
      tr: 'Veri toplama ve temizleme görseli',
    },
  },
  {
    title: {
      en: 'Multi-agent intelligence in parallel',
      tr: 'Paralel çoklu ajan zekâsı',
    },
    description: {
      en: 'Specialized AI agents evaluate growth, brand, conversion, attention, community and niche positioning.',
      tr: 'Uzman AI ajanları büyüme, marka, dönüşüm, dikkat, topluluk ve niş konumlandırmayı değerlendirir.',
    },
    badge: { en: 'Step 2', tr: 'Adım 2' },
    image: '/landing-slider/step-2.svg',
    imageAlt: {
      en: 'Multi-agent analysis visual',
      tr: 'Çoklu ajan analiz görseli',
    },
  },
  {
    title: {
      en: 'Decision-grade report & action plan',
      tr: 'Karar seviyesinde rapor ve aksiyon planı',
    },
    description: {
      en: 'You receive benchmarked scores, prioritized recommendations, and export-ready PDF reports.',
      tr: 'Kıyaslamalı skorlar, önceliklendirilmiş öneriler ve dışa aktarılabilir PDF raporları elde edersiniz.',
    },
    badge: { en: 'Step 3', tr: 'Adım 3' },
    image: '/landing-slider/step-3.svg',
    imageAlt: {
      en: 'Report and action plan visual',
      tr: 'Rapor ve aksiyon planı görseli',
    },
  },
];

const copy = {
  en: {
    dashboard: 'Dashboard',
    login: 'Login',
    getStarted: 'Get Started',
    heroTitleTop: 'AI-Powered',
    heroTitleBottom: 'Instagram Analytics',
    heroDesc:
      'Specialized AI agents analyze your Instagram account and provide actionable insights to grow audience and revenue.',
    startTrial: 'Start Free Trial',
    learnMore: 'Learn More',
    featuresTitle: 'Powerful Features for Creators',
    agentsTitle: 'Specialized AI Agents',
    agentsSubtitle: 'Agent coverage varies by plan. Starter starts with 3, Professional 5, Premium/Enterprise 7.',
    pricingTitle: 'Simple, Transparent Pricing',
    pricingSubtitle: 'Choose the plan that fits your growth stage',
    pricingPeriod: '/month',
    mostPopular: 'Most Popular',
    agentsIncluded: 'Agents included',
    systemSliderTitle: 'Platform Walkthrough',
    systemSliderDesc: 'This slider pulls visuals directly from the landing-slider folder in public assets.',
    imagePlaceholder: 'Visual placeholder',
    previous: 'Previous',
    next: 'Next',
    ctaTitle: 'Ready to Transform Your Instagram?',
    ctaDesc: 'Join creators using AI to grow their audience and revenue.',
    ctaButton: 'Start Your Free Trial',
    footer: 'Instagram Intelligence Platform. All rights reserved.',
  },
  tr: {
    dashboard: 'Kontrol Paneli',
    login: 'Giriş Yap',
    getStarted: 'Başlayın',
    heroTitleTop: 'AI Destekli',
    heroTitleBottom: 'Instagram Analizi',
    heroDesc:
      'Uzman AI ajanları Instagram hesabınızı analiz eder, büyüme ve gelir için uygulanabilir içgörüler sunar.',
    startTrial: 'Ücretsiz Denemeyi Başlat',
    learnMore: 'Daha Fazla Bilgi',
    featuresTitle: 'İçerik Üreticiler için Güçlü Özellikler',
    agentsTitle: 'Uzman AI Ajanları',
    agentsSubtitle: 'Planlara göre ajan kapsamı değişir. Starter 3, Professional 5, Premium/Enterprise 7 ajan ile çalışır.',
    pricingTitle: 'Basit ve Şeffaf Fiyatlandırma',
    pricingSubtitle: 'Büyüme seviyenize uygun planı seçin',
    pricingPeriod: '/ay',
    mostPopular: 'En Popüler',
    agentsIncluded: 'Dahil olan ajan',
    systemSliderTitle: 'Platform Akışı',
    systemSliderDesc: 'Bu slider görselleri doğrudan public içindeki landing-slider klasöründen çeker.',
    imagePlaceholder: 'Görsel alanı',
    previous: 'Önceki',
    next: 'Sonraki',
    ctaTitle: 'Instagram Hesabınızı Dönüştürmeye Hazır mısınız?',
    ctaDesc: 'Kitlesini ve gelirini AI ile büyüten içerik üreticilerine katılın.',
    ctaButton: 'Ücretsiz Denemeni Başlat',
    footer: 'Instagram Intelligence Platform. Tüm hakları saklıdır.',
  },
} as const;

export default function Home() {
  const { isAuthenticated } = useAuthStore();
  const { locale, setLocale } = useTranslation();
  const [mounted, setMounted] = useState(false);
  const [activeSlide, setActiveSlide] = useState(0);

  const lang = locale === 'en' ? 'en' : 'tr';
  const text = copy[lang];
  const totalAgentCount = allAgents.length;

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveSlide((prev) => (prev + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50">
      <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-28 -left-20 h-72 w-72 rounded-full bg-primary-100/40 blur-3xl" />
        <div className="absolute top-1/3 -right-24 h-72 w-72 rounded-full bg-blue-100/40 blur-3xl" />
      </div>

      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 border-b border-slate-200 bg-white/80 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <MagicWandIcon className="h-8 w-8 text-primary-500" />
              <span className="text-xl font-bold text-slate-900">corium.ai</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="inline-flex items-center rounded-lg border border-slate-200 bg-white p-1 shadow-sm">
                <button
                  onClick={() => setLocale('tr')}
                  className={`rounded-md px-2.5 py-1 text-xs font-semibold transition-colors ${
                    lang === 'tr' ? 'bg-primary-600 text-white' : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  TR
                </button>
                <button
                  onClick={() => setLocale('en')}
                  className={`rounded-md px-2.5 py-1 text-xs font-semibold transition-colors ${
                    lang === 'en' ? 'bg-primary-600 text-white' : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  EN
                </button>
              </div>

              {mounted && isAuthenticated ? (
                <Link
                  href="/dashboard"
                  className="rounded-lg bg-primary-600 px-4 py-2 text-white transition-colors hover:bg-primary-700"
                >
                  {text.dashboard}
                </Link>
              ) : (
                <>
                  <Link
                    href="/login"
                    className="px-4 py-2 text-slate-700 transition-colors hover:text-primary-600"
                  >
                    {text.login}
                  </Link>
                  <Link
                    href="/register"
                    className="rounded-lg bg-primary-600 px-4 py-2 text-white transition-colors hover:bg-primary-700"
                  >
                    {text.getStarted}
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-slate-900 mb-6">
              <span className="gradient-text">{text.heroTitleTop}</span>
              <br />
              {text.heroTitleBottom}
            </h1>
            <p className="text-xl text-slate-600 mb-8 max-w-2xl mx-auto">
              {text.heroDesc}
            </p>

            <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-primary-200 bg-primary-50 px-4 py-2 text-sm text-primary-700">
              <span className="h-2 w-2 rounded-full bg-primary-500" />
              {totalAgentCount} AI agents • Starter 3 • Pro 5 • Premium 7
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/register"
                className="flex items-center justify-center gap-2 rounded-xl bg-primary-600 px-8 py-4 text-lg font-semibold text-white transition-all hover:scale-[1.02] hover:bg-primary-700"
              >
                {text.startTrial}
                <ArrowRightIcon className="h-5 w-5" />
              </Link>
              <Link
                href="#features"
                className="rounded-xl bg-slate-100 px-8 py-4 text-lg font-semibold text-slate-900 transition-colors hover:bg-slate-200"
              >
                {text.learnMore}
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* System Slider Section */}
      <section className="pb-8 px-4">
        <div className="max-w-7xl mx-auto rounded-3xl border border-slate-200 bg-white/90 p-6 shadow-sm backdrop-blur">
          <div className="mb-6 flex items-start justify-between gap-4">
            <div>
              <h2 className="text-2xl md:text-3xl font-bold text-slate-900">{text.systemSliderTitle}</h2>
              <p className="mt-2 text-slate-600">{text.systemSliderDesc}</p>
            </div>
            <div className="hidden md:flex items-center gap-2">
              <button
                onClick={() => setActiveSlide((prev) => (prev - 1 + slides.length) % slides.length)}
                className="rounded-lg border border-slate-200 p-2 text-slate-600 hover:bg-slate-50"
                aria-label={text.previous}
              >
                <ChevronLeftIcon className="h-5 w-5" />
              </button>
              <button
                onClick={() => setActiveSlide((prev) => (prev + 1) % slides.length)}
                className="rounded-lg border border-slate-200 p-2 text-slate-600 hover:bg-slate-50"
                aria-label={text.next}
              >
                <ChevronRightIcon className="h-5 w-5" />
              </button>
            </div>
          </div>

          <motion.div
            key={activeSlide}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35 }}
            className="grid gap-5 lg:grid-cols-[1.1fr_1fr]"
          >
            <div className="rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-6">
              <span className="inline-flex rounded-full bg-primary-100 px-3 py-1 text-xs font-semibold text-primary-700">
                {slides[activeSlide].badge[lang]}
              </span>
              <h3 className="mt-4 text-2xl font-semibold text-slate-900">{slides[activeSlide].title[lang]}</h3>
              <p className="mt-3 leading-7 text-slate-600">{slides[activeSlide].description[lang]}</p>
            </div>

            <div className="overflow-hidden rounded-2xl border border-slate-200 bg-slate-50/70 min-h-[240px]">
              <img
                src={slides[activeSlide].image}
                alt={slides[activeSlide].imageAlt[lang]}
                className="h-full w-full object-cover"
                loading="lazy"
              />
            </div>
          </motion.div>

          <div className="mt-5 flex items-center justify-center gap-2">
            {slides.map((_, index) => (
              <button
                key={index}
                onClick={() => setActiveSlide(index)}
                className={`h-2.5 rounded-full transition-all ${activeSlide === index ? 'w-8 bg-primary-600' : 'w-2.5 bg-slate-300 hover:bg-slate-400'}`}
                aria-label={`Slide ${index + 1}`}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 text-center mb-12">
            {text.featuresTitle}
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title.en}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-lg"
              >
                <feature.icon className="h-12 w-12 text-primary-500 mb-4" />
                <h3 className="text-xl font-semibold text-slate-900 mb-2">
                  {feature.title[lang]}
                </h3>
                <p className="text-slate-600">{feature.description[lang]}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Agents Section */}
      <section className="py-20 px-4 bg-slate-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 text-center mb-4">
            {totalAgentCount} {text.agentsTitle}
          </h2>
          <p className="text-slate-600 text-center mb-12 max-w-2xl mx-auto">
            {text.agentsSubtitle}
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {allAgents.map((agent, index) => (
              <motion.div
                key={agent.name.en}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="rounded-xl border border-primary-200 bg-gradient-to-br from-primary-50 to-primary-100 p-4 shadow-sm"
              >
                <h4 className="mb-1 font-semibold text-slate-900">{agent.name[lang]}</h4>
                <p className="text-sm text-slate-600">{agent.role[lang]}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 text-center mb-4">
            {text.pricingTitle}
          </h2>
          <p className="text-slate-600 text-center mb-12">
            {text.pricingSubtitle}
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {pricingPlans.map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className={`p-6 rounded-2xl ${
                  plan.popular
                    ? 'bg-gradient-to-br from-primary-600 to-primary-700 border-2 border-primary-400'
                    : 'bg-white border border-slate-200 shadow-sm hover:shadow-md'
                } relative`}
              >
                {plan.popular && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-yellow-500 text-black text-sm font-semibold rounded-full">
                    {text.mostPopular}
                  </span>
                )}
                <h3 className={`text-xl font-bold mb-2 ${plan.popular ? 'text-white' : 'text-slate-900'}`}>{plan.name}</h3>
                <p className={`text-sm mb-4 ${plan.popular ? 'text-white/80' : 'text-slate-600'}`}>{plan.description[lang]}</p>
                <div className="mb-6">
                  <span className={`text-4xl font-bold ${plan.popular ? 'text-white' : 'text-slate-900'}`}>{plan.price}</span>
                  <span className={plan.popular ? 'text-white/80' : 'text-slate-600'}>{text.pricingPeriod}</span>
                </div>

                <div className={`mb-4 rounded-lg px-3 py-2 text-sm ${plan.popular ? 'bg-white/15 text-white' : 'bg-primary-50 text-primary-700'}`}>
                  {text.agentsIncluded}: <span className="font-semibold">{plan.agentCount}</span>
                </div>

                <ul className="space-y-3 mb-6">
                  {plan.features[lang].map((feature) => (
                    <li key={feature} className={`flex items-center gap-2 ${plan.popular ? 'text-white/90' : 'text-slate-700'}`}>
                      <CheckIcon className="h-5 w-5 text-green-500 flex-shrink-0" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  href="/register"
                  className={`block w-full py-3 text-center rounded-lg font-semibold transition-colors ${
                    plan.popular
                      ? 'bg-white text-primary-600 hover:bg-slate-100'
                      : 'bg-primary-600 text-white hover:bg-primary-700'
                  }`}
                >
                  {text.getStarted}
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-slate-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-6">
            {text.ctaTitle}
          </h2>
          <p className="text-slate-600 mb-8">
            {text.ctaDesc}
          </p>
          <Link
            href="/register"
            className="inline-flex items-center gap-2 px-8 py-4 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-semibold text-lg transition-all hover:scale-105"
          >
            {text.ctaButton}
            <ArrowRightIcon className="h-5 w-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-slate-200 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <MagicWandIcon className="h-6 w-6 text-primary-500" />
              <span className="text-lg font-bold text-slate-900">corium.ai</span>
            </div>
            <p className="text-slate-500 text-sm">
              © {new Date().getFullYear()} corium.ai - {text.footer}
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
