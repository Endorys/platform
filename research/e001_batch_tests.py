# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Sadhu Shobab Bollipo
"""Batch audit invariants on generated toy data; no instrument validation."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import e001
import e001_batch
from e001_generate_demo import generate


class BatchAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.inputs = generate(self.root / "inputs")
        self.config = self.inputs / "e001_demo_config.json"

    def records(self, *names):
        return [self.inputs / f"e001_{n}.json" for n in names]

    def run_batch(self, *names, output="results"):
        return e001_batch.batch(self.records(*names), self.config, self.root / output)

    def test_all_inputs_retained_in_counts_and_outputs(self):
        manifest = self.run_batch("reference", "changed", "reduced", "incomplete")
        self.assertEqual(manifest["counts"], {"accepted": 2, "rejected": 1, "invalid": 1})
        self.assertEqual(manifest["declared_records"], 4)
        page = (self.root / "results" / "index.html").read_text()
        self.assertIn("synthetic software checks only", page)
        self.assertIn("Declared records: <strong>4", page)
        invalid = manifest["records"][-1]
        self.assertIn("calibration_id", invalid["error"])
        self.assertIsNone(invalid["analysis_file"])
        for entry in manifest["records"][:-1]:
            self.assertTrue((self.root / "results" / entry["analysis_file"]).is_file())
            self.assertIn("SYNTHETIC", (self.root / "results" / entry["waveform_file"]).read_text())

    def test_missing_record_is_visible_not_silently_skipped(self):
        manifest = self.run_batch("reference", "missing")
        self.assertEqual(manifest["counts"]["invalid"], 1)
        self.assertIsNone(manifest["records"][1]["record_sha256"])

    def test_duplicate_paths_block_before_output(self):
        with self.assertRaisesRegex(ValueError, "Duplicate record path"):
            self.run_batch("reference", "reference")
        self.assertFalse((self.root / "results").exists())

    def test_duplicate_run_ids_never_overwrite_or_count_twice(self):
        record = e001.read_json(self.records("changed")[0])
        record["run_id"] = "reference"
        self.records("changed")[0].write_text(json.dumps(record))
        manifest = self.run_batch("reference", "changed")
        self.assertEqual(manifest["counts"], {"accepted": 1, "rejected": 0, "invalid": 1})
        self.assertIn("Duplicate run_id", manifest["records"][1]["error"])
        self.assertEqual(len(list((self.root / "results" / "analysis").glob("*_analysis.json"))), 1)

    def test_existing_output_is_never_overwritten(self):
        self.run_batch("reference")
        before = (self.root / "results" / "manifest.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "new directory"):
            self.run_batch("changed")
        self.assertEqual(before, (self.root / "results" / "manifest.json").read_bytes())

    def test_mixed_origin_is_recorded_invalid(self):
        path = self.records("changed")[0]
        record = e001.read_json(path)
        record["data_origin"] = "physical"
        record["waveform"]["amplitude_unit"] = "V"
        path.write_text(json.dumps(record))
        manifest = self.run_batch("reference", "changed")
        self.assertEqual(manifest["counts"]["invalid"], 1)
        self.assertIn("Mixed data origins", manifest["records"][1]["error"])

    def test_raw_records_and_waveforms_unchanged(self):
        originals = {p: p.read_bytes() for p in self.inputs.iterdir()}
        self.run_batch("reference", "reduced")
        self.assertTrue(all(p.read_bytes() == b for p, b in originals.items()))

    def test_hashes_match_actual_files_and_saved_config(self):
        manifest = self.run_batch("reference")
        self.assertEqual(manifest["configuration_file_sha256"],
                         hashlib.sha256(self.config.read_bytes()).hexdigest())
        for name, digest in manifest["software_sha256"].items():
            self.assertEqual(digest, hashlib.sha256((e001.HERE / name).read_bytes()).hexdigest())
        self.assertEqual(manifest["records"][0]["record_sha256"],
                         hashlib.sha256(self.records("reference")[0].read_bytes()).hexdigest())

    def test_same_inputs_produce_identical_manifest(self):
        one = self.run_batch("reference", "reduced", output="one")
        two = self.run_batch("reference", "reduced", output="two")
        self.assertEqual(one, two)

    def test_empty_batch_blocked(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            self.run_batch()

    def test_output_cannot_replace_a_missing_declared_input(self):
        missing = self.root / "missing.json"
        with self.assertRaisesRegex(ValueError, "separate"):
            e001_batch.batch([missing], self.config, missing)
        self.assertFalse(missing.exists())

    def test_error_and_filename_are_escaped_in_html(self):
        path = self.inputs / "record&input.json"
        path.write_text('{"<untrusted>":1,"<untrusted>":2}')
        e001_batch.batch([path], self.config, self.root / "results")
        page = (self.root / "results" / "index.html").read_text()
        self.assertIn("record&amp;input.json", page)
        self.assertIn("&lt;untrusted&gt;", page)
        self.assertNotIn("<untrusted>", page)

    def test_invalid_config_blocks_before_output(self):
        self.config.write_text("{}")
        with self.assertRaises(ValueError):
            self.run_batch("reference")
        self.assertFalse((self.root / "results").exists())

    def test_duplicate_json_keys_rejected_even_when_values_match(self):
        path = self.root / "duplicate.json"
        path.write_text('{"acquisition":{"gain":1,"gain":1}}')
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key: gain"):
            e001.read_json(path)

    def test_corrupt_record_does_not_hide_other_records(self):
        self.records("changed")[0].write_text("not JSON")
        manifest = self.run_batch("reference", "changed", "reduced")
        self.assertEqual(manifest["counts"], {"accepted": 1, "rejected": 1, "invalid": 1})

    def test_cli_exit_status_distinguishes_quality_and_invalidity(self):
        for names, expected in [(('reference',), 0), (('reduced',), 2), (('incomplete',), 1)]:
            args = [str(p) for p in self.records(*names)]
            args += ["--config", str(self.config), "--out", str(self.root / names[0])]
            self.assertEqual(e001_batch.main(args), expected)


if __name__ == "__main__":
    unittest.main()
