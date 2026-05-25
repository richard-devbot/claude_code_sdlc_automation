---
allowed-tools: Bash
description: "Update the SDLC plugin to the latest version from GitHub main branch"
---

# SDLC Update — Pull Latest from GitHub

Updates the plugin (commands + agents) from the `main` branch of the GitHub repo,
then refreshes the helpers and scripts in your current project.

**Step 1 — Refresh marketplace cache from GitHub:**
!`claude plugin marketplace update claude_code_sdlc_automation 2>&1`

**Step 2 — Reinstall the plugin at the latest version:**
!`claude plugin update sdlc-automation@claude_code_sdlc_automation 2>&1`

**Step 3 — Refresh helpers and scripts in this project:**
!`python3 - <<'UPDATE_EOF'
import pathlib, shutil, sys

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
    print("Plugin not found in install locations. Run /sdlc-setup first.")
    sys.exit(1)

updated = []
for src_dir, dst_dir in [
    (plugin_root / "helpers", cwd / "helpers"),
    (plugin_root / "scripts", cwd / "scripts"),
]:
    if src_dir.exists() and dst_dir.exists():
        for f in src_dir.iterdir():
            shutil.copy2(f, dst_dir / f.name)
            updated.append(f"{dst_dir.name}/{f.name}")

# Update sdlc-pipeline.yml only if the user has the default (no local edits)
dst_yml = cwd / "sdlc-pipeline.yml"
src_yml = plugin_root / "sdlc-pipeline.yml"
if dst_yml.exists() and src_yml.exists():
    if dst_yml.read_bytes() != src_yml.read_bytes():
        backup = cwd / "sdlc-pipeline.yml.bak"
        shutil.copy2(dst_yml, backup)
        print(f"Your sdlc-pipeline.yml has local edits — backed up to sdlc-pipeline.yml.bak")
        print("Review the backup and merge any custom settings into the updated file.")
    shutil.copy2(src_yml, dst_yml)
    updated.append("sdlc-pipeline.yml")

print(f"Updated {len(updated)} files:")
for f in updated:
    print(f"  ~ {f}")
print("\nRestart Claude Code to apply the updated commands and agents.")
UPDATE_EOF`

---

> **Note:** Restart Claude Code after updating for new commands and agents to take effect.
>
> To see what changed: visit https://github.com/richard-devbot/claude_code_sdlc_automation/commits/main
