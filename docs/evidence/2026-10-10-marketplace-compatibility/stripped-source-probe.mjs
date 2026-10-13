import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdir, readFile, writeFile, rm, lstat, readdir } from 'node:fs/promises';
import { join, relative, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { discoverSkills } from './src/skills.ts';

const probeRoot = dirname(fileURLToPath(import.meta.url));
const canonical = resolve(process.argv[2]);
const outputRoot = resolve(process.argv[3]);
const sourceCommit = '7af4cd94a485aa9e72eed0c02dd211bc35004121';
const upstreamCommit = '13e4063a1cf913f5606d57d42ab83a86f5001e04';
const git = (root, ...args) => execFileSync('git', ['-C', root, ...args], { encoding: 'utf8' }).trim();
const hash = buffer => createHash('sha256').update(buffer).digest('hex');
assert.equal(process.env.DISABLE_TELEMETRY, '1');
assert.equal(process.env.DO_NOT_TRACK, '1');
assert.equal(git(canonical, 'rev-parse', 'HEAD'), sourceCommit);
assert.equal(git(probeRoot, 'rev-parse', 'HEAD'), upstreamCommit);
assert.ok(!outputRoot.startsWith(canonical + '/'));
await mkdir(outputRoot, { recursive: false });
const archive = join(outputRoot, 'canonical.tar');
const source = join(outputRoot, 'source');
const release = join(outputRoot, 'release');
await mkdir(source);
execFileSync('git', ['-C', canonical, 'archive', '--format=tar', '--output=' + archive, sourceCommit]);
execFileSync('tar', ['-xf', archive, '-C', source]);
const archiveSha256 = hash(await readFile(archive));
const removed = ['distributions', '.claude-plugin/marketplace.json'];
for (const path of removed) await rm(join(source, path), { recursive: true });
const absent = async path => { try { await lstat(path); return false; } catch (e) { if (e.code === 'ENOENT') return true; throw e; } };
for (const path of removed) assert.equal(await absent(join(source, path)), true);

async function inventory(root, current = root) {
  const rows = [];
  for (const entry of await readdir(current, { withFileTypes: true })) {
    const path = join(current, entry.name);
    if (entry.isDirectory()) rows.push(...await inventory(root, path));
    else {
      const info = await lstat(path);
      assert.ok(info.isFile(), 'Expected regular file ' + path);
      rows.push({ path: relative(root, path), sha256: hash(await readFile(path)), mode: info.mode & 0o777 });
    }
  }
  return rows.sort((a, b) => a.path.localeCompare(b.path, 'en'));
}

async function discovery(root) {
  const result = {};
  for (const [name, options] of [['normal', {}], ['fullDepth', { fullDepth: true }]]) {
    const skills = await discoverSkills(root, undefined, options);
    const entries = skills.map(skill => ({ name: skill.name, path: relative(root, skill.path), pluginName: skill.pluginName ?? null }));
    result[name] = { options, count: entries.length, buckets: entries.reduce((counts, entry) => { const key = entry.path.split('/')[0]; counts[key] = (counts[key] ?? 0) + 1; return counts; }, {}), entries };
  }
  return result;
}

const before = await inventory(source);
const strippedDiscovery = await discovery(source);
const buildArgs = ['-B', join(source, 'scripts/skills_install.py'), 'build', '--source', source, '--output', release];
const buildLog = execFileSync('python3', buildArgs, { encoding: 'utf8', env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' }, maxBuffer: 8 * 1024 * 1024 });
await writeFile(join(outputRoot, 'build.log'), buildLog);
const validationLog = execFileSync('python3', ['-B', join(source, 'scripts/skills_install.py'), 'validate', '--release', release], { encoding: 'utf8', env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' } });
await writeFile(join(outputRoot, 'validation.log'), validationLog);
const verifiedDiscovery = await discovery(release);
const after = await inventory(source);
assert.deepEqual(after, before);
for (const path of removed) assert.equal(await absent(join(source, path)), true);
const manifest = JSON.parse(await readFile(join(release, 'build-manifest.json'), 'utf8'));
const receipt = {
  schemaVersion: 1,
  observedAt: new Date().toISOString(),
  scope: 'Local-only direct upstream discovery API on an exact Git archive with two generated paths removed, followed by the canonical staged build/validate and discovery of its verified release. The source archive has no .git directory, so build-manifest source.commit is null; provenance is recorded externally here. No packaged CLI invocation, remote skill installation, listing submission, global installation, or model invocation.',
  node: process.version,
  telemetry: { DISABLE_TELEMETRY: '1', DO_NOT_TRACK: '1', telemetryModuleImported: false },
  upstreamCommit,
  source: { repository: '4444J99/a-i--skills', commit: sourceCommit, tree: git(canonical, 'rev-parse', sourceCommit + '^{tree}'), archiveSha256, removedPaths: removed, strippedSourceFileCount: before.length, strippedSourceManifestSha256: hash(JSON.stringify(before)), sourceUnchangedByBuild: true, generatedPathsStillAbsentInSource: true },
  build: { command: ['python3', ...buildArgs.map(arg => arg.startsWith(outputRoot) ? '$OUTPUT/' + relative(outputRoot, arg) : arg)], exitCode: 0, stdoutSha256: hash(buildLog), validationExitCode: 0, validationStdoutSha256: hash(validationLog), releaseManifestSha256: hash(await readFile(join(release, 'build-manifest.json'))), buildId: manifest.build_id, releaseSourceCommit: manifest.source.commit, sourceInputSha256: manifest.source.input_sha256, counts: manifest.counts },
  discovery: { strippedSource: strippedDiscovery, verifiedRelease: verifiedDiscovery },
  probeSha256: hash(await readFile(fileURLToPath(import.meta.url))),
};
await writeFile(join(outputRoot, 'receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify({ source: receipt.source, build: { buildId: receipt.build.buildId, releaseSourceCommit: receipt.build.releaseSourceCommit, exitCode: 0, validationExitCode: 0 }, discovery: Object.fromEntries(Object.entries(receipt.discovery).map(([name, modes]) => [name, Object.fromEntries(Object.entries(modes).map(([mode, data]) => [mode, { count: data.count, buckets: data.buckets }]))])), receipt: join(outputRoot, 'receipt.json') }, null, 2));
