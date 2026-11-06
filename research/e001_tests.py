# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Sadhu Shobab Bollipo
"""Software tests on toy data only, not instrument validation."""
import copy
import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import e001
import e001_check_links
from e001_demo import demo
from e001_generate_demo import generate


class ResearchPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.inputs=generate(self.root/"inputs")
        self.config=e001.read_json(self.inputs/"e001_demo_config.json")

    def record(self,name="reference"):
        return self.inputs/("e001_"+name+".json")

    def mutate(self,change):
        data=e001.read_json(self.record())
        change(data)
        target=self.inputs/"mutated.json"
        target.write_text(json.dumps(data),encoding="utf-8")
        return target

    def modify_raw(self,change):
        data=e001.read_json(self.record())
        raw=self.inputs/data["waveform"]["path"]
        with raw.open(newline="") as stream:
            rows=list(csv.reader(stream))
        change(rows)
        with raw.open("w",newline="") as stream:
            csv.writer(stream).writerows(rows)
        data["waveform"]["sha256"]=hashlib.sha256(raw.read_bytes()).hexdigest()
        self.record().write_text(json.dumps(data),encoding="utf-8")

    def test_reference_and_changed_timing(self):
        for name,speed in (("reference",1500),("changed",1560)):
            result,*_=e001.analyze(self.record(name),self.config)
            self.assertEqual(result["quality"],"accepted")
            self.assertAlmostEqual(result["apparent_speed_m_per_s"],speed,delta=5)
            self.assertGreater(result["partial_standard_uncertainty_m_per_s"],0)
            self.assertEqual(result["data_origin"],"synthetic")

    def test_low_signal_rejected(self):
        result,*_=e001.analyze(self.record("reduced"),self.config)
        self.assertIn("signal_below_threshold",result["rejection_reasons"])
        self.assertIsNone(result["apparent_speed_m_per_s"])

    def test_disconnection_rejected(self):
        result,*_=e001.analyze(self.record("disconnected"),self.config)
        self.assertIn("coupling_disconnected",result["rejection_reasons"])

    def test_clipping_rejected(self):
        result,*_=e001.analyze(self.record("clipped"),self.config)
        self.assertIn("possible_clipping",result["rejection_reasons"])

    def test_ambiguous_arrival_rejected(self):
        result,*_=e001.analyze(self.record("ambiguous"),self.config)
        self.assertIn("ambiguous_peak",result["rejection_reasons"])

    def test_operator_rejection_preserved(self):
        result,*_=e001.analyze(self.record("operator_rejected"),self.config)
        self.assertIn("operator_rejection",result["rejection_reasons"])

    def test_incomplete_metadata_rejected(self):
        with self.assertRaisesRegex(ValueError,"calibration_id"):
            e001.load_record(self.record("incomplete"))

    def test_checksum_tampering_rejected(self):
        raw=self.inputs/"e001_reference.csv"
        raw.write_text(raw.read_text()+"0,0\n")
        with self.assertRaisesRegex(ValueError,"checksum"):
            e001.load_record(self.record())

    def test_sample_rate_mismatch_rejected(self):
        path=self.mutate(lambda d:d["acquisition"].update(sample_interval_s=2e-7))
        with self.assertRaisesRegex(ValueError,"sampling"):
            e001.load_record(path)

    def test_nonmonotonic_time_rejected(self):
        self.modify_raw(lambda rows:rows[3].__setitem__(0,rows[2][0]))
        with self.assertRaisesRegex(ValueError,"sampling"):
            e001.load_record(self.record())

    def test_nonfinite_csv_rejected(self):
        self.modify_raw(lambda rows:rows[20].__setitem__(1,"nan"))
        with self.assertRaisesRegex(ValueError,"Non-finite"):
            e001.load_record(self.record())

    def test_path_escape_rejected(self):
        path=self.mutate(lambda d:d["waveform"].update(path="../outside.csv"))
        with self.assertRaisesRegex(ValueError,"inside"):
            e001.load_record(path)

    def test_toy_thresholds_cannot_analyze_physical_record(self):
        path=self.mutate(lambda d:(d.update(data_origin="physical"),d["waveform"].update(amplitude_unit="V")))
        with self.assertRaisesRegex(ValueError,"origin"):
            e001.analyze(path,self.config)

    def test_physical_origin_requires_physical_units(self):
        path=self.mutate(lambda d:d.update(data_origin="physical"))
        with self.assertRaisesRegex(ValueError,"unit"):
            e001.load_record(path)

    def test_unknown_metadata_rejected(self):
        path=self.mutate(lambda d:d.update(patient_name="not-supported"))
        with self.assertRaisesRegex(ValueError,"unknown fields"):
            e001.load_record(path)

    def test_boolean_is_not_distance(self):
        path=self.mutate(lambda d:d["geometry"].update(path_length_m=True))
        with self.assertRaises(ValueError):
            e001.load_record(path)

    def test_nonpositive_corrected_transit_rejected(self):
        path=self.mutate(lambda d:d["acquisition"].update(electronic_delay_s=.001))
        result,*_=e001.analyze(path,self.config)
        self.assertIn("nonpositive_corrected_transit",result["rejection_reasons"])

    def test_window_coverage_rejected(self):
        self.config["signal_window_s"]=[15e-6,80e-6]
        with self.assertRaisesRegex(ValueError,"cover"):
            e001.analyze(self.record(),self.config)

    def test_overlap_windows_rejected(self):
        self.config["noise_window_s"]=[0,20e-6]
        with self.assertRaisesRegex(ValueError,"before"):
            e001.analyze(self.record(),self.config)

    def test_missing_physical_configuration_rejected(self):
        self.config["min_peak"]=None
        with self.assertRaisesRegex(ValueError,"unset"):
            e001.analyze(self.record(),self.config)

    def test_schema_evolution_not_silently_ignored(self):
        with self.assertRaisesRegex(ValueError,"Unsupported"):
            e001.validate_schema(1,{"type":"number","unimplementedKeyword":True})

    def test_nonfinite_json_rejected(self):
        path=self.inputs/"bad.json"
        path.write_text('{"value": NaN}')
        with self.assertRaisesRegex(ValueError,"Non-finite"):
            e001.read_json(path)

    def test_nonobject_configuration_has_clear_input_error(self):
        with self.assertRaisesRegex(ValueError, "must be an object"):
            e001.config_check([], "synthetic")

    def test_finite_metadata_cannot_produce_accepted_infinite_speed(self):
        path = self.mutate(lambda d: d["geometry"].update(path_length_m=1e308))
        with self.assertRaisesRegex(ValueError, "Non-finite derived"):
            e001.analyze(path, self.config)

    def test_large_uncertainty_is_not_squared_into_overflow(self):
        path = self.mutate(lambda d: d["acquisition"].update(trigger_standard_uncertainty_s=1e308))
        with self.assertRaisesRegex(ValueError, "Non-finite derived"):
            e001.analyze(path, self.config)

    def test_complete_output_and_raw_preserved(self):
        raw=self.inputs/"e001_reference.csv"
        before=raw.read_bytes()
        result=e001.run(self.record(),self.inputs/"e001_demo_config.json",self.root/"results")
        output=self.root/"results"/"reference_analysis.json"
        self.assertEqual(json.loads(output.read_text())["quality"],"accepted")
        self.assertIn("SYNTHETIC",(self.root/"results"/"reference_waveform.svg").read_text())
        self.assertEqual(raw.read_bytes(),before)
        self.assertEqual(result["configuration_sha256"],hashlib.sha256(json.dumps(self.config,sort_keys=True).encode()).hexdigest())

    def test_output_must_be_separate(self):
        with self.assertRaisesRegex(ValueError,"separate"):
            e001.run(self.record(),self.inputs/"e001_demo_config.json",self.inputs)

    def test_existing_analysis_artifact_is_preserved(self):
        output = self.root / "results"
        e001.run(self.record(), self.inputs / "e001_demo_config.json", output)
        before = {p.name: p.read_bytes() for p in output.iterdir()}
        with self.assertRaisesRegex(ValueError, "already exists"):
            e001.run(self.record(), self.inputs / "e001_demo_config.json", output)
        self.assertEqual(before, {p.name: p.read_bytes() for p in output.iterdir()})

    def test_existing_plot_blocks_before_analysis_is_written(self):
        output = self.root / "results"
        output.mkdir()
        existing = output / "reference_waveform.svg"
        existing.write_text("retain this artifact")
        with self.assertRaisesRegex(ValueError, "already exists"):
            e001.run(self.record(), self.inputs / "e001_demo_config.json", output)
        self.assertFalse((output / "reference_analysis.json").exists())
        self.assertEqual(existing.read_text(), "retain this artifact")

    def test_demo_generator_cannot_overwrite_an_existing_directory(self):
        originals = {p.name: p.read_bytes() for p in self.inputs.iterdir()}
        with self.assertRaises(FileExistsError):
            generate(self.inputs)
        self.assertEqual(originals, {p.name: p.read_bytes() for p in self.inputs.iterdir()})

    def test_demo_report_matches_expected_conditions(self):
        results=demo(self.root/"demo")
        self.assertEqual([r["run_id"] for r in results if r["quality"]=="accepted"],["reference","changed"])
        self.assertEqual(len(results),7)
        self.assertTrue((self.root/"demo"/"index.html").exists())

    def test_link_checker_reports_missing_local_file(self):
        folder=self.root/"docs"
        folder.mkdir()
        (folder/"README.md").write_text("[missing](missing.md) [web](https://example.invalid) [anchor](#section)")
        failures=e001_check_links.check(folder)
        self.assertEqual(len(failures),1)
        self.assertIn("missing.md",failures[0])

    def test_checked_in_examples(self):
        base=Path(e001.__file__).parent
        if not (base/"e001_reference.json").exists():
            self.fail("Checked-in synthetic examples are missing")
        cfg=e001.read_json(base/"e001_demo_config.json")
        for name in ("reference","changed","reduced","disconnected","clipped","ambiguous","operator_rejected"):
            result,*_=e001.analyze(base/("e001_"+name+".json"),cfg)
            self.assertEqual(result["quality"],"accepted" if name in ("reference","changed") else "rejected")
        with self.assertRaises(ValueError):
            e001.load_record(base/"e001_incomplete.json")


if __name__=="__main__":
    unittest.main()
