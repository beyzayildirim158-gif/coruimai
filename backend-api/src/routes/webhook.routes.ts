// Webhook Routes
import { Router } from 'express';
import Stripe from 'stripe';
import { prisma } from '../config/database.js';
import { config } from '../config/index.js';
import { logger } from '../utils/logger.js';
import { broadcastAnalysisUpdate } from '../websocket/index.js';

const router = Router();
const stripe = new Stripe(config.stripe.secretKey || '', {
  apiVersion: '2023-10-16',
});

/**
 * Stripe Webhook Handler
 * Handles subscription events from Stripe
 */
router.post('/stripe', async (req, res) => {
  const sig = req.headers['stripe-signature'] as string;
  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      config.stripe.webhookSecret || ''
    );
  } catch (err: any) {
    logger.error('Stripe webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  logger.info(`Stripe webhook received: ${event.type}`);

  try {
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session;
        await handleCheckoutCompleted(session);
        break;
      }

      case 'customer.subscription.created':
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;
        await handleSubscriptionUpdate(subscription);
        break;
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;
        await handleSubscriptionDeleted(subscription);
        break;
      }

      case 'invoice.payment_succeeded': {
        const invoice = event.data.object as Stripe.Invoice;
        await handlePaymentSucceeded(invoice);
        break;
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice;
        await handlePaymentFailed(invoice);
        break;
      }

      default:
        logger.info(`Unhandled Stripe event type: ${event.type}`);
    }

    res.json({ received: true });
  } catch (error) {
    logger.error('Error handling Stripe webhook:', error);
    res.status(500).json({ error: 'Webhook handler failed' });
  }
});

/**
 * Agent Orchestrator Webhook Handler
 * Receives analysis progress updates from the AI agent system
 */
router.post('/analysis-update', async (req, res) => {
  const { 
    analysisId, 
    status, 
    progress, 
    currentAgent, 
    agentResults, 
    eli5Report,
    finalVerdict,
    businessIdentity,
    sanitizationReport,
    hardValidation,
    finalScore,
    finalGrade,
    error 
  } = req.body;

  if (!analysisId) {
    return res.status(400).json({ error: 'analysisId is required' });
  }

  try {
    // Update analysis in database
    const updateData: any = {};

    if (status) updateData.status = status;
    if (progress !== undefined) updateData.progress = progress;
    if (currentAgent) updateData.currentAgent = currentAgent;
    if (error) updateData.errorMessage = error;

    // Combine all results into agentResults for storage
    if (agentResults || eli5Report || finalVerdict || businessIdentity || sanitizationReport || hardValidation) {
      const combinedResults = {
        ...(agentResults || {}),
        ...(eli5Report && { eli5Report }),
        ...(finalVerdict && { finalVerdict }),
        ...(businessIdentity && { businessIdentity }),
        ...(sanitizationReport && { sanitizationReport }),
        ...(hardValidation && { hardValidation }),
      };
      updateData.agentResults = combinedResults;
    }

    // Use finalScore/finalGrade from orchestrator if provided
    if (finalScore !== undefined) {
      updateData.overallScore = finalScore;
    }
    if (finalGrade) {
      updateData.scoreGrade = finalGrade;
    }

    if (status === 'COMPLETED') {
      updateData.completedAt = new Date();
      
      // Use finalScore from orchestrator if available, otherwise calculate from agents
      if (finalScore === undefined && agentResults) {
        const scores = Object.values(agentResults as Record<string, any>)
          .filter((r: any) => r.metrics?.score)
          .map((r: any) => r.metrics.score);
        
        if (scores.length > 0) {
          const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
          updateData.overallScore = avgScore;
          updateData.scoreGrade = getGrade(avgScore);
        }
      }

      // Aggregate recommendations
      if (agentResults) {
        const recommendations = Object.values(agentResults as Record<string, any>)
          .flatMap((r: any) => r.recommendations || [])
          .slice(0, 10);
        updateData.recommendations = recommendations;
      }

      // Update Instagram account
      const analysis = await prisma.analysis.findUnique({
        where: { id: analysisId },
        include: { account: true },
      });

      if (analysis) {
        await prisma.instagramAccount.update({
          where: { id: analysis.accountId },
          data: {
            lastAnalyzedAt: new Date(),
            analysisCount: { increment: 1 },
          },
        });
      }
    }

    await prisma.analysis.update({
      where: { id: analysisId },
      data: updateData,
    });

    // Broadcast update via WebSocket
    broadcastAnalysisUpdate(analysisId, {
      status,
      progress,
      currentAgent,
      error,
    });

    logger.info(`Analysis ${analysisId} updated: ${status} (${progress}%)`);
    res.json({ success: true });
  } catch (error) {
    logger.error('Error handling analysis update:', error);
    res.status(500).json({ error: 'Failed to process update' });
  }
});

// Helper functions
async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId;
  const tier = session.metadata?.tier;

  if (!userId || !tier) {
    logger.warn('Checkout session missing userId or tier in metadata');
    return;
  }

  const subscriptionId = session.subscription as string;

  await prisma.user.update({
    where: { id: userId },
    data: {
      subscriptionTier: tier as any,
      subscriptionStatus: 'ACTIVE',
      stripeSubscriptionId: subscriptionId,
      trialEndsAt: null, // End trial
    },
  });

  logger.info(`User ${userId} upgraded to ${tier}`);
}

async function handleSubscriptionUpdate(subscription: Stripe.Subscription) {
  const userId = subscription.metadata?.userId;
  const tier = subscription.metadata?.tier;

  if (!userId) {
    // Try to find user by customer ID
    const user = await prisma.user.findFirst({
      where: { stripeCustomerId: subscription.customer as string },
    });
    if (!user) return;
  }

  const status = mapStripeStatus(subscription.status);

  await prisma.user.updateMany({
    where: {
      OR: [
        { id: userId || '' },
        { stripeCustomerId: subscription.customer as string },
      ],
    },
    data: {
      subscriptionStatus: status as any,
      stripeSubscriptionId: subscription.id,
      ...(tier && { subscriptionTier: tier as any }),
    },
  });

  logger.info(`Subscription ${subscription.id} updated: ${status}`);
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  await prisma.user.updateMany({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      subscriptionStatus: 'CANCELLED',
      subscriptionTier: 'STARTER', // Downgrade to starter
    },
  });

  logger.info(`Subscription ${subscription.id} cancelled`);
}

async function handlePaymentSucceeded(invoice: Stripe.Invoice) {
  if (!invoice.customer || !invoice.subscription) return;

  const user = await prisma.user.findFirst({
    where: { stripeCustomerId: invoice.customer as string },
  });

  if (!user) return;

  // Record payment
  await prisma.payment.create({
    data: {
      userId: user.id,
      stripePaymentId: invoice.payment_intent as string,
      stripeInvoiceId: invoice.id,
      amount: invoice.amount_paid,
      currency: invoice.currency,
      status: 'SUCCEEDED',
      planType: user.subscriptionTier,
      receiptUrl: invoice.hosted_invoice_url,
      paidAt: new Date(),
    },
  });

  logger.info(`Payment recorded for user ${user.id}: $${invoice.amount_paid / 100}`);
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  if (!invoice.customer) return;

  const user = await prisma.user.findFirst({
    where: { stripeCustomerId: invoice.customer as string },
  });

  if (!user) return;

  // Update subscription status
  await prisma.user.update({
    where: { id: user.id },
    data: { subscriptionStatus: 'PAST_DUE' },
  });

  // Record failed payment
  await prisma.payment.create({
    data: {
      userId: user.id,
      stripeInvoiceId: invoice.id,
      amount: invoice.amount_due,
      currency: invoice.currency,
      status: 'FAILED',
      planType: user.subscriptionTier,
    },
  });

  logger.warn(`Payment failed for user ${user.id}`);
}

function mapStripeStatus(status: Stripe.Subscription.Status): string {
  const statusMap: Record<string, string> = {
    active: 'ACTIVE',
    past_due: 'PAST_DUE',
    canceled: 'CANCELLED',
    trialing: 'TRIALING',
    paused: 'PAUSED',
    unpaid: 'PAST_DUE',
    incomplete: 'PAST_DUE',
    incomplete_expired: 'CANCELLED',
  };
  return statusMap[status] || 'ACTIVE';
}

function getGrade(score: number): string {
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  if (score >= 70) return 'C';
  if (score >= 60) return 'D';
  return 'F';
}

export default router;
