# Statement of Work (SOW)

**Project:** Unified Agency Management Platform — Phase 1
**Client:** TechNova Solutions
**Vendor:** [Vendor Name]
**SOW Reference:** SOW-TECHNOVA-2026-001
**Version:** 1.0
**Date:** 2026-03-12
**Status:** Draft — For Client Review and Approval

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Scope of Work](#2-scope-of-work)
3. [Deliverables Table](#3-deliverables-table)
4. [Project Timeline](#4-project-timeline)
5. [Team Structure](#5-team-structure)
6. [Assumptions](#6-assumptions)
7. [Acceptance Criteria](#7-acceptance-criteria)
8. [Change Management Process](#8-change-management-process)
9. [Sign-Off](#9-sign-off)

---

## 1. Project Overview

### 1.1 Background

TechNova Solutions is a digital agency employing approximately 150 people, managing over 40 active client projects across healthcare, finance, and technology verticals. The organization currently operates with a fragmented set of tools — spreadsheets for project tracking, manual time entry, email-based client communication, and shared drives for document storage — resulting in revenue leakage estimated at 15-20%, missed deadlines, and a prior security incident.

### 1.2 Objective

This Statement of Work defines the scope, deliverables, timeline, team structure, and acceptance criteria for the design, development, testing, and deployment of a **Unified Agency Management Platform (Phase 1)** — a cloud-hosted web application that will consolidate TechNova's project management, client communication, time tracking, invoicing, resource allocation, document management, and operational reporting into a single, secure platform.

### 1.3 Engagement Model

- **Methodology**: Agile (Scrum) with 2-week sprints
- **Duration**: 5 months (approximately 10 sprints)
- **Budget**: $150,000 (fixed price for Phase 1 scope)
- **Communication**: Weekly sprint reviews with TechNova product owner; daily standups within the development team; bi-weekly steering committee updates

### 1.4 Reference Documents

| Document | Location |
|---|---|
| Business Requirements Document (BRD) | `outputs/documents/BRD.md` |
| Functional Requirements Document (FRD) | `outputs/documents/FRD.md` |
| Requirement Specification | `outputs/requirements/requirement_spec.json` |

---

## 2. Scope of Work

### 2.1 In-Scope Modules and Features

The following modules and their associated functional requirements (as defined in the FRD) are included in this engagement:

| # | Module | Functional Requirements | Priority |
|---|---|---|---|
| 1 | Project Management | FR-001, FR-002, FR-003, FR-004, FR-005 | CRITICAL |
| 2 | Client Portal | FR-006, FR-007, FR-008, FR-009, FR-010 | CRITICAL |
| 3 | Time Tracking & Invoicing | FR-011, FR-012, FR-026, FR-027, FR-028 | CRITICAL |
| 4 | Resource Management | FR-013, FR-014, FR-015 | HIGH |
| 5 | Document Management | FR-016, FR-017, FR-018, FR-019 | HIGH |
| 6 | Integrations | FR-020, FR-021, FR-022, FR-023, FR-024, FR-025 | HIGH |
| 7 | Reporting & Analytics | FR-029, FR-030, FR-031, FR-032 | CRITICAL |
| 8 | Security & Access Control | FR-033, FR-034, FR-035, FR-036, FR-046, FR-047, FR-048 | CRITICAL |
| 9 | Platform & UX | FR-037, FR-038, FR-039 | HIGH |
| 10 | Administration | FR-040, FR-041 | CRITICAL |
| 11 | Data Migration | FR-042 | HIGH |

**Total Functional Requirements in Scope**: 44 (excludes FR-043, FR-044, FR-045 which are deferred to Phase 2)

### 2.2 Technical Scope

| Area | Scope |
|---|---|
| **Platform** | Responsive web application (desktop and tablet, minimum 768px viewport) |
| **Hosting** | Cloud-hosted (AWS, Azure, or GCP — to be determined during architecture phase) |
| **Integrations** | QuickBooks Online, Slack, Google Calendar, Figma (link/preview), GitHub (read-only), Google Workspace SSO |
| **Security** | RBAC, 2FA, SSO, audit trails, encryption (TLS 1.2+ / AES-256), client data isolation |
| **Compliance** | SOC2 Type II readiness design; GDPR compliance design |
| **Data Migration** | Bulk import tool for CSV/Excel migration of projects, clients, and time entries |
| **Performance** | Page load <= 2s; dashboard load <= 5s; API response <= 500ms (CRUD); 200 concurrent users |

### 2.3 Out of Scope

The following items are explicitly excluded from this engagement and may be addressed in a separate Phase 2 SOW:

1. Native mobile application (iOS/Android) — FR-043
2. AI-powered project estimation — FR-044
3. Advanced analytics and custom dashboards — FR-045
4. Deep Figma integration with real-time design sync
5. GitHub CI/CD pipeline visibility
6. NPS survey tool integration (manual entry only in Phase 1)
7. Multi-language / internationalization
8. Offline mode / PWA capabilities
9. Custom workflow builder
10. White-labeling / per-client branding
11. Integration with Jira, Asana, Monday.com, or other project management tools
12. Payroll calculations or HR management
13. Customer support / ticketing system
14. Hardware security keys (FIDO2/WebAuthn) for 2FA
15. On-premises deployment
16. Ongoing hosting, maintenance, and support (covered under a separate agreement)

---

## 3. Deliverables Table

| # | Deliverable | Description | Acceptance Criteria | Target Sprint |
|---|---|---|---|---|
| D-01 | Solution Architecture Document | Technical architecture including system design, technology stack, database schema, API design, integration architecture, deployment topology, and security architecture | Architecture reviewed and approved by TechNova technical stakeholder; addresses all NFRs | Sprint 1 |
| D-02 | UX Wireframes & Design Mockups | Wireframes for all major screens; high-fidelity mockups for client portal and executive dashboard; responsive layout specifications | Wireframes reviewed with 3-5 TechNova clients; approved by TechNova product owner | Sprint 1-2 |
| D-03 | Project Management Module | Fully functional project dashboard, project CRUD, task management with status tracking and dependencies, milestone management, Kanban and list views (FR-001 through FR-005) | All acceptance criteria for FR-001 through FR-005 verified through QA testing | Sprint 2-4 |
| D-04 | Security & Access Control Module | RBAC with 7 roles, 2FA (TOTP + SMS), audit trails, client data isolation, SSO, password policies, session management (FR-033 through FR-036, FR-046 through FR-048) | All acceptance criteria for FR-033 through FR-036, FR-046 through FR-048 verified; penetration test confirms no cross-tenant data access | Sprint 2-4 |
| D-05 | Administration Module | Admin panel for user management, roles, integrations, billing rates, system settings; email invitation onboarding (FR-040, FR-041) | All acceptance criteria for FR-040, FR-041 verified | Sprint 3-4 |
| D-06 | Time Tracking & Invoicing Module | Time tracking with timer/manual entry, billing rate configuration, time approval workflow, timesheet views, automated invoice generation (FR-011, FR-012, FR-026 through FR-028) | All acceptance criteria for FR-011, FR-012, FR-026 through FR-028 verified | Sprint 4-6 |
| D-07 | Document Management Module | Project document repository, version history, commenting, client approval workflow (FR-016 through FR-019) | All acceptance criteria for FR-016 through FR-019 verified | Sprint 4-5 |
| D-08 | Client Portal | Client dashboard, deliverable review/approval, messaging, timeline visualization, email notifications (FR-006 through FR-010) | All acceptance criteria for FR-006 through FR-010 verified; SUS score >= 75 with client user sample | Sprint 5-7 |
| D-09 | Resource Management Module | Visual resource board, assignment with conflict detection, capacity forecasting (FR-013 through FR-015) | All acceptance criteria for FR-013 through FR-015 verified | Sprint 5-6 |
| D-10 | Integrations Module | QuickBooks bi-directional sync, Slack notifications, Google Calendar sync, Figma link/preview, GitHub commit display, QuickBooks config panel (FR-020 through FR-025) | All acceptance criteria for FR-020 through FR-025 verified; integration error handling demonstrated | Sprint 5-8 |
| D-11 | Reporting & Analytics Module | Executive dashboard, profitability reports, configurable exports, NPS tracking (FR-029 through FR-032) | All acceptance criteria for FR-029 through FR-032 verified; dashboard loads within 5 seconds | Sprint 7-8 |
| D-12 | Platform & UX Features | Responsive web app, global search, notification center (FR-037 through FR-039) | Application functional on all target viewports; search returns results within 2 seconds; notifications delivered within 5 seconds | Sprint 3-8 |
| D-13 | Data Migration Tool | Bulk import wizard for CSV/Excel with validation, dry-run mode, and error reporting (FR-042) | Successful test migration of TechNova sample data with zero data loss; validation errors reported correctly | Sprint 8-9 |
| D-14 | QA Test Suite | Comprehensive test plan, test cases for all FRs, automated regression tests, performance test results, security scan results | Test coverage >= 80% of FRs; zero critical/high defects; performance targets met | Sprint 8-9 |
| D-15 | User Documentation | User guides for internal users (admin, PM, team member) and client portal users; video walkthroughs for key workflows | Documentation reviewed and approved by TechNova product owner | Sprint 9 |
| D-16 | Production Deployment | Deployed application in production cloud environment with monitoring, alerting, and backup configuration | Application accessible at production URL; all health checks passing; backup/restore tested | Sprint 10 |
| D-17 | Data Migration Execution | Execution of production data migration from TechNova's spreadsheets and shared drives | All migrated data verified by TechNova; zero data loss confirmed | Sprint 10 |
| D-18 | Handover Package | Source code repository access, deployment runbooks, architecture documentation, admin guides, environment configuration documentation | All documentation reviewed; knowledge transfer sessions completed with TechNova IT team | Sprint 10 |

---

## 4. Project Timeline

### 4.1 Phase Overview

| Phase | Duration | Sprints | Activities |
|---|---|---|---|
| **Phase A: Foundation** | Weeks 1-4 | Sprint 1-2 | Architecture, UX design, RBAC/Security core, environment setup |
| **Phase B: Core Platform** | Weeks 5-10 | Sprint 3-5 | Project management, time tracking, document management, admin panel |
| **Phase C: Client & Integrations** | Weeks 11-16 | Sprint 6-8 | Client portal, integrations, resource management, reporting |
| **Phase D: Quality & Launch** | Weeks 17-20 | Sprint 9-10 | QA, performance testing, data migration, deployment, handover |

### 4.2 Sprint-by-Sprint Plan

| Sprint | Dates (Approximate) | Key Deliverables | Milestone |
|---|---|---|---|
| Sprint 1 | Weeks 1-2 (Mar 2026) | Solution architecture; QuickBooks API spike; UX wireframes; environment setup | Architecture Sign-off |
| Sprint 2 | Weeks 3-4 (Apr 2026) | RBAC & authentication (FR-033, FR-034, FR-047, FR-048); UX mockups finalized | Security Foundation Complete |
| Sprint 3 | Weeks 5-6 (Apr 2026) | Project dashboard, CRUD, task management (FR-001, FR-002, FR-003); admin panel start (FR-040) | Project Management MVP |
| Sprint 4 | Weeks 7-8 (May 2026) | Milestones, Kanban (FR-004, FR-005); time tracking (FR-011); billing rates (FR-026); audit trails (FR-035); admin panel (FR-040, FR-041) | Core Tracking Complete |
| Sprint 5 | Weeks 9-10 (May 2026) | Document management (FR-016 through FR-019); time approval and timesheets (FR-027, FR-028); client data isolation (FR-036); resource board start (FR-013) | Document Management Complete |
| Sprint 6 | Weeks 11-12 (Jun 2026) | Invoice generation (FR-012); client portal core (FR-006, FR-007, FR-008); resource management (FR-013, FR-014, FR-015) | Client Portal MVP |
| Sprint 7 | Weeks 13-14 (Jun 2026) | Client portal polish (FR-009, FR-010); executive dashboard (FR-029); profitability reports (FR-030); SSO (FR-046) | Reporting MVP |
| Sprint 8 | Weeks 15-16 (Jul 2026) | Integrations — QuickBooks (FR-020, FR-025), Slack (FR-021), Google Calendar (FR-022), Figma (FR-023), GitHub (FR-024); report exports (FR-031); NPS (FR-032); global search (FR-038); notifications (FR-039) | Integrations Complete |
| Sprint 9 | Weeks 17-18 (Jul 2026) | QA & regression testing; performance testing; security scanning; data migration tool (FR-042); user documentation; bug fixes | QA Sign-off |
| Sprint 10 | Weeks 19-20 (Aug 2026) | Production deployment; data migration execution; UAT; handover; training | Go-Live |

### 4.3 Key Milestones

| Milestone | Target Date | Gate Criteria |
|---|---|---|
| Architecture Sign-off | End of Sprint 1 | Architecture document approved by TechNova |
| Security Foundation Complete | End of Sprint 2 | RBAC, 2FA, and session management functional |
| Core Platform Demo | End of Sprint 4 | Project management, time tracking, admin panel demonstrated |
| Client Portal MVP | End of Sprint 6 | Client portal demonstrated to TechNova with sample client data |
| Integrations Complete | End of Sprint 8 | All 5 integrations functional and tested |
| QA Sign-off | End of Sprint 9 | Zero critical/high defects; performance targets met |
| Go-Live | End of Sprint 10 | Production deployment; data migration complete; UAT passed |

---

## 5. Team Structure

### 5.1 Vendor Team

| Role | Count | Responsibilities |
|---|---|---|
| **Project Manager** | 1 | Sprint planning, client communication, risk management, progress reporting |
| **Solution Architect** | 1 | Technical architecture, technology decisions, integration design, code reviews |
| **Senior Full-Stack Developer** | 2 | Core platform development (front-end and back-end), API design |
| **Front-End Developer** | 1 | UI/UX implementation, responsive design, client portal, dashboards |
| **Back-End Developer** | 1 | Integrations, data migration, reporting engine, background jobs |
| **QA Engineer** | 1 | Test planning, test case development, manual and automated testing, performance testing |
| **DevOps Engineer** | 0.5 (part-time) | Cloud infrastructure, CI/CD pipeline, deployment, monitoring setup |
| **UX Designer** | 0.5 (part-time) | Wireframes, mockups, usability testing, design system |

**Total**: Approximately 8 team members (7 FTE equivalent)

### 5.2 TechNova Team (Client Responsibilities)

| Role | Count | Responsibilities |
|---|---|---|
| **Product Owner** | 1 | Requirement clarification, sprint review participation, acceptance decisions, priority arbitration |
| **IT Contact** | 1 | SSO configuration, infrastructure access, security reviews |
| **Finance Contact** | 1 | QuickBooks access, billing rate validation, invoice workflow validation |
| **Client Liaison** | 1 | Coordinate client portal user testing, gather client feedback |
| **Data Migration Lead** | 1 | Provide sample data, validate migration results, assist with data cleansing |

### 5.3 Communication Plan

| Ceremony | Frequency | Participants | Duration |
|---|---|---|---|
| Sprint Planning | Bi-weekly (start of sprint) | Vendor team + Product Owner | 2 hours |
| Daily Standup | Daily (vendor internal) | Vendor team | 15 minutes |
| Sprint Review / Demo | Bi-weekly (end of sprint) | Full vendor team + TechNova stakeholders | 1 hour |
| Sprint Retrospective | Bi-weekly | Vendor team | 30 minutes |
| Steering Committee | Bi-weekly | Project Manager + TechNova leadership | 30 minutes |
| Ad-hoc Clarification | As needed | Developer + Product Owner | Response within 24 hours |

---

## 6. Assumptions

The following assumptions underpin this Statement of Work. If any assumption proves invalid, it may constitute grounds for a change request.

| # | Assumption |
|---|---|
| 1 | TechNova has an active QuickBooks Online subscription with API access enabled. |
| 2 | TechNova's Slack workspace allows third-party app integrations and webhook configurations. |
| 3 | TechNova's Google Workspace administrator will cooperate to configure SSO (SAML/OIDC) integration within 2 weeks of request. |
| 4 | TechNova will designate a Product Owner available for weekly sprint reviews and ad-hoc clarifications within 24 hours. |
| 5 | TechNova's existing spreadsheet data is structured consistently enough for automated migration with reasonable data cleansing effort. Sample data will be provided within the first week. |
| 6 | The 5-month timeline assumes no major scope changes after SOW signing and timely client feedback (within 3 business days) during UAT. |
| 7 | TechNova's existing shared drive documents can be exported in standard file formats (PDF, DOCX, PNG, etc.) for migration. |
| 8 | The $150,000 budget covers development, testing, and initial deployment. Ongoing hosting, maintenance, and support costs are excluded and will be covered under a separate agreement. |
| 9 | Cloud hosting (AWS, Azure, or GCP) is acceptable. No on-premises deployment requirement exists. |
| 10 | All 150 internal users have access to modern web browsers (Chrome, Firefox, Safari, or Edge — latest two major versions). |
| 11 | Client portal users (60-80) have valid email addresses and are willing to set up 2FA. |
| 12 | TechNova will provide sample board meeting report templates during the design phase (Sprint 1). |
| 13 | Two-factor authentication via authenticator app (TOTP) is the primary method. SMS is a fallback only. |
| 14 | Phase 2 scope, budget, and timeline will be negotiated separately after Phase 1 go-live. |
| 15 | No regulatory approvals or external compliance audits are required before Phase 1 go-live. SOC2 compliance is design-only; the actual audit is post-go-live. |

---

## 7. Acceptance Criteria

### 7.1 General Acceptance Criteria

All deliverables must meet the following general criteria:

1. **Functional Completeness**: All 44 in-scope functional requirements (FR-001 through FR-042, FR-046 through FR-048, excluding FR-043, FR-044, FR-045) pass acceptance testing against their defined acceptance criteria in the FRD.
2. **Non-Functional Compliance**: All 20 non-functional requirements (NFR-001 through NFR-020) are verified through appropriate testing methods (performance testing, security scanning, usability testing).
3. **Defect-Free**: Zero critical or high-severity defects remain open at the time of acceptance. Medium and low-severity defects may be deferred to a post-launch patch with TechNova's written agreement.
4. **Data Integrity**: Production data migration results in zero data loss, verified by TechNova's data migration lead.
5. **Documentation**: All user guides, admin guides, and technical documentation are delivered and approved.

### 7.2 Per-Module Acceptance Criteria

| Module | Key Acceptance Criteria |
|---|---|
| Project Management | 40+ projects viewable in dashboard; task dependencies functional; Kanban drag-and-drop works in real time |
| Client Portal | Client users see only their own projects; deliverable approval workflow complete; SUS score >= 75 |
| Time Tracking & Invoicing | Timer and manual entry functional; billing rates cascade correctly (project > client > global); invoices generate from approved entries only |
| Resource Management | Utilization percentages calculate correctly; capacity conflict warnings trigger at threshold; forecast extends 4-12 weeks |
| Document Management | Version history tracks all uploads; in-browser preview works for common file types; client approval workflow complete |
| Integrations | QuickBooks bi-directional sync operational; Slack notifications delivered within 5 seconds; Google Calendar events created/updated on date changes |
| Reporting & Analytics | Executive dashboard loads within 5 seconds; profitability variance calculations correct; PDF/CSV/Excel exports functional |
| Security & Access Control | RBAC enforced on all endpoints; 2FA mandatory for all users; audit logs immutable and searchable; no cross-tenant data leakage in penetration test |
| Platform & UX | Application functional at 768px, 1024px, 1366px, and 1920px viewports; global search returns results within 2 seconds |
| Administration | User CRUD operational; email invitations delivered; role assignment functional |
| Data Migration | Sample data imported successfully; validation errors reported per row; dry-run mode functional; zero data loss on production migration |

### 7.3 User Acceptance Testing (UAT)

- **Duration**: 5 business days during Sprint 10
- **Participants**: TechNova Product Owner, 2-3 internal power users, 1-2 client user representatives
- **Environment**: Staging environment with production-equivalent configuration and migrated data
- **Process**: TechNova executes predefined UAT test scripts and reports findings. Critical/high findings block go-live. Medium/low findings documented for post-launch resolution.
- **Sign-off**: Written UAT approval from TechNova Product Owner required before production deployment.

---

## 8. Change Management Process

Given TechNova's prior experience with scope creep, a formal change management process is mandatory for this engagement.

### 8.1 Change Request Process

1. **Initiation**: Either party identifies a change to scope, timeline, or budget. A Change Request (CR) is submitted in writing (email or shared document).
2. **Assessment**: The Vendor assesses the CR within 3 business days, providing:
   - Impact on timeline (sprint/day estimate)
   - Impact on budget (cost estimate)
   - Impact on existing scope (what is affected)
   - Recommendation (approve, defer to Phase 2, or reject)
3. **Decision**: TechNova Product Owner and Vendor Project Manager jointly decide to approve, defer, or reject the CR.
4. **Implementation**: Approved CRs are added to the sprint backlog with updated timeline and budget. Both parties sign the CR document before work begins.

### 8.2 Change Request Thresholds

| Change Type | Approval Required |
|---|---|
| Bug fix or clarification (no scope change) | Project Manager |
| Minor scope addition (less than or equal to 2 story points, no budget impact) | Product Owner + Project Manager |
| Moderate scope change (3-8 story points or less than or equal to $5,000) | Product Owner + Vendor leadership |
| Major scope change (more than 8 story points or more than $5,000) | Steering Committee + written amendment to SOW |

### 8.3 Out-of-Scope Boundary

Any request for functionality listed in Section 2.3 (Out of Scope) automatically triggers a formal Change Request and requires Steering Committee approval. Phase 2 items will not be pulled into Phase 1 without explicit written agreement from both parties.

---

## 9. Sign-Off

### 9.1 SOW Approval

By signing below, both parties agree to the scope, deliverables, timeline, budget, assumptions, and terms described in this Statement of Work.

---

**TechNova Solutions (Client)**

| Field | Value |
|---|---|
| Name | ________________________________________ |
| Title | ________________________________________ |
| Signature | ________________________________________ |
| Date | ________________________________________ |

---

**[Vendor Name]**

| Field | Value |
|---|---|
| Name | ________________________________________ |
| Title | ________________________________________ |
| Signature | ________________________________________ |
| Date | ________________________________________ |

---

### 9.2 Milestone Sign-Off Log

The following milestone sign-offs will be collected throughout the engagement:

| Milestone | Expected Date | Client Signee | Vendor Signee | Date Signed |
|---|---|---|---|---|
| Architecture Sign-off | End Sprint 1 | ____________ | ____________ | ____________ |
| UX Design Approval | End Sprint 2 | ____________ | ____________ | ____________ |
| Core Platform Demo Acceptance | End Sprint 4 | ____________ | ____________ | ____________ |
| Client Portal Demo Acceptance | End Sprint 6 | ____________ | ____________ | ____________ |
| Integrations Complete Acceptance | End Sprint 8 | ____________ | ____________ | ____________ |
| QA Sign-off | End Sprint 9 | ____________ | ____________ | ____________ |
| UAT Sign-off | Sprint 10 | ____________ | ____________ | ____________ |
| Go-Live Approval | End Sprint 10 | ____________ | ____________ | ____________ |
| Final Handover Acceptance | End Sprint 10 | ____________ | ____________ | ____________ |

---

*End of Statement of Work*
