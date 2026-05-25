# Changelog

All notable changes to the SDLC Automation Platform are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.1.2] — 2026-05-25

### Added
- **CHANGELOG.md bundled inside plugin** — users who install the plugin can now
  read the full version history directly from `plugins/sdlc-automation/CHANGELOG.md`
  without visiting GitHub.

### Changed
- **Plugin README rewritten for clarity** — now leads with Install → Setup →
  Quick start → Update as a clear lifecycle, with `/sdlc-setup` and `/sdlc-update`
  prominently featured. Command tables reorganised into Lifecycle, Pipeline control,
  and Individual agent sections.

---

## [3.1.0] — 2026-05-25

### Added
- **`/sdlc-update` command** — one command to update the plugin to the latest
  version from GitHub. Pulls fresh marketplace cache, reinstalls plugin, and
  copies updated helpers + scripts into the current project. Backs up
  `sdlc-pipeline.yml` if you have local edits before overwriting.
- **`/sdlc-setup` command** — bootstraps a new project from the plugin install.
  Copies `helpers/`, `scripts/`, `sdlc-pipeline.yml`, creates `inputs/` and all
  `outputs/` directories. Run once after installing the plugin in any new project.
- **GitHub Action: auto-stamp SHA** — `.github/workflows/update-marketplace-sha.yml`
  fires on every push to `main`, stamps the latest commit SHA into
  `.claude-plugin/marketplace.json`, and bumps the plugin patch version.
  Ensures `claude plugin marketplace update` always fetches the exact latest commit.
- **Path-resolver in all orchestrator commands** — `/sdlc-parallel`,
  `/sdlc-sequential`, `/sdlc-status`, `/sdlc-resume`, `/sdlc-agent` now find
  `scripts/orchestrator.py` whether it is in the local project (after `/sdlc-setup`)
  or inside the plugin install directory. No longer silently fails on fresh installs.

### Fixed
- **Bug: optional agent toggles ignored** — `_parse_optional_toggles()` in
  `scripts/orchestrator.py` used the stripped line to detect block boundaries,
  so it exited on the first indented key and always returned defaults.
  Fixed to use the raw line for indentation detection.
- **Bug: Slack/Teams webhooks never parsed** — `load_notification_config()` in
  `.claude/hooks/notification_dispatcher.py` exited the `notifications:` block
  when it saw `channels:`, so `webhook_url` values were never read.
  Fixed with an indentation-aware state machine that tracks the active channel.
- **Contract version mismatch** — `_COMMUNICATION_PROTOCOL.md` documented
  version `"1.1"` but all agents and validators used `"1.0"`. Corrected to `"1.0"`.
- **Hooks never fired** — `.claude/settings.json` had no `hooks` block, so all
  hook scripts (security gate, contract validator, notifications) were dead code.
  Wired up `PreToolUse`, `PostToolUse`, and `SessionEnd` hooks.
- **Plugin zip blocked validation** — `claude plugin validate` cannot read a zip
  directly. Rebuilt plugin distribution to validate against the extracted directory.

### Changed
- **Plugin version bumped 3.0.0 → 3.1.0**
- **README restored to full 941 lines** — previous rewrite accidentally dropped
  the directory structure, agent inventory, hooks catalog, skills table,
  specialist agents, sample transcripts, configuration, and more. All sections
  restored and updated with v3.x content.
- **`.gitignore` hardened** — output directories ignored by content (`dir/*`
  not `dir/`), `.gitkeep` placeholders tracked, plugin zips excluded,
  `.bak`/`.tmp` excluded. `git status` now clean after every run.

---

## [3.0.0] — 2026-05-25

### Added
- **Shift-left security** — Agent 12 (Security Threat Model) now runs between
  Architecture and Code. STRIDE + OWASP Top 10 analysis happens before a single
  line is written. Enabled in `sdlc-pipeline.yml` by default.
- **Real-time notifications** — `notification_dispatcher.py` hook fires on every
  agent completion. Posts to Slack, MS Teams, or macOS desktop. Configurable
  via `sdlc-pipeline.yml notifications:` block.
- **Cost estimation enabled by default** — Agent 14 (Cost Estimation) now runs
  in `phase_9_delivery` without needing manual opt-in. Stakeholders get an
  AWS/Azure/GCP cost forecast at the end of every pipeline run.
- **Self-healing test loop** — Agent 08 (Testing) now retries Agent 07 (Code)
  automatically when tests fail. Up to 3 retries with `failed_tests.json`
  listing each failure and suggested fix. Escalates to user after max retries.
- **Live deployment** — Agent 09 (Deployment) optionally runs
  `docker compose up -d` + health check. Writes `live_staging_url` to the
  deployment contract on success.
- **DAG Orchestrator** — `scripts/orchestrator.py` runs agents as isolated
  `claude -p` subprocesses. Each agent gets a fresh 200K context window.
  Supports `--mode parallel`, `--mode sequential`, `--status`, `--resume-from`,
  `--mode single`. No more context accumulation or mid-pipeline compaction.
- **Agent lifecycle harness** — `helpers/harness.py` wraps every agent with
  `pre_agent()` (input validation), `post_agent()` (contract validation + notify),
  and `phase_boundary()` (cross-phase consistency check).
- **Plugin v3.0 — GitHub marketplace** — `plugins/sdlc-automation/` restructures
  the repo as a Claude Code plugin marketplace. Install with one command:
  ```
  claude plugin marketplace add richard-devbot/claude_code_sdlc_automation
  claude plugin install sdlc-automation@claude_code_sdlc_automation
  ```
- **22 `/sdlc-*` slash commands** — full pipeline control and individual agent
  triggers available in any Claude Code session after plugin install.
- **`/sdlc-parallel` and `/sdlc-sequential`** — run the orchestrator directly
  from Claude Code without opening a terminal.
- **`AGENT_SKILL_MAP.md`** — canonical agent→skill routing table so agents
  invoke the right skills rather than reasoning from scratch.
- **`_ISOLATED_MODE.md`** — rules for agents running as orchestrator subprocesses
  (do not call Task tool; orchestrator manages sequencing).

### Changed
- `sdlc-pipeline.yml` extended with `testing_retry_loop`, `live_deployment`,
  `notifications` (with Slack/Teams/desktop support), and updated `optional_agents`
  defaults (security + cost now `true`).
- `scripts/run_pipeline.sh` updated from a simple pre-flight check to an
  interactive mode chooser (parallel / sequential / interactive / status).
- All 15 agent `.md` files updated with YAML frontmatter for plugin compatibility.

---

## [2.0.0] — 2026-05-22

### Added
- 15 cooperating agents (11 core SDLC + 4 optional)
- 42 specialist sub-agents across 7 disciplines
- 93 skills imported from 14 source domains
- 26 quality gate hooks (security, devops, code quality)
- 22 slash commands for common SDLC workflows
- DAG-based parallel execution via `sdlc-pipeline.yml`
- Domain-agnostic design with auto-detection for 13+ industries
- Interactive decision framework (interactive / express / replay modes)
- Multi-transcript merger support
- Tool fallback strategy (Jira → files, Docker → scripts, etc.)
- 5 domain-specific sample transcripts (healthcare, fintech, e-commerce,
  education, SaaS)
- `helpers/pipeline_status.py`, `contract_validator.py`, `output_reporter.py`,
  `pipeline_analytics.py`
- Visual architecture showcase (`case-study.html`, `diagrams.html`)

---

## [1.0.0] — 2026-05-21

### Added
- Initial pipeline structure with 10 core agents
- JSON contract communication protocol
- Basic environment setup, transcript parsing, requirements, documentation,
  planning, ticketing, architecture, code generation, testing, deployment,
  and summary agents
- `inputs/transcript.txt` as pipeline entry point
- `outputs/` directory structure
