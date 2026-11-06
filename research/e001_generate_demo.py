# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Sadhu Shobab Bollipo
"""Generate deterministic toy waveforms. These are NOT simulated tissue physics."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import random


def generate(output):
    output = Path(output)
    # Never replace an existing acquisition/export directory with toy files.
    output.mkdir(parents=True, exist_ok=False)
    rng = random.Random(20261029)
    conditions = [("reference",1500,1), ("changed",1560,1),
                  ("reduced",1500,.02), ("disconnected",1500,0),
                  ("clipped",1500,3), ("ambiguous",1500,1)]
    for name,speed,amplitude in conditions:
        raw = output/("e001_"+name+".csv")
        arrival = .04/speed
        with raw.open("w",newline="",encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(["time_s","amplitude"])
            for i in range(601):
                t = i*1e-7
                value = amplitude*math.exp(-.5*((t-arrival)/4e-7)**2)+rng.uniform(-.002,.002)
                if name == "ambiguous":
                    value += math.exp(-.5*((t-35e-6)/4e-7)**2)
                if name == "clipped":
                    value = min(1.,value)
                writer.writerow([t,value])
        record = {
            "schema_version":"1.0","experiment_id":"E001","run_id":name,
            "protocol_version":"synthetic-demo-0.1","data_origin":"synthetic",
            "specimen_kind":"non_biological_phantom","specimen_id":"toy-placeholder",
            "session_id":"synthetic-session-01","record_status":"complete",
            "quality_flags":[],"calibration_id":"synthetic-not-calibrated-hardware",
            "hardware_revision":"none-toy-generator","source_id":"toy-gaussian",
            "receiver_id":"toy-samples","coupling":name if name in ("reduced","disconnected") else "reference",
            "temperature_c":None,
            "acquisition":{"sample_interval_s":1e-7,"trigger_time_s":0.,
                "electronic_delay_s":0.,"trigger_standard_uncertainty_s":0.,
                "delay_standard_uncertainty_s":0.,"gain_setting":"toy-unity",
                "filter_setting":"none","clock_domain":"synthetic-clock"},
            "geometry":{"mode":"through_transmission","coordinate_frame":"toy-fixed-line",
                "path_length_m":.04,"path_standard_uncertainty_m":.0001},
            "waveform":{"path":raw.name,"format":"csv_time_amplitude","time_unit":"s",
                "amplitude_unit":"synthetic_arb","sha256":hashlib.sha256(raw.read_bytes()).hexdigest()}}
        (output/("e001_"+name+".json")).write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
        if name == "reference":
            record["record_status"]="incomplete"
            del record["calibration_id"]
            (output/"e001_incomplete.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
            record["calibration_id"]="synthetic-not-calibrated-hardware"
            record["record_status"]="rejected"
            record["run_id"]="operator_rejected"
            record["quality_flags"]=["operator_rejection"]
            (output/"e001_operator_rejected.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    config={"schema_version":"1.0","data_origin":"synthetic","threshold_scope":"toy_demo_only",
            "noise_window_s":[0,10e-6],"signal_window_s":[15e-6,45e-6],
            "min_peak":.1,"min_peak_to_noise_ratio":10.,"rail_abs":1.,
            "max_rail_fraction":.005,"ambiguous_peak_fraction":.95,"minimum_peak_separation_s":2e-6}
    (output/"e001_demo_config.json").write_text(json.dumps(config,indent=2)+"\n",encoding="utf-8")
    return output


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    generate(args.out)
    print("Generated six toy conditions and complete/rejected/incomplete records. No physical data.")
