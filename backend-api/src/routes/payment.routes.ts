// Payment Routes - Stripe Integration
import { Router } from 'express';
import Stripe from 'stripe';
import { prisma } from '../config/database.js';
import { config, tierLimits } from '../config/index.js';
import { authenticate } from '../middleware/auth.js';
import { asyncHandler } from '../utils/asyncHandler.js';
import { BadRequestError, NotFoundError } from '../utils/errors.js';
import { logger } from '../utils/logger.js';

const router = Router();
const stripe = new Stripe(config.stripe.secretKey, {
  apiVersion: '2023-10-16',
});

// Price IDs mapping
const priceIds: Record<string, string> = {
  STARTER: config.stripe.prices.starter,
  PROFESSIONAL: config.stripe.prices.professional,
  PREMIUM: config.stripe.prices.premium,
  ENTERPRISE: config.stripe.prices.enterprise,
};

/**
 * @swagger
 * /api/payments/create-checkout:
 *   post:
 *     summary: Create Stripe checkout session
 *     tags: [Payments]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [tier]
 *             properties:
 *               tier:
 *                 type: string
 *                 enum: [STARTER, PROFESSIONAL, PREMIUM, ENTERPRISE]
 *     responses:
 *       200:
 *         description: Checkout session created
 */
router.post(
  '/create-checkout',
  authenticate,
  asyncHandler(async (req, res) => {
    const { tier } = req.body;
    const userId = req.user!.id;

    if (!tier || !priceIds[tier]) {
      throw new BadRequestError('Invalid subscription tier');
    }

    // Get user
    const user = await prisma.user.findUnique({
      where: { id: userId },
    });

    if (!user) {
      throw new NotFoundError('User not found');
    }

    // Create or get Stripe customer
    let customerId = user.stripeCustomerId;

    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.email,
        name: user.name,
        metadata: {
          userId: user.id,
        },
      });
      customerId = customer.id;

      await prisma.user.update({
        where: { id: userId },
        data: { stripeCustomerId: customerId },
      });
    }

    // Create checkout session
    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceIds[tier],
          quantity: 1,
        },
      ],
      success_url: `${process.env.APP_URL}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.APP_URL}/pricing`,
      metadata: {
        userId,
        tier,
      },
      subscription_data: {
        metadata: {
          userId,
          tier,
        },
      },
      allow_promotion_codes: true,
    });

    res.json({
      success: true,
      data: {
        checkoutUrl: session.url,
        sessionId: session.id,
      },
    });
  })
);

/**
 * @swagger
 * /api/payments/portal:
 *   get:
 *     summary: Get Stripe customer portal URL
 *     tags: [Payments]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Portal URL
 */
router.get(
  '/portal',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;

    const user = await prisma.user.findUnique({
      where: { id: userId },
    });

    if (!user?.stripeCustomerId) {
      throw new BadRequestError('No billing information found');
    }

    const session = await stripe.billingPortal.sessions.create({
      customer: user.stripeCustomerId,
      return_url: `${process.env.APP_URL}/settings/billing`,
    });

    res.json({
      success: true,
      data: {
        portalUrl: session.url,
      },
    });
  })
);

/**
 * @swagger
 * /api/payments/subscription:
 *   get:
 *     summary: Get current subscription details
 *     tags: [Payments]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Subscription details
 */
router.get(
  '/subscription',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;

    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: {
        subscriptionTier: true,
        subscriptionStatus: true,
        stripeSubscriptionId: true,
        trialEndsAt: true,
      },
    });

    if (!user) {
      throw new NotFoundError('User not found');
    }

    let subscription = null;

    if (user.stripeSubscriptionId) {
      try {
        const stripeSub = await stripe.subscriptions.retrieve(user.stripeSubscriptionId);
        subscription = {
          id: stripeSub.id,
          status: stripeSub.status,
          currentPeriodStart: new Date(stripeSub.current_period_start * 1000),
          currentPeriodEnd: new Date(stripeSub.current_period_end * 1000),
          cancelAtPeriodEnd: stripeSub.cancel_at_period_end,
        };
      } catch (error) {
        logger.error('Failed to fetch Stripe subscription:', error);
      }
    }

    const tierConfig = tierLimits[user.subscriptionTier as keyof typeof tierLimits];

    res.json({
      success: true,
      data: {
        tier: user.subscriptionTier,
        status: user.subscriptionStatus,
        trialEndsAt: user.trialEndsAt,
        subscription,
        limits: {
          analysesPerMonth: tierConfig.analysesPerMonth,
          requestsPerHour: tierConfig.requestsPerHour,
          agentCount: tierConfig.agentCount,
        },
        features: tierConfig.features,
      },
    });
  })
);

/**
 * @swagger
 * /api/payments/invoices:
 *   get:
 *     summary: Get payment history
 *     tags: [Payments]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Invoice list
 */
router.get(
  '/invoices',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;

    const user = await prisma.user.findUnique({
      where: { id: userId },
    });

    if (!user?.stripeCustomerId) {
      return res.json({
        success: true,
        data: [],
      });
    }

    const invoices = await stripe.invoices.list({
      customer: user.stripeCustomerId,
      limit: 20,
    });

    const formattedInvoices = invoices.data.map((invoice) => ({
      id: invoice.id,
      number: invoice.number,
      amount: invoice.amount_paid / 100,
      currency: invoice.currency.toUpperCase(),
      status: invoice.status,
      paidAt: invoice.status_transitions?.paid_at
        ? new Date(invoice.status_transitions.paid_at * 1000)
        : null,
      pdfUrl: invoice.invoice_pdf,
      hostedUrl: invoice.hosted_invoice_url,
    }));

    res.json({
      success: true,
      data: formattedInvoices,
    });
  })
);

/**
 * @swagger
 * /api/payments/cancel:
 *   post:
 *     summary: Cancel subscription
 *     tags: [Payments]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Subscription cancelled
 */
router.post(
  '/cancel',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;

    const user = await prisma.user.findUnique({
      where: { id: userId },
    });

    if (!user?.stripeSubscriptionId) {
      throw new BadRequestError('No active subscription found');
    }

    // Cancel at period end
    await stripe.subscriptions.update(user.stripeSubscriptionId, {
      cancel_at_period_end: true,
    });

    res.json({
      success: true,
      message: 'Subscription will be cancelled at the end of the billing period',
    });
  })
);

/**
 * @swagger
 * /api/payments/resume:
 *   post:
 *     summary: Resume cancelled subscription
 *     tags: [Payments]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Subscription resumed
 */
router.post(
  '/resume',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;

    const user = await prisma.user.findUnique({
      where: { id: userId },
    });

    if (!user?.stripeSubscriptionId) {
      throw new BadRequestError('No subscription found');
    }

    await stripe.subscriptions.update(user.stripeSubscriptionId, {
      cancel_at_period_end: false,
    });

    res.json({
      success: true,
      message: 'Subscription resumed',
    });
  })
);

export default router;
