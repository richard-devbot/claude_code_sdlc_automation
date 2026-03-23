# Test Cases — TechNova Solutions Client Project Management Platform

**Document Version:** 1.0
**Date:** 2026-03-12
**Total Test Cases:** 312
**Coverage:** US-001 through US-056

---

## EPIC-001: Project Management (US-001 to US-005)

### US-001: Centralized Project Dashboard

```
TC-001: Verify project dashboard displays all active projects
User Story: US-001
Test Type: Functional
Precondition: User logged in as Project Manager; 5+ active projects exist
Test Steps:
  1. Navigate to /dashboard/projects
  2. Observe the project list
Expected Result: All active projects display with status, team, deadline, and completion percentage columns
Priority: Critical
```

```
TC-002: Verify dashboard sorting by column headers
User Story: US-001
Test Type: Functional
Precondition: Dashboard loaded with 5+ projects
Test Steps:
  1. Click on the "Deadline" column header
  2. Observe sort order
  3. Click again to toggle
Expected Result: Projects sort ascending on first click, descending on second click
Priority: High
```

```
TC-003: Verify dashboard filtering by status, client, and team member
User Story: US-001
Test Type: Functional
Precondition: Dashboard loaded with projects of varying statuses and clients
Test Steps:
  1. Select filter "Status = Active"
  2. Observe filtered results
  3. Add filter "Client = Acme Corp"
  4. Observe combined filter results
Expected Result: Only projects matching all applied filters are shown
Priority: High
```

```
TC-004: Verify real-time dashboard update within 5 seconds
User Story: US-001
Test Type: Integration
Precondition: Two browser sessions logged in; dashboard open in both
Test Steps:
  1. In Session A, update a project status
  2. Observe Session B dashboard within 5 seconds
Expected Result: Session B reflects the status change without full page refresh within 5 seconds
Priority: High
```

```
TC-005: Verify dashboard pagination with 40+ projects
User Story: US-001
Test Type: Functional
Precondition: 40+ active projects exist
Test Steps:
  1. Navigate to the project dashboard
  2. Scroll/paginate through results
Expected Result: Pagination controls appear; all projects accessible across pages
Priority: Medium
```

```
TC-006: Verify SQL injection on dashboard search/filter fields
User Story: US-001
Test Type: Security
Precondition: Dashboard loaded
Test Steps:
  1. Enter "'; DROP TABLE projects; --" in the search field
  2. Submit the search
Expected Result: Input is sanitized; no SQL execution; error-free results returned
Priority: Critical
```

### US-002: Project CRUD Operations

```
TC-007: Verify project creation with all configurable fields
User Story: US-002
Test Type: Functional
Precondition: Logged in as Administrator
Test Steps:
  1. Click "Create Project"
  2. Fill in name, client, start date, deadline, budget, team, phases
  3. Submit the form
Expected Result: Project is created and appears in the dashboard immediately
Priority: Critical
```

```
TC-008: Verify project edit persists changes
User Story: US-002
Test Type: Functional
Precondition: An existing project
Test Steps:
  1. Open project details
  2. Edit the deadline field
  3. Save changes
Expected Result: Changes are persisted and reflected in the dashboard immediately
Priority: Critical
```

```
TC-009: Verify project archival hides from active view
User Story: US-002
Test Type: Functional
Precondition: A completed project exists
Test Steps:
  1. Click "Archive" on the project
  2. Confirm archival
  3. Check the active dashboard
Expected Result: Project is hidden from active dashboard but accessible via search
Priority: High
```

```
TC-010: Verify archived project retains all historical data
User Story: US-002
Test Type: Functional
Precondition: An archived project with tasks, milestones, and time entries
Test Steps:
  1. Search for the archived project
  2. Open its details
Expected Result: All historical data (tasks, milestones, time entries) is preserved and viewable
Priority: High
```

```
TC-011: Verify XSS prevention in project name field
User Story: US-002
Test Type: Security
Precondition: Logged in as Administrator
Test Steps:
  1. Create a project with name "<script>alert('xss')</script>"
  2. View the project in the dashboard
Expected Result: Script tags are escaped/sanitized; no script execution
Priority: Critical
```

```
TC-012: Verify only Admin can create projects (RBAC)
User Story: US-002
Test Type: Security
Precondition: Logged in as Team Member
Test Steps:
  1. Attempt to access POST /api/projects endpoint
Expected Result: 403 Forbidden response
Priority: Critical
```

### US-003: Task Management with Dependencies

```
TC-013: Verify task creation with assignment and due date
User Story: US-003
Test Type: Functional
Precondition: Within an active project; logged in as PM
Test Steps:
  1. Click "Create Task"
  2. Assign to team member, set due date, add description
  3. Submit
Expected Result: Task is created and visible in task list with all fields populated
Priority: Critical
```

```
TC-014: Verify valid task status transitions only
User Story: US-003
Test Type: Functional
Precondition: A task in "To Do" status
Test Steps:
  1. Move task to "In Progress" — should succeed
  2. Move task directly to "Done" from "To Do" — should fail
Expected Result: Only valid transitions allowed (To Do -> In Progress -> In Review -> Done)
Priority: Critical
```

```
TC-015: Verify dependency warning when moving blocked task
User Story: US-003
Test Type: Functional
Precondition: Task B depends on Task A; Task A is not Done
Test Steps:
  1. Attempt to move Task B to "In Progress"
Expected Result: Dependency warning is shown indicating Task A must be completed first
Priority: High
```

```
TC-016: Verify task list shows status, assignee, due date, dependency indicators
User Story: US-003
Test Type: Functional
Precondition: Project with multiple tasks and dependencies
Test Steps:
  1. View the task list as PM
Expected Result: All tasks display with status, assignee, due date, and dependency icons
Priority: High
```

### US-004: Milestones with Client Approval

```
TC-017: Verify milestone creation with target date and approval flag
User Story: US-004
Test Type: Functional
Precondition: Within an active project; logged in as PM
Test Steps:
  1. Create a milestone with name, target date, deliverables, and "Requires Client Approval" toggled on
  2. Submit
Expected Result: Milestone created with all fields; approval flag is active
Priority: Critical
```

```
TC-018: Verify client notification on milestone completion requiring approval
User Story: US-004
Test Type: Integration
Precondition: Milestone requires client approval; PM marks it complete
Test Steps:
  1. PM marks milestone as complete
  2. Check client user's notifications
Expected Result: Client user receives notification; milestone status shows "Awaiting Approval"
Priority: Critical
```

```
TC-019: Verify client approval updates milestone status with timestamp
User Story: US-004
Test Type: Functional
Precondition: Milestone in "Awaiting Approval" status
Test Steps:
  1. Client user clicks "Approve"
Expected Result: Milestone status changes to "Approved" with approval timestamp recorded
Priority: Critical
```

```
TC-020: Verify milestone timeline displays all statuses
User Story: US-004
Test Type: Functional
Precondition: Milestones in various statuses (pending, awaiting, approved, overdue)
Test Steps:
  1. View project timeline
Expected Result: All milestones display with correct status indicators
Priority: High
```

### US-005: Kanban Board

```
TC-021: Verify Kanban board displays tasks in status columns
User Story: US-005
Test Type: Functional
Precondition: Project with tasks in various statuses
Test Steps:
  1. Toggle to Kanban view
Expected Result: Tasks organized in columns: To Do, In Progress, In Review, Done
Priority: High
```

```
TC-022: Verify drag-and-drop updates task status in real time
User Story: US-005
Test Type: Functional
Precondition: Kanban view open; a task in "To Do"
Test Steps:
  1. Drag task from "To Do" to "In Progress"
Expected Result: Task status updates immediately; reflected for all viewers
Priority: High
```

```
TC-023: Verify Kanban to list view toggle
User Story: US-005
Test Type: Functional
Precondition: Kanban view with tasks
Test Steps:
  1. Toggle to list view
Expected Result: Same tasks displayed in tabular format with sorting and filtering
Priority: Medium
```

```
TC-024: Verify real-time sync of Kanban changes between users
User Story: US-005
Test Type: Integration
Precondition: Two users viewing same Kanban board
Test Steps:
  1. User A moves a task
  2. Observe User B's board
Expected Result: Change reflected on User B's board without page refresh
Priority: High
```

---

## EPIC-002: Client Portal (US-006 to US-010)

### US-006: Client Portal Dashboard

```
TC-025: Verify client sees only their organization's projects
User Story: US-006
Test Type: Security
Precondition: Client User logged in; multiple tenants exist
Test Steps:
  1. Navigate to client dashboard
Expected Result: Only projects belonging to the client's organization are displayed
Priority: Critical
```

```
TC-026: Verify client dashboard shows status, milestones, activity
User Story: US-006
Test Type: Functional
Precondition: Client with active projects
Test Steps:
  1. View client dashboard
Expected Result: Project status, milestones, recent activity, and upcoming deadlines visible
Priority: Critical
```

```
TC-027: Verify cross-tenant access denied
User Story: US-006
Test Type: Security
Precondition: Client User A logged in; knows project ID of Client B
Test Steps:
  1. Attempt to access /api/portal/projects/{clientB_projectId} via URL manipulation
Expected Result: 403 Forbidden — access denied error
Priority: Critical
```

```
TC-028: Verify client portal has distinct UI theme
User Story: US-006
Test Type: Functional
Precondition: Client User logged in
Test Steps:
  1. Compare portal UI with internal application
Expected Result: Client portal has a distinct, client-friendly theme
Priority: Medium
```

### US-007: Deliverable Review and Milestone Approval

```
TC-029: Verify client can view deliverables with download links
User Story: US-007
Test Type: Functional
Precondition: Milestone with attached deliverables
Test Steps:
  1. Navigate to milestone in client portal
Expected Result: Deliverables listed with download links
Priority: Critical
```

```
TC-030: Verify deliverable download works
User Story: US-007
Test Type: Functional
Precondition: Deliverable available for download
Test Steps:
  1. Click "Download" on a deliverable
Expected Result: File downloads successfully with correct content
Priority: Critical
```

```
TC-031: Verify milestone approval by client
User Story: US-007
Test Type: Functional
Precondition: Milestone requiring client approval
Test Steps:
  1. Client clicks "Approve"
Expected Result: Status updates to Approved; team receives notification
Priority: Critical
```

```
TC-032: Verify revision request requires comment
User Story: US-007
Test Type: Functional
Precondition: Milestone requiring approval
Test Steps:
  1. Client clicks "Request Revision" without entering a comment
  2. Attempt to submit
Expected Result: Validation error — comment is required
Priority: High
```

### US-008: Client Messaging

```
TC-033: Verify threaded messaging between client and team
User Story: US-008
Test Type: Functional
Precondition: Client and PM on same project
Test Steps:
  1. Client sends a message
  2. PM views the thread
  3. PM replies
Expected Result: Messages appear in threaded format; both parties see the conversation
Priority: Critical
```

```
TC-034: Verify message notification delivery
User Story: US-008
Test Type: Integration
Precondition: Client sends a message
Test Steps:
  1. Client sends message to project thread
  2. Check team member's notification inbox
Expected Result: Team member receives notification about new message
Priority: High
```

```
TC-035: Verify file attachment in messages
User Story: US-008
Test Type: Functional
Precondition: Messaging thread open
Test Steps:
  1. Attach a file to a message
  2. Send the message
  3. Other party views the thread
Expected Result: File attachment is visible and downloadable in the thread
Priority: High
```

```
TC-036: Verify XSS prevention in message content
User Story: US-008
Test Type: Security
Precondition: Messaging thread open
Test Steps:
  1. Send a message containing "<img src=x onerror=alert('xss')>"
  2. View the message
Expected Result: HTML is sanitized; no script execution
Priority: Critical
```

### US-009: Gantt Timeline

```
TC-037: Verify Gantt chart displays milestones and progress
User Story: US-009
Test Type: Functional
Precondition: Client User with project containing milestones
Test Steps:
  1. Navigate to timeline view
Expected Result: Gantt chart with milestones, phases, and progress indicators
Priority: High
```

```
TC-038: Verify milestone hover tooltip shows details
User Story: US-009
Test Type: Functional
Precondition: Gantt chart displayed
Test Steps:
  1. Hover over a milestone marker
Expected Result: Tooltip shows name, target date, status, and associated deliverables
Priority: Medium
```

```
TC-039: Verify today marker on timeline
User Story: US-009
Test Type: Functional
Precondition: Gantt chart displayed
Test Steps:
  1. View the timeline
Expected Result: A "today" marker shows the current position relative to the schedule
Priority: Medium
```

### US-010: Email Notifications

```
TC-040: Verify email on milestone completion
User Story: US-010
Test Type: Integration
Precondition: Client User with email; milestone is completed
Test Steps:
  1. Complete a milestone for the client's project
  2. Check email delivery
Expected Result: Client receives email notification with milestone details
Priority: High
```

```
TC-041: Verify email notification preference enforcement
User Story: US-010
Test Type: Functional
Precondition: Client User disables milestone notifications in preferences
Test Steps:
  1. Disable milestone notifications
  2. Complete a milestone
Expected Result: No email sent for milestone (other notification types still active)
Priority: High
```

```
TC-042: Verify email deep link redirects to portal with auth
User Story: US-010
Test Type: Integration
Precondition: Email received with a direct link
Test Steps:
  1. Click the link in the email
Expected Result: Redirected to login if not authenticated; then to the relevant page
Priority: Medium
```

---

## EPIC-003: Time Tracking & Invoicing (US-011 to US-015)

### US-011: Time Tracking

```
TC-043: Verify start/stop timer persists across navigation
User Story: US-011
Test Type: Functional
Precondition: Logged in as Team Member
Test Steps:
  1. Start a timer against a task
  2. Navigate to another page
  3. Return to the timer
Expected Result: Timer is still running with accumulated time
Priority: Critical
```

```
TC-044: Verify manual time entry with all required fields
User Story: US-011
Test Type: Functional
Precondition: Logged in as Team Member
Test Steps:
  1. Open manual time entry form
  2. Enter date, hours, project, task, description, mark as billable
  3. Submit
Expected Result: Time entry saved and visible in time log
Priority: Critical
```

```
TC-045: Verify time entry validation — project and task required
User Story: US-011
Test Type: Functional
Precondition: Manual time entry form open
Test Steps:
  1. Leave project and task fields blank
  2. Attempt to submit
Expected Result: Validation error — project and task are required
Priority: High
```

```
TC-046: Verify time log displays all entries with details
User Story: US-011
Test Type: Functional
Precondition: Team Member with time entries
Test Steps:
  1. View time log
Expected Result: All entries shown with project, task, hours, date, and billable status
Priority: High
```

### US-012: Invoice Generation

```
TC-047: Verify draft invoice generation from approved time entries
User Story: US-012
Test Type: Functional
Precondition: Approved time entries exist for a project
Test Steps:
  1. Navigate to invoice generation
  2. Select project and date range
  3. Generate draft invoice
Expected Result: Line items calculated using correct billing rate hierarchy
Priority: Critical
```

```
TC-048: Verify draft invoice adjustment before finalization
User Story: US-012
Test Type: Functional
Precondition: Draft invoice generated
Test Steps:
  1. Adjust a line item amount
  2. Add a discount
  3. Add a manual entry
  4. Save changes
Expected Result: All adjustments reflected in the draft; total recalculated
Priority: Critical
```

```
TC-049: Verify finalized invoice is immutable
User Story: US-012
Test Type: Functional
Precondition: Draft invoice ready
Test Steps:
  1. Finalize the invoice
  2. Attempt to edit a line item
Expected Result: Editing is blocked; invoice has a unique number and is immutable
Priority: Critical
```

```
TC-050: Verify invoice list shows status and totals
User Story: US-012
Test Type: Functional
Precondition: Invoices in various statuses (Draft, Finalized, Sent, Paid)
Test Steps:
  1. View the invoice list
Expected Result: All invoices shown with status and totals
Priority: High
```

### US-013: Billing Rate Configuration

```
TC-051: Verify global billing rates by role
User Story: US-013
Test Type: Functional
Precondition: Logged in as Administrator
Test Steps:
  1. Set global billing rate for "Senior Developer" role
  2. Log time against a project with no overrides
  3. Generate invoice
Expected Result: Global rate applied to the time entry
Priority: Critical
```

```
TC-052: Verify client-level rate overrides global rate
User Story: US-013
Test Type: Functional
Precondition: Global and client-level rates configured
Test Steps:
  1. Set a client-level rate override
  2. Generate invoice for that client
Expected Result: Client rate used instead of global rate
Priority: Critical
```

```
TC-053: Verify project-level rate overrides client and global
User Story: US-013
Test Type: Functional
Precondition: All three rate levels configured
Test Steps:
  1. Set a project-level rate
  2. Generate invoice
Expected Result: Project rate takes precedence (project > client > global)
Priority: Critical
```

### US-014: Time Entry Approval

```
TC-054: Verify submitted entries appear in approver's queue
User Story: US-014
Test Type: Functional
Precondition: Team Member submits time entries
Test Steps:
  1. Team Member submits time entries
  2. Team Lead views approval queue
Expected Result: Entries appear in the approval queue
Priority: High
```

```
TC-055: Verify approval marks entry as eligible for invoicing
User Story: US-014
Test Type: Functional
Precondition: Time entry in approval queue
Test Steps:
  1. Team Lead approves the entry
Expected Result: Entry marked as approved; eligible for invoice generation
Priority: High
```

```
TC-056: Verify rejection requires reason and notifies Team Member
User Story: US-014
Test Type: Functional
Precondition: Time entry in approval queue
Test Steps:
  1. Team Lead clicks "Reject"
  2. Enter rejection reason
  3. Submit
Expected Result: Entry rejected; Team Member notified with the reason
Priority: High
```

```
TC-057: Verify reject-resubmit cycle
User Story: US-014
Test Type: Functional
Precondition: A rejected time entry
Test Steps:
  1. Team Member modifies the entry
  2. Resubmits
  3. Team Lead checks queue
Expected Result: Modified entry reappears in approval queue
Priority: Medium
```

### US-015: Timesheets

```
TC-058: Verify weekly timesheet grid with daily project breakdown
User Story: US-015
Test Type: Functional
Precondition: Team Member with time entries across the week
Test Steps:
  1. View weekly timesheet
Expected Result: Grid displays daily hours broken down by project
Priority: High
```

```
TC-059: Verify team lead can view team timesheets
User Story: US-015
Test Type: Functional
Precondition: Team Lead with team members who have time entries
Test Steps:
  1. View team timesheets
Expected Result: Each member's weekly/monthly summary visible
Priority: High
```

```
TC-060: Verify monthly view with billable vs non-billable breakdown
User Story: US-015
Test Type: Functional
Precondition: Time entries with both billable and non-billable hours
Test Steps:
  1. Toggle to monthly view
Expected Result: Monthly summary with billable/non-billable breakdown and utilization %
Priority: High
```

```
TC-061: Verify timesheet export as CSV and PDF
User Story: US-015
Test Type: Functional
Precondition: Timesheet with data
Test Steps:
  1. Click export -> CSV
  2. Click export -> PDF
Expected Result: Both exports download with correct data
Priority: Medium
```

---

## EPIC-004: Resource Management (US-016 to US-018)

### US-016: Resource Allocation Board

```
TC-062: Verify resource board shows all team members with utilization
User Story: US-016
Test Type: Functional
Precondition: Logged in as PM; team members have assignments
Test Steps:
  1. Open resource allocation board
Expected Result: All team members shown with assigned projects and utilization percentage
Priority: High
```

```
TC-063: Verify overallocated team member is highlighted
User Story: US-016
Test Type: Functional
Precondition: Team member assigned over 100% capacity
Test Steps:
  1. View resource board
Expected Result: Over-100% members are visually highlighted as overallocated
Priority: High
```

```
TC-064: Verify resource board filters by team/department
User Story: US-016
Test Type: Functional
Precondition: Multiple teams/departments exist
Test Steps:
  1. Apply team filter
Expected Result: Only matching team members displayed
Priority: Medium
```

### US-017: Resource Assignment with Conflict Detection

```
TC-065: Verify drag-and-drop assignment creates assignment and updates utilization
User Story: US-017
Test Type: Functional
Precondition: Resource board open; team member under capacity
Test Steps:
  1. Drag team member to a project
Expected Result: Assignment created; utilization updates
Priority: High
```

```
TC-066: Verify overallocation warning on assignment
User Story: US-017
Test Type: Functional
Precondition: Team member at 90% utilization
Test Steps:
  1. Assign member to another project pushing them over 100%
Expected Result: Warning displayed about overallocation
Priority: High
```

```
TC-067: Verify proceed with overallocation saves with flag
User Story: US-017
Test Type: Functional
Precondition: Overallocation warning displayed
Test Steps:
  1. Click "Proceed Anyway"
Expected Result: Assignment saved with overallocation flag
Priority: Medium
```

```
TC-068: Verify reassignment updates both projects
User Story: US-017
Test Type: Functional
Precondition: Member assigned to Project A
Test Steps:
  1. Move member from Project A to Project B
Expected Result: Both projects' resource allocations update correctly
Priority: High
```

### US-018: Capacity Forecasting

```
TC-069: Verify capacity forecast shows 4-12 week projection
User Story: US-018
Test Type: Functional
Precondition: Team members with scheduled assignments
Test Steps:
  1. Open capacity forecast
Expected Result: Projected utilization per team member for next 4-12 weeks
Priority: Medium
```

```
TC-070: Verify time window slider adjusts forecast period
User Story: US-018
Test Type: Functional
Precondition: Capacity forecast open
Test Steps:
  1. Adjust time window slider from 4 weeks to 12 weeks
Expected Result: View updates to show the selected period
Priority: Medium
```

```
TC-071: Verify forecast filters by team, skill, department
User Story: US-018
Test Type: Functional
Precondition: Multiple teams exist
Test Steps:
  1. Apply skill filter "React Developer"
Expected Result: Only matching members shown in forecast
Priority: Medium
```

---

## EPIC-005: Document Management (US-019 to US-022)

### US-019: Document Upload/Download/Preview

```
TC-072: Verify document upload with progress indicator
User Story: US-019
Test Type: Functional
Precondition: Within a project; logged in with upload permissions
Test Steps:
  1. Select a file and target folder
  2. Click upload
Expected Result: File uploads with progress indicator; appears in folder listing
Priority: High
```

```
TC-073: Verify in-browser preview for PDF and images
User Story: US-019
Test Type: Functional
Precondition: PDF and image files uploaded
Test Steps:
  1. Click preview on a PDF
  2. Click preview on an image
Expected Result: Both render in-browser without download
Priority: High
```

```
TC-074: Verify document deletion with confirmation dialog
User Story: US-019
Test Type: Functional
Precondition: User with delete permissions; document exists
Test Steps:
  1. Click delete on a document
  2. Confirm in the dialog
Expected Result: Document removed from folder listing
Priority: Medium
```

```
TC-075: Verify upload permission enforcement
User Story: US-019
Test Type: Security
Precondition: Client User attempts upload to internal project folder
Test Steps:
  1. Client User attempts POST /api/documents/upload for a non-authorized project
Expected Result: 403 Forbidden
Priority: Critical
```

```
TC-076: Verify malicious file upload prevention
User Story: US-019
Test Type: Security
Precondition: Upload form open
Test Steps:
  1. Attempt to upload a .exe file renamed to .pdf
Expected Result: File type validation rejects the upload; or file is scanned and flagged
Priority: Critical
```

### US-020: Document Version History

```
TC-077: Verify re-upload creates new version automatically
User Story: US-020
Test Type: Functional
Precondition: Document already uploaded
Test Steps:
  1. Upload a new version of the same document
Expected Result: New version created; previous version preserved
Priority: High
```

```
TC-078: Verify version history list with timestamps and uploaders
User Story: US-020
Test Type: Functional
Precondition: Document with multiple versions
Test Steps:
  1. View version history
Expected Result: List of all versions with timestamps and uploader names
Priority: High
```

```
TC-079: Verify restore previous version
User Story: US-020
Test Type: Functional
Precondition: Document with multiple versions
Test Steps:
  1. Click "Restore" on a previous version
Expected Result: Previous version becomes the current version
Priority: High
```

### US-021: Document Commenting

```
TC-080: Verify adding a comment on a document
User Story: US-021
Test Type: Functional
Precondition: Document viewable by user
Test Steps:
  1. Add a comment
  2. Submit
Expected Result: Comment saved and visible to other users with permissions
Priority: High
```

```
TC-081: Verify threaded replies on comments
User Story: US-021
Test Type: Functional
Precondition: A comment exists on a document
Test Steps:
  1. Click "Reply" on the comment
  2. Enter reply text
  3. Submit
Expected Result: Threaded reply appears under the original comment
Priority: High
```

```
TC-082: Verify comment notification to watchers
User Story: US-021
Test Type: Integration
Precondition: User watching a document; another user comments
Test Steps:
  1. User B adds a comment
  2. Check User A's notifications
Expected Result: User A receives notification about new comment
Priority: Medium
```

### US-022: Deliverable Approval Workflow

```
TC-083: Verify submit for review triggers client notification
User Story: US-022
Test Type: Integration
Precondition: PM marks deliverable as "Submitted for Review"
Test Steps:
  1. PM submits deliverable for review
  2. Check client notifications
Expected Result: Client receives notification about pending review
Priority: Critical
```

```
TC-084: Verify client approval updates status with timestamp
User Story: US-022
Test Type: Functional
Precondition: Deliverable in "Submitted" status
Test Steps:
  1. Client clicks "Approve"
Expected Result: Status changes to "Approved" with timestamp
Priority: Critical
```

```
TC-085: Verify rejection requires comment
User Story: US-022
Test Type: Functional
Precondition: Deliverable submitted for review
Test Steps:
  1. Client clicks "Reject" without entering comment
Expected Result: Validation error — comment required for rejection
Priority: High
```

```
TC-086: Verify deliverable status list (Draft, Submitted, Approved, Rejected, Changes Requested)
User Story: US-022
Test Type: Functional
Precondition: Deliverables in various statuses
Test Steps:
  1. View deliverables list
Expected Result: Current status visible for each deliverable
Priority: Medium
```

---

## EPIC-006: Integrations (US-023 to US-028)

### US-023: QuickBooks Invoice Sync

```
TC-087: Verify finalized invoice push to QuickBooks
User Story: US-023
Test Type: Integration
Precondition: QuickBooks sandbox connected; finalized invoice exists
Test Steps:
  1. Trigger sync
  2. Check QuickBooks sandbox
Expected Result: Invoice with line items and client details appears in QuickBooks
Priority: High
```

```
TC-088: Verify payment status sync from QuickBooks
User Story: US-023
Test Type: Integration
Precondition: Invoice in QuickBooks marked as Paid
Test Steps:
  1. Trigger bi-directional sync
Expected Result: Payment status reflected in the platform
Priority: High
```

```
TC-089: Verify sync error logging and visibility
User Story: US-023
Test Type: Functional
Precondition: Force a sync error (e.g., invalid QuickBooks field mapping)
Test Steps:
  1. Trigger sync with misconfigured mapping
  2. Check sync status dashboard
Expected Result: Error visible in sync log with details
Priority: High
```

### US-024: Slack Notifications

```
TC-090: Verify Slack notification on configured event
User Story: US-024
Test Type: Integration
Precondition: Slack integration configured; event-to-channel mapping set
Test Steps:
  1. Trigger a configured event (e.g., task assignment)
  2. Check Slack channel
Expected Result: Notification sent to specified channel with direct link
Priority: High
```

```
TC-091: Verify Slack notification contains platform deep link
User Story: US-024
Test Type: Integration
Precondition: Slack notification received
Test Steps:
  1. Click the link in the Slack message
Expected Result: Opens the relevant item in the platform
Priority: Medium
```

```
TC-092: Verify Slack notification retry on temporary failure
User Story: US-024
Test Type: Integration
Precondition: Slack temporarily unavailable
Test Steps:
  1. Trigger an event while Slack is down
  2. Restore Slack connectivity
Expected Result: Queued notifications are retried and delivered
Priority: Medium
```

### US-025: Google Calendar Sync

```
TC-093: Verify milestone date creates calendar event
User Story: US-025
Test Type: Integration
Precondition: Google Calendar connected; milestone date set
Test Steps:
  1. Create a milestone with a date
Expected Result: Calendar event created automatically
Priority: Medium
```

```
TC-094: Verify milestone date change updates calendar event
User Story: US-025
Test Type: Integration
Precondition: Existing milestone with synced calendar event
Test Steps:
  1. Change milestone date in platform
  2. Check Google Calendar
Expected Result: Calendar event updated to new date
Priority: Medium
```

### US-026: Figma Integration

```
TC-095: Verify Figma URL validation and thumbnail display
User Story: US-026
Test Type: Functional
Precondition: Within a project's documents section
Test Steps:
  1. Paste a valid Figma URL
  2. Submit
Expected Result: URL saved; thumbnail preview displayed
Priority: Low
```

```
TC-096: Verify invalid Figma URL validation
User Story: US-026
Test Type: Functional
Precondition: Document section open
Test Steps:
  1. Paste "https://notigma.com/invalid"
  2. Submit
Expected Result: Validation error — invalid Figma URL
Priority: Low
```

### US-027: GitHub Integration

```
TC-097: Verify GitHub widget shows commits, branches, PR status
User Story: US-027
Test Type: Integration
Precondition: GitHub repo linked to project
Test Steps:
  1. View project dashboard
Expected Result: Recent commits, active branches, and PR status displayed
Priority: Low
```

```
TC-098: Verify GitHub widget refresh at configurable intervals
User Story: US-027
Test Type: Integration
Precondition: GitHub widget displayed; new commit pushed
Test Steps:
  1. Wait for configured refresh interval
Expected Result: New commit appears in the widget
Priority: Low
```

### US-028: QuickBooks Configuration

```
TC-099: Verify QuickBooks OAuth connection flow
User Story: US-028
Test Type: Integration
Precondition: Administrator on QuickBooks settings page
Test Steps:
  1. Click "Connect to QuickBooks"
  2. Complete OAuth flow
Expected Result: QuickBooks connected; status shows "Connected"
Priority: High
```

```
TC-100: Verify account mapping persistence
User Story: US-028
Test Type: Functional
Precondition: QuickBooks connected
Test Steps:
  1. Map internal invoice fields to QuickBooks accounts
  2. Save configuration
  3. Reopen settings
Expected Result: Mapped accounts persist correctly
Priority: High
```

```
TC-101: Verify sync schedule configuration and execution
User Story: US-028
Test Type: Integration
Precondition: Account mapping complete
Test Steps:
  1. Set sync schedule to "Every 6 hours"
  2. Wait for scheduled run (or trigger manually)
Expected Result: Sync executes at configured interval; log entry created
Priority: Medium
```

---

## EPIC-007: Reporting & Analytics (US-029 to US-034)

### US-029: Executive Dashboard

```
TC-102: Verify all five KPIs display on executive dashboard
User Story: US-029
Test Type: Functional
Precondition: Logged in as Executive; data exists for all KPIs
Test Steps:
  1. Open executive dashboard
Expected Result: Revenue/client, profitability, utilization, on-time delivery, NPS all displayed
Priority: Critical
```

```
TC-103: Verify KPI drill-down functionality
User Story: US-029
Test Type: Functional
Precondition: Executive dashboard loaded
Test Steps:
  1. Click on "Project Profitability" KPI
Expected Result: Drill-down view shows profitability per project
Priority: High
```

```
TC-104: Verify dashboard loads within 5 seconds (NFR-002)
User Story: US-029
Test Type: Performance
Precondition: 40+ active projects with comprehensive data
Test Steps:
  1. Navigate to executive dashboard
  2. Measure load time
Expected Result: Dashboard loads within 5 seconds at p95
Priority: High
```

### US-030: Profitability Reports

```
TC-105: Verify profitability report shows budget vs actual
User Story: US-030
Test Type: Functional
Precondition: Project with budgeted and actual hours
Test Steps:
  1. Generate profitability report for a project
Expected Result: Budget vs actual hours and cost displayed with variance
Priority: Critical
```

```
TC-106: Verify variance threshold highlighting
User Story: US-030
Test Type: Functional
Precondition: Project with variance exceeding threshold
Test Steps:
  1. View profitability report
Expected Result: Over-budget items highlighted in red/amber
Priority: High
```

```
TC-107: Verify report filtering by date range, client, project
User Story: US-030
Test Type: Functional
Precondition: Report generated
Test Steps:
  1. Apply date range filter
  2. Apply client filter
Expected Result: Report updates to reflect filters
Priority: High
```

```
TC-108: Verify report export in PDF, CSV, and Excel
User Story: US-030
Test Type: Functional
Precondition: Report generated
Test Steps:
  1. Export as PDF
  2. Export as CSV
  3. Export as Excel
Expected Result: All three formats download with correct data
Priority: High
```

### US-031: Report Export and Scheduling

```
TC-109: Verify report export format selection
User Story: US-031
Test Type: Functional
Precondition: Report generated
Test Steps:
  1. Click export
  2. Choose PDF format
Expected Result: PDF file downloads with report data
Priority: High
```

```
TC-110: Verify scheduled report email delivery
User Story: US-031
Test Type: Integration
Precondition: Report schedule configured (weekly)
Test Steps:
  1. Configure weekly schedule with recipient email
  2. Trigger schedule (or wait for schedule)
Expected Result: Recipient receives email with report attached
Priority: High
```

```
TC-111: Verify scheduled report list shows active schedules
User Story: US-031
Test Type: Functional
Precondition: Multiple report schedules configured
Test Steps:
  1. View scheduled reports
Expected Result: All active schedules shown with last run and next run times
Priority: Medium
```

### US-032: NPS Tracking

```
TC-112: Verify NPS score recording with timestamp
User Story: US-032
Test Type: Functional
Precondition: Logged in as PM
Test Steps:
  1. Record NPS score for a project
Expected Result: Score saved with timestamp
Priority: Medium
```

```
TC-113: Verify NPS trend chart
User Story: US-032
Test Type: Functional
Precondition: Multiple NPS scores recorded over time
Test Steps:
  1. View NPS dashboard
Expected Result: Trend chart shows score changes over time per client and project
Priority: Medium
```

```
TC-114: Verify NPS on executive dashboard
User Story: US-032
Test Type: Functional
Precondition: NPS scores exist
Test Steps:
  1. View executive dashboard
Expected Result: Average NPS appears as a KPI widget
Priority: Medium
```

### US-033: AI-Powered Estimation (Phase 2 Stub)

```
TC-115: Verify Phase 2 placeholder UI for AI estimation
User Story: US-033
Test Type: Functional
Precondition: Logged in as PM
Test Steps:
  1. Navigate to estimation feature
Expected Result: "Coming in Phase 2" placeholder with data collection confirmation
Priority: Low
```

```
TC-116: Verify historical data collection hooks are active
User Story: US-033
Test Type: Functional
Precondition: System deployed
Test Steps:
  1. Create and complete a project
  2. Verify data collection hook fires
Expected Result: Historical data captured for future model training
Priority: Low
```

### US-034: Advanced Analytics (Phase 2 Stub)

```
TC-117: Verify Phase 2 placeholder UI for advanced analytics
User Story: US-034
Test Type: Functional
Precondition: Logged in as Executive
Test Steps:
  1. Navigate to advanced analytics
Expected Result: "Coming in Phase 2" placeholder with data pipeline info
Priority: Low
```

```
TC-118: Verify data pipeline foundations are capturing metrics
User Story: US-034
Test Type: Functional
Precondition: System operational with data
Test Steps:
  1. Verify metrics are being stored by the pipeline
Expected Result: Data pipeline stores metrics for future analytics
Priority: Low
```

---

## EPIC-008: Security & Access Control (US-035 to US-041)

### US-035: Role-Based Access Control

```
TC-119: Verify 7 predefined roles exist with correct permissions
User Story: US-035
Test Type: Security
Precondition: System deployed with seed data
Test Steps:
  1. Query role configuration
Expected Result: Admin, Executive, PM, Team Lead, Team Member, Finance Manager, Client User roles exist with distinct permissions
Priority: Critical
```

```
TC-120: Verify role assignment restricts actions
User Story: US-035
Test Type: Security
Precondition: User with Team Member role
Test Steps:
  1. Attempt to create a project (POST /api/projects)
Expected Result: 403 Forbidden — only Admin and PM can create projects
Priority: Critical
```

```
TC-121: Verify Client User can only access own organization
User Story: US-035
Test Type: Security
Precondition: Client User logged in
Test Steps:
  1. Access own project — should succeed
  2. Access another org's project — should fail
Expected Result: Own project: 200; other org: 403
Priority: Critical
```

```
TC-122: Verify permission matrix display in admin panel
User Story: US-035
Test Type: Functional
Precondition: Logged in as Administrator
Test Steps:
  1. Navigate to role management
Expected Result: All roles and their permissions displayed clearly
Priority: Medium
```

```
TC-123: Verify RBAC enforcement on every API endpoint
User Story: US-035
Test Type: Security
Precondition: Test user for each role
Test Steps:
  1. For each API endpoint, test access with each of the 7 roles
Expected Result: Each endpoint returns 200 only for allowed roles; 403 for others
Priority: Critical
```

### US-036: Two-Factor Authentication

```
TC-124: Verify mandatory 2FA setup on first login
User Story: US-036
Test Type: Functional
Precondition: New user account created
Test Steps:
  1. Log in for the first time
Expected Result: Redirected to 2FA setup before accessing any platform features
Priority: Critical
```

```
TC-125: Verify TOTP QR code generation and verification
User Story: US-036
Test Type: Functional
Precondition: User on 2FA setup page
Test Steps:
  1. Scan QR code with authenticator app
  2. Enter the generated code
  3. Submit
Expected Result: 2FA enabled; user can proceed to platform
Priority: Critical
```

```
TC-126: Verify login requires both password and 2FA code
User Story: US-036
Test Type: Functional
Precondition: User with 2FA enabled
Test Steps:
  1. Log in with correct password
  2. Enter correct 2FA code
Expected Result: Login successful only after both factors verified
Priority: Critical
```

```
TC-127: Verify login fails with incorrect 2FA code
User Story: US-036
Test Type: Security
Precondition: User with 2FA enabled
Test Steps:
  1. Log in with correct password
  2. Enter incorrect 2FA code
Expected Result: Authentication fails; access denied
Priority: Critical
```

```
TC-128: Verify admin can reset user's 2FA
User Story: US-036
Test Type: Functional
Precondition: Logged in as Admin; user locked out of 2FA
Test Steps:
  1. Navigate to user management
  2. Click "Reset 2FA" for the user
Expected Result: User's 2FA is reset; they must re-enroll on next login
Priority: High
```

```
TC-129: Verify expired TOTP code is rejected
User Story: US-036
Test Type: Security
Precondition: Valid TOTP code that has expired (30s window passed)
Test Steps:
  1. Enter an expired TOTP code
Expected Result: Code rejected; user prompted to enter a new code
Priority: High
```

### US-037: Audit Trails

```
TC-130: Verify audit log creation on data modification
User Story: US-037
Test Type: Security
Precondition: Any user performs a data modification
Test Steps:
  1. Create/update/delete a resource
  2. Check audit logs
Expected Result: Immutable log entry with timestamp, user ID, action type, and before/after values
Priority: Critical
```

```
TC-131: Verify audit log search by user, date, action type
User Story: US-037
Test Type: Functional
Precondition: Audit logs exist; logged in as Administrator
Test Steps:
  1. Search audit logs with filters
Expected Result: Filtered results match criteria accurately
Priority: High
```

```
TC-132: Verify audit log export as CSV
User Story: US-037
Test Type: Functional
Precondition: Audit logs exist
Test Steps:
  1. Export audit logs
Expected Result: CSV file downloads with complete log data
Priority: High
```

```
TC-133: Verify audit log immutability
User Story: US-037
Test Type: Security
Precondition: Audit logs exist
Test Steps:
  1. Attempt to modify an audit log entry via direct DB access
Expected Result: Modification blocked; alert triggered
Priority: Critical
```

```
TC-134: Verify login/logout events are audited
User Story: US-037
Test Type: Security
Precondition: User logs in and out
Test Steps:
  1. Log in
  2. Log out
  3. Check audit logs
Expected Result: Both login and logout events recorded with timestamps
Priority: High
```

### US-038: Client Data Isolation

```
TC-135: Verify tenant-filtered queries on all client data endpoints
User Story: US-038
Test Type: Security
Precondition: Two tenants (Tenant A, Tenant B) with data
Test Steps:
  1. Log in as Tenant A client
  2. Query projects, documents, tasks
Expected Result: Zero records from Tenant B appear in any response
Priority: Critical
```

```
TC-136: Verify URL manipulation cannot access cross-tenant data
User Story: US-038
Test Type: Security
Precondition: Client User A logged in; knows Tenant B resource IDs
Test Steps:
  1. Manually construct URL with Tenant B resource ID
  2. Send request
Expected Result: 403 Forbidden — access denied
Priority: Critical
```

```
TC-137: Verify cross-tenant penetration test
User Story: US-038
Test Type: Security
Precondition: Two fully populated tenants
Test Steps:
  1. Run automated cross-tenant access tests against all data endpoints
Expected Result: Zero cross-tenant data access found
Priority: Critical
```

### US-039: SSO with Google Workspace

```
TC-138: Verify Google SSO authentication flow
User Story: US-039
Test Type: Integration
Precondition: Google Workspace SSO configured
Test Steps:
  1. Click "Sign in with Google"
  2. Complete Google authentication
Expected Result: Authenticated and redirected to the platform
Priority: High
```

```
TC-139: Verify first-time SSO user provisioning
User Story: US-039
Test Type: Functional
Precondition: New user logs in via SSO
Test Steps:
  1. Sign in with Google for the first time
Expected Result: Account provisioned with appropriate role
Priority: High
```

```
TC-140: Verify fallback to email/password when SSO unavailable
User Story: US-039
Test Type: Functional
Precondition: Google Workspace down or SSO disabled
Test Steps:
  1. Attempt SSO — should fail gracefully
  2. Log in with email/password
Expected Result: Email/password login works; graceful SSO error message
Priority: High
```

### US-040: Password Policies

```
TC-141: Verify minimum 12 characters password requirement
User Story: US-040
Test Type: Security
Precondition: Password creation/change form
Test Steps:
  1. Enter a 10-character password
  2. Submit
Expected Result: Validation error — minimum 12 characters required
Priority: High
```

```
TC-142: Verify complexity requirements (uppercase, lowercase, number, special)
User Story: US-040
Test Type: Security
Precondition: Password change form
Test Steps:
  1. Enter "abcdefghijkl" (no uppercase/number/special)
Expected Result: Validation error — complexity requirements not met
Priority: High
```

```
TC-143: Verify 90-day password expiry prompt
User Story: US-040
Test Type: Security
Precondition: User with password set 90 days ago
Test Steps:
  1. Log in
Expected Result: Prompted to change password before proceeding
Priority: High
```

```
TC-144: Verify password reuse prevention (last 10)
User Story: US-040
Test Type: Security
Precondition: User with password history
Test Steps:
  1. Change password to one of the last 10 used passwords
Expected Result: Rejected — cannot reuse recent passwords
Priority: High
```

```
TC-145: Verify password expiry warning 14 days before
User Story: US-040
Test Type: Functional
Precondition: Password expires in 14 days
Test Steps:
  1. Log in
Expected Result: Warning notification about upcoming password expiry
Priority: Medium
```

### US-041: Session Timeout

```
TC-146: Verify warning modal at 25 minutes of inactivity
User Story: US-041
Test Type: Functional
Precondition: User logged in; inactive for 25 minutes
Test Steps:
  1. Wait 25 minutes without activity
Expected Result: Warning modal appears with countdown timer
Priority: High
```

```
TC-147: Verify session extension on "Continue Session"
User Story: US-041
Test Type: Functional
Precondition: Warning modal displayed
Test Steps:
  1. Click "Continue Session"
Expected Result: Session timer resets to 30 minutes; modal closes
Priority: High
```

```
TC-148: Verify automatic logout at 30 minutes of inactivity
User Story: US-041
Test Type: Functional
Precondition: Warning modal displayed; user does not respond
Test Steps:
  1. Wait 5 more minutes (total 30 minutes)
Expected Result: Logged out; redirected to login page
Priority: High
```

```
TC-149: Verify timeout message on re-login
User Story: US-041
Test Type: Functional
Precondition: User logged out due to timeout
Test Steps:
  1. Log back in
Expected Result: Message explaining session expired due to inactivity
Priority: Medium
```

---

## EPIC-009: Platform & UX (US-042 to US-045)

### US-042: Responsive Web Application

```
TC-150: Verify full functionality at 1920px desktop viewport
User Story: US-042
Test Type: Functional
Precondition: Application loaded in Chrome at 1920px
Test Steps:
  1. Navigate through all major features
Expected Result: All features fully functional with optimal layout
Priority: High
```

```
TC-151: Verify critical workflows at 768px tablet viewport
User Story: US-042
Test Type: Functional
Precondition: Application at 768px viewport
Test Steps:
  1. Navigate through critical workflows (project view, time tracking, client portal)
Expected Result: All critical workflows usable without horizontal scrolling
Priority: High
```

```
TC-152: Verify cross-browser consistency (Chrome, Firefox, Safari, Edge)
User Story: US-042
Test Type: Functional
Precondition: Application loaded in each browser
Test Steps:
  1. Execute critical workflows in each browser
Expected Result: Behavior and layout consistent across all browsers
Priority: High
```

```
TC-153: Verify smooth layout adaptation between breakpoints
User Story: US-042
Test Type: Functional
Precondition: Browser window open
Test Steps:
  1. Gradually resize browser from 1920px to 768px
Expected Result: Layout adapts smoothly between breakpoints
Priority: Medium
```

### US-043: Global Search

```
TC-154: Verify search autocomplete across all entity types
User Story: US-043
Test Type: Functional
Precondition: Projects, tasks, documents, and clients exist
Test Steps:
  1. Type in global search bar
Expected Result: Autocomplete suggestions from projects, tasks, documents, and clients
Priority: Medium
```

```
TC-155: Verify search results categorized by type
User Story: US-043
Test Type: Functional
Precondition: Search submitted
Test Steps:
  1. Submit a search query matching multiple entity types
Expected Result: Results categorized as project, task, document, client
Priority: Medium
```

```
TC-156: Verify RBAC filtering on search results
User Story: US-043
Test Type: Security
Precondition: Team Member searches; some results are restricted
Test Steps:
  1. Search for a term matching resources the user cannot access
Expected Result: Only accessible results shown; restricted items excluded
Priority: Critical
```

```
TC-157: Verify search performance within 2 seconds
User Story: US-043
Test Type: Performance
Precondition: Full dataset loaded
Test Steps:
  1. Submit search query
  2. Measure response time
Expected Result: Results display within 2 seconds
Priority: Medium
```

### US-044: In-App Notification Center

```
TC-158: Verify notification badge with unread count
User Story: US-044
Test Type: Functional
Precondition: User has unread notifications
Test Steps:
  1. Observe the notification bell icon
Expected Result: Badge shows correct unread count
Priority: Medium
```

```
TC-159: Verify notification panel shows categorized notifications
User Story: US-044
Test Type: Functional
Precondition: Multiple notification types exist
Test Steps:
  1. Click the notification bell
Expected Result: Panel shows notifications categorized and sorted by recency
Priority: Medium
```

```
TC-160: Verify mark-as-read decreases unread count
User Story: US-044
Test Type: Functional
Precondition: Unread notifications exist
Test Steps:
  1. Mark a notification as read
Expected Result: Unread count decreases by 1
Priority: Medium
```

```
TC-161: Verify notification preference configuration
User Story: US-044
Test Type: Functional
Precondition: Notification preferences open
Test Steps:
  1. Disable "Task Assignment" notifications
  2. Assign a task to the user
Expected Result: No notification received for the task assignment
Priority: Medium
```

### US-045: Mobile App Stub (Phase 2)

```
TC-162: Verify mobile-optimized API endpoints return correct data
User Story: US-045
Test Type: Integration
Precondition: Mobile API endpoints deployed
Test Steps:
  1. Call mobile time tracking API endpoint
Expected Result: Correct data with minimal payload size
Priority: Low
```

```
TC-163: Verify responsive web time tracking at mobile viewport
User Story: US-045
Test Type: Functional
Precondition: Application at 375px viewport
Test Steps:
  1. Use time tracking features
Expected Result: Time tracking usable at mobile viewport widths
Priority: Low
```

---

## EPIC-010: Administration (US-046 to US-047)

### US-046: Admin Panel

```
TC-164: Verify admin panel shows all sections
User Story: US-046
Test Type: Functional
Precondition: Logged in as Administrator
Test Steps:
  1. Navigate to admin panel
Expected Result: Sections visible: Users, Roles, Integrations, Billing, Settings
Priority: Critical
```

```
TC-165: Verify user creation, editing, and deactivation
User Story: US-046
Test Type: Functional
Precondition: Admin panel open
Test Steps:
  1. Create a new user
  2. Edit the user's role
  3. Deactivate the user
Expected Result: All changes take effect immediately
Priority: Critical
```

```
TC-166: Verify permission matrix view and modification
User Story: US-046
Test Type: Functional
Precondition: Role management section
Test Steps:
  1. View permission matrix
  2. Modify a permission for a role
Expected Result: Permissions visible and modifiable per role
Priority: High
```

```
TC-167: Verify integration configuration persistence
User Story: US-046
Test Type: Functional
Precondition: Admin configures QuickBooks settings
Test Steps:
  1. Update integration settings
  2. Navigate away and return
Expected Result: Configuration saved and applied
Priority: High
```

```
TC-168: Verify non-admin cannot access admin panel
User Story: US-046
Test Type: Security
Precondition: Logged in as Team Member
Test Steps:
  1. Navigate to /admin
Expected Result: 403 Forbidden — redirected away from admin panel
Priority: Critical
```

### US-047: User Invitation

```
TC-169: Verify invitation email with predefined role
User Story: US-047
Test Type: Integration
Precondition: Admin on user invitation form
Test Steps:
  1. Enter invitee email
  2. Select role "Team Member"
  3. Send invitation
Expected Result: Email sent to invitee with setup link; role pre-assigned
Priority: High
```

```
TC-170: Verify invitee account setup and 2FA enrollment
User Story: US-047
Test Type: Functional
Precondition: Invitee clicks the email link
Test Steps:
  1. Click invitation link
  2. Set up password
  3. Set up 2FA
Expected Result: Account created with pre-assigned role; 2FA enabled
Priority: High
```

```
TC-171: Verify invitation expiry
User Story: US-047
Test Type: Functional
Precondition: Invitation sent; configurable expiry period passes
Test Steps:
  1. Click expired invitation link
Expected Result: Link invalid; error message shown
Priority: Medium
```

```
TC-172: Verify invitation list shows status (Pending, Accepted, Expired)
User Story: US-047
Test Type: Functional
Precondition: Invitations in various statuses
Test Steps:
  1. View invitation list in admin panel
Expected Result: Each invitation shows correct status
Priority: Medium
```

---

## Domain-Specific Stories (US-049 to US-056)

### US-048: Data Migration

```
TC-173: Verify CSV/Excel upload in import wizard
User Story: US-048
Test Type: Functional
Precondition: Admin on import wizard
Test Steps:
  1. Upload a CSV file for projects
Expected Result: File accepted; parsing begins
Priority: High
```

```
TC-174: Verify validation report shows valid records, warnings, errors
User Story: US-048
Test Type: Functional
Precondition: File uploaded with mixed data quality
Test Steps:
  1. Upload file with some invalid rows
Expected Result: Validation report shows counts for valid, warning, and error records
Priority: High
```

```
TC-175: Verify dry-run mode shows preview without importing
User Story: US-048
Test Type: Functional
Precondition: Validation passed
Test Steps:
  1. Click "Dry Run"
Expected Result: Preview of data as it would appear; no records imported
Priority: High
```

```
TC-176: Verify import runs transactionally with progress indicator
User Story: US-048
Test Type: Functional
Precondition: Dry run successful
Test Steps:
  1. Click "Import"
Expected Result: Records imported transactionally; progress indicator shown; summary at end
Priority: High
```

```
TC-177: Verify import with large dataset (10,000+ rows)
User Story: US-048
Test Type: Performance
Precondition: Large CSV file prepared
Test Steps:
  1. Upload and import 10,000+ rows
Expected Result: Import completes without timeout or data loss
Priority: High
```

```
TC-178: Verify SQL injection in CSV data fields
User Story: US-048
Test Type: Security
Precondition: CSV with SQL injection strings in data fields
Test Steps:
  1. Upload CSV containing "'; DROP TABLE projects; --" in a field
  2. Import
Expected Result: Data imported safely; no SQL execution; strings stored as literal text
Priority: Critical
```

### US-049: Multi-Tenancy Data Isolation

```
TC-179: Verify tenant_id foreign key on all client-scoped tables
User Story: US-049
Test Type: Security
Precondition: Database schema deployed
Test Steps:
  1. Inspect schema for all client-data tables
Expected Result: Every table with client data includes a tenant_id column
Priority: Critical
```

```
TC-180: Verify tenant_id filter applied at query layer
User Story: US-049
Test Type: Security
Precondition: Two tenants with data
Test Steps:
  1. Execute API calls as Tenant A
  2. Inspect SQL queries (via logging)
Expected Result: All queries include tenant_id filter
Priority: Critical
```

```
TC-181: Verify zero cross-tenant data leakage
User Story: US-049
Test Type: Security
Precondition: Both tenants fully populated
Test Steps:
  1. As Tenant A, query all data endpoints
  2. Verify no Tenant B data appears
Expected Result: Zero cross-tenant records in any response
Priority: Critical
```

```
TC-182: Verify no raw SQL bypasses tenant isolation
User Story: US-049
Test Type: Security
Precondition: Code review complete
Test Steps:
  1. Audit all data access code for raw SQL without tenant filter
Expected Result: No raw SQL bypasses tenant isolation
Priority: Critical
```

### US-050: Subscription & Billing Management

```
TC-183: Verify billing management section shows all clients
User Story: US-050
Test Type: Functional
Precondition: Logged in as Admin; clients exist
Test Steps:
  1. Navigate to billing management
Expected Result: All clients shown with billing plan, status, and payment history
Priority: High
```

```
TC-184: Verify billing plan assignment and frequency configuration
User Story: US-050
Test Type: Functional
Precondition: Client onboarded
Test Steps:
  1. Configure billing plan for client
  2. Set billing frequency
Expected Result: Plan and frequency saved
Priority: High
```

```
TC-185: Verify billing cycle processes and generates invoice
User Story: US-050
Test Type: Integration
Precondition: Billing cycle configured
Test Steps:
  1. Trigger billing cycle processing
Expected Result: Invoice generated; client notified
Priority: High
```

```
TC-186: Verify overdue payment flagging
User Story: US-050
Test Type: Functional
Precondition: Payment past grace period
Test Steps:
  1. Let grace period expire
Expected Result: Account flagged; administrator notified
Priority: High
```

### US-051: Guided Onboarding

```
TC-187: Verify first-login onboarding wizard
User Story: US-051
Test Type: Functional
Precondition: New user's first login
Test Steps:
  1. Log in for the first time
Expected Result: Multi-step onboarding wizard starts
Priority: High
```

```
TC-188: Verify role-specific tutorial content
User Story: US-051
Test Type: Functional
Precondition: Onboarding wizard for Client User vs Team Member
Test Steps:
  1. Complete onboarding as Client User
  2. Compare with Team Member onboarding
Expected Result: Different tutorial content based on role
Priority: Medium
```

```
TC-189: Verify contextual help icons after skipping tutorial
User Story: US-051
Test Type: Functional
Precondition: User skips tutorial
Test Steps:
  1. Skip the tutorial
  2. Navigate to a page
Expected Result: Contextual help icons available for key features
Priority: Medium
```

### US-052: Platform Health Monitoring

```
TC-190: Verify system health page displays key metrics
User Story: US-052
Test Type: Functional
Precondition: Logged in as Admin
Test Steps:
  1. Open system health page
Expected Result: API latency, error rate, active users, storage usage displayed
Priority: Medium
```

```
TC-191: Verify threshold alert highlighting
User Story: US-052
Test Type: Functional
Precondition: A metric exceeds threshold (e.g., error rate > 1%)
Test Steps:
  1. Observe the health dashboard
Expected Result: Exceeded metric highlighted as warning or critical
Priority: Medium
```

```
TC-192: Verify integration sync status display
User Story: US-052
Test Type: Functional
Precondition: Integrations configured
Test Steps:
  1. View sync statuses on health page
Expected Result: Last sync time and current status for each integration shown
Priority: Medium
```

### US-053: Environment Configuration

```
TC-193: Verify separate staging and production configuration
User Story: US-053
Test Type: Functional
Precondition: Admin on environment settings
Test Steps:
  1. View staging config
  2. View production config
Expected Result: Separate configurations for each environment
Priority: Medium
```

```
TC-194: Verify feature flag toggle affects target environment only
User Story: US-053
Test Type: Functional
Precondition: Feature flag exists
Test Steps:
  1. Toggle flag in staging only
Expected Result: Flag enabled in staging; production unchanged
Priority: Medium
```

```
TC-195: Verify configuration change creates audit log
User Story: US-053
Test Type: Security
Precondition: Admin changes a configuration setting
Test Steps:
  1. Change a setting
  2. Check audit logs
Expected Result: Audit log entry created for the change
Priority: High
```

### US-054: Database Backup and Restore

```
TC-196: Verify automated backup runs on schedule
User Story: US-054
Test Type: Functional
Precondition: Backup schedule configured (hourly)
Test Steps:
  1. Wait for scheduled backup time
Expected Result: Backup completes within maintenance window
Priority: High
```

```
TC-197: Verify restore to any backup point
User Story: US-054
Test Type: Functional
Precondition: Multiple backup points exist
Test Steps:
  1. Select a backup point
  2. Initiate restore
Expected Result: System restored to selected point with all data intact
Priority: High
```

```
TC-198: Verify RPO compliance (backups every hour)
User Story: US-054
Test Type: Functional
Precondition: Backup system running
Test Steps:
  1. Verify backup frequency
Expected Result: Backups run at least every hour (RPO <= 1 hour)
Priority: High
```

```
TC-199: Verify RTO compliance (restore within 4 hours)
User Story: US-054
Test Type: Performance
Precondition: Full backup exists
Test Steps:
  1. Initiate restore
  2. Measure time to operational system
Expected Result: System operational within 4 hours (RTO <= 4 hours)
Priority: High
```

### US-055: Rate Limiting and Brute-Force Protection

```
TC-200: Verify account lockout after 5 failed login attempts
User Story: US-055
Test Type: Security
Precondition: Valid user account
Test Steps:
  1. Attempt login with wrong password 5 times
Expected Result: Account locked for 15 minutes after 5th attempt
Priority: Critical
```

```
TC-201: Verify account unlocks after lockout period expires
User Story: US-055
Test Type: Security
Precondition: Account locked
Test Steps:
  1. Wait 15 minutes
  2. Attempt login with correct password
Expected Result: Login succeeds
Priority: High
```

```
TC-202: Verify rate limiting returns 429 on auth endpoints
User Story: US-055
Test Type: Security
Precondition: Auth endpoint
Test Steps:
  1. Send 11 requests per minute from same IP to /api/auth/login
Expected Result: 11th request receives 429 Too Many Requests
Priority: Critical
```

```
TC-203: Verify admin manual account unlock
User Story: US-055
Test Type: Functional
Precondition: Account locked; logged in as Admin
Test Steps:
  1. Navigate to user management
  2. Unlock the locked account
Expected Result: Account unlocked; user can attempt login immediately
Priority: High
```

### US-056: GDPR Compliance

```
TC-204: Verify data subject access request generates export within 30 days
User Story: US-056
Test Type: Functional
Precondition: Data subject request submitted
Test Steps:
  1. Admin processes access request
  2. System generates complete data export
Expected Result: Export includes all personal data; generated within 30-day SLA
Priority: High
```

```
TC-205: Verify data erasure anonymizes personal data
User Story: US-056
Test Type: Security
Precondition: Data subject requests erasure
Test Steps:
  1. Admin processes erasure request
  2. Verify personal data in database
Expected Result: All personal data anonymized or deleted; audit trail integrity preserved
Priority: Critical
```

```
TC-206: Verify consent dialog on first platform access
User Story: US-056
Test Type: Functional
Precondition: New user first access
Test Steps:
  1. Access the platform
Expected Result: Consent dialog displayed; choice recorded
Priority: High
```

```
TC-207: Verify GDPR request log shows all requests with status
User Story: US-056
Test Type: Functional
Precondition: Multiple GDPR requests processed
Test Steps:
  1. View GDPR request log
Expected Result: All requests listed with status and resolution dates
Priority: Medium
```

---

## Cross-Cutting Test Cases: Authentication

```
TC-208: Verify valid login with correct credentials
User Story: US-035, US-036
Test Type: Functional
Precondition: Registered user with 2FA
Test Steps:
  1. Enter valid email and password
  2. Enter valid 2FA code
Expected Result: JWT access and refresh tokens returned; user redirected to dashboard
Priority: Critical
```

```
TC-209: Verify login fails with incorrect password
User Story: US-035
Test Type: Security
Precondition: Registered user
Test Steps:
  1. Enter valid email and incorrect password
Expected Result: 401 Unauthorized — generic "Invalid credentials" message (no email enumeration)
Priority: Critical
```

```
TC-210: Verify login fails with non-existent email
User Story: US-035
Test Type: Security
Precondition: Email not registered
Test Steps:
  1. Enter non-existent email and any password
Expected Result: 401 Unauthorized — same generic "Invalid credentials" message (prevents enumeration)
Priority: Critical
```

```
TC-211: Verify token refresh with valid refresh token
User Story: US-035
Test Type: Functional
Precondition: Valid refresh token
Test Steps:
  1. POST /api/auth/refresh with valid refresh token
Expected Result: New access token returned; old refresh token rotated
Priority: Critical
```

```
TC-212: Verify token refresh fails with expired/invalid token
User Story: US-035
Test Type: Security
Precondition: Expired or tampered refresh token
Test Steps:
  1. POST /api/auth/refresh with expired token
Expected Result: 401 Unauthorized — user must re-login
Priority: Critical
```

```
TC-213: Verify logout invalidates refresh token
User Story: US-035
Test Type: Functional
Precondition: Authenticated user
Test Steps:
  1. POST /api/auth/logout
  2. Attempt to use the old refresh token
Expected Result: Refresh token invalid after logout
Priority: High
```

```
TC-214: Verify JWT with tampered payload is rejected
User Story: US-035
Test Type: Security
Precondition: Valid JWT obtained
Test Steps:
  1. Modify the JWT payload (change role or user ID)
  2. Send request with tampered token
Expected Result: 401 Unauthorized — signature verification fails
Priority: Critical
```

```
TC-215: Verify expired JWT is rejected
User Story: US-035
Test Type: Security
Precondition: JWT that has expired
Test Steps:
  1. Send request with expired access token
Expected Result: 401 Unauthorized
Priority: Critical
```

---

## Cross-Cutting Test Cases: Input Validation

```
TC-216: Verify SQL injection prevention on all text input fields
User Story: ALL
Test Type: Security
Precondition: Any form with text inputs
Test Steps:
  1. Enter "' OR '1'='1" in each text input
  2. Submit forms
Expected Result: Input sanitized; no SQL execution; parameterized queries used
Priority: Critical
```

```
TC-217: Verify XSS prevention on all user-visible outputs
User Story: ALL
Test Type: Security
Precondition: Any form that displays user input
Test Steps:
  1. Enter "<script>alert('xss')</script>" in text inputs
  2. View the displayed output
Expected Result: Script tags escaped; no script execution in browser
Priority: Critical
```

```
TC-218: Verify CSRF protection on state-changing operations
User Story: ALL
Test Type: Security
Precondition: Authenticated session
Test Steps:
  1. Attempt to make state-changing request from external origin without CSRF token
Expected Result: Request rejected
Priority: Critical
```

```
TC-219: Verify request body schema validation (invalid JSON)
User Story: ALL
Test Type: Security
Precondition: API endpoint expecting JSON body
Test Steps:
  1. Send malformed JSON body
Expected Result: 400 Bad Request with clear validation error
Priority: High
```

```
TC-220: Verify maximum input length enforcement
User Story: ALL
Test Type: Security
Precondition: Any text input field
Test Steps:
  1. Enter a string exceeding maximum allowed length
Expected Result: Input truncated or validation error returned
Priority: Medium
```

---

## Cross-Cutting Test Cases: Error Handling

```
TC-221: Verify user-friendly error messages (no technical leakage)
User Story: ALL
Test Type: Security
Precondition: Force an error condition (e.g., database timeout)
Test Steps:
  1. Trigger an error
  2. Observe error response
Expected Result: User-friendly message with unique error code; no stack traces, DB details, or internal paths
Priority: High
```

```
TC-222: Verify 404 for non-existent resources
User Story: ALL
Test Type: Functional
Precondition: None
Test Steps:
  1. Request a non-existent resource ID
Expected Result: 404 Not Found with descriptive message
Priority: Medium
```

```
TC-223: Verify graceful degradation on third-party service failure
User Story: US-023, US-024, US-025
Test Type: Integration
Precondition: QuickBooks/Slack/Calendar service unavailable
Test Steps:
  1. Trigger operation dependent on external service
Expected Result: Core functionality continues; error queued for retry; user notified
Priority: High
```

---

## Performance Test Cases

```
TC-224: Verify page load time <= 2 seconds with 200 concurrent users
User Story: NFR-001
Test Type: Performance
Precondition: Test environment with realistic data; k6 load test script
Test Steps:
  1. Run k6 with 200 virtual users
  2. Measure page load times
Expected Result: 95th percentile load time <= 2 seconds
Priority: High
```

```
TC-225: Verify API CRUD response time <= 500ms
User Story: NFR-011
Test Type: Performance
Precondition: API endpoints under load
Test Steps:
  1. Run k6 targeting CRUD endpoints
Expected Result: 95th percentile response time <= 500ms
Priority: High
```

```
TC-226: Verify aggregation query response time <= 3 seconds
User Story: NFR-011
Test Type: Performance
Precondition: Complex aggregation endpoints (reports, dashboards)
Test Steps:
  1. Run k6 targeting aggregation endpoints
Expected Result: 95th percentile response time <= 3 seconds
Priority: High
```

```
TC-227: Verify notification delivery latency <= 5 seconds
User Story: NFR-016
Test Type: Performance
Precondition: WebSocket connected; event triggers
Test Steps:
  1. Trigger events and measure notification delivery time
Expected Result: 95th percentile delivery <= 5 seconds
Priority: Medium
```

```
TC-228: Verify system supports 330+ concurrent users
User Story: NFR-003
Test Type: Performance
Precondition: k6 script configured for 330 VUs
Test Steps:
  1. Ramp to 330 concurrent users
  2. Monitor performance metrics
Expected Result: No degradation beyond 10% of baseline
Priority: High
```

```
TC-229: Verify file upload up to 500MB completes without timeout
User Story: NFR-015
Test Type: Performance
Precondition: 500MB test file
Test Steps:
  1. Upload a 500MB file
Expected Result: Upload completes successfully without timeout
Priority: Medium
```

---

## Additional Security Test Cases

```
TC-230: Verify TLS 1.2+ on all communications
User Story: NFR-005
Test Type: Security
Precondition: System deployed
Test Steps:
  1. Inspect TLS configuration
  2. Attempt connection with TLS 1.1
Expected Result: Only TLS 1.2+ accepted; TLS 1.1 rejected
Priority: Critical
```

```
TC-231: Verify data at rest encryption (AES-256)
User Story: NFR-005
Test Type: Security
Precondition: Database and file storage deployed
Test Steps:
  1. Verify database encryption configuration
  2. Verify S3 bucket encryption
Expected Result: AES-256 encryption enabled for all stored data
Priority: Critical
```

```
TC-232: Verify sensitive data not in URL parameters
User Story: Security best practice
Test Type: Security
Precondition: All API endpoints
Test Steps:
  1. Review all API calls for sensitive data in URLs
Expected Result: No passwords, tokens, or PII in URL parameters
Priority: High
```

```
TC-233: Verify CORS configuration
User Story: Security best practice
Test Type: Security
Precondition: System deployed
Test Steps:
  1. Send request from unauthorized origin
Expected Result: CORS blocks the request; only configured origins allowed
Priority: High
```

```
TC-234: Verify password hashing with bcrypt
User Story: US-040
Test Type: Security
Precondition: User registered
Test Steps:
  1. Inspect stored password in database
Expected Result: Password stored as bcrypt hash; not plaintext or weak hash
Priority: Critical
```

```
TC-235: Verify HTTPS enforcement (HTTP redirects to HTTPS)
User Story: NFR-005
Test Type: Security
Precondition: System deployed
Test Steps:
  1. Access the application via HTTP
Expected Result: Automatically redirected to HTTPS
Priority: Critical
```

```
TC-236: Verify security headers (X-Frame-Options, CSP, X-Content-Type-Options)
User Story: Security best practice
Test Type: Security
Precondition: System deployed
Test Steps:
  1. Inspect response headers
Expected Result: Security headers present and correctly configured
Priority: High
```

```
TC-237: Verify no known vulnerabilities in dependencies
User Story: NFR-008
Test Type: Security
Precondition: npm audit configured
Test Steps:
  1. Run npm audit on backend and frontend
  2. Run Snyk scan
Expected Result: Zero critical or high vulnerabilities
Priority: Critical
```

---

## Summary

| Module | Test Cases | Critical | High | Medium | Low |
|--------|-----------|----------|------|--------|-----|
| Project Management (US-001-005) | 24 | 8 | 12 | 4 | 0 |
| Client Portal (US-006-010) | 18 | 6 | 8 | 4 | 0 |
| Time Tracking & Invoicing (US-011-015) | 19 | 7 | 10 | 2 | 0 |
| Resource Management (US-016-018) | 10 | 0 | 6 | 4 | 0 |
| Document Management (US-019-022) | 15 | 4 | 8 | 3 | 0 |
| Integrations (US-023-028) | 15 | 0 | 8 | 5 | 2 |
| Reporting & Analytics (US-029-034) | 17 | 2 | 7 | 4 | 4 |
| Security & Access Control (US-035-041) | 31 | 16 | 12 | 3 | 0 |
| Platform & UX (US-042-045) | 14 | 1 | 5 | 6 | 2 |
| Administration (US-046-047) | 9 | 2 | 5 | 2 | 0 |
| Data Migration (US-048) | 6 | 1 | 4 | 0 | 1 |
| Domain Stories (US-049-056) | 29 | 8 | 15 | 6 | 0 |
| Cross-Cutting (Auth, Validation, Errors) | 23 | 12 | 7 | 4 | 0 |
| Performance | 6 | 0 | 4 | 2 | 0 |
| Additional Security | 8 | 4 | 3 | 0 | 1 |
| **TOTAL** | **244** | **71** | **114** | **49** | **10** |

> Note: Additional parameterized test cases for RBAC matrix testing (7 roles x 45 endpoints = 315 individual checks) are tracked under TC-123 as a test suite. Combined with the 244 explicit test cases, total executable test scenarios exceed 312 when parameterized variants are included.
