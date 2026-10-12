# Skills consolidation checkpoint

## Scope

This first consolidation change adds portable versions of two existing authored
skills to the public catalog. Their private source copies remain available.
Per-file source commits, Git blob hashes, destination paths, and transformations
are recorded in [skill-import-provenance.json](skill-import-provenance.json).

| Skill | Catalog destination | Treatment |
|---|---|---|
| `d2l-discussion-responder` | `skills/education/d2l-discussion-responder` | Preserve the verified-reply workflow and existing MIT declaration; replace live course details and browser-specific workarounds with blank inputs and supported-tool operations. |
| `recommendation-letter` | `skills/education/recommendation-letter` | Preserve the evidence-based drafting workflow and existing MIT declaration; make Markdown the independent core output and requested PDF rendering optional. |

The D2L skill was introduced by Anthony James Padavano in
[`_agent` commit fe2383c](https://github.com/4444J99/_agent/commit/fe2383caaad4977f27fcde98c297d4a4545cc7fb).
The recommendation skill was introduced by the same author in
[`edu-organism` commit 9904d20](https://github.com/4444J99/edu-organism/commit/9904d20c29f6af795198e58ec4e84dcf7186ff98).
Both source entrypoints already declare MIT. These imports retain those
declarations; repository ownership alone was not used to assign a license.

The change also corrects `specstory-session-summary` metadata from MIT to
Apache-2.0, matching its included `LICENSE.txt` and the
[upstream license at 9454d3f](https://github.com/specstoryai/agent-skills/blob/9454d3f2b9ac5397d735ae3bbdcfa6dc83392036/skills/specstory-session-summary/LICENSE.txt).
The license text itself is unchanged.

## Verified baseline after PR #41

The handoff mixed pre-cleanup and post-cleanup inventory. The following values
were measured from `a-i--skills` at
[`73d027d15e474380186831fed764df16bca1cb15`](https://github.com/4444J99/a-i--skills/commit/73d027d15e474380186831fed764df16bca1cb15),
before these two imports:

| Measure | Baseline |
|---|---:|
| Canonical catalog definitions | 165 |
| Plugin definitions | 11 |
| Total distinct source definitions | 176 |
| Declared third-party or derived definitions | 23 |
| Remaining definitions under the repository's authorship classification | 153 |
| Generated copies of catalog skills | 660 |
| Total tracked uppercase `SKILL.md` paths | 836 |
| Tracked bytes under `distributions/` | 39,879,039 |
| Tracked bytes in the whole repository tree | 51,957,997 |

The original-work figure reconciles as `165 - 23 + 11 = 153`. It is inventory
arithmetic using the repository's provenance classifications, not independent
authorship proof for every file. The 23 third-party or derived entries comprise
11 Anthropic, six SpecStory, one spec-kit, and five everything-claude-code entries.
The earlier count of 31 predates the eight removals in PR #41.

After this change the source catalog contains **167 catalog + 11 plugin = 178
definitions**. All 176 existing definitions are retained. The only existing
skill-source change is the SpecStory license metadata correction.

The two reported remaining name occurrences were absent from tracked content.
All 40 `.skill` archives and three ZIP archives, including nested ZIP contents,
were inspected without archive errors. None contained the reported names or an
entrypoint for the eight removed skills. There were no tracked `.docx` files.
This check covered the pinned current tree, not Git history, forks, or release
assets. References to earlier inventory remain in historical plans and audits.

The Pages workflow uploads only `site/`; its sole tracked file at the baseline
was `site/index.html`. Repository-content checks do not independently establish
the response status of every historical public URL.

## Third candidate still pending

`taxonomic-ontological-teleological-domain-expert` remains in its private source
at [`_agent` 21d62c1](https://github.com/4444J99/_agent/tree/21d62c13bab0f7b82bfa3f6cb3c9a1ee89ad1a2f/skills/taxonomic-ontological-teleological-domain-expert).
Its 35-file payload is distinct from the existing knowledge skills, but is not
ready for public catalog admission:

1. No license declaration or applicable source license file was found. Record
   the author's chosen license before publishing; do not infer MIT.
2. Normalize lowercase `skill.md` to `SKILL.md`, add a task-focused description,
   and map or separate its domain lifecycle values from catalog governance fields.
3. Replace personal contact data in the examples with fictional placeholders.
4. Resolve differences between the contracts, templates, and examples, including
   required relation IDs, change-field types, and draft versus approved emission.
5. Describe its Markdown rules and tests as specifications. There is no executable
   validator or machine-readable schema in the inspected payload.

## Snapshot retirement requires a consumer migration

The runtime audit used these pinned sources:

| Repository | Commit |
|---|---|
| `_agent` | `21d62c13bab0f7b82bfa3f6cb3c9a1ee89ad1a2f` |
| `_agent-ontology` | `ffbdb42a7a751e1304db5da4746abec111df2cb8` |
| `domus-genoma` | `0d93f029a8200b98686f95c4dfd173a0f1aaf357` |

Against the PR #41 baseline, 132 of 161 exported `_agent` skill folders and 115
of 160 `_agent-ontology` skill folders have identical Git tree hashes to the
corresponding catalog folders. Comparing entrypoint blobs alone gives larger
counts, 144 and 118, and does not prove whole-folder equality. Preserve and
classify all differing folders before retirement.

`_agent` has 162 uppercase `SKILL.md` files and two additional lowercase
`skill.md` files. A scanner that searches only uppercase paths misses both the
taxonomy skill and `codebase-visualizer`.

The snapshot is an executable dependency of the declared
[`_agent` pre-commit configuration](https://github.com/4444J99/_agent/blob/21d62c13bab0f7b82bfa3f6cb3c9a1ee89ad1a2f/.pre-commit-config.yaml):
its scanner path points inside the exported `specstory-guard` skill. Dependabot
also names two directories inside the snapshot. The separate `.githooks` setup
does not run that scanner, so this audit establishes configured dependencies,
not which hooks are installed on a user's host. Replace the references and prove
the scanner still works before removing the snapshot. The whole `_agent`
repository contains additional work and is not synonymous with this snapshot.

## Generated-output retirement requires a complete build

`distributions/` accounts for 76.75% of baseline tracked file bytes. Removing it
now would break committed consumers:

- The [Claude skills symlink](https://github.com/4444J99/domus-genoma/blob/0d93f029a8200b98686f95c4dfd173a0f1aaf357/private_dot_claude/symlink_skills.tmpl)
  points into `distributions/claude/skills`.
- [Cowork synchronization](https://github.com/4444J99/domus-genoma/blob/0d93f029a8200b98686f95c4dfd173a0f1aaf357/dot_local/bin/executable_cowork-skills-sync)
  copies from that directory and uses `rsync --delete`.
- The `composer` command and skill-planning commands read the generated registry.
- The [Gemini installer](https://github.com/4444J99/domus-genoma/blob/0d93f029a8200b98686f95c4dfd173a0f1aaf357/.chezmoiscripts/run_onchange_after_install-gemini-extensions.sh.tmpl)
  uses distribution descriptors and still declares the removed document extension.

The [Domus sync hook](https://github.com/4444J99/domus-genoma/blob/0d93f029a8200b98686f95c4dfd173a0f1aaf357/.chezmoiscripts/run_onchange_after_sync-skills.sh.tmpl)
clones or updates the repository but does not build it. The current refresh
script also does not reconstruct every tracked descriptor from nothing, and it
prints registry/lockfile subprocess failures as warnings. A simple added refresh
call is not sufficient evidence of a complete installation contract.

Before removing tracked outputs, implement and verify a build that generates
every descriptor, fails on generator errors, validates staged output, and then
switches consumers to the completed output. Preserve Cowork's separate writable
copy. Exercise a fresh checkout and an update with both additions and removals,
and change CI's expectation of committed generated files in the same migration.

## Portal implementation material has no verified deployment here

Domus retains `_portal/skills/_arms` files, but its
[current ignore configuration](https://github.com/4444J99/domus-genoma/blob/0d93f029a8200b98686f95c4dfd173a0f1aaf357/.chezmoiignore)
excludes `_portal/**` and describes `_portal` as independently owned. The retained
resolver also has an old root-path assumption. These files are useful source
material; they do not prove an operating multi-runtime portal. Locate its current
owner and deployed source before treating it as the destination of a migration.

## Next changes in dependency order

1. Review and merge these two portable imports through the normal review gate.
2. Resolve the taxonomy admission conditions above.
3. Reconcile differing snapshot folders and replace their executable consumers.
4. Implement and verify complete staged builds and runtime installation.
5. Remove generated copies and retire duplicate snapshots only after replacements
   are accepted. Route unrelated project clusters with file-level provenance and
   destination verification; repository deletion is a separate decision.

No history rewrite, fork modification, repository archival, permission change,
source deletion, or review-rule bypass is part of this change.
