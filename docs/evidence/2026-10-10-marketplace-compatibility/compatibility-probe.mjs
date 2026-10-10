import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdir, readdir, readFile, writeFile, lstat, realpath, access } from 'node:fs/promises';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { discoverSkills } from './src/skills.ts';
import { installSkillForAgent } from './src/installer.ts';
import { computeSkillFolderHash } from './src/local-lock.ts';

const probeRoot = dirname(fileURLToPath(import.meta.url));
const sourceRoot = resolve(process.argv[2]);
const outputRoot = resolve(process.argv[3]);
const upstreamCommit = '13e4063a1cf913f5606d57d42ab83a86f5001e04';
const sourceCommit = '7af4cd94a485aa9e72eed0c02dd211bc35004121';
const git = (dir, ...args) => execFileSync('git', ['-C', dir, ...args], { encoding: 'utf8' }).trim();
const sha256 = (value) => createHash('sha256').update(value).digest('hex');
assert.equal(process.env.DISABLE_TELEMETRY, '1');
assert.equal(process.env.DO_NOT_TRACK, '1');
assert.equal(git(probeRoot, 'rev-parse', 'HEAD'), upstreamCommit);
assert.equal(git(sourceRoot, 'rev-parse', 'HEAD'), sourceCommit);
assert.notEqual(sourceRoot, outputRoot);
assert.ok(!outputRoot.startsWith(sourceRoot + '/'));
await mkdir(outputRoot, { recursive: false });

async function inventory(root, start = root) {
  const rows = [];
  for (const item of await readdir(start, { withFileTypes: true })) {
    const path = join(start, item.name);
    const info = await lstat(path);
    if (item.isDirectory()) rows.push(...await inventory(root, path));
    else if (item.isFile()) rows.push({ path: relative(root, path), sha256: sha256(await readFile(path)), mode: info.mode & 0o777, bytes: info.size });
    else throw new Error('Unexpected nonregular file: ' + path);
  }
  return rows.sort((a, b) => a.path.localeCompare(b.path, 'en'));
}

async function trackedSkillInputs() {
  const rows = [];
  const entries = execFileSync('git', ['-C', sourceRoot, 'ls-files', '-z', 'skills', 'plugins', 'distributions', '.claude-plugin'], { encoding: 'utf8' }).split('\0').filter(Boolean);
  for (const path of entries) {
    const info = await lstat(join(sourceRoot, path));
    assert.ok(info.isFile(), 'Expected regular tracked input ' + path);
    rows.push({ path, sha256: sha256(await readFile(join(sourceRoot, path))), mode: info.mode & 0o777 });
  }
  rows.sort((a, b) => a.path.localeCompare(b.path, 'en'));
  return { fileCount: rows.length, manifestSha256: sha256(JSON.stringify(rows)) };
}

const sourceBefore = await trackedSkillInputs();
const records = {};
for (const [label, options] of [
  ['normal', {}],
  ['fullDepth', { fullDepth: true }],
  ['normalWithDuplicates', { includeDuplicateNames: true }],
  ['fullDepthWithDuplicates', { fullDepth: true, includeDuplicateNames: true }],
]) {
  const skills = await discoverSkills(sourceRoot, undefined, options);
  const entries = skills.map(skill => ({ name: skill.name, path: relative(sourceRoot, skill.path), pluginName: skill.pluginName ?? null }));
  const buckets = entries.reduce((result, entry) => {
    const bucket = entry.path.split('/')[0];
    result[bucket] = (result[bucket] || 0) + 1;
    return result;
  }, {});
  const byName = {};
  for (const entry of entries) (byName[entry.name] ??= []).push(entry.path);
  records[label] = { options, count: entries.length, uniqueNames: Object.keys(byName).length, buckets, duplicateNames: Object.fromEntries(Object.entries(byName).filter(([, paths]) => paths.length > 1)), entries };
}

const normal = await discoverSkills(sourceRoot);
const installRecords = [];
for (const name of ['recommendation-letter', 'coliseum-orchestrator']) {
  const skill = normal.find(item => item.name === name);
  assert.ok(skill, 'Expected discoverable skill ' + name);
  const before = await inventory(skill.path);
  const markdown = await readFile(join(skill.path, 'SKILL.md'), 'utf8');
  const references = [...new Set([...markdown.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)].map(match => match[1]).filter(target => !/^[a-z][a-z0-9+.-]*:|^#/.test(target)))];
  for (const mode of ['symlink', 'copy']) {
    const cwd = join(outputRoot, name + '-' + mode);
    await mkdir(cwd);
    const result = await installSkillForAgent(skill, 'claude-code', { global: false, cwd, mode, createMissingAgentRoot: true });
    assert.equal(result.success, true);
    const physicalPath = await realpath(result.path);
    const after = await inventory(physicalPath);
    const links = [];
    for (const target of references) {
      const check = async path => { try { await access(path); return true; } catch { return false; } };
      links.push({ target, sourceExists: await check(resolve(skill.path, target)), installedExists: await check(resolve(physicalPath, target)) });
    }
    installRecords.push({
      name, mode, sourcePath: relative(sourceRoot, skill.path), result: { ...result, path: relative(outputRoot, result.path), ...(result.canonicalPath ? { canonicalPath: relative(outputRoot, result.canonicalPath) } : {}) },
      physicalPath: relative(outputRoot, physicalPath),
      sourceFolderGitTree: git(sourceRoot, 'rev-parse', sourceCommit + ':' + relative(sourceRoot, skill.path)),
      sourceFileCount: before.length,
      installedFileCount: after.length,
      fullSkillFolderPreserved: JSON.stringify(before) === JSON.stringify(after),
      sourceManifestSha256: sha256(JSON.stringify(before)),
      installedManifestSha256: sha256(JSON.stringify(after)),
      sourceLocalLockHash: await computeSkillFolderHash(skill.path),
      installedLocalLockHash: await computeSkillFolderHash(physicalPath),
      references: links,
      missingInstalledReferences: links.filter(link => link.sourceExists && !link.installedExists).length,
    });
  }
}

const sourceAfter = await trackedSkillInputs();
assert.deepEqual(sourceAfter, sourceBefore);
const lock = JSON.parse(await readFile(join(probeRoot, '.probe-runtime/package-lock.json'), 'utf8'));
const upstreamFiles = {};
for (const path of ['src/skills.ts', 'src/plugin-manifest.ts', 'src/installer.ts', 'src/local-lock.ts', 'src/agents.ts', 'src/frontmatter.ts', 'pnpm-lock.yaml', 'package.json']) {
  upstreamFiles[path] = { gitBlob: git(probeRoot, 'rev-parse', upstreamCommit + ':' + path), sha256: sha256(await readFile(join(probeRoot, path))) };
}
const receipt = {
  schemaVersion: 1,
  observedAt: new Date().toISOString(),
  scope: 'Direct execution of reviewed upstream discovery and per-skill installation APIs, using a local canonical checkout and isolated project destinations. Not a packaged CLI end-to-end test, authenticated application load, remote listing submission, or runtime model invocation.',
  telemetry: { DISABLE_TELEMETRY: process.env.DISABLE_TELEMETRY, DO_NOT_TRACK: process.env.DO_NOT_TRACK, telemetryModuleImported: false, remoteSkillSourceUsed: false },
  node: process.version,
  upstream: { repository: 'vercel-labs/skills', commit: upstreamCommit, packageVersion: JSON.parse(await readFile(join(probeRoot, 'package.json'), 'utf8')).version, files: upstreamFiles, dependencies: Object.fromEntries(Object.entries(lock.packages).filter(([key]) => key).map(([key, entry]) => [key, { version: entry.version, integrity: entry.integrity }])) },
  source: { repository: '4444J99/a-i--skills', commit: sourceCommit, gitTree: git(sourceRoot, 'rev-parse', sourceCommit + '^{tree}'), trackedSkillInputsBefore: sourceBefore, trackedSkillInputsAfter: sourceAfter, unchanged: true },
  discovery: records,
  installation: installRecords,
  probeSha256: sha256(await readFile(fileURLToPath(import.meta.url))),
};
await writeFile(join(outputRoot, 'receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify({ source: receipt.source, discovery: Object.fromEntries(Object.entries(records).map(([name, record]) => [name, { count: record.count, uniqueNames: record.uniqueNames, buckets: record.buckets, duplicateNameCount: Object.keys(record.duplicateNames).length }])), installation: installRecords, receipt: join(outputRoot, 'receipt.json') }, null, 2));
