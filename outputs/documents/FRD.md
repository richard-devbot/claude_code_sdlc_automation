# Functional Requirements Document (FRD)

**Project:** TechNova Solutions — Unified Agency Management Platform
**Client:** TechNova Solutions
**Domain:** Professional Services / Digital Agency Management
**Version:** 1.0
**Date:** 2026-03-12
**Prepared By:** Documentation Agent — SDLC Automation Pipeline
**Status:** Draft — Pending Technical Review

---

## Table of Contents

1. [Introduction & Purpose](#1-introduction--purpose)
2. [System Overview](#2-system-overview)
3. [User Roles & Permissions Matrix](#3-user-roles--permissions-matrix)
4. [Functional Requirements by Module](#4-functional-requirements-by-module)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Data Requirements](#6-data-requirements)
7. [Integration Requirements](#7-integration-requirements)
8. [UI/UX Requirements](#8-uiux-requirements)
9. [Security Requirements](#9-security-requirements)
10. [Traceability Matrix](#10-traceability-matrix)

---

## 1. Introduction & Purpose

### 1.1 Purpose

This Functional Requirements Document (FRD) provides a detailed technical specification of all functional and non-functional requirements for the TechNova Solutions Unified Agency Management Platform, Phase 1. It serves as the authoritative reference for the development team, QA engineers, and solution architects during design, implementation, and testing.

### 1.2 Intended Audience

- Development team (front-end and back-end engineers)
- QA engineers and test leads
- Solution architects
- DevOps engineers
- Project managers and scrum masters

### 1.3 Scope

This document covers all 48 functional requirements (FR-001 through FR-048) and 20 non-functional requirements (NFR-001 through NFR-020) organized across 11 modules. Requirements are derived from the structured requirement specification (`requirement_spec.json`) produced by the Requirements Agent.

### 1.4 References

- Requirement Specification: `outputs/requirements/requirement_spec.json`
- Business Requirements Document: `outputs/documents/BRD.md`

---

## 2. System Overview

### 2.1 System Description

The Unified Agency Management Platform is a cloud-hosted, multi-tenant web application that consolidates project management, client communication, time tracking, invoicing, resource allocation, document management, and operational reporting into a single platform. The system serves two primary user populations: TechNova's internal team (~150-250 users) and their external clients (~60-80 users) through a dedicated client portal.

### 2.2 High-Level Architecture Context

| Component | Description |
|---|---|
| **Web Application** | Responsive SPA (Single Page Application) supporting viewports from 768px to 1920px |
| **Client Portal** | Separate portal view with scoped access for client users |
| **API Layer** | RESTful API backend serving both internal and client portal front-ends |
| **Integration Layer** | Service integrations with QuickBooks, Slack, Google Calendar, Figma, GitHub |
| **Authentication** | SSO (Google Workspace via SAML/OIDC), email/password with mandatory 2FA |
| **Data Layer** | Multi-tenant database with logical client data isolation |
| **Notification Engine** | In-app, email, and Slack notification delivery |
| **Reporting Engine** | Dashboard and report generation with export capabilities |

### 2.3 Module Map

The system comprises 11 functional modules:

1. Project Management (5 FRs)
2. Client Portal (5 FRs)
3. Time Tracking & Invoicing (5 FRs)
4. Resource Management (3 FRs)
5. Document Management (4 FRs)
6. Integrations (6 FRs)
7. Reporting & Analytics (6 FRs)
8. Security & Access Control (7 FRs)
9. Platform & UX (4 FRs)
10. Administration (2 FRs)
11. Data Migration (1 FR)

---

## 3. User Roles & Permissions Matrix

### 3.1 Role Definitions

| Role | Description | User Type |
|---|---|---|
| **Administrator** | Full system access. Manages users, roles, integrations, billing rates, system settings. | Internal |
| **Executive** | Read-only access to all dashboards, reports, and portfolio-level data. | Internal |
| **Project Manager** | Manages projects, tasks, milestones, resource assignments, time approvals, and client communication. | Internal |
| **Team Lead** | Manages team assignments, approves time entries, views team utilization. | Internal |
| **Team Member** | Executes tasks, logs time, uploads documents, participates in messaging. | Internal |
| **Finance Manager** | Manages invoicing, billing rates, QuickBooks integration, and financial reports. | Internal |
| **Client User** | Views own project status, reviews deliverables, approves milestones, communicates with project team. | External |

### 3.2 Permissions Matrix

| Capability | Admin | Executive | Project Mgr | Team Lead | Team Member | Finance Mgr | Client User |
|---|---|---|---|---|---|---|---|
| **Projects — View All** | Yes | Yes | Yes | Yes (assigned) | Yes (assigned) | Yes | No |
| **Projects — Create/Edit** | Yes | No | Yes | No | No | No | No |
| **Projects — Archive** | Yes | No | Yes | No | No | No | No |
| **Tasks — Create/Assign** | Yes | No | Yes | Yes | No | No | No |
| **Tasks — Update Status** | Yes | No | Yes | Yes | Yes (own) | No | No |
| **Milestones — Define** | Yes | No | Yes | No | No | No | No |
| **Milestones — Approve** | No | No | No | No | No | No | Yes (own projects) |
| **Time — Log Entries** | No | No | No | Yes | Yes | No | No |
| **Time — Approve Entries** | Yes | No | Yes | Yes | No | No | No |
| **Invoices — Generate** | Yes | No | Yes | No | No | Yes | No |
| **Invoices — Finalize** | Yes | No | No | No | No | Yes | No |
| **Documents — Upload** | Yes | No | Yes | Yes | Yes | No | No |
| **Documents — Download** | Yes | Yes | Yes | Yes | Yes | Yes | Yes (own projects) |
| **Documents — Delete** | Yes | No | Yes | No | No | No | No |
| **Documents — Approve** | No | No | No | No | No | No | Yes (own projects) |
| **Resource Board — View** | Yes | Yes | Yes | Yes | No | No | No |
| **Resource Board — Assign** | Yes | No | Yes | Yes | No | No | No |
| **Reports — View Dashboards** | Yes | Yes | Yes | Yes (team) | No | Yes | No |
| **Reports — Export** | Yes | Yes | Yes | No | No | Yes | No |
| **Client Portal — Access** | No | No | No | No | No | No | Yes |
| **Client Messaging — Send** | Yes | No | Yes | Yes | Yes (assigned) | No | Yes (own projects) |
| **Admin Panel — Access** | Yes | No | No | No | No | No | No |
| **User Management** | Yes | No | No | No | No | No | No |
| **Integration Config** | Yes | No | No | No | No | Yes (QuickBooks) | No |
| **Audit Logs — View** | Yes | No | No | No | No | No | No |
| **Global Search** | Yes | Yes | Yes | Yes | Yes | Yes | No |
| **Notifications — Receive** | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

---

## 4. Functional Requirements by Module

### 4.1 Project Management Module

#### FR-001: Centralized Project Dashboard

| Attribute | Detail |
|---|---|
| **ID** | FR-001 |
| **Module** | Project Management |
| **Priority** | CRITICAL |
| **Description** | The system shall provide a centralized project dashboard displaying all active projects with their current status, assigned team members, deadlines, and completion percentages. |
| **Actors** | Project Manager, Team Lead, Administrator |
| **Source Feature** | F-001 |
| **Acceptance Criteria** | Users can view all 40+ active client projects in a single dashboard with real-time status indicators, filtering, and sorting capabilities. |
| **Dependencies** | Requires FR-033 (RBAC) to filter visible projects per user role. |

#### FR-002: Project CRUD Operations

| Attribute | Detail |
|---|---|
| **ID** | FR-002 |
| **Module** | Project Management |
| **Priority** | CRITICAL |
| **Description** | The system shall allow creation, editing, and archival of projects with configurable fields including project name, client, start date, deadline, budget, assigned team, and project phases/milestones. |
| **Actors** | Project Manager, Administrator |
| **Source Feature** | F-001 |
| **Acceptance Criteria** | A project can be created with all required fields, edited at any time, and archived when completed. Archived projects remain searchable but are hidden from active views. |
| **Dependencies** | Requires FR-033 (RBAC) for role-based permission checks. |

#### FR-003: Task Management

| Attribute | Detail |
|---|---|
| **ID** | FR-003 |
| **Module** | Project Management |
| **Priority** | CRITICAL |
| **Description** | The system shall provide task management within projects, including task creation, assignment to team members, due dates, status tracking (To Do, In Progress, In Review, Done), and dependencies between tasks. |
| **Actors** | Project Manager, Team Member, Team Lead |
| **Source Feature** | F-001 |
| **Acceptance Criteria** | Tasks can be created within a project, assigned to one or more team members, tracked through status transitions, and linked with predecessor/successor dependencies. |
| **Dependencies** | Requires FR-002 (Project CRUD) — tasks exist within projects. |

#### FR-004: Milestone Management

| Attribute | Detail |
|---|---|
| **ID** | FR-004 |
| **Module** | Project Management |
| **Priority** | CRITICAL |
| **Description** | The system shall support milestone definition within projects, with configurable milestone names, target dates, deliverable associations, and client approval requirements. |
| **Actors** | Project Manager, Client User |
| **Source Feature** | F-001 |
| **Acceptance Criteria** | Milestones can be created per project with target dates. Milestones requiring client approval trigger notifications and cannot be marked complete until the client approves. |
| **Dependencies** | Requires FR-002 (Project CRUD) — milestones are defined within projects. |

#### FR-005: Kanban and List Views

| Attribute | Detail |
|---|---|
| **ID** | FR-005 |
| **Module** | Project Management |
| **Priority** | HIGH |
| **Description** | The system shall provide Kanban and list views for task management within each project, allowing team members to drag-and-drop tasks between status columns. |
| **Actors** | Team Member, Project Manager, Team Lead |
| **Source Feature** | F-001 |
| **Acceptance Criteria** | Users can toggle between Kanban board and list views. Tasks can be moved between status columns via drag-and-drop and the change is reflected in real time. |
| **Dependencies** | Requires FR-003 (Task Management). |

---

### 4.2 Client Portal Module

#### FR-006: Client Portal Dashboard

| Attribute | Detail |
|---|---|
| **ID** | FR-006 |
| **Module** | Client Portal |
| **Priority** | CRITICAL |
| **Description** | The system shall provide a dedicated client-facing portal where client users can log in, view their project dashboard, see overall project status, and access project-specific information. |
| **Actors** | Client User |
| **Source Feature** | F-002 |
| **Acceptance Criteria** | Client users can log in and see only their own projects with a dashboard showing project status, upcoming milestones, and recent activity. |
| **Dependencies** | Requires FR-033 (RBAC) and FR-036 (Client Data Isolation). |

#### FR-007: Deliverable Review and Approval

| Attribute | Detail |
|---|---|
| **ID** | FR-007 |
| **Module** | Client Portal |
| **Priority** | CRITICAL |
| **Description** | The system shall allow client users to view and download deliverables associated with their projects, and to approve or request revisions on milestones through the portal. |
| **Actors** | Client User |
| **Source Feature** | F-002 |
| **Acceptance Criteria** | Client users can browse deliverables per milestone, download files, and click Approve or Request Revision with an optional comment. Approval status is tracked with timestamps. |
| **Dependencies** | Requires FR-006 (Client Portal) and FR-016 (Document Management). |

#### FR-008: Client Messaging

| Attribute | Detail |
|---|---|
| **ID** | FR-008 |
| **Module** | Client Portal |
| **Priority** | CRITICAL |
| **Description** | The system shall provide a messaging/communication feature within the client portal, allowing client users to communicate with their dedicated project team in a threaded conversation format. |
| **Actors** | Client User, Project Manager, Team Member |
| **Source Feature** | F-002 |
| **Acceptance Criteria** | Clients and team members can exchange messages in project-scoped threads. Messages support text and file attachments. All parties receive notifications for new messages. |
| **Dependencies** | Requires FR-006 (Client Portal). |

#### FR-009: Project Timeline Visualization

| Attribute | Detail |
|---|---|
| **ID** | FR-009 |
| **Module** | Client Portal |
| **Priority** | HIGH |
| **Description** | The system shall display project timeline/Gantt-style visualization to client users showing milestone dates, current progress, and upcoming deliverables. |
| **Actors** | Client User |
| **Source Feature** | F-002 |
| **Acceptance Criteria** | Client users can view a timeline visualization of their project showing past and upcoming milestones, current phase, and expected completion date. |
| **Dependencies** | Requires FR-006 (Client Portal) and FR-004 (Milestone Management). |

#### FR-010: Automated Client Notifications

| Attribute | Detail |
|---|---|
| **ID** | FR-010 |
| **Module** | Client Portal |
| **Priority** | HIGH |
| **Description** | The system shall send automated email notifications to client users for key events: milestone completion, deliverable uploads, approval requests, and message replies. |
| **Actors** | Client User, System |
| **Source Feature** | F-002 |
| **Acceptance Criteria** | Client users receive email notifications for predefined events. Notification preferences can be configured per client user. |
| **Dependencies** | Enhances FR-007 (Deliverable Approval). |

---

### 4.3 Time Tracking & Invoicing Module

#### FR-011: Time Tracking

| Attribute | Detail |
|---|---|
| **ID** | FR-011 |
| **Module** | Time Tracking & Invoicing |
| **Priority** | CRITICAL |
| **Description** | The system shall provide time tracking functionality where team members can log billable and non-billable hours against specific projects and tasks, with start/stop timer and manual entry options. |
| **Actors** | Team Member, Team Lead |
| **Source Feature** | F-003 |
| **Acceptance Criteria** | Team members can start/stop a timer or manually enter time entries linked to a project and task. Each entry captures date, hours, description, and billable/non-billable flag. |
| **Dependencies** | Requires FR-002 (Project CRUD) — time entries are linked to projects. |

#### FR-012: Automated Invoice Generation

| Attribute | Detail |
|---|---|
| **ID** | FR-012 |
| **Module** | Time Tracking & Invoicing |
| **Priority** | CRITICAL |
| **Description** | The system shall automatically generate draft invoices from approved time entries, calculating totals based on project-specific billing rates, and support manual adjustments before finalization. |
| **Actors** | Project Manager, Administrator, Finance Manager |
| **Source Feature** | F-003 |
| **Acceptance Criteria** | Draft invoices are generated from approved time entries with correct billing rates. Authorized users can adjust line items before finalizing. Finalized invoices are immutable. |
| **Dependencies** | Requires FR-011 (Time Tracking), FR-026 (Billing Rates), FR-027 (Time Approval). |

#### FR-026: Configurable Billing Rates

| Attribute | Detail |
|---|---|
| **ID** | FR-026 |
| **Module** | Time Tracking & Invoicing |
| **Priority** | CRITICAL |
| **Description** | The system shall support configurable billing rates per project, per team member role, and per client. Rate overrides at the project level shall take precedence over defaults. |
| **Actors** | Administrator, Finance Manager, Project Manager |
| **Source Feature** | F-003 |
| **Acceptance Criteria** | Billing rates can be set at global (role-based), client-level, and project-level. Project-level rates override client rates, which override global rates. |
| **Dependencies** | None. |

#### FR-027: Time Entry Approval Workflow

| Attribute | Detail |
|---|---|
| **ID** | FR-027 |
| **Module** | Time Tracking & Invoicing |
| **Priority** | HIGH |
| **Description** | The system shall provide time entry approval workflow where team leads or project managers review and approve time entries before they are included in invoice generation. |
| **Actors** | Team Lead, Project Manager |
| **Source Feature** | F-003 |
| **Acceptance Criteria** | Time entries are submitted for approval. Approvers can approve, reject (with reason), or request modification. Only approved entries are included in invoice calculations. |
| **Dependencies** | Requires FR-011 (Time Tracking). |

#### FR-028: Timesheet Views

| Attribute | Detail |
|---|---|
| **ID** | FR-028 |
| **Module** | Time Tracking & Invoicing |
| **Priority** | HIGH |
| **Description** | The system shall provide timesheet views showing weekly and monthly summaries per team member with breakdown by project, billable vs. non-billable hours, and utilization percentage. |
| **Actors** | Team Member, Team Lead, Project Manager |
| **Source Feature** | F-003 |
| **Acceptance Criteria** | Team members can view their own timesheets. Managers can view timesheets for their team. Views support weekly and monthly groupings with export capability. |
| **Dependencies** | Requires FR-011 (Time Tracking). |

---

### 4.4 Resource Management Module

#### FR-013: Visual Resource Allocation Board

| Attribute | Detail |
|---|---|
| **ID** | FR-013 |
| **Module** | Resource Management |
| **Priority** | HIGH |
| **Description** | The system shall provide a visual resource allocation board showing all team members, their assigned projects, utilization rate (percentage of capacity used), and availability windows. |
| **Actors** | Project Manager, Team Lead, Administrator |
| **Source Feature** | F-004 |
| **Acceptance Criteria** | A visual board displays each team member with their project assignments, utilization percentage, and open availability slots. Data updates in real time as assignments change. |
| **Dependencies** | Requires FR-003 (Task Management) for task assignment data. |

#### FR-014: Team Assignment with Conflict Detection

| Attribute | Detail |
|---|---|
| **ID** | FR-014 |
| **Module** | Resource Management |
| **Priority** | HIGH |
| **Description** | The system shall allow managers to assign and reassign team members to projects and tasks, with conflict detection when a team member would exceed their capacity threshold. |
| **Actors** | Project Manager, Team Lead, Administrator |
| **Source Feature** | F-004 |
| **Acceptance Criteria** | Managers can drag-and-drop or select team members for assignment. The system warns when assignment would push utilization above a configurable threshold (e.g., 100%). |
| **Dependencies** | Requires FR-013 (Resource Board). |

#### FR-015: Capacity Forecasting

| Attribute | Detail |
|---|---|
| **ID** | FR-015 |
| **Module** | Resource Management |
| **Priority** | MEDIUM |
| **Description** | The system shall provide capacity forecasting showing projected team availability over the next 4-12 weeks based on current project schedules and assignments. |
| **Actors** | Project Manager, Team Lead, Administrator |
| **Source Feature** | F-004 |
| **Acceptance Criteria** | A forecast view shows projected utilization per team member for the next 4-12 weeks. Users can adjust the time window and filter by team, skill, or department. |
| **Dependencies** | Requires FR-013 (Resource Board). |

---

### 4.5 Document Management Module

#### FR-016: Document Repository

| Attribute | Detail |
|---|---|
| **ID** | FR-016 |
| **Module** | Document Management |
| **Priority** | HIGH |
| **Description** | The system shall provide a document management repository for each project with folder structures, supporting upload, download, preview, and deletion of deliverables and project files. |
| **Actors** | Team Member, Project Manager, Client User |
| **Source Feature** | F-005 |
| **Acceptance Criteria** | Users can upload documents to project-specific folders, preview common file types in-browser, download files, and delete files (with appropriate permissions). |
| **Dependencies** | Requires FR-002 (Project CRUD). |

#### FR-017: Document Version History

| Attribute | Detail |
|---|---|
| **ID** | FR-017 |
| **Module** | Document Management |
| **Priority** | HIGH |
| **Description** | The system shall maintain automatic version history for all uploaded documents, allowing users to view previous versions, compare versions, and restore earlier versions. |
| **Actors** | Team Member, Project Manager |
| **Source Feature** | F-005 |
| **Acceptance Criteria** | Each document upload creates a new version. Users can view the version history list, download any previous version, and restore a previous version as the current one. |
| **Dependencies** | Requires FR-016 (Document Repository). |

#### FR-018: Document Commenting and Annotation

| Attribute | Detail |
|---|---|
| **ID** | FR-018 |
| **Module** | Document Management |
| **Priority** | HIGH |
| **Description** | The system shall support commenting and annotation on deliverables, allowing team members and clients to provide feedback directly on documents. |
| **Actors** | Team Member, Project Manager, Client User |
| **Source Feature** | F-005 |
| **Acceptance Criteria** | Users can add comments on documents. Comments are threaded and support replies. Notifications are sent to relevant parties when new comments are added. |
| **Dependencies** | Requires FR-016 (Document Repository). |

#### FR-019: Client Approval Workflow for Deliverables

| Attribute | Detail |
|---|---|
| **ID** | FR-019 |
| **Module** | Document Management |
| **Priority** | HIGH |
| **Description** | The system shall provide a client approval workflow for deliverables, where documents can be submitted for client review and the client can approve, reject, or request changes with comments. |
| **Actors** | Project Manager, Client User |
| **Source Feature** | F-005 |
| **Acceptance Criteria** | A deliverable can be marked 'Submitted for Review.' The client receives a notification, reviews the document, and selects Approve, Reject, or Request Changes with a required comment for non-approvals. |
| **Dependencies** | Requires FR-017 (Version History). |

---

### 4.6 Integrations Module

#### FR-020: QuickBooks Invoice Sync

| Attribute | Detail |
|---|---|
| **ID** | FR-020 |
| **Module** | Integrations |
| **Priority** | HIGH |
| **Description** | The system shall integrate with QuickBooks to synchronize finalized invoices, including line items, client details, and payment status. The integration shall support bi-directional sync for payment status updates. |
| **Actors** | Finance Manager, Administrator, System |
| **Source Feature** | F-006 |
| **Acceptance Criteria** | Finalized invoices are automatically pushed to QuickBooks. Payment status updates in QuickBooks are reflected back in the platform. Sync errors are logged and reported. |
| **Dependencies** | Requires FR-012 (Invoice Generation) and FR-025 (QuickBooks Config). |

#### FR-021: Slack Notifications

| Attribute | Detail |
|---|---|
| **ID** | FR-021 |
| **Module** | Integrations |
| **Priority** | HIGH |
| **Description** | The system shall send Slack notifications for configurable events including: milestone approvals, new client comments, task assignments, approaching deadlines, and deliverable uploads. |
| **Actors** | Team Member, Project Manager, System |
| **Source Feature** | F-007 |
| **Acceptance Criteria** | Slack notifications are sent to configured channels or DMs for each event type. Users and admins can configure which events trigger notifications and to which channels. |
| **Dependencies** | Enhances FR-003 (Task Management). |

#### FR-022: Google Calendar Sync

| Attribute | Detail |
|---|---|
| **ID** | FR-022 |
| **Module** | Integrations |
| **Priority** | MEDIUM |
| **Description** | The system shall integrate with Google Calendar to sync project deadlines, milestone dates, and meeting schedules. Calendar events shall be created/updated automatically when project dates change. |
| **Actors** | Team Member, Project Manager, System |
| **Source Feature** | F-008 |
| **Acceptance Criteria** | Project milestones and deadlines appear as events in connected Google Calendars. Changes to dates in the platform are automatically reflected in the calendar. |
| **Dependencies** | Enhances FR-004 (Milestone Management). |

#### FR-023: Figma Integration

| Attribute | Detail |
|---|---|
| **ID** | FR-023 |
| **Module** | Integrations |
| **Priority** | LOW |
| **Description** | The system shall provide a Figma integration that allows linking Figma project files to platform projects and embedding preview thumbnails of Figma designs within the document management system. |
| **Actors** | Team Member, Project Manager |
| **Source Feature** | F-009 |
| **Acceptance Criteria** | Users can paste a Figma URL to link a design file to a project. The system displays a thumbnail preview. Clicking the thumbnail opens Figma in a new tab. |
| **Dependencies** | Enhances FR-016 (Document Repository). |

#### FR-024: GitHub Integration

| Attribute | Detail |
|---|---|
| **ID** | FR-024 |
| **Module** | Integrations |
| **Priority** | LOW |
| **Description** | The system shall integrate with GitHub to display commit activity per project, showing recent commits, active branches, and pull request status within the project dashboard. |
| **Actors** | Team Lead, Project Manager |
| **Source Feature** | F-010 |
| **Acceptance Criteria** | A linked GitHub repository shows recent commits, branch activity, and PR status within the project view. Data refreshes at configurable intervals. |
| **Dependencies** | Enhances FR-002 (Project CRUD). |

#### FR-025: QuickBooks Connection Configuration

| Attribute | Detail |
|---|---|
| **ID** | FR-025 |
| **Module** | Integrations |
| **Priority** | HIGH |
| **Description** | The system shall provide a QuickBooks connection configuration interface where administrators can authenticate, map chart of accounts, configure sync frequency, and monitor sync status. |
| **Actors** | Administrator, Finance Manager |
| **Source Feature** | F-006 |
| **Acceptance Criteria** | An admin panel allows OAuth connection to QuickBooks, mapping of internal invoice fields to QuickBooks accounts, setting sync schedules, and viewing sync logs. |
| **Dependencies** | None. |

---

### 4.7 Reporting & Analytics Module

#### FR-029: Executive Dashboard

| Attribute | Detail |
|---|---|
| **ID** | FR-029 |
| **Module** | Reporting & Analytics |
| **Priority** | CRITICAL |
| **Description** | The system shall provide an executive dashboard displaying: revenue per client, project profitability (hours spent vs. hours quoted), team utilization rates, on-time delivery percentage, and client satisfaction scores. |
| **Actors** | Administrator, Executive |
| **Source Feature** | F-013 |
| **Acceptance Criteria** | An executive dashboard shows all five KPIs with drill-down capability. Data is refreshed in real time or near-real-time. Dashboard is suitable for board meeting presentations. |
| **Dependencies** | Requires FR-011 (Time Tracking), FR-012 (Invoicing), FR-013 (Resource Allocation). |

#### FR-030: Project Profitability Reports

| Attribute | Detail |
|---|---|
| **ID** | FR-030 |
| **Module** | Reporting & Analytics |
| **Priority** | CRITICAL |
| **Description** | The system shall provide project profitability reports comparing actual hours spent and costs against quoted/budgeted values, with variance analysis at the project, client, and portfolio levels. |
| **Actors** | Project Manager, Administrator, Executive |
| **Source Feature** | F-013 |
| **Acceptance Criteria** | Reports show budget vs. actual for hours and cost per project. Variance is calculated as percentage and absolute value. Reports can be filtered by date range, client, and project. |
| **Dependencies** | Requires FR-029 (Executive Dashboard). |

#### FR-031: Configurable Report Exports

| Attribute | Detail |
|---|---|
| **ID** | FR-031 |
| **Module** | Reporting & Analytics |
| **Priority** | HIGH |
| **Description** | The system shall provide configurable reports with export functionality (PDF, CSV, Excel) and the ability to schedule automated report delivery via email. |
| **Actors** | Project Manager, Administrator, Executive |
| **Source Feature** | F-013 |
| **Acceptance Criteria** | Users can generate reports with configurable parameters, export in PDF/CSV/Excel formats, and schedule recurring report delivery to specified email addresses. |
| **Dependencies** | Requires FR-029 (Executive Dashboard). |

#### FR-032: NPS Tracking

| Attribute | Detail |
|---|---|
| **ID** | FR-032 |
| **Module** | Reporting & Analytics |
| **Priority** | MEDIUM |
| **Description** | The system shall track and display client satisfaction scores (NPS) per project and per client, with the ability to record NPS survey results and display trends over time. |
| **Actors** | Project Manager, Administrator |
| **Source Feature** | F-013 |
| **Acceptance Criteria** | NPS scores can be recorded per project or client. A trend chart shows score changes over time. Scores are included in the executive dashboard. |
| **Dependencies** | Enhances FR-029 (Executive Dashboard). |

#### FR-044: AI-Powered Project Estimation (Phase 2)

| Attribute | Detail |
|---|---|
| **ID** | FR-044 |
| **Module** | Reporting & Analytics |
| **Priority** | LOW |
| **Description** | The system shall provide AI-powered project estimation capabilities that analyze historical project data to suggest effort estimates, timelines, and resource requirements for new projects. |
| **Actors** | Project Manager, Executive |
| **Source Feature** | F-016 |
| **Acceptance Criteria** | When creating a new project, the system suggests estimated hours, timeline, and team size based on analysis of similar completed projects. Estimates include confidence intervals. |
| **Dependencies** | Requires FR-029 (Historical reporting data). |

#### FR-045: Advanced Analytics (Phase 2)

| Attribute | Detail |
|---|---|
| **ID** | FR-045 |
| **Module** | Reporting & Analytics |
| **Priority** | LOW |
| **Description** | The system shall provide advanced analytics including trend analysis, predictive project health scoring, revenue forecasting, and custom dashboard widgets beyond standard reports. |
| **Actors** | Executive, Administrator |
| **Source Feature** | F-017 |
| **Acceptance Criteria** | Advanced analytics provide trend lines, predictive scores, and forecasts. Users can create custom dashboards with drag-and-drop widgets. Data supports drill-down to granular levels. |
| **Dependencies** | Requires FR-029 (Executive Dashboard). |

---

### 4.8 Security & Access Control Module

#### FR-033: Role-Based Access Control (RBAC)

| Attribute | Detail |
|---|---|
| **ID** | FR-033 |
| **Module** | Security & Access Control |
| **Priority** | CRITICAL |
| **Description** | The system shall implement role-based access control (RBAC) with predefined roles: Administrator, Executive, Project Manager, Team Lead, Team Member, Finance Manager, and Client User. Each role has specific permissions for viewing, creating, editing, and deleting resources. |
| **Actors** | Administrator, System |
| **Source Feature** | F-011 |
| **Acceptance Criteria** | Roles are predefined with granular permissions. Users are assigned one or more roles. Access to every resource is checked against the user's role permissions. Client users can only access their own projects. |
| **Dependencies** | None — foundational requirement. |

#### FR-034: Two-Factor Authentication (2FA)

| Attribute | Detail |
|---|---|
| **ID** | FR-034 |
| **Module** | Security & Access Control |
| **Priority** | CRITICAL |
| **Description** | The system shall enforce mandatory two-factor authentication (2FA) for all users, supporting authenticator app (TOTP) and SMS-based verification methods. |
| **Actors** | All Users, System |
| **Source Feature** | F-012 |
| **Acceptance Criteria** | All users must set up 2FA during first login. Login requires password + 2FA code. Both TOTP (Google Authenticator, Authy) and SMS methods are supported. Admins can reset 2FA for locked-out users. |
| **Dependencies** | Requires FR-040 (Admin Panel) for 2FA reset capability. |

#### FR-035: Comprehensive Audit Trails

| Attribute | Detail |
|---|---|
| **ID** | FR-035 |
| **Module** | Security & Access Control |
| **Priority** | CRITICAL |
| **Description** | The system shall maintain comprehensive audit trails logging all user actions including data creation, modification, deletion, login/logout events, permission changes, and export activities with timestamps and user identification. |
| **Actors** | System, Administrator |
| **Source Feature** | F-011 |
| **Acceptance Criteria** | Every data modification is logged with timestamp, user ID, action type, affected resource, and before/after values. Audit logs are immutable, searchable, and exportable. |
| **Dependencies** | None. |

#### FR-036: Client Data Isolation

| Attribute | Detail |
|---|---|
| **ID** | FR-036 |
| **Module** | Security & Access Control |
| **Priority** | CRITICAL |
| **Description** | The system shall ensure strict client data isolation so that client users can only view and interact with projects, documents, and data belonging to their organization. No cross-client data leakage shall be possible. |
| **Actors** | System, Client User |
| **Source Feature** | F-011 |
| **Acceptance Criteria** | Client users see only their own organization's data. All queries are tenant-filtered. Penetration tests confirm no cross-tenant data access is possible. |
| **Dependencies** | Requires FR-033 (RBAC). |

#### FR-046: Single Sign-On (SSO) with Google Workspace

| Attribute | Detail |
|---|---|
| **ID** | FR-046 |
| **Module** | Security & Access Control |
| **Priority** | HIGH |
| **Description** | The system shall support Single Sign-On (SSO) integration with Google Workspace using SAML 2.0 or OIDC protocols for internal user authentication. |
| **Actors** | All Internal Users, Administrator, System |
| **Source Feature** | F-011 |
| **Acceptance Criteria** | Internal users can authenticate using their Google Workspace credentials via SSO. SSO can be configured by administrators. Fallback to email/password is available if SSO is unavailable. |
| **Dependencies** | Enhances FR-033 (RBAC). |

#### FR-047: Password Policies

| Attribute | Detail |
|---|---|
| **ID** | FR-047 |
| **Module** | Security & Access Control |
| **Priority** | HIGH |
| **Description** | The system shall enforce password policies including minimum length (12 characters), complexity requirements, password expiry (90 days), and prevention of password reuse for the last 10 passwords. |
| **Actors** | All Users, System |
| **Source Feature** | F-012 |
| **Acceptance Criteria** | Password creation and change enforce all configured policies. Users are notified before password expiry. Passwords are stored using bcrypt or equivalent hashing. |
| **Dependencies** | None. |

#### FR-048: Session Management

| Attribute | Detail |
|---|---|
| **ID** | FR-048 |
| **Module** | Security & Access Control |
| **Priority** | HIGH |
| **Description** | The system shall implement automatic session timeout after 30 minutes of inactivity, with a warning prompt 5 minutes before session expiry allowing the user to extend their session. |
| **Actors** | All Users, System |
| **Source Feature** | F-012 |
| **Acceptance Criteria** | Sessions expire after 30 minutes of inactivity. Users see a warning at 25 minutes. Clicking 'Continue Session' resets the timer. Expired sessions redirect to the login page. |
| **Dependencies** | None. |

---

### 4.9 Platform & UX Module

#### FR-037: Responsive Web Application

| Attribute | Detail |
|---|---|
| **ID** | FR-037 |
| **Module** | Platform & UX |
| **Priority** | HIGH |
| **Description** | The system shall be delivered as a responsive web application that functions correctly on desktop browsers (Chrome, Firefox, Safari, Edge) and tablet devices with a minimum viewport of 768px. |
| **Actors** | All Users |
| **Source Feature** | F-014 |
| **Acceptance Criteria** | The application renders correctly and is fully functional on desktop and tablet viewports. All critical workflows are usable on a 768px-wide screen without horizontal scrolling. |
| **Dependencies** | None. |

#### FR-038: Global Search

| Attribute | Detail |
|---|---|
| **ID** | FR-038 |
| **Module** | Platform & UX |
| **Priority** | MEDIUM |
| **Description** | The system shall provide a global search functionality allowing users to search across projects, tasks, documents, and client records with results filtered by the user's access permissions. |
| **Actors** | All Internal Users |
| **Source Feature** | F-001 |
| **Acceptance Criteria** | A search bar is available from all pages. Search results include projects, tasks, documents, and clients. Results respect RBAC — users only see results they have permission to access. |
| **Dependencies** | Requires FR-033 (RBAC). |

#### FR-039: In-App Notification Center

| Attribute | Detail |
|---|---|
| **ID** | FR-039 |
| **Module** | Platform & UX |
| **Priority** | MEDIUM |
| **Description** | The system shall provide an in-app notification center displaying real-time notifications for task assignments, mentions, approaching deadlines, approval requests, and client messages. |
| **Actors** | All Users |
| **Source Feature** | F-001 |
| **Acceptance Criteria** | A notification bell icon shows unread count. Clicking it opens a notification panel with categorized items. Users can mark notifications as read and configure notification preferences. |
| **Dependencies** | None. |

#### FR-043: Mobile App for Time Tracking (Phase 2)

| Attribute | Detail |
|---|---|
| **ID** | FR-043 |
| **Module** | Platform & UX |
| **Priority** | LOW |
| **Description** | The system shall provide a mobile-optimized native application focused on time tracking, allowing team members to start/stop timers, log hours, and view current task assignments on the go. |
| **Actors** | Team Member |
| **Source Feature** | F-015 |
| **Acceptance Criteria** | A native mobile app (iOS and Android) provides time tracking with timer, manual entry, and task list views. Syncs with the web platform in real time. |
| **Dependencies** | Requires FR-011 (Time Tracking). |

---

### 4.10 Administration Module

#### FR-040: Administration Panel

| Attribute | Detail |
|---|---|
| **ID** | FR-040 |
| **Module** | Administration |
| **Priority** | CRITICAL |
| **Description** | The system shall provide an administration panel for managing users, roles, permissions, system configuration, integration settings, billing rate configuration, and platform-wide settings. |
| **Actors** | Administrator |
| **Source Feature** | F-011 |
| **Acceptance Criteria** | Administrators can create/edit/deactivate users, assign roles, configure integrations, set billing rates, and manage system-wide settings from a centralized admin panel. |
| **Dependencies** | None — foundational requirement. |

#### FR-041: User Onboarding with Email Invitations

| Attribute | Detail |
|---|---|
| **ID** | FR-041 |
| **Module** | Administration |
| **Priority** | HIGH |
| **Description** | The system shall support user onboarding with email invitation workflow, allowing administrators to invite new internal users and client users with predefined role assignments. |
| **Actors** | Administrator, Project Manager |
| **Source Feature** | F-011 |
| **Acceptance Criteria** | Admins can send email invitations with a role pre-assigned. Invitees receive a link to set up their account and 2FA. Invitations expire after a configurable period. |
| **Dependencies** | Requires FR-033 (RBAC) and FR-034 (2FA). |

---

### 4.11 Data Migration Module

#### FR-042: Bulk Data Import

| Attribute | Detail |
|---|---|
| **ID** | FR-042 |
| **Module** | Data Migration |
| **Priority** | HIGH |
| **Description** | The system shall support bulk import of existing project data, client records, and historical time entries from CSV/Excel files to facilitate migration from TechNova's current spreadsheet-based system. |
| **Actors** | Administrator, System |
| **Source Feature** | F-001 |
| **Acceptance Criteria** | An import wizard supports CSV and Excel uploads for projects, clients, and time entries. Validation errors are reported before import. A dry-run mode previews changes without committing. |
| **Dependencies** | Requires FR-002 (Project data model). |

---

## 5. Non-Functional Requirements

### 5.1 Performance

| ID | Requirement | Measurable Target |
|---|---|---|
| NFR-001 | All standard pages shall load within 2 seconds under normal operating conditions (up to 200 concurrent users). | Page load time <= 2 seconds at 95th percentile with 200 concurrent users |
| NFR-002 | Executive and reporting dashboards shall load within 5 seconds, including data aggregation across all active projects. | Dashboard load time <= 5 seconds at 95th percentile with complex queries spanning 40+ projects |
| NFR-011 | API response times shall not exceed 500ms for standard CRUD operations and 3 seconds for complex aggregation queries. | 95th percentile API response time <= 500ms for CRUD, <= 3 seconds for aggregations |
| NFR-016 | Real-time notifications (in-app and Slack) shall be delivered within 5 seconds of the triggering event. | Notification delivery latency <= 5 seconds at 95th percentile |

### 5.2 Scalability

| ID | Requirement | Measurable Target |
|---|---|---|
| NFR-003 | The system shall support scaling from 150 internal users and 60-80 client users to 250 internal users and 80 client users within 18 months without architecture changes. | Support 330+ concurrent users with no degradation beyond 10% of baseline performance metrics |
| NFR-015 | The document management system shall support file uploads up to 500MB per file and total storage of at least 1TB with the ability to scale storage as needed. | Max file size >= 500MB; initial storage >= 1TB; auto-scaling storage enabled |

### 5.3 Availability

| ID | Requirement | Measurable Target |
|---|---|---|
| NFR-004 | The system shall maintain 99.5% uptime during business hours (6 AM - 10 PM local time, Monday-Friday), excluding planned maintenance windows. | 99.5% availability during business hours, measured monthly |
| NFR-012 | The system shall support automated backups with a Recovery Point Objective (RPO) of 1 hour and a Recovery Time Objective (RTO) of 4 hours. | RPO <= 1 hour; RTO <= 4 hours; backup restoration tested quarterly |
| NFR-017 | Planned maintenance windows shall not exceed 2 hours per month and shall be scheduled outside business hours with 48 hours advance notice. | Maintenance downtime <= 2 hours/month; scheduled with >= 48 hours notice |

### 5.4 Security

| ID | Requirement | Measurable Target |
|---|---|---|
| NFR-005 | All data in transit shall be encrypted using TLS 1.2 or higher. All data at rest shall be encrypted using AES-256 encryption. | 100% of communications use TLS 1.2+; 100% of stored data encrypted with AES-256 |
| NFR-008 | The system shall undergo regular security assessments including vulnerability scanning (monthly) and penetration testing (annually) with all critical and high findings remediated before go-live. | Zero critical/high vulnerabilities at go-live; monthly vulnerability scans; annual penetration test |
| NFR-013 | Audit logs shall be retained for a minimum of 2 years and stored in an immutable, tamper-proof manner separate from application data. | Audit log retention >= 2 years; logs stored in append-only storage with integrity verification |
| NFR-014 | The system shall implement input validation on all user inputs to prevent SQL injection, XSS, CSRF, and other OWASP Top 10 vulnerabilities. | Zero OWASP Top 10 vulnerabilities in security scans; all user inputs validated server-side |
| NFR-020 | The system shall implement rate limiting on authentication endpoints to prevent brute-force attacks, locking accounts after 5 consecutive failed login attempts for 15 minutes. | Account lockout after 5 failed attempts; 15-minute lockout period; rate limiting at 10 requests/minute on auth endpoints |

### 5.5 Compliance

| ID | Requirement | Measurable Target |
|---|---|---|
| NFR-006 | The system shall be designed and operated in compliance with SOC2 Type II requirements, covering Security, Availability, and Confidentiality trust service criteria. | Pass SOC2 Type II audit within 12 months of go-live |
| NFR-007 | The system shall comply with GDPR requirements for handling personal data of EU-based clients and employees, including data subject rights (access, erasure, portability). | Full GDPR compliance including data processing records, consent management, and subject rights fulfillment within 30 days of request |
| NFR-018 | The system shall implement multi-tenancy architecture ensuring logical data separation between client organizations to support SOC2 confidentiality requirements. | Client data isolation verified through automated tests and annual penetration testing |

### 5.6 Usability

| ID | Requirement | Measurable Target |
|---|---|---|
| NFR-009 | The system shall be intuitive enough for non-technical client users to navigate without training, targeting a System Usability Scale (SUS) score of 75 or above. | SUS score >= 75 in user acceptance testing with a sample of client users |
| NFR-010 | The system shall support responsive design with full functionality on viewports from 768px (tablet) to 1920px (desktop) width. | All critical user flows functional and visually correct at 768px, 1024px, 1366px, and 1920px viewport widths |
| NFR-019 | The system shall provide user-friendly error messages for all error conditions, with unique error codes for support escalation and contextual help links. | 100% of error states display user-friendly messages with error codes; no raw technical errors shown to end users |

---

## 6. Data Requirements

### 6.1 Core Data Entities

| Entity | Key Attributes | Relationships |
|---|---|---|
| **Organization** | id, name, type (internal/client), status | Has many Users, Projects |
| **User** | id, email, name, role(s), organization_id, status, 2fa_status | Belongs to Organization; Has many TimeEntries, TaskAssignments |
| **Project** | id, name, client_id, start_date, deadline, budget, status, phase | Belongs to Client Organization; Has many Tasks, Milestones, Documents |
| **Task** | id, project_id, title, description, assignee_ids, status, due_date, dependencies | Belongs to Project; Has many TimeEntries |
| **Milestone** | id, project_id, name, target_date, approval_status, approver_id | Belongs to Project; Has many Deliverables |
| **TimeEntry** | id, user_id, project_id, task_id, date, hours, billable, description, approval_status | Belongs to User, Project, Task |
| **Invoice** | id, project_id, client_id, line_items, total, status, quickbooks_id | Belongs to Project, Client; Generated from TimeEntries |
| **Document** | id, project_id, folder_path, filename, version, uploaded_by, upload_date | Belongs to Project; Has many Versions, Comments |
| **Comment** | id, document_id, user_id, content, parent_comment_id, timestamp | Belongs to Document, User |
| **Notification** | id, user_id, type, content, read_status, trigger_event, timestamp | Belongs to User |
| **AuditLog** | id, user_id, action, resource_type, resource_id, before_value, after_value, timestamp | Immutable append-only |

### 6.2 Data Migration Requirements

- Import sources: CSV and Excel files from existing spreadsheets and shared drives
- Data types to migrate: Projects, clients, team members, historical time entries
- Validation: All imported data must pass validation rules before committing
- Dry-run mode: Preview import results without committing changes
- Error handling: Report validation errors per row with specific field-level detail
- Rollback: Failed imports must not leave partial data in the system

### 6.3 Data Retention

- Application data: Retained for the life of the platform
- Audit logs: Minimum 2-year retention in immutable storage (NFR-013)
- Deleted records: Soft-delete with administrator ability to purge per GDPR (NFR-007)
- Backups: RPO of 1 hour, RTO of 4 hours (NFR-012)

---

## 7. Integration Requirements

### 7.1 Integration Summary

| Integration | Direction | Protocol | Priority | FR Reference |
|---|---|---|---|---|
| QuickBooks Online | Bi-directional | REST API / OAuth 2.0 | HIGH | FR-020, FR-025 |
| Slack | Outbound | Webhooks / Slack API | HIGH | FR-021 |
| Google Calendar | Bi-directional | Google Calendar API / OAuth 2.0 | MEDIUM | FR-022 |
| Figma | Inbound (read-only) | Figma REST API / oEmbed | LOW | FR-023 |
| GitHub | Inbound (read-only) | GitHub REST API / Webhooks | LOW | FR-024 |
| Google Workspace SSO | Inbound (authentication) | SAML 2.0 / OIDC | HIGH | FR-046 |
| Email (SMTP) | Outbound | SMTP / Transactional Email Service | HIGH | FR-010, FR-041 |

### 7.2 Integration Design Principles

1. **Graceful Degradation**: Core platform functionality must operate without external integrations. If QuickBooks, Slack, or Google Calendar is unavailable, the platform continues operating with queued sync.
2. **Circuit Breaker Pattern**: All external API calls must implement circuit breaker patterns to prevent cascading failures.
3. **Retry Logic**: Failed API calls are retried with exponential backoff. After maximum retries, errors are logged and administrators are notified.
4. **Sync Queue**: All integration operations are processed through a durable message queue to ensure reliability.
5. **Error Logging**: All integration errors are logged with full request/response context for debugging.

### 7.3 QuickBooks Integration Detail

- **Authentication**: OAuth 2.0 with token refresh
- **Sync Direction**: Finalized invoices pushed to QuickBooks; payment status synced back
- **Data Mapping**: Invoice line items, client details, tax calculations, payment terms
- **Sync Frequency**: Configurable (default: every 15 minutes for payment status; immediate for new invoices)
- **Error Handling**: Sync errors queued for retry; admin dashboard shows sync status and error log
- **Configuration**: Admin panel for OAuth connection, account mapping, sync schedule

---

## 8. UI/UX Requirements

### 8.1 General UX Principles

1. The interface must be intuitive for non-technical users (client portal SUS score >= 75)
2. All critical workflows must be completable in 3 clicks or fewer from the main navigation
3. Consistent design language across all modules (spacing, typography, color, component patterns)
4. Error messages must be user-friendly with unique error codes and contextual help (NFR-019)
5. No raw technical errors displayed to end users

### 8.2 Responsive Design

| Viewport | Support Level | Key Adaptations |
|---|---|---|
| 1920px (Desktop) | Full | All features and layouts at maximum fidelity |
| 1366px (Laptop) | Full | Minor layout adjustments; no feature reduction |
| 1024px (Tablet Landscape) | Full | Collapsible sidebars; condensed tables |
| 768px (Tablet Portrait) | Full | Stacked layouts; touch-friendly targets; no horizontal scrolling |
| Below 768px (Mobile) | Not supported in Phase 1 | Redirect to mobile app (Phase 2) or basic responsive fallback |

### 8.3 Key UI Components

| Component | Description | Used In |
|---|---|---|
| **Project Dashboard** | Card or table view with status indicators, progress bars, filters, sorting | FR-001 |
| **Kanban Board** | Drag-and-drop columns (To Do, In Progress, In Review, Done) | FR-005 |
| **Resource Board** | Visual grid showing team members, projects, utilization percentages | FR-013 |
| **Timeline / Gantt** | Horizontal timeline with milestones and phase markers | FR-009 |
| **Time Tracker Widget** | Persistent timer widget accessible from any page | FR-011 |
| **Notification Bell** | Badge count with dropdown panel showing categorized notifications | FR-039 |
| **Global Search Bar** | Omnipresent search with instant results and RBAC filtering | FR-038 |
| **Document Viewer** | In-browser preview for common file types with comment panel | FR-016, FR-018 |
| **Admin Panel** | Tabbed interface for user management, integrations, settings | FR-040 |
| **Invoice Preview** | Line-item table with totals, adjustment controls, and finalization action | FR-012 |

### 8.4 Accessibility

- Minimum WCAG 2.1 Level AA compliance for all interactive elements
- Keyboard navigation support for all critical workflows
- Sufficient color contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Screen reader compatible labels on all form elements and interactive components

---

## 9. Security Requirements

### 9.1 Authentication

| Requirement | Implementation |
|---|---|
| Primary authentication | Email/password with mandatory 2FA (FR-034) |
| SSO authentication | Google Workspace via SAML 2.0 or OIDC (FR-046) |
| 2FA methods | TOTP (Google Authenticator, Authy) and SMS fallback (FR-034) |
| Password policy | Minimum 12 characters, complexity requirements, 90-day expiry, no reuse of last 10 passwords (FR-047) |
| Session management | 30-minute inactivity timeout with 5-minute warning (FR-048) |
| Account lockout | Lock after 5 failed login attempts for 15 minutes (NFR-020) |
| Rate limiting | 10 requests/minute on authentication endpoints (NFR-020) |

### 9.2 Authorization

| Requirement | Implementation |
|---|---|
| Access control model | Role-Based Access Control (RBAC) with 7 predefined roles (FR-033) |
| Client data isolation | Tenant-scoped queries; no cross-client data leakage (FR-036) |
| Permission enforcement | Server-side authorization checks on every API endpoint |
| Multi-tenancy | Logical data separation with tenant-scoped database queries (NFR-018) |

### 9.3 Data Protection

| Requirement | Implementation |
|---|---|
| Data in transit | TLS 1.2 or higher for all communications (NFR-005) |
| Data at rest | AES-256 encryption for all stored data (NFR-005) |
| Password storage | bcrypt or equivalent hashing algorithm (FR-047) |
| Audit logging | Immutable, append-only audit logs with 2-year retention (FR-035, NFR-013) |
| Input validation | Server-side validation on all inputs; OWASP Top 10 prevention (NFR-014) |

### 9.4 Compliance

| Framework | Requirement |
|---|---|
| SOC2 Type II | Security, Availability, and Confidentiality trust service criteria; audit-ready within 12 months (NFR-006) |
| GDPR | Data subject rights (access, erasure, portability); consent management; data processing records (NFR-007) |
| Security testing | Monthly vulnerability scans; annual penetration tests; zero critical/high findings at go-live (NFR-008) |

---

## 10. Traceability Matrix

### 10.1 Feature to Functional Requirement to Module Mapping

| Feature ID | Feature Name | Functional Requirements | Module |
|---|---|---|---|
| F-001 | Project Management & Centralization | FR-001, FR-002, FR-003, FR-004, FR-005 | Project Management |
| F-002 | Client Portal | FR-006, FR-007, FR-008, FR-009, FR-010 | Client Portal |
| F-003 | Time Tracking & Invoicing | FR-011, FR-012, FR-026, FR-027, FR-028 | Time Tracking & Invoicing |
| F-004 | Resource Management | FR-013, FR-014, FR-015 | Resource Management |
| F-005 | Document Management | FR-016, FR-017, FR-018, FR-019 | Document Management |
| F-006 | QuickBooks Integration | FR-020, FR-025 | Integrations |
| F-007 | Slack Integration | FR-021 | Integrations |
| F-008 | Google Calendar Integration | FR-022 | Integrations |
| F-009 | Figma Integration | FR-023 | Integrations |
| F-010 | GitHub Integration | FR-024 | Integrations |
| F-011 | RBAC & Security Administration | FR-033, FR-035, FR-036, FR-040 | Security & Access Control, Administration |
| F-012 | Authentication & Session Security | FR-034, FR-047, FR-048 | Security & Access Control |
| F-013 | Reporting & Dashboards | FR-029, FR-030, FR-031, FR-032 | Reporting & Analytics |
| F-014 | Responsive Web Platform | FR-037 | Platform & UX |
| F-015 | Mobile App (Phase 2) | FR-043 | Platform & UX |
| F-016 | AI-Powered Estimation (Phase 2) | FR-044 | Reporting & Analytics |
| F-017 | Advanced Analytics (Phase 2) | FR-045 | Reporting & Analytics |

### 10.2 Cross-Cutting Concerns

| Concern | Applicable FRs | Description |
|---|---|---|
| Search | FR-038 | Global search across projects, tasks, documents, clients |
| Notifications | FR-010, FR-021, FR-039 | Email (client), Slack (team), in-app (all) |
| Data Migration | FR-042 | Bulk import to project management data model |
| User Onboarding | FR-041 | Email invitations with role assignment and 2FA setup |
| SSO | FR-046 | Google Workspace authentication for internal users |

### 10.3 Dependency Map

The following table summarizes inter-requirement dependencies. "Requires" means the dependent FR cannot function without the prerequisite. "Enhances" means the FR adds value but is not strictly necessary.

| FR (Dependent) | Prerequisite FR | Dependency Type |
|---|---|---|
| FR-001 | FR-033 | Requires |
| FR-002 | FR-033 | Requires |
| FR-003 | FR-002 | Requires |
| FR-004 | FR-002 | Requires |
| FR-006 | FR-033, FR-036 | Requires |
| FR-007 | FR-006, FR-016 | Requires |
| FR-008 | FR-006 | Requires |
| FR-011 | FR-002 | Requires |
| FR-012 | FR-011, FR-026, FR-027 | Requires |
| FR-013 | FR-003 | Requires |
| FR-014 | FR-013 | Requires |
| FR-015 | FR-013 | Requires |
| FR-017 | FR-016 | Requires |
| FR-018 | FR-016 | Requires |
| FR-019 | FR-017 | Requires |
| FR-020 | FR-012, FR-025 | Requires |
| FR-021 | FR-003 | Enhances |
| FR-022 | FR-004 | Enhances |
| FR-023 | FR-016 | Enhances |
| FR-024 | FR-002 | Enhances |
| FR-028 | FR-011 | Requires |
| FR-029 | FR-011, FR-012, FR-013 | Requires |
| FR-030 | FR-029 | Requires |
| FR-031 | FR-029 | Requires |
| FR-032 | FR-029 | Enhances |
| FR-034 | FR-040 | Requires |
| FR-036 | FR-033 | Requires |
| FR-038 | FR-033 | Requires |
| FR-041 | FR-033, FR-034 | Requires |
| FR-042 | FR-002 | Requires |
| FR-044 | FR-029 | Requires |
| FR-045 | FR-029 | Requires |
| FR-046 | FR-033 | Enhances |
| FR-010 | FR-007 | Enhances |

---

*End of Functional Requirements Document*
