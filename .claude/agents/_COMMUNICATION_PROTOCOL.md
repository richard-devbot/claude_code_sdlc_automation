# Agent Communication Protocol — SDLC Automation Pipeline

## Communication Model: JSON Contract Chain

```
Agent A completes work
    → Writes output JSON contract to outputs/ directory
    → Calls Task tool to invoke Agent B
        → Agent B reads input JSON contract
        → Agent B performs its work
        → Agent B writes its output JSON contract
        → Agent B calls Task tool to invoke Agent C
            → ... continues until final agent
```

## Contract Standard Fields

Every JSON contract MUST include:

| Field | Type | Description |
|-------|------|-------------|
| `contract_version` | string | Always "1.0" |
| `produced_by` | string | Agent identifier (e.g., "transcript_agent") |
| `timestamp` | string | ISO 8601 timestamp |
| `next_agent` | string | Name of the next agent to invoke |
| `next_input_file` | string | Path to this contract |
| `user_preferences` | object | (Optional) User choices made during interactive decisions |

The final agent sets `pipeline_complete: true` instead of next_agent.

## User Preferences Field

When an agent presents options to the user and receives a choice, it records
the decision in the `user_preferences` object. Downstream agents MUST check
this field from ALL previous contracts before presenting redundant options.

```json
"user_preferences": {
  "ticketing_platform": "jira_cloud",
  "ticketing_credentials_provided": true,
  "database_engine": "postgresql",
  "deployment_platform": "docker_compose",
  "ci_cd_platform": "github_actions",
  "cloud_provider": "aws",
  "install_tools_when_missing": true
}
```

If a user chose "Jira Cloud" in Agent 05, Agent 10 should reference that
choice — not re-ask. Preferences propagate forward through the chain.

## Contract Chain (15 Agents — 11 core + 4 optional)

| # | Agent | Reads | Writes | Optional |
|---|-------|-------|--------|----------|
| 00 | Environment | System scan | `outputs/environment_report.json` | No |
| 01 | Transcript | `inputs/transcript.txt` | `outputs/transcripts/structured_meeting_output.json` | No |
| 02 | Requirement | transcript output | `outputs/requirements/requirement_spec.json` | No |
| 03 | Documentation | requirement spec | `outputs/documents/documentation_output.json` | No |
| 04 | Planning | documentation + requirements | `outputs/planning/sprint_plan.json` | No |
| 05 | Jira | sprint plan + requirements | `outputs/jira/jira_tickets.json` | No |
| 06 | Architecture | jira tickets + requirements | `outputs/architecture/system_design.json` | No |
| 12 | Security Threat Model | system design + requirements | `outputs/security/threat_model.json` | Yes |
| 07 | Code | system design + threat model (if run) | `outputs/code/code_output.json` | No |
| 08 | Testing | code output + jira + requirements | `outputs/qa/qa_results.json` | No |
| 13 | Compliance Checker | all contracts | `outputs/compliance/compliance_matrix.json` | Yes (auto for regulated domains) |
| 09 | Deployment | qa results + architecture + code | `outputs/deployment/deployment_output.json` | No |
| 10 | Summary | ALL contracts | `outputs/pipeline_final.json` | No |
| 14 | Cost Estimation | system design + sprint plan | `outputs/cost/cost_estimation.json` | Yes |
| 11 | Feedback Loop | ALL contracts | `outputs/feedback/consistency_report.json` | Yes |

> Optional agents are enabled/disabled in `sdlc-pipeline.yml` under `optional_agents`.
> Their output directories (`outputs/security/`, `outputs/compliance/`, `outputs/cost/`,
> `outputs/feedback/`) are created by `scripts/run_pipeline.sh` regardless of toggle state.

## Handoff Rules
1. Never stop early — trigger the next agent
2. Always write before handing off
3. Pass the exact file path to the next agent
4. Use the Task tool for handoff

## Error Recovery
Resume from any agent by providing the correct input path.

## Domain Agnosticism
All contracts carry a `domain` field propagated from Agent 01.
Downstream agents use this to apply domain-specific rules automatically.
