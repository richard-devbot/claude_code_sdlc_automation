# SDLC Automation — Agent Teams Mode

## What is Agent Teams Mode?

Instead of running agents sequentially (peer-to-peer chain), Agent Teams mode
uses Claude Code's **experimental Agent Teams feature** to run multiple agents
in parallel where possible. One session acts as the **Team Lead**, coordinating
work, spawning teammates, and synthesizing results.

## Prerequisites
Agent Teams must be enabled in settings.json:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```
This is already configured in this project's `.claude/settings.json`.

## How It Works

### Team Structure
```
Team Lead (You / Orchestrator)
├── Teammate 1: Business Analysis Team
│   ├── Transcript Agent (Agent 01)
│   ├── Requirement Agent (Agent 02)
│   └── Documentation Agent (Agent 03)
│
├── Teammate 2: Project Planning Team
│   ├── Planning Agent (Agent 04)
│   └── Jira Agent (Agent 05)
│
├── Teammate 3: Technical Team
│   ├── Architecture Agent (Agent 06)
│   └── Code Agent (Agent 07)
│
└── Teammate 4: Quality & Delivery Team
    ├── Testing Agent (Agent 08)
    ├── Deployment Agent (Agent 09)
    └── Summary Agent (Agent 10)
```

### Parallel Execution Opportunities

**Phase 1 (Sequential — must go first):**
Agents 01 → 02 → 03 must run sequentially because each depends on the previous.

**Phase 2 (Parallelizable after Phase 1):**
Once documentation is complete, these can run in parallel:
- **Planning Team**: Agent 04 (Sprint Planning) + Agent 05 (Jira Tickets)
- **Architecture Team**: Agent 06 (Architecture Design)

**Phase 3 (After Phase 2):**
- **Code Team**: Agent 07 (Code Generation) — needs architecture output
- **Testing Team**: Agent 08 (Test Plans) — can start with requirements + jira tickets

**Phase 4 (Final — sequential):**
- Agent 09 (Deployment) → Agent 10 (Summary)

## How to Start Agent Teams Mode

### Option 1: Let Claude Create the Team
```
I need to run the SDLC automation pipeline using Agent Teams.

Create an agent team with 4 teammates:
1. "Business Analyst" — runs agents 01, 02, 03 sequentially
2. "Project Planner" — waits for BA, then runs agents 04, 05
3. "Tech Lead" — waits for Planner, then runs agents 06, 07
4. "QA & DevOps" — waits for Tech Lead, then runs agents 08, 09, 10

The input file is inputs/transcript.txt.
Each agent reads its .claude/agents/NN_*.md file for instructions.
Agents communicate through JSON files in the outputs/ directory.
```

### Option 2: Phased Parallel Execution
```
Create an agent team for SDLC automation:

Phase 1 (Sequential): Spawn a "Business Analysis" teammate to:
- Execute .claude/agents/01_transcript_agent.md
- Then .claude/agents/02_requirement_agent.md
- Then .claude/agents/03_documentation_agent.md

Once Phase 1 completes, spawn two teammates in parallel:
- "Planner" teammate: Execute agents 04 and 05
- "Architect" teammate: Execute agent 06

Once both finish, spawn:
- "Developer" teammate: Execute agent 07
- "QA" teammate: Execute agent 08

Finally, sequential: agents 09 and 10.
```

### Option 3: Research + Implementation Split
```
Create an agent team with 3 teammates:

Teammate 1 "Researcher": Read inputs/transcript.txt and analyze the client
requirements. Identify the domain, key features, compliance needs, and risks.
Share findings with the team.

Teammate 2 "Planner": Based on Researcher's findings, create the sprint plan,
team composition, and Jira ticket structure. Challenge the Researcher if
anything seems incomplete.

Teammate 3 "Architect": Design the technical architecture. Debate technology
choices with Planner to ensure feasibility within the timeline.

After all three finish, synthesize their work into the full pipeline output.
```

## Agent Teams vs Sequential Pipeline

| Aspect | Sequential Pipeline | Agent Teams |
|--------|-------------------|-------------|
| Speed | Slower (one at a time) | Faster (parallel where possible) |
| Token Usage | Lower | Higher (separate context per teammate) |
| Coordination | Automatic (JSON chain) | Team Lead manages |
| Error Recovery | Resume from any agent | Spawn replacement teammate |
| Best For | Full end-to-end runs | When you need speed or debate |
| Complexity | Simple | Moderate |

## When to Use Agent Teams

Use Agent Teams when:
- You want faster execution through parallelism
- You want teammates to debate/challenge each other's outputs
- You want to observe and steer individual teammates
- The project is complex enough to benefit from parallel work

Use Sequential Pipeline when:
- You want the simplest, most reliable execution
- Token budget is a concern
- The project is straightforward
- You want fully autonomous execution

## Task Dependencies in Agent Teams

When using Agent Teams, the shared task list handles dependencies:

```
Task 1: Analyze transcript → No dependencies
Task 2: Extract requirements → Blocked by Task 1
Task 3: Generate documentation → Blocked by Task 2
Task 4: Create sprint plan → Blocked by Task 3
Task 5: Create Jira tickets → Blocked by Task 3 (can parallel with 4)
Task 6: Design architecture → Blocked by Task 4, 5
Task 7: Generate code → Blocked by Task 6
Task 8: Create test plans → Blocked by Task 5, 7
Task 9: Create deployment configs → Blocked by Task 7, 8
Task 10: Final summary → Blocked by all above
```

## Quality Gates with Hooks

Use Claude Code hooks to enforce quality when teammates finish:

- **TeammateIdle**: When a teammate finishes, validate their output JSON
- **TaskCompleted**: When a task is marked complete, run contract validation

These hooks are configured in `.claude/hooks/` and integrate with Agent Teams
automatically.
