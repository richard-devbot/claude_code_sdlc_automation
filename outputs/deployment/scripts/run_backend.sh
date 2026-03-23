#!/usr/bin/env bash
# ============================================================================
# TechNova Platform — Backend Manual Deployment Script (No Docker)
# Usage: bash run_backend.sh [--dev|--prod]
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${SCRIPT_DIR}/../../code/backend"
ENV_MODE="${1:---dev}"

echo "============================================"
echo "  TechNova Backend — Manual Deployment"
echo "  Mode: ${ENV_MODE}"
echo "============================================"
echo ""

# ---------- Pre-flight checks ----------
echo "[1/6] Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed."
    echo "Install Node.js 20 LTS from: https://nodejs.org/"
    echo "  macOS:   brew install node@20"
    echo "  Ubuntu:  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs"
    echo "  Windows: Download from https://nodejs.org/en/download/"
    exit 1
fi

NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    echo "ERROR: Node.js 20+ required. Current: $(node -v)"
    exit 1
fi
echo "  Node.js: $(node -v) ✓"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "ERROR: npm is not installed."
    exit 1
fi
echo "  npm: $(npm -v) ✓"

# Check PostgreSQL client (optional but useful)
if command -v psql &> /dev/null; then
    echo "  psql: $(psql --version | head -1) ✓"
else
    echo "  psql: not found (optional — needed for migrations)"
fi

echo ""

# ---------- Navigate to backend directory ----------
echo "[2/6] Navigating to backend directory..."
if [ ! -d "$BACKEND_DIR" ]; then
    echo "ERROR: Backend directory not found at: $BACKEND_DIR"
    echo "Expected path: outputs/code/backend/"
    exit 1
fi
cd "$BACKEND_DIR"
echo "  Directory: $(pwd) ✓"
echo ""

# ---------- Install dependencies ----------
echo "[3/6] Installing dependencies..."
if [ "$ENV_MODE" = "--prod" ]; then
    npm ci --only=production
else
    npm install
fi
echo "  Dependencies installed ✓"
echo ""

# ---------- Environment file ----------
echo "[4/6] Checking environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "  No .env file found. Copying from .env.example..."
        cp .env.example .env
        echo "  IMPORTANT: Edit .env with your actual configuration values!"
        echo "  Especially: DB_PASSWORD, JWT_ACCESS_SECRET, JWT_REFRESH_SECRET"
    else
        echo "  WARNING: No .env or .env.example found."
        echo "  Creating minimal .env file..."
        cat > .env << 'ENVFILE'
NODE_ENV=development
PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=technova
DB_USER=technova_user
DB_PASSWORD=change_me
JWT_ACCESS_SECRET=dev_jwt_access_secret_must_be_at_least_32_characters
JWT_REFRESH_SECRET=dev_jwt_refresh_secret_must_be_at_least_32_characters
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d
BCRYPT_SALT_ROUNDS=10
CORS_ORIGIN=http://localhost:5173
FRONTEND_URL=http://localhost:5173
LOG_LEVEL=debug
ENVFILE
        echo "  IMPORTANT: Edit .env with your actual configuration values!"
    fi
else
    echo "  .env file found ✓"
fi
echo ""

# ---------- Run migrations ----------
echo "[5/6] Running database migrations..."
MIGRATION_FILE="src/migrations/001_initial_schema.sql"
if [ -f "$MIGRATION_FILE" ]; then
    if command -v psql &> /dev/null; then
        # Source .env for DB connection details
        set -a
        source .env 2>/dev/null || true
        set +a

        echo "  Attempting migration against ${DB_HOST:-localhost}:${DB_PORT:-5432}/${DB_NAME:-technova}..."
        if PGPASSWORD="${DB_PASSWORD:-}" psql \
            -h "${DB_HOST:-localhost}" \
            -p "${DB_PORT:-5432}" \
            -U "${DB_USER:-technova_user}" \
            -d "${DB_NAME:-technova}" \
            -f "$MIGRATION_FILE" 2>/dev/null; then
            echo "  Migrations applied ✓"
        else
            echo "  WARNING: Migration failed. Ensure PostgreSQL is running and .env is configured."
            echo "  You can run migrations manually:"
            echo "    psql -h localhost -U technova_user -d technova -f $MIGRATION_FILE"
        fi
    else
        echo "  WARNING: psql not found. Run migrations manually:"
        echo "    psql -h localhost -U technova_user -d technova -f $MIGRATION_FILE"
    fi
else
    echo "  No migration files found."
fi
echo ""

# ---------- Start server ----------
echo "[6/6] Starting backend server..."
echo ""

if [ "$ENV_MODE" = "--prod" ]; then
    echo "Starting in PRODUCTION mode..."
    echo "  URL: http://localhost:${PORT:-3000}"
    echo "  Health: http://localhost:${PORT:-3000}/api/health"
    echo ""
    NODE_ENV=production node src/app.js
else
    echo "Starting in DEVELOPMENT mode (with auto-reload)..."
    echo "  URL: http://localhost:${PORT:-3000}"
    echo "  Health: http://localhost:${PORT:-3000}/api/health"
    echo ""
    if npx --no-install nodemon --version &> /dev/null; then
        npm run dev
    else
        echo "  nodemon not available, using node directly..."
        node src/app.js
    fi
fi
