# -*- coding: utf-8 -*-
"""
Obsidian Vault Generator for AI Workstation projects.

Creates a structured Obsidian vault that serves as project memory.
The AI agent (Cline) can read/write these markdown files, and the user
can browse them in Obsidian with graph view, backlinks, etc.

Usage:
    python create_vault.py <project_path> <project_name>

Example:
    python create_vault.py D:\Projects\myapp myapp
"""

import os
import sys
import json
from datetime import datetime


def create_vault(project_path: str, project_name: str):
    """Create Obsidian vault structure in the given project path."""
    vault_root = os.path.join(project_path, ".obsidian-memory")
    os.makedirs(vault_root, exist_ok=True)

    # --- Obsidian config ---
    obsidian_config = {
        "appVersion": "1.0.0",
        "mainWorkspace": {"id": "main", "type": "split", "children": []},
        "attachmentFolderPath": "_attachments",
        "newFileLocation": "folder",
        "newFileFolderPath": "notes",
    }
    with open(os.path.join(vault_root, ".obsidian"), "w", encoding="utf-8") as f:
        json.dump(obsidian_config, f, indent=2)

    # --- Directories ---
    dirs = [
        "",  # root
        "notes",
        "architecture",
        "decisions",
        "research",
        "rules",
        "progress",
        "issues",
        "_attachments",
        "_templates",
    ]
    for d in dirs:
        os.makedirs(os.path.join(vault_root, d), exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d")

    # --- README / Index ---
    write_file(vault_root, "README.md", f"""---
created: {now}
tags: [index, {project_name}]
---

# {project_name} — Project Memory

This is the Obsidian vault for **{project_name}**.
The AI agent (Cline) reads and writes here. You browse in Obsidian.

## Structure

| Folder | Purpose |
|--------|---------|
| `notes/` | General notes, observations |
| `architecture/` | Architecture docs, diagrams (Mermaid) |
| `decisions/` | Architecture Decision Records (ADR) |
| `research/` | Research findings, analysis |
| `rules/` | Rules, patterns, conventions the agent must follow |
| `progress/` | Daily/weekly progress logs |
| `issues/` | Known issues, bugs, TODOs |
| `_templates/` | Templates for new notes |
| `_attachments/` | Images, files |

## Quick Links

- [[Architecture Overview]]
- [[Rules and Conventions]]
- [[Progress Log]]
- [[Decision Log]]

## How the agent uses this

1. **Before working**: reads `rules/` and `architecture/`
2. **During work**: updates `progress/` and `notes/`
3. **After work**: creates `decisions/` ADR if architectural choice made
""")

    # --- Architecture Overview ---
    write_file(vault_root, "architecture/architecture-overview.md", f"""---
created: {now}
tags: [architecture, {project_name}]
---

# Architecture Overview

> Describe the high-level architecture here.

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
- Database: 

## Related

- [[Rules and Conventions]]
- [[Decision Log]]
""")

    # --- Rules ---
    write_file(vault_root, "rules/rules-and-conventions.md", f"""---
created: {now}
tags: [rules, conventions, {project_name}]
---

# Rules and Conventions

> The AI agent MUST follow these rules when working on this project.

## Naming Conventions

- 

## Code Style

- 

## Architecture Rules

- 

## Forbidden

- 

## Related

- [[Architecture Overview]]
""")

    # --- Progress Log ---
    write_file(vault_root, "progress/progress-log.md", f"""---
created: {now}
tags: [progress, log, {project_name}]
---

# Progress Log

## {now}

- Project vault initialized

---

> The agent appends to this file after each work session.
> Format: ## YYYY-MM-DD HH:MM — task summary
""")

    # --- Decision Log ---
    write_file(vault_root, "decisions/decision-log.md", f"""---
created: {now}
tags: [decisions, adr, {project_name}]
---

# Decision Log

> Architecture Decision Records. One section per decision.

## ADR-001 — [Title]

**Date:** {now}
**Status:** Proposed

### Context

### Decision

### Consequences

---

> Copy this template for each new decision.
""")

    # --- Issues ---
    write_file(vault_root, "issues/known-issues.md", f"""---
created: {now}
tags: [issues, bugs, {project_name}]
---

# Known Issues

> Track bugs, TODOs, and known limitations.

## Issue Template

**ID:** ISS-001
**Severity:** High/Medium/Low
**Status:** Open/Closed
**Description:**
**Repro:**
**Notes:**

---

""")

    # --- Template: Note ---
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

    # --- Template: Decision ---
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

    # --- .clinerules (Cline reads this automatically) ---
    clinerules = f"""# {project_name} — Agent Rules

## Project Memory

The Obsidian vault is at `.obsidian-memory/` in the project root.

### Before starting any task:
1. Read `.obsidian-memory/rules/rules-and-conventions.md`
2. Read `.obsidian-memory/architecture/architecture-overview.md`
3. Check `.obsidian-memory/issues/known-issues.md`

### After completing a task:
1. Append progress entry to `.obsidian-memory/progress/progress-log.md`
2. If architectural decision made, create ADR in `.obsidian-memory/decisions/`
3. If new issue found, add to `.obsidian-memory/issues/known-issues.md`
4. Update architecture docs if structure changed

### Formatting:
- Use Obsidian wikilinks: `[[Note Title]]`
- Use frontmatter (YAML) with `created` and `tags`
- Use Mermaid for diagrams
- One topic per file

### Ghidra (if applicable):
- Use GhidraMCP tools to read/decompile
- Document findings in `.obsidian-memory/research/`
- Record renaming rules in `.obsidian-memory/rules/`
"""
    write_file(project_path, ".clinerules", clinerules)

    print(f"Obsidian vault created at: {vault_root}")
    print(f"  Open in Obsidian: File -> Open vault -> {vault_root}")
    print(f"  .clinerules created at project root")
    print(f"\nStructure:")
    for root, dirs, files in os.walk(vault_root):
        level = root.replace(vault_root, "").count(os.sep)
        indent = "  " * level
        print(f"{indent}{os.path.basename(root)}/")
        for f in sorted(files):
            print(f"{indent}  {f}")


def write_file(base_path: str, rel_path: str, content: str):
    """Write a file with UTF-8 encoding."""
    full_path = os.path.join(base_path, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8", newline="") as f:
        f.write(content)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_vault.py <project_path> <project_name>")
        print("Example: python create_vault.py D:\\Projects\\myapp myapp")
        sys.exit(1)

    project_path = sys.argv[1]
    project_name = sys.argv[2]

    if not os.path.exists(project_path):
        os.makedirs(project_path, exist_ok=True)

    create_vault(project_path, project_name)
