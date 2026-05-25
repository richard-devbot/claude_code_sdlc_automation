---
allowed-tools: Bash, Read
description: "Resume SDLC pipeline from a specific agent"
argument-hint: <agent-name-or-number>
---

# SDLC Pipeline — Resume

Resume the pipeline starting from the specified agent.
All agents before it are assumed to have completed (their JSON contracts exist).

!`python3 scripts/orchestrator.py --resume-from $ARGUMENTS`

---

## Examples

```
/sdlc-resume code_agent
/sdlc-resume 07_code_agent
/sdlc-resume deployment_agent
```

## Manual resume (web fallback)

If shell commands are not available, read the agent file directly:

"Resume the SDLC pipeline from [agent].
Read outputs/[previous_output].json and execute .claude/agents/[NN_agent].md"

## Agent reference

| # | Agent ID | Resume from |
|---|----------|-------------|
| 00 | environment_agent | `/sdlc-resume environment_agent` |
| 01 | transcript_agent | `/sdlc-resume transcript_agent` |
| 02 | requirement_agent | `/sdlc-resume requirement_agent` |
| 03 | documentation_agent | `/sdlc-resume documentation_agent` |
| 04 | planning_agent | `/sdlc-resume planning_agent` |
| 05 | jira_agent | `/sdlc-resume jira_agent` |
| 06 | architecture_agent | `/sdlc-resume architecture_agent` |
| 12 | security_threat_model_agent | `/sdlc-resume security_threat_model_agent` |
| 07 | code_agent | `/sdlc-resume code_agent` |
| 08 | testing_agent | `/sdlc-resume testing_agent` |
| 13 | compliance_checker_agent | `/sdlc-resume compliance_checker_agent` |
| 09 | deployment_agent | `/sdlc-resume deployment_agent` |
| 14 | cost_estimation_agent | `/sdlc-resume cost_estimation_agent` |
| 10 | summary_agent | `/sdlc-resume summary_agent` |
| 11 | feedback_loop_agent | `/sdlc-resume feedback_loop_agent` |
