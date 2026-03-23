# TechNova Solutions -- Client Project Management Platform

## Overview

Full-stack project management platform for a digital agency with client portal, time tracking, invoicing, resource management, and SOC2 compliance.

**Tech Stack:**
- Backend: Node.js 20 / Express.js 4.x
- Frontend: React 18 / Vite / React Router
- Database: PostgreSQL 16
- Auth: JWT + Refresh Tokens + TOTP 2FA

## Directory Structure

```
code/
  backend/
    src/
      app.js                      Main Express application
      config/
        database.js               PostgreSQL connection pool
      middleware/
        auth.middleware.js         JWT authentication + RBAC authorization
        audit.middleware.js        Audit logging for SOC2 compliance
      routes/
        auth.routes.js             Auth endpoints
        project.routes.js          Project CRUD endpoints
      controllers/
        auth.controller.js         Auth business logic (bcrypt, JWT, TOTP)
        project.controller.js      Project/task/milestone business logic
      migrations/
        001_initial_schema.sql     Full database schema
    .env.example                   Required environment variables
    package.json                   Backend dependencies
  frontend/
    src/
      App.jsx                      React Router with protected routes
      pages/
        Login.jsx                  Login page with 2FA step
        Dashboard.jsx              Role-based dashboard
      services/
        api.service.js             Axios HTTP client with interceptors
        auth.service.js            Auth service (login, logout, refresh)
      hooks/
        useAuth.js                 Auth context + hook
      components/
        ProtectedRoute.jsx         Route guard component
    package.json                   Frontend dependencies
```

## Prerequisites

- Node.js 20 LTS or later
- PostgreSQL 16 (or Docker for containerised PostgreSQL)
- npm or yarn

## Backend Setup

```bash
cd backend

# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
# Edit .env with your database credentials and secrets

# 3. Create the database
createdb technova
# Or via psql:
# psql -c "CREATE DATABASE technova;"

# 4. Run the initial migration
psql -d technova -f src/migrations/001_initial_schema.sql

# 5. Start the server
npm run dev          # development with auto-reload
npm start            # production
```

The API starts on `http://localhost:3000` by default.

### Health Check

```
GET http://localhost:3000/health
```

## Frontend Setup

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Configure API URL (optional, defaults to localhost:3000)
# Create .env with: VITE_API_BASE_URL=http://localhost:3000

# 3. Start development server
npm run dev

# 4. Build for production
npm run build
```

The frontend starts on `http://localhost:5173` by default (Vite).

## Default Roles

After running the migration, the following roles are seeded:

| Role | Description |
|------|-------------|
| admin | Full system access |
| executive | Read-only, full reports |
| pm | Project management |
| team_lead | Task management, time approval |
| team_member | Work on tasks, log time |
| finance_manager | Invoicing, billing rates |
| client_user | Client portal access |

## API Endpoints

### Auth (`/api/auth`)
- `POST /register` -- Register new user
- `POST /login` -- Login (returns JWT or 2FA challenge)
- `POST /2fa/setup` -- Setup TOTP 2FA (requires auth)
- `POST /2fa/verify` -- Verify TOTP code
- `POST /refresh` -- Refresh access token
- `POST /logout` -- Logout
- `GET /me` -- Get current user profile

### Projects (`/api/projects`)
- `GET /` -- List projects (with filtering, sorting, pagination)
- `GET /:projectId` -- Get project details
- `POST /` -- Create project
- `PATCH /:projectId` -- Update project
- `DELETE /:projectId` -- Soft-delete project
- `GET /:projectId/members` -- List project members
- `POST /:projectId/members` -- Add project member
- `GET /:projectId/tasks` -- List tasks
- `POST /:projectId/tasks` -- Create task
- `PATCH /:projectId/tasks/:taskId` -- Update task
- `GET /:projectId/milestones` -- List milestones
- `POST /:projectId/milestones` -- Create milestone

## Environment Variables

See `backend/.env.example` for the complete list. Key variables:

| Variable | Description |
|----------|-------------|
| `PORT` | API server port (default: 3000) |
| `DB_HOST` | PostgreSQL host |
| `DB_NAME` | Database name |
| `DB_USER` / `DB_PASSWORD` | Database credentials |
| `JWT_ACCESS_SECRET` | Secret for signing access tokens |
| `JWT_REFRESH_SECRET` | Secret for signing refresh tokens |
| `BCRYPT_SALT_ROUNDS` | Password hashing cost (default: 12) |

## Security Features

- JWT access tokens (15-minute expiry)
- Refresh tokens (7-day expiry)
- TOTP-based 2FA
- bcrypt password hashing (cost factor 12)
- RBAC with 7 predefined roles
- Rate limiting (10 req/min on auth, 100 req/min global)
- Account lockout after 5 failed attempts
- CORS whitelist
- Helmet security headers
- Input validation on all endpoints
- Immutable audit log table
- Row-level security for client data isolation
