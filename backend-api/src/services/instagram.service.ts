// Instagram Data Service - Apify Integration
// Cache disabled - always fetch fresh data for each analysis
import axios, { AxiosError } from 'axios';
import { config } from '../config/index.js';
import { logger } from '../utils/logger.js';
import { ServiceUnavailableError, BadRequestError } from '../utils/errors.js';

export interface AccountData {
  username: string;
  followers: number;
  following: number;
  posts: number;
  bio: string | null;
  profilePicUrl: string | null;
  profilePicBase64: string | null; // Base64 encoded profile picture
  verified: boolean;
  isPrivate: boolean;
  isBusiness: boolean;
  engagementRate: number | null;   // null = veri çekilemedi, 0 = gerçek sıfır
  avgLikes: number | null;         // null = veri çekilemedi, 0 = gerçek sıfır
  avgComments: number | null;      // null = veri çekilemedi, 0 = gerçek sıfır
  botScore: number;
  isBot: boolean;
  suspiciousPatterns: string[];
  niche: string;
  fullName: string | null;
  externalUrl: string | null;
  recentPosts: RecentPost[];
  rawData: Record<string, any>;
  dataFetchWarning: string | null; // Veri çekme uyarısı (HAYALET VERİ tespiti)
}

interface RecentPost {
  id: string;
  type: 'image' | 'video' | 'carousel';
  likes: number;
  comments: number;
  caption: string | null;
  timestamp: string;
}

interface ApifyRunResponse {
  data: {
    id: string;
    defaultDatasetId: string;
    status: string;
  };
}

interface ApifyDatasetItem {
  // Both naming conventions supported
  username?: string;
  followersCount?: number;
  followers?: number;
  followsCount?: number;
  following?: number;
  postsCount?: number;
  posts?: number;
  biography?: string;
  profilePicUrl?: string;
  verified?: boolean;
  isVerified?: boolean;
  private?: boolean;
  isPrivate?: boolean;
  business?: boolean;
  isBusinessAccount?: boolean;
  isProfessionalAccount?: boolean;
  fullName?: string;
  externalUrl?: string;
  botScore?: number;
  isBot?: boolean;
  isLikelyBot?: boolean;
  humanScore?: number;
  suspiciousPatterns?: string[];
  engagementRate?: number;
  averageEngagementRate?: number;
  avgLikesPerPost?: number;
  avgCommentsPerPost?: number;
  latestPosts?: any[];
  highlightReelCount?: number;
  hasClips?: boolean;
  followerFollowingRatio?: number;
  [key: string]: any;
}

class InstagramDataService {
  private readonly APIFY_BASE_URL = 'https://api.apify.com/v2';
  private readonly MAX_POLL_TIME = 90000; // 90 seconds (increased for fallback)
  private readonly POLL_INTERVAL = 2000; // 2 seconds

  // Profile scraper fallback chain
  private getProfileActors(): string[] {
    return [
      config.apify.actorProfile1,
      config.apify.actorProfile2,
      config.apify.actorProfile3,
    ].filter(Boolean);
  }

  // Fetch account data from Apify with fallback
  async fetchAccountData(username: string): Promise<AccountData> {
    // Normalize username
    const normalizedUsername = this.normalizeUsername(username);
    
    // No cache - always fetch fresh data for each analysis
    logger.info(`Fetching fresh data for @${normalizedUsername} from Apify`);

    const actors = this.getProfileActors();
    let lastError: Error | null = null;

    // Try each actor in the fallback chain
    for (let i = 0; i < actors.length; i++) {
      const actorId = actors[i];
      logger.info(`Trying actor ${i + 1}/${actors.length}: ${actorId}`);

      try {
        // Start Apify actor run
        const runId = await this.startActorRun(normalizedUsername, actorId);
        
        // Poll for completion
        const datasetId = await this.pollForCompletion(runId);
        
        // Fetch results
        const rawData = await this.fetchDatasetItems(datasetId);
        
        // Parse and normalize data
        const accountData = this.parseAccountData(rawData, normalizedUsername);
        
        // Check if we got valid data
        if (accountData.followers > 0 || accountData.posts > 0) {
          logger.info(`✅ Successfully fetched data using ${actorId}`);
          
          // Download and convert profile picture to base64 (for persistence)
          if (accountData.profilePicUrl) {
            accountData.profilePicBase64 = await this.fetchProfilePicBase64(accountData.profilePicUrl);
          }
          
          return accountData;
        } else {
          logger.warn(`Actor ${actorId} returned empty data, trying next...`);
          lastError = new Error(`Empty data from ${actorId}`);
        }
      } catch (error) {
        logger.warn(`Actor ${actorId} failed:`, (error as Error).message);
        lastError = error as Error;
        // Continue to next actor
      }
    }

    // All actors failed
    logger.error(`All ${actors.length} actors failed for @${normalizedUsername}`);
    
    if (lastError instanceof BadRequestError || lastError instanceof ServiceUnavailableError) {
      throw lastError;
    }
    
    throw new ServiceUnavailableError(
      'Failed to fetch Instagram data. All scrapers failed. Please try again later.'
    );
  }

  // Start Apify actor run with specific actor
  private async startActorRun(username: string, actorId: string): Promise<string> {
    // Apify API uses ~ instead of / for actor ID format (e.g., apify~instagram-scraper)
    const apiActorId = actorId.replace('/', '~');
    const url = `${this.APIFY_BASE_URL}/acts/${apiActorId}/runs`;
    
    try {
      // ============================================================
      // MULTI-ACTOR SUPPORT - Dynamic input based on actor type
      // Different actors have different input schemas
      // ============================================================
      const input = this.getActorInput(username, actorId);
      
      logger.info(`Starting actor ${actorId} (API: ${apiActorId}) with input:`, JSON.stringify(input));
      
      const response = await axios.post<ApifyRunResponse>(
        url,
        input,
        {
          headers: {
            Authorization: `Bearer ${config.apify.apiToken}`,
            'Content-Type': 'application/json',
          },
          params: {
            token: config.apify.apiToken,
          },
        }
      );

      const runId = response.data.data.id;
      logger.info(`Started Apify run: ${runId} (actor: ${actorId})`);
      
      return runId;
    } catch (error) {
      const axiosError = error as AxiosError;
      
      // Build detailed error information
      const errorDetails = {
        actorId: actorId,
        apiActorId: apiActorId,
        url: url,
        errorMessage: axiosError.message,
        httpStatus: axiosError.response?.status,
        httpStatusText: axiosError.response?.statusText,
        responseData: axiosError.response?.data,
        requestData: axiosError.config?.data ? JSON.parse(axiosError.config.data) : null,
        errorCode: axiosError.code,
      };
      
      // Log each piece of information separately for better visibility
      logger.error(`❌ Failed to start Apify actor ${actorId}`);
      logger.error(`Error Message: ${axiosError.message}`);
      logger.error(`HTTP Status: ${axiosError.response?.status} ${axiosError.response?.statusText || ''}`);
      logger.error(`Error Code: ${axiosError.code || 'N/A'}`);
      
      if (axiosError.response?.data) {
        logger.error(`Response Data: ${JSON.stringify(axiosError.response.data, null, 2)}`);
      }
      
      // Log full error details as structured object
      logger.error('Full Apify Error Details:', errorDetails);
      
      // Handle specific error codes
      if (axiosError.response?.status === 402) {
        throw new ServiceUnavailableError('Apify credits exhausted. Please add credits to your Apify account.');
      }
      
      if (axiosError.response?.status === 404) {
        throw new Error(`Apify actor not found or not accessible: ${actorId}. Please check the actor ID and your permissions.`);
      }
      
      if (axiosError.response?.status === 401 || axiosError.response?.status === 403) {
        throw new Error(`Apify authentication failed for actor ${actorId}. Please check your API token.`);
      }
      
      // Generic error with full details
      throw new Error(`Failed to start actor ${actorId}: ${axiosError.message} (Status: ${axiosError.response?.status || 'N/A'})`);
    }
  }

  // Get actor-specific input parameters
  private getActorInput(username: string, actorId: string): Record<string, any> {
    // Different actors have different input schemas
    const actorInputMap: Record<string, Record<string, any>> = {
      // curious_coder/instagram-scraper
      'curious_coder/instagram-scraper': {
        username: username,
        resultsLimit: 30,
      },
      // coderx/instagram-profile-scraper-bio-posts
      'coderx/instagram-profile-scraper-bio-posts': {
        usernames: [username],
        maxPosts: 20,
      },
      // apify/instagram-profile-scraper
      'apify/instagram-profile-scraper': {
        usernames: [username],
      },
      // apify/instagram-scraper (generic)
      'apify/instagram-scraper': {
        directUrls: [`https://www.instagram.com/${username}/`],
        resultsLimit: 30,
        searchType: 'user',
      },
      // louisdeconinck/instagram-bot-detector (legacy)
      'louisdeconinck/instagram-bot-detector': {
        usernames: [username],
        resultsLimit: 20,
        resultsType: 'posts',
        searchLimit: 1,
        addParentData: true,
      },
    };

    // Return actor-specific input or default
    return actorInputMap[actorId] || {
      usernames: [username],
      username: username,
      resultsLimit: 20,
    };
  }

  // Poll for actor completion
  private async pollForCompletion(runId: string): Promise<string> {
    const url = `${this.APIFY_BASE_URL}/actor-runs/${runId}`;
    const startTime = Date.now();
    
    while (Date.now() - startTime < this.MAX_POLL_TIME) {
      try {
        const response = await axios.get(url, {
          params: { token: config.apify.apiToken },
        });

        const { status, defaultDatasetId } = response.data.data;
        
        if (status === 'SUCCEEDED') {
          logger.info(`Apify run ${runId} completed successfully`);
          return defaultDatasetId;
        }
        
        if (status === 'FAILED' || status === 'ABORTED') {
          throw new ServiceUnavailableError(`Apify run failed with status: ${status}`);
        }
        
        // Wait before next poll
        await this.sleep(this.POLL_INTERVAL);
      } catch (error) {
        if (error instanceof ServiceUnavailableError) {
          throw error;
        }
        logger.error('Error polling Apify run:', error);
      }
    }

    throw new ServiceUnavailableError('Analysis timed out. Please try again.');
  }

  // Fetch dataset items
  private async fetchDatasetItems(datasetId: string): Promise<ApifyDatasetItem[]> {
    const url = `${this.APIFY_BASE_URL}/datasets/${datasetId}/items`;
    
    try {
      const response = await axios.get<ApifyDatasetItem[]>(url, {
        params: { token: config.apify.apiToken },
      });

      if (!response.data || response.data.length === 0) {
        throw new BadRequestError('No data found for this account');
      }

      return response.data;
    } catch (error) {
      if (error instanceof BadRequestError) {
        throw error;
      }
      logger.error('Failed to fetch dataset items:', error);
      throw new ServiceUnavailableError('Failed to retrieve analysis results');
    }
  }

  // Parse and normalize account data
  private parseAccountData(
    rawData: ApifyDatasetItem[],
    username: string
  ): AccountData {
    const data = rawData[0];
    
    if (!data) {
      throw new BadRequestError('No data found for this account');
    }

    // Log raw data for debugging
    logger.debug('Raw Apify data:', JSON.stringify(data, null, 2));

    // ============================================================
    // OPERATION SIGHT RESTORATION - HAYALET VERİ KONTROLÜ
    // Profil dolu ama post çekilemedi mi? Bu kritik bir API sorunudur!
    // ============================================================
    const reportedPostCount = data.postsCount || data.posts || 0;
    const scrapedPosts = data.latestPosts || [];
    
    if (reportedPostCount > 0 && scrapedPosts.length === 0) {
      logger.error(`⚠️ HAYALET VERİ TESPİT EDİLDİ: @${username}`);
      logger.error(`   Profilde ${reportedPostCount} post var ama 0 post çekildi!`);
      logger.error(`   OLASI SEBEPLER:`);
      logger.error(`   1. resultsType: 'details' yerine 'posts' olmalı`);
      logger.error(`   2. resultsLimit çok düşük (0 veya 1)`);
      logger.error(`   3. Hesap gizli veya yaş kısıtlamalı`);
      logger.error(`   4. Apify cookie/login gerekebilir`);
      // Uyarıyı data'ya ekle (analiz sırasında görülebilir)
      (data as any).__dataFetchWarning = `SCRAPER_PARTIAL_DATA: Profil erişildi ancak ${reportedPostCount} gönderiden 0 tanesi çekildi. Engagement metrikleri güvenilir değil.`;
    } else if (reportedPostCount > 10 && scrapedPosts.length < 5) {
      logger.warn(`⚠️ KISMİ VERİ: @${username} - ${reportedPostCount} posttan sadece ${scrapedPosts.length} tanesi çekildi`);
      (data as any).__dataFetchWarning = `SCRAPER_LIMITED_DATA: ${reportedPostCount} gönderiden sadece ${scrapedPosts.length} tanesi çekildi. Sonuçlar kısmi olabilir.`;
    }

    // Handle both field naming conventions from Apify (followersCount vs followers)
    const followers = data.followersCount || data.followers || 0;
    const following = data.followsCount || data.following || 0;
    const posts = data.postsCount || data.posts || 0;
    
    // ============================================================
    // OPERATION SIGHT RESTORATION - GÜVENLİ METRİK HESAPLAMA
    // Post çekilmediyse 0 DEĞİL null döndür! Ajanlar farkı bilmeli.
    // ============================================================
    const scrapedPostsForCalc = data.latestPosts || [];
    const hasValidPosts = scrapedPostsForCalc.length > 0 && 
                          scrapedPostsForCalc.some((p: any) => (p.likesCount || p.likes || 0) > 0);
    
    // Manuel hesaplama (Apify bazen avgLikes vermez)
    let calculatedAvgLikes: number | null = null;
    let calculatedAvgComments: number | null = null;
    
    if (hasValidPosts) {
      const validPosts = scrapedPostsForCalc.filter((p: any) => 
        (p.likesCount || p.likes || 0) > 0 || (p.commentsCount || p.comments || 0) > 0
      ).slice(0, 12); // Son 12 post
      
      if (validPosts.length > 0) {
        const totalLikes = validPosts.reduce((sum: number, p: any) => 
          sum + (p.likesCount || p.likes || 0), 0);
        const totalComments = validPosts.reduce((sum: number, p: any) => 
          sum + (p.commentsCount || p.comments || 0), 0);
        
        calculatedAvgLikes = Math.round(totalLikes / validPosts.length);
        calculatedAvgComments = Math.round(totalComments / validPosts.length);
        
        logger.info(`✅ Manuel engagement hesaplandı: ${validPosts.length} posttan avgLikes=${calculatedAvgLikes}, avgComments=${calculatedAvgComments}`);
      }
    }
    
    // Apify'dan gelen veya manuel hesaplanan değeri kullan
    const avgLikes = calculatedAvgLikes ?? data.avgLikesPerPost ?? null;
    const avgComments = calculatedAvgComments ?? data.avgCommentsPerPost ?? null;
    
    // Engagement rate: Sadece geçerli veri varsa hesapla
    let engagementRate: number | null = null;
    if (avgLikes !== null && avgComments !== null && followers > 0) {
      engagementRate = Number((((avgLikes + avgComments) / followers) * 100).toFixed(2));
    } else if (data.engagementRate || data.averageEngagementRate) {
      engagementRate = data.engagementRate || data.averageEngagementRate || null;
    }
    
    // Veri yoksa log'la
    if (avgLikes === null) {
      logger.warn(`⚠️ @${username}: avgLikes = NULL (veri çekilemedi, 0 DEĞİL!)`);
    }
    if (engagementRate === null) {
      logger.warn(`⚠️ @${username}: engagementRate = NULL (veri çekilemedi, 0 DEĞİL!)`);
    }

    // Determine niche based on bio/posts (simplified)
    const niche = this.determineNiche(data.biography || '', data.latestPosts || []);

    // Parse recent posts
    const recentPosts: RecentPost[] = (data.latestPosts || [])
      .slice(0, 12)
      .map((post: any) => ({
        id: post.id || post.shortCode || '',
        type: post.type || 'image',
        likes: post.likesCount || post.likes || 0,
        comments: post.commentsCount || post.comments || 0,
        caption: post.caption || null,
        timestamp: post.timestamp || post.takenAt || new Date().toISOString(),
      }));

    // Log parsed values
    logger.info(`Parsed account data: followers=${followers}, following=${following}, posts=${posts}, engagement=${engagementRate}`);

    return {
      username: data.username || username,
      followers,
      following,
      posts,
      bio: data.biography || null,
      profilePicUrl: data.profilePicUrl || null,
      profilePicBase64: null, // Will be populated after parsing
      verified: data.verified || data.isVerified || false,
      isPrivate: data.private || data.isPrivate || false,
      isBusiness: data.business || data.isBusinessAccount || data.isProfessionalAccount || false,
      // NULL-SAFE metrikler: 0 ve null farklı anlama gelir!
      // null = "veri yok", 0 = "gerçekten sıfır etkileşim"
      engagementRate: engagementRate,  // null olabilir!
      avgLikes: avgLikes,              // null olabilir!
      avgComments: avgComments,        // null olabilir!
      // Veri erişim uyarısı
      dataFetchWarning: (data as any).__dataFetchWarning || null,
      botScore: data.botScore || this.calculateBotScore(data),
      isBot: data.isBot ?? data.isLikelyBot ?? (data.botScore !== undefined && data.botScore > 50),
      suspiciousPatterns: data.suspiciousPatterns || this.detectSuspiciousPatterns(data),
      niche,
      fullName: data.fullName || null,
      externalUrl: data.externalUrl || null,
      recentPosts,
      rawData: data,
    };
  }

  // Calculate bot score if not provided
  private calculateBotScore(data: ApifyDatasetItem): number {
    let score = 0;
    
    // High following/follower ratio
    const followers = data.followersCount || 0;
    const following = data.followsCount || 0;
    
    if (followers > 0) {
      const ratio = following / followers;
      if (ratio > 10) score += 30;
      else if (ratio > 5) score += 20;
      else if (ratio > 2) score += 10;
    }
    
    // Low engagement
    const engagementRate = data.engagementRate || 0;
    if (engagementRate < 0.5) score += 20;
    else if (engagementRate < 1) score += 10;
    
    // Very low or high post count
    const posts = data.postsCount || 0;
    if (posts < 10 && followers > 1000) score += 15;
    if (posts > 5000) score += 10;
    
    // No profile pic
    if (!data.profilePicUrl) score += 10;
    
    // No bio
    if (!data.biography) score += 10;
    
    // Private account with high followers
    if (data.private && followers > 10000) score += 15;
    
    return Math.min(100, score);
  }

  // Detect suspicious patterns
  private detectSuspiciousPatterns(data: ApifyDatasetItem): string[] {
    const patterns: string[] = [];
    
    const followers = data.followersCount || 0;
    const following = data.followsCount || 0;
    const posts = data.postsCount || 0;
    
    if (following / followers > 5) {
      patterns.push('High following-to-followers ratio');
    }
    
    if (posts < 10 && followers > 5000) {
      patterns.push('Low posts with high followers');
    }
    
    if (!data.biography) {
      patterns.push('No bio');
    }
    
    if (!data.profilePicUrl) {
      patterns.push('No profile picture');
    }
    
    const engagement = data.engagementRate || 0;
    if (engagement < 0.5 && followers > 1000) {
      patterns.push('Unusually low engagement rate');
    }
    
    if (engagement > 20) {
      patterns.push('Unusually high engagement rate');
    }
    
    return patterns;
  }

  // Determine niche from bio and posts
  private determineNiche(bio: string, posts: any[]): string {
    const bioLower = bio.toLowerCase();
    const allText = bioLower + ' ' + posts.map(p => p.caption || '').join(' ').toLowerCase();
    
    const niches: Record<string, string[]> = {
      'Fitness': ['fitness', 'gym', 'workout', 'training', 'health', 'muscle', 'fit'],
      'Fashion': ['fashion', 'style', 'outfit', 'wear', 'clothing', 'designer'],
      'Beauty': ['beauty', 'makeup', 'skincare', 'cosmetics', 'hair'],
      'Food': ['food', 'recipe', 'cooking', 'chef', 'restaurant', 'foodie'],
      'Travel': ['travel', 'wanderlust', 'explore', 'adventure', 'destination'],
      'Technology': ['tech', 'technology', 'coding', 'developer', 'programming', 'gadget'],
      'Business': ['entrepreneur', 'business', 'startup', 'ceo', 'founder'],
      'Lifestyle': ['lifestyle', 'life', 'daily', 'blogger'],
      'Photography': ['photo', 'photographer', 'photography', 'camera'],
      'Art': ['art', 'artist', 'creative', 'design', 'illustration'],
      'Music': ['music', 'musician', 'singer', 'producer', 'dj'],
      'Gaming': ['gaming', 'gamer', 'esports', 'twitch', 'streamer'],
    };

    for (const [niche, keywords] of Object.entries(niches)) {
      if (keywords.some(keyword => allText.includes(keyword))) {
        return niche;
      }
    }
    
    return 'General';
  }

  // Normalize username
  private normalizeUsername(username: string): string {
    return username.replace(/^@/, '').trim().toLowerCase();
  }

  // Sleep utility
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Download and convert profile picture to base64
  async fetchProfilePicBase64(url: string): Promise<string | null> {
    if (!url) return null;
    
    try {
      logger.info(`Downloading profile picture: ${url.substring(0, 50)}...`);
      
      const response = await axios.get(url, {
        responseType: 'arraybuffer',
        timeout: 10000,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
          'Referer': 'https://www.instagram.com/',
        },
      });

      const contentType = response.headers['content-type'] || 'image/jpeg';
      const base64 = Buffer.from(response.data).toString('base64');
      const dataUri = `data:${contentType};base64,${base64}`;
      
      logger.info(`Profile picture converted to base64 (${Math.round(base64.length / 1024)}KB)`);
      return dataUri;
    } catch (error) {
      logger.warn('Failed to download profile picture:', error instanceof Error ? error.message : error);
      return null;
    }
  }
}

export const instagramDataService = new InstagramDataService();
