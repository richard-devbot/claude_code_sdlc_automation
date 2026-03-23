'use strict';

const { v4: uuidv4 } = require('uuid');
const db = require('../config/database');
const winston = require('winston');

// ---------------------------------------------------------------------------
// Logger
// ---------------------------------------------------------------------------
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'audit' },
  transports: [new winston.transports.Console()],
});

// ---------------------------------------------------------------------------
// Determine the real client IP (respects X-Forwarded-For behind a proxy)
// ---------------------------------------------------------------------------
const getClientIp = (req) => {
  const forwarded = req.headers['x-forwarded-for'];
  if (forwarded) {
    return forwarded.split(',')[0].trim();
  }
  return req.ip || req.connection?.remoteAddress || null;
};

// ---------------------------------------------------------------------------
// auditLog — middleware factory for logging sensitive operations
// ---------------------------------------------------------------------------
/**
 * Returns Express middleware that writes an audit log entry AFTER the
 * response has been sent.  The middleware captures:
 *   - who: authenticated user id
 *   - what: action + resource_type
 *   - when: timestamp (DB default)
 *   - from where: IP address + User-Agent
 *
 * @param {string} action        e.g. 'CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT'
 * @param {string} resourceType  e.g. 'user', 'project', 'invoice'
 * @returns {Function} Express middleware
 */
const auditLog = (action, resourceType) => {
  return (req, res, next) => {
    // Capture the original json method so we can intercept the response
    const originalJson = res.json.bind(res);

    res.json = (body) => {
      // Fire-and-forget the audit log write (non-blocking)
      const userId = req.user?.id || null;
      const resourceId = req.params.id || req.params.projectId || req.params.invoiceId || body?.data?.id || null;
      const ipAddress = getClientIp(req);
      const userAgent = req.headers['user-agent'] || null;

      // Capture before / after values for state-changing operations
      const beforeValue = req._auditBefore || null;
      const afterValue = body?.data || null;

      db.query(
        `INSERT INTO audit_logs (id, user_id, action, resource_type, resource_id,
                                  before_value, after_value, ip_address, user_agent)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
        [
          uuidv4(),
          userId,
          action,
          resourceType,
          resourceId,
          beforeValue ? JSON.stringify(beforeValue) : null,
          afterValue ? JSON.stringify(afterValue) : null,
          ipAddress,
          userAgent,
        ]
      ).catch((err) => {
        logger.error('Failed to write audit log', {
          action,
          resourceType,
          error: err.message,
        });
      });

      // Log to structured logger as well
      logger.info('Audit event', {
        userId,
        action,
        resourceType,
        resourceId,
        ipAddress,
        method: req.method,
        path: req.originalUrl,
        statusCode: res.statusCode,
      });

      return originalJson(body);
    };

    next();
  };
};

// ---------------------------------------------------------------------------
// Capture "before" state for UPDATE / DELETE operations
// ---------------------------------------------------------------------------
/**
 * Attach a "before" snapshot to the request so the auditLog middleware can
 * compare before/after.  Call this in your controller before mutating data.
 *
 * @param {import('express').Request} req
 * @param {object} data  The current state of the resource
 */
const setAuditBefore = (req, data) => {
  req._auditBefore = data;
};

// ---------------------------------------------------------------------------
// Direct audit log write (for non-middleware use, e.g. login events)
// ---------------------------------------------------------------------------
/**
 * Write an audit log entry directly (not as middleware).
 *
 * @param {object} params
 * @param {string|null} params.userId
 * @param {string} params.action
 * @param {string} params.resourceType
 * @param {string|null} params.resourceId
 * @param {object|null} params.beforeValue
 * @param {object|null} params.afterValue
 * @param {string|null} params.ipAddress
 * @param {string|null} params.userAgent
 */
const writeAuditLog = async ({
  userId,
  action,
  resourceType,
  resourceId = null,
  beforeValue = null,
  afterValue = null,
  ipAddress = null,
  userAgent = null,
}) => {
  try {
    await db.query(
      `INSERT INTO audit_logs (id, user_id, action, resource_type, resource_id,
                                before_value, after_value, ip_address, user_agent)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
      [
        uuidv4(),
        userId,
        action,
        resourceType,
        resourceId,
        beforeValue ? JSON.stringify(beforeValue) : null,
        afterValue ? JSON.stringify(afterValue) : null,
        ipAddress,
        userAgent,
      ]
    );
  } catch (err) {
    logger.error('Failed to write direct audit log', {
      action,
      resourceType,
      error: err.message,
    });
  }
};

module.exports = {
  auditLog,
  setAuditBefore,
  writeAuditLog,
  getClientIp,
};
