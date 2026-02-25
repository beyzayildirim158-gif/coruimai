// Redis Configuration
import Redis from 'ioredis';
import { config } from './index.js';
import { logger } from '../utils/logger.js';

export const redis = new Redis(config.redisUrl, {
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

redis.on('connect', () => {
  logger.info('Redis connected');
});

redis.on('error', (err) => {
  logger.error('Redis error:', err);
});

redis.on('close', () => {
  logger.warn('Redis connection closed');
});

// Cache helper functions
export const cache = {
  async get<T>(key: string): Promise<T | null> {
    const data = await redis.get(key);
    if (!data) return null;
    try {
      return JSON.parse(data) as T;
    } catch {
      return data as unknown as T;
    }
  },
  
  async set(key: string, value: unknown, ttlSeconds?: number): Promise<void> {
    const data = typeof value === 'string' ? value : JSON.stringify(value);
    if (ttlSeconds) {
      await redis.setex(key, ttlSeconds, data);
    } else {
      await redis.set(key, data);
    }
  },
  
  async del(key: string): Promise<void> {
    await redis.del(key);
  },
  
  async exists(key: string): Promise<boolean> {
    const result = await redis.exists(key);
    return result === 1;
  },
  
  async incr(key: string): Promise<number> {
    return redis.incr(key);
  },
  
  async expire(key: string, seconds: number): Promise<void> {
    await redis.expire(key, seconds);
  },
  
  async ttl(key: string): Promise<number> {
    return redis.ttl(key);
  },
};

export default redis;
