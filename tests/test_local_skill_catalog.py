"""Safety and preservation checks for the opt-in local collection tool."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "local_skill_catalog.py"
SPEC = importlib.util.spec_from_file_location("local_skill_catalog", MODULE)
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "source"
        self.source.mkdir()
        self.output = self.root / "collection"

    def skill(self, name, resource=b"hello", filename="SKILL.md"):
        folder = self.source / name
        folder.mkdir(parents=True)
        (folder / filename).write_text('---\nname: "shared"\ndescription: >-\n  first line\n  second line\n---\n# Skill\n')
        (folder / "asset.bin").write_bytes(resource)
        return folder

    def build(self, **kwargs):
        return catalog.build([dict(id="test", path=str(self.source), kind="repository",
                                   working_directory="/original/work")], self.output, **kwargs)

    def test_complete_package_duplicates_preserve_provenance(self):
        self.skill("a")
        self.skill("b")
        result = self.build()
        self.assertEqual(result["counts"], dict(objects=1, occurrences=2))
        self.assertEqual(len(result["exact_duplicates"]), 1)
        self.assertTrue(all(x["working_directory"] == "/original/work" for x in result["occurrences"]))
        self.assertEqual(result["occurrences"][0]["description"], "first line second line")
        self.assertFalse(result["incomplete"])
        self.assertTrue(catalog.verify(self.output / "catalog.json")["verified"])

    def test_resources_and_executable_bits_are_identity(self):
        self.skill("a", b"one")
        self.skill("b", b"two")
        folder = self.skill("c", b"one")
        (folder / "asset.bin").chmod(0o744)
        result = self.build()
        self.assertEqual(len(result["objects"]), 3)
        self.assertEqual(len(result["same_name_variants"]["shared"]), 3)

    def test_aggregate_catalog_reads_are_independent_of_package_file_limit(self):
        import contextlib
        import io
        import sys

        self.skill("a")
        self.skill("b")
        self.assertFalse(self.build(limits=catalog.Limits(file_bytes=1024))["incomplete"])
        path = self.output / "catalog.json"
        self.assertGreater(path.stat().st_size, 1024)
        try:
            report = catalog.verify(path, catalog.Limits(file_bytes=1024))
        except catalog.LimitError as error:
            self.fail(f"Aggregate catalog incorrectly uses the package file limit: {error}")
        self.assertTrue(report["verified"])
        stdout = io.StringIO()
        with patch.object(sys, "argv", [str(MODULE), "--catalog", str(path),
                                       "--find", "shared", "--max-file-bytes", "1024"]), \
                contextlib.redirect_stdout(stdout):
            self.assertEqual(catalog.main(), 0)
        self.assertEqual(len(stdout.getvalue().splitlines()), 2)

    def test_catalog_byte_limit_prevents_publication_and_bounds_readers(self):
        import contextlib
        import io
        import sys

        self.skill("a")
        with self.assertRaises(catalog.LimitError):
            self.build(limits=catalog.Limits(catalog_bytes=1024))
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob(".collection-*")), [])
        self.build()
        path = self.output / "catalog.json"
        with self.assertRaises(catalog.LimitError):
            catalog.verify(path, catalog.Limits(catalog_bytes=1024))
        stderr = io.StringIO()
        with patch.object(sys, "argv", [str(MODULE), "--catalog", str(path),
                                       "--find", "shared", "--max-catalog-bytes", "1024"]), \
                contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as error:
            catalog.main()
        self.assertEqual(error.exception.code, 1)
        self.assertIn("catalog", stderr.getvalue().lower())

    def test_inaccessible_source_keeps_successful_sources_and_incomplete_status(self):
        self.skill("a")
        inaccessible = self.root / "private-parent" / "skills"
        original_is_dir = Path.is_dir

        def check_access(path):
            if path == inaccessible:
                raise PermissionError("parent directory is not traversable")
            return original_is_dir(path)

        sources = [dict(id="good", path=str(self.source), kind="repo"),
                   dict(id="denied", path=str(inaccessible), kind="runtime")]
        with patch.object(Path, "is_dir", check_access):
            try:
                result = catalog.build(sources, self.output)
            except PermissionError as error:
                self.fail(f"One inaccessible root aborted the whole inventory: {error}")
        self.assertTrue(result["incomplete"])
        self.assertEqual(result["counts"], dict(objects=1, occurrences=1))
        self.assertEqual(result["sources"][1]["status"], "incomplete")
        self.assertIn("not traversable", result["sources"][1]["error"])
        report = catalog.verify(self.output / "catalog.json")
        self.assertTrue(report["retained_objects_verified"])
        self.assertFalse(report["catalog_complete"])

    def test_case_insensitive_discovery(self):
        self.skill("a", filename="skill.md")
        self.assertEqual(self.build()["counts"]["objects"], 1)

    def test_broken_and_nested_links_are_not_traversed(self):
        self.skill("a")
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        (elsewhere / "SKILL.md").write_text("secret outside package")
        (self.source / "outside").symlink_to(elsewhere, target_is_directory=True)
        (self.source / "broken").symlink_to(self.root / "missing")
        (self.source / "loop").symlink_to(self.source, target_is_directory=True)
        result = self.build()
        self.assertEqual(result["counts"]["occurrences"], 1)
        self.assertEqual({x["status"] for x in result["events"]}, {"symlink-skipped", "broken-symlink"})
        self.assertEqual(len(result["events"]), 3)
        self.assertEqual({x["path"] for x in result["events"]},
                         {str(self.source / name) for name in ("outside", "broken", "loop")})

    def test_root_marker_is_not_a_collection_package(self):
        (self.source / "SKILL.md").write_text("collection marker")
        self.skill("a")
        self.assertEqual(self.build()["counts"], dict(objects=1, occurrences=1))

    def test_index_metadata_cannot_introduce_markup(self):
        folder = self.skill("a")
        (folder / "SKILL.md").write_text('---\nname: <script>alert(1)</script> [link](https://example.com)\n---\n')
        self.build()
        text = (self.output / "INDEX.md").read_text()
        self.assertNotIn("<script>", text)
        self.assertNotIn("[link]", text)

    def test_index_preview_bounds_large_name_without_losing_catalog_metadata(self):
        folder = self.skill("a")
        name = "a" * 250000 + "<script>outside preview</script>"
        (folder / "SKILL.md").write_text(f"---\nname: {name}\n---\n")
        result = self.build()
        preview = (self.output / "INDEX.md").read_text()
        self.assertEqual(result["occurrences"][0]["name"], name)
        self.assertLess(len(preview), 32768)
        self.assertNotIn("<script>", preview)

    def test_directory_replacement_before_enumeration_cannot_discover_external_skill(self):
        folder = self.source / "candidate"
        folder.mkdir()
        identity = (folder.stat().st_dev, folder.stat().st_ino)
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "SKILL.md").write_text("---\nname: outside\n---\n")
        original = os.scandir
        replaced = []

        def exchange_before_scandir(directory):
            info = os.fstat(directory) if isinstance(directory, int) else Path(directory).stat()
            if (info.st_dev, info.st_ino) == identity and not replaced:
                folder.rename(self.root / "original-directory")
                folder.symlink_to(outside, target_is_directory=True)
                replaced.append(True)
            return original(directory)

        with patch.object(catalog.os, "scandir", exchange_before_scandir):
            result = self.build()
        self.assertEqual(result["counts"]["occurrences"], 0)
        self.assertTrue(result["incomplete"])
        self.assertTrue(any(event["path"] == str(folder) and event["status"] == "scan-error"
                            for event in result["events"]))

    def test_manifest_rejects_file_replacement_with_changed_executable_bits(self):
        folder = self.skill("a")
        resource = folder / "asset.bin"
        original = catalog.regular_bytes
        for old_mode, new_mode in ((0o644, 0o755), (0o755, 0o644)):
            with self.subTest(old_mode=old_mode, new_mode=new_mode):
                resource.chmod(old_mode)
                replaced = []

                def exchange_before_read(path, limits, **kwargs):
                    if path == resource and not replaced:
                        replacement = self.root / "replacement"
                        replacement.write_bytes(b"new contents")
                        replacement.chmod(new_mode)
                        os.replace(replacement, resource)
                        replaced.append(True)
                    return original(path, limits, **kwargs)

                with patch.object(catalog, "regular_bytes", exchange_before_read):
                    with self.assertRaisesRegex(ValueError, "file changed"):
                        catalog.package_manifest(folder, catalog.Limits())

    def test_directory_replacement_before_read_cannot_expose_external_metadata(self):
        folder = self.skill("a")
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "SKILL.md").write_text("---\nname: external metadata\n---\n")
        original = catalog.regular_bytes
        replaced = []

        def exchange_before_read(path, limits, **kwargs):
            if path == folder / "SKILL.md" and not replaced:
                folder.rename(self.root / "original-directory")
                folder.symlink_to(outside, target_is_directory=True)
                replaced.append(True)
            return original(path, limits, **kwargs)

        with patch.object(catalog, "regular_bytes", exchange_before_read):
            result = self.build()
        self.assertNotIn("name", result["occurrences"][0])
        self.assertEqual(result["objects"], {})
        self.assertTrue(result["incomplete"])

    def test_malformed_sources_are_validation_errors(self):
        for value in ({}, [dict(id=[], path="x", kind="repository")],
                      [dict(id="a", path="", kind="repository")],
                      [dict(id="a", path=None, kind="repository")]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                catalog.build(value, self.output)
            self.assertFalse(self.output.exists())

    def test_malformed_catalog_is_validation_error(self):
        self.output.mkdir()
        path = self.output / "catalog.json"
        for value in ([], {}, dict(objects={"abc": None}, incomplete=False, occurrences=[]),
                      dict(objects={"abc": {"path": "x", "files": None}}, incomplete=False, occurrences=[])):
            path.write_text(json.dumps(value))
            with self.subTest(value=value), self.assertRaises(ValueError):
                catalog.verify(path)

    def test_directory_enumeration_stops_at_limit(self):
        for name in range(10):
            (self.source / str(name)).touch()
        with self.assertRaises(catalog.LimitError):
            catalog.bounded_children(self.source, catalog.Limits(entries=3))

    def test_interrupted_publication_can_be_retried(self):
        self.skill("a")
        with patch.object(catalog.os, "replace", side_effect=OSError("publish failed")):
            with self.assertRaises(OSError):
                self.build()
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob(".collection-*")), [])
        self.assertFalse(self.build()["incomplete"])

    def test_incomplete_search_reports_coverage(self):
        import subprocess
        self.skill("a")
        self.build()
        path = self.output / "catalog.json"
        data = json.loads(path.read_text())
        data["incomplete"] = True
        path.write_text(json.dumps(data))
        result = subprocess.run([__import__("sys").executable, str(MODULE),
                                 "--catalog", str(path), "--find", "absent"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("incomplete catalog", result.stderr)

    def test_metadata_describes_verified_object_after_source_replacement(self):
        folder = self.skill("a")
        original = catalog.package_manifest
        replaced = []

        def replace_before_manifest(root, limits, excluded=None):
            if root == folder and not replaced:
                (folder / "SKILL.md").write_text("---\nname: replacement\ndescription: new content\n---\n")
                replaced.append(True)
            return original(root, limits, excluded)

        with patch.object(catalog, "package_manifest", replace_before_manifest):
            result = self.build()
        self.assertEqual(result["occurrences"][0]["name"], "replacement")
        self.assertEqual(result["occurrences"][0]["description"], "new content")
        self.assertEqual(set(result["same_name_variants"]), set())

    def test_package_limit_counts_actual_read_bytes(self):
        folder = self.skill("a", b"small")
        original = catalog.regular_bytes

        def expanded(path, limits, **kwargs):
            data = original(path, limits, **kwargs)
            return data + b"x" * 1000 if path.name == "asset.bin" else data

        with patch.object(catalog, "regular_bytes", expanded):
            with self.assertRaises(catalog.LimitError):
                catalog.package_manifest(folder, catalog.Limits(package_bytes=500))

    def test_search_includes_review_events_and_missing_source_paths(self):
        import subprocess
        self.skill("a")
        (self.source / "review-only-link").symlink_to(self.root / "missing")
        self.build()
        result = subprocess.run([__import__("sys").executable, str(MODULE),
                                 "--catalog", str(self.output / "catalog.json"),
                                 "--find", "review-only-link"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("broken-symlink", result.stdout)
        data = json.loads((self.output / "catalog.json").read_text())
        data["sources"].append(dict(path="/missing-source-unique", status="missing-or-invalid-root"))
        data["incomplete"] = True
        (self.output / "catalog.json").write_text(json.dumps(data))
        result = subprocess.run([__import__("sys").executable, str(MODULE),
                                 "--catalog", str(self.output / "catalog.json"),
                                 "--find", "missing-source-unique"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing-or-invalid-root", result.stdout)

    def test_explicit_root_alias_is_resolved(self):
        self.skill("a")
        alias = self.root / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        result = catalog.build([dict(id="alias", path=str(alias), kind="repository")], self.output)
        self.assertEqual(result["counts"]["objects"], 1)
        self.assertIn("/alias/", result["occurrences"][0]["source_path"])
        self.assertEqual(result["sources"][0]["resolved_path"], str(self.source))

    def test_catalog_commands_accept_explicit_directory_alias(self):
        import subprocess
        self.skill("a")
        self.build()
        alias = self.root / "catalog-alias"
        alias.symlink_to(self.output, target_is_directory=True)
        for operation in (("--verify",), ("--find", "shared")):
            with self.subTest(operation=operation):
                result = subprocess.run([__import__("sys").executable, str(MODULE),
                                         "--catalog", str(alias / "catalog.json"), *operation],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_link_inside_package_remains_catalog_only(self):
        folder = self.skill("unsafe")
        (folder / "linked").symlink_to(self.root, target_is_directory=True)
        result = self.build()
        self.assertEqual(result["objects"], {})
        self.assertEqual(result["occurrences"][0]["status"], "needs-review")
        self.assertTrue(result["incomplete"])
        self.assertTrue((folder / "linked").is_symlink())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "requires POSIX FIFO")
    def test_special_file_is_never_read(self):
        folder = self.skill("unsafe")
        os.mkfifo(folder / "pipe")
        result = self.build()
        self.assertEqual(result["objects"], {})
        self.assertIn("special file", result["occurrences"][0]["error"])

    def test_overlap_and_nonempty_refusal(self):
        self.skill("a")
        for output in (self.source, self.source / "nested", self.root):
            with self.subTest(output=output), self.assertRaises(ValueError):
                catalog.build([dict(id="test", path=str(self.source), kind="repository")], output)
        self.output.mkdir()
        (self.output / "keep").write_text("untouched")
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual((self.output / "keep").read_text(), "untouched")

    def test_overlap_preflight_does_not_create_ancestors_inside_source(self):
        self.skill("a")
        alias = self.root / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        for root in (self.source, alias):
            with self.subTest(root=root), self.assertRaises(ValueError):
                catalog.build([dict(id="test", path=str(root), kind="repository")],
                              self.source / "new" / "snapshot")
            self.assertFalse((self.source / "new").exists())

    def test_cyclic_source_alias_is_incomplete_without_cli_traceback(self):
        import subprocess
        cycle = self.root / "cycle"
        cycle.symlink_to(cycle)
        sources = self.root / "sources.json"
        sources.write_text(json.dumps([dict(id="cycle", path=str(cycle), kind="repository")]))
        result = subprocess.run([__import__("sys").executable, str(MODULE),
                                 "--sources", str(sources), "--output", str(self.output)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        data = json.loads((self.output / "catalog.json").read_text())
        self.assertTrue(data["incomplete"])
        self.assertEqual(data["sources"][0]["status"], "missing-or-invalid-root")

    def test_missing_root_and_limits_are_explicit(self):
        self.skill("a", b"long resource")
        result = self.build(limits=catalog.Limits(file_bytes=4))
        self.assertTrue(result["incomplete"])
        self.assertEqual(result["sources"][0]["status"], "incomplete")
        result = catalog.build([dict(id="missing", path=str(self.root / "missing"), kind="repository")], self.root / "other")
        self.assertTrue(result["incomplete"])
        self.assertEqual(result["sources"][0]["status"], "missing-or-invalid-root")

    def test_copy_corruption_is_not_marked_verified(self):
        self.skill("a")
        original = catalog.copy_package

        def corrupt(source, target, entries, limits):
            original(source, target, entries, limits)
            (target / "asset.bin").write_bytes(b"tampered")

        with patch.object(catalog, "copy_package", corrupt):
            result = self.build()
        self.assertEqual(result["objects"], {})
        self.assertTrue(result["incomplete"])
        self.assertIn("failed verification", result["occurrences"][0]["error"])
        report = catalog.verify(self.output / "catalog.json")
        self.assertFalse(report["verified"])
        self.assertFalse(report["catalog_complete"])
        self.assertEqual(report["orphan_objects"], [])

    def test_failed_copy_does_not_prevent_valid_duplicate(self):
        self.skill("a")
        self.skill("b")
        original = catalog.copy_package
        attempts = []

        def fail_once(source, target, entries, limits):
            original(source, target, entries, limits)
            attempts.append(source)
            if len(attempts) == 1:
                raise OSError("interrupted object copy")

        with patch.object(catalog, "copy_package", fail_once):
            result = self.build()
        self.assertEqual(len(result["objects"]), 1)
        self.assertEqual(len(attempts), 2)
        report = catalog.verify(self.output / "catalog.json")
        self.assertTrue(report["retained_objects_verified"])
        self.assertEqual(report["orphan_objects"], [])

    def test_verified_occurrence_requires_registered_object(self):
        self.skill("a")
        self.build()
        path = self.output / "catalog.json"
        data = json.loads(path.read_text())
        data["occurrences"][0]["package_sha256"] = "0" * 64
        path.write_text(json.dumps(data))
        report = catalog.verify(path)
        self.assertFalse(report["retained_objects_verified"])
        self.assertIn("unregistered object", report["failures"][0])

    def test_readback_detects_tampering(self):
        self.skill("a")
        result = self.build()
        obj = next(iter(result["objects"].values()))
        (self.output / obj["path"] / "asset.bin").write_bytes(b"tampered")
        report = catalog.verify(self.output / "catalog.json")
        self.assertEqual(len(report["failures"]), 1)
        self.assertFalse(report["retained_objects_verified"])

    def test_generated_state_does_not_change_identity_or_get_copied(self):
        self.skill("a")
        folder = self.skill("b")
        for directory in ("__pycache__", ".git", "node_modules", ".pytest_cache", ".ruff_cache"):
            (folder / directory).mkdir()
            (folder / directory / "temporary").write_text("generated")
        for filename in (".DS_Store", "module.pyc", "module.pyo"):
            (folder / filename).write_text("generated")
        result = self.build()
        self.assertEqual(result["counts"]["objects"], 1)
        occurrence = next(item for item in result["occurrences"] if item["package_path"] == str(folder))
        self.assertEqual(len(occurrence["excluded_generated_paths"]), 8)
        self.assertIn(".DS_Store", result["exclusion_policy"]["package_names"])
        copied = self.output / next(iter(result["objects"].values()))["path"]
        self.assertEqual({item.name for item in copied.iterdir()}, {"SKILL.md", "asset.bin"})

    def test_existing_empty_output_is_made_private(self):
        self.skill("a")
        self.output.mkdir(mode=0o755)
        self.output.chmod(0o755)
        self.build()
        self.assertEqual(self.output.stat().st_mode & 0o777, 0o700)

    def test_orphan_object_prevents_overall_verification(self):
        self.skill("a")
        self.build()
        (self.output / "objects" / "unregistered").mkdir()
        report = catalog.verify(self.output / "catalog.json")
        self.assertFalse(report["verified"])
        self.assertTrue(report["retained_objects_verified"])
        self.assertTrue(report["catalog_complete"])
        self.assertEqual(report["orphan_objects"], ["unregistered"])

    def test_incomplete_catalog_never_reports_overall_verified(self):
        self.skill("a")
        self.build()
        path = self.output / "catalog.json"
        data = json.loads(path.read_text())
        data["incomplete"] = True
        path.write_text(json.dumps(data))
        report = catalog.verify(path)
        self.assertFalse(report["verified"])
        self.assertTrue(report["retained_objects_verified"])
        self.assertFalse(report["catalog_complete"])

    def test_pruned_runtime_dirs_are_visible_but_repository_projects_survive(self):
        self.skill("projects/a")
        self.assertEqual(self.build()["counts"]["objects"], 1)
        result = catalog.build([dict(id="native", path=str(self.source), kind="runtime")], self.root / "runtime-collection")
        self.assertEqual(result["counts"]["objects"], 0)
        self.assertEqual(result["events"][0]["status"], "excluded-directory")


if __name__ == "__main__":
    unittest.main()
