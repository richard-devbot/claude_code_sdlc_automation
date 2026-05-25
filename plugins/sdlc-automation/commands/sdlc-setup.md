---
allowed-tools: Bash, Read, Write
description: "Bootstrap SDLC pipeline in this project — copies helpers, scripts, config from plugin install"
---

# SDLC Setup — Bootstrap This Project

Copies `helpers/`, `scripts/`, and `sdlc-pipeline.yml` from the plugin install directory
into your current project, then creates the `inputs/` and `outputs/` directory structure.

**Run this once after installing the plugin in a new project.**

!`python3 - <<'SETUP_EOF'
import pathlib, shutil, sys, os

cwd = pathlib.Path.cwd()

def find_plugin_root():
    for base in [
        pathlib.Path.home() / ".claude/plugins/marketplaces",
        pathlib.Path.home() / ".claude/plugins/data",
        pathlib.Path.home() / ".claude/plugins/cache",
    ]:
        for p in base.rglob("sdlc-automation/scripts/orchestrator.py"):
            return p.parent.parent
    return None

plugin_root = find_plugin_root()
if not plugin_root:
    print("ERROR: sdlc-automation plugin not found. Install with:")
    print("  claude plugin marketplace add richard-devbot/claude_code_sdlc_automation")
    print("  claude plugin install sdlc-automation@claude_code_sdlc_automation")
    sys.exit(1)

print(f"Plugin found: {plugin_root}")
copied = []

# Copy helpers/
src_helpers = plugin_root / "helpers"
dst_helpers = cwd / "helpers"
if src_helpers.exists():
    dst_helpers.mkdir(exist_ok=True)
    for f in src_helpers.glob("*.py"):
        shutil.copy2(f, dst_helpers / f.name)
        copied.append(f"helpers/{f.name}")

# Copy scripts/
src_scripts = plugin_root / "scripts"
dst_scripts = cwd / "scripts"
if src_scripts.exists():
    dst_scripts.mkdir(exist_ok=True)
    for f in src_scripts.iterdir():
        shutil.copy2(f, dst_scripts / f.name)
        copied.append(f"scripts/{f.name}")

# Copy sdlc-pipeline.yml (only if not already present)
src_yml = plugin_root / "sdlc-pipeline.yml"
dst_yml = cwd / "sdlc-pipeline.yml"
if src_yml.exists() and not dst_yml.exists():
    shutil.copy2(src_yml, dst_yml)
    copied.append("sdlc-pipeline.yml")

# Create inputs/ and outputs/ directory structure
(cwd / "inputs").mkdir(exist_ok=True)
(cwd / "inputs" / "samples").mkdir(exist_ok=True)
for d in ["transcripts","requirements","documents","planning","jira","architecture",
          "code","qa","deployment","security","compliance","cost","feedback","analytics"]:
    out_dir = cwd / "outputs" / d
    out_dir.mkdir(parents=True, exist_ok=True)
    keep = out_dir / ".gitkeep"
    if not keep.exists():
        keep.touch()

# Create transcript placeholder if missing
transcript = cwd / "inputs" / "transcript.txt"
if not transcript.exists():
    transcript.write_text("# Paste your client meeting transcript here\n")
    copied.append("inputs/transcript.txt (placeholder)")

print(f"\nSetup complete! Copied {len(copied)} files:")
for f in copied:
    print(f"  + {f}")
print("\nNext step: add your transcript to inputs/transcript.txt")
print("Then run: /sdlc-start")
SETUP_EOF`
