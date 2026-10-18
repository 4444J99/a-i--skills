"""Closeout ownership must be measured from content-bound remote records."""

import importlib.util
import json
import os
import shlex
import subprocess
import sys
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
            args,
            input=data,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
            env=CHECK.observation_env(),
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

    def test_hidden_index_flags_never_make_modified_files_disappear(self):
        for flag in ("--assume-unchanged", "--skip-worktree"):
            with self.subTest(flag=flag):
                self.g("update-index", flag, "tracked")
                (self.root / "tracked").write_text("hidden work")
                code, result = CHECK.check(self.document)
                self.assertEqual(code, 1)
                self.assertTrue(
                    any(row["id"] == "code:file:tracked" for row in result["dangling"])
                )
                self.g(
                    "update-index",
                    "--no-assume-unchanged",
                    "--no-skip-worktree",
                    "tracked",
                )

    def test_ignored_artifact_is_content_bound(self):
        (self.root / ".gitignore").write_text("artifact.tmp\n")
        self.g("add", ".gitignore")
        self.g("commit", "-m", "ignore generated artifact")
        self.g("push", "publisher", "HEAD:refs/heads/trunk")
        self.document["scopes"][0]["base"] = self.g("rev-parse", "HEAD").strip()
        (self.root / "artifact.tmp").write_text("important output")
        inventory = CHECK.inventory(self.document)
        item = next(
            row for row in inventory["items"] if row["id"] == "code:file:artifact.tmp"
        )
        self.assertEqual(item["content"]["status"], "!!")
        self.assertEqual(CHECK.check(self.document)[0], 1)
        self.publish_records()
        self.assertEqual(CHECK.check(self.document)[0], 0)
        (self.root / "artifact.tmp").write_text("updated output")
        self.assertEqual(CHECK.check(self.document)[0], 1)

    def test_commits_on_non_checked_out_branch_are_not_lost(self):
        self.g("switch", "-c", "unpublished")
        (self.root / "tracked").write_text("topic work")
        self.g("add", "tracked")
        self.g("commit", "-m", "topic")
        sha = self.g("rev-parse", "HEAD").strip()
        self.g("switch", "trunk")
        inventory = CHECK.inventory(self.document)
        self.assertTrue(
            any(row["id"] == "code:commit:" + sha for row in inventory["items"])
        )
        self.assertTrue(any(row["kind"] == "branch" for row in inventory["items"]))
        self.assertEqual(CHECK.check(self.document)[0], 1)

    def test_git_repository_environment_cannot_redirect_observation(self):
        (self.root / "tracked").write_text("actual changed content")
        variables = {
            "GIT_DIR": str(self.remote),
            "GIT_WORK_TREE": str(self.area),
            "GIT_INDEX_FILE": str(self.area / "foreign-index"),
            "GIT_COMMON_DIR": str(self.remote),
        }
        with patch.dict(os.environ, variables):
            self.assertEqual(CHECK.check(self.document)[0], 1)
            self.assertEqual(
                str(Path(self.g("rev-parse", "--show-toplevel").strip()).resolve()),
                str(self.root.resolve()),
            )

    def test_directory_symlink_is_a_file_obligation(self):
        (self.root / "link").symlink_to(self.area, target_is_directory=True)
        inventory = CHECK.inventory(self.document)
        self.assertTrue(
            any(row["id"] == "code:file:link" for row in inventory["items"])
        )
        self.publish_records()
        self.assertEqual(CHECK.check(self.document)[0], 0)

    def test_bare_repository_anchor_is_not_a_worktree_to_status(self):
        linked = self.area / "linked"
        self.call(
            "git", "-C", str(self.remote), "worktree", "add", str(linked), "trunk"
        )
        self.document["scopes"][0]["root"] = str(linked)
        self.call(
            "git", "-C", str(linked), "remote", "add", "publication", str(self.root)
        )
        self.call(
            "git", "-C", str(linked), "config", "branch.trunk.remote", "publication"
        )
        # Publish to the independent original repository, not the bare anchor itself.
        snapshot = CHECK.inventory(self.document)
        self.assertFalse(
            any(
                row["kind"] == "worktree" and row["content"].get("bare") is not None
                for row in snapshot["items"]
            )
        )

    def test_malformed_obligation_cli_returns_unmeasured_json(self):
        self.document["non_file_obligations"] = [None]
        evidence = self.area / "malformed.json"
        evidence.write_text(json.dumps(self.document))
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "check", "--evidence", str(evidence)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
            env=CHECK.observation_env(),
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "unmeasured")
        self.assertNotIn("Traceback", result.stderr)

    def test_malformed_remote_response_is_scoped_to_item(self):
        (self.root / "work").write_text("retained")
        self.publish_records()
        for owner in self.document["owners"].values():
            owner.update(kind="github-issue", number=9)
        with (
            patch.object(CHECK, "github_repo", return_value="example/repo"),
            patch.object(CHECK, "gh_json", return_value=[]),
        ):
            code, result = CHECK.check(self.document)
        self.assertEqual(code, 2)
        self.assertEqual(len(result["unmeasured"]), len(self.document["owners"]))

    def test_github_host_is_explicit(self):
        with (
            patch.dict(os.environ, {"GH_HOST": "enterprise.invalid"}),
            patch.object(CHECK, "run", return_value=b"{}") as observer,
        ):
            CHECK.gh_json("repos/example/repo/issues/1")
        args = observer.call_args.args[0]
        self.assertIn("--hostname", args)
        self.assertEqual(args[args.index("--hostname") + 1], "github.com")

    def test_local_self_remote_is_not_durable_publication(self):
        self.g("remote", "set-url", "publisher", ".")
        with self.assertRaises(CHECK.Unmeasured):
            CHECK.check(self.document)

    def test_remote_url_credentials_are_redacted(self):
        fake = "https://user:private-test-value@github.com/example/repo.git?token=private-test-value"  # allow-secret: synthetic redaction fixture
        self.assertEqual(CHECK.identity(fake), "github.com/example/repo")
        original = CHECK.git

        def observe(root, *args):
            if args == ("remote", "get-url", "publisher"):
                return fake.encode()
            if args[:2] == ("ls-remote", "--symref"):
                return f"ref: refs/heads/trunk\tHEAD\n{self.base}\tHEAD\n".encode()
            return original(root, *args)

        with patch.object(CHECK, "git", side_effect=observe):
            state = CHECK.remote_state(self.root)
        self.assertNotIn("private-test-value", json.dumps(state))
        self.assertEqual(state["repository"], "github.com/example/repo")

    def test_non_utf8_filename_is_reversible(self):
        # APFS refuses invalid UTF-8 filenames; exercise the raw Git index boundary.
        raw = b"binary-\xff-name"
        name = os.fsdecode(raw)
        original = CHECK.git

        def observe(root, *args):
            if args == ("ls-files", "-z"):
                return raw + b"\0"
            return original(root, *args)

        with patch.object(CHECK, "git", side_effect=observe):
            self.assertIsNone(CHECK.discover(self.root))
            self.assertFalse(CHECK.organvm_overlay(self.root))
        self.assertEqual(len(CHECK.digest({"path": name})), 64)

    def test_shared_owner_is_read_once_per_pass(self):
        (self.root / "work").write_text("retained")
        self.publish_records()
        with patch.object(CHECK, "git", wraps=CHECK.git) as observer:
            self.assertEqual(CHECK.check(self.document)[0], 0)
            first = [
                call
                for call in observer.call_args_list
                if call.args[1:3] == ("ls-remote", "publisher")
                and call.args[3:] == ("refs/heads/ownership",)
            ]
            self.assertEqual(len(first), 1)
            self.assertEqual(CHECK.check(self.document)[0], 0)
            repeated = [
                call
                for call in observer.call_args_list
                if call.args[1:3] == ("ls-remote", "publisher")
                and call.args[3:] == ("refs/heads/ownership",)
            ]
            self.assertEqual(len(repeated), 2)

    def test_scoped_instruction_discovery_is_nearest_first(self):
        nested = self.root / "component"
        nested.mkdir()
        (self.root / "AGENTS.md").write_text("# Session end\nroot procedure")
        (nested / "CLAUDE.md").write_text("# Session Review\nscoped procedure")
        self.assertEqual(
            CHECK.discover(self.root, working_directory=nested)["path"],
            str((nested / "CLAUDE.md").resolve()),
        )

    def test_empty_ledger_filename_does_not_opt_in(self):
        name = "INST-INDEX-RERUM-FACIENDARUM.md"
        (self.root / name).write_text("# Ledger example\nIRF-XXX-NNN\nDONE-NNN\n")
        self.g("add", name)
        self.assertFalse(CHECK.organvm_overlay(self.root))
        (self.root / name).write_text("# Actual ledger\nIRF-SYS-001\n")
        self.assertTrue(CHECK.organvm_overlay(self.root))

    def test_active_clean_filter_is_not_executed_by_inventory(self):
        sentinel = self.area / "filter-executed"
        command = shlex.join(
            [
                sys.executable,
                "-c",
                "from pathlib import Path; import sys; "
                + "Path("
                + repr(str(sentinel))
                + ").write_text('executed'); "
                + "sys.stdout.write(sys.stdin.read())",
            ]
        )
        self.g("config", "filter.audit.clean", command)
        (self.root / ".gitattributes").write_text("tracked filter=audit\n")
        (self.root / "tracked").write_text("changed content\n")
        with self.assertRaises(CHECK.Unmeasured):
            CHECK.inventory(self.document)
        self.assertFalse(sentinel.exists())

    def test_gitlinks_are_unmeasured_before_recursive_status(self):
        self.g(
            "update-index", "--add", "--cacheinfo", "160000," + self.base + ",nested"
        )
        with self.assertRaisesRegex(CHECK.Unmeasured, "submodule content"):
            CHECK.working_status(self.root)

    def test_unused_filter_does_not_prevent_measurement(self):
        self.g("config", "filter.unused.clean", "false")
        self.assertEqual(CHECK.inventory(self.document)["items"], [])

    def test_cached_diff_disables_external_programs(self):
        with patch.object(CHECK, "run", return_value=b"") as command:
            CHECK.git(self.root, "diff", "--cached", "--binary", "--", "tracked")
        args = command.call_args.args[0]
        self.assertIn("--no-ext-diff", args)
        self.assertIn("--no-textconv", args)

    def test_retained_landed_branch_remains_an_obligation(self):
        self.g("branch", "retained-landed", self.base)
        inventory = CHECK.inventory(self.document)
        self.assertTrue(
            any(
                row["id"] == "code:branch:refs/heads/retained-landed"
                for row in inventory["items"]
            )
        )
        self.assertEqual(CHECK.check(self.document)[0], 1)

    def test_open_pr_census_is_bound_to_local_branch(self):
        self.g("branch", "topic", self.base)
        actual_remote = CHECK.remote_state

        def remote(*args, **kwargs):
            return {
                **actual_remote(*args, **kwargs),
                "repository": "github.com/example/repo",
            }

        payload = [
            {
                "number": 7,
                "state": "open",
                "body": "remote work",
                "head": {
                    "ref": "topic",
                    "sha": self.base,
                    "repo": {"full_name": "example/repo"},
                },
            }
        ]
        with (
            patch.object(CHECK, "remote_state", side_effect=remote),
            patch.object(CHECK, "gh_json", return_value=payload),
        ):
            inventory = CHECK.inventory(self.document)
        self.assertTrue(
            any(row["id"] == "code:pull-request:7" for row in inventory["items"])
        )
        with (
            patch.object(CHECK, "remote_state", side_effect=remote),
            patch.object(
                CHECK, "gh_json", side_effect=CHECK.Unmeasured("no authentication")
            ),
        ):
            with self.assertRaises(CHECK.Unmeasured):
                CHECK.inventory(self.document)


if __name__ == "__main__":
    unittest.main()
