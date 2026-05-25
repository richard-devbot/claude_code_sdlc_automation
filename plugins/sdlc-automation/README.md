# sdlc-automation — Claude Code Plugin v3.1

End-to-end SDLC automation pipeline. Drop in a single client meeting transcript
and 15 cooperating agents produce:

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
claude plugin marketplace add richard-devbot/claude_code_sdlc_automation && \
claude plugin install sdlc-automation@claude_code_sdlc_automation
```

---

## First-time setup (run once per project)

```
/sdlc-setup
```

Copies `helpers/`, `scripts/`, and `sdlc-pipeline.yml` from the plugin install
into your current project, and creates the `inputs/` + `outputs/` directory structure.

---

## Quick start

1. Add your transcript to `inputs/transcript.txt`
2. Run `/sdlc-start`
3. When complete, open `outputs/PROJECT_COMPLETE_SUMMARY.md`

---

## Staying up to date

```
/sdlc-update
```

Pulls the latest version from GitHub, reinstalls the plugin, and refreshes
helpers and scripts in your project. Restart Claude Code to apply.

---

## Commands

### Lifecycle

| Command | Description |
|---------|-------------|
| `/sdlc-setup` | Bootstrap this project — copies helpers, scripts, config |
| `/sdlc-update` | Update plugin to latest version from GitHub |

### Pipeline control

| Command | Description |
|---------|-------------|
| `/sdlc-start` | Start full pipeline (interactive, agents chain autonomously) |
| `/sdlc-parallel` | Parallel DAG mode — each agent gets a fresh 200K context window |
| `/sdlc-sequential` | Sequential mode — one agent at a time, easiest to debug |
| `/sdlc-status` | Show which agents completed `[OK]` vs pending `[  ]` |
| `/sdlc-resume <agent>` | Resume pipeline from any agent after a failure |
| `/sdlc-agent <agent>` | Run exactly one agent in isolation |
| `/sdlc-clean` | Remove all outputs for a fresh run |

### Individual agent triggers

| Command | Agent | Role |
|---------|-------|------|
| `/sdlc-env` | 00 Environment | System scan + tool detection |
| `/sdlc-transcript` | 01 Transcript | Parse meeting → structured JSON |
| `/sdlc-requirements` | 02 Requirements | FRs + NFRs with traceability |
| `/sdlc-docs` | 03 Documentation | BRD, FRD, SOW |
| `/sdlc-planning` | 04 Planning | Sprint plan + timeline |
| `/sdlc-tickets` | 05 Ticketing | Jira/GitHub epics + stories |
| `/sdlc-architecture` | 06 Architecture | System design + API contracts |
| `/sdlc-security` | 12 Security *(opt)* | STRIDE + OWASP threat model |
| `/sdlc-code` | 07 Code | Production scaffolding |
| `/sdlc-testing` | 08 Testing | Test plan + self-healing loop |
| `/sdlc-compliance` | 13 Compliance *(opt)* | HIPAA/GDPR/PCI gap analysis |
| `/sdlc-deploy` | 09 Deployment | Docker + CI/CD + IaC |
| `/sdlc-cost` | 14 Cost *(opt)* | Cloud cost forecast |
| `/sdlc-summary` | 10 Summary | Executive dashboard |
| `/sdlc-feedback` | 11 Feedback *(opt)* | Consistency review + remediation |

---

## Supported domains

Healthcare · Fintech · E-Commerce · Education · HR Tech · Logistics · SaaS ·
Government · Real Estate · Manufacturing · Legal · Media · Travel · Agriculture

Domain intelligence is detected automatically from your transcript.

---

## Notifications (optional)

Edit `sdlc-pipeline.yml` in your project:

```yaml
notifications:
  enabled: true
  channels:
    slack:
      webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    teams:
      webhook_url: "https://outlook.office.com/webhook/YOUR/URL"
```

Falls back to macOS desktop notification if no webhook configured.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for full version history.
