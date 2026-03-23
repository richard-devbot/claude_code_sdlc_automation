#!/usr/bin/env bash
# ============================================================================
# TechNova Platform — Frontend Manual Deployment Script (No Docker)
# Usage: bash run_frontend.sh [--dev|--build|--preview]
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="${SCRIPT_DIR}/../../code/frontend"
MODE="${1:---dev}"

echo "============================================"
echo "  TechNova Frontend — Manual Deployment"
echo "  Mode: ${MODE}"
echo "============================================"
echo ""

# ---------- Pre-flight checks ----------
echo "[1/5] Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed."
    echo "Install Node.js 20 LTS from: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    echo "ERROR: Node.js 20+ required. Current: $(node -v)"
    exit 1
fi
echo "  Node.js: $(node -v) ✓"
echo "  npm: $(npm -v) ✓"
echo ""

# ---------- Navigate to frontend directory ----------
echo "[2/5] Navigating to frontend directory..."
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "ERROR: Frontend directory not found at: $FRONTEND_DIR"
    echo "Expected path: outputs/code/frontend/"
    exit 1
fi
cd "$FRONTEND_DIR"
echo "  Directory: $(pwd) ✓"
echo ""

# ---------- Install dependencies ----------
echo "[3/5] Installing dependencies..."
npm install
echo "  Dependencies installed ✓"
echo ""

# ---------- Environment variables ----------
echo "[4/5] Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "  Creating .env with default values..."
    cat > .env << 'ENVFILE'
VITE_API_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000
VITE_APP_NAME=TechNova Platform
ENVFILE
    echo "  IMPORTANT: Edit .env to match your backend URL if different."
else
    echo "  .env file found ✓"
fi
echo ""

# ---------- Run the frontend ----------
echo "[5/5] Running frontend..."
echo ""

case "$MODE" in
    --dev)
        echo "Starting Vite development server..."
        echo "  URL: http://localhost:5173"
        echo "  Hot Module Replacement (HMR) enabled"
        echo ""
        npm run dev
        ;;
    --build)
        echo "Building production bundle..."
        npm run build
        echo ""
        echo "Build complete! Output in: dist/"
        echo ""
        echo "To serve the build locally:"
        echo "  npm run preview"
        echo ""
        echo "To deploy to a web server:"
        echo "  Copy the dist/ directory to your web server root."
        echo "  Configure your web server for SPA routing (all routes -> index.html)."
        echo ""
        echo "Nginx example config:"
        echo "  location / {"
        echo "    try_files \$uri \$uri/ /index.html;"
        echo "  }"
        ;;
    --preview)
        echo "Building and previewing production bundle..."
        npm run build
        echo ""
        echo "Starting preview server..."
        echo "  URL: http://localhost:4173"
        echo ""
        npm run preview
        ;;
    *)
        echo "ERROR: Unknown mode '${MODE}'"
        echo "Usage: bash run_frontend.sh [--dev|--build|--preview]"
        echo "  --dev      Start Vite dev server with HMR (default)"
        echo "  --build    Build production bundle only"
        echo "  --preview  Build and preview production bundle"
        exit 1
        ;;
esac
