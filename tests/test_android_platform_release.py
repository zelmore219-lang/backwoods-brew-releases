import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

MODULE = Path(__file__).resolve().parents[1] / "scripts/publish_android_platform.py"
spec = importlib.util.spec_from_file_location("android_release", MODULE)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class AndroidReleaseTests(unittest.TestCase):
    def setUp(self):
        self.previous = {
            "version": "0.4.2", "versionCode": 7, "packageName": "com.backwoods.employees",
            "certificateSha256": "c" * 64, "sha256": "a" * 64, "size": 100,
            "url": "https://example.invalid/old.apk", "minSdk": 26,
            "abis": ["arm64-v8a", "x86_64"], "firstInstallOnly": False,
        }
        self.feed = {"schemaVersion": 1, "apps": {"employees": {
            "windows": {"version": "0.4.3", "sha256": "w" * 64, "custom": "retain"},
            "android": self.previous.copy(), "notes": "Windows acceptance passed",
        }}, "custom": {"retain": True}}
        self.info = {**self.previous, "version": "0.4.3", "versionCode": 8,
                     "sha256": "b" * 64, "size": 120, "url": "https://example.invalid/new.apk"}

    def test_only_android_changes_and_input_is_preserved(self):
        before = copy.deepcopy(self.feed)
        updated = release.revised_feed(self.feed, self.info)
        self.assertEqual(self.feed, before)
        self.assertEqual(updated["apps"]["employees"]["windows"], before["apps"]["employees"]["windows"])
        self.assertEqual(updated["custom"], before["custom"])
        self.assertEqual(updated["apps"]["employees"]["android"], self.info)

    def test_cannot_change_installed_package_or_key(self):
        for field in ("packageName", "certificateSha256"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                release.revised_feed(self.feed, {**self.info, field: "different"})

    def test_cannot_downgrade_either_version(self):
        for info in ({**self.info, "version": "0.4.1"}, {**self.info, "versionCode": 6}):
            with self.assertRaises(ValueError):
                release.revised_feed(self.feed, info)

    def test_existing_version_bytes_cannot_change(self):
        with self.assertRaises(ValueError):
            release.revised_feed(self.feed, {**self.previous, "sha256": "b" * 64})
        self.assertEqual(release.revised_feed(self.feed, self.previous), self.feed)

    def test_new_code_requires_new_version(self):
        with self.assertRaises(ValueError):
            release.revised_feed(self.feed, {**self.info, "version": "0.4.2"})

    def test_acceptance_requires_both_platforms_and_exact_source(self):
        metadata = {"version": "0.4.3", "sourceSHA": "a" * 40, "acceptanceRun": 123}
        evidence = {"headSha": "a" * 40, "status": "completed", "conclusion": "success",
                    "jobs": [{"name": name, "status": "completed", "conclusion": "success"}
                             for name in ("android", "windows")]}
        provenance = {"version": "0.4.3", "sourceSha": "a" * 40, "windowsAcceptanceRun": 123}
        release.accepted_source(metadata, evidence, provenance)
        for mutation in ("source", "job", "run"):
            trial = copy.deepcopy(evidence)
            proof = provenance.copy()
            if mutation == "source":
                trial["headSha"] = "b" * 40
            elif mutation == "job":
                trial["jobs"][0]["conclusion"] = "failure"
            else:
                proof["windowsAcceptanceRun"] = 124
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                release.accepted_source(metadata, trial, proof)

    def test_payload_hash_detects_code_change(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = []
            for text in ("accepted", "changed"):
                path = Path(directory) / (text + ".apk")
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr("classes.dex", text)
                paths.append(path)
            self.assertNotEqual(release.payload_checksum(paths[0]), release.payload_checksum(paths[1]))

    def test_reassembly_rejects_tampered_parts_and_path_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packages = root / "android-platform-updates/employees"
            packages.mkdir(parents=True)
            apk = packages / "original.apk"
            with zipfile.ZipFile(apk, "w") as archive:
                archive.writestr("classes.dex", b"accepted")
            raw = apk.read_bytes()
            part = packages / "android.part000"
            part.write_bytes(raw)
            metadata = {
                "app": "employees", "platform": "android", "version": "0.4.3",
                "name": "Backwoods-Employees-0.4.3.apk", "size": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(), "payloadSHA256": release.payload_checksum(apk),
                "parts": [{"path": str(part.relative_to(root)), "size": len(raw),
                           "sha256": hashlib.sha256(raw).hexdigest()}],
            }
            with patch.object(release, "ROOT", root), patch.object(release, "PACKAGES", packages):
                self.assertEqual(release.assemble(metadata).read_bytes(), raw)
                part.write_bytes(raw + b"tampered")
                with self.assertRaises(ValueError):
                    release.assemble(metadata)
                metadata["parts"][0]["path"] = "../escape.apk"
                with self.assertRaises(ValueError):
                    release.assemble(metadata)


if __name__ == "__main__":
    unittest.main()
