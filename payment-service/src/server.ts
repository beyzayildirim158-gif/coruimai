import express from 'express';
import Stripe from 'stripe';
import { config } from './config.js';
import { logger } from './logger.js';
import { prisma } from './prisma.js';

const stripe = new Stripe(config.stripeSecretKey, {
  apiVersion: '2023-10-16',
});

const app = express();

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'payment-service' });
});

app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const signature = req.headers['stripe-signature'] as string;
  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(req.body, signature, config.stripeWebhookSecret);
  } catch (error: any) {
    logger.error({ error }, 'Stripe signature verification failed');
    return res.status(400).send(`Webhook Error: ${error.message}`);
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutCompleted(event.data.object as Stripe.Checkout.Session);
        break;
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
        await handleSubscriptionUpdate(event.data.object as Stripe.Subscription);
        break;
      case 'customer.subscription.deleted':
        await handleSubscriptionDeleted(event.data.object as Stripe.Subscription);
        break;
      case 'invoice.payment_succeeded':
        await handlePaymentSucceeded(event.data.object as Stripe.Invoice);
        break;
      case 'invoice.payment_failed':
        await handlePaymentFailed(event.data.object as Stripe.Invoice);
        break;
      default:
        logger.info({ type: event.type }, 'Unhandled Stripe event');
    }
    res.json({ received: true });
  } catch (error) {
    logger.error({ error }, 'Stripe webhook handler failed');
    res.status(500).json({ error: 'Webhook handler failed' });
  }
});

app.listen(config.port, () => {
  logger.info(`Payment service listening on port ${config.port}`);
});

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId;
  const tier = session.metadata?.tier;
  if (!userId || !tier) {
    logger.warn('Checkout metadata missing userId or tier');
    return;
  }

  await prisma.user.update({
    where: { id: userId },
    data: {
      subscriptionTier: tier as any,
      subscriptionStatus: 'ACTIVE',
      stripeSubscriptionId: session.subscription as string,
      trialEndsAt: null,
    },
  });

  logger.info({ userId, tier }, 'Checkout completed');
}

async function handleSubscriptionUpdate(subscription: Stripe.Subscription) {
  const userId = subscription.metadata?.userId;
  const tier = subscription.metadata?.tier;

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

  const status = statusMap[subscription.status] || 'ACTIVE';

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

  logger.info({ subscriptionId: subscription.id, status }, 'Subscription updated');
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  await prisma.user.updateMany({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      subscriptionStatus: 'CANCELLED',
      subscriptionTier: 'STARTER',
    },
  });

  logger.info({ subscriptionId: subscription.id }, 'Subscription cancelled');
}

async function handlePaymentSucceeded(invoice: Stripe.Invoice) {
  if (!invoice.customer || !invoice.payment_intent) return;

  const user = await prisma.user.findFirst({
    where: { stripeCustomerId: invoice.customer as string },
  });
  if (!user) return;

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
      paidAt: invoice.status_transitions?.paid_at
        ? new Date(invoice.status_transitions.paid_at * 1000)
        : new Date(),
    },
  });

  logger.info({ invoiceId: invoice.id }, 'Payment succeeded');
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  if (!invoice.customer) return;

  const user = await prisma.user.findFirst({
    where: { stripeCustomerId: invoice.customer as string },
  });
  if (!user) return;

  await prisma.user.update({
    where: { id: user.id },
    data: { subscriptionStatus: 'PAST_DUE' },
  });

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

  logger.warn({ invoiceId: invoice.id }, 'Payment failed');
}
