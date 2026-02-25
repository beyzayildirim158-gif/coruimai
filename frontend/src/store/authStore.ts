import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import api from '@/lib/api';
import type { SubscriptionTier, SubscriptionStatus } from '@/types/shared';

interface User {
  id: string;
  email: string;
  name: string;
  avatarUrl?: string | null;
  emailVerified: boolean;
  subscriptionTier: SubscriptionTier;
  subscriptionStatus: SubscriptionStatus;
  trialEndsAt?: string | null;
  createdAt: string;
  lastLoginAt?: string | null;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
  fetchProfile: () => Promise<void>;
  clearError: () => void;
  setUser: (user: User) => void;
  setAccessToken: (token: string | null) => void;
}

interface RegisterData {
  email: string;
  password: string;
  name: string;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const response = await api.post('/auth/login', { email, password });
          const { user, tokens } = response.data.data;
          
          set({
            user,
            accessToken: tokens.accessToken,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: any) {
          set({
            error: error.response?.data?.message || 'Login failed',
            isLoading: false,
          });
          throw error;
        }
      },

      register: async (data: RegisterData) => {
        set({ isLoading: true, error: null });
        try {
          const response = await api.post('/auth/register', data);
          const { user, tokens } = response.data.data;
          
          set({
            user,
            accessToken: tokens.accessToken,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error: any) {
          set({
            error: error.response?.data?.message || 'Registration failed',
            isLoading: false,
          });
          throw error;
        }
      },

      logout: async () => {
        try {
          await api.post('/auth/logout');
        } catch (error) {
          // Ignore logout errors
        } finally {
          set({
            user: null,
            accessToken: null,
            isAuthenticated: false,
          });
        }
      },

      refreshToken: async () => {
        try {
          const response = await api.post('/auth/refresh');
          const { accessToken } = response.data.data;
          set({ accessToken });
        } catch (error) {
          // If refresh fails, logout
          get().logout();
        }
      },

      fetchProfile: async () => {
        try {
          const response = await api.get('/users/profile');
          set({ user: response.data.data, isAuthenticated: true });
        } catch (error) {
          // ignore, handled by guard
        }
      },

      clearError: () => set({ error: null }),
      
      setUser: (user: User) => set({ user }),
      
      setAccessToken: (token) => set({ accessToken: token, isAuthenticated: !!token }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
