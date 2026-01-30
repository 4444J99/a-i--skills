# /specstory-organize

Organizes the project's .specstory/history directory into year and month subfolders.

## What It Does

Moves `.md` files from `.specstory/history/` into `.specstory/history/YYYY/MM/` subdirectories based on the timestamp in each filename (not the file's modification time). Creates year and month directories as needed, and leaves non-.md files or files without valid timestamps in place.

## Installation

If using npx skills from the [npx skills repository](https://skills.sh/):

```zsh
npx skills add specstoryai/agent-skills
```

To install manually, clone the repo:

```zsh
git clone https://github.com/specstoryai/agent-skills
cp -r agent-skills/skills/specstory-organize ~/.claude/skills/
```

## Usage

```
/specstory-organize
```

## License

The /specstory-organize skill is licensed under the [Apache 2.0 open source license](LICENSE.txt).

Copyright 2025-2026 by SpecStory, Inc., All Rights Reserved.

SpecStory® is a registered trademark of SpecStory, Inc.