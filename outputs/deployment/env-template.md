# TechNova Platform — Environment Variables Reference

All environment variables required to run the TechNova Client Project Management Platform.
Copy each section into your `.env` file and replace placeholder values.

---

## Backend Service (Node.js / Express)

### Core Application

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `NODE_ENV` | Application environment (`development`, `staging`, `production`) | `production` | Yes |
| `PORT` | Port the API server listens on | `3000` | Yes |
| `LOG_LEVEL` | Winston log level (`error`, `warn`, `info`, `debug`) | `info` | No (default: `info`) |

### Database — PostgreSQL 16

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DB_HOST` | PostgreSQL hostname | `localhost` | Yes |
| `DB_PORT` | PostgreSQL port | `5432` | Yes |
| `DB_NAME` | Database name | `technova` | Yes |
| `DB_USER` | Database username | `technova_user` | Yes |
| `DB_PASSWORD` | Database password | `your_secure_password_here` | Yes |
| `DB_SSL` | Enable SSL for database connection (`true`/`false`) | `false` | No (default: `false`) |
| `DB_POOL_MIN` | Minimum connection pool size | `2` | No (default: `2`) |
| `DB_POOL_MAX` | Maximum connection pool size | `10` | No (default: `10`) |

### Cache — Redis 7

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `REDIS_HOST` | Redis hostname | `localhost` | Yes |
| `REDIS_PORT` | Redis port | `6379` | Yes |
| `REDIS_PASSWORD` | Redis password | `your_redis_password` | Yes (production) |

### Authentication — JWT + 2FA

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `JWT_ACCESS_SECRET` | Secret key for signing JWT access tokens (min 32 chars) | `a1b2c3d4e5f6...` | Yes |
| `JWT_REFRESH_SECRET` | Secret key for signing JWT refresh tokens (min 32 chars) | `f6e5d4c3b2a1...` | Yes |
| `JWT_ACCESS_EXPIRY` | Access token expiry duration | `15m` | No (default: `15m`) |
| `JWT_REFRESH_EXPIRY` | Refresh token expiry duration | `7d` | No (default: `7d`) |
| `BCRYPT_SALT_ROUNDS` | bcrypt hashing cost factor (10-14 recommended) | `12` | No (default: `12`) |
| `TOTP_ISSUER` | Issuer name displayed in authenticator apps for 2FA | `TechNova Platform` | No (default: `TechNova Platform`) |

### Rate Limiting

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `RATE_LIMIT_WINDOW_MS` | Global rate limit window in milliseconds | `60000` | No (default: `60000`) |
| `RATE_LIMIT_MAX_REQUESTS` | Max requests per window (global) | `100` | No (default: `100`) |
| `AUTH_RATE_LIMIT_WINDOW_MS` | Auth endpoint rate limit window in ms | `60000` | No (default: `60000`) |
| `AUTH_RATE_LIMIT_MAX_REQUESTS` | Max auth requests per window | `10` | No (default: `10`) |

### Account Security

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `ACCOUNT_LOCKOUT_THRESHOLD` | Failed login attempts before account lockout | `5` | No (default: `5`) |
| `ACCOUNT_LOCKOUT_DURATION_MS` | Lockout duration in milliseconds (default: 15 min) | `900000` | No (default: `900000`) |

### CORS & Frontend Integration

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `CORS_ORIGIN` | Allowed CORS origins (comma-separated for multiple) | `http://localhost:5173` | Yes |
| `FRONTEND_URL` | Frontend URL for redirects and email links | `http://localhost:5173` | Yes |

---

## Frontend Service (React / Vite)

Frontend variables must be prefixed with `VITE_` to be exposed to the browser bundle.

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:3000/api` | Yes |
| `VITE_WS_URL` | WebSocket server URL for real-time features | `ws://localhost:3000` | Yes |
| `VITE_APP_NAME` | Application display name | `TechNova Platform` | No (default: `TechNova Platform`) |

---

## Docker Compose Overrides

These variables configure the Docker Compose setup itself:

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `BACKEND_PORT` | Host port mapped to backend container | `3000` | No (default: `3000`) |
| `FRONTEND_PORT` | Host port mapped to frontend container | `80` | No (default: `80`) |
| `DB_PORT` | Host port mapped to PostgreSQL container | `5432` | No (default: `5432`) |
| `REDIS_PORT` | Host port mapped to Redis container | `6379` | No (default: `6379`) |

---

## Example .env File (Development)

```bash
# === Core ===
NODE_ENV=development
PORT=3000
LOG_LEVEL=debug

# === Database ===
DB_HOST=localhost
DB_PORT=5432
DB_NAME=technova
DB_USER=technova_user
DB_PASSWORD=dev_password_123
DB_SSL=false
DB_POOL_MIN=2
DB_POOL_MAX=10

# === Redis ===
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=dev_redis_password

# === JWT ===
JWT_ACCESS_SECRET=dev_jwt_access_secret_must_be_at_least_32_characters
JWT_REFRESH_SECRET=dev_jwt_refresh_secret_must_be_at_least_32_characters
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# === Security ===
BCRYPT_SALT_ROUNDS=10
TOTP_ISSUER=TechNova Platform (Dev)
RATE_LIMIT_WINDOW_MS=60000
RATE_LIMIT_MAX_REQUESTS=200
AUTH_RATE_LIMIT_WINDOW_MS=60000
AUTH_RATE_LIMIT_MAX_REQUESTS=20
ACCOUNT_LOCKOUT_THRESHOLD=10
ACCOUNT_LOCKOUT_DURATION_MS=300000

# === CORS ===
CORS_ORIGIN=http://localhost:5173
FRONTEND_URL=http://localhost:5173

# === Frontend (Vite) ===
VITE_API_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000
VITE_APP_NAME=TechNova Platform (Dev)
```

---

## Example .env File (Production)

```bash
# === Core ===
NODE_ENV=production
PORT=3000
LOG_LEVEL=warn

# === Database ===
DB_HOST=technova-db.cluster-abc123.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=technova
DB_USER=technova_prod
DB_PASSWORD=<use-secrets-manager>
DB_SSL=true
DB_POOL_MIN=5
DB_POOL_MAX=20

# === Redis ===
REDIS_HOST=technova-redis.abc123.0001.use1.cache.amazonaws.com
REDIS_PORT=6379
REDIS_PASSWORD=<use-secrets-manager>

# === JWT (generate with: openssl rand -base64 48) ===
JWT_ACCESS_SECRET=<use-secrets-manager>
JWT_REFRESH_SECRET=<use-secrets-manager>
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# === Security ===
BCRYPT_SALT_ROUNDS=12
TOTP_ISSUER=TechNova Platform
RATE_LIMIT_WINDOW_MS=60000
RATE_LIMIT_MAX_REQUESTS=100
AUTH_RATE_LIMIT_WINDOW_MS=60000
AUTH_RATE_LIMIT_MAX_REQUESTS=10
ACCOUNT_LOCKOUT_THRESHOLD=5
ACCOUNT_LOCKOUT_DURATION_MS=900000

# === CORS ===
CORS_ORIGIN=https://app.technova.example.com
FRONTEND_URL=https://app.technova.example.com

# === Frontend (set at Docker build time) ===
VITE_API_URL=https://api.technova.example.com/api
VITE_WS_URL=wss://api.technova.example.com
VITE_APP_NAME=TechNova Platform
```

---

## Security Notes

1. **Never commit `.env` files** to version control. Add `.env` to `.gitignore`.
2. **Use a secrets manager** in production (AWS Secrets Manager, HashiCorp Vault, etc.).
3. **Rotate JWT secrets** periodically (at least every 90 days for SOC2 compliance).
4. **Generate secrets** with: `openssl rand -base64 48`
5. **Database passwords** should be at least 16 characters with mixed case, numbers, and symbols.
6. **Redis** should always require a password in production, even in private networks.
