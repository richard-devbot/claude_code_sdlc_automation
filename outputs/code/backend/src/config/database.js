'use strict';

const { Pool } = require('pg');
const winston = require('winston');

// ---------------------------------------------------------------------------
// Logger for database module
// ---------------------------------------------------------------------------
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'database' },
  transports: [new winston.transports.Console()],
});

// ---------------------------------------------------------------------------
// PostgreSQL connection pool configuration (all values from env)
// ---------------------------------------------------------------------------
const poolConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT, 10) || 5432,
  database: process.env.DB_NAME || 'technova',
  user: process.env.DB_USER || 'technova_user',
  password: process.env.DB_PASSWORD || '',
  min: parseInt(process.env.DB_POOL_MIN, 10) || 2,
  max: parseInt(process.env.DB_POOL_MAX, 10) || 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
};

// Enable SSL in non-development environments
if (process.env.DB_SSL === 'true') {
  poolConfig.ssl = { rejectUnauthorized: false };
}

const pool = new Pool(poolConfig);

// ---------------------------------------------------------------------------
// Pool event handlers
// ---------------------------------------------------------------------------
pool.on('connect', () => {
  logger.debug('New database connection established');
});

pool.on('error', (err) => {
  logger.error('Unexpected database pool error', { error: err.message });
});

// ---------------------------------------------------------------------------
// Convenience query helper — wraps pool.query for easy import
// ---------------------------------------------------------------------------
/**
 * Execute a parameterised SQL query against the connection pool.
 * @param {string} text  SQL query string with $1, $2, ... placeholders
 * @param {Array}  params  Parameter values
 * @returns {Promise<import('pg').QueryResult>}
 */
const query = async (text, params) => {
  const start = Date.now();
  try {
    const result = await pool.query(text, params);
    const duration = Date.now() - start;
    logger.debug('Executed query', {
      text: text.substring(0, 120),
      duration,
      rows: result.rowCount,
    });
    return result;
  } catch (err) {
    logger.error('Query execution failed', {
      text: text.substring(0, 120),
      error: err.message,
    });
    throw err;
  }
};

// ---------------------------------------------------------------------------
// Transaction helper — obtains a client, runs callback, commits / rolls back
// ---------------------------------------------------------------------------
/**
 * Run a function inside a database transaction.
 * @param {(client: import('pg').PoolClient) => Promise<any>} callback
 * @returns {Promise<any>} The value returned by the callback
 */
const transaction = async (callback) => {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const result = await callback(client);
    await client.query('COMMIT');
    return result;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
};

// ---------------------------------------------------------------------------
// Health check
// ---------------------------------------------------------------------------
const healthCheck = async () => {
  try {
    const result = await pool.query('SELECT NOW() AS server_time');
    return { status: 'healthy', serverTime: result.rows[0].server_time };
  } catch (err) {
    return { status: 'unhealthy', error: err.message };
  }
};

module.exports = {
  pool,
  query,
  transaction,
  healthCheck,
};
