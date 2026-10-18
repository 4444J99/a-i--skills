"""Closeout ownership must be measured from content-bound remote records."""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/tools/closeout/scripts/closeout_check.py"
)
SPEC = importlib.util.spec_from_file_location("closeout_check", SCRIPT)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class CloseoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.area = Path(self.temp.name)
        self.root = self.area / "work"
        self.remote = self.area / "remote.git"
        self.call("git", "init", "--bare", "--initial-branch=trunk", str(self.remote))
        self.call("git", "init", "--initial-branch=trunk", str(self.root))
        self.g("config", "user.name", "Closeout Test")
        self.g("config", "user.email", "test@example.invalid")
        self.g("config", "commit.gpgsign", "false")
        (self.root / "tracked").write_text("base\n")
        self.g("add", "tracked")
        self.g("commit", "-m", "base")
        self.base = self.g("rev-parse", "HEAD").strip()
        self.g("remote", "add", "publisher", str(self.remote))
        self.g("push", "publisher", "HEAD:refs/heads/trunk")
        self.document = {
            "schema": "closeout.evidence.v1",
            "session_id": "native-test-session",
            "scopes": [{"id": "code", "root": str(self.root), "base": self.base}],
            "non_file_obligations": [],
            "owners": {},
        }

    def call(self, *args, data=None):
        result = subprocess.run(
            args, input=data, check=False, capture_output=True, text=True, timeout=15
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def g(self, *args, data=None):
        return self.call("git", "-C", str(self.root), *args, data=data)

    def publish_records(self, disposition="owned"):
        snapshot = CHECK.inventory(self.document)
        records = []
        for item in snapshot["items"]:
            state = snapshot["scopes"][item["scope"]]
            records.append(
                {
                    "binding": CHECK.binding(
                        self.document["session_id"], state["repository"], item
                    ),
                    "disposition": disposition,
                    "owner": "existing-owner",
                    "next_action": "finish acceptance",
                    "rationale": "other native session",
                    "source_session": "native-other-session",
                }
            )
            self.document["owners"][item["id"]] = {
                "kind": "git-record",
                "fingerprint": item["fingerprint"],
                "ref": "refs/heads/ownership",
                "path": "record.json",
                "disposition": disposition,
            }
        if disposition == "excluded":
            sources = []
            for record in records:
                record["source_evidence"] = {
                    "kind": "git-record",
                    "ref": "refs/heads/ownership",
                    "path": "record.json",
                }
                sources.append(
                    {
                        **record,
                        "disposition": "owned",
                        "binding": {
                            **record["binding"],
                            "session_id": record["source_session"],
                        },
                    }
                )
            records.extend(sources)
        blob = self.g("hash-object", "-w", "--stdin", data=json.dumps(records)).strip()
        tree = self.g("mktree", data=f"100644 blob {blob}\trecord.json\n").strip()
        commit = self.g(
            "-c", "commit.gpgsign=false", "commit-tree", tree, data="ownership\n"
        ).strip()
        self.g("push", "publisher", f"{commit}:refs/heads/ownership")
        return records

    def test_clean_inventory_and_missing_upstream(self):
        before = (self.root / ".git/index").read_bytes()
        result = CHECK.inventory(self.document)
        self.assertEqual(result["items"], [])
        self.assertIsNone(result["scopes"]["code"]["upstream"])
        self.assertEqual(result["scopes"]["code"]["remote"], "publisher")
        self.assertEqual(result["scopes"]["code"]["default_ref"], "refs/heads/trunk")
        self.assertEqual(CHECK.check(self.document)[0], 0)
        self.assertEqual((self.root / ".git/index").read_bytes(), before)

    def test_unknown_change_is_dangling_despite_success_flags(self):
        (self.root / "retained").write_text("work")
        self.document["complete"] = True
        self.document["verified"] = True
        code, result = CHECK.check(self.document)
        self.assertEqual(code, 1)
        self.assertTrue(result["dangling"])
        self.assertFalse(result["session_released"])

    def test_remote_owned_retained_work_and_stale_content(self):
        (self.root / "retained").write_text("work")
        self.publish_records()
        first = CHECK.check(self.document)
        second = CHECK.check(self.document)
        self.assertEqual((first[0], second[0]), (0, 0))
        self.assertEqual(
            first[1]["inventory_fingerprint"], second[1]["inventory_fingerprint"]
        )
        (self.root / "retained").write_text("changed after receipt")
        self.assertEqual(CHECK.check(self.document)[0], 1)

    def test_unpublished_handoff_cannot_pass(self):
        (self.root / "handoff.md").write_text("unfinished work")
        self.publish_records()
        self.g("push", "publisher", ":refs/heads/ownership")
        self.assertEqual(CHECK.check(self.document)[0], 2)

    def test_exclusions_need_remote_session_and_rationale(self):
        (self.root / "other-session").write_text("preserved")
        self.publish_records(disposition="excluded")
        self.assertEqual(CHECK.check(self.document)[0], 0)
        with patch.object(CHECK, "read_record", return_value={"complete": True}):
            self.assertEqual(CHECK.check(self.document)[0], 1)

    def test_non_file_obligations_require_durable_owner(self):
        self.document["non_file_obligations"] = [
            {
                "id": "inline",
                "scope": "code",
                "description": "substantive inline report",
            }
        ]
        self.assertEqual(CHECK.check(self.document)[0], 1)
        self.publish_records()
        self.assertEqual(CHECK.check(self.document)[0], 0)
        del self.document["non_file_obligations"]
        with self.assertRaises(CHECK.Unmeasured):
            CHECK.check(self.document)

    def test_generic_copy_skipped_but_custom_codex_overlay_preserved(self):
        invoked = SCRIPT.parents[1] / "SKILL.md"
        generic = self.root / ".agents/skills/closeout/SKILL.md"
        generic.parent.mkdir(parents=True)
        generic.write_bytes(invoked.read_bytes())
        custom = self.root / ".codex/skills/closeout/SKILL.md"
        custom.parent.mkdir(parents=True)
        custom.write_bytes(invoked.read_bytes() + b"\nCustom local protocol\n")
        self.assertEqual(CHECK.discover(self.root)["path"], str(custom))
        custom.unlink()
        (self.root / "CLAUDE.md").write_text("# Session end\nRun local predicate\n")
        self.assertEqual(CHECK.discover(self.root)["kind"], "instructions")

    def test_documentation_and_bundled_organvm_examples_do_not_opt_in(self):
        for name in ("docs/example.md", "skills/tools/example/SKILL.md"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("<!-- ORGANVM:AUTO:START -->\nDONE-123 IRF-SYS-111")
            self.g("add", name)
        self.assertFalse(CHECK.organvm_overlay(self.root))
        (self.root / "AGENTS.md").write_text("<!-- ORGANVM:AUTO:START -->\n")
        self.g("add", "AGENTS.md")
        self.assertTrue(CHECK.organvm_overlay(self.root))

    def test_github_readback_and_inaccessible_evidence(self):
        (self.root / "retained").write_text("work")
        records = self.publish_records()
        for owner in self.document["owners"].values():
            owner.update(kind="github-issue", number=7)
        with patch.object(
            CHECK, "read_record", side_effect=CHECK.Unmeasured("auth unavailable")
        ):
            self.assertEqual(CHECK.check(self.document)[0], 2)
        state = {"repository": "github.com/example/repo"}
        owner = {"kind": "github-issue", "number": 7}
        with patch.object(
            CHECK,
            "gh_json",
            return_value={
                "state": "open",
                "body": "<!-- closeout-owner\n" + json.dumps(records[0]) + "\n-->",
            },
        ):
            self.assertEqual(CHECK.read_record(owner, state), records[0])

    def test_squash_landing_requires_repository_qualified_pr_and_landed_commit(self):
        item = {"kind": "commit", "content": {"sha": "original-feature-sha"}}
        state = {
            "repository": "github.com/example/repo",
            "root": str(self.root),
            "default_tip": self.base,
        }
        pull = {
            "state": "closed",
            "merged_at": "2026-01-01",
            "merge_commit_sha": self.base,
            "base": {"repo": {"clone_url": "https://github.com/example/repo.git"}},
        }
        with patch.object(
            CHECK, "gh_json", side_effect=[pull, [{"sha": "original-feature-sha"}]]
        ):
            self.assertTrue(CHECK.landed({"pull_request": 5}, state, item))
        pull["base"]["repo"]["clone_url"] = "https://github.com/other/repo.git"
        with patch.object(CHECK, "gh_json", return_value=pull):
            self.assertFalse(CHECK.landed({"pull_request": 5}, state, item))

    def test_unpublished_head_cannot_be_claimed_as_empty_session_base(self):
        (self.root / "tracked").write_text("unpublished")
        self.g("add", "tracked")
        self.g("commit", "-m", "unpublished")
        self.document["scopes"][0]["base"] = self.g("rev-parse", "HEAD").strip()
        with self.assertRaises(CHECK.Unmeasured):
            CHECK.check(self.document)

    def test_sibling_worktree_changes_invalidate_retained_owner(self):
        sibling = self.area / "sibling"
        self.g("worktree", "add", "-b", "other", str(sibling))
        self.publish_records()
        self.assertEqual(CHECK.check(self.document)[0], 0)
        (sibling / "untracked").write_text("other session changed")
        self.assertEqual(CHECK.check(self.document)[0], 1)

    def test_git_replace_cannot_forge_remote_owner_content(self):
        (self.root / "retained").write_text("work")
        self.publish_records()
        tip = self.g("ls-remote", "publisher", "refs/heads/ownership").split()[0]
        tree = self.g("mktree", data="").strip()
        forged = self.g(
            "-c", "commit.gpgsign=false", "commit-tree", tree, data="local forgery"
        ).strip()
        self.g("replace", tip, forged)
        self.assertEqual(CHECK.check(self.document)[0], 0)

    def test_remote_owner_tip_change_alters_readback_fingerprint(self):
        (self.root / "retained").write_text("work")
        self.publish_records()
        first = CHECK.check(self.document)[1]
        # Move its owner branch to a different immutable commit with identical record bytes.
        tip = self.g("ls-remote", "publisher", "refs/heads/ownership").split()[0]
        tree = self.g("--no-replace-objects", "rev-parse", tip + "^{tree}").strip()
        moved = self.g(
            "-c",
            "commit.gpgsign=false",
            "commit-tree",
            tree,
            "-p",
            tip,
            data="owner readback generation",
        ).strip()
        self.g("push", "publisher", f"{moved}:refs/heads/ownership")
        second = CHECK.check(self.document)[1]
        self.assertNotEqual(
            first["readback_fingerprint"], second["readback_fingerprint"]
        )

    def test_cli_twice_and_malformed_evidence(self):
        evidence = self.area / "evidence.json"
        evidence.write_text(json.dumps(self.document))
        result = subprocess.run(
            ["python3", str(SCRIPT), "check", "--evidence", str(evidence), "--twice"],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["passes"], [0, 0])
        self.assertTrue(json.loads(result.stdout)["stable"])
        evidence.write_text("[]")
        result = subprocess.run(
            ["python3", str(SCRIPT), "check", "--evidence", str(evidence)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
