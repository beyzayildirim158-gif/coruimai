// Redis Configuration
import Redis from 'ioredis';
import { config } from './index.js';
import { logger } from '../utils/logger.js';

// Create Redis client only if URL is provided
const createRedisClient = () => {
  if (!config.redisUrl) {
    logger.warn('Redis URL not configured - using in-memory fallback (not for production)');
    return null;
  }
  
  return new Redis(config.redisUrl, {
    maxRetriesPerRequest: 3,
    retryStrategy: (times) => {
      if (times > 3) {
        logger.error('Redis connection failed after 3 retries');
        return null;
      }
      return Math.min(times * 100, 3000);
    },
    reconnectOnError: (err) => {
      const targetErrors = ['READONLY', 'ECONNRESET', 'ETIMEDOUT'];
      return targetErrors.some((e) => err.message.includes(e));
    },
  });
};

export const redis = createRedisClient();

// In-memory cache fallback when Redis is not available
const memoryCache = new Map<string, { value: string; expires?: number }>();

if (redis) {
  redis.on('connect', () => {
    logger.info('Redis connected');
  });

  redis.on('error', (err) => {
    logger.error('Redis error:', err);
  });

  redis.on('close', () => {
    logger.warn('Redis connection closed');
  });
}

// Cache helper functions
export const cache = {
  async get<T>(key: string): Promise<T | null> {
    // Use Redis if available, otherwise memory cache
    if (redis) {
      const data = await redis.get(key);
      if (!data) return null;
      try {
        return JSON.parse(data) as T;
      } catch {
        return data as unknown as T;
      }
    }
    // Memory fallback
    const entry = memoryCache.get(key);
    if (!entry) return null;
    if (entry.expires && Date.now() > entry.expires) {
      memoryCache.delete(key);
      return null;
    }
    try {
      return JSON.parse(entry.value) as T;
    } catch {
      return entry.value as unknown as T;
    }
  },
  
  async set(key: string, value: unknown, ttlSeconds?: number): Promise<void> {
    const data = typeof value === 'string' ? value : JSON.stringify(value);
    if (redis) {
      if (ttlSeconds) {
        await redis.setex(key, ttlSeconds, data);
      } else {
        await redis.set(key, data);
      }
    } else {
      // Memory fallback
      memoryCache.set(key, {
        value: data,
        expires: ttlSeconds ? Date.now() + ttlSeconds * 1000 : undefined,
      });
    }
  },
  
  async del(key: string): Promise<void> {
    if (redis) {
      await redis.del(key);
    } else {
      memoryCache.delete(key);
    }
  },
  
  async exists(key: string): Promise<boolean> {
    if (redis) {
      const result = await redis.exists(key);
      return result === 1;
    }
    const entry = memoryCache.get(key);
    if (!entry) return false;
    if (entry.expires && Date.now() > entry.expires) {
      memoryCache.delete(key);
      return false;
    }
    return true;
  },
  
  async incr(key: string): Promise<number> {
    if (redis) {
      return redis.incr(key);
    }
    const entry = memoryCache.get(key);
    const current = entry ? parseInt(entry.value, 10) || 0 : 0;
    const newVal = current + 1;
    memoryCache.set(key, { value: String(newVal), expires: entry?.expires });
    return newVal;
  },
  
  async expire(key: string, seconds: number): Promise<void> {
    if (redis) {
      await redis.expire(key, seconds);
    } else {
      const entry = memoryCache.get(key);
      if (entry) {
        entry.expires = Date.now() + seconds * 1000;
      }
    }
  },
  
  async ttl(key: string): Promise<number> {
    if (redis) {
      return redis.ttl(key);
    }
    const entry = memoryCache.get(key);
    if (!entry || !entry.expires) return -1;
    return Math.max(0, Math.floor((entry.expires - Date.now()) / 1000));
  },

  // Helper to check if Redis is connected
  isConnected(): boolean {
    return redis !== null && redis.status === 'ready';
  },

  // Ping for health check
  async ping(): Promise<string> {
    if (redis) {
      return redis.ping();
    }
    return 'PONG (memory)';
  },
};

export default redis;
