# SDLC Terminology & End-to-End Pipeline Guide

## What You're Building — The Big Picture

You're automating the **entire software development lifecycle** — from the moment
a client calls your company to discuss a project idea, all the way through to
production deployment. Here's the real-world flow that IT companies follow,
mapped to what this automation does.

---

## The Complete SDLC Pipeline (Real-World)

### Phase 1: Pre-Sales & Discovery
**What happens in real IT companies:**
- The **Sales Team** receives a lead — a potential client interested in building software
- A **Discovery Call** (or Requirements Gathering session) is set up
- Attendees: Client stakeholders, Sales Lead, Business Analyst (BA), sometimes a Technical Lead
- The client describes their pain points, desired features, timeline, and budget
- The BA takes notes and asks clarifying questions
- This call is often recorded or transcribed

**Our automation:** Agent 01 (Transcript Agent) processes this transcript.

**Key terms:**
- **Discovery Call**: First meeting where the client explains what they need
- **Client Stakeholder**: Decision-makers from the client side (CEO, CTO, Product Owner)
- **Pre-Sales**: Activities before the contract is signed

---

### Phase 2: Requirements Engineering
**What happens:**
- The BA analyzes the meeting notes and creates formal requirements
- Requirements are classified as:
  - **Functional Requirements (FR)**: What the system must DO (e.g., "Users can log in")
  - **Non-Functional Requirements (NFR)**: How the system must PERFORM (e.g., "Page load < 2 seconds")
- Requirements are prioritized using **MoSCoW method**:
  - **Must Have**: Critical for go-live
  - **Should Have**: Important but not blocking
  - **Could Have**: Nice to have
  - **Won't Have**: Deferred to later phases
- Each requirement gets a unique ID (FR-001, NFR-001) for **traceability**

**Our automation:** Agent 02 (Requirement Agent) does this.

**Key terms:**
- **FR / NFR**: Functional / Non-Functional Requirements
- **MoSCoW**: Prioritization method (Must/Should/Could/Won't)
- **Traceability**: Ability to track a feature from client request → requirement → code → test

---

### Phase 3: Documentation & SOW
**What happens:**
- The BA/PM creates formal documents for client sign-off:
  - **BRD (Business Requirements Document)**: High-level, non-technical, for C-suite
  - **FRD (Functional Requirements Document)**: Detailed technical specs for dev team
  - **SOW (Statement of Work)**: Legal/contractual document defining scope, deliverables, timeline, cost
- Client reviews and approves the SOW before development starts
- This is the **contract** between the IT company and the client

**Our automation:** Agent 03 (Documentation Agent) generates BRD, FRD, and SOW.

**Key terms:**
- **BRD**: Business Requirements Document — for executives
- **FRD**: Functional Requirements Document — for developers
- **SOW**: Statement of Work — the contract defining what will be built, when, and for how much
- **Sign-off**: Client's formal approval to proceed

---

### Phase 4: Sprint Planning (Agile/Scrum)
**What happens:**
- The **Project Manager (PM)** creates a sprint plan using **Agile methodology**
- Work is divided into **Sprints** (typically 2-week iterations)
- Each sprint has specific goals and deliverables
- Team composition is determined:
  - **Backend Developers**: Build the server-side logic, APIs, database
  - **Frontend Developers**: Build the user interface (UI)
  - **QA Engineers**: Test the software
  - **UI/UX Designer**: Design the user interface and experience
  - **Project Manager**: Manages timeline, resources, risks
  - **Business Analyst**: Bridges client needs and technical implementation
  - **DevOps Engineer**: Handles deployment, CI/CD, infrastructure
  - **Scrum Master**: Facilitates Agile ceremonies, removes blockers

**Our automation:** Agent 04 (Planning Agent) creates the sprint plan.

**Key terms:**
- **Sprint**: A fixed-duration work period (usually 2 weeks)
- **Sprint 0**: Setup sprint — environment setup, architecture, CI/CD baseline
- **Agile/Scrum**: Iterative development methodology
- **Capacity Planning**: Ensuring the team isn't overloaded
- **Velocity**: How much work a team can complete per sprint

---

### Phase 5: Ticket Creation (Jira/ServiceNow)
**What happens:**
- The PM/Scrum Master creates tickets in a **ticketing tool** (Jira, ServiceNow, Azure DevOps, Linear)
- Ticket hierarchy:
  - **Epic**: A large body of work (maps to a module, e.g., "User Authentication")
  - **User Story**: A feature from the user's perspective ("As a user, I want to log in so that I can access my dashboard")
  - **Task**: Technical work item ("Implement JWT authentication middleware")
  - **Bug**: A defect found during testing
  - **Sub-task**: A smaller piece of a task
- Each story has:
  - **Acceptance Criteria**: Conditions that must be met (Given/When/Then format)
  - **Story Points**: Complexity estimate (Fibonacci: 1, 2, 3, 5, 8, 13)
  - **Sprint assignment**: Which sprint it belongs to
  - **Assignee**: The developer/tester responsible

**Our automation:** Agent 05 (Jira Agent) creates Epics, Stories, and Tasks.

**Key terms:**
- **Epic → Story → Task**: The ticket hierarchy
- **Story Points**: Relative complexity (not time) — 8 is roughly 4x harder than 2
- **Acceptance Criteria**: "How do we know this is done?"
- **Sprint Backlog**: Stories selected for a specific sprint
- **Product Backlog**: All stories waiting to be worked on

---

### Phase 6: Architecture & Design
**What happens:**
- The **Solution Architect** designs the technical architecture:
  - **Tech Stack**: What technologies to use (React, Node.js, PostgreSQL, etc.)
  - **Architecture Pattern**: Monolith vs Microservices vs Modular Monolith
  - **Database Schema**: Table structure, relationships, indexes
  - **API Design**: REST endpoints, request/response formats
  - **Security Architecture**: Authentication, authorization, encryption
- Produces:
  - **HLD (High-Level Design)**: System overview, service interactions
  - **LLD (Low-Level Design)**: Detailed component design (optional)

**Our automation:** Agent 06 (Architecture Agent) designs the full system.

**Key terms:**
- **Tech Stack**: The combination of technologies used
- **HLD/LLD**: High-Level Design / Low-Level Design documents
- **API Contract**: Formal definition of an API endpoint
- **Database Schema**: Structure of database tables and relationships
- **Microservices**: Architecture where each service runs independently
- **Monolith**: Single application containing all functionality

---

### Phase 7: Development (Coding)
**What happens:**
- Developers work on assigned tasks from Jira
- Code is organized by module and pushed to a **Git repository** (GitHub, GitLab, Bitbucket)
- Teams involved:
  - **Backend team**: APIs, business logic, database queries
  - **Frontend team**: UI components, state management, routing
- **Code reviews** are done via **Pull Requests (PRs)**
- **Branching strategy**: feature branches → develop → staging → main/production
- **CI (Continuous Integration)**: Automated builds and tests on every push

**Our automation:** Agent 07 (Code Agent) generates production-ready scaffolding.

**Key terms:**
- **Git Repository**: Version-controlled code storage
- **Pull Request (PR)**: Request to merge code changes, reviewed by peers
- **Branch**: An isolated copy of code for a specific feature
- **CI/CD**: Continuous Integration / Continuous Deployment
- **Code Review**: Peer review of code changes before merging

---

### Phase 8: Testing / QA
**What happens:**
- The **QA team** tests the software:
  - **Unit Testing**: Testing individual functions (done by developers)
  - **Integration Testing**: Testing how components work together
  - **E2E Testing**: Testing complete user journeys (login → action → logout)
  - **Security Testing**: Checking for vulnerabilities (SQL injection, XSS, etc.)
  - **Performance Testing**: Load testing, stress testing
  - **UAT (User Acceptance Testing)**: Client tests the system
- Bugs are logged as Jira tickets and assigned back to developers
- **Test environments**:
  - **DEV**: Developer's local or shared dev environment
  - **QA/TEST**: Dedicated testing environment
  - **STAGING**: Pre-production mirror of production
  - **PRODUCTION (PROD)**: Live environment for real users

**Our automation:** Agent 08 (Testing Agent) creates test plans, test cases, and security checklists.

**Key terms:**
- **QA**: Quality Assurance team
- **UAT**: User Acceptance Testing — client tests before go-live
- **Test Case**: Step-by-step instructions to verify a feature works
- **Bug/Defect**: Something that doesn't work as expected
- **Regression Testing**: Ensuring new code doesn't break existing features
- **Environment**: DEV → QA → STAGING → PROD

---

### Phase 9: Deployment
**What happens:**
- The **DevOps team** handles deployment:
  - **Containerization**: Packaging the app in Docker containers
  - **CI/CD Pipeline**: Automated build → test → deploy workflow
  - **Infrastructure as Code (IaC)**: Server setup defined in code (Terraform, CloudFormation)
  - **Cloud hosting**: AWS, Azure, GCP, or on-premise servers
- **Deployment flow**: Code merged to main → CI/CD builds → deploys to staging → manual approval → deploys to production
- **Production Readiness Checklist**: SSL, monitoring, backups, logging, etc.

**Our automation:** Agent 09 (Deployment Agent) creates Dockerfiles, docker-compose, CI/CD configs, and production checklist.

**Key terms:**
- **Docker**: Container platform for packaging applications
- **CI/CD Pipeline**: Automated workflow from code commit to deployment
- **Staging**: Environment identical to production for final testing
- **Production**: Live environment serving real users
- **Rollback**: Reverting to a previous working version if deployment fails
- **Blue-Green Deployment**: Running two identical production environments for zero-downtime deploys

---

### Phase 10: Project Delivery & Handoff
**What happens:**
- **Project Summary** is created with all artifacts
- **Client demo** of the working system
- **Knowledge transfer**: Documentation, training materials
- **Go-live**: System is made available to real users
- **Post-launch support**: Bug fixes, monitoring, iteration

**Our automation:** Agent 10 (Summary Agent) creates the final project summary and executive dashboard.

---

## Teams Involved in a Real IT Project

| Team | Role | Members |
|------|------|---------|
| **Sales Team** | Client relationship, initial requirements | Sales Lead, Account Manager |
| **Business Analysis** | Requirements gathering, documentation | Business Analyst(s) |
| **Project Management** | Planning, tracking, risk management | Project Manager, Scrum Master |
| **Architecture** | Technical design, tech stack decisions | Solution Architect |
| **Backend Development** | Server-side code, APIs, databases | Backend Developers (2-4) |
| **Frontend Development** | User interface, client-side code | Frontend Developers (1-3) |
| **UI/UX Design** | Visual design, user experience | UI/UX Designer(s) |
| **Quality Assurance** | Testing, bug reporting | QA Engineers (1-3) |
| **DevOps** | Deployment, infrastructure, CI/CD | DevOps Engineer(s) |
| **Management** | Budget, resource allocation, approvals | Delivery Manager, VP Engineering |

---

## How Claude Code Agent Teams Maps to This

With **Claude Code Agent Teams**, each team above becomes a **teammate**:

```
Team Lead (Orchestrator)
├── Teammate: "Business Analyst" — Agents 01-03
├── Teammate: "Project Manager" — Agents 04-05
├── Teammate: "Tech Lead" — Agents 06-07
└── Teammate: "QA & DevOps" — Agents 08-10
```

Each teammate is a **separate Claude Code instance** with its own context.
They communicate through the **shared task list** and **JSON contract files**.
The Team Lead coordinates and synthesizes results.

This mirrors real IT companies where teams work in parallel and coordinate
through meetings, Jira boards, and shared documents.

---

## Environments in Real Projects

```
Developer's Machine → DEV Server → QA/TEST → STAGING → PRODUCTION
     (coding)          (integration)  (testing)  (pre-prod)  (live)
```

| Environment | Purpose | Who Uses It |
|-------------|---------|-------------|
| **DEV** | Active development, frequent changes | Developers |
| **QA/TEST** | Dedicated testing | QA Engineers |
| **STAGING** | Mirror of production, final validation | QA, PM, Client (UAT) |
| **PRODUCTION** | Live system, real users | End users |

---

## The Complete Flow in One Picture

```
Client Call → Transcript → Requirements → BRD/FRD/SOW → Sprint Plan
     ↓             ↓            ↓              ↓              ↓
  (Sales)    (Agent 01)   (Agent 02)     (Agent 03)     (Agent 04)

→ Jira Tickets → Architecture → Code → Testing → Deployment → Summary
       ↓              ↓           ↓        ↓          ↓           ↓
  (Agent 05)     (Agent 06)  (Agent 07) (Agent 08) (Agent 09) (Agent 10)
```
