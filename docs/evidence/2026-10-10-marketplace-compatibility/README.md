# Marketplace compatibility evidence

Observed October 10, 2026. See the
[evaluation and decisions](../../marketplace-evaluation.md).

## Scope

These are direct executions of reviewed Vercel discovery and per-skill
installation APIs against local inputs. They are not end-to-end tests of the
published npm CLI package, remote listing submissions, user/global installations,
skill workflow executions, signed-in model calls, or native application loading.
Telemetry was disabled, and the direct APIs do not import its module.

Both probes use:

| Input | Exact identity |
|---|---|
| Canonical source | `4444J99/a-i--skills@7af4cd94a485aa9e72eed0c02dd211bc35004121` |
| Canonical tree | `fdbb2aa9c5856bdba0198e1c8b189c4b70563059` |
| Upstream APIs | `vercel-labs/skills@13e4063a1cf913f5606d57d42ab83a86f5001e04` |
| Node runtime | `v24.19.0` |
| Runtime dependencies | `yaml@2.9.0`, `xdg-basedir@5.1.0`; exact integrity values in the preserved lockfile |

The upstream package metadata declares `1.7.2`. This receipt identifies the Git
commit actually executed and does not assert npm-package equivalence. Only the
two dependencies imported by these API paths were installed; lifecycle scripts
were disabled. Their versions and integrities match the inspected upstream
`pnpm-lock.yaml`. The preserved [runtime lock](runtime/package-lock.json) also
allows a fresh `npm ci` preparation with those same packages.

## Results

| Probe | Observation |
|---|---|
| Normal and full-depth discovery | Each returns 178 unique definitions at canonical skill/plugin paths. |
| Full depth retaining duplicate names | Returns 679 entries: 178 canonical definitions and 501 generated copies. Its depth limit omits the deeper Gemini copies, so this is not an exhaustive duplicate inventory. |
| Standalone installation | `recommendation-letter` preserves both files and its rubric link in symlink and copy modes. |
| Plugin skill installation | `coliseum-orchestrator` reports success and preserves its one-file skill folder in both modes, but all four links to plugin-level references fail to resolve. Its matching folder hash does not cover those external dependencies. |
| Source without generated output | Removing `distributions/` and `.claude-plugin/marketplace.json` from an exact source archive yields 167 via normal discovery and 178 via full depth. |
| Canonical staged build | Build and explicit validation succeed; the verified release yields 178 via both discovery modes. All 969 stripped-source files remain unchanged, and removed generated paths remain absent there. |

The first probe compares 3,768 tracked skill, plugin, distribution, and manifest
inputs before and after execution. They are unchanged. It records complete
discovered name/path lists and per-install resource checks in
[compatibility-receipt.json](compatibility-receipt.json).

The second probe's source is a Git archive without `.git`, so the release
manifest correctly records `source.commit: null`. The
[stripped-source receipt](stripped-source-receipt.json) records the originating
commit, tree, archive SHA-256, remaining source inventory SHA-256, generated build
identity, and log hashes. The archive fixture's build identity is
`b6eb5d37729ac675796765c562378d6408ca4122f04d17614f8faedf3208d62e`.
It should not be confused with an artifact built from a Git checkout or a
published release.

## Reproduce

Requirements: Git, tar, Python 3.11 or later, Node with native TypeScript support
(the observed run used Node 24.19.0), and npm. The following preparation uses a
new temporary workspace and leaves the current checkout unchanged. Run it from
the root of the checkout containing these evidence files. The two output
directories must not already exist.

```sh
skills_evidence=$(pwd)/docs/evidence/2026-10-10-marketplace-compatibility
skills_probe_workspace=$(mktemp -d)

git clone https://github.com/4444J99/a-i--skills.git "$skills_probe_workspace/canonical"
git -C "$skills_probe_workspace/canonical" checkout --detach 7af4cd94a485aa9e72eed0c02dd211bc35004121
git clone https://github.com/vercel-labs/skills.git "$skills_probe_workspace/upstream"
git -C "$skills_probe_workspace/upstream" checkout --detach 13e4063a1cf913f5606d57d42ab83a86f5001e04

cp "$skills_evidence/compatibility-probe.mjs" "$skills_probe_workspace/upstream/"
cp "$skills_evidence/stripped-source-probe.mjs" "$skills_probe_workspace/upstream/"
mkdir "$skills_probe_workspace/upstream/.probe-runtime"
cp "$skills_evidence/runtime/package.json" "$skills_probe_workspace/upstream/.probe-runtime/"
cp "$skills_evidence/runtime/package-lock.json" "$skills_probe_workspace/upstream/.probe-runtime/"
npm ci --prefix "$skills_probe_workspace/upstream/.probe-runtime" --ignore-scripts --no-audit --no-fund
ln -s .probe-runtime/node_modules "$skills_probe_workspace/upstream/node_modules"

DISABLE_TELEMETRY=1 DO_NOT_TRACK=1 node "$skills_probe_workspace/upstream/compatibility-probe.mjs" \
  "$skills_probe_workspace/canonical" "$skills_probe_workspace/compatibility"
DISABLE_TELEMETRY=1 DO_NOT_TRACK=1 node "$skills_probe_workspace/upstream/stripped-source-probe.mjs" \
  "$skills_probe_workspace/canonical" "$skills_probe_workspace/stripped-source"
```

The original preparation used `npm install --ignore-scripts --no-audit --no-fund
--save-exact yaml@2.9.0 xdg-basedir@5.1.0` in the separate runtime directory. The
instructions above use its preserved lockfile. The harnesses assert the source
and upstream HEAD identities, require disabled telemetry, and create fresh
output directories. Run them only in this isolated layout; they intentionally
import upstream `src/` files relative to their own location.

Timestamps and output-location strings can change on a rerun. Compare source
identities, dependency integrity, discovery membership, folder inventories,
resource results, and build identities rather than demanding identical receipt
bytes after timestamps change.

## Preserved artifact hashes

| File | SHA-256 |
|---|---|
| [compatibility-probe.mjs](compatibility-probe.mjs) | `f727436682576a31c751c0d595ca99179384443b93a6488a77ed7c73c86e9044` |
| [compatibility-receipt.json](compatibility-receipt.json) | `60631837fb5c77c70669abb9e5037f467a1e2541e0d7595f91cec61bb0a11d5e` |
| [stripped-source-probe.mjs](stripped-source-probe.mjs) | `db64b17c20cdbd4916693078d22bc911b35846adc9f521f17792869061321ce7` |
| [stripped-source-receipt.json](stripped-source-receipt.json) | `2a03bbfa7d47c66b9d582eaca818a15157b7fdcf9213ea828a3938ff25a4df72` |
| [build.log](build.log) | `8eef15e0f53455b93a8be2153f4471dc10f82dda1b0177ce6044e882a994af5d` |
| [validation.log](validation.log) | `5d46467e0c7cc56466e73192197fef446ac5559b5863912aebd2b1bab34bcbf5` |
