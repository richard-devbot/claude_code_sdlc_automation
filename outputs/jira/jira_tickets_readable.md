# TechNova Solutions — JIRA Ticket Definitions

**Project:** TechNova Solutions — Client Project Management Platform
**Domain:** Professional Services / Digital Agency Management
**Generated:** 2026-03-12
**Ticketing Mode:** File-Based (Mode 3)

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Epics | 11 |
| Total User Stories | 56 (48 FR-based + 8 domain-specific SaaS) |
| Total Technical Tasks | 168 |
| Total Story Points | 299 |
| FR Coverage | 48/48 (100%) |

### Stories Per Sprint

| Sprint | Theme | Story Count |
|--------|-------|-------------|
| Sprint 0 | Foundation & Setup | 6 (domain-specific) |
| Sprint 1 | Core Auth, Security & Admin | 10 |
| Sprint 2 | Project Management Core | 4 |
| Sprint 3 | Kanban & Time Tracking | 5 |
| Sprint 4 | Client Portal & Documents | 5 |
| Sprint 5 | Portal Completion & Resources | 5 |
| Sprint 6 | Resources & Core Integrations | 5 |
| Sprint 7 | Integrations & Reporting | 6 |
| Sprint 8 | Reports, Platform & Migration | 7 |
| Sprint 9 | Hardening & Phase 2 Prep | 3 |

---

## EPIC-001: Project Management

**Module:** Project Management | **Priority:** CRITICAL
**Description:** Core project tracking, task management, milestone tracking, and Kanban/list views to replace spreadsheet-based project tracking.
**Requirements:** FR-001, FR-002, FR-003, FR-004, FR-005

---

### US-001 — Centralized Project Dashboard
**Sprint 2** | **8 SP** | **Priority:** Critical | **FR:** FR-001

> As a Project Manager, I want to view a centralized dashboard of all active projects so that I can monitor status, deadlines, and team assignments at a glance

**Acceptance Criteria:**
1. GIVEN I am a logged-in Project Manager WHEN I navigate to the project dashboard THEN I see all active projects with status, team, deadline, and completion percentage columns
2. GIVEN the dashboard is displayed WHEN I click on a column header THEN the projects are sorted by that column in ascending/descending order
3. GIVEN the dashboard is displayed WHEN I apply filters by status, client, or team member THEN only matching projects are shown
4. GIVEN a project status changes WHEN another user updates it THEN the dashboard reflects the change within 5 seconds without a full page refresh

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-001 | Build project dashboard REST API with filtering, sorting, and pagination | Backend Dev | 12 | development |
| T-002 | Implement project dashboard UI with data table, filters, and real-time indicators | Frontend Dev | 14 | development |
| T-003 | Write E2E tests for dashboard filtering, sorting, pagination, and real-time updates | QA Engineer | 8 | testing |

---

### US-002 — Project CRUD Operations
**Sprint 2** | **5 SP** | **Priority:** Critical | **FR:** FR-002

> As an Administrator, I want to create, edit, and archive projects with configurable fields so that project records are complete and organized

**Acceptance Criteria:**
1. GIVEN I am an Administrator WHEN I click 'Create Project' THEN I see a form with all configurable fields (name, client, dates, budget, team, phases)
2. GIVEN a project exists WHEN I edit any field and save THEN the changes are persisted and reflected in the dashboard immediately
3. GIVEN a completed project WHEN I click 'Archive' THEN it is hidden from the active dashboard but remains accessible via search
4. GIVEN I search for an archived project WHEN I view its details THEN all historical data including tasks, milestones, and time entries are preserved

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-004 | Build Project domain model and CRUD REST APIs with validation | Backend Dev | 10 | development |
| T-005 | Implement project creation wizard and edit forms with field validation | Frontend Dev | 10 | development |
| T-006 | Test project CRUD operations, archival, and search for archived projects | QA Engineer | 6 | testing |

---

### US-003 — Task Management with Dependencies
**Sprint 2** | **8 SP** | **Priority:** Critical | **FR:** FR-003

> As a Team Member, I want to manage tasks within projects with status tracking and dependencies so that I can organize and track my work

**Acceptance Criteria:**
1. GIVEN I am within a project WHEN I create a task THEN I can assign it to team members, set a due date, and add a description
2. GIVEN a task exists WHEN I change its status THEN only valid transitions are allowed (e.g., To Do -> In Progress, In Progress -> In Review)
3. GIVEN Task B depends on Task A WHEN Task A is not yet Done THEN Task B shows a dependency warning if moved to In Progress
4. GIVEN I am a Project Manager WHEN I view the task list THEN I can see all tasks with their status, assignee, due date, and dependency indicators

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-007 | Build Task domain model, status workflow engine, and dependency graph logic | Backend Dev | 14 | development |
| T-008 | Implement task list view with inline editing, status transitions, and dependency indicators | Frontend Dev | 12 | development |
| T-009 | Test task workflow transitions, dependency validation, and edge cases | QA Engineer | 8 | testing |

---

### US-004 — Milestone Tracking with Approvals
**Sprint 2** | **5 SP** | **Priority:** Critical | **FR:** FR-004

> As a Project Manager, I want to define milestones with target dates and client approval requirements so that I can track project progress against key deliverables

**Acceptance Criteria:**
1. GIVEN I am a Project Manager WHEN I create a milestone THEN I can set a name, target date, link deliverables, and toggle client approval requirement
2. GIVEN a milestone requires client approval WHEN it is marked complete THEN the client receives a notification and the milestone cannot be finalized until approved
3. GIVEN a Client User receives an approval request WHEN they approve the milestone THEN it is marked as approved with a timestamp
4. GIVEN milestones exist WHEN I view the project timeline THEN all milestones display with their status (pending, awaiting approval, approved, overdue)

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-010 | Build Milestone service with approval state machine and notification triggers | Backend Dev | 10 | development |
| T-011 | Implement milestone timeline component and approval UI | Frontend Dev | 8 | development |
| T-012 | Test milestone approval flows, notifications, and edge cases | QA Engineer | 6 | testing |

---

### US-005 — Kanban Board with Drag-and-Drop
**Sprint 3** | **5 SP** | **Priority:** High | **FR:** FR-005

> As a Team Member, I want to use a Kanban board with drag-and-drop to move tasks between status columns so that I can visually manage my workflow

**Acceptance Criteria:**
1. GIVEN I am viewing a project WHEN I toggle to Kanban view THEN I see tasks organized in columns by status (To Do, In Progress, In Review, Done)
2. GIVEN I am in Kanban view WHEN I drag a task from one column to another THEN the task status updates in real time for all viewers
3. GIVEN I am in Kanban view WHEN I toggle to list view THEN I see the same tasks in a tabular format with sorting and filtering
4. GIVEN another user moves a task WHEN I am viewing the Kanban board THEN the change is reflected without a page refresh

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-013 | Build Kanban board API endpoints with real-time status update support via WebSocket | Backend Dev | 8 | development |
| T-014 | Implement Kanban board UI with drag-and-drop and list view toggle | Frontend Dev | 12 | development |
| T-015 | Test Kanban drag-and-drop across browsers and real-time sync between users | QA Engineer | 6 | testing |

---

## EPIC-002: Client Portal

**Module:** Client Portal | **Priority:** CRITICAL
**Description:** Client-facing portal with project dashboards, deliverable review, milestone approvals, messaging, and email notifications.
**Requirements:** FR-006, FR-007, FR-008, FR-009, FR-010

---

### US-006 — Client Portal Dashboard
**Sprint 4** | **8 SP** | **Priority:** Critical | **FR:** FR-006

> As a Client User, I want to log in to a dedicated portal and view my project dashboard so that I can check project status without contacting the team

**Acceptance Criteria:**
1. GIVEN I am a Client User WHEN I log in to the client portal THEN I see only projects belonging to my organization
2. GIVEN I am on my client dashboard WHEN I view project details THEN I see status, milestones, recent activity, and upcoming deadlines
3. GIVEN I am a Client User WHEN I attempt to access another client's project THEN I receive an access denied error
4. GIVEN I am a Client User WHEN I navigate the portal THEN the UI is distinct from the internal application with a client-friendly theme

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-016 | Build client portal API layer with tenant isolation middleware | Backend Dev | 12 | development |
| T-017 | Build client portal UI shell with separate theme and client dashboard | Frontend Dev | 14 | development |
| T-018 | Test client data isolation with cross-tenant access penetration tests | QA Engineer | 8 | testing |

---

### US-007 — Deliverable Review and Milestone Approval
**Sprint 4** | **5 SP** | **Priority:** Critical | **FR:** FR-007

> As a Client User, I want to view and download deliverables and approve or request revisions on milestones so that I can provide timely feedback

**Acceptance Criteria:**
1. GIVEN I am a Client User WHEN I navigate to a milestone THEN I see associated deliverables with download links
2. GIVEN a deliverable is available WHEN I click 'Download' THEN the file downloads successfully
3. GIVEN a milestone requires my approval WHEN I click 'Approve' THEN the milestone status updates and the team is notified
4. GIVEN a milestone requires my approval WHEN I click 'Request Revision' THEN I must enter a comment explaining the required changes

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-019 | Build deliverable approval state machine and notification triggers for client actions | Backend Dev | 8 | development |
| T-020 | Implement deliverable review interface with download, approve, and revision request UI | Frontend Dev | 10 | development |
| T-021 | Test deliverable approval workflow including edge cases and notification delivery | QA Engineer | 6 | testing |

---

### US-008 — Client Portal Messaging
**Sprint 4** | **5 SP** | **Priority:** Critical | **FR:** FR-008

> As a Client User, I want to communicate with my project team through threaded messages so that all project discussions are centralized

**Acceptance Criteria:**
1. GIVEN I am a Client User WHEN I open a project's messaging section THEN I see threaded conversations with the project team
2. GIVEN I am composing a message WHEN I type and send THEN the message appears in the thread and the team receives a notification
3. GIVEN a Team Member replies WHEN I return to the portal THEN I see the new reply in the conversation thread
4. GIVEN I am sending a message WHEN I attach a file THEN the file is uploaded and accessible within the thread

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-022 | Build messaging service with WebSocket real-time delivery and file attachment support | Backend Dev | 12 | development |
| T-023 | Implement threaded messaging component with file attachment and real-time updates | Frontend Dev | 10 | development |
| T-024 | Test messaging delivery, notifications, file attachments, and cross-browser behavior | QA Engineer | 6 | testing |

---

### US-009 — Project Timeline / Gantt View
**Sprint 5** | **5 SP** | **Priority:** High | **FR:** FR-009

> As a Client User, I want to view a Gantt-style timeline of my project showing milestones and progress so that I understand the project schedule

**Acceptance Criteria:**
1. GIVEN I am a Client User WHEN I navigate to the timeline view THEN I see a Gantt chart with milestones, phases, and progress indicators
2. GIVEN the timeline is displayed WHEN I hover over a milestone THEN I see details including name, target date, status, and associated deliverables
3. GIVEN a project date changes WHEN I view the timeline THEN the updated dates are reflected automatically
4. GIVEN the current date is displayed WHEN I view the timeline THEN a 'today' marker shows the current position relative to the schedule

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-025 | Build timeline data API aggregating milestones, phases, and progress metrics | Backend Dev | 6 | development |
| T-026 | Implement Gantt chart component with milestone markers and progress visualization | Frontend Dev | 12 | development |
| T-027 | Test Gantt chart rendering accuracy, date updates, and responsiveness | QA Engineer | 4 | testing |

---

### US-010 — Automated Email Notifications
**Sprint 5** | **5 SP** | **Priority:** High | **FR:** FR-010

> As a Client User, I want to receive automated email notifications for key project events so that I stay informed without logging in

**Acceptance Criteria:**
1. GIVEN I am a Client User WHEN a milestone is completed THEN I receive an email notification with details
2. GIVEN I am a Client User WHEN a new deliverable is uploaded for my review THEN I receive an email with a direct link
3. GIVEN I am a Client User WHEN I configure my notification preferences THEN only selected event types trigger emails
4. GIVEN an email is sent WHEN I click a link in the email THEN I am directed to the relevant page in the client portal (with authentication)

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-028 | Build email notification service with event-driven triggers and user preference management | Backend Dev | 10 | development |
| T-029 | Implement email notification preference settings UI in client portal | Frontend Dev | 6 | development |
| T-030 | Test email delivery for all event types, preference enforcement, and link deep-linking | QA Engineer | 6 | testing |

---

## EPIC-003: Time Tracking & Invoicing

**Module:** Time Tracking & Invoicing | **Priority:** CRITICAL
**Description:** Billable/non-billable time tracking with timers and manual entry, configurable billing rates, approval workflows, timesheet views, and automated invoice generation.
**Requirements:** FR-011, FR-012, FR-026, FR-027, FR-028

---

### US-011 — Time Tracking with Timer
**Sprint 3** | **8 SP** | **Priority:** Critical | **FR:** FR-011

> As a Team Member, I want to log billable and non-billable hours using a start/stop timer or manual entry so that my time is accurately captured

**Acceptance Criteria:**
1. GIVEN I am a Team Member WHEN I start a timer against a task THEN the timer runs persistently across page navigation until I stop it
2. GIVEN I am a Team Member WHEN I manually enter time THEN I can specify date, hours, project, task, description, and billable/non-billable flag
3. GIVEN I have logged time entries WHEN I view my time log THEN I see all entries with project, task, hours, date, and billable status
4. GIVEN I am logging time WHEN I do not select a project and task THEN the system prevents submission and shows a validation error

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-031 | Build time entry service with timer state management and manual entry APIs | Backend Dev | 12 | development |
| T-032 | Implement timer widget persistent across navigation and manual time entry form | Frontend Dev | 10 | development |
| T-033 | Test timer accuracy, persistence, manual entry validation, and edge cases | QA Engineer | 6 | testing |

---

### US-012 — Automated Invoice Generation
**Sprint 7** | **8 SP** | **Priority:** Critical | **FR:** FR-012

> As a Finance Manager, I want the system to generate draft invoices from approved time entries so that billing is accurate and automated

**Acceptance Criteria:**
1. GIVEN approved time entries exist WHEN I generate a draft invoice THEN line items are calculated using the correct billing rate hierarchy
2. GIVEN a draft invoice is generated WHEN I review it THEN I can adjust line items, add discounts, or add manual entries before finalizing
3. GIVEN I finalize an invoice WHEN the invoice is saved THEN it becomes immutable and receives a unique invoice number
4. GIVEN finalized invoices exist WHEN I view the invoice list THEN I see status (Draft, Finalized, Sent, Paid) and totals

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-034 | Build invoice generation engine aggregating approved time entries with billing rate application | Backend Dev | 14 | development |
| T-035 | Implement invoice generation wizard with line item editing, adjustment, and finalization UI | Frontend Dev | 12 | development |
| T-036 | Test invoice calculation accuracy against time entries and billing rates, immutability after finalization | QA Engineer | 8 | testing |

---

### US-013 — Configurable Billing Rates
**Sprint 3** | **5 SP** | **Priority:** Critical | **FR:** FR-026

> As an Administrator, I want to configure billing rates at global, client, and project levels so that invoicing reflects our pricing structure

**Acceptance Criteria:**
1. GIVEN I am an Administrator WHEN I set global billing rates by role THEN those rates apply as defaults for all clients and projects
2. GIVEN I am a Finance Manager WHEN I set a client-level rate override THEN it takes precedence over the global rate for that client
3. GIVEN I set a project-level rate WHEN time is logged against that project THEN the project rate takes precedence over both client and global rates
4. GIVEN multiple rate levels exist WHEN an invoice is generated THEN the system correctly applies the most specific rate (project > client > global)

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-037 | Build billing rate hierarchy engine with cascading override logic | Backend Dev | 10 | development |
| T-038 | Implement billing rate configuration UI for global, client, and project levels | Frontend Dev | 8 | development |
| T-039 | Test billing rate override precedence validation across all levels | QA Engineer | 6 | testing |

---

### US-014 — Time Entry Approval Workflow
**Sprint 3** | **5 SP** | **Priority:** High | **FR:** FR-027

> As a Team Lead, I want to review and approve time entries before they are included in invoices so that billing accuracy is ensured

**Acceptance Criteria:**
1. GIVEN a Team Member submits time entries WHEN I am their approver THEN I see the entries in my approval queue
2. GIVEN I review a time entry WHEN I approve it THEN it is marked as approved and eligible for invoice generation
3. GIVEN I review a time entry WHEN I reject it THEN I must provide a reason and the Team Member is notified
4. GIVEN I reject a time entry WHEN the Team Member modifies and resubmits THEN it reappears in my approval queue

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-040 | Build time entry approval workflow state machine with notification triggers | Backend Dev | 8 | development |
| T-041 | Implement approval queue view with approve, reject, and request modification actions | Frontend Dev | 8 | development |
| T-042 | Test approval workflow edge cases including reject-resubmit cycles | QA Engineer | 6 | testing |

---

### US-015 — Timesheet Views
**Sprint 3** | **5 SP** | **Priority:** High | **FR:** FR-028

> As a Team Member, I want to view weekly and monthly timesheets with project breakdowns so that I can track my utilization

**Acceptance Criteria:**
1. GIVEN I am a Team Member WHEN I view my timesheet THEN I see a weekly grid with daily hours broken down by project
2. GIVEN I am a Team Lead WHEN I view my team's timesheets THEN I see each member's weekly/monthly summary
3. GIVEN I toggle to monthly view WHEN viewing timesheets THEN I see the monthly summary with billable vs. non-billable breakdown
4. GIVEN I am viewing a timesheet WHEN I click export THEN I can download the data as CSV or PDF

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-043 | Build timesheet aggregation queries with billable/non-billable breakdowns and export | Backend Dev | 8 | development |
| T-044 | Implement timesheet grid with weekly/monthly toggle and export functionality | Frontend Dev | 10 | development |
| T-045 | Test timesheet calculation accuracy and export format validation | QA Engineer | 4 | testing |

---

## EPIC-004: Resource Management

**Module:** Resource Management | **Priority:** HIGH
**Description:** Visual resource allocation board, team assignment management with capacity conflict detection, and capacity forecasting.
**Requirements:** FR-013, FR-014, FR-015

---

### US-016 — Resource Allocation Board
**Sprint 5** | **5 SP** | **Priority:** High | **FR:** FR-013

> As a Project Manager, I want to view a visual resource allocation board showing team utilization so that I can identify availability and overallocation

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-046 | Build resource allocation query service with utilization calculations | Backend Dev | 8 | development |
| T-047 | Implement resource allocation board with utilization bars and availability indicators | Frontend Dev | 12 | development |
| T-048 | Test resource utilization calculation accuracy and filter functionality | QA Engineer | 4 | testing |

---

### US-017 — Resource Assignment with Conflict Detection
**Sprint 6** | **5 SP** | **Priority:** High | **FR:** FR-014

> As a Project Manager, I want to assign and reassign team members with conflict detection so that no one is overallocated

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-049 | Build resource assignment service with capacity threshold conflict detection | Backend Dev | 10 | development |
| T-050 | Implement drag-and-drop assignment UI with overallocation warnings | Frontend Dev | 10 | development |
| T-051 | Test resource conflict detection edge cases and reassignment flows | QA Engineer | 6 | testing |

---

### US-018 — Capacity Forecasting
**Sprint 6** | **5 SP** | **Priority:** Medium | **FR:** FR-015

> As a Team Lead, I want to view capacity forecasting for the next 4-12 weeks so that I can plan future project staffing

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-052 | Build capacity forecasting engine using current schedule data with time window parameters | Backend Dev | 10 | development |
| T-053 | Implement capacity forecast chart with time window slider and team/skill/department filters | Frontend Dev | 10 | development |
| T-054 | Test forecast accuracy against manual calculations and filter functionality | QA Engineer | 4 | testing |

---

## EPIC-005: Document Management

**Module:** Document Management | **Priority:** HIGH
**Description:** Project document repository with version control, in-browser preview, commenting/annotation, and client approval workflows for deliverables.
**Requirements:** FR-016, FR-017, FR-018, FR-019

---

### US-019 — Document Repository with Upload/Preview
**Sprint 4** | **8 SP** | **Priority:** High | **FR:** FR-016

> As a Team Member, I want to upload, download, preview, and organize documents in project folders so that all project files are centralized

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-055 | Build document storage service (S3-compatible) with folder CRUD and permission checks | Backend Dev | 12 | development |
| T-056 | Implement document manager UI with folder tree, upload progress, and in-browser preview | Frontend Dev | 14 | development |
| T-057 | Test document upload/download/preview/delete across file types and permissions | QA Engineer | 6 | testing |

---

### US-020 — Document Version History
**Sprint 4** | **5 SP** | **Priority:** High | **FR:** FR-017

> As a Project Manager, I want automatic version history for all documents so that I can view, compare, and restore previous versions

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-058 | Build document versioning engine with version history, comparison, and restore APIs | Backend Dev | 10 | development |
| T-059 | Implement version history UI with list view, preview, and restore functionality | Frontend Dev | 8 | development |
| T-060 | Test version creation, download, preview, and restore across file types | QA Engineer | 4 | testing |

---

### US-021 — Document Commenting and Annotation
**Sprint 5** | **5 SP** | **Priority:** High | **FR:** FR-018

> As a Team Member, I want to comment and annotate on documents so that I can provide feedback directly on deliverables

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-061 | Build document comment service with threading, notifications, and permission enforcement | Backend Dev | 8 | development |
| T-062 | Implement document annotation and commenting overlay with threaded replies | Frontend Dev | 10 | development |
| T-063 | Test commenting and annotation across browsers, user roles, and notification delivery | QA Engineer | 4 | testing |

---

### US-022 — Deliverable Client Approval Workflow
**Sprint 5** | **5 SP** | **Priority:** High | **FR:** FR-019

> As a Project Manager, I want to submit deliverables for client approval through a formal workflow so that sign-offs are tracked

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-064 | Build deliverable approval workflow engine with status transitions and notification triggers | Backend Dev | 8 | development |
| T-065 | Implement deliverable submission and approval UI flow with status indicators | Frontend Dev | 8 | development |
| T-066 | Test deliverable approval state transitions and edge cases | QA Engineer | 4 | testing |

---

## EPIC-006: Integrations

**Module:** Integrations | **Priority:** HIGH
**Description:** Third-party integrations with QuickBooks, Slack, Google Calendar, Figma, and GitHub.
**Requirements:** FR-020, FR-021, FR-022, FR-023, FR-024, FR-025

---

### US-023 — QuickBooks Bi-directional Invoice Sync
**Sprint 6** | **8 SP** | **Priority:** High | **FR:** FR-020

> As a Finance Manager, I want finalized invoices to sync bi-directionally with QuickBooks so that our accounting system stays current

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-067 | Build QuickBooks API client with OAuth2 flow, invoice push, and payment status pull with retry queue | Backend Dev | 16 | development |
| T-068 | Implement QuickBooks sync status dashboard with log viewer | Frontend Dev | 6 | development |
| T-069 | Test QuickBooks sync data mapping, error handling, and retry behavior | QA Engineer | 8 | testing |

---

### US-024 — Slack Notification Integration
**Sprint 6** | **5 SP** | **Priority:** High | **FR:** FR-021

> As a Team Member, I want to receive Slack notifications for project events so that I stay informed in my primary communication tool

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-070 | Build Slack webhook/bot integration with event routing and retry queue | Backend Dev | 8 | development |
| T-071 | Implement Slack integration settings page with event-to-channel mapping | Frontend Dev | 6 | development |
| T-072 | Test Slack notification delivery per event type and retry behavior | QA Engineer | 4 | testing |

---

### US-025 — Google Calendar Sync
**Sprint 7** | **5 SP** | **Priority:** Medium | **FR:** FR-022

> As a Project Manager, I want project deadlines and milestones to sync with Google Calendar so that schedules are visible in my calendar

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-073 | Build Google Calendar API integration with OAuth, event CRUD, and auto-sync on date changes | Backend Dev | 10 | development |
| T-074 | Implement Google Calendar connection settings UI | Frontend Dev | 4 | development |
| T-075 | Test calendar sync accuracy and bi-directional update handling | QA Engineer | 4 | testing |

---

### US-026 — Figma Design Preview Integration
**Sprint 7** | **3 SP** | **Priority:** Low | **FR:** FR-023

> As a Team Member, I want to link Figma files to projects with preview thumbnails so that design assets are accessible from the platform

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-076 | Build Figma oEmbed/API integration for URL validation and thumbnail generation | Backend Dev | 6 | development |
| T-077 | Implement Figma link input with preview embed in document view | Frontend Dev | 4 | development |
| T-078 | Test Figma URL validation, thumbnail rendering, and link navigation | QA Engineer | 2 | testing |

---

### US-027 — GitHub Activity Integration
**Sprint 7** | **3 SP** | **Priority:** Low | **FR:** FR-024

> As a Team Lead, I want to view GitHub commit activity and PR status within the project dashboard so that I can track development progress

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-079 | Build GitHub API client for commit, branch, and PR data retrieval with OAuth | Backend Dev | 8 | development |
| T-080 | Implement GitHub activity widget for project dashboard | Frontend Dev | 6 | development |
| T-081 | Test GitHub integration display accuracy and data refresh | QA Engineer | 3 | testing |

---

### US-028 — QuickBooks Configuration Panel
**Sprint 6** | **5 SP** | **Priority:** High | **FR:** FR-025

> As an Administrator, I want to configure the QuickBooks connection with OAuth, account mapping, and sync monitoring so that the integration runs reliably

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-082 | Build QuickBooks OAuth configuration API with account mapping and schedule management | Backend Dev | 8 | development |
| T-083 | Implement QuickBooks admin configuration panel with OAuth, mapping, and sync logs | Frontend Dev | 8 | development |
| T-084 | Test QuickBooks OAuth flow, account mapping persistence, and sync schedule execution | QA Engineer | 4 | testing |

---

## EPIC-007: Reporting & Analytics

**Module:** Reporting & Analytics | **Priority:** CRITICAL
**Description:** Executive dashboards, project profitability reports, configurable report exports, NPS tracking, AI-powered estimation, and advanced analytics.
**Requirements:** FR-029, FR-030, FR-031, FR-032, FR-044, FR-045

---

### US-029 — Executive Dashboard with 5 KPIs
**Sprint 7** | **8 SP** | **Priority:** Critical | **FR:** FR-029

> As an Executive, I want an executive dashboard displaying five core KPIs so that I have real-time operational visibility

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-085 | Build executive dashboard aggregation queries for all five KPIs with drill-down data | Backend Dev | 14 | development |
| T-086 | Implement executive dashboard UI with drill-down charts using Chart.js or Recharts | Frontend Dev | 14 | development |
| T-087 | Test executive dashboard data accuracy, drill-down functionality, and performance | QA Engineer | 6 | testing |

---

### US-030 — Project Profitability Reports
**Sprint 8** | **8 SP** | **Priority:** Critical | **FR:** FR-030

> As a Project Manager, I want project profitability reports with variance analysis so that I can identify budget overruns early

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-088 | Build report generation engine with variance calculations at project/client/portfolio levels | Backend Dev | 12 | development |
| T-089 | Implement report builder UI with parameter selection, variance highlighting, and chart visualizations | Frontend Dev | 12 | development |
| T-090 | Test report calculation accuracy against raw data and export format validation | QA Engineer | 6 | testing |

---

### US-031 — Configurable Report Export and Scheduling
**Sprint 8** | **5 SP** | **Priority:** High | **FR:** FR-031

> As an Administrator, I want to export reports in multiple formats and schedule automated delivery so that stakeholders receive reports regularly

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-091 | Build PDF/CSV/Excel export service and scheduled report cron with email delivery | Backend Dev | 12 | development |
| T-092 | Implement export buttons and schedule configuration dialog for reports | Frontend Dev | 6 | development |
| T-093 | Test export format integrity (PDF rendering, CSV/Excel data accuracy) and scheduled delivery | QA Engineer | 6 | testing |

---

### US-032 — NPS Score Tracking
**Sprint 8** | **3 SP** | **Priority:** Medium | **FR:** FR-032

> As a Project Manager, I want to track and display NPS scores per project and client so that I can monitor client satisfaction trends

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-094 | Build NPS data model and aggregation service with trend calculations | Backend Dev | 6 | development |
| T-095 | Implement NPS entry form and trend chart with filtering | Frontend Dev | 6 | development |
| T-096 | Test NPS trend chart data accuracy and executive dashboard integration | QA Engineer | 3 | testing |

---

### US-033 — AI-Powered Project Estimation (Phase 2 Stub)
**Sprint 9** | **3 SP** | **Priority:** Low | **FR:** FR-044

> As a Project Manager, I want AI-powered project estimation suggesting effort and timelines based on historical data so that I can plan new projects more accurately

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-097 | Implement historical data collection hooks and feature flag for AI estimation stub | Backend Dev | 6 | development |
| T-098 | Build Phase 2 placeholder UI for AI estimation with data collection status | Frontend Dev | 3 | development |
| T-099 | Verify data collection hooks capture necessary fields for future model training | QA Engineer | 2 | testing |

---

### US-034 — Advanced Analytics (Phase 2 Stub)
**Sprint 9** | **3 SP** | **Priority:** Low | **FR:** FR-045

> As an Executive, I want advanced analytics with trend analysis and predictive scoring so that I can make data-driven strategic decisions

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-100 | Build advanced analytics data pipeline foundations and feature flag stub | Backend Dev | 6 | development |
| T-101 | Build Phase 2 placeholder UI for advanced analytics with pipeline status | Frontend Dev | 3 | development |
| T-102 | Verify data pipeline foundations capture and store metrics for future analytics | QA Engineer | 2 | testing |

---

## EPIC-008: Security & Access Control

**Module:** Security & Access Control | **Priority:** CRITICAL
**Description:** Role-based access control, two-factor authentication, audit trails, client data isolation, SSO, password policies, and session management.
**Requirements:** FR-033, FR-034, FR-035, FR-036, FR-046, FR-047, FR-048

---

### US-035 — RBAC with 7 Predefined Roles
**Sprint 1** | **8 SP** | **Priority:** Critical | **FR:** FR-033

> As an Administrator, I want to define and enforce role-based access control with 7 predefined roles so that each user sees only what they are authorized to access

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-103 | Build RBAC engine with 7 roles, permission matrix, and middleware enforcement | Backend Dev | 16 | development |
| T-104 | Implement role management UI and permission matrix display in admin panel | Frontend Dev | 8 | development |
| T-105 | Test RBAC permission matrix validation across all 7 roles and edge cases | QA Engineer | 10 | testing |

---

### US-036 — Mandatory Two-Factor Authentication
**Sprint 1** | **5 SP** | **Priority:** Critical | **FR:** FR-034

> As a User, I want to set up mandatory two-factor authentication so that my account is protected against unauthorized access

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-106 | Build 2FA service with TOTP (speakeasy) and SMS (Twilio) support including admin reset | Backend Dev | 12 | development |
| T-107 | Implement 2FA setup wizard with QR code generation and SMS verification flow | Frontend Dev | 8 | development |
| T-108 | Test 2FA enrollment, login flow, bypass attempts, and admin reset functionality | QA Engineer | 8 | testing |

---

### US-037 — Comprehensive Audit Trails
**Sprint 1** | **8 SP** | **Priority:** Critical | **FR:** FR-035

> As an Administrator, I want comprehensive audit trails of all user actions so that we can meet SOC2 compliance requirements

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-109 | Build audit trail event system with immutable log storage and search/export APIs | Backend Dev | 14 | development |
| T-110 | Implement audit log viewer in admin panel with search, filter, and export functionality | Frontend Dev | 6 | development |
| T-111 | Test audit log completeness, immutability, search accuracy, and export integrity | QA Engineer | 8 | testing |

---

### US-038 — Client Data Isolation
**Sprint 1** | **5 SP** | **Priority:** Critical | **FR:** FR-036

> As a Client User, I want strict data isolation so that I can never see another client's data

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-112 | Implement tenant-scoped query filters across all data access layers | Backend Dev | 10 | development |
| T-113 | Ensure all UI data-fetching passes tenant context and handles isolation errors gracefully | Frontend Dev | 4 | development |
| T-114 | Execute cross-tenant penetration tests and data isolation validation | QA Engineer | 8 | testing |

---

### US-039 — Google Workspace SSO
**Sprint 7** | **5 SP** | **Priority:** High | **FR:** FR-046

> As an Internal User, I want to log in using my Google Workspace credentials via SSO so that I do not need a separate password

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-115 | Build SSO service with SAML 2.0/OIDC for Google Workspace with email/password fallback | Backend Dev | 12 | development |
| T-116 | Implement SSO login button and admin SSO configuration UI | Frontend Dev | 6 | development |
| T-117 | Test SSO authentication flow, first-time provisioning, fallback, and edge cases | QA Engineer | 6 | testing |

---

### US-040 — Password Policies
**Sprint 1** | **3 SP** | **Priority:** High | **FR:** FR-047

> As a User, I want enforced password policies so that account security meets organizational standards

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-118 | Build password policy engine with complexity, expiry, and reuse prevention logic | Backend Dev | 8 | development |
| T-119 | Implement password change flow with real-time complexity indicator and expiry warnings | Frontend Dev | 4 | development |
| T-120 | Test password policy enforcement including all complexity rules, expiry, and reuse prevention | QA Engineer | 4 | testing |

---

### US-041 — Session Timeout with Warning
**Sprint 1** | **3 SP** | **Priority:** High | **FR:** FR-048

> As a User, I want automatic session timeout with a warning before expiry so that idle sessions do not pose a security risk

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-121 | Build session management service with inactivity tracking and timeout logic | Backend Dev | 6 | development |
| T-122 | Implement session timeout warning modal with countdown and extend session button | Frontend Dev | 4 | development |
| T-123 | Test session timeout at 30 minutes, warning at 25 minutes, and session extension | QA Engineer | 4 | testing |

---

## EPIC-009: Platform & UX

**Module:** Platform & UX | **Priority:** HIGH
**Description:** Responsive web application, global search, in-app notification center, and mobile app (Phase 2).
**Requirements:** FR-037, FR-038, FR-039, FR-043

---

### US-042 — Responsive Web Application
**Sprint 8** | **5 SP** | **Priority:** High | **FR:** FR-037

> As a User, I want the application to work responsively across desktop and tablet browsers so that I can use it on any supported device

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-124 | Audit and fix responsive layout across all breakpoints (768px-1920px) | Frontend Dev | 16 | development |
| T-125 | Execute cross-browser responsive testing matrix (Chrome, Firefox, Safari, Edge) | QA Engineer | 10 | testing |
| T-126 | Ensure all API responses work correctly with responsive UI components | Backend Dev | 4 | development |

---

### US-043 — Global Search
**Sprint 8** | **5 SP** | **Priority:** Medium | **FR:** FR-038

> As an Internal User, I want a global search that searches across projects, tasks, documents, and clients so that I can quickly find anything

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-127 | Build full-text search index across projects, tasks, documents, clients with RBAC filtering | Backend Dev | 12 | development |
| T-128 | Implement global search bar with autocomplete and categorized result display | Frontend Dev | 8 | development |
| T-129 | Test search relevance, RBAC filtering accuracy, and performance under load | QA Engineer | 6 | testing |

---

### US-044 — In-App Notification Center
**Sprint 8** | **5 SP** | **Priority:** Medium | **FR:** FR-039

> As a User, I want an in-app notification center so that I can see real-time updates for task assignments, deadlines, and messages

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-130 | Build WebSocket notification service with event dispatching and user preference management | Backend Dev | 10 | development |
| T-131 | Implement notification bell icon with dropdown panel, categories, and preference settings | Frontend Dev | 8 | development |
| T-132 | Test notification delivery timing, preference enforcement, and real-time updates | QA Engineer | 6 | testing |

---

### US-045 — Mobile App (Phase 2 Stub)
**Sprint 9** | **3 SP** | **Priority:** Low | **FR:** FR-043

> As a Team Member, I want a mobile-optimized native app for time tracking so that I can log hours on the go

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-133 | Document and build mobile-optimized API endpoints for time tracking and task views | Backend Dev | 6 | development |
| T-134 | Ensure responsive web time tracking is usable at mobile viewport widths | Frontend Dev | 4 | development |
| T-135 | Test mobile API endpoints for payload size, response time, and correctness | QA Engineer | 3 | testing |

---

## EPIC-010: Administration

**Module:** Administration | **Priority:** CRITICAL
**Description:** Admin panel for user management, role/permission configuration, integration settings, billing rate management, and user onboarding with email invitations.
**Requirements:** FR-040, FR-041

---

### US-046 — Centralized Admin Panel
**Sprint 1** | **8 SP** | **Priority:** Critical | **FR:** FR-040

> As an Administrator, I want a centralized admin panel to manage users, roles, integrations, and system settings so that I have full platform control

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-136 | Build admin panel API endpoints for user CRUD, role management, and system configuration | Backend Dev | 14 | development |
| T-137 | Implement admin panel layout with user management, role management, and settings screens | Frontend Dev | 14 | development |
| T-138 | Test admin panel CRUD operations, role changes, and settings persistence | QA Engineer | 6 | testing |

---

### US-047 — User Invitation and Onboarding
**Sprint 1** | **5 SP** | **Priority:** High | **FR:** FR-041

> As an Administrator, I want to invite users via email with predefined role assignments so that onboarding is streamlined

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-139 | Build invitation service with email dispatch, token generation, expiry, and acceptance flow | Backend Dev | 8 | development |
| T-140 | Implement invitation form in admin panel and account setup page for invitees | Frontend Dev | 6 | development |
| T-141 | Test invitation sending, acceptance, expiry, and role pre-assignment | QA Engineer | 4 | testing |

---

## EPIC-011: Data Migration

**Module:** Data Migration | **Priority:** HIGH
**Description:** Bulk import of existing project data, client records, and historical time entries from CSV/Excel.
**Requirements:** FR-042

---

### US-048 — Data Migration Import Wizard
**Sprint 8** | **8 SP** | **Priority:** High | **FR:** FR-042

> As an Administrator, I want to bulk import project data, clients, and time entries from CSV/Excel so that historical data is migrated into the platform

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-142 | Build CSV/Excel parser with validation engine, dry-run mode, and batch import transaction management | Backend Dev | 14 | development |
| T-143 | Implement data migration wizard with file upload, field mapping, validation results, and import progress | Frontend Dev | 12 | development |
| T-144 | Test data migration with valid, invalid, and edge-case data files including large datasets | QA Engineer | 8 | testing |

---

## Domain-Specific SaaS Stories

These stories address standard SaaS platform requirements that cross-cut the functional requirements.

---

### US-049 — Multi-Tenancy Data Isolation (SaaS)
**Sprint 0** | **5 SP** | **Priority:** Critical | **Epic:** EPIC-008

> As an Administrator, I want multi-tenancy data isolation configured from day one so that client data is never exposed across organizations

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-145 | Design and implement multi-tenant database schema with tenant_id on all client-scoped tables | Backend Dev | 12 | development |
| T-146 | Implement tenant context provider in frontend for all API requests | Frontend Dev | 4 | development |
| T-147 | Write automated tests verifying tenant isolation across all data access endpoints | QA Engineer | 8 | testing |

---

### US-050 — Subscription and Billing Management (SaaS)
**Sprint 0** | **5 SP** | **Priority:** High | **Epic:** EPIC-010

> As an Administrator, I want subscription and billing management so that we can manage client billing plans and payment tracking

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-148 | Build billing management service with subscription plans, payment tracking, and invoice generation | Backend Dev | 10 | development |
| T-149 | Implement billing management UI in admin panel | Frontend Dev | 8 | development |
| T-150 | Test billing cycle processing, payment status updates, and overdue flagging | QA Engineer | 6 | testing |

---

### US-051 — Guided Onboarding Experience (SaaS)
**Sprint 0** | **5 SP** | **Priority:** High | **Epic:** EPIC-009

> As a new User, I want a guided onboarding experience so that I can quickly learn how to use the platform

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-151 | Build onboarding state tracker and role-specific tutorial content API | Backend Dev | 6 | development |
| T-152 | Implement multi-step onboarding wizard and contextual tooltip system | Frontend Dev | 10 | development |
| T-153 | Test onboarding flow for all 7 user roles and tooltip display | QA Engineer | 4 | testing |

---

### US-052 — Platform Health Monitoring (SaaS)
**Sprint 0** | **5 SP** | **Priority:** Medium | **Epic:** EPIC-010

> As an Administrator, I want platform health monitoring and system status so that I can proactively identify issues

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-154 | Build system health metrics collection and aggregation service | Backend Dev | 8 | development |
| T-155 | Implement system health dashboard with metric charts and alert indicators | Frontend Dev | 8 | development |
| T-156 | Test metric accuracy, threshold alerts, and historical trend data | QA Engineer | 4 | testing |

---

### US-053 — Environment Configuration Management (SaaS)
**Sprint 0** | **3 SP** | **Priority:** Medium | **Epic:** EPIC-010

> As an Administrator, I want to configure environment-specific settings for staging and production so that deployments are consistent and controlled

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-157 | Build environment configuration management service with feature flags and audit logging | Backend Dev | 8 | development |
| T-158 | Implement environment configuration UI with feature flag toggles | Frontend Dev | 4 | development |
| T-159 | Test environment configuration isolation and feature flag enforcement | QA Engineer | 3 | testing |

---

### US-054 — Automated Backup and Restore (SaaS)
**Sprint 0** | **5 SP** | **Priority:** High | **Epic:** EPIC-008

> As an Administrator, I want automated database backup and restore capabilities so that data is protected against loss

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-160 | Configure automated database backup service with hourly snapshots and retention policies | Backend Dev | 8 | development |
| T-161 | Build backup status and restore initiation UI in admin panel | Frontend Dev | 4 | development |
| T-162 | Test backup execution, restore procedures, and RPO/RTO compliance | QA Engineer | 6 | testing |

---

### US-055 — Rate Limiting and Brute-Force Protection (SaaS)
**Sprint 1** | **3 SP** | **Priority:** High | **Epic:** EPIC-008

> As an Administrator, I want rate limiting and brute-force protection on authentication endpoints so that the platform is protected from attacks

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-163 | Implement rate limiting middleware and account lockout logic on authentication endpoints | Backend Dev | 6 | development |
| T-164 | Display account lockout status and manual unlock option in admin panel | Frontend Dev | 2 | development |
| T-165 | Test brute-force protection: 5 failed attempts lockout, rate limiting, and manual unlock | QA Engineer | 4 | testing |

---

### US-056 — GDPR-Compliant Data Management (SaaS)
**Sprint 1** | **5 SP** | **Priority:** High | **Epic:** EPIC-008

> As an Administrator, I want GDPR-compliant data management with data subject rights support so that we meet regulatory requirements

**Tasks:**
| ID | Task | Role | Hours | Type |
|----|------|------|-------|------|
| T-166 | Build GDPR data subject rights service with export, erasure, and consent tracking | Backend Dev | 10 | development |
| T-167 | Implement consent dialog, data request form, and GDPR request log in admin panel | Frontend Dev | 6 | development |
| T-168 | Test data export completeness, erasure thoroughness, and consent enforcement | QA Engineer | 6 | testing |

---

## FR Coverage Traceability Matrix

| FR ID | User Story | Sprint | Epic |
|-------|-----------|--------|------|
| FR-001 | US-001 | 2 | EPIC-001 |
| FR-002 | US-002 | 2 | EPIC-001 |
| FR-003 | US-003 | 2 | EPIC-001 |
| FR-004 | US-004 | 2 | EPIC-001 |
| FR-005 | US-005 | 3 | EPIC-001 |
| FR-006 | US-006 | 4 | EPIC-002 |
| FR-007 | US-007 | 4 | EPIC-002 |
| FR-008 | US-008 | 4 | EPIC-002 |
| FR-009 | US-009 | 5 | EPIC-002 |
| FR-010 | US-010 | 5 | EPIC-002 |
| FR-011 | US-011 | 3 | EPIC-003 |
| FR-012 | US-012 | 7 | EPIC-003 |
| FR-013 | US-016 | 5 | EPIC-004 |
| FR-014 | US-017 | 6 | EPIC-004 |
| FR-015 | US-018 | 6 | EPIC-004 |
| FR-016 | US-019 | 4 | EPIC-005 |
| FR-017 | US-020 | 4 | EPIC-005 |
| FR-018 | US-021 | 5 | EPIC-005 |
| FR-019 | US-022 | 5 | EPIC-005 |
| FR-020 | US-023 | 6 | EPIC-006 |
| FR-021 | US-024 | 6 | EPIC-006 |
| FR-022 | US-025 | 7 | EPIC-006 |
| FR-023 | US-026 | 7 | EPIC-006 |
| FR-024 | US-027 | 7 | EPIC-006 |
| FR-025 | US-028 | 6 | EPIC-006 |
| FR-026 | US-013 | 3 | EPIC-003 |
| FR-027 | US-014 | 3 | EPIC-003 |
| FR-028 | US-015 | 3 | EPIC-003 |
| FR-029 | US-029 | 7 | EPIC-007 |
| FR-030 | US-030 | 8 | EPIC-007 |
| FR-031 | US-031 | 8 | EPIC-007 |
| FR-032 | US-032 | 8 | EPIC-007 |
| FR-033 | US-035 | 1 | EPIC-008 |
| FR-034 | US-036 | 1 | EPIC-008 |
| FR-035 | US-037 | 1 | EPIC-008 |
| FR-036 | US-038 | 1 | EPIC-008 |
| FR-037 | US-042 | 8 | EPIC-009 |
| FR-038 | US-043 | 8 | EPIC-009 |
| FR-039 | US-044 | 8 | EPIC-009 |
| FR-040 | US-046 | 1 | EPIC-010 |
| FR-041 | US-047 | 1 | EPIC-010 |
| FR-042 | US-048 | 8 | EPIC-011 |
| FR-043 | US-045 | 9 | EPIC-009 |
| FR-044 | US-033 | 9 | EPIC-007 |
| FR-045 | US-034 | 9 | EPIC-007 |
| FR-046 | US-039 | 7 | EPIC-008 |
| FR-047 | US-040 | 1 | EPIC-008 |
| FR-048 | US-041 | 1 | EPIC-008 |
