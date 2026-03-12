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

The final agent sets `pipeline_complete: true` instead of next_agent.

## Contract Chain (11 Agents)

| # | Agent | Reads | Writes |
|---|-------|-------|--------|
| 00 | Environment | System scan | `outputs/environment_report.json` |
| 01 | Transcript | `inputs/transcript.txt` | `outputs/transcripts/structured_meeting_output.json` |
| 02 | Requirement | transcript output | `outputs/requirements/requirement_spec.json` |
| 03 | Documentation | requirement spec | `outputs/documents/documentation_output.json` |
| 04 | Planning | documentation + requirements | `outputs/planning/sprint_plan.json` |
| 05 | Jira | sprint plan + requirements | `outputs/jira/jira_tickets.json` |
| 06 | Architecture | jira tickets + requirements | `outputs/architecture/system_design.json` |
| 07 | Code | system design + HLD | `outputs/code/code_output.json` |
| 08 | Testing | code output + jira + requirements | `outputs/qa/qa_results.json` |
| 09 | Deployment | qa results + architecture + code | `outputs/deployment/deployment_output.json` |
| 10 | Summary | ALL contracts | `outputs/pipeline_final.json` |

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
