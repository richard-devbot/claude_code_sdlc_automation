#!/usr/bin/env bash
# ============================================================================
# TechNova Platform — Database Setup Script (No Docker)
# Usage: bash setup_database.sh [--create|--migrate|--seed|--reset|--full]
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${SCRIPT_DIR}/../../code/backend"
MIGRATION_DIR="${BACKEND_DIR}/src/migrations"
ACTION="${1:---full}"

# ---------- Configuration ----------
# Source .env if it exists
if [ -f "${BACKEND_DIR}/.env" ]; then
    set -a
    source "${BACKEND_DIR}/.env" 2>/dev/null || true
    set +a
fi

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-technova}"
DB_USER="${DB_USER:-technova_user}"
DB_PASSWORD="${DB_PASSWORD:-change_me}"
DB_SUPERUSER="${DB_SUPERUSER:-postgres}"

echo "============================================"
echo "  TechNova Database Setup"
echo "  Action: ${ACTION}"
echo "  Target: ${DB_HOST}:${DB_PORT}/${DB_NAME}"
echo "============================================"
echo ""

# ---------- Pre-flight checks ----------
echo "[CHECK] Verifying prerequisites..."

if ! command -v psql &> /dev/null; then
    echo "ERROR: PostgreSQL client (psql) is not installed."
    echo ""
    echo "Install PostgreSQL:"
    echo "  macOS:   brew install postgresql@16"
    echo "  Ubuntu:  sudo apt-get install -y postgresql-client-16"
    echo "  Windows: Download from https://www.postgresql.org/download/windows/"
    echo "  Amazon Linux: sudo yum install -y postgresql16"
    echo ""
    echo "Or install just the client:"
    echo "  macOS:   brew install libpq && brew link --force libpq"
    exit 1
fi
echo "  psql: $(psql --version | head -1) ✓"

# Test connection
echo "  Testing connection to ${DB_HOST}:${DB_PORT}..."
if PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "postgres" -c "SELECT 1;" &>/dev/null; then
    echo "  Connection: OK ✓"
elif PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_SUPERUSER" -d "postgres" -c "SELECT 1;" &>/dev/null; then
    echo "  Connection (superuser): OK ✓"
else
    echo ""
    echo "  WARNING: Cannot connect to PostgreSQL."
    echo "  Ensure PostgreSQL is running and credentials are correct."
    echo ""
    echo "  Start PostgreSQL:"
    echo "    macOS:   brew services start postgresql@16"
    echo "    Ubuntu:  sudo systemctl start postgresql"
    echo "    Windows: net start postgresql-x64-16"
    echo ""
    echo "  If this is a fresh install, you may need to:"
    echo "    1. sudo -u postgres createuser --superuser $DB_USER"
    echo "    2. sudo -u postgres psql -c \"ALTER USER $DB_USER PASSWORD '$DB_PASSWORD';\""
    echo ""

    if [ "$ACTION" != "--create" ]; then
        exit 1
    fi
fi
echo ""

# ---------- Functions ----------
create_database() {
    echo "[CREATE] Creating database and user..."
    echo ""

    # Create user if not exists
    echo "  Creating user '${DB_USER}'..."
    PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_SUPERUSER" -d postgres << EOSQL || true
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${DB_USER}') THEN
        CREATE ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASSWORD}';
        RAISE NOTICE 'User created: ${DB_USER}';
    ELSE
        RAISE NOTICE 'User already exists: ${DB_USER}';
    END IF;
END
\$\$;
EOSQL

    # Create database if not exists
    echo "  Creating database '${DB_NAME}'..."
    if PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_SUPERUSER" -lqt | grep -qw "$DB_NAME"; then
        echo "  Database '${DB_NAME}' already exists."
    else
        PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_SUPERUSER" -d postgres \
            -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER} ENCODING 'UTF8' LC_COLLATE 'en_US.UTF-8' LC_CTYPE 'en_US.UTF-8';" 2>/dev/null || \
        PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_SUPERUSER" -d postgres \
            -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER} ENCODING 'UTF8';"
        echo "  Database '${DB_NAME}' created ✓"
    fi

    # Grant privileges
    echo "  Granting privileges..."
    PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_SUPERUSER" -d postgres << EOSQL || true
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
ALTER DATABASE ${DB_NAME} OWNER TO ${DB_USER};
EOSQL

    echo "  Database setup complete ✓"
    echo ""
}

run_migrations() {
    echo "[MIGRATE] Running database migrations..."
    echo ""

    if [ ! -d "$MIGRATION_DIR" ]; then
        echo "  ERROR: Migration directory not found at: $MIGRATION_DIR"
        exit 1
    fi

    # Run migration files in order
    for migration_file in "$MIGRATION_DIR"/*.sql; do
        if [ -f "$migration_file" ]; then
            filename=$(basename "$migration_file")
            echo "  Applying: $filename ..."
            if PGPASSWORD="${DB_PASSWORD}" psql \
                -h "$DB_HOST" \
                -p "$DB_PORT" \
                -U "$DB_USER" \
                -d "$DB_NAME" \
                -f "$migration_file" \
                -v ON_ERROR_STOP=1 2>&1; then
                echo "  Applied: $filename ✓"
            else
                echo "  WARNING: Errors in $filename (may be expected if tables already exist)"
            fi
            echo ""
        fi
    done

    echo "  All migrations processed ✓"
    echo ""
}

seed_data() {
    echo "[SEED] Checking for seed data..."
    echo ""

    # Check if seed data exists in migration file
    SEED_FILE="${MIGRATION_DIR}/002_seed_data.sql"
    if [ -f "$SEED_FILE" ]; then
        echo "  Applying seed data from: $(basename $SEED_FILE) ..."
        PGPASSWORD="${DB_PASSWORD}" psql \
            -h "$DB_HOST" \
            -p "$DB_PORT" \
            -U "$DB_USER" \
            -d "$DB_NAME" \
            -f "$SEED_FILE" || echo "  WARNING: Seed data may already exist"
        echo "  Seed data applied ✓"
    else
        echo "  No separate seed file found."
        echo "  Seed data is included in the initial migration (001_initial_schema.sql)."
    fi
    echo ""
}

reset_database() {
    echo "[RESET] Resetting database (DESTRUCTIVE)..."
    echo ""
    read -p "  Are you sure you want to DROP and recreate the database? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "  Aborted."
        exit 0
    fi

    echo "  Dropping database '${DB_NAME}'..."
    PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_SUPERUSER" -d postgres \
        -c "DROP DATABASE IF EXISTS ${DB_NAME};"
    echo "  Database dropped ✓"
    echo ""

    create_database
    run_migrations
    seed_data
}

show_status() {
    echo "[STATUS] Database status..."
    echo ""

    echo "  Connection info:"
    echo "    Host: ${DB_HOST}:${DB_PORT}"
    echo "    Database: ${DB_NAME}"
    echo "    User: ${DB_USER}"
    echo ""

    echo "  Tables:"
    PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        -c "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;" 2>/dev/null || \
        echo "  Could not connect to database."
    echo ""

    echo "  Row counts:"
    PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        -c "SELECT schemaname, relname AS table, n_live_tup AS row_count FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 20;" 2>/dev/null || true
    echo ""
}

# ---------- Execute action ----------
case "$ACTION" in
    --create)
        create_database
        ;;
    --migrate)
        run_migrations
        ;;
    --seed)
        seed_data
        ;;
    --reset)
        reset_database
        ;;
    --status)
        show_status
        ;;
    --full)
        create_database
        run_migrations
        seed_data
        show_status
        ;;
    *)
        echo "Usage: bash setup_database.sh [--create|--migrate|--seed|--reset|--status|--full]"
        echo ""
        echo "  --create   Create database and user"
        echo "  --migrate  Run SQL migration files"
        echo "  --seed     Insert seed/demo data"
        echo "  --reset    DROP and recreate database (destructive!)"
        echo "  --status   Show database tables and row counts"
        echo "  --full     Run create + migrate + seed + status (default)"
        exit 1
        ;;
esac

echo "============================================"
echo "  Database setup complete!"
echo "============================================"
