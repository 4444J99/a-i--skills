# Marketplace interoperability and publication

## Decision and scope

Use external directories to discover candidate skills and help people find the
public catalog. Keep the verified build and installation transaction as the
publisher of managed runtime files. Preserve complete plugins when their skills
depend on shared references, commands, agents, or descriptors.

This evaluation was made on October 10, 2026, against canonical source
[`7af4cd94a485aa9e72eed0c02dd211bc35004121`](https://github.com/4444J99/a-i--skills/commit/7af4cd94a485aa9e72eed0c02dd211bc35004121):
167 catalog definitions and 11 definitions in two complete plugins. It supports
the [installation contract](installation.md) and
[activation issue #23](https://github.com/4444J99/a-i--skills/issues/23).
Directory listings, successful filesystem installation, native runtime loading,
and publication of a versioned release each require their own evidence.

## The six references

| Reference | Verified role | Application here | Material limit |
|---|---|---|---|
| [SkillsMP](https://skillsmp.com/) | Public GitHub skill index with source previews, categories, occupation browsing, and a search API. | Discovery and a possible publication channel for the canonical public source. | Its own site says it does not install or certify indexed skills. A search result is not an installation receipt. |
| [agent-skills.cc](https://agent-skills.cc/) | Repository directory with copy and plugin installation guidance. | An additional discovery surface. | No concrete self-service publication flow was verified in the inspected pages. An inspected collection page offers clone commands without proving a working installation. |
| [dukelyuu/skills-marketplace](https://github.com/dukelyuu/skills-marketplace/tree/7aa4a5cc01111096f2560af837d5298c7c7382b5) | Marketplace frontend and static server. | Interface ideas for the later skills window. | The inspected checkout lacks backend and deployment components described in its setup instructions; its ZIP export omits supporting folders. |
| [agentskill.sh](https://agentskill.sh/) | Directory, public import flow, CLI, and `/learn` instructions. | Candidate discovery and a separately verified publication channel. | The inspected client updates destinations in place and records server-supplied content markers; it does not implement the complete-release transaction required here. |
| [skills.sh](https://www.skills.sh/) | Vercel directory and open-source `skills` CLI, including Claude marketplace discovery. | A useful interoperability target for individual self-contained skills. | Discovery of a plugin skill does not preserve its enclosing package during the tested installation modes. |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills/tree/c68487d721e419ec87af1ae6412a842978eab785) | Product-management skills and command workflows packaged as nine plugins. | Packaging reference and a focused future admission candidate. | Prompt methods and structural tests do not establish task performance or safe managed updates. |

Site-wide counts and popularity labels were not used as acceptance evidence.
Several inspected pages display inconsistent catalog totals. The following
findings instead identify exact source revisions and bounded executable checks.

## Vercel CLI: discovery and package preservation

The inspected implementation is
[`vercel-labs/skills@13e4063a1cf913f5606d57d42ab83a86f5001e04`](https://github.com/vercel-labs/skills/tree/13e4063a1cf913f5606d57d42ab83a86f5001e04).
Its package metadata declares version `1.7.2`; the probe runs the reviewed APIs
from that Git commit, rather than assuming the npm package contains the same
revision.

The source supports categorized `skills/` directories and local paths declared
by [Claude marketplace and plugin manifests](https://github.com/vercel-labs/skills/blob/13e4063a1cf913f5606d57d42ab83a86f5001e04/src/plugin-manifest.ts).
The bounded local probe found all **178 unique definitions**, using the canonical
paths, in both normal and full-depth discovery. When duplicate names were
explicitly retained, full-depth discovery also included generated distribution
copies. Name deduplication therefore hides copies; it does not establish
complete-folder equivalence or authorize retiring them.

The duplicate-retaining full-depth probe returned 679 entries, while the checkout
contains 846 tracked uppercase entrypoints. Its bounded recursion misses the
deeper Gemini distribution copies. It cannot replace the exhaustive,
case-insensitive file inventory required for snapshot reconciliation.

Removing both `distributions/` and the generated marketplace from an exact source
archive exposed another distinction:

| Input | Normal discovery | Full-depth discovery |
|---|---:|---:|
| Source archive without pre-existing generated output | 167 | 178 |
| Verified release built from that source | 178 | 178 |

The canonical build and explicit validation both succeeded. All 969 remaining
source files were unchanged, and the generated paths remained absent in the
source fixture. The manifest was regenerated in the separate verified release.
The archive has no `.git` directory, so its release manifest records a null
source commit; the companion receipt pins the archive to `7af4cd9` and its full
tree and archive hashes.

The probe then called the real
[installation routine](https://github.com/vercel-labs/skills/blob/13e4063a1cf913f5606d57d42ab83a86f5001e04/src/installer.ts)
in isolated project directories, with telemetry disabled:

| Payload | Default symlink mode and copy mode | Result |
|---|---|---|
| `recommendation-letter` | Both skill files preserve their hashes and modes; its rubric link resolves. | The tested standalone folder is preserved. |
| `coliseum-orchestrator` | The entrypoint is copied and installation reports success, but all four `../../references/...` links fail. | The complete plugin is required. |

This is a filesystem/API compatibility result. It does not claim a signed-in
model invocation, npm-package equivalence, all catalog workflows passing, or
runtime cache refresh. The
[reproduction guide](evidence/2026-10-10-marketplace-compatibility/README.md),
[discovery/install receipt](evidence/2026-10-10-marketplace-compatibility/compatibility-receipt.json),
and [stripped-source/build receipt](evidence/2026-10-10-marketplace-compatibility/stripped-source-receipt.json)
preserve the commands, exact source identities, all returned name/path records,
and both tested installation modes.

The managed installation should continue to expose the complete local Claude
marketplace and its plugin packages. A generic `skills add` command is suitable
only after the selected skill's folder and dependencies have been verified for
that installation mode. Do not advertise an all-skills CLI command as equivalent
to the full installation contract.

The inspected CLI also has a
[project lockfile with a computed folder hash](https://github.com/vercel-labs/skills/blob/13e4063a1cf913f5606d57d42ab83a86f5001e04/src/local-lock.ts).
Its installation routine clears and copies individual destination directories.
These are useful management features, but they do not establish atomic catalog
activation or recovery across Claude, Cowork, Gemini, and registry consumers.

## Other implementation findings

### agentskill.sh

At [`agentskill-sh/ags@ede92fd8fc94335d40dc0f74c60b4355c83c4a4c`](https://github.com/agentskill-sh/ags/tree/ede92fd8fc94335d40dc0f74c60b4355c83c4a4c),
the CLI package declares version `2.0.2`. The
[installer](https://github.com/agentskill-sh/ags/blob/ede92fd8fc94335d40dc0f74c60b4355c83c4a4c/src/installer.ts)
writes `SKILL.md` and supplied supporting files directly into existing
directories, then creates links or copies for additional agents. The
[update command](https://github.com/agentskill-sh/ags/blob/ede92fd8fc94335d40dc0f74c60b4355c83c4a4c/src/commands/update.ts)
uses that same routine. The inspected paths do not reconcile supporting files
removed from a newer payload or preserve an atomic previous installation.

Its [lockfile](https://github.com/agentskill-sh/ags/blob/ede92fd8fc94335d40dc0f74c60b4355c83c4a4c/src/skill-lock.ts)
stores slug, server-supplied `contentSha`, installation time, and chosen agents.
Those routines do not recompute the installed bytes against the supplied marker.
These are source-review findings; no failure-injection test of `ags` was run.

An interactive
[`ags install` with a GitHub URL](https://github.com/agentskill-sh/ags/blob/ede92fd8fc94335d40dc0f74c60b4355c83c4a4c/src/commands/install.ts)
first posts the URL to the service's submission API. It is an external import
action as well as a local installation command. It was not used as a read-only
probe. The same source's JSON branch returns before the interactive low-score
confirmation. The website's security descriptions and `/learn`'s written review
instructions should therefore remain distinct from executable installation
guarantees.

### dukelyuu/skills-marketplace

At [`7aa4a5cc01111096f2560af837d5298c7c7382b5`](https://github.com/dukelyuu/skills-marketplace/tree/7aa4a5cc01111096f2560af837d5298c7c7382b5),
complete-tree inspection found no `backend/`, `deploy/`, `docker-compose.yml`,
recognized dependency lockfile, or case-insensitive `SKILL.md` entrypoint. The
[README](https://github.com/dukelyuu/skills-marketplace/blob/7aa4a5cc01111096f2560af837d5298c7c7382b5/README.md)
requires several of those absent paths for its documented setup. The committed
[server](https://github.com/dukelyuu/skills-marketplace/blob/7aa4a5cc01111096f2560af837d5298c7c7382b5/src/server/index.ts)
serves static files; the frontend expects a separate API.

The [ZIP export](https://github.com/dukelyuu/skills-marketplace/blob/7aa4a5cc01111096f2560af837d5298c7c7382b5/src/client/src/pages/SkillDetail.tsx)
writes only `SKILL.md`, synthesized `skill.json`, and synthesized `README.md`.
It does not package scripts, references, assets, or license notices from the
complete source folder. This export cannot replace the verified bundles.

The actual root [LICENSE](https://github.com/dukelyuu/skills-marketplace/blob/7aa4a5cc01111096f2560af837d5298c7c7382b5/LICENSE)
is Apache-2.0, while its
[frontend package metadata](https://github.com/dukelyuu/skills-marketplace/blob/7aa4a5cc01111096f2560af837d5298c7c7382b5/src/package.json)
still says MIT. Record and resolve that discrepancy before copying implementation
code. Interface concepts can inform a later window over the verified registry.

## PM Skills: focused admission preparation

[`phuryn/pm-skills@c68487d721e419ec87af1ae6412a842978eab785`](https://github.com/phuryn/pm-skills/tree/c68487d721e419ec87af1ae6412a842978eab785)
is the exact source of `v2.2.0`, published October 10, 2026. Case-insensitive
entrypoint discovery found **69 skills**, all uppercase `SKILL.md`, plus **42
command files** and **nine plugin descriptors**. The repository's "100+" wording
combines these different kinds of definition.

Its [marketplace](https://github.com/phuryn/pm-skills/blob/c68487d721e419ec87af1ae6412a842978eab785/.claude-plugin/marketplace.json)
uses relative sources for coherent domain packages, each with its own manifest,
skills, and commands. The root
[MIT license](https://github.com/phuryn/pm-skills/blob/c68487d721e419ec87af1ae6412a842978eab785/LICENSE)
and attribution must accompany any retained subset; copying a plugin directory
alone would omit that root license file.

Comparison with the canonical 178 entrypoints found zero matching directory
slugs and zero byte-identical entrypoint blobs. Purpose overlap still matters:

| Upstream candidate | Existing or related capability | Evaluation needed |
|---|---|---|
| `create-prd` | `product-requirements-designer` | Compare PRD outputs and activation conditions before adding another trigger. |
| `pre-mortem` | `premortem` | Direct purpose overlap despite different spelling. |
| `code-review` | `code-review-checklist` | Assess its additional review method against representative defects. |
| `shipping-artifacts` | Documentation, verification, and handoff skills | Compare its evidence and coverage records with existing host conventions. |
| `opportunity-solution-tree` and assumption-testing workflows | Product discovery and requirements work | A focused candidate group for task-level evaluation. |

The upstream [structural validator](https://github.com/phuryn/pm-skills/blob/c68487d721e419ec87af1ae6412a842978eab785/validate_plugins.py)
and [consistency tests](https://github.com/phuryn/pm-skills/blob/c68487d721e419ec87af1ae6412a842978eab785/tests/test_consistency.py)
are useful models for catalog membership, counts, references, and synchronized
versions. Its Markdown methods remain written specifications whose performance
requires separate task trials. Its
[release workflow](https://github.com/phuryn/pm-skills/blob/c68487d721e419ec87af1ae6412a842978eab785/.github/workflows/tag-on-merge.yml)
provides a version-consistency model, but `v2.2.0` has no uploaded built assets.
Its direct-copy examples for other assistants do not establish update recovery.

For any future import, record repository, exact commit, full folder path, Git
tree identity, complete SHA-256 file inventory and modes, original license,
transformations, command dependencies, and intended canonical destination.
Normalize metadata deliberately and trial representative tasks before admission.
The separate taxonomy candidate still requires its author's own license decision.

## Publication work and the skills window

The next publication receipt should follow the installation milestone:

1. Land the reviewed source and installer through existing rules. Retarget
   [PR #43](https://github.com/4444J99/a-i--skills/pull/43) to `main` after
   [PR #42](https://github.com/4444J99/a-i--skills/pull/42) merges.
2. Publish a new version matching the canonical manifest, attach the built
   installation archive and SHA-256 sidecar, download them again, and repeat
   installation from the downloaded artifact. The historical `v1.2.0` release
   still has zero uploaded assets at this inspection.
3. Verify the chosen directory's actual repository identity, skill paths,
   displayed source, and working installation instructions. Record a listing URL
   and observation time separately from the release and runtime receipts.

[SkillsMP's FAQ](https://skillsmp.com/docs/faq) documents daily GitHub indexing
for repositories with valid frontmatter and the topic `claude-skills` or
`claude-code-skill`. The current canonical repository topics do not include
either topic. A retrieved historical
[GDPR skill listing](https://skillsmp.com/skills/organvm-iv-taxis-a-i-skills-skills-security-gdpr-compliance-check-skill-md)
names `organvm-iv-taxis/a-i--skills` and March 2026 source activity. This is an
identity/listing reconciliation lead, not a receipt for the current catalog.

[skills.sh's FAQ](https://www.skills.sh/docs/faq) describes listing through
installation telemetry. Its
[`skills.sh.json` configuration](https://www.skills.sh/docs/customize) controls
display groups on a repository page and must be on the default branch; it does
not alter CLI discovery or installation. If used later, derive groups from the
admitted catalog and verify the resulting listing. The present local probe has
telemetry disabled and does not establish listing publication.

[agentskill.sh's submission page](https://agentskill.sh/submit) offers repository
import, daily synchronization, optional push webhooks, and ownership claiming.
Each is a separate external action. Neither a listing badge nor an upstream
author's repository establishes eligibility to approve this repository's PRs.

A later skills window can read the verified registry and show task/category
search, canonical provenance, per-skill licenses, package dependencies, current
release identity, and observed runtime status. Downloads should use the complete
validated release or independently validated package artifacts. Keep imported
candidates outside the admitted catalog until their own acceptance is complete.
