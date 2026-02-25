// WebSocket Handler
import { WebSocketServer, WebSocket } from 'ws';
import jwt from 'jsonwebtoken';
import { config } from '../config/index.js';
import { logger } from '../utils/logger.js';

interface Client {
  ws: WebSocket;
  userId: string;
  analysisId?: string;
}

// Store active connections
const clients: Map<string, Client[]> = new Map();
const analysisSubscriptions: Map<string, Set<WebSocket>> = new Map();

export function setupWebSocket(wss: WebSocketServer): void {
  wss.on('connection', (ws: WebSocket, req) => {
    logger.info('New WebSocket connection');

    let userId: string | null = null;
    let authenticated = false;

    // Handle messages
    ws.on('message', (data) => {
      try {
        const message = JSON.parse(data.toString());

        switch (message.type) {
          case 'auth':
            // Authenticate with JWT
            try {
              const decoded = jwt.verify(message.token, config.jwt.secret) as {
                userId: string;
                type: string;
              };
              
              if (decoded.type !== 'access') {
                ws.send(JSON.stringify({ type: 'auth_error', message: 'Invalid token' }));
                return;
              }

              userId = decoded.userId;
              authenticated = true;

              // Add to clients map
              const userClients = clients.get(userId) || [];
              userClients.push({ ws, userId });
              clients.set(userId, userClients);

              ws.send(JSON.stringify({ type: 'auth_success', userId }));
              logger.info(`WebSocket authenticated for user ${userId}`);
            } catch (error) {
              ws.send(JSON.stringify({ type: 'auth_error', message: 'Authentication failed' }));
            }
            break;

          case 'subscribe_analysis':
            // Subscribe to analysis updates
            if (!authenticated) {
              ws.send(JSON.stringify({ type: 'error', message: 'Not authenticated' }));
              return;
            }

            const { analysisId } = message;
            if (analysisId) {
              const subscribers = analysisSubscriptions.get(analysisId) || new Set();
              subscribers.add(ws);
              analysisSubscriptions.set(analysisId, subscribers);

              ws.send(JSON.stringify({ 
                type: 'subscribed', 
                analysisId,
                message: `Subscribed to analysis ${analysisId}` 
              }));
              logger.info(`User ${userId} subscribed to analysis ${analysisId}`);
            }
            break;

          case 'unsubscribe_analysis':
            // Unsubscribe from analysis updates
            const { analysisId: unsubId } = message;
            if (unsubId) {
              const subscribers = analysisSubscriptions.get(unsubId);
              if (subscribers) {
                subscribers.delete(ws);
                if (subscribers.size === 0) {
                  analysisSubscriptions.delete(unsubId);
                }
              }
              ws.send(JSON.stringify({ type: 'unsubscribed', analysisId: unsubId }));
            }
            break;

          case 'ping':
            ws.send(JSON.stringify({ type: 'pong', timestamp: Date.now() }));
            break;

          default:
            logger.warn(`Unknown WebSocket message type: ${message.type}`);
        }
      } catch (error) {
        logger.error('Error processing WebSocket message:', error);
        ws.send(JSON.stringify({ type: 'error', message: 'Invalid message format' }));
      }
    });

    // Handle close
    ws.on('close', () => {
      if (userId) {
        // Remove from clients
        const userClients = clients.get(userId);
        if (userClients) {
          const index = userClients.findIndex((c) => c.ws === ws);
          if (index > -1) {
            userClients.splice(index, 1);
          }
          if (userClients.length === 0) {
            clients.delete(userId);
          }
        }

        // Remove from analysis subscriptions
        analysisSubscriptions.forEach((subscribers, analysisId) => {
          subscribers.delete(ws);
          if (subscribers.size === 0) {
            analysisSubscriptions.delete(analysisId);
          }
        });

        logger.info(`WebSocket closed for user ${userId}`);
      }
    });

    // Handle errors
    ws.on('error', (error) => {
      logger.error('WebSocket error:', error);
    });

    // Send initial message
    ws.send(JSON.stringify({
      type: 'connected',
      message: 'Connected to Instagram AI WebSocket. Please authenticate.',
      timestamp: Date.now(),
    }));
  });

  // Heartbeat to keep connections alive
  const heartbeatInterval = setInterval(() => {
    wss.clients.forEach((ws) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.ping();
      }
    });
  }, 30000);

  wss.on('close', () => {
    clearInterval(heartbeatInterval);
  });

  logger.info('WebSocket server initialized');
}

// Broadcast analysis update to subscribed clients
export function broadcastAnalysisUpdate(
  analysisId: string,
  update: {
    status?: string;
    progress?: number;
    currentAgent?: string;
    agentResult?: any;
    error?: string;
  }
): void {
  const subscribers = analysisSubscriptions.get(analysisId);
  
  if (!subscribers || subscribers.size === 0) {
    logger.debug(`No subscribers for analysis ${analysisId}`);
    return;
  }

  const message = JSON.stringify({
    type: 'analysis_update',
    analysisId,
    ...update,
    timestamp: Date.now(),
  });

  let delivered = 0;
  subscribers.forEach((ws) => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(message);
      delivered++;
    }
  });

  logger.info(`Broadcast analysis update for ${analysisId} to ${delivered} clients`);
}

// Send message to specific user
export function sendToUser(userId: string, message: any): void {
  const userClients = clients.get(userId);
  
  if (!userClients || userClients.length === 0) {
    return;
  }

  const data = JSON.stringify(message);
  userClients.forEach((client) => {
    if (client.ws.readyState === WebSocket.OPEN) {
      client.ws.send(data);
    }
  });
}

// Get connected client count
export function getConnectedClients(): number {
  let count = 0;
  clients.forEach((userClients) => {
    count += userClients.length;
  });
  return count;
}
