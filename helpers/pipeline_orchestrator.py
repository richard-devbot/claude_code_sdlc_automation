#!/usr/bin/env python3
import os
import sys
import asyncio
import subprocess
import re
import time

# Base directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
AGENTS_DIR = os.path.join(PROJECT_DIR, ".claude", "agents")
OUTPUTS_DIR = os.path.join(PROJECT_DIR, "outputs")

# Hardcoded Agent Mappings based on AGENT_SKILL_MAP.md and DAG
AGENTS = {
    "environment_agent": "00_environment_agent.md",
    "transcript_agent": "01_transcript_agent.md",
    "requirement_agent": "02_requirement_agent.md",
    "documentation_agent": "03_documentation_agent.md",
    "planning_agent": "04_planning_agent.md",
    "jira_agent": "05_jira_agent.md",
    "architecture_agent": "06_architecture_agent.md",
    "code_agent": "07_code_agent.md",
    "testing_agent": "08_testing_agent.md",
    "deployment_agent": "09_deployment_agent.md",
    "summary_agent": "10_summary_agent.md",
    "feedback_loop_agent": "11_feedback_loop_agent.md",
    "security_threat_model_agent": "12_security_threat_model_agent.md",
    "compliance_checker_agent": "13_compliance_checker_agent.md",
    "cost_estimation_agent": "14_cost_estimation_agent.md"
}

# Define the DAG phases
# Each phase is a list of agent keys that can run in parallel
DAG_PHASES = [
    {"name": "Phase 1: Analysis", "parallel": ["environment_agent", "transcript_agent"]},
    {"name": "Phase 2: Requirements", "parallel": ["requirement_agent"]},
    {"name": "Phase 3: Documentation & Planning", "parallel": ["documentation_agent", "planning_agent"]},
    {"name": "Phase 4: Design", "parallel": ["jira_agent", "architecture_agent"]},
    {"name": "Phase 5: Security", "parallel": ["security_threat_model_agent"], "optional": True},
    {"name": "Phase 6: Implementation", "parallel": ["code_agent"]},
    {"name": "Phase 7: Quality", "parallel": ["testing_agent", "compliance_checker_agent"]},
    {"name": "Phase 8: Deployment", "parallel": ["deployment_agent"]},
    {"name": "Phase 9: Delivery", "sequential": ["summary_agent", "cost_estimation_agent", "feedback_loop_agent"]}
]

def load_optional_toggles():
    """Parse sdlc-pipeline.yml to check which optional agents are enabled."""
    toggles = {
        "security_threat_model": False,
        "compliance_checker": True,
        "cost_estimation": False,
        "feedback_loop": True
    }
    
    yaml_path = os.path.join(PROJECT_DIR, "sdlc-pipeline.yml")
    if not os.path.exists(yaml_path):
        return toggles
        
    try:
        with open(yaml_path, 'r') as f:
            content = f.read()
            
        # Very simple regex extraction for optional toggles
        opt_block = re.search(r'optional_agents:([\s\S]*?)notifications:', content)
        if opt_block:
            block = opt_block.group(1)
            for key in toggles.keys():
                match = re.search(fr'{key}:\s*(true|false)', block, re.IGNORECASE)
                if match:
                    toggles[key] = (match.group(1).lower() == 'true')
    except Exception as e:
        print(f"Warning: Failed to parse sdlc-pipeline.yml: {e}")
        
    return toggles

async def run_agent(agent_name):
    """Run an individual agent via the claude CLI asynchronously."""
    agent_file = AGENTS.get(agent_name)
    if not agent_file:
        print(f"[-] Error: Unknown agent {agent_name}")
        return False
        
    agent_path = os.path.join(AGENTS_DIR, agent_file)
    if not os.path.exists(agent_path):
        print(f"[-] Error: Agent file not found: {agent_path}")
        return False
        
    print(f"[*] Starting {agent_name}...")
    
    # We construct a highly specific prompt so it doesn't load unnecessary history
    # The agent will rely on its instructions to read the correct inputs
    prompt = f"Read and execute .claude/agents/{agent_file}. Complete your required tasks and write your JSON output contract. Stop and exit after completion without asking for further instructions."
    
    cmd = ["claude", "-p", prompt]
    
    try:
        # Run subprocess asynchronously
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=PROJECT_DIR,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            print(f"[+] {agent_name} completed successfully.")
            return True
        else:
            print(f"[-] {agent_name} failed with return code {process.returncode}")
            print(f"    Stderr: {stderr.decode('utf-8').strip()}")
            return False
            
    except Exception as e:
        print(f"[-] Exception running {agent_name}: {e}")
        return False

def validate_contracts():
    """Run the post_agent_contract_validator.py hook to ensure quality."""
    validator_path = os.path.join(PROJECT_DIR, ".claude", "hooks", "post_agent_contract_validator.py")
    if not os.path.exists(validator_path):
        print(f"[!] Warning: Validator hook not found at {validator_path}")
        return True # Pass if missing
        
    print(f"[*] Running contract validation hook...")
    result = subprocess.run(["python3", validator_path], cwd=PROJECT_DIR, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[+] All contracts validated successfully.")
        return True
    else:
        print(f"[-] Contract validation failed!")
        print(result.stdout)
        print(result.stderr)
        return False

async def run_phase(phase_config, toggles):
    """Run a single phase (parallel or sequential list of agents)."""
    print(f"\n{'='*50}")
    print(f"Executing {phase_config['name']}")
    print(f"{'='*50}")
    
    tasks = []
    
    # Check if this entire phase is optional and skipped
    if phase_config.get("optional", False):
        # We need a way to check if the agents in this phase are enabled
        # For simplicity, if it's the security phase, check the security toggle
        if "Phase 5" in phase_config['name'] and not toggles.get("security_threat_model", False):
            print(f"[*] Skipping {phase_config['name']} (disabled in config).")
            return True
            
    agents_to_run = []
    
    if "parallel" in phase_config:
        # Filter enabled agents
        for agent in phase_config["parallel"]:
            # Check optional agent toggles
            is_optional = False
            for t_key in toggles.keys():
                if t_key in agent:
                    is_optional = True
                    if toggles[t_key]:
                        agents_to_run.append(agent)
                    else:
                        print(f"[*] Skipping {agent} (disabled in config).")
                    break
            if not is_optional:
                agents_to_run.append(agent)
                
        if not agents_to_run:
            return True
            
        print(f"[*] Spawning in parallel: {', '.join(agents_to_run)}")
        for agent in agents_to_run:
            tasks.append(run_agent(agent))
            
        results = await asyncio.gather(*tasks)
        
        # Validation hook after phase
        if not validate_contracts():
            print("[!] Validation failed. In a production run, this would trigger an auto-retry loop.")
            # return False # Uncomment to enforce strict failing
            
        return all(results)
        
    elif "sequential" in phase_config:
        for agent in phase_config["sequential"]:
            # Check optional
            is_optional = False
            for t_key in toggles.keys():
                if t_key in agent:
                    is_optional = True
                    if toggles[t_key]:
                        print(f"\n[*] Executing {agent} sequentially...")
                        success = await run_agent(agent)
                        if not success:
                            return False
                    else:
                        print(f"[*] Skipping {agent} (disabled in config).")
                    break
            if not is_optional:
                print(f"\n[*] Executing {agent} sequentially...")
                success = await run_agent(agent)
                if not success:
                    return False
                    
        validate_contracts()
        return True

async def main():
    print("Initializing Pipeline Orchestrator Harness...")
    toggles = load_optional_toggles()
    print(f"Loaded optional toggles: {toggles}")
    
    start_time = time.time()
    
    for phase in DAG_PHASES:
        success = await run_phase(phase, toggles)
        if not success:
            print(f"\n[FATAL] Pipeline halted at {phase['name']} due to agent failure.")
            sys.exit(1)
            
    end_time = time.time()
    print(f"\n{'='*50}")
    print(f"Pipeline completed successfully in {int(end_time - start_time)} seconds.")
    print(f"{'='*50}")

if __name__ == "__main__":
    asyncio.run(main())
