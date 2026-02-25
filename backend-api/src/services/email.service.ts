// Email Service
import nodemailer from 'nodemailer';
import { config } from '../config/index.js';
import { logger } from '../utils/logger.js';

class EmailService {
  private transporter: nodemailer.Transporter;

  constructor() {
    this.transporter = nodemailer.createTransport({
      host: config.email.host,
      port: config.email.port,
      secure: config.email.port === 465,
      auth: {
        user: config.email.user,
        pass: config.email.password,
      },
    });
  }

  async sendVerificationEmail(
    email: string,
    name: string,
    token: string
  ): Promise<void> {
    const verificationUrl = `${process.env.APP_URL}/verify-email?token=${token}`;

    const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { text-align: center; padding: 20px 0; }
    .logo { font-size: 24px; font-weight: bold; color: #6366f1; }
    .content { background: #f9fafb; padding: 30px; border-radius: 10px; }
    .button { display: inline-block; background: #6366f1; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }
    .footer { text-align: center; padding: 20px; font-size: 12px; color: #666; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="logo">Instagram AI</div>
    </div>
    <div class="content">
      <h2>Verify Your Email</h2>
      <p>Hi ${name},</p>
      <p>Thank you for signing up for Instagram AI Management System. Please verify your email address by clicking the button below:</p>
      <p style="text-align: center;">
        <a href="${verificationUrl}" class="button">Verify Email</a>
      </p>
      <p>Or copy and paste this link in your browser:</p>
      <p style="word-break: break-all; color: #6366f1;">${verificationUrl}</p>
      <p>This link will expire in 24 hours.</p>
    </div>
    <div class="footer">
      <p>If you didn't create an account, you can safely ignore this email.</p>
      <p>© ${new Date().getFullYear()} Instagram AI Management System</p>
    </div>
  </div>
</body>
</html>
    `;

    await this.sendEmail({
      to: email,
      subject: 'Verify your email - Instagram AI',
      html,
    });
  }

  async sendPasswordResetEmail(
    email: string,
    name: string,
    token: string
  ): Promise<void> {
    const resetUrl = `${process.env.APP_URL}/reset-password?token=${token}`;

    const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { text-align: center; padding: 20px 0; }
    .logo { font-size: 24px; font-weight: bold; color: #6366f1; }
    .content { background: #f9fafb; padding: 30px; border-radius: 10px; }
    .button { display: inline-block; background: #6366f1; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }
    .footer { text-align: center; padding: 20px; font-size: 12px; color: #666; }
    .warning { background: #fef3c7; padding: 15px; border-radius: 6px; margin: 15px 0; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="logo">Instagram AI</div>
    </div>
    <div class="content">
      <h2>Reset Your Password</h2>
      <p>Hi ${name},</p>
      <p>We received a request to reset your password. Click the button below to create a new password:</p>
      <p style="text-align: center;">
        <a href="${resetUrl}" class="button">Reset Password</a>
      </p>
      <p>Or copy and paste this link in your browser:</p>
      <p style="word-break: break-all; color: #6366f1;">${resetUrl}</p>
      <div class="warning">
        <strong>⚠️ This link will expire in 1 hour.</strong>
      </div>
    </div>
    <div class="footer">
      <p>If you didn't request a password reset, please ignore this email or contact support if you have concerns.</p>
      <p>© ${new Date().getFullYear()} Instagram AI Management System</p>
    </div>
  </div>
</body>
</html>
    `;

    await this.sendEmail({
      to: email,
      subject: 'Reset your password - Instagram AI',
      html,
    });
  }

  async sendWelcomeEmail(email: string, name: string): Promise<void> {
    const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { text-align: center; padding: 20px 0; }
    .logo { font-size: 24px; font-weight: bold; color: #6366f1; }
    .content { background: #f9fafb; padding: 30px; border-radius: 10px; }
    .button { display: inline-block; background: #6366f1; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }
    .feature { padding: 15px 0; border-bottom: 1px solid #e5e7eb; }
    .feature:last-child { border-bottom: none; }
    .footer { text-align: center; padding: 20px; font-size: 12px; color: #666; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="logo">Instagram AI</div>
    </div>
    <div class="content">
      <h2>Welcome to Instagram AI! 🎉</h2>
      <p>Hi ${name},</p>
      <p>Thank you for joining Instagram AI Management System. We're excited to help you grow your Instagram presence with our 7 AI-powered agents!</p>
      
      <h3>What you can do:</h3>
      <div class="feature">
        <strong>📊 Analyze Instagram Accounts</strong>
        <p>Get comprehensive insights from our 7 specialized AI agents.</p>
      </div>
      <div class="feature">
        <strong>📈 Track Growth Potential</strong>
        <p>Understand your viral potential and growth opportunities.</p>
      </div>
      <div class="feature">
        <strong>📄 Generate PDF Reports</strong>
        <p>Create professional reports to share with clients or team.</p>
      </div>
      
      <p style="text-align: center;">
        <a href="${process.env.APP_URL}/dashboard" class="button">Go to Dashboard</a>
      </p>
    </div>
    <div class="footer">
      <p>Questions? Reply to this email or visit our help center.</p>
      <p>© ${new Date().getFullYear()} Instagram AI Management System</p>
    </div>
  </div>
</body>
</html>
    `;

    await this.sendEmail({
      to: email,
      subject: 'Welcome to Instagram AI! 🎉',
      html,
    });
  }

  async sendAnalysisCompleteEmail(
    email: string,
    name: string,
    username: string,
    analysisId: string
  ): Promise<void> {
    const reportUrl = `${process.env.APP_URL}/reports/${analysisId}`;

    const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { text-align: center; padding: 20px 0; }
    .logo { font-size: 24px; font-weight: bold; color: #6366f1; }
    .content { background: #f9fafb; padding: 30px; border-radius: 10px; }
    .button { display: inline-block; background: #6366f1; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }
    .footer { text-align: center; padding: 20px; font-size: 12px; color: #666; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="logo">Instagram AI</div>
    </div>
    <div class="content">
      <h2>Analysis Complete! ✅</h2>
      <p>Hi ${name},</p>
      <p>Your analysis for <strong>@${username}</strong> is complete!</p>
      <p>Our 7 AI agents have finished analyzing the account and generated comprehensive insights including:</p>
      <ul>
        <li>Bot detection & account health</li>
        <li>Growth strategy recommendations</li>
        <li>Content optimization tips</li>
        <li>Monetization opportunities</li>
        <li>And much more...</li>
      </ul>
      <p style="text-align: center;">
        <a href="${reportUrl}" class="button">View Full Report</a>
      </p>
    </div>
    <div class="footer">
      <p>© ${new Date().getFullYear()} Instagram AI Management System</p>
    </div>
  </div>
</body>
</html>
    `;

    await this.sendEmail({
      to: email,
      subject: `Analysis Complete: @${username} - Instagram AI`,
      html,
    });
  }

  private async sendEmail(options: {
    to: string;
    subject: string;
    html: string;
  }): Promise<void> {
    try {
      await this.transporter.sendMail({
        from: `"Instagram AI" <${config.email.from}>`,
        to: options.to,
        subject: options.subject,
        html: options.html,
      });
      logger.info(`Email sent to ${options.to}: ${options.subject}`);
    } catch (error) {
      logger.error('Failed to send email:', error);
      throw error;
    }
  }
}

export const emailService = new EmailService();
