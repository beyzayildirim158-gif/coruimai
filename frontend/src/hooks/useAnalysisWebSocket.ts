"use client";

import { useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { useAnalysisStore } from '@/store/analysisStore';
import toast from 'react-hot-toast';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:3001';

interface UseAnalysisWebSocketOptions {
  onComplete?: (analysisId: string) => void;
  autoNavigate?: boolean;
}

export function useAnalysisWebSocket(
  analysisId?: string,
  options: UseAnalysisWebSocketOptions = { autoNavigate: true }
) {
  const router = useRouter();
  const { accessToken } = useAuthStore();
  const { updateAnalysisProgress, setIsAnalyzing, setCurrentAnalysis, isAnalyzing } = useAnalysisStore();
  const socketRef = useRef<WebSocket | null>(null);
  const hasNavigatedRef = useRef(false);
  const mountedRef = useRef(false);

  // Reset navigation flag when analysisId changes
  useEffect(() => {
    hasNavigatedRef.current = false;
  }, [analysisId]);

  // Memoize options callbacks to prevent effect re-runs
  const onCompleteRef = useRef(options.onComplete);
  const autoNavigateRef = useRef(options.autoNavigate);
  useEffect(() => {
    onCompleteRef.current = options.onComplete;
    autoNavigateRef.current = options.autoNavigate;
  }, [options.onComplete, options.autoNavigate]);

  const connectWebSocket = useCallback(() => {
    // Guard: don't connect if no analysisId or token
    if (!analysisId || !accessToken) {
      return;
    }

    // Guard: don't connect if already connected/connecting
    if (socketRef.current?.readyState === WebSocket.OPEN ||
        socketRef.current?.readyState === WebSocket.CONNECTING) {
      return;
    }

    const ws = new WebSocket(`${WS_URL}/ws`);
    socketRef.current = ws;

    ws.onopen = () => {
      ws.send(JSON.stringify({ type: 'auth', token: accessToken }));
      ws.send(JSON.stringify({ type: 'subscribe_analysis', analysisId }));
    };

    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.type === 'analysis_update' && payload.analysisId === analysisId) {
          updateAnalysisProgress({
            status: payload.status,
            progress: payload.progress ?? 0,
            currentAgent: payload.currentAgent,
            completedAgents: payload.completedAgents ?? [],
            agentResults: payload.agentResult ? payload.agentResult : undefined,
          });

          // Handle completion
          if (payload.status === 'COMPLETED' && !hasNavigatedRef.current) {
            hasNavigatedRef.current = true;
            setIsAnalyzing(false);
            toast.success('Analysis completed! Redirecting to results...');
            
            if (onCompleteRef.current) {
              onCompleteRef.current(analysisId);
            }
            
            if (autoNavigateRef.current !== false) {
              setTimeout(() => {
                setCurrentAnalysis(null);
                router.push(`/analysis/${analysisId}`);
              }, 500);
            }
          }

          // Handle failure
          if (payload.status === 'FAILED' && !hasNavigatedRef.current) {
            hasNavigatedRef.current = true;
            setIsAnalyzing(false);
            toast.error(payload.errorMessage || 'Analysis failed. Please try again.');
          }
        }
      } catch (error) {
        // swallow parse errors
      }
    };

    ws.onerror = () => {
      // Error handling - socket will close automatically
    };

    ws.onclose = () => {
      socketRef.current = null;
    };
  }, [analysisId, accessToken, updateAnalysisProgress, setIsAnalyzing, setCurrentAnalysis, router]);

  // Only connect when isAnalyzing becomes true with a valid analysisId
  useEffect(() => {
    mountedRef.current = true;
    
    if (isAnalyzing && analysisId && accessToken) {
      connectWebSocket();
    }

    return () => {
      mountedRef.current = false;
      if (socketRef.current) {
        if (socketRef.current.readyState === WebSocket.OPEN) {
          socketRef.current.send(
            JSON.stringify({
              type: 'unsubscribe_analysis',
              analysisId,
            })
          );
        }
        socketRef.current.close();
        socketRef.current = null;
      }
    };
  }, [isAnalyzing, analysisId, accessToken, connectWebSocket]);
}
