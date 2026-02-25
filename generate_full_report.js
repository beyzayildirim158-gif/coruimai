// Kapsamli Analiz Raporu Olusturucu
// @bununfiyatine - 2d778291-16d0-41df-94c6-1e2716133bbc

const fs = require('fs');
const path = require('path');
const http = require('http');

const ANALYSIS_ID = '2d778291-16d0-41df-94c6-1e2716133bbc';
const USERNAME = 'bununfiyatine';

// Agent verilerini temiz JSON dosyasindan oku
const agentResultsRaw = fs.readFileSync(path.join(__dirname, 'agent_results_clean.json'), 'utf8');
// BOM karakterlerini temizle
const cleanedJson = agentResultsRaw.replace(/^\uFEFF/, '').trim();
const agentResults = JSON.parse(cleanedJson);

// Hesap verilerini oku
const accountDataRaw = fs.readFileSync(path.join(__dirname, 'temp_account.txt'), 'utf8');
const accountParts = accountDataRaw.split('|').map(function(s) { return s.trim(); });
const accountJson = accountParts[accountParts.length - 1];
const rawAccountData = JSON.parse(accountJson);

const accountData = {
  username: rawAccountData.username || USERNAME,
  followers: rawAccountData.followersCount || 339398,
  following: rawAccountData.followsCount || 18,
  posts: rawAccountData.postsCount || 483,
  bio: rawAccountData.biography || '',
  profilePicUrl: rawAccountData.profilePicUrl || '',
  verified: rawAccountData.verified || true,
  engagementRate: 0.05,
  avgLikes: 173,
  avgComments: 6,
  latestPosts: rawAccountData.latestPosts || []
};

// Kapsamli rapor objesi
const fullReport = {
  reportMetadata: {
    reportId: 'full_report_' + ANALYSIS_ID.slice(0, 8),
    analysisId: ANALYSIS_ID,
    generatedAt: new Date().toISOString(),
    version: '2.0',
    reportType: 'COMPREHENSIVE_ANALYSIS'
  },
  
  accountOverview: {
    username: accountData.username,
    fullName: rawAccountData.fullName || 'Bunun Fiyati Ne',
    bio: accountData.bio,
    verified: accountData.verified,
    profilePicUrl: accountData.profilePicUrl,
    statistics: {
      followers: accountData.followers,
      following: accountData.following,
      posts: accountData.posts,
      engagementRate: accountData.engagementRate,
      avgLikes: accountData.avgLikes,
      avgComments: accountData.avgComments
    },
    externalUrl: rawAccountData.external_url || '',
    highlightReelCount: rawAccountData.highlight_reel_count || 0
  },
  
  overallAssessment: {
    overallScore: 35,
    scoreGrade: 'F',
    verdict: 'KRITIK',
    headline: agentResults.eli5Report && agentResults.eli5Report.executiveSummary ? agentResults.eli5Report.executiveSummary.headline : '339K takipciye ragmen etkilesim orani %0.05',
    gradeExplanation: agentResults.eli5Report && agentResults.eli5Report.executiveSummary ? agentResults.eli5Report.executiveSummary.gradeExplanation : 'KRITIK BASARISIZLIK'
  },
  
  agentAnalyses: {
    domainMaster: {
      agentName: 'Domain Master',
      description: 'Niche analizi, sektor karsilastirmasi ve icerik ayaklari',
      metrics: agentResults.domainMaster ? agentResults.domainMaster.metrics : {},
      rawResponse: agentResults.domainMaster && agentResults.domainMaster.rawResponse ? 'Detayli analiz mevcut' : null,
      timestamp: agentResults.domainMaster ? agentResults.domainMaster.timestamp : null
    },
    
    growthVirality: {
      agentName: 'Growth & Virality Architect',
      description: 'Buyume analizi, viral potansiyel ve projeksiyon',
      metrics: agentResults.growthVirality ? agentResults.growthVirality.metrics : {},
      growthOverview: agentResults.growthVirality ? agentResults.growthVirality.growth_overview : {},
      projections: agentResults.growthVirality ? agentResults.growthVirality.projections : {},
      milestones: agentResults.growthVirality ? agentResults.growthVirality.milestones : {},
      channelAnalysis: agentResults.growthVirality ? agentResults.growthVirality.channel_analysis : {},
      funnelAnalysis: agentResults.growthVirality ? agentResults.growthVirality.funnelAnalysis : {},
      viralAnalysis: agentResults.growthVirality ? agentResults.growthVirality.viral_analysis : {},
      riskAssessment: agentResults.growthVirality ? agentResults.growthVirality.risk_assessment : {},
      findings: agentResults.growthVirality ? agentResults.growthVirality.findings : [],
      recommendations: agentResults.growthVirality ? agentResults.growthVirality.recommendations : [],
      timestamp: agentResults.growthVirality ? agentResults.growthVirality.timestamp : null
    },
    
    visualBrand: {
      agentName: 'Visual Brand Analyst',
      description: 'Gorsel kimlik, renk analizi ve grid estetigi',
      metrics: agentResults.visualBrand ? agentResults.visualBrand.metrics : {},
      brandOverview: agentResults.visualBrand ? agentResults.visualBrand.brand_overview : {},
      colorAnalysis: agentResults.visualBrand ? agentResults.visualBrand.color_analysis : {},
      recommendedPalette: agentResults.visualBrand ? agentResults.visualBrand.recommendedPalette : {},
      gridAnalysis: agentResults.visualBrand ? agentResults.visualBrand.grid_analysis : {},
      formatAnalysis: agentResults.visualBrand ? agentResults.visualBrand.format_analysis : {},
      typographyAnalysis: agentResults.visualBrand ? agentResults.visualBrand.typography_analysis : {},
      thumbnailAnalysis: agentResults.visualBrand ? agentResults.visualBrand.thumbnailAnalysis : {},
      consistencyAnalysis: agentResults.visualBrand ? agentResults.visualBrand.consistency_analysis : {},
      brandGuidelines: agentResults.visualBrand ? agentResults.visualBrand.brand_guidelines_suggestion : {},
      findings: agentResults.visualBrand ? agentResults.visualBrand.findings : [],
      recommendations: agentResults.visualBrand ? agentResults.visualBrand.recommendations : [],
      timestamp: agentResults.visualBrand ? agentResults.visualBrand.timestamp : null
    },
    
    communityLoyalty: {
      agentName: 'Community Loyalty Architect',
      description: 'Topluluk sagligi, sadakat ve etkilesim kalitesi',
      metrics: agentResults.communityLoyalty ? agentResults.communityLoyalty.metrics : {},
      communityOverview: agentResults.communityLoyalty ? agentResults.communityLoyalty.community_overview : {},
      communityInsights: agentResults.communityLoyalty ? agentResults.communityLoyalty.communityInsights : {},
      sentimentBreakdown: agentResults.communityLoyalty ? agentResults.communityLoyalty.sentiment_breakdown : {},
      loyaltyBuilders: agentResults.communityLoyalty ? agentResults.communityLoyalty.loyaltyBuilders : [],
      communityRituals: agentResults.communityLoyalty ? agentResults.communityLoyalty.communityRituals : [],
      engagementStrategies: agentResults.communityLoyalty ? agentResults.communityLoyalty.engagementStrategies : [],
      actionPlan: agentResults.communityLoyalty ? agentResults.communityLoyalty.action_plan : {},
      findings: agentResults.communityLoyalty ? agentResults.communityLoyalty.findings : [],
      recommendations: agentResults.communityLoyalty ? agentResults.communityLoyalty.recommendations : [],
      timestamp: agentResults.communityLoyalty ? agentResults.communityLoyalty.timestamp : null
    },
    
    attentionArchitect: {
      agentName: 'Attention Architect',
      description: 'Hook etkinligi, dikkat tutma ve scroll-stop analizi',
      metrics: agentResults.attentionArchitect ? agentResults.attentionArchitect.metrics : {},
      grade: agentResults.attentionArchitect ? agentResults.attentionArchitect.grade : {},
      attentionOverview: agentResults.attentionArchitect ? agentResults.attentionArchitect.attention_overview : {},
      scoreBreakdown: agentResults.attentionArchitect ? agentResults.attentionArchitect.score_breakdown : {},
      retentionPrediction: agentResults.attentionArchitect ? agentResults.attentionArchitect.retentionPrediction : {},
      hookTemplates: agentResults.attentionArchitect ? agentResults.attentionArchitect.hookTemplates : [],
      captionFormulas: agentResults.attentionArchitect ? agentResults.attentionArchitect.captionFormulas : [],
      emotionalTriggers: agentResults.attentionArchitect ? agentResults.attentionArchitect.emotionalTriggers : [],
      thumbnailRecommendations: agentResults.attentionArchitect ? agentResults.attentionArchitect.thumbnailRecommendations : {},
      dropoffAnalysis: agentResults.attentionArchitect ? agentResults.attentionArchitect.dropoff_analysis : {},
      contentSpecificAnalysis: agentResults.attentionArchitect ? agentResults.attentionArchitect.content_specific_analysis : {},
      psychologicalTriggers: agentResults.attentionArchitect ? agentResults.attentionArchitect.psychological_triggers_analysis : {},
      findings: agentResults.attentionArchitect ? agentResults.attentionArchitect.findings : [],
      recommendations: agentResults.attentionArchitect ? agentResults.attentionArchitect.recommendations : [],
      actionPlan: agentResults.attentionArchitect ? agentResults.attentionArchitect.action_plan : {},
      timestamp: agentResults.attentionArchitect ? agentResults.attentionArchitect.timestamp : null
    },
    
    salesConversion: {
      agentName: 'Sales & Conversion Specialist',
      description: 'Monetizasyon, gelir akislari ve marka anlasmalari',
      metrics: agentResults.salesConversion ? agentResults.salesConversion.metrics : {},
      rawResponse: agentResults.salesConversion && agentResults.salesConversion.rawResponse ? 'Detayli analiz mevcut' : null,
      timestamp: agentResults.salesConversion ? agentResults.salesConversion.timestamp : null
    },
    
    systemGovernor: {
      agentName: 'System Governor',
      description: 'Bot tespiti, veri dogrulama ve hesap sagligi',
      metrics: agentResults.systemGovernor ? agentResults.systemGovernor.metrics : {},
      alerts: agentResults.systemGovernor ? agentResults.systemGovernor.alerts : [],
      validation: agentResults.systemGovernor ? agentResults.systemGovernor.validation : {},
      riskAssessment: agentResults.systemGovernor ? agentResults.systemGovernor.risk_assessment : {},
      detailedAnalysis: agentResults.systemGovernor ? agentResults.systemGovernor.detailed_analysis : {},
      qualityAssurance: agentResults.systemGovernor ? agentResults.systemGovernor.quality_assurance : {},
      validationSummary: agentResults.systemGovernor ? agentResults.systemGovernor.validation_summary : {},
      findings: agentResults.systemGovernor ? agentResults.systemGovernor.findings : [],
      recommendations: agentResults.systemGovernor ? agentResults.systemGovernor.recommendations : [],
      timestamp: agentResults.systemGovernor ? agentResults.systemGovernor.timestamp : null
    }
  },
  
  eli5Report: {
    executiveSummary: agentResults.eli5Report ? agentResults.eli5Report.executiveSummary : {},
    findings: agentResults.eli5Report ? agentResults.eli5Report.findings : [],
    rewrittenHooks: agentResults.eli5Report ? agentResults.eli5Report.rewrittenHooks : [],
    weeklyActionPlan: agentResults.eli5Report ? agentResults.eli5Report.weeklyActionPlan : {},
    supremeHookFormula: agentResults.eli5Report ? agentResults.eli5Report.supremeHookFormula : {},
    criticalWarning: agentResults.eli5Report ? agentResults.eli5Report.criticalWarning : '',
    motivationalKick: agentResults.eli5Report ? agentResults.eli5Report.motivationalKick : ''
  },
  
  latestPosts: (accountData.latestPosts || []).slice(0, 5).map(function(post) {
    return {
      id: post.id,
      url: post.url,
      caption: post.caption,
      likes: post.likesCount,
      comments: post.commentsCount,
      timestamp: post.timestamp,
      type: post.productType || post.mediaType
    };
  }),
  
  keyMetricsSummary: {
    engagement: {
      rate: '0.05%',
      benchmark: '2.5-3.5%',
      status: 'KRITIK',
      percentile: 5
    },
    growth: {
      rate: '0%',
      benchmark: '4-6%',
      status: 'DURGUN',
      percentile: 0
    },
    authenticity: {
      score: 35,
      botRisk: 'YUKSEK',
      botScore: 65,
      ghostFollowers: '70%'
    },
    visual: {
      score: 28,
      colorConsistency: 20,
      gridProfessionalism: 40
    },
    community: {
      loyaltyIndex: 41,
      superfanPercentage: 0.5,
      healthScore: 42
    },
    attention: {
      score: 39,
      hookEffectiveness: 42,
      retentionPotential: 38
    }
  },
  
  criticalIssues: [
    {
      issue: 'Etkilesim orani kritik seviyede dusuk (%0.05)',
      impact: 'Algoritma hesabi gormezden geliyor',
      priority: 1
    },
    {
      issue: 'Bot/Ghost takipci orani cok yuksek (~70%)',
      impact: 'Hesap sagligi ve guvenilirlik riski',
      priority: 2
    },
    {
      issue: 'Bio ve icerik uyumsuzlugu',
      impact: 'Algoritma ve kitle karisikligi',
      priority: 3
    },
    {
      issue: 'Reels ve Carousel formatlari kullanilmiyor',
      impact: 'Buyume kanallari kapali',
      priority: 4
    },
    {
      issue: 'Gorsel tutarlilik yok (%85 renk varyansi)',
      impact: 'Marka tanirligi dusuk',
      priority: 5
    }
  ],
  
  immediateActions: [
    'Bio\'yu netlestir ve icerikle uyumlu hale getir',
    'Haftada en az 4 Reels icerigi uretmeye basla',
    'Ghost/bot takipci temizligi yap',
    '3 renkli tutarli bir palet belirle ve uygula',
    'Her gonderide soru sorarak etkilesimi artir'
  ]
};

// JSON dosyasini kaydet
const jsonPath = path.join(__dirname, 'full_report_' + ANALYSIS_ID.slice(0, 8) + '.json');
fs.writeFileSync(jsonPath, JSON.stringify(fullReport, null, 2), 'utf8');
console.log('JSON raporu olusturuldu: ' + jsonPath);

// PDF olusturmak icin PDF generator servisine istek gonder
const pdfPayload = {
  reportId: 'full_report_' + ANALYSIS_ID.slice(0, 8),
  analysisId: ANALYSIS_ID,
  accountData: accountData,
  agentResults: agentResults,
  eli5Report: agentResults.eli5Report,
  overallScore: 35,
  scoreGrade: 'F',
  recommendations: fullReport.immediateActions,
  tier: 'premium'
};

const postData = JSON.stringify(pdfPayload);

const options = {
  hostname: 'localhost',
  port: 3002,
  path: '/generate',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

console.log('\nPDF olusturuluyor...');

const req = http.request(options, function(res) {
  let data = '';
  res.on('data', function(chunk) { data += chunk; });
  res.on('end', function() {
    try {
      const result = JSON.parse(data);
      if (result.success) {
        console.log('PDF raporu olusturuldu: ' + result.filename);
        console.log('Path: ' + result.path);
      } else {
        console.log('PDF olusturma hatasi: ' + result.error);
      }
    } catch (e) {
      console.log('PDF Response:', data);
    }
  });
});

req.on('error', function(e) {
  console.log('PDF servisine baglanilamadi: ' + e.message);
  console.log('PDF generator servisinin calistigindan emin olun.');
});

req.write(postData);
req.end();

console.log('\nRapor Ozeti:');
console.log('==================================================');
console.log('Hesap: @' + accountData.username);
console.log('Takipci: ' + accountData.followers.toLocaleString());
console.log('Genel Skor: ' + fullReport.overallAssessment.overallScore + '/100 (' + fullReport.overallAssessment.scoreGrade + ')');
console.log('Durum: ' + fullReport.overallAssessment.verdict);
console.log('==================================================');
