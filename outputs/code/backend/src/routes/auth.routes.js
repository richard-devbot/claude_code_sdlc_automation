'use strict';

const express = require('express');
const router = express.Router();
const authController = require('../controllers/auth.controller');
const { authenticate } = require('../middleware/auth.middleware');
const { auditLog } = require('../middleware/audit.middleware');
const rateLimit = require('express-rate-limit');

// ---------------------------------------------------------------------------
// Auth-specific rate limiter (stricter than global)
// 10 requests per minute per IP on auth endpoints (NFR-020)
// ---------------------------------------------------------------------------
const authLimiter = rateLimit({
  windowMs: parseInt(process.env.AUTH_RATE_LIMIT_WINDOW_MS, 10) || 60000,
  max: parseInt(process.env.AUTH_RATE_LIMIT_MAX_REQUESTS, 10) || 10,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: 'Too many authentication attempts. Please try again later.',
  },
});

// ---------------------------------------------------------------------------
// Public routes (no authentication required)
// ---------------------------------------------------------------------------

/**
 * POST /api/auth/register
 * Register a new user account
 */
router.post(
  '/register',
  authLimiter,
  auditLog('REGISTER', 'user'),
  authController.register
);

/**
 * POST /api/auth/login
 * Authenticate with email + password, returns JWT tokens
 */
router.post(
  '/login',
  authLimiter,
  auditLog('LOGIN', 'session'),
  authController.login
);

/**
 * POST /api/auth/refresh
 * Exchange a valid refresh token for a new access token
 */
router.post(
  '/refresh',
  authLimiter,
  authController.refreshToken
);

// ---------------------------------------------------------------------------
// Protected routes (authentication required)
// ---------------------------------------------------------------------------

/**
 * POST /api/auth/2fa/setup
 * Generate a TOTP secret + QR code for 2FA enrolment
 */
router.post(
  '/2fa/setup',
  authenticate,
  auditLog('2FA_SETUP', 'user'),
  authController.setup2FA
);

/**
 * POST /api/auth/2fa/verify
 * Verify a TOTP code to complete 2FA enrolment or login
 */
router.post(
  '/2fa/verify',
  authLimiter,
  authController.verify2FA
);

/**
 * POST /api/auth/logout
 * Invalidate refresh token and end the session
 */
router.post(
  '/logout',
  authenticate,
  auditLog('LOGOUT', 'session'),
  authController.logout
);

/**
 * GET /api/auth/me
 * Return the authenticated user's profile
 */
router.get(
  '/me',
  authenticate,
  authController.getProfile
);

module.exports = router;
