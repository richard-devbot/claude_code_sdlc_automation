# High Level Design (HLD)
## TechNova Solutions -- Client Project Management Platform

**Version:** 1.0
**Date:** 2026-03-12
**Author:** Architecture Agent (SDLC Automation Pipeline)
**Domain:** Professional Services / Digital Agency Management
**Compliance:** SOC2 Type II

---

## Table of Contents

1. [System Context Diagram](#1-system-context-diagram)
2. [Service Architecture](#2-service-architecture)
3. [Tech Stack Decisions](#3-tech-stack-decisions)
4. [Database Strategy](#4-database-strategy)
5. [Security Architecture](#5-security-architecture)
6. [Integration Architecture](#6-integration-architecture)
7. [Deployment Architecture](#7-deployment-architecture)

---

## 1. System Context Diagram

The system context diagram shows the TechNova Platform and its interactions with external actors and systems.

```
                         +---------------------+
                         |   Google Workspace   |
                         |  (SSO / Calendar)    |
                         +----------+----------+
                                    |
                                    | SAML 2.0 / OIDC
                                    | Calendar API v3
                                    |
+----------------+        +---------v---------+        +----------------+
|                |  HTTPS |                   | HTTPS  |                |
| Internal Users +--------> TechNova Platform <--------+ Client Users   |
| (150-250)      |  JWT   |                   |  JWT   | (60-80)        |
| - Admin        |        |  +-------------+  |        | - View projects|
| - PM           |        |  | React SPA   |  |        | - Approve      |
| - Team Lead    |        |  +------+------+  |        | - Message      |
| - Team Member  |        |         |         |        | - Download     |
| - Finance Mgr  |        |  +------v------+  |        +----------------+
| - Executive    |        |  | Node.js API |  |
+----------------+        |  +------+------+  |
                          |         |         |
                          |  +------v------+  |
                          |  | PostgreSQL  |  |
                          |  | Redis Cache |  |
                          |  +-------------+  |
                          +----+----+----+----+
                               |    |    |
              +----------------+    |    +----------------+
              |                     |                     |
   +----------v----------+  +------v-------+  +----------v----------+
   |    QuickBooks        |  |    Slack      |  |    SendGrid /       |
   |    Online API        |  |    API        |  |    Email Service     |
   |  (Invoice Sync)      |  | (Notify)     |  |  (Email Notify)      |
   +----------------------+  +--------------+  +----------------------+
```

### External Systems and Actors

| Actor / System | Interaction | Protocol |
|---|---|---|
| Internal Users (150-250) | Full platform access via web browser | HTTPS, JWT Auth |
| Client Users (60-80) | Client portal with restricted scope | HTTPS, JWT Auth |
| QuickBooks Online | Bi-directional invoice sync, payment status | OAuth 2.0, REST API |
| Slack | Event-driven notifications to channels/DMs | OAuth 2.0, Webhooks |
| Google Workspace | SSO (SAML 2.0/OIDC), Calendar sync | SAML 2.0, Calendar API v3 |
| SendGrid / Email | Transactional and notification emails | SMTP / REST API |
| Figma (Phase 1 - basic) | Link embedding, thumbnail preview | REST API (read-only) |
| GitHub (Phase 1 - basic) | Commit activity display | REST API (read-only) |

---

## 2. Service Architecture

### Architecture Pattern: Modular Monolith

**Rationale:** With 11 modules, a medium-sized team, and a 5-month delivery timeline, a modular monolith is optimal. It provides clear module boundaries for future extraction into microservices while keeping deployment simple and development velocity high.

```
+------------------------------------------------------------------+
|                        FRONTEND (React SPA)                       |
|                                                                    |
|  +----------+ +----------+ +----------+ +----------+ +----------+ |
|  |  Project  | |  Client  | |   Time   | | Resource | |  Report  | |
|  |  Mgmt UI  | | Portal UI| | Track UI | | Mgmt UI  | |  Dash UI | |
|  +----------+ +----------+ +----------+ +----------+ +----------+ |
|  +----------+ +----------+ +----------+ +----------+ +----------+ |
|  |  Doc Mgmt | |  Invoice | |  Admin   | |  Search  | |  Notif.  | |
|  |  UI       | |  UI      | |  Panel   | |  UI      | |  Center  | |
|  +----------+ +----------+ +----------+ +----------+ +----------+ |
+----------------------------------+-----------------------------------+
                                   |  REST API + WebSocket
+----------------------------------v-----------------------------------+
|                     API GATEWAY / REVERSE PROXY                      |
|                   (Nginx - Rate Limiting, TLS, CORS)                 |
+----------------------------------+-----------------------------------+
                                   |
+----------------------------------v-----------------------------------+
|                   BACKEND (Node.js / Express)                        |
|                                                                      |
|  MIDDLEWARE LAYER:                                                    |
|  [Auth JWT] [RBAC] [Audit Log] [Rate Limit] [Validation] [CORS]     |
|                                                                      |
|  MODULE LAYER:                                                       |
|  +------------------+ +------------------+ +------------------+      |
|  | auth_module      | | project_module   | | client_module    |      |
|  | - Login/Logout   | | - Project CRUD   | | - Portal API     |      |
|  | - 2FA (TOTP)     | | - Task Mgmt      | | - Data Isolation |      |
|  | - SSO (Google)   | | - Milestones     | | - Messaging      |      |
|  | - Sessions       | | - Kanban Board   | | - Approvals      |      |
|  | - Password Policy| | - Dependencies   | | - Timeline       |      |
|  +------------------+ +------------------+ +------------------+      |
|                                                                      |
|  +------------------+ +------------------+ +------------------+      |
|  | time_module      | | invoice_module   | | resource_module  |      |
|  | - Timer Start/   | | - Invoice Gen    | | - Allocation     |      |
|  |   Stop           | | - Rate Hierarchy | |   Board          |      |
|  | - Manual Entry   | | - Line Items     | | - Utilization    |      |
|  | - Approval WF    | | - Finalization   | | - Forecasting    |      |
|  | - Timesheets     | | - QB Sync        | | - Conflict Detect|      |
|  +------------------+ +------------------+ +------------------+      |
|                                                                      |
|  +------------------+ +------------------+ +------------------+      |
|  | document_module  | | report_module    | | integration_mod  |      |
|  | - Upload/Download| | - Exec Dashboard | | - QuickBooks     |      |
|  | - Version Control| | - Profitability  | | - Slack           |      |
|  | - Preview        | | - Configurable   | | - Google Cal     |      |
|  | - Comments       | |   Reports        | | - Figma (basic)  |      |
|  | - Client Approval| | - NPS Tracking   | | - GitHub (basic) |      |
|  +------------------+ +------------------+ +------------------+      |
|                                                                      |
|  +------------------+ +------------------+                           |
|  | admin_module     | | notification_mod |                           |
|  | - User CRUD      | | - In-App Notif   |                          |
|  | - Role/Perm Mgmt | | - Email (SendGrid)|                         |
|  | - Integration Cfg| | - Slack Dispatch  |                          |
|  | - Billing Rates  | | - WebSocket Push  |                         |
|  | - Data Migration | | - Preferences     |                         |
|  +------------------+ +------------------+                           |
|                                                                      |
|  SHARED SERVICES:                                                    |
|  [Event Bus (in-process)] [File Storage (S3)] [Search (Elasticsearch)]|
+----------------------------------+-----------------------------------+
                                   |
            +----------------------+----------------------+
            |                                             |
   +--------v--------+                          +--------v--------+
   |   PostgreSQL     |                          |     Redis       |
   |   (Primary DB)   |                          |   (Cache +      |
   |                  |                          |    Sessions)     |
   +------------------+                          +-----------------+
```

### Module Responsibilities

| Module | Responsibility | Key APIs | FR Coverage |
|---|---|---|---|
| auth_module | Authentication, authorization, 2FA, SSO, sessions | /api/auth/* | FR-033, FR-034, FR-046, FR-047, FR-048 |
| project_module | Projects, tasks, milestones, Kanban | /api/projects/*, /api/tasks/* | FR-001 to FR-005 |
| client_module | Client portal, data isolation, messaging, approvals | /api/portal/* | FR-006 to FR-010 |
| time_module | Time tracking, timers, approval workflows, timesheets | /api/time-entries/*, /api/timesheets/* | FR-011, FR-027, FR-028 |
| invoice_module | Invoice generation, billing rates, finalization | /api/invoices/*, /api/billing-rates/* | FR-012, FR-026 |
| resource_module | Resource allocation, utilization, forecasting | /api/resources/* | FR-013, FR-014, FR-015 |
| document_module | File upload/download, versioning, comments, approvals | /api/documents/* | FR-016 to FR-019 |
| report_module | Executive dashboards, profitability, NPS, exports | /api/reports/*, /api/dashboards/* | FR-029 to FR-032 |
| integration_module | QuickBooks, Slack, Google Calendar, Figma, GitHub | /api/integrations/* | FR-020 to FR-025 |
| admin_module | User management, roles, settings, data migration | /api/admin/* | FR-033, FR-040, FR-041, FR-042 |
| notification_module | In-app, email, Slack notifications, preferences | /api/notifications/* | FR-010, FR-021, FR-039 |

---

## 3. Tech Stack Decisions

### Summary

| Layer | Technology | Version |
|---|---|---|
| Frontend | React.js + TypeScript | React 18.x |
| UI Framework | Ant Design (antd) | 5.x |
| State Management | Redux Toolkit + RTK Query | 2.x |
| Backend | Node.js + Express.js + TypeScript | Node 20 LTS, Express 4.x |
| ORM | Prisma | 5.x |
| Primary Database | PostgreSQL | 16.x |
| Cache / Sessions | Redis | 7.x |
| Search | Elasticsearch | 8.x |
| File Storage | AWS S3 (or S3-compatible) | - |
| Email | SendGrid | - |
| Authentication | JWT + Refresh Tokens + TOTP (2FA) | jsonwebtoken, speakeasy |
| Real-time | Socket.IO (WebSocket) | 4.x |
| API Documentation | OpenAPI 3.0 (Swagger) | - |
| Containerization | Docker + Docker Compose | - |
| CI/CD | GitHub Actions | - |
| Cloud Provider | AWS | - |
| Monitoring | CloudWatch + X-Ray | - |
| Logging | Winston + structured JSON logs | - |

### Detailed Rationale

#### Backend: Node.js / Express / TypeScript

- **Why Node.js:** The platform is API-heavy with 11 modules and 4+ external integrations. Node.js excels at I/O-bound operations (database queries, external API calls, file uploads). Non-blocking event loop handles concurrent requests efficiently for 200+ users.
- **Why Express:** Mature, lightweight, enormous middleware ecosystem. Pairs well with modular monolith architecture. Express middleware maps cleanly to cross-cutting concerns (auth, audit, rate limiting).
- **Why TypeScript:** SOC2 compliance benefits from type safety, reducing runtime errors. Self-documenting codebase aids future maintainability. Shared types between frontend and backend reduce integration bugs.

#### Frontend: React.js / TypeScript

- **Why React:** Dashboard-heavy UI with data tables, Kanban boards, Gantt charts, and resource allocation boards. React's component model and ecosystem (AG Grid, react-beautiful-dnd, recharts) directly support these complex UI patterns. Largest talent pool for future hires.
- **Why Ant Design:** Enterprise-grade component library with tables, forms, date pickers, and layouts that match a project management platform's needs. Reduces custom UI development time significantly.
- **Why Redux Toolkit + RTK Query:** Centralized state management for complex cross-module state (e.g., notifications, active timer, user permissions). RTK Query provides built-in caching, polling, and WebSocket integration for real-time features.

#### Database: PostgreSQL 16

- **Why PostgreSQL:** SOC2 compliance demands ACID transactions, strong data integrity, and audit-grade consistency. Relational data model is ideal for the highly structured domain (projects have tasks, tasks have time entries, time entries generate invoices). Row-level security supports client data isolation (NFR-018). JSON columns available for flexible metadata where needed.
- **Why not MongoDB:** The data is inherently relational with strict referential integrity requirements (e.g., time entries must reference valid projects and tasks). Financial data (invoicing, billing rates) requires ACID transactions. SOC2 audit trails require immutable, consistent logging.

#### Cache: Redis 7

- **Why Redis:** Session storage for JWT refresh tokens (fast lookup, TTL-based expiry). Dashboard query caching to meet the 5-second executive dashboard load target (NFR-002). Rate limiting counters for auth endpoints (NFR-020). Real-time timer state persistence for the time tracking module.

#### Authentication: JWT + Refresh Tokens + TOTP 2FA

- **Why this combination:** JWT access tokens (15-minute expiry) for stateless API authentication. Refresh tokens (stored in Redis, 7-day expiry) for seamless session continuity. TOTP-based 2FA via authenticator apps (Google Authenticator, Authy) satisfies SOC2 MFA requirements. SMS fallback for users who cannot use authenticator apps.
- **SSO via Google Workspace:** SAML 2.0 / OIDC integration for internal users. Federated identity eliminates password management burden for most users while maintaining 2FA requirement.

#### Search: Elasticsearch 8

- **Why Elasticsearch:** Global search (FR-038) spanning projects, tasks, documents, and clients requires full-text search with RBAC-filtered results. Elasticsearch provides sub-second search across large datasets with relevance ranking and fuzzy matching.

#### File Storage: AWS S3

- **Why S3:** Document management requires up to 500MB per file and 1TB+ total storage (NFR-015). S3 provides virtually unlimited, cost-effective storage with built-in versioning, encryption at rest (AES-256), and lifecycle policies for compliance retention.

---

## 4. Database Strategy

### Overview

- **Primary:** PostgreSQL 16 -- all transactional data
- **Cache:** Redis 7 -- sessions, dashboard cache, rate limit counters, timer state
- **Search:** Elasticsearch 8 -- full-text search index (synced from PostgreSQL)
- **Files:** AWS S3 -- document storage with versioning

### Multi-Tenancy Strategy

Client data isolation uses **row-level filtering** with a mandatory `client_id` foreign key on all client-scoped tables. A PostgreSQL Row-Level Security (RLS) policy ensures queries from client user sessions automatically filter by their `client_id`. This satisfies SOC2 confidentiality requirements (NFR-018) and FR-036.

### Schema Design Principles

1. **UUIDs for primary keys** -- prevents sequential ID enumeration (security)
2. **Timestamps on all tables** -- `created_at`, `updated_at` for audit compliance
3. **Soft deletes** -- `deleted_at` column on critical tables (SOC2 data retention)
4. **Immutable audit log** -- append-only `audit_logs` table with 2-year retention
5. **Normalized structure** -- 3NF for transactional data; denormalized views for dashboards

### Core Tables (Summary)

| Table | Purpose | Key Relationships |
|---|---|---|
| users | All platform users (internal + client) | -> roles, -> clients |
| roles | RBAC role definitions | -> permissions |
| permissions | Granular permission flags | -> roles (M:M) |
| user_roles | User-to-role mapping | users M:M roles |
| clients | Client organizations | -> projects |
| projects | Project records | -> clients, -> users |
| project_members | Project team assignments | projects M:M users |
| tasks | Tasks within projects | -> projects, -> users |
| task_dependencies | Task predecessor/successor links | tasks M:M tasks |
| milestones | Project milestones | -> projects |
| time_entries | Logged hours | -> users, -> projects, -> tasks |
| invoices | Generated invoices | -> clients, -> projects |
| invoice_line_items | Invoice detail lines | -> invoices, -> time_entries |
| billing_rates | Rate configuration hierarchy | -> clients, -> projects, -> roles |
| documents | Uploaded files | -> projects, -> users |
| document_versions | File version history | -> documents |
| document_comments | Comments on documents | -> documents, -> users |
| messages | Client-team communication | -> projects, -> users |
| message_threads | Threaded conversations | -> projects |
| notifications | In-app notification records | -> users |
| notification_preferences | User notification settings | -> users |
| audit_logs | Immutable audit trail | -> users |
| integration_configs | Third-party integration settings | -> clients |
| resource_allocations | Team member assignments with hours | -> users, -> projects |
| nps_scores | Client satisfaction tracking | -> clients, -> projects |
| sessions | Active user sessions for management | -> users |

See `system_design.json` for complete column-level schema definition.

---

## 5. Security Architecture

### SOC2 Compliance Controls

The platform is designed to satisfy SOC2 Type II trust service criteria: **Security, Availability, and Confidentiality**.

```
+--------------------------------------------------------------------+
|                     SECURITY ARCHITECTURE                           |
|                                                                      |
|  PERIMETER:                                                         |
|  +--------------------------------------------------------------+   |
|  | Nginx Reverse Proxy                                           |   |
|  | - TLS 1.2+ termination (NFR-005)                             |   |
|  | - Rate limiting: 10 req/min on /auth (NFR-020)               |   |
|  | - CORS whitelist                                              |   |
|  | - Request size limits (500MB for uploads)                     |   |
|  | - WAF rules (OWASP Top 10 protection)                        |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  APPLICATION:                                                       |
|  +--------------------------------------------------------------+   |
|  | Authentication Layer                                          |   |
|  | - JWT access tokens (15 min expiry, RS256)                   |   |
|  | - Refresh tokens (Redis, 7-day TTL)                          |   |
|  | - TOTP 2FA (mandatory for all users, FR-034)                 |   |
|  | - Google Workspace SSO (SAML 2.0, FR-046)                    |   |
|  | - Account lockout after 5 failures (15 min, NFR-020)         |   |
|  | - Session timeout after 30 min inactivity (FR-048)           |   |
|  | - Password policy: 12+ chars, complexity, 90-day expiry      |   |
|  |   (FR-047)                                                    |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | Authorization Layer (RBAC, FR-033)                            |   |
|  | Roles: Admin, Executive, PM, Team Lead, Team Member,         |   |
|  |        Finance Manager, Client User                           |   |
|  | - Permission matrix per role per resource per action          |   |
|  | - Client data isolation via tenant_id filtering (FR-036)     |   |
|  | - PostgreSQL Row-Level Security policies                      |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | Audit & Monitoring (FR-035)                                   |   |
|  | - All CRUD operations logged with before/after values        |   |
|  | - Login/logout events with IP, user-agent                    |   |
|  | - Permission changes logged                                   |   |
|  | - Export activities tracked                                   |   |
|  | - Immutable audit log (append-only, 2-year retention)        |   |
|  | - Separate audit database / table with integrity checks      |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  DATA:                                                              |
|  +--------------------------------------------------------------+   |
|  | - AES-256 encryption at rest (PostgreSQL, S3, Redis)         |   |
|  | - TLS 1.2+ for all data in transit (NFR-005)                 |   |
|  | - bcrypt password hashing (cost factor 12)                   |   |
|  | - Encrypted backup storage with 1-hour RPO (NFR-012)         |   |
|  | - PII data classification and handling per GDPR (NFR-007)    |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  INPUT VALIDATION:                                                  |
|  +--------------------------------------------------------------+   |
|  | - Server-side validation on ALL inputs (NFR-014)             |   |
|  | - Parameterized queries (Prisma ORM) -- SQL injection        |   |
|  | - Output encoding -- XSS prevention                          |   |
|  | - CSRF tokens on state-changing requests                     |   |
|  | - Content Security Policy headers                            |   |
|  | - File upload type/size validation                           |   |
|  +--------------------------------------------------------------+   |
+--------------------------------------------------------------------+
```

### RBAC Permission Matrix

| Resource | Admin | Executive | PM | Team Lead | Team Member | Finance Mgr | Client User |
|---|---|---|---|---|---|---|---|
| Projects | CRUD | Read | CRUD | Read | Read | Read | Read (own) |
| Tasks | CRUD | Read | CRUD | CRUD | CRU (own) | - | Read (own) |
| Time Entries | CRUD | Read | Read/Approve | Read/Approve | CRU (own) | Read | - |
| Invoices | CRUD | Read | Read | - | - | CRUD | Read (own) |
| Documents | CRUD | Read | CRUD | CRUD | CRU | Read | Read (own) |
| Users | CRUD | Read | Read | Read | Read (self) | Read | Read (self) |
| Reports | Full | Full | Filtered | Filtered | Own | Financial | - |
| Integrations | CRUD | Read | Read | - | - | Config QB | - |
| Audit Logs | Read | Read | - | - | - | - | - |
| Client Portal | - | - | - | - | - | - | Full (own) |

---

## 6. Integration Architecture

### Integration Pattern: Event-Driven with Circuit Breaker

All integrations follow a consistent pattern:
1. Internal events trigger integration actions via an event bus
2. Integration adapters translate internal events to external API calls
3. Circuit breaker pattern prevents cascading failures from external service outages
4. Retry queues with exponential backoff handle transient failures
5. Core platform functions operate independently of integration availability

```
+-------------------------------------------------------------------+
|                   INTEGRATION ARCHITECTURE                         |
|                                                                     |
|  INTERNAL EVENT BUS (in-process)                                   |
|  +--------------------------------------------------------------+  |
|  | invoice.finalized | task.assigned | milestone.completed |     |  |
|  | document.uploaded | deadline.approaching | message.sent  |     |  |
|  +----------+-------------------+-------------------+-----------+  |
|             |                   |                   |              |
|  +----------v------+  +--------v--------+  +-------v---------+   |
|  | QuickBooks       |  | Slack            |  | Google Calendar  |  |
|  | Adapter          |  | Adapter          |  | Adapter          |  |
|  |                  |  |                  |  |                  |  |
|  | - OAuth 2.0 auth |  | - Bot token auth |  | - OAuth 2.0 auth |  |
|  | - Invoice push   |  | - Channel msgs   |  | - Event create   |  |
|  | - Payment pull   |  | - DM notifs      |  | - Event update   |  |
|  | - Retry queue    |  | - Webhook listen |  | - Bi-dir sync    |  |
|  | - Circuit breaker|  | - Circuit breaker|  | - Circuit breaker|  |
|  +------------------+  +------------------+  +------------------+  |
|                                                                     |
|  +------------------+  +------------------+                        |
|  | SendGrid         |  | Figma/GitHub     |                       |
|  | Adapter          |  | Adapter (basic)  |                       |
|  |                  |  |                  |                        |
|  | - API key auth   |  | - API key / OAuth|                       |
|  | - Template emails|  | - Read-only fetch|                       |
|  | - Delivery track |  | - Thumbnail gen  |                       |
|  +------------------+  +------------------+                        |
+-------------------------------------------------------------------+
```

### Integration Details

| Integration | Auth Method | Sync Type | Rate Limit Handling | Failure Mode |
|---|---|---|---|---|
| QuickBooks Online | OAuth 2.0 | Bi-directional (push invoices, pull payments) | Token bucket, 500 req/min | Queue + retry, manual reconciliation |
| Slack | Bot Token (OAuth 2.0) | Outbound push (notifications) | 1 msg/sec per channel | Queue + retry, fallback to email |
| Google Calendar | OAuth 2.0 | Bi-directional (event CRUD) | 100 req/100sec per user | Exponential backoff |
| SendGrid | API Key | Outbound push (emails) | 100 emails/sec | Queue + retry, log failures |
| Figma | OAuth 2.0 | Read-only (thumbnails) | 30 req/min | Cache thumbnails, graceful degrade |
| GitHub | OAuth 2.0 | Read-only (commit activity) | 5000 req/hr | Cache responses, graceful degrade |

---

## 7. Deployment Architecture

### Cloud Infrastructure (AWS)

```
+--------------------------------------------------------------------+
|                        AWS CLOUD                                    |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  |  VPC (10.0.0.0/16)                                           |   |
|  |                                                                |   |
|  |  PUBLIC SUBNET                                                |   |
|  |  +----------------------------------------------------------+ |   |
|  |  | Application Load Balancer (ALB)                           | |   |
|  |  | - TLS termination (ACM certificate)                       | |   |
|  |  | - WAF rules attached                                      | |   |
|  |  | - Health checks                                           | |   |
|  |  +----+-----------------------------------------------------+ |   |
|  |       |                                                        |   |
|  |  PRIVATE SUBNET (App Tier)                                    |   |
|  |  +----------------------------------------------------------+ |   |
|  |  | ECS Fargate Cluster                                       | |   |
|  |  |                                                            | |   |
|  |  | +------------------+  +------------------+                | |   |
|  |  | | API Service      |  | API Service      |  (auto-scale  | |   |
|  |  | | Container (x2+)  |  | Container (x2+)  |   2-6 tasks)  | |   |
|  |  | | Node.js:3000     |  | Node.js:3000     |                | |   |
|  |  | +------------------+  +------------------+                | |   |
|  |  |                                                            | |   |
|  |  | +------------------+                                      | |   |
|  |  | | Worker Service   |  (background jobs: sync, reports,   | |   |
|  |  | | Container (x1+)  |   email, notifications)              | |   |
|  |  | | Node.js:3001     |                                      | |   |
|  |  | +------------------+                                      | |   |
|  |  +----------------------------------------------------------+ |   |
|  |                                                                |   |
|  |  PRIVATE SUBNET (Data Tier)                                   |   |
|  |  +----------------------------------------------------------+ |   |
|  |  | RDS PostgreSQL 16    | ElastiCache Redis  | ES Domain    | |   |
|  |  | (Multi-AZ, encrypted)| (Cluster mode)     | (2-node)     | |   |
|  |  | db.r6g.large         | cache.r6g.large    |              | |   |
|  |  +----------------------------------------------------------+ |   |
|  |                                                                |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | S3 Bucket (Documents)  | S3 Bucket (Audit Logs)              |   |
|  | - Versioning enabled   | - Object lock (WORM)                |   |
|  | - AES-256 SSE          | - 2-year retention policy           |   |
|  | - Lifecycle policies   | - Cross-region replication           |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | CloudFront CDN                                                |   |
|  | - React SPA static assets (S3 origin)                        |   |
|  | - Cache headers, gzip/brotli compression                     |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | Monitoring & Observability                                    |   |
|  | - CloudWatch (metrics, alarms, logs)                          |   |
|  | - X-Ray (distributed tracing)                                 |   |
|  | - SNS (alerting)                                              |   |
|  +--------------------------------------------------------------+   |
+--------------------------------------------------------------------+
```

### Deployment Pipeline (CI/CD)

```
Developer Push --> GitHub Actions Pipeline:
  1. Lint + Type Check (ESLint, tsc)
  2. Unit Tests (Jest, coverage >= 80%)
  3. Integration Tests (Supertest + test DB)
  4. Security Scan (npm audit, Snyk)
  5. Docker Build + Push to ECR
  6. Deploy to Staging (ECS blue/green)
  7. E2E Tests (Playwright)
  8. Manual Approval Gate (production)
  9. Deploy to Production (ECS blue/green)
  10. Smoke Tests + Health Checks
```

### Environment Strategy

| Environment | Purpose | Infrastructure |
|---|---|---|
| Development | Local development | Docker Compose (PostgreSQL, Redis, Elasticsearch, S3-compatible MinIO) |
| Staging | Pre-production testing, client UAT | AWS (scaled-down, same architecture) |
| Production | Live system | AWS (full scale, Multi-AZ, auto-scaling) |

### Scalability

- **Horizontal scaling:** ECS Fargate auto-scales API containers from 2 to 6 based on CPU/memory utilization
- **Database scaling:** RDS read replicas for reporting queries; connection pooling via PgBouncer
- **Cache scaling:** Redis cluster mode for session distribution across scaled API instances
- **CDN:** CloudFront for static assets and document downloads (reduces origin load)
- **Target:** Support 330+ concurrent users (NFR-003) with sub-2-second page loads (NFR-001)

### Backup and Disaster Recovery

| Component | Backup Strategy | RPO | RTO |
|---|---|---|---|
| PostgreSQL (RDS) | Automated daily snapshots + continuous WAL archiving | 1 hour | 4 hours |
| Redis | AOF persistence + daily RDB snapshots | 1 hour | 1 hour |
| S3 Documents | Cross-region replication + versioning | Near-zero | 1 hour |
| S3 Audit Logs | Object lock (WORM) + cross-region replication | Near-zero | 1 hour |
| Elasticsearch | Daily snapshots to S3 | 24 hours | 4 hours |

---

## Appendix A: Technology Version Matrix

| Component | Version | EOL / Support |
|---|---|---|
| Node.js | 20 LTS | April 2026 |
| TypeScript | 5.x | Active |
| React | 18.x | Active |
| Express | 4.x | Active |
| PostgreSQL | 16 | November 2028 |
| Redis | 7.x | Active |
| Elasticsearch | 8.x | Active |
| Docker | 24.x | Active |
| Prisma | 5.x | Active |
| Nginx | 1.25+ | Active |

## Appendix B: Key Architecture Decision Records (ADRs)

### ADR-001: Modular Monolith over Microservices
- **Status:** Accepted
- **Context:** 11 modules, 5-month timeline, small/medium team
- **Decision:** Modular monolith with clear module boundaries
- **Rationale:** Faster delivery, simpler deployment, lower operational overhead. Module boundaries support future extraction to microservices if scaling demands it.

### ADR-002: PostgreSQL over MongoDB
- **Status:** Accepted
- **Context:** SOC2 compliance, financial data (invoicing), relational data model
- **Decision:** PostgreSQL as sole primary database
- **Rationale:** ACID compliance, row-level security for tenant isolation, mature tooling for audit trails, strong referential integrity for financial data.

### ADR-003: JWT + Redis over Session-based Auth
- **Status:** Accepted
- **Context:** RESTful API architecture, multiple client types, horizontal scaling
- **Decision:** Stateless JWT access tokens + Redis-backed refresh tokens
- **Rationale:** Supports horizontal scaling without sticky sessions. Redis enables fast token revocation (logout, session timeout). Short-lived access tokens limit exposure window.

### ADR-004: AWS over Azure/GCP
- **Status:** Accepted
- **Context:** Cloud hosting preference, SOC2 compliance, service maturity
- **Decision:** AWS as primary cloud provider
- **Rationale:** Broadest SOC2-compliant service portfolio. ECS Fargate eliminates server management. RDS Multi-AZ provides high availability. S3 Object Lock supports immutable audit log storage.

### ADR-005: Event-driven Integration Pattern
- **Status:** Accepted
- **Context:** 4+ external integrations, requirement for graceful degradation
- **Decision:** Internal event bus with adapter pattern per integration
- **Rationale:** Core platform operates independently of integration availability. Circuit breakers prevent cascading failures. Consistent retry and error handling across all integrations.

---

*End of High Level Design Document*
