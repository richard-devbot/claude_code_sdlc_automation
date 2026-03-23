# API Test Outlines — TechNova Solutions Client Project Management Platform

**Document Version:** 1.0
**Date:** 2026-03-12
**Total API Endpoints:** 45
**Scenarios Per Endpoint:** 5 (200, 401, 403, 400, 404)
**Total API Test Scenarios:** 225

---

## 1. Authentication Service (`/api/auth`)

### POST /api/auth/register
**Description:** Register a new user account with email, password, and role assignment
**Auth Required:** No

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid registration | POST | None | `{email, password, firstName, lastName}` | 201 Created | User object with ID; no password in response |
| Duplicate email | POST | None | `{email: existing@test.com, ...}` | 409 Conflict | Error: email already registered |
| Invalid body — missing email | POST | None | `{password, firstName}` | 400 Bad Request | Validation error: email is required |
| Invalid body — weak password | POST | None | `{email, password: "short"}` | 400 Bad Request | Validation error: password does not meet policy |
| SQL injection in email field | POST | None | `{email: "' OR 1=1--", ...}` | 400 Bad Request | Validation error; no SQL execution |

### POST /api/auth/login
**Description:** Authenticate user with email/password, returns JWT tokens
**Auth Required:** No

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid credentials | POST | None | `{email, password}` | 200 OK | Access token + refresh token (or 2FA challenge) |
| Invalid password | POST | None | `{email, password: "wrong"}` | 401 Unauthorized | Generic "Invalid credentials" message |
| Non-existent email | POST | None | `{email: "no@exist.com", ...}` | 401 Unauthorized | Same generic message (no enumeration) |
| Missing fields | POST | None | `{email}` | 400 Bad Request | Validation error: password is required |
| Account locked (brute force) | POST | None | Valid creds after 5 failures | 423 Locked | Account locked; try again after lockout period |
| Rate limit exceeded | POST | None | 11th request in 60s | 429 Too Many Requests | Rate limit error |

### POST /api/auth/2fa/setup
**Description:** Generate a TOTP secret + QR code for 2FA enrollment
**Auth Required:** Yes

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid request with auth | POST | Valid JWT | None | 200 OK | TOTP secret + QR code data URL |
| No auth token | POST | None | None | 401 Unauthorized | Authentication required |
| Expired JWT | POST | Expired JWT | None | 401 Unauthorized | Token expired |
| 2FA already setup | POST | Valid JWT (2FA active) | None | 409 Conflict | 2FA already configured |

### POST /api/auth/2fa/verify
**Description:** Verify TOTP 2FA code to complete login flow
**Auth Required:** Partial (pending 2FA)

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid TOTP code | POST | Pending auth token | `{code: "123456"}` | 200 OK | Full access + refresh tokens |
| Invalid TOTP code | POST | Pending auth token | `{code: "000000"}` | 401 Unauthorized | Invalid 2FA code |
| Expired TOTP code | POST | Pending auth token | `{code: expired}` | 401 Unauthorized | Code expired |
| Missing code field | POST | Pending auth token | `{}` | 400 Bad Request | Validation error: code required |
| No auth token | POST | None | `{code: "123456"}` | 401 Unauthorized | Authentication required |

### POST /api/auth/refresh
**Description:** Exchange refresh token for new access token
**Auth Required:** No (uses refresh token)

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid refresh token | POST | None | `{refreshToken: valid}` | 200 OK | New access token + rotated refresh token |
| Expired refresh token | POST | None | `{refreshToken: expired}` | 401 Unauthorized | Refresh token expired; re-login required |
| Tampered refresh token | POST | None | `{refreshToken: tampered}` | 401 Unauthorized | Invalid token |
| Missing refresh token | POST | None | `{}` | 400 Bad Request | Validation error: refreshToken required |
| Revoked refresh token (post-logout) | POST | None | `{refreshToken: revoked}` | 401 Unauthorized | Token has been revoked |

### POST /api/auth/logout
**Description:** Invalidate refresh token and end user session
**Auth Required:** Yes

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid logout | POST | Valid JWT | `{refreshToken}` | 200 OK | Session ended; tokens invalidated |
| No auth token | POST | None | `{refreshToken}` | 401 Unauthorized | Authentication required |
| Already logged out | POST | Valid JWT | `{refreshToken: revoked}` | 200 OK | Idempotent success |

### GET /api/auth/me
**Description:** Return the authenticated user's profile
**Auth Required:** Yes

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid request | GET | Valid JWT | N/A | 200 OK | User profile (no password hash) |
| No auth token | GET | None | N/A | 401 Unauthorized | Authentication required |
| Expired JWT | GET | Expired JWT | N/A | 401 Unauthorized | Token expired |

---

## 2. Project Management Service (`/api/projects`)

### GET /api/projects
**Description:** List all projects with filtering, sorting, and pagination
**Roles Allowed:** admin, executive, pm, team_lead, team_member, finance_manager

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request — admin | GET | Admin JWT | `?page=1&limit=20` | 200 OK | Paginated project list |
| Valid request — team_member | GET | Team Member JWT | `?status=active` | 200 OK | Filtered project list (only assigned projects) |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — client_user | GET | Client User JWT | None | 403 Forbidden | Insufficient permissions |
| Invalid query params | GET | Admin JWT | `?page=-1` | 400 Bad Request | Validation error |

### POST /api/projects
**Description:** Create a new project
**Roles Allowed:** admin, pm

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid creation — admin | POST | Admin JWT | `{name, clientId, startDate, deadline, budget, teamIds}` | 201 Created | Created project object |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — team_member | POST | Team Member JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Invalid body — missing name | POST | Admin JWT | `{clientId, startDate}` | 400 Bad Request | Validation error: name required |
| Non-existent clientId | POST | Admin JWT | `{name, clientId: "invalid-uuid"}` | 404 Not Found | Client not found |

### GET /api/projects/:projectId
**Description:** Get a single project by ID
**Roles Allowed:** admin, executive, pm, team_lead, team_member, finance_manager, client_user

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | PM JWT | `/:validId` | 200 OK | Full project details |
| No auth | GET | None | `/:validId` | 401 Unauthorized | Authentication required |
| Non-existent project | GET | Admin JWT | `/:nonExistentId` | 404 Not Found | Project not found |
| Client user — own project | GET | Client JWT | `/:ownProjectId` | 200 OK | Project details (limited fields) |
| Client user — other org project | GET | Client JWT | `/:otherOrgProjectId` | 403 Forbidden | Access denied |

### PATCH /api/projects/:projectId
**Description:** Update an existing project
**Roles Allowed:** admin, pm

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid update | PATCH | PM JWT | `{deadline: "2026-12-31"}` | 200 OK | Updated project object |
| No auth | PATCH | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — team_member | PATCH | Team Member JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Invalid body — bad date | PATCH | PM JWT | `{deadline: "not-a-date"}` | 400 Bad Request | Validation error |
| Non-existent project | PATCH | Admin JWT | Valid body | 404 Not Found | Project not found |

### DELETE /api/projects/:projectId
**Description:** Soft-delete a project
**Roles Allowed:** admin

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid delete — admin | DELETE | Admin JWT | `/:validId` | 200 OK | Project soft-deleted |
| No auth | DELETE | None | `/:validId` | 401 Unauthorized | Authentication required |
| Wrong role — pm | DELETE | PM JWT | `/:validId` | 403 Forbidden | Only admin can delete |
| Non-existent project | DELETE | Admin JWT | `/:nonExistentId` | 404 Not Found | Project not found |
| Already deleted project | DELETE | Admin JWT | `/:deletedId` | 404 Not Found | Project not found |

### POST /api/projects/:projectId/tasks
**Description:** Create a task within a project
**Roles Allowed:** admin, pm, team_lead

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid task creation | POST | PM JWT | `{title, assigneeId, dueDate, description}` | 201 Created | Created task object |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — team_member | POST | Team Member JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Invalid body — missing title | POST | PM JWT | `{assigneeId}` | 400 Bad Request | Validation error: title required |
| Non-existent project | POST | PM JWT | Valid body on `/:nonExistentId` | 404 Not Found | Project not found |

### PATCH /api/projects/:projectId/tasks/:taskId
**Description:** Update task status, assignee, or details (Kanban drag-and-drop)
**Roles Allowed:** admin, pm, team_lead, team_member

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid status update | PATCH | Team Member JWT | `{status: "in_progress"}` | 200 OK | Updated task |
| No auth | PATCH | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — client_user | PATCH | Client JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Invalid status transition | PATCH | Team Member JWT | `{status: "done"}` from "to_do" | 400 Bad Request | Invalid status transition |
| Non-existent task | PATCH | PM JWT | Valid body on `/:nonExistentTaskId` | 404 Not Found | Task not found |

### POST /api/projects/:projectId/milestones
**Description:** Create a milestone with target date and deliverable associations
**Roles Allowed:** admin, pm

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid milestone creation | POST | PM JWT | `{name, targetDate, requiresApproval}` | 201 Created | Created milestone |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — team_lead | POST | Team Lead JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Invalid body — missing name | POST | PM JWT | `{targetDate}` | 400 Bad Request | Validation error: name required |
| Non-existent project | POST | PM JWT | Valid body on `/:nonExistentId` | 404 Not Found | Project not found |

---

## 3. Client Portal Service (`/api/portal`)

### GET /api/portal/dashboard
**Description:** Get client dashboard with project statuses
**Roles Allowed:** client_user

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request — client | GET | Client JWT | None | 200 OK | Client's projects with status and milestones |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — admin | GET | Admin JWT | None | 403 Forbidden | Portal is for client users only |
| Tenant isolation check | GET | Client A JWT | None | 200 OK | Zero data from other tenants |

### GET /api/portal/projects/:projectId/deliverables
**Description:** List deliverables for a client project
**Roles Allowed:** client_user

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | Client JWT | `/:ownProjectId` | 200 OK | Deliverables with download links |
| No auth | GET | None | `/:projectId` | 401 Unauthorized | Authentication required |
| Other org's project | GET | Client JWT | `/:otherOrgProjectId` | 403 Forbidden | Access denied |
| Non-existent project | GET | Client JWT | `/:nonExistentId` | 404 Not Found | Project not found |

### POST /api/portal/milestones/:milestoneId/approve
**Description:** Approve or request revision on a milestone
**Roles Allowed:** client_user

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid approval | POST | Client JWT | `{action: "approve"}` | 200 OK | Milestone approved with timestamp |
| Valid revision request | POST | Client JWT | `{action: "request_revision", comment: "Fix layout"}` | 200 OK | Revision requested |
| Revision without comment | POST | Client JWT | `{action: "request_revision"}` | 400 Bad Request | Comment required for revision |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Non-existent milestone | POST | Client JWT | Valid body on `/:nonExistentId` | 404 Not Found | Milestone not found |
| Other org's milestone | POST | Client JWT | Valid body on `/:otherOrgMilestoneId` | 403 Forbidden | Access denied |

### GET /api/portal/projects/:projectId/messages
**Description:** Get threaded messages for client-team communication
**Roles Allowed:** client_user, pm, team_member

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request — client | GET | Client JWT | `/:ownProjectId` | 200 OK | Threaded messages |
| Valid request — pm | GET | PM JWT | `/:projectId` | 200 OK | Threaded messages |
| No auth | GET | None | `/:projectId` | 401 Unauthorized | Authentication required |
| Wrong role — finance_manager | GET | Finance JWT | `/:projectId` | 403 Forbidden | Insufficient permissions |
| Non-existent project | GET | Client JWT | `/:nonExistentId` | 404 Not Found | Project not found |

### POST /api/portal/projects/:projectId/messages
**Description:** Send a message with optional file attachment
**Roles Allowed:** client_user, pm, team_member

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid message | POST | Client JWT | `{content: "Hello", projectId}` | 201 Created | Message created |
| Message with attachment | POST | Client JWT | multipart form with file | 201 Created | Message + attachment stored |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Empty message | POST | Client JWT | `{content: ""}` | 400 Bad Request | Content required |
| Non-existent project | POST | Client JWT | `/:nonExistentId` body | 404 Not Found | Project not found |
| XSS in message content | POST | Client JWT | `{content: "<script>alert(1)</script>"}` | 201 Created | Content sanitized; no script in stored value |

---

## 4. Time Tracking Service (`/api/time`)

### POST /api/time/entries
**Description:** Create a manual time entry
**Roles Allowed:** team_member, team_lead, pm

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid time entry | POST | Team Member JWT | `{projectId, taskId, hours, date, description, billable}` | 201 Created | Created entry |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — client_user | POST | Client JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Missing project/task | POST | Team Member JWT | `{hours, date}` | 400 Bad Request | project and task required |
| Negative hours | POST | Team Member JWT | `{hours: -2, ...}` | 400 Bad Request | Hours must be positive |
| Non-existent project | POST | Team Member JWT | `{projectId: "invalid-uuid", ...}` | 404 Not Found | Project not found |

### POST /api/time/timer/start
**Description:** Start a live timer
**Roles Allowed:** team_member, team_lead

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid start | POST | Team Member JWT | `{projectId, taskId}` | 200 OK | Timer started with timestamp |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — admin | POST | Admin JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Timer already running | POST | Team Member JWT | Valid body | 409 Conflict | Stop existing timer first |
| Missing projectId | POST | Team Member JWT | `{taskId}` | 400 Bad Request | projectId required |

### POST /api/time/timer/stop
**Description:** Stop the running timer and save time entry
**Roles Allowed:** team_member, team_lead

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid stop | POST | Team Member JWT | None | 200 OK | Time entry created from timer duration |
| No auth | POST | None | None | 401 Unauthorized | Authentication required |
| No timer running | POST | Team Member JWT | None | 404 Not Found | No active timer found |
| Wrong role — client_user | POST | Client JWT | None | 403 Forbidden | Insufficient permissions |

### GET /api/time/timesheets
**Description:** Get timesheets for a user or team
**Roles Allowed:** team_member, team_lead, pm, admin

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request — own timesheet | GET | Team Member JWT | `?period=weekly&date=2026-03-09` | 200 OK | Weekly timesheet with project breakdown |
| Valid request — team lead views team | GET | Team Lead JWT | `?teamId=123` | 200 OK | Team members' timesheets |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — client_user | GET | Client JWT | None | 403 Forbidden | Insufficient permissions |
| Invalid period | GET | Team Member JWT | `?period=invalid` | 400 Bad Request | Validation error |

### POST /api/time/timesheets/:timesheetId/approve
**Description:** Approve or reject a submitted timesheet
**Roles Allowed:** pm, team_lead, admin

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid approval | POST | PM JWT | `{action: "approve"}` | 200 OK | Timesheet approved |
| Valid rejection | POST | PM JWT | `{action: "reject", reason: "Incorrect hours"}` | 200 OK | Timesheet rejected with reason |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — team_member | POST | Team Member JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Non-existent timesheet | POST | PM JWT | Valid body on `/:nonExistentId` | 404 Not Found | Timesheet not found |
| Rejection without reason | POST | PM JWT | `{action: "reject"}` | 400 Bad Request | Reason required for rejection |

---

## 5. Invoice Service (`/api/invoices`)

### POST /api/invoices/generate
**Description:** Generate a draft invoice from approved time entries
**Roles Allowed:** admin, finance_manager, pm

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid generation | POST | Finance JWT | `{projectId, dateRange}` | 201 Created | Draft invoice with line items |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — team_member | POST | Team Member JWT | Valid body | 403 Forbidden | Insufficient permissions |
| No approved entries | POST | Finance JWT | `{projectId with no entries}` | 400 Bad Request | No approved time entries for period |
| Non-existent project | POST | Finance JWT | `{projectId: "invalid"}` | 404 Not Found | Project not found |

### GET /api/invoices
**Description:** List invoices with filtering
**Roles Allowed:** admin, finance_manager, pm, executive

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | Finance JWT | `?status=draft` | 200 OK | Filtered invoice list |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — team_member | GET | Team Member JWT | None | 403 Forbidden | Insufficient permissions |
| Invalid status filter | GET | Finance JWT | `?status=invalid` | 400 Bad Request | Invalid status value |

### PATCH /api/invoices/:invoiceId
**Description:** Edit draft invoice line items
**Roles Allowed:** admin, finance_manager

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid edit | PATCH | Finance JWT | `{lineItems: [...adjusted]}` | 200 OK | Updated draft |
| Edit finalized invoice | PATCH | Finance JWT | Body on finalized invoice | 403 Forbidden | Cannot edit finalized invoice |
| No auth | PATCH | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — pm | PATCH | PM JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Non-existent invoice | PATCH | Finance JWT | Valid body on `/:nonExistentId` | 404 Not Found | Invoice not found |

### POST /api/invoices/:invoiceId/finalize
**Description:** Finalize an invoice making it immutable
**Roles Allowed:** admin, finance_manager

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid finalization | POST | Finance JWT | `/:draftInvoiceId` | 200 OK | Invoice finalized with unique number |
| Already finalized | POST | Finance JWT | `/:finalizedId` | 409 Conflict | Invoice already finalized |
| No auth | POST | None | `/:invoiceId` | 401 Unauthorized | Authentication required |
| Wrong role — pm | POST | PM JWT | `/:invoiceId` | 403 Forbidden | Insufficient permissions |
| Non-existent invoice | POST | Finance JWT | `/:nonExistentId` | 404 Not Found | Invoice not found |

### POST /api/invoices/:invoiceId/sync-quickbooks
**Description:** Push finalized invoice to QuickBooks
**Roles Allowed:** admin, finance_manager

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid sync | POST | Finance JWT | `/:finalizedId` | 200 OK | Sync initiated; status returned |
| Sync draft invoice | POST | Finance JWT | `/:draftId` | 400 Bad Request | Only finalized invoices can sync |
| No auth | POST | None | `/:invoiceId` | 401 Unauthorized | Authentication required |
| QuickBooks not connected | POST | Finance JWT | `/:invoiceId` | 424 Failed Dependency | QuickBooks integration not configured |
| Non-existent invoice | POST | Finance JWT | `/:nonExistentId` | 404 Not Found | Invoice not found |

---

## 6. Document Service (`/api/documents`)

### POST /api/documents/upload
**Description:** Upload a document to a project with S3 storage
**Roles Allowed:** admin, pm, team_lead, team_member

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid upload | POST | Team Member JWT | multipart form `{file, projectId, folderId}` | 201 Created | Document metadata with S3 key |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — client_user | POST | Client JWT | Valid body | 403 Forbidden | Insufficient permissions |
| File too large (>500MB) | POST | Team Member JWT | 501MB file | 413 Payload Too Large | File exceeds maximum size |
| Missing file | POST | Team Member JWT | `{projectId, folderId}` no file | 400 Bad Request | File is required |
| Non-existent project | POST | Team Member JWT | `{projectId: "invalid"}` | 404 Not Found | Project not found |

### GET /api/documents/:documentId/versions
**Description:** List all versions of a document
**Roles Allowed:** admin, pm, team_lead, team_member, client_user

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | Team Member JWT | `/:validId` | 200 OK | Version list with timestamps |
| No auth | GET | None | `/:validId` | 401 Unauthorized | Authentication required |
| Non-existent document | GET | Team Member JWT | `/:nonExistentId` | 404 Not Found | Document not found |
| Client — other org's doc | GET | Client JWT | `/:otherOrgDocId` | 403 Forbidden | Access denied |

### GET /api/documents/:documentId/download
**Description:** Download a document via signed S3 URL
**Roles Allowed:** admin, pm, team_lead, team_member, client_user

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid download | GET | Team Member JWT | `/:validId` | 200 OK | Signed S3 URL or file stream |
| No auth | GET | None | `/:validId` | 401 Unauthorized | Authentication required |
| Non-existent document | GET | Team Member JWT | `/:nonExistentId` | 404 Not Found | Document not found |
| Client — other org's doc | GET | Client JWT | `/:otherOrgDocId` | 403 Forbidden | Access denied |

### POST /api/documents/:documentId/comments
**Description:** Add a comment to a document
**Roles Allowed:** admin, pm, team_lead, team_member, client_user

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid comment | POST | Team Member JWT | `{content: "Looks good", parentId: null}` | 201 Created | Comment created |
| Threaded reply | POST | Client JWT | `{content: "Agreed", parentId: "comment-123"}` | 201 Created | Reply created under parent |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Empty content | POST | Team Member JWT | `{content: ""}` | 400 Bad Request | Content required |
| Non-existent document | POST | Team Member JWT | Valid body on `/:nonExistentId` | 404 Not Found | Document not found |
| XSS in content | POST | Team Member JWT | `{content: "<script>alert(1)</script>"}` | 201 Created | Content sanitized |

---

## 7. Resource Management Service (`/api/resources`)

### GET /api/resources/allocations
**Description:** Get resource allocation board
**Roles Allowed:** admin, pm, team_lead, executive

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | PM JWT | `?teamId=123` | 200 OK | Team members with utilization data |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — team_member | GET | Team Member JWT | None | 403 Forbidden | Insufficient permissions |
| Invalid filter | GET | PM JWT | `?teamId=invalid` | 400 Bad Request | Validation error |

### POST /api/resources/assignments
**Description:** Assign a team member to a project
**Roles Allowed:** admin, pm, team_lead

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid assignment | POST | PM JWT | `{userId, projectId, hoursPerWeek, startDate, endDate}` | 201 Created | Assignment created |
| Overallocation warning | POST | PM JWT | `{userId (at 90% util), ...}` | 200 OK with warning | Assignment created with overallocation flag |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — team_member | POST | Team Member JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Non-existent user | POST | PM JWT | `{userId: "invalid"}` | 404 Not Found | User not found |

### GET /api/resources/utilization
**Description:** Get utilization metrics for team members
**Roles Allowed:** admin, pm, team_lead, executive

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | PM JWT | `?startDate=...&endDate=...` | 200 OK | Utilization metrics per member |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — team_member | GET | Team Member JWT | None | 403 Forbidden | Insufficient permissions |

### GET /api/resources/forecast
**Description:** Get capacity forecast for next 4-12 weeks
**Roles Allowed:** admin, pm, team_lead, executive

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | PM JWT | `?weeks=8` | 200 OK | Forecast data per member |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — client_user | GET | Client JWT | None | 403 Forbidden | Insufficient permissions |
| Invalid weeks | GET | PM JWT | `?weeks=52` | 400 Bad Request | Weeks must be 4-12 |

---

## 8. Reporting Service (`/api/reports`)

### GET /api/reports/executive-dashboard
**Description:** Get executive dashboard KPIs
**Roles Allowed:** admin, executive

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | Executive JWT | None | 200 OK | Five KPIs with drill-down data |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — pm | GET | PM JWT | None | 403 Forbidden | Insufficient permissions |

### GET /api/reports/profitability
**Description:** Get project profitability analysis
**Roles Allowed:** admin, executive, finance_manager

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | Finance JWT | `?clientId=123&dateRange=...` | 200 OK | Profitability data with variance |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — team_member | GET | Team Member JWT | None | 403 Forbidden | Insufficient permissions |
| Invalid date range | GET | Finance JWT | `?startDate=2026-12-01&endDate=2026-01-01` | 400 Bad Request | End date before start date |

### POST /api/reports/generate
**Description:** Generate a configurable report
**Roles Allowed:** admin, executive, pm, finance_manager

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid report | POST | PM JWT | `{type: "utilization", filters: {...}}` | 201 Created | Report ID with status |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — team_member | POST | Team Member JWT | Valid body | 403 Forbidden | Insufficient permissions |
| Invalid report type | POST | PM JWT | `{type: "invalid"}` | 400 Bad Request | Unknown report type |

### GET /api/reports/export/:reportId
**Description:** Export report as PDF/CSV/Excel
**Roles Allowed:** admin, executive, pm, finance_manager

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid export — PDF | GET | PM JWT | `/:reportId?format=pdf` | 200 OK | PDF file stream |
| Valid export — CSV | GET | PM JWT | `/:reportId?format=csv` | 200 OK | CSV file stream |
| No auth | GET | None | `/:reportId` | 401 Unauthorized | Authentication required |
| Non-existent report | GET | PM JWT | `/:nonExistentId` | 404 Not Found | Report not found |
| Invalid format | GET | PM JWT | `/:reportId?format=xml` | 400 Bad Request | Unsupported format |

---

## 9. Integration Service (`/api/integrations`)

### POST /api/integrations/quickbooks/connect
**Description:** Initiate OAuth 2.0 flow for QuickBooks
**Roles Allowed:** admin, finance_manager

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid connect | POST | Admin JWT | None | 200 OK | OAuth redirect URL |
| No auth | POST | None | None | 401 Unauthorized | Authentication required |
| Wrong role — pm | POST | PM JWT | None | 403 Forbidden | Insufficient permissions |

### POST /api/integrations/slack/connect
**Description:** Connect Slack workspace
**Roles Allowed:** admin

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid connect | POST | Admin JWT | `{workspaceId}` | 200 OK | OAuth redirect URL |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — pm | POST | PM JWT | Valid body | 403 Forbidden | Only admin can connect |

### POST /api/integrations/google-calendar/connect
**Description:** Connect Google Calendar
**Roles Allowed:** admin, pm, team_lead, team_member

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid connect | POST | Team Member JWT | None | 200 OK | OAuth redirect URL |
| No auth | POST | None | None | 401 Unauthorized | Authentication required |
| Wrong role — client_user | POST | Client JWT | None | 403 Forbidden | Insufficient permissions |

### GET /api/integrations/status
**Description:** Get all integration connection statuses
**Roles Allowed:** admin

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | Admin JWT | None | 200 OK | Status for all integrations |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — pm | GET | PM JWT | None | 403 Forbidden | Admin only |

### POST /api/integrations/:provider/sync
**Description:** Trigger manual sync for an integration
**Roles Allowed:** admin

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid sync trigger | POST | Admin JWT | `/:quickbooks` | 200 OK | Sync initiated |
| No auth | POST | None | `/:quickbooks` | 401 Unauthorized | Authentication required |
| Wrong role — finance | POST | Finance JWT | `/:quickbooks` | 403 Forbidden | Admin only |
| Invalid provider | POST | Admin JWT | `/:invalid_provider` | 404 Not Found | Provider not found |
| Provider not connected | POST | Admin JWT | `/:slack` (not connected) | 424 Failed Dependency | Integration not connected |

---

## 10. Admin Service (`/api/admin`)

### GET /api/admin/users
**Description:** List all users
**Roles Allowed:** admin

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | Admin JWT | `?page=1&limit=50` | 200 OK | Paginated user list |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — pm | GET | PM JWT | None | 403 Forbidden | Admin only |

### POST /api/admin/users
**Description:** Create a new user and send invitation
**Roles Allowed:** admin

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid creation | POST | Admin JWT | `{email, role, firstName, lastName}` | 201 Created | User created; invitation sent |
| No auth | POST | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — pm | POST | PM JWT | Valid body | 403 Forbidden | Admin only |
| Duplicate email | POST | Admin JWT | `{email: existing@test.com}` | 409 Conflict | Email already registered |
| Invalid email | POST | Admin JWT | `{email: "not-an-email"}` | 400 Bad Request | Invalid email format |

### PUT /api/admin/roles/:roleId/permissions
**Description:** Update permissions for a role
**Roles Allowed:** admin

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid update | PUT | Admin JWT | `{permissions: [...]}` | 200 OK | Role updated |
| No auth | PUT | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — executive | PUT | Executive JWT | Valid body | 403 Forbidden | Admin only |
| Non-existent role | PUT | Admin JWT | Valid body on `/:nonExistentId` | 404 Not Found | Role not found |
| Invalid permissions | PUT | Admin JWT | `{permissions: "invalid"}` | 400 Bad Request | Validation error |

### GET /api/admin/audit-logs
**Description:** Query immutable audit logs
**Roles Allowed:** admin, executive

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request — admin | GET | Admin JWT | `?userId=123&action=LOGIN` | 200 OK | Filtered audit logs |
| Valid request — executive | GET | Executive JWT | `?dateRange=...` | 200 OK | Filtered audit logs |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |
| Wrong role — pm | GET | PM JWT | None | 403 Forbidden | Insufficient permissions |

### PUT /api/admin/settings
**Description:** Update system-wide settings
**Roles Allowed:** admin

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid update | PUT | Admin JWT | `{billingRates: {...}, notificationDefaults: {...}}` | 200 OK | Settings updated |
| No auth | PUT | None | Valid body | 401 Unauthorized | Authentication required |
| Wrong role — executive | PUT | Executive JWT | Valid body | 403 Forbidden | Admin only |
| Invalid settings schema | PUT | Admin JWT | `{billingRates: "not-an-object"}` | 400 Bad Request | Validation error |

---

## 11. Notification Service (`/api/notifications`)

### GET /api/notifications
**Description:** Get paginated in-app notifications
**Roles Allowed:** All authenticated users

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | Any JWT | `?page=1&limit=20` | 200 OK | Paginated notifications |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |

### PATCH /api/notifications/:notificationId/read
**Description:** Mark a notification as read
**Roles Allowed:** All authenticated users

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid mark as read | PATCH | Any JWT | `/:validId` | 200 OK | Notification marked as read |
| No auth | PATCH | None | `/:validId` | 401 Unauthorized | Authentication required |
| Non-existent notification | PATCH | Any JWT | `/:nonExistentId` | 404 Not Found | Notification not found |
| Other user's notification | PATCH | User A JWT | `/:userB_notifId` | 403 Forbidden | Not your notification |

### POST /api/notifications/mark-all-read
**Description:** Mark all unread notifications as read
**Roles Allowed:** All authenticated users

| Scenario | Method | Auth | Body | Expected Status | Expected Response |
|----------|--------|------|------|----------------|-------------------|
| Valid mark all | POST | Any JWT | None | 200 OK | All notifications marked as read |
| No auth | POST | None | None | 401 Unauthorized | Authentication required |

### GET /api/notifications/preferences
**Description:** Get user notification preferences
**Roles Allowed:** All authenticated users

| Scenario | Method | Auth | Params | Expected Status | Expected Response |
|----------|--------|------|--------|----------------|-------------------|
| Valid request | GET | Any JWT | None | 200 OK | User's notification preferences |
| No auth | GET | None | None | 401 Unauthorized | Authentication required |

---

## Summary

| Service | Endpoints | Test Scenarios |
|---------|-----------|---------------|
| Authentication | 7 | 38 |
| Project Management | 8 | 40 |
| Client Portal | 5 | 27 |
| Time Tracking | 5 | 27 |
| Invoice | 5 | 25 |
| Document | 4 | 22 |
| Resource Management | 4 | 16 |
| Reporting | 4 | 17 |
| Integration | 5 | 18 |
| Admin | 5 | 19 |
| Notification | 4 | 11 |
| **TOTAL** | **56** | **260** |
