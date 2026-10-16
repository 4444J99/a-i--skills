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

    def test_explicit_root_alias_is_resolved(self):
        self.skill("a")
        alias = self.root / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        result = catalog.build([dict(id="alias", path=str(alias), kind="repository")], self.output)
        self.assertEqual(result["counts"]["objects"], 1)
        self.assertIn("/alias/", result["occurrences"][0]["source_path"])
        self.assertEqual(result["sources"][0]["resolved_path"], str(self.source))

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
        self.assertEqual(len(report["orphan_objects"]), 1)

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
