# Security Checklist — TechNova Solutions Client Project Management Platform

**Document Version:** 1.0
**Date:** 2026-03-12
**Compliance Targets:** OWASP Top 10, SOC2 Type II, GDPR
**Domain:** Professional Services / Digital Agency Management (SaaS)

---

## 1. OWASP Top 10 (2021) Checklist

### A01: Broken Access Control
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1.1 | RBAC enforced on every API endpoint for all 7 roles | [ ] | Admin, Executive, PM, Team Lead, Team Member, Finance Manager, Client User |
| 1.2 | Deny by default — endpoints require explicit role allowance | [ ] | Middleware rejects unrecognized roles |
| 1.3 | CORS restricted to configured origins only | [ ] | CORS_ORIGIN env var enforced |
| 1.4 | Directory listing disabled on web server | [ ] | Nginx config verified |
| 1.5 | JWT token contains minimal claims (no sensitive data) | [ ] | Only userId, role, tenantId in payload |
| 1.6 | File access permissions enforce ownership checks | [ ] | Document download checks project membership |
| 1.7 | IDOR (Insecure Direct Object Reference) prevention | [ ] | All resource access checks ownership/membership |
| 1.8 | Admin panel accessible only to Administrator role | [ ] | /api/admin/* requires admin role |
| 1.9 | Client portal enforces tenant-scoped data access | [ ] | All client queries filtered by tenant_id |
| 1.10 | Rate limiting on sensitive endpoints | [ ] | Auth endpoints: 10/min; global: 100/min |

### A02: Cryptographic Failures
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 2.1 | All data in transit encrypted with TLS 1.2+ | [ ] | HTTPS enforced; HTTP redirects to HTTPS |
| 2.2 | Data at rest encrypted with AES-256 | [ ] | PostgreSQL TDE; S3 SSE-AES256 |
| 2.3 | Passwords hashed with bcrypt (cost factor >= 12) | [ ] | BCRYPT_SALT_ROUNDS=12 |
| 2.4 | JWT secrets are strong (>= 32 characters) | [ ] | JWT_ACCESS_SECRET, JWT_REFRESH_SECRET |
| 2.5 | No sensitive data in URL query parameters | [ ] | Tokens, passwords never in URLs |
| 2.6 | Sensitive data not logged | [ ] | Passwords, tokens filtered from logs |
| 2.7 | TOTP secrets encrypted at rest | [ ] | Stored encrypted in database |
| 2.8 | Refresh tokens stored hashed (not plaintext) | [ ] | bcrypt or SHA-256 hashed |
| 2.9 | S3 pre-signed URLs have short expiration | [ ] | Max 15 minutes |
| 2.10 | Database connection uses SSL in production | [ ] | DB_SSL=true in production |

### A03: Injection
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 3.1 | All database queries use parameterized statements | [ ] | No string concatenation in SQL |
| 3.2 | ORM used for all standard queries (Prisma) | [ ] | Raw SQL audited separately |
| 3.3 | Input validation on all API request bodies | [ ] | Joi/Zod schema validation |
| 3.4 | SQL injection tested on all text input fields | [ ] | Automated OWASP ZAP scan |
| 3.5 | NoSQL injection prevention (if applicable) | [ ] | N/A — PostgreSQL only |
| 3.6 | OS command injection prevention | [ ] | No shell exec with user input |
| 3.7 | LDAP injection prevention (if applicable) | [ ] | N/A — no LDAP |
| 3.8 | CSV injection prevention in data exports | [ ] | Escape formulas in CSV exports |
| 3.9 | Data migration import sanitizes all imported values | [ ] | CSV/Excel import validates and escapes |

### A04: Insecure Design
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 4.1 | Threat modeling completed for all modules | [ ] | Focus on auth, client portal, invoicing |
| 4.2 | Business logic abuse prevention | [ ] | Rate limits, validation on workflows |
| 4.3 | Separation of duties for financial operations | [ ] | Invoice finalization requires finance_manager/admin |
| 4.4 | Account lockout after failed login attempts | [ ] | 5 attempts, 15-minute lockout |
| 4.5 | Multi-tenancy isolation by design | [ ] | tenant_id enforced at data layer |
| 4.6 | Secure password reset flow | [ ] | Token-based with expiration |

### A05: Security Misconfiguration
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 5.1 | Security headers configured (Helmet.js) | [ ] | X-Frame-Options, CSP, X-Content-Type-Options, Strict-Transport-Security |
| 5.2 | No default credentials in production | [ ] | Seed data uses bcrypt-hashed passwords |
| 5.3 | Error messages do not leak stack traces | [ ] | Production NODE_ENV hides details |
| 5.4 | Unnecessary HTTP methods disabled | [ ] | Only required methods per route |
| 5.5 | Debug mode disabled in production | [ ] | NODE_ENV=production |
| 5.6 | Server version headers removed | [ ] | X-Powered-By removed by Helmet |
| 5.7 | File upload content-type validation | [ ] | Validate MIME type, not just extension |
| 5.8 | Docker containers run as non-root | [ ] | USER node in Dockerfile |
| 5.9 | Environment variables not hardcoded | [ ] | .env file with .env.example template |
| 5.10 | Nginx security hardening | [ ] | Buffer overflow protection, rate limiting |

### A06: Vulnerable and Outdated Components
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 6.1 | npm audit shows zero critical/high vulnerabilities | [ ] | Backend and frontend |
| 6.2 | Snyk or Dependabot configured for dependency scanning | [ ] | Automated PR on vulnerability discovery |
| 6.3 | Node.js version is LTS (20.x) | [ ] | No EOL runtime |
| 6.4 | All dependencies at latest stable versions | [ ] | express, react, prisma, etc. |
| 6.5 | Docker base images are official and up-to-date | [ ] | node:20-alpine |
| 6.6 | PostgreSQL at supported version (16) | [ ] | Receives security patches |

### A07: Identification and Authentication Failures
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 7.1 | Mandatory 2FA for all users | [ ] | TOTP + SMS fallback |
| 7.2 | Password policy enforced (12 char, complexity, expiry, reuse) | [ ] | FR-047 |
| 7.3 | Account lockout after 5 failed attempts | [ ] | 15-minute lockout (NFR-020) |
| 7.4 | Session timeout after 30 minutes inactivity | [ ] | FR-048 |
| 7.5 | JWT access tokens have short expiry (15 minutes) | [ ] | JWT_ACCESS_EXPIRY=15m |
| 7.6 | Refresh token rotation on each use | [ ] | Old token invalidated |
| 7.7 | Login does not reveal whether email exists | [ ] | Generic "Invalid credentials" |
| 7.8 | SSO integration with Google Workspace (SAML/OIDC) | [ ] | FR-046 |
| 7.9 | Invitation tokens are single-use and expire | [ ] | FR-041 |
| 7.10 | Password reset tokens expire after configurable period | [ ] | Default 1 hour |

### A08: Software and Data Integrity Failures
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 8.1 | CI/CD pipeline includes security scanning | [ ] | npm audit, OWASP ZAP in GitHub Actions |
| 8.2 | Package integrity verified (package-lock.json) | [ ] | npm ci in production builds |
| 8.3 | Docker image scanning for vulnerabilities | [ ] | Trivy or Snyk container scan |
| 8.4 | Subresource Integrity (SRI) for CDN assets | [ ] | If any CDN dependencies used |
| 8.5 | Signed commits and protected main branch | [ ] | GitHub branch protection rules |

### A09: Security Logging and Monitoring Failures
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 9.1 | Comprehensive audit trail for all data changes | [ ] | FR-035; immutable logs |
| 9.2 | Login/logout events logged | [ ] | With timestamp, IP, user agent |
| 9.3 | Failed authentication attempts logged | [ ] | For brute-force detection |
| 9.4 | Permission violations logged | [ ] | 403 responses logged with context |
| 9.5 | Audit logs retained >= 2 years | [ ] | NFR-013 |
| 9.6 | Audit logs stored separately from app data | [ ] | Immutable, append-only storage |
| 9.7 | Alerting on suspicious activity | [ ] | Repeated 403s, lockouts, unusual patterns |
| 9.8 | Log aggregation (CloudWatch) | [ ] | Structured JSON logging (Winston) |
| 9.9 | No sensitive data in logs | [ ] | Passwords, tokens redacted |

### A10: Server-Side Request Forgery (SSRF)
| # | Check | Status | Notes |
|---|-------|--------|-------|
| 10.1 | URL validation on Figma integration links | [ ] | Only figma.com domains accepted |
| 10.2 | Webhook URLs validated (Slack, QuickBooks) | [ ] | Whitelist known domains |
| 10.3 | Internal network addresses blocked in URL inputs | [ ] | 127.0.0.1, 10.x, 192.168.x blocked |
| 10.4 | S3 pre-signed URL generation does not accept user-controlled buckets | [ ] | Bucket name hardcoded |

---

## 2. SOC2 Type II Specific Checklist

### Security Trust Service Criteria
| # | Check | Status | SOC2 Control | Notes |
|---|-------|--------|-------------|-------|
| S2-01 | Role-based access control with 7 roles | [ ] | CC6.1 | Permission matrix documented and tested |
| S2-02 | Mandatory multi-factor authentication | [ ] | CC6.1 | TOTP/SMS for all users |
| S2-03 | Unique user accounts (no shared credentials) | [ ] | CC6.2 | Email-based accounts, no anonymous access |
| S2-04 | User provisioning and deprovisioning process | [ ] | CC6.2 | Admin invitations; deactivation workflow |
| S2-05 | Access reviews and recertification | [ ] | CC6.3 | Admin can view and audit user access |
| S2-06 | Encryption in transit (TLS 1.2+) | [ ] | CC6.7 | All communications encrypted |
| S2-07 | Encryption at rest (AES-256) | [ ] | CC6.7 | Database and file storage encrypted |
| S2-08 | Comprehensive audit trails | [ ] | CC7.2 | All data changes, logins, access events |
| S2-09 | Audit log immutability | [ ] | CC7.2 | Append-only storage; tamper detection |
| S2-10 | Audit log retention (>= 2 years) | [ ] | CC7.2 | NFR-013 compliant |
| S2-11 | Incident response procedures documented | [ ] | CC7.3 | Escalation paths defined |
| S2-12 | Vulnerability scanning (monthly) | [ ] | CC7.1 | npm audit + OWASP ZAP |
| S2-13 | Penetration testing (annual) | [ ] | CC7.1 | Third-party pen test |
| S2-14 | Change management process | [ ] | CC8.1 | PR reviews, CI/CD gates |
| S2-15 | Secure coding standards enforced | [ ] | CC8.1 | ESLint security rules, code review |

### Availability Trust Service Criteria
| # | Check | Status | SOC2 Control | Notes |
|---|-------|--------|-------------|-------|
| A2-01 | 99.5% uptime SLA during business hours | [ ] | A1.1 | Monitoring and alerting in place |
| A2-02 | Automated backups (RPO <= 1 hour) | [ ] | A1.2 | Hourly PostgreSQL backups |
| A2-03 | Tested restore procedures (RTO <= 4 hours) | [ ] | A1.2 | Quarterly restore drills |
| A2-04 | Health check endpoints | [ ] | A1.1 | /health endpoint on backend |
| A2-05 | Graceful degradation on external service failure | [ ] | A1.1 | Circuit breaker pattern |
| A2-06 | Planned maintenance windows (< 2 hours/month) | [ ] | A1.2 | 48-hour advance notice |

### Confidentiality Trust Service Criteria
| # | Check | Status | SOC2 Control | Notes |
|---|-------|--------|-------------|-------|
| C2-01 | Multi-tenant data isolation | [ ] | C1.1 | tenant_id on all client-scoped tables |
| C2-02 | Cross-tenant access prevention verified | [ ] | C1.1 | Penetration testing confirms isolation |
| C2-03 | Data classification implemented | [ ] | C1.2 | PII, financial data identified and protected |
| C2-04 | Data retention policies defined | [ ] | C1.2 | Audit logs: 2 years; user data per GDPR |
| C2-05 | Secure data disposal on account deletion | [ ] | C1.2 | GDPR erasure with audit trail preservation |
| C2-06 | Access to production data restricted | [ ] | C1.1 | Only authorized DevOps/admin personnel |

---

## 3. GDPR Compliance Checklist

| # | Check | Status | GDPR Article | Notes |
|---|-------|--------|-------------|-------|
| G-01 | Consent obtained before processing personal data | [ ] | Art. 6 | Consent dialog on first access |
| G-02 | Privacy policy accessible and clear | [ ] | Art. 13 | Link in footer and during registration |
| G-03 | Data subject access requests supported | [ ] | Art. 15 | Complete data export within 30 days |
| G-04 | Right to erasure (right to be forgotten) | [ ] | Art. 17 | Anonymize/delete personal data on request |
| G-05 | Data portability supported | [ ] | Art. 20 | Export in machine-readable format (JSON/CSV) |
| G-06 | Data processing records maintained | [ ] | Art. 30 | Processing activities documented |
| G-07 | Data Protection Impact Assessment (DPIA) | [ ] | Art. 35 | Completed for high-risk processing |
| G-08 | Data breach notification within 72 hours | [ ] | Art. 33 | Incident response plan includes notification |
| G-09 | Cross-border data transfer protections | [ ] | Art. 46 | Standard contractual clauses if applicable |
| G-10 | GDPR request tracking and audit | [ ] | Art. 12 | Request log with status and resolution dates |
| G-11 | Consent withdrawal mechanism | [ ] | Art. 7 | User can withdraw consent from settings |
| G-12 | Age verification (if applicable) | [ ] | Art. 8 | N/A — B2B platform, no minors |

---

## 4. SaaS Domain Security Checklist

### Multi-Tenancy Security
| # | Check | Status | Notes |
|---|-------|--------|-------|
| MT-01 | tenant_id column on every client-scoped database table | [ ] | Verified in schema migration |
| MT-02 | Application-level query filtering always includes tenant_id | [ ] | Middleware enforces tenant context |
| MT-03 | No raw SQL queries bypass tenant isolation | [ ] | Code audit completed |
| MT-04 | API responses never include cross-tenant data | [ ] | Automated tests for every endpoint |
| MT-05 | File storage paths include tenant isolation (S3 prefixes) | [ ] | /tenants/{tenantId}/documents/* |
| MT-06 | WebSocket connections scoped to tenant | [ ] | Notifications filtered by tenant |
| MT-07 | Search index partitioned by tenant | [ ] | Elasticsearch tenant-filtered queries |
| MT-08 | Audit logs include tenant context | [ ] | tenant_id in every audit entry |
| MT-09 | Database Row-Level Security (RLS) policies active | [ ] | PostgreSQL RLS as defense-in-depth |

### API Security
| # | Check | Status | Notes |
|---|-------|--------|-------|
| API-01 | Rate limiting on all endpoints | [ ] | Global: 100/min; Auth: 10/min |
| API-02 | Request payload size limits | [ ] | Express body-parser limit: 10MB (files via S3) |
| API-03 | API versioning strategy in place | [ ] | /api/v1/* path prefix ready |
| API-04 | OpenAPI/Swagger documentation up to date | [ ] | Auto-generated from route definitions |
| API-05 | CORS whitelist configured | [ ] | Only frontend URL allowed |
| API-06 | Content-Type enforcement (accept only application/json) | [ ] | Except multipart for file uploads |
| API-07 | Response does not expose internal error details | [ ] | Generic errors in production |
| API-08 | Pagination enforced on list endpoints | [ ] | Max page size: 100 |

### Session and Token Security
| # | Check | Status | Notes |
|---|-------|--------|-------|
| ST-01 | JWT access token expiry: 15 minutes | [ ] | Short-lived access tokens |
| ST-02 | Refresh token expiry: 7 days | [ ] | Longer-lived but rotated |
| ST-03 | Refresh token rotation on each use | [ ] | Old token invalidated |
| ST-04 | Refresh token stored httpOnly, secure, sameSite | [ ] | If cookie-based |
| ST-05 | Session timeout: 30 minutes inactivity | [ ] | With 5-minute warning |
| ST-06 | Concurrent session limiting (optional) | [ ] | Configurable max sessions per user |
| ST-07 | Logout invalidates all tokens | [ ] | Refresh token revoked on logout |

### Infrastructure Security
| # | Check | Status | Notes |
|---|-------|--------|-------|
| IS-01 | Docker containers run as non-root user | [ ] | USER node in Dockerfile |
| IS-02 | Docker images scanned for vulnerabilities | [ ] | Trivy in CI pipeline |
| IS-03 | Secrets managed via environment variables (not code) | [ ] | .env not committed; .env.example provided |
| IS-04 | Database credentials rotated periodically | [ ] | Rotation schedule documented |
| IS-05 | Network security groups restrict access | [ ] | DB only accessible from app tier |
| IS-06 | WAF configured for public endpoints | [ ] | AWS WAF or CloudFront |
| IS-07 | DDoS protection enabled | [ ] | AWS Shield Standard |
| IS-08 | SSL/TLS certificates auto-renewed | [ ] | Let's Encrypt or ACM |

### Integration Security
| # | Check | Status | Notes |
|---|-------|--------|-------|
| INT-01 | OAuth 2.0 tokens stored encrypted | [ ] | QuickBooks, Slack, Google tokens |
| INT-02 | OAuth token refresh handled automatically | [ ] | Token expiry managed by integration service |
| INT-03 | Integration webhook endpoints validate signatures | [ ] | Slack, QuickBooks webhook verification |
| INT-04 | Circuit breaker pattern on external API calls | [ ] | Prevent cascading failures |
| INT-05 | Integration sync errors logged and alertable | [ ] | Error dashboard for admins |
| INT-06 | Third-party API rate limits respected | [ ] | Backoff and queue mechanisms |

---

## 5. Security Testing Schedule

| Activity | Frequency | Tool | Owner |
|----------|-----------|------|-------|
| Dependency vulnerability scan | Every CI build | npm audit, Snyk | CI/CD Pipeline |
| Static Application Security Testing (SAST) | Every PR | ESLint security rules | Developer |
| Dynamic Application Security Testing (DAST) | Weekly | OWASP ZAP | QA Engineer |
| Penetration testing | Annually (pre-launch + annual) | Third-party | Security Consultant |
| Cross-tenant isolation testing | Every sprint | Automated test suite | QA Engineer |
| RBAC matrix testing | Every sprint | Automated test suite | QA Engineer |
| Container image scanning | Every build | Trivy | CI/CD Pipeline |
| SSL/TLS configuration audit | Monthly | SSL Labs, testssl.sh | DevOps |
| Backup/restore testing | Quarterly | Manual procedure | DevOps |

---

## Summary

| Category | Total Checks | Critical | High | Medium |
|----------|-------------|----------|------|--------|
| OWASP Top 10 | 61 | 25 | 22 | 14 |
| SOC2 Type II | 27 | 15 | 8 | 4 |
| GDPR | 12 | 6 | 4 | 2 |
| SaaS Domain | 41 | 15 | 18 | 8 |
| **TOTAL** | **141** | **61** | **52** | **28** |
