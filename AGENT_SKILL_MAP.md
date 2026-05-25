# Agent → Skill & Specialist Map

This is the canonical reference for which skills and specialist sub-agents each
pipeline agent should invoke. Every agent file references this map in its
"Required Skills & Specialists" section.

## Why this matters
The repo carries 121 skills + 42 specialists. Without an explicit map, agents
default to reasoning from their own prompt and ignore the library. This map
turns the pipeline from "agents doing it themselves" into "agents orchestrating
a deep skill library" — which is what makes the output production-grade.

## How to use this map (rule for every agent)
1. Before starting your tasks, read the row for your agent below.
2. For each listed skill: invoke it via the Skill tool (or `Read` its
   `SKILL.md` if the Skill tool is not available) BEFORE you generate output.
3. For each listed specialist: invoke it via the Task tool with a focused
   sub-prompt. Capture its output and merge into your contract.
4. Record the skills & specialists you actually used in your output contract
   under `skills_invoked` and `specialists_invoked` arrays.

## Pipeline Mechanics Skills (every agent reads these)
- `.claude/skills/pipeline/contract_protocol.md` — JSON contract standards
- `.claude/skills/pipeline/agent_chain.md` — how to trigger the next agent
- `.claude/skills/pipeline/interactive_decision_framework.md` — when to ask the user
- `.claude/skills/pipeline/tool_registry.md` — fallback strategy
- `.claude/skills/pipeline/notification_system.md` — progress notifications

## Per-Agent Map

### 00 Environment Agent
- Skills: `automation/bash-linux`, `automation/bash-scripting`, `pipeline/tool_registry`
- Specialists: none (this is setup)

### 01 Transcript Agent
- Skills: `requirements-planning/jobs-to-be-done`, `internal-comms`, `doc-coauthoring`
- Specialists: none

### 02 Requirement Agent
- Skills: `sdlc-process/requirement_analysis.md`,
  `requirements-planning/agile-product-owner`,
  `requirements-planning/backlog-grooming-assistant`,
  `domain-adaptation/domain_rules.md`
- Specialists: `project-management/cs-product-manager`,
  `project-management/cs-agile-product-owner`

### 03 Documentation Agent
- Skills: `docx`, `pdf`, `pptx`,
  `documentation-writing/crafting-effective-readmes`,
  `documentation-writing/mermaid-diagram-specialist`,
  `documentation-writing/documentation-templates`,
  `sdlc-process/documentation_standards.md`
- Specialists: `documentation/technical-writer`,
  `documentation/se-technical-writer`,
  `documentation/diagram-architect`

### 04 Planning Agent
- Skills: `sdlc-process/sprint_planning.md`,
  `requirements-planning/sprint-planner`,
  `requirements-planning/scrum-master`,
  `requirements-planning/roadmap-communicator`,
  `requirements-planning/okr-tracker-creator`
- Specialists: `project-management/scrum-master`,
  `project-management/cs-project-manager`,
  `project-management/product-sprint-prioritizer`

### 05 Jira Agent
- Skills: `requirements-planning/jira`,
  `requirements-planning/jira-expert`
- Specialists: `project-management/atlassian-requirements-to-jira`

### 06 Architecture Agent
- Skills: `sdlc-process/architecture_patterns.md`,
  `architecture-design/api-design`,
  `architecture-design/api-design-principles`,
  `architecture-design/database-architecture`,
  `architecture-design/backend-patterns`,
  `documentation-writing/architecture-doc-creator`,
  `documentation-writing/mermaid-diagrams`
- Specialists: `architecture/backend-architect`,
  `architecture/database-architect`,
  `architecture/api-architect`,
  `devops/cloud-architect`

### 07 Code Agent
- Skills: choose stack-appropriate ones from `code-patterns/`
  (e.g., `django-patterns`, `fastapi-router-creator`, `express-route-generator`,
  `flask-blueprint-creator`, `go-handler-generator`, `laravel-patterns`,
  `angular`),
  `code-patterns/cc-skill-coding-standards`
- Specialists: `architecture/code-architect`,
  `architecture/api-builder`,
  `architecture/database-designer`,
  `devops/build-engineer`

### 08 Testing Agent
- Skills: `sdlc-process/testing_strategy.md`,
  `testing-qa/api-test-suite-builder`,
  `testing-qa/api-test-generator`,
  `testing-qa/analyzing-test-coverage`,
  `testing-qa/ai-regression-testing`,
  `webapp-testing`,
  `playwright-e2e-testing`
- Specialists: `testing/e2e-runner`,
  `testing/codebase-pattern-finder`,
  `testing/error-detective`,
  `testing/cs-quality-regulatory`

### 09 Deployment Agent
- Skills: `devops-deployment/argocd-app-deployer`,
  `devops-deployment/ansible-playbook-creator`,
  `devops-deployment/auto-scaling-configurator`,
  `devops-deployment/aws-serverless`,
  `devops-deployment/aws-solution-architect`,
  `devops-deployment/architecture-decision-records`,
  `devops-deployment/appdeploy`
- Specialists: `devops/build-engineer`,
  `devops/cloud-architect`,
  `performance/devops-troubleshooter`

### 10 Summary Agent
- Skills: `pptx`, `xlsx`, `pdf`, `theme-factory`,
  `documentation-writing/crafting-effective-readmes`,
  `web-artifacts-builder`
- Specialists: `documentation/changelog-generator`

### 11 Feedback Loop Agent
- Skills: `internal-comms`, `doc-coauthoring`
- Specialists: none

### 12 Security Threat Model Agent
- Skills: `security-compliance/attack-surface-analyzer`,
  `security-compliance/auth-implementation-patterns`,
  `security-compliance/broken-authentication`,
  `security-compliance/cc-skill-security-review`,
  `security-compliance/api-security-best-practices`
- Specialists: `security/engineering-security-engineer`,
  `security/api-security-audit`,
  `security/engineering-code-reviewer`

### 13 Compliance Checker Agent
- Skills: `security-compliance/auditing-access-control`,
  `security-compliance/api-key-auth-setup`,
  `security-compliance/api-security-best-practices`
- Specialists: `security/compliance-auditor`,
  `security/compliance-specialist`

### 14 Cost Estimation Agent
- Skills: `devops-deployment/aws-cost-optimizer`,
  `performance-monitoring/cost-optimization`,
  `xlsx` (for cost spreadsheets)
- Specialists: none

## Contract additions
Every agent's output JSON must now include:
```json
"skills_invoked": ["skill-id-1", "skill-id-2"],
"specialists_invoked": ["specialist-name-1"]
```
This makes skill usage auditable and traceable across the pipeline.
