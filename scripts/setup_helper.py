# -*- coding: utf-8 -*-
"""
Project Setup Helper for AI Workstation.

Automatically creates project infrastructure when a new project is opened.
Cline calls this script via terminal tool to set up:
- Obsidian vault (.obsidian-memory/)
- .clinerules
- Git repository (if not exists)
- Project documentation template

Usage (called by Cline agent):
    python scripts/setup_helper.py <project_path> <project_type> [--project-name <name>]

Project types:
    generic   - Standard code project (default)
    reverse   - Reverse engineering project (includes GhidraMCP rules)
    rag       - RAG/AI project
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            cwd=cwd, timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def detect_project_type(project_path: str) -> str:
    """Detect project type by analyzing files."""
    path = Path(project_path)
    
    # Check for reverse engineering indicators
    ghidra_files = list(path.glob("**/*.ghidra"))
    elf_files = list(path.glob("**/*.elf"))
    bin_files = list(path.glob("**/*.bin"))
    so_files = list(path.glob("**/*.so"))
    dll_files = list(path.glob("**/*.dll"))
    
    if ghidra_files or elf_files or bin_files or so_files or dll_files:
        return "reverse"
    
    # Check for Python project
    if (path / "pyproject.toml").exists() or (path / "setup.py").exists():
        return "python"
    
    # Check for JS/TS project
    if (path / "package.json").exists():
        return "javascript"
    
    # Check for C/C++ project
    if (path / "CMakeLists.txt").exists() or (path / "Makefile").exists():
        return "cpp"
    
    # Default
    return "generic"


def create_obsidian_vault(project_path: str, project_name: str, project_type: str):
    """Create Obsidian memory vault."""
    vault_root = os.path.join(project_path, ".obsidian-memory")
    os.makedirs(vault_root, exist_ok=True)
    
    now = datetime.now().strftime("%Y-%m-%d")
    
    # Vault config
    obsidian_config = {
        "appVersion": "1.0.0",
        "attachmentFolderPath": "_attachments",
        "newFileLocation": "folder",
        "newFileFolderPath": "notes",
    }
    with open(os.path.join(vault_root, ".obsidian"), "w", encoding="utf-8") as f:
        json.dump(obsidian_config, f, indent=2)
    
    # Directories
    for d in ["notes", "architecture", "decisions", "research", "rules", "progress", "issues", "_attachments", "_templates"]:
        os.makedirs(os.path.join(vault_root, d), exist_ok=True)
    
    # README
    write_file(vault_root, "README.md", f"""---
created: {now}
tags: [index, {project_name}]
---

# {project_name} — Project Memory

> AI agent workspace. Agent reads/writes here. You browse in Obsidian.

## Structure

| Folder | Purpose |
|--------|---------|
| `notes/` | General notes, observations |
| `architecture/` | Architecture docs, diagrams (Mermaid) |
| `decisions/` | Architecture Decision Records (ADR) |
| `research/` | Research findings, analysis |
| `rules/` | Rules, patterns, conventions |
| `progress/` | Daily/weekly progress logs |
| `issues/` | Known issues, bugs, TODOs |
| `_templates/` | Templates for new notes |
| `_attachments/` | Images, files |

## Quick Links

- [[Architecture Overview]]
- [[Rules and Conventions]]
- [[Progress Log]]
- [[Decision Log]]
""")
    
    # Architecture
    write_file(vault_root, "architecture/architecture-overview.md", f"""---
created: {now}
tags: [architecture, {project_name}]
---

# Architecture Overview

## Components

- 

## Data Flow

```mermaid
graph TD
    A[Input] --> B[Process]
    B --> C[Output]
```

## Tech Stack

- Language: 
- Framework: 

## Related

- [[Rules and Conventions]]
""")
    
    # Rules
    if project_type == "reverse":
        rules_content = f"""---
created: {now}
tags: [rules, conventions, reverse, {project_name}]
---

# Rules and Conventions (Reverse Engineering)

## Ghidra Analysis Rules

- Always use GhidraMCP tools for decompilation
- Document findings in `.obsidian-memory/research/`
- Record renaming patterns in `.obsidian-memory/rules/`
- Track xrefs (cross-references) for important functions
- Identify standard library calls (printf, memcpy, etc.)
- Look for encryption routines, hash functions, string decoding
- Note obfuscation patterns

## Naming Conventions

- Functions: `func_{description}_{type}` (snake_case)
- Variables: `var_{description}` (snake_case)
- Comments: English only, concise

## Analysis Patterns

- Entry points → trace execution flow
- String references → identify functionality
- API imports → identify libraries used
- Encryption constants → identify algorithms

## Related

- [[Architecture Overview]]
""")
    else:
        rules_content = f"""---
created: {now}
tags: [rules, conventions, {project_name}]
---

# Rules and Conventions

## Code Style

- 

## Architecture Rules

- 

## Naming Conventions

- 

## Related

- [[Architecture Overview]]
""")
    write_file(vault_root, "rules/rules-and-conventions.md", rules_content)
    
    # Progress Log
    write_file(vault_root, "progress/progress-log.md", f"""---
created: {now}
tags: [progress, log, {project_name}]
---

# Progress Log

## {now}

- Project vault initialized
- Project type detected: {project_type}

---

> Agent appends to this file after each work session.
""")
    
    # Decision Log
    write_file(vault_root, "decisions/decision-log.md", f"""---
created: {now}
tags: [decisions, adr, {project_name}]
---

# Decision Log

## ADR-001 — Project Initialization

**Date:** {now}
**Status:** Accepted

### Context
Project started.

### Decision
Use Obsidian vault at `.obsidian-memory/` for project memory.

### Consequences
All documentation tracked. Graph view available in Obsidian.

---
""")
    
    # Issues
    write_file(vault_root, "issues/known-issues.md", f"""---
created: {now}
tags: [issues, bugs, {project_name}]
---

# Known Issues

## ISS-001 — Project Initialized

**Severity:** Low
**Status:** Open
**Description:** Project just created. Issues to be documented as discovered.

---
""")
    
    # Templates
    write_file(vault_root, "_templates/note.md", """---
created: {{date:YYYY-MM-DD}}
tags: [note]
---

# {{title}}

> Summary

## Details

## Related

- 
""")
    
    write_file(vault_root, "_templates/decision.md", """---
created: {{date:YYYY-MM-DD}}
tags: [decision, adr]
---

# ADR-{{number}} — {{title}}

**Date:** {{date:YYYY-MM-DD}}
**Status:** Proposed

## Context

## Decision

## Consequences

## Alternatives Considered

## Related

- 
""")
    
    # Research dir for reverse engineering
    if project_type == "reverse":
        write_file(vault_root, "research/analysis-template.md", f"""---
created: {now}
tags: [research, reverse, decompilation, {project_name}]
---

# Analysis: {{function_name}}

**Address:** 0x{{address}}
**Size:** {{size}} bytes
**Called by:** {{xrefs_to}}
**Calls:** {{xrefs_from}}

## Decompiled Code

```c
// Paste Ghidra decompilation here
```

## Analysis

- 

## Identified Patterns

- 

## Related

- [[Rules and Conventions]]
""")
    
    return vault_root


def create_clinerules(project_path: str, project_name: str, project_type: str, vault_root: str):
    """Create .clinerules file."""
    
    base_rules = f"""# {project_name} — Agent Rules

## Project Memory

The Obsidian vault is at `{vault_root}` in the project root.

### Before starting any task:
1. Read `{vault_root}/rules/rules-and-conventions.md`
2. Read `{vault_root}/architecture/architecture-overview.md`
3. Check `{vault_root}/issues/known-issues.md`

### After completing a task:
1. Append progress entry to `{vault_root}/progress/progress-log.md`
2. If architectural decision made, create ADR in `{vault_root}/decisions/`
3. If new issue found, add to `{vault_root}/issues/known-issues.md`
4. Update architecture docs if structure changed

### Formatting:
- Use Obsidian wikilinks: `[[Note Title]]`
- Use frontmatter (YAML) with `created` and `tags`
- Use Mermaid for diagrams
- One topic per file
"""
    
    if project_type == "reverse":
        base_rules += f"""

## Reverse Engineering Rules

- Use GhidraMCP tools for decompilation and analysis
- Document ALL findings in `{vault_root}/research/`
- Record renaming patterns in `{vault_root}/rules/`
- Always check xrefs (cross-references) before renaming
- Look for: encryption, hashing, string decoding, API calls
- Identify standard library functions (printf, memcpy, etc.)
- Note obfuscation techniques used

## GhidraMCP Workflow

1. Start Ghidra with the target binary
2. Ensure GhidraMCP HTTP server is running (port 8080)
3. Start MCP Bridge: `start-ghidra-mcp.bat`
4. Use tools: decompile_function, list_functions, get_xrefs_to
5. Rename functions and add comments in Ghidra
6. Document analysis in `.obsidian-memory/research/`

## Night-long Analysis

For extended analysis sessions:
- Start with `list_functions` to get overview
- Prioritize: entry points → string references → API imports
- Process functions in batches (10-20 at a time)
- Update progress log after each batch
- Save state in `.obsidian-memory/progress/` between sessions
"""
    
    write_file(project_path, ".clinerules", base_rules)


def setup_git(project_path: str):
    """Initialize git if not exists."""
    if os.path.exists(os.path.join(project_path, ".git")):
        return False, "Git already initialized"
    
    success, out, err = run_command("git init", cwd=project_path)
    if success:
        # Create .gitignore
        gitignore = "# Python\n__pycache__/\n*.pyc\n.env\n\n# IDE\n.vscode/\n.idea/\n\n# OS\n.DS_Store\nThumbs.db\n\n# Obsidian Memory\n.obsidian-memory/.obsidian\n"
        write_file(project_path, ".gitignore", gitignore)
        return True, "Git initialized"
    return False, err


def write_file(base_path: str, rel_path: str, content: str):
    """Write file with UTF-8."""
    full_path = os.path.join(base_path, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8", newline="") as f:
        f.write(content)


def main():
    if len(sys.argv) < 2:
        print("Usage: python setup_helper.py <project_path> [project_type] [--project-name <name>]")
        print("Types: generic, reverse, python, javascript, cpp")
        print("Example: python setup_helper.py D:\\Projects\\myapp reverse --project-name MyApp")
        sys.exit(1)
    
    project_path = sys.argv[1]
    project_type = sys.argv[2] if len(sys.argv) > 2 else None
    project_name = None
    
    # Parse --project-name
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--project-name" and i + 1 < len(sys.argv):
            project_name = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if project_type is None:
        project_type = detect_project_type(project_path)
        print(f"Auto-detected type: {project_type}")
    
    if project_name is None:
        project_name = os.path.basename(project_path)
    
    print(f"Setting up: {project_name} (type: {project_type})")
    print(f"Path: {project_path}\n")
    
    # 1. Create Obsidian vault
    vault_root = create_obsidian_vault(project_path, project_name, project_type)
    print(f"[OK] Obsidian vault: {vault_root}")
    
    # 2. Create .clinerules
    create_clinerules(project_path, project_name, project_type, vault_root)
    print(f"[OK] .clinerules created")
    
    # 3. Setup git
    success, msg = setup_git(project_path)
    print(f"[OK] Git: {msg}")
    
    print(f"\nDone! Open in Obsidian: {vault_root}")


if __name__ == "__main__":
    main()
