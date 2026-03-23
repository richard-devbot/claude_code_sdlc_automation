'use strict';

const jwt = require('jsonwebtoken');
const db = require('../config/database');

// ---------------------------------------------------------------------------
// JWT access-token secret (must be set in environment)
// ---------------------------------------------------------------------------
const JWT_ACCESS_SECRET = process.env.JWT_ACCESS_SECRET || 'CHANGE_ME_IN_ENV';

// ---------------------------------------------------------------------------
// authenticate — verifies the JWT access token from the Authorization header
// ---------------------------------------------------------------------------
/**
 * Express middleware that verifies a Bearer JWT access token.
 * On success it attaches `req.user` with { id, email, roles }.
 */
const authenticate = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        success: false,
        error: 'Authentication required. Provide a Bearer token.',
      });
    }

    const token = authHeader.split(' ')[1];

    let decoded;
    try {
      decoded = jwt.verify(token, JWT_ACCESS_SECRET);
    } catch (err) {
      if (err.name === 'TokenExpiredError') {
        return res.status(401).json({
          success: false,
          error: 'Token expired. Please refresh your token.',
          code: 'TOKEN_EXPIRED',
        });
      }
      return res.status(401).json({
        success: false,
        error: 'Invalid token.',
      });
    }

    // Ensure the user still exists and is active
    const userResult = await db.query(
      `SELECT u.id, u.email, u.first_name, u.last_name, u.is_active, u.client_id,
              COALESCE(array_agg(r.name) FILTER (WHERE r.name IS NOT NULL), '{}') AS roles
       FROM users u
       LEFT JOIN user_roles ur ON ur.user_id = u.id
       LEFT JOIN roles r ON r.id = ur.role_id
       WHERE u.id = $1 AND u.deleted_at IS NULL
       GROUP BY u.id`,
      [decoded.sub]
    );

    if (userResult.rows.length === 0) {
      return res.status(401).json({
        success: false,
        error: 'User account not found.',
      });
    }

    const user = userResult.rows[0];

    if (!user.is_active) {
      return res.status(403).json({
        success: false,
        error: 'User account is deactivated.',
      });
    }

    // Attach user context to the request
    req.user = {
      id: user.id,
      email: user.email,
      firstName: user.first_name,
      lastName: user.last_name,
      roles: user.roles,
      clientId: user.client_id,
    };

    next();
  } catch (err) {
    console.error('Auth middleware error:', err);
    return res.status(500).json({
      success: false,
      error: 'Internal authentication error.',
    });
  }
};

// ---------------------------------------------------------------------------
// authorize — checks that the authenticated user has one of the allowed roles
// ---------------------------------------------------------------------------
/**
 * Returns an Express middleware that verifies the user has at least one of
 * the specified roles.  Must be placed AFTER `authenticate`.
 *
 * @param  {...string} allowedRoles  Role names (e.g. 'admin', 'pm')
 *                                   Pass '*' to allow any authenticated user.
 * @returns {Function} Express middleware
 */
const authorize = (...allowedRoles) => {
  return (req, res, next) => {
    // If wildcard, any authenticated user is permitted
    if (allowedRoles.includes('*')) {
      return next();
    }

    if (!req.user || !req.user.roles) {
      return res.status(403).json({
        success: false,
        error: 'Forbidden. No roles assigned.',
      });
    }

    const hasRole = req.user.roles.some((role) => allowedRoles.includes(role));
    if (!hasRole) {
      return res.status(403).json({
        success: false,
        error: `Forbidden. Required roles: ${allowedRoles.join(', ')}`,
      });
    }

    next();
  };
};

// ---------------------------------------------------------------------------
// optionalAuth — same as authenticate but does NOT reject if no token
// ---------------------------------------------------------------------------
/**
 * If a valid token is present, `req.user` is populated.
 * If no token is present the request continues without `req.user`.
 */
const optionalAuth = async (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return next();
  }
  // Delegate to full authenticate
  return authenticate(req, res, next);
};

module.exports = {
  authenticate,
  authorize,
  optionalAuth,
};
