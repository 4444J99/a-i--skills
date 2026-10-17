---
name: workspace-autopsy-governance
description: Conducts a full automated autopsy of the current workspace directory to map files, identifies structural issues, proposes a restructuring plan (the signal), and establishes unified governance using templates. Use this skill when a user asks to map, restructure, reorganize, or apply new governance to an existing messy repository.
license: MIT
---

# Workspace Autopsy & Governance Restructure

## Overview

This skill enables agents to systematically analyze (autopsy) an existing, potentially disorganized workspace, propose a logical new directory structure, and migrate the workspace to this new structure while enforcing new governance standards.

## Workflow

To execute this skill, follow these sequential steps:

### Phase 1: Workspace Autopsy (Mapping)
To begin, you must understand the current state of the workspace.
1. Run the autopsy script to map the directory:
   `python /Users/4jp/.agents/skills/workspace-autopsy-governance/scripts/workspace_autopsy.py --dir .`
2. Review the generated map and statistics. Identify:
   - Where the core source code lives.
   - Where documentation, scripts, and assets are currently scattered.
   - Legacy folders or structural chaos that need cleaning.

### Phase 2: Sending the Signal (Restructure Proposal)
Before moving any files, you must "send out the signal" to the user proposing the new structure and governance.
1. Read the template from `assets/RESTRUCTURE_PROPOSAL-template.md`.
2. Draft a customized `RESTRUCTURE_PROPOSAL.md` based on your findings from the autopsy. Detail exactly which directories will be created and which files will move where.
3. Present this proposal to the user and wait for their explicit approval. Do not proceed to Phase 3 without approval.

### Phase 3: Unite Under New Locations (Migration)
Once the user approves the proposal:
1. Create the new target directories (e.g., `/src`, `/docs`, `/scripts`, `/assets`, `/tests`) as agreed upon in the proposal.
2. Use standard shell commands (`mv`) to systematically migrate files from their old locations to the newly created, unified locations.
3. Ensure no orphaned files remain in chaotic root locations unless they are standard configuration files (e.g., `.gitignore`, `package.json`).

### Phase 4: Establish New Governance
With the files in their new locations, establish the rules that will govern them going forward.
1. Read the template from `assets/GEMINI-template.md`.
2. Customize it to reflect the specific standards, workflows, and constraints of the newly restructured project.
3. Write this customized governance document to `GEMINI.md` at the root of the project.
4. If appropriate, create subdirectory-specific `GEMINI.md` files for deeper governance (e.g., in `/src/GEMINI.md`).

## Resources Included

### `scripts/workspace_autopsy.py`
A Python script that traverses the specified directory, ignores common build/dependency folders, and prints a tree map along with statistics about file types and counts.

### `assets/RESTRUCTURE_PROPOSAL-template.md`
A template for the document you will generate to propose the new structure to the user.

### `assets/GEMINI-template.md`
A template for the governance rules to establish in the repository after the restructure.
