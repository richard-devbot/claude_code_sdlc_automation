# sdlc-automation

End-to-end SDLC automation pipeline for Claude Code and Claude Desktop.

Drop in a single client meeting transcript — 15 cooperating agents produce:

- Requirements (BRD, FRD, SOW)
- Sprint plan + Jira/GitHub tickets  
- System architecture + API contracts
- Production-ready code scaffolding
- Test plans + self-healing auto-fix loop
- Security threat model (STRIDE/OWASP)
- Compliance matrix (HIPAA, GDPR, PCI-DSS, SOC 2)
- Deployment configs (Docker, CI/CD, IaC)
- Cloud cost forecast
- Executive dashboard

Works in **Claude.ai web**, **Claude Desktop**, and **Claude Code CLI**.

---

## Install (one command)

```bash
claude plugin marketplace add richard-devbot/claude_code_sdlc_automation --sparse plugins && claude plugin install sdlc-automation@claude_code_sdlc_automation
```

---

## Quick Start

1. Place your meeting transcript in `inputs/transcript.txt`
2. Type `/sdlc-start` in Claude Code

---

## Commands

| Command | Description |
|---------|-------------|
| `/sdlc-start` | Start full pipeline (interactive) |
| `/sdlc-parallel` | Run in parallel DAG mode |
| `/sdlc-sequential` | Run sequentially |
| `/sdlc-status` | Show agent completion status |
| `/sdlc-resume <agent>` | Resume from any agent |
| `/sdlc-agent <agent>` | Run one agent in isolation |
| `/sdlc-env` | Agent 00 — environment setup |
| `/sdlc-transcript` | Agent 01 — transcript analysis |
| `/sdlc-requirements` | Agent 02 — requirements |
| `/sdlc-docs` | Agent 03 — documentation |
| `/sdlc-planning` | Agent 04 — sprint planning |
| `/sdlc-tickets` | Agent 05 — Jira tickets |
| `/sdlc-architecture` | Agent 06 — system design |
| `/sdlc-security` | Agent 12 — threat model *(optional)* |
| `/sdlc-code` | Agent 07 — code generation |
| `/sdlc-testing` | Agent 08 — QA + auto-fix loop |
| `/sdlc-compliance` | Agent 13 — compliance *(optional)* |
| `/sdlc-deploy` | Agent 09 — deployment |
| `/sdlc-cost` | Agent 14 — cost estimation *(optional)* |
| `/sdlc-summary` | Agent 10 — executive dashboard |
| `/sdlc-feedback` | Agent 11 — consistency review *(optional)* |

---

## Supported Domains

Healthcare · Fintech · E-Commerce · Education · HR Tech · Logistics · SaaS ·
Government · Real Estate · Manufacturing · Legal · Media · Travel · Agriculture

Domain intelligence flows automatically from the transcript through JSON contracts.
