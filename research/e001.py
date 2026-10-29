# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Sadhu Shobab Bollipo
"""Offline, non-biological phantom research. No hardware control or diagnosis."""
import argparse
import csv
import hashlib
import html
import json
import math
from pathlib import Path
import re
import statistics

HERE = Path(__file__).resolve().parent
VERSION = "0.1.0"


def read_json(path):
    def reject(value):
        raise ValueError("Non-finite JSON number: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_constant=reject)


def validate_schema(value, schema, location="record"):
    """Strict validator for the deliberately small keyword subset in our schema.

    Not a general JSON Schema implementation. Reject unknown keywords so schema
    evolution cannot silently bypass checks. The published schema is also usable
    with an independent Draft 2020-12 validator.
    """
    supported = {"$schema", "$id", "title", "description", "type", "properties",
                 "required", "additionalProperties", "items", "minItems", "enum",
                 "const", "minimum", "exclusiveMinimum", "minLength", "pattern"}
    if set(schema) - supported:
        raise ValueError("Unsupported schema keywords: " + str(set(schema) - supported))
    kinds = {
        "object": lambda x: isinstance(x, dict),
        "array": lambda x: isinstance(x, list),
        "string": lambda x: isinstance(x, str),
        "number": lambda x: type(x) in (int, float) and math.isfinite(x),
        "integer": lambda x: type(x) is int,
        "null": lambda x: x is None,
    }
    requested = schema.get("type", list(kinds))
    requested = [requested] if isinstance(requested, str) else requested
    if not any(kinds[k](value) for k in requested):
        raise ValueError(f"{location}: expected {requested}")
    if "const" in schema and value != schema["const"]:
        raise ValueError(f"{location}: wrong constant")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{location}: not an allowed value")
    if type(value) in (int, float):
        if "minimum" in schema and value < schema["minimum"]:
            raise ValueError(f"{location}: below minimum")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            raise ValueError(f"{location}: must exceed minimum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ValueError(f"{location}: string too short")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            raise ValueError(f"{location}: pattern mismatch")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValueError(f"{location}: too few items")
        for i, item in enumerate(value):
            validate_schema(item, schema.get("items", {}), f"{location}[{i}]")
    if isinstance(value, dict):
        missing = set(schema.get("required", [])) - set(value)
        if missing:
            raise ValueError(f"{location}: missing {sorted(missing)}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False and set(value) - set(props):
            raise ValueError(f"{location}: unknown fields {sorted(set(value)-set(props))}")
        for key, item in value.items():
            if key in props:
                validate_schema(item, props[key], f"{location}.{key}")


def inside(base, relative):
    target = (base / relative).resolve()
    if Path(relative).is_absolute() or not target.is_relative_to(base.resolve()):
        raise ValueError("Waveform path must stay inside the record directory")
    return target


def load_record(path):
    path = Path(path).resolve()
    record = read_json(path)
    validate_schema(record, read_json(HERE / "e001_record.schema.json"))
    expected_unit = "synthetic_arb" if record["data_origin"] == "synthetic" else "V"
    if record["waveform"]["amplitude_unit"] != expected_unit:
        raise ValueError("Amplitude unit does not match data origin")
    raw = inside(path.parent, record["waveform"]["path"])
    if hashlib.sha256(raw.read_bytes()).hexdigest() != record["waveform"]["sha256"]:
        raise ValueError("Raw waveform checksum mismatch")
    times, values = [], []
    with raw.open(newline="", encoding="utf-8") as stream:
        rows = csv.DictReader(stream)
        if rows.fieldnames != ["time_s", "amplitude"]:
            raise ValueError("CSV must have exactly time_s,amplitude columns")
        for row in rows:
            if None in row or any(v is None for v in row.values()):
                raise ValueError("Malformed waveform row")
            t, v = float(row["time_s"]), float(row["amplitude"])
            if not (math.isfinite(t) and math.isfinite(v)):
                raise ValueError("Non-finite waveform sample")
            times.append(t)
            values.append(v)
    if len(times) < 10:
        raise ValueError("Too few waveform samples")
    dt = record["acquisition"]["sample_interval_s"]
    for a, b in zip(times, times[1:]):
        if b <= a or not math.isclose(b-a, dt, rel_tol=1e-5, abs_tol=dt*1e-6):
            raise ValueError("Non-monotonic or inconsistent sampling interval")
    return record, times, values


def config_check(config, origin):
    required = {"schema_version", "data_origin", "threshold_scope", "noise_window_s",
                "signal_window_s", "min_peak", "min_peak_to_noise_ratio",
                "rail_abs", "max_rail_fraction", "ambiguous_peak_fraction",
                "minimum_peak_separation_s"}
    if set(config) != required or config["schema_version"] != "1.0":
        raise ValueError("Unknown or incomplete analysis configuration")
    if config["data_origin"] != origin or origin not in ("synthetic", "physical"):
        raise ValueError("Configuration/data origin mismatch")
    expected_scope = "toy_demo_only" if origin == "synthetic" else "protocol_prespecified"
    if config["threshold_scope"] != expected_scope:
        raise ValueError("Threshold scope does not match data origin")
    for key in ("noise_window_s", "signal_window_s"):
        pair = config[key]
        if not isinstance(pair, list) or len(pair) != 2 or any(type(v) not in (int,float) or not math.isfinite(v) for v in pair) or pair[0] >= pair[1]:
            raise ValueError("Invalid/unset " + key)
    if config["noise_window_s"][1] >= config["signal_window_s"][0]:
        raise ValueError("Noise window must end before signal window")
    for key in required - {"schema_version", "data_origin", "threshold_scope", "noise_window_s", "signal_window_s"}:
        val = config[key]
        if type(val) not in (int, float) or not math.isfinite(val) or val <= 0:
            raise ValueError("Invalid/unset " + key)
    if config["max_rail_fraction"] > 1 or config["ambiguous_peak_fraction"] > 1:
        raise ValueError("Fractions must not exceed one")


def analyze(path, config):
    record, times, values = load_record(path)
    config_check(config, record["data_origin"])
    reasons = list(record["quality_flags"])
    if record["coupling"] in ("unknown", "disconnected"):
        reasons.append("coupling_" + record["coupling"])
    if record["record_status"] != "complete":
        reasons.append("record_declared_" + record["record_status"])
    noise_lo, noise_hi = config["noise_window_s"]
    sig_lo, sig_hi = config["signal_window_s"]
    if times[0] > noise_lo or times[-1] < sig_hi:
        raise ValueError("Acquisition does not cover configured windows")
    noise = [v for t, v in zip(times, values) if noise_lo <= t <= noise_hi]
    signal = [(t, v) for t, v in zip(times, values) if sig_lo <= t <= sig_hi]
    if len(noise) < 3 or len(signal) < 3:
        raise ValueError("Too few samples in analysis windows")
    offset = statistics.mean(noise)
    noise_rms = math.sqrt(statistics.mean((v-offset)**2 for v in noise))
    absolute = [(t, abs(v-offset)) for t, v in signal]
    peak_time, peak = max(absolute, key=lambda row: row[1])
    ratio = peak/noise_rms if noise_rms else None
    if peak < config["min_peak"]:
        reasons.append("signal_below_threshold")
    if noise_rms and ratio < config["min_peak_to_noise_ratio"]:
        reasons.append("low_peak_to_noise_ratio")
    rail_fraction = sum(abs(v) >= config["rail_abs"] for v in values)/len(values)
    if rail_fraction > config["max_rail_fraction"]:
        reasons.append("possible_clipping")
    if peak_time in (signal[0][0], signal[-1][0]):
        reasons.append("peak_at_search_boundary")
    if peak >= config["min_peak"] and any(
            abs(t-peak_time) >= config["minimum_peak_separation_s"] and v >= peak*config["ambiguous_peak_fraction"]
            for t,v in absolute):
        reasons.append("ambiguous_peak")
    acquisition = record["acquisition"]
    transit = peak_time-acquisition["trigger_time_s"]-acquisition["electronic_delay_s"]
    if transit <= 0:
        reasons.append("nonpositive_corrected_transit")
    reasons = sorted(set(reasons))
    accepted = not reasons
    geometry = record["geometry"]
    speed = geometry["path_length_m"]/transit if accepted else None
    # Partial standard uncertainty only: uniform sample quantization, supplied
    # trigger/delay and distance standard uncertainties, assumed independent.
    # Excludes peak-estimator bias, coupling, temperature effects and model error.
    time_u = math.sqrt((acquisition["sample_interval_s"]/math.sqrt(12))**2 +
                       acquisition["trigger_standard_uncertainty_s"]**2 +
                       acquisition["delay_standard_uncertainty_s"]**2)
    speed_u = speed*math.sqrt((geometry["path_standard_uncertainty_m"]/geometry["path_length_m"])**2+(time_u/transit)**2) if accepted else None
    return {
        "analysis_version": VERSION, "run_id": record["run_id"],
        "session_id": record["session_id"], "specimen_id": record["specimen_id"],
        "data_origin": record["data_origin"], "quality": "accepted" if accepted else "rejected",
        "rejection_reasons": reasons, "threshold_scope": config["threshold_scope"],
        "peak_amplitude": peak, "amplitude_unit": record["waveform"]["amplitude_unit"],
        "noise_rms": noise_rms, "peak_to_noise_ratio": ratio,
        "rail_fraction": rail_fraction, "corrected_peak_transit_s": transit if accepted else None,
        "apparent_speed_m_per_s": speed, "partial_standard_uncertainty_m_per_s": speed_u,
        "uncertainty_scope": "Independent sampling/trigger/delay/path terms only; incomplete physical error budget",
        "estimator": "absolute_peak_in_prespecified_window; NOT validated time-of-flight or elasticity estimator",
        "input_waveform_sha256": record["waveform"]["sha256"],
        "configuration_sha256": hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest(),
        "claim_status": "synthetic illustration only" if record["data_origin"] == "synthetic" else "unvalidated phantom research estimate; not clinical evidence",
    }, times, values


def write_plot(path, times, values, result):
    low, high = min(values), max(values)
    span = high-low or 1
    points = " ".join(f"{50+700*(t-times[0])/(times[-1]-times[0]):.2f},{210-140*(v-low)/span:.2f}" for t,v in zip(times,values))
    label = html.escape(f"{result['data_origin'].upper()} | {result['run_id']} | {result['quality']}")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="300" viewBox="0 0 800 300"><rect width="800" height="300" fill="white"/><g font-family="sans-serif" fill="#102030"><text x="30" y="28">{label}</text><text x="30" y="48">Raw waveform; no diagnostic or validated device output</text><text x="30" y="245">Time: {times[0]:.3g} to {times[-1]:.3g} s</text><text x="30" y="265">Amplitude: {low:.3g} to {high:.3g} {html.escape(result['amplitude_unit'])}</text><text x="30" y="285">Peak estimator and partial uncertainty are research examples only.</text></g><polyline points="{points}" fill="none" stroke="#126a90" stroke-width="1.5"/></svg>'''
    Path(path).write_text(svg, encoding="utf-8")


def run(record_path, config_path, output):
    output = Path(output)
    record_path = Path(record_path).resolve()
    if output.resolve() == record_path.parent:
        raise ValueError("Use an output directory separate from the raw-record directory")
    result, times, values = analyze(record_path, read_json(config_path))
    output.mkdir(parents=True, exist_ok=True)
    stem = result["run_id"]
    (output/(stem+"_analysis.json")).write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    write_plot(output/(stem+"_waveform.svg"), times, values, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    valid = sub.add_parser("validate")
    valid.add_argument("record")
    analysis = sub.add_parser("analyze")
    analysis.add_argument("record")
    analysis.add_argument("--config", required=True)
    analysis.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            record, _, _ = load_record(args.record)
            print("Structurally valid record and checksum: " + record["run_id"] + "; this is not measurement validation")
        else:
            result = run(args.record, args.config, args.out)
            print(json.dumps(result, indent=2, allow_nan=False))
            return 0 if result["quality"] == "accepted" else 2
    except (ValueError, OSError, KeyError, csv.Error) as error:
        parser.exit(1, "Input error: " + str(error) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
