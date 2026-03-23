'use strict';

const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
const speakeasy = require('speakeasy');
const QRCode = require('qrcode');
const db = require('../config/database');
const { writeAuditLog, getClientIp } = require('../middleware/audit.middleware');

// ---------------------------------------------------------------------------
// Environment configuration
// ---------------------------------------------------------------------------
const JWT_ACCESS_SECRET = process.env.JWT_ACCESS_SECRET || 'CHANGE_ME_IN_ENV';
const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'CHANGE_ME_IN_ENV_REFRESH';
const JWT_ACCESS_EXPIRY = process.env.JWT_ACCESS_EXPIRY || '15m';
const JWT_REFRESH_EXPIRY = process.env.JWT_REFRESH_EXPIRY || '7d';
const BCRYPT_SALT_ROUNDS = parseInt(process.env.BCRYPT_SALT_ROUNDS, 10) || 12;
const TOTP_ISSUER = process.env.TOTP_ISSUER || 'TechNova Platform';
const LOCKOUT_THRESHOLD = parseInt(process.env.ACCOUNT_LOCKOUT_THRESHOLD, 10) || 5;
const LOCKOUT_DURATION_MS = parseInt(process.env.ACCOUNT_LOCKOUT_DURATION_MS, 10) || 900000;

// ---------------------------------------------------------------------------
// Helper — generate token pair
// ---------------------------------------------------------------------------
const generateTokens = (user) => {
  const accessToken = jwt.sign(
    {
      sub: user.id,
      email: user.email,
      roles: user.roles,
    },
    JWT_ACCESS_SECRET,
    { expiresIn: JWT_ACCESS_EXPIRY }
  );

  const refreshToken = jwt.sign(
    { sub: user.id, type: 'refresh' },
    JWT_REFRESH_SECRET,
    { expiresIn: JWT_REFRESH_EXPIRY }
  );

  return { accessToken, refreshToken };
};

// ---------------------------------------------------------------------------
// Helper — validate email format
// ---------------------------------------------------------------------------
const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

// ---------------------------------------------------------------------------
// Helper — validate password strength (min 12 chars, complexity)
// ---------------------------------------------------------------------------
const isStrongPassword = (password) => {
  if (password.length < 12) return false;
  if (!/[A-Z]/.test(password)) return false;
  if (!/[a-z]/.test(password)) return false;
  if (!/[0-9]/.test(password)) return false;
  if (!/[^A-Za-z0-9]/.test(password)) return false;
  return true;
};

// ---------------------------------------------------------------------------
// In-memory login-attempt tracker (use Redis in production)
// ---------------------------------------------------------------------------
const loginAttempts = new Map();

const checkAccountLockout = (email) => {
  const attempts = loginAttempts.get(email);
  if (!attempts) return false;
  if (attempts.count >= LOCKOUT_THRESHOLD) {
    const elapsed = Date.now() - attempts.lastAttempt;
    if (elapsed < LOCKOUT_DURATION_MS) {
      return true; // still locked
    }
    // Lockout expired — reset
    loginAttempts.delete(email);
    return false;
  }
  return false;
};

const recordFailedAttempt = (email) => {
  const attempts = loginAttempts.get(email) || { count: 0, lastAttempt: 0 };
  attempts.count += 1;
  attempts.lastAttempt = Date.now();
  loginAttempts.set(email, attempts);
};

const clearFailedAttempts = (email) => {
  loginAttempts.delete(email);
};

// ---------------------------------------------------------------------------
// POST /api/auth/register
// ---------------------------------------------------------------------------
const register = async (req, res) => {
  try {
    const { email, password, firstName, lastName } = req.body;

    // --- Input validation ---
    if (!email || !password || !firstName || !lastName) {
      return res.status(400).json({
        success: false,
        error: 'All fields are required: email, password, firstName, lastName.',
      });
    }

    if (!isValidEmail(email)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid email format.',
      });
    }

    if (!isStrongPassword(password)) {
      return res.status(400).json({
        success: false,
        error:
          'Password must be at least 12 characters with uppercase, lowercase, number, and special character.',
      });
    }

    if (firstName.length > 100 || lastName.length > 100) {
      return res.status(400).json({
        success: false,
        error: 'First name and last name must be 100 characters or fewer.',
      });
    }

    // --- Check for existing user ---
    const existing = await db.query(
      'SELECT id FROM users WHERE email = $1 AND deleted_at IS NULL',
      [email.toLowerCase()]
    );
    if (existing.rows.length > 0) {
      return res.status(409).json({
        success: false,
        error: 'An account with this email already exists.',
      });
    }

    // --- Create user ---
    const passwordHash = await bcrypt.hash(password, BCRYPT_SALT_ROUNDS);
    const userId = uuidv4();

    await db.transaction(async (client) => {
      await client.query(
        `INSERT INTO users (id, email, password_hash, first_name, last_name)
         VALUES ($1, $2, $3, $4, $5)`,
        [userId, email.toLowerCase(), passwordHash, firstName.trim(), lastName.trim()]
      );

      // Assign default role: team_member
      const roleResult = await client.query(
        "SELECT id FROM roles WHERE name = 'team_member' LIMIT 1"
      );
      if (roleResult.rows.length > 0) {
        await client.query(
          'INSERT INTO user_roles (id, user_id, role_id) VALUES ($1, $2, $3)',
          [uuidv4(), userId, roleResult.rows[0].id]
        );
      }
    });

    // Fetch the created user with roles
    const userResult = await db.query(
      `SELECT u.id, u.email, u.first_name, u.last_name,
              COALESCE(array_agg(r.name) FILTER (WHERE r.name IS NOT NULL), '{}') AS roles
       FROM users u
       LEFT JOIN user_roles ur ON ur.user_id = u.id
       LEFT JOIN roles r ON r.id = ur.role_id
       WHERE u.id = $1
       GROUP BY u.id`,
      [userId]
    );

    const user = userResult.rows[0];
    const tokens = generateTokens({ id: user.id, email: user.email, roles: user.roles });

    return res.status(201).json({
      success: true,
      data: {
        id: user.id,
        email: user.email,
        firstName: user.first_name,
        lastName: user.last_name,
        roles: user.roles,
        tokens: {
          accessToken: tokens.accessToken,
          refreshToken: tokens.refreshToken,
        },
      },
    });
  } catch (err) {
    console.error('Register error:', err);
    return res.status(500).json({
      success: false,
      error: 'Internal server error during registration.',
    });
  }
};

// ---------------------------------------------------------------------------
// POST /api/auth/login
// ---------------------------------------------------------------------------
const login = async (req, res) => {
  try {
    const { email, password } = req.body;

    // --- Input validation ---
    if (!email || !password) {
      return res.status(400).json({
        success: false,
        error: 'Email and password are required.',
      });
    }

    const normalizedEmail = email.toLowerCase();

    // --- Account lockout check ---
    if (checkAccountLockout(normalizedEmail)) {
      return res.status(429).json({
        success: false,
        error: 'Account temporarily locked due to too many failed attempts. Try again later.',
      });
    }

    // --- Find user ---
    const userResult = await db.query(
      `SELECT u.id, u.email, u.password_hash, u.first_name, u.last_name,
              u.is_active, u.totp_secret, u.client_id,
              COALESCE(array_agg(r.name) FILTER (WHERE r.name IS NOT NULL), '{}') AS roles
       FROM users u
       LEFT JOIN user_roles ur ON ur.user_id = u.id
       LEFT JOIN roles r ON r.id = ur.role_id
       WHERE u.email = $1 AND u.deleted_at IS NULL
       GROUP BY u.id`,
      [normalizedEmail]
    );

    if (userResult.rows.length === 0) {
      recordFailedAttempt(normalizedEmail);
      return res.status(401).json({
        success: false,
        error: 'Invalid email or password.',
      });
    }

    const user = userResult.rows[0];

    if (!user.is_active) {
      return res.status(403).json({
        success: false,
        error: 'Account is deactivated. Contact an administrator.',
      });
    }

    // --- Verify password ---
    const passwordValid = await bcrypt.compare(password, user.password_hash);
    if (!passwordValid) {
      recordFailedAttempt(normalizedEmail);

      await writeAuditLog({
        userId: user.id,
        action: 'LOGIN_FAILED',
        resourceType: 'session',
        ipAddress: getClientIp(req),
        userAgent: req.headers['user-agent'],
      });

      return res.status(401).json({
        success: false,
        error: 'Invalid email or password.',
      });
    }

    clearFailedAttempts(normalizedEmail);

    // --- Check if 2FA is enabled ---
    if (user.totp_secret) {
      // 2FA is enabled — return a temporary token so the client can send the TOTP code
      const tempToken = jwt.sign(
        { sub: user.id, type: '2fa_pending' },
        JWT_ACCESS_SECRET,
        { expiresIn: '5m' }
      );

      return res.status(200).json({
        success: true,
        data: {
          requiresTwoFactor: true,
          tempToken,
        },
      });
    }

    // --- No 2FA — issue full token pair ---
    const tokens = generateTokens({ id: user.id, email: user.email, roles: user.roles });

    // Update last_login_at
    await db.query('UPDATE users SET last_login_at = NOW() WHERE id = $1', [user.id]);

    await writeAuditLog({
      userId: user.id,
      action: 'LOGIN_SUCCESS',
      resourceType: 'session',
      ipAddress: getClientIp(req),
      userAgent: req.headers['user-agent'],
    });

    return res.status(200).json({
      success: true,
      data: {
        requiresTwoFactor: false,
        user: {
          id: user.id,
          email: user.email,
          firstName: user.first_name,
          lastName: user.last_name,
          roles: user.roles,
        },
        tokens: {
          accessToken: tokens.accessToken,
          refreshToken: tokens.refreshToken,
        },
      },
    });
  } catch (err) {
    console.error('Login error:', err);
    return res.status(500).json({
      success: false,
      error: 'Internal server error during login.',
    });
  }
};

// ---------------------------------------------------------------------------
// POST /api/auth/2fa/setup
// ---------------------------------------------------------------------------
const setup2FA = async (req, res) => {
  try {
    const userId = req.user.id;

    // Generate TOTP secret
    const secret = speakeasy.generateSecret({
      name: `${TOTP_ISSUER} (${req.user.email})`,
      issuer: TOTP_ISSUER,
      length: 20,
    });

    // Store the secret (unverified until the user confirms with a code)
    await db.query(
      'UPDATE users SET totp_secret = $1, updated_at = NOW() WHERE id = $2',
      [secret.base32, userId]
    );

    // Generate QR code as data URL
    const qrCodeUrl = await QRCode.toDataURL(secret.otpauth_url);

    return res.status(200).json({
      success: true,
      data: {
        secret: secret.base32,
        qrCode: qrCodeUrl,
        otpauthUrl: secret.otpauth_url,
      },
    });
  } catch (err) {
    console.error('2FA setup error:', err);
    return res.status(500).json({
      success: false,
      error: 'Internal server error during 2FA setup.',
    });
  }
};

// ---------------------------------------------------------------------------
// POST /api/auth/2fa/verify
// ---------------------------------------------------------------------------
const verify2FA = async (req, res) => {
  try {
    const { tempToken, code } = req.body;

    if (!tempToken || !code) {
      return res.status(400).json({
        success: false,
        error: 'Temporary token and TOTP code are required.',
      });
    }

    // Verify the temp token
    let decoded;
    try {
      decoded = jwt.verify(tempToken, JWT_ACCESS_SECRET);
    } catch {
      return res.status(401).json({
        success: false,
        error: 'Invalid or expired temporary token. Please login again.',
      });
    }

    if (decoded.type !== '2fa_pending') {
      return res.status(400).json({
        success: false,
        error: 'Invalid token type for 2FA verification.',
      });
    }

    // Fetch user with TOTP secret
    const userResult = await db.query(
      `SELECT u.id, u.email, u.first_name, u.last_name, u.totp_secret,
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
        error: 'User not found.',
      });
    }

    const user = userResult.rows[0];

    // Verify TOTP code
    const isValid = speakeasy.totp.verify({
      secret: user.totp_secret,
      encoding: 'base32',
      token: code,
      window: 1, // allow 30s window
    });

    if (!isValid) {
      return res.status(401).json({
        success: false,
        error: 'Invalid 2FA code.',
      });
    }

    // Issue full tokens
    const tokens = generateTokens({ id: user.id, email: user.email, roles: user.roles });

    // Update last_login_at
    await db.query('UPDATE users SET last_login_at = NOW() WHERE id = $1', [user.id]);

    await writeAuditLog({
      userId: user.id,
      action: 'LOGIN_2FA_SUCCESS',
      resourceType: 'session',
      ipAddress: getClientIp(req),
      userAgent: req.headers['user-agent'],
    });

    return res.status(200).json({
      success: true,
      data: {
        user: {
          id: user.id,
          email: user.email,
          firstName: user.first_name,
          lastName: user.last_name,
          roles: user.roles,
        },
        tokens: {
          accessToken: tokens.accessToken,
          refreshToken: tokens.refreshToken,
        },
      },
    });
  } catch (err) {
    console.error('2FA verify error:', err);
    return res.status(500).json({
      success: false,
      error: 'Internal server error during 2FA verification.',
    });
  }
};

// ---------------------------------------------------------------------------
// POST /api/auth/refresh
// ---------------------------------------------------------------------------
const refreshToken = async (req, res) => {
  try {
    const { refreshToken: token } = req.body;

    if (!token) {
      return res.status(400).json({
        success: false,
        error: 'Refresh token is required.',
      });
    }

    let decoded;
    try {
      decoded = jwt.verify(token, JWT_REFRESH_SECRET);
    } catch (err) {
      return res.status(401).json({
        success: false,
        error: 'Invalid or expired refresh token. Please login again.',
      });
    }

    if (decoded.type !== 'refresh') {
      return res.status(400).json({
        success: false,
        error: 'Invalid token type.',
      });
    }

    // Fetch current user data
    const userResult = await db.query(
      `SELECT u.id, u.email, u.is_active,
              COALESCE(array_agg(r.name) FILTER (WHERE r.name IS NOT NULL), '{}') AS roles
       FROM users u
       LEFT JOIN user_roles ur ON ur.user_id = u.id
       LEFT JOIN roles r ON r.id = ur.role_id
       WHERE u.id = $1 AND u.deleted_at IS NULL
       GROUP BY u.id`,
      [decoded.sub]
    );

    if (userResult.rows.length === 0 || !userResult.rows[0].is_active) {
      return res.status(401).json({
        success: false,
        error: 'User account not found or deactivated.',
      });
    }

    const user = userResult.rows[0];
    const tokens = generateTokens({ id: user.id, email: user.email, roles: user.roles });

    return res.status(200).json({
      success: true,
      data: {
        tokens: {
          accessToken: tokens.accessToken,
          refreshToken: tokens.refreshToken,
        },
      },
    });
  } catch (err) {
    console.error('Refresh token error:', err);
    return res.status(500).json({
      success: false,
      error: 'Internal server error during token refresh.',
    });
  }
};

// ---------------------------------------------------------------------------
// POST /api/auth/logout
// ---------------------------------------------------------------------------
const logout = async (req, res) => {
  try {
    // In a Redis-backed setup we would delete the refresh token from the store.
    // For now we acknowledge the logout and rely on short-lived access tokens.

    await writeAuditLog({
      userId: req.user.id,
      action: 'LOGOUT',
      resourceType: 'session',
      ipAddress: getClientIp(req),
      userAgent: req.headers['user-agent'],
    });

    return res.status(200).json({
      success: true,
      data: { message: 'Logged out successfully.' },
    });
  } catch (err) {
    console.error('Logout error:', err);
    return res.status(500).json({
      success: false,
      error: 'Internal server error during logout.',
    });
  }
};

// ---------------------------------------------------------------------------
// GET /api/auth/me
// ---------------------------------------------------------------------------
const getProfile = async (req, res) => {
  try {
    const userResult = await db.query(
      `SELECT u.id, u.email, u.first_name, u.last_name, u.is_active,
              u.client_id, u.last_login_at, u.created_at,
              (u.totp_secret IS NOT NULL) AS has_2fa,
              COALESCE(array_agg(r.name) FILTER (WHERE r.name IS NOT NULL), '{}') AS roles
       FROM users u
       LEFT JOIN user_roles ur ON ur.user_id = u.id
       LEFT JOIN roles r ON r.id = ur.role_id
       WHERE u.id = $1 AND u.deleted_at IS NULL
       GROUP BY u.id`,
      [req.user.id]
    );

    if (userResult.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'User not found.',
      });
    }

    const user = userResult.rows[0];

    return res.status(200).json({
      success: true,
      data: {
        id: user.id,
        email: user.email,
        firstName: user.first_name,
        lastName: user.last_name,
        roles: user.roles,
        clientId: user.client_id,
        has2FA: user.has_2fa,
        lastLoginAt: user.last_login_at,
        createdAt: user.created_at,
      },
    });
  } catch (err) {
    console.error('Get profile error:', err);
    return res.status(500).json({
      success: false,
      error: 'Internal server error.',
    });
  }
};

module.exports = {
  register,
  login,
  setup2FA,
  verify2FA,
  refreshToken,
  logout,
  getProfile,
};
