"use client";

import { ReactNode, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { LoaderIcon } from '@/components/icons';
import { useAuthStore } from '@/store/authStore';
import toast from 'react-hot-toast';

interface AuthGuardProps {
  children: ReactNode;
}

export function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter();
  const {
    user,
    accessToken,
    isAuthenticated,
    fetchProfile,
    logout,
  } = useAuthStore();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    let mounted = true;

    const initialize = async () => {
      if (!accessToken) {
        setIsChecking(false);
        router.replace('/login');
        return;
      }

      if (!user && accessToken) {
        try {
          await fetchProfile();
        } catch (error) {
          toast.error('Session expired. Please log in again.');
          await logout();
          router.replace('/login');
          return;
        }
      }

      if (mounted) {
        setIsChecking(false);
      }
    };

    initialize();

    return () => {
      mounted = false;
    };
  }, [accessToken, user, fetchProfile, logout, router]);

  useEffect(() => {
    if (!isChecking && !isAuthenticated) {
      router.replace('/login');
    }
  }, [isChecking, isAuthenticated, router]);

  if (isChecking || !isAuthenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-white text-slate-900">
        <div className="flex flex-col items-center gap-3">
          <LoaderIcon className="h-10 w-10 animate-spin text-primary-500" />
          <p className="text-sm text-slate-500">Securing your workspace...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
