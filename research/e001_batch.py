# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Sadhu Shobab Bollipo
"""Audit a declared E001 record list. Offline research only; never drives hardware."""
import argparse
import csv
import hashlib
import html
import json
from pathlib import Path
import platform
import sys

import e001


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_report(output, manifest):
    rows = []
    for entry in manifest["records"]:
        links = "No analysis output"
        if entry["analysis_file"]:
            links = (f'<a href="{html.escape(entry["analysis_file"], quote=True)}">Analysis JSON</a> · '
                     f'<a href="{html.escape(entry["waveform_file"], quote=True)}">Raw waveform plot</a>')
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in
                    (entry["ordinal"], entry["record_name"], entry["run_id"] or "unresolved",
                     entry["status"], entry["error"] or "; ".join(entry["rejection_reasons"]) or "Software checks passed"))
                    + f"<td>{links}</td></tr>")
    counts = manifest["counts"]
    page = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Endorys E001 batch audit</title><style>
body{font:16px system-ui;line-height:1.5;max-width:1200px;margin:32px auto;padding:20px;color:#163044}
.notice{padding:18px;background:#fff0bf;border-left:5px solid #9c6500}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #b7c7d1;padding:10px;text-align:left;vertical-align:top}
.table-wrap{overflow-x:auto}a{color:#065b8d}code{overflow-wrap:anywhere}</style>
<h1>Endorys E001 — batch audit</h1>'''
    page += f'<p class="notice"><strong>{html.escape(manifest["claim_status"])}</strong>. '
    page += 'Accepted means software checks passed. It does not establish measurement validity or clinical performance.</p>'
    page += (f'<p>Declared records: <strong>{manifest["declared_records"]}</strong>. '
             f'Accepted: {counts["accepted"]}; rejected: {counts["rejected"]}; invalid: {counts["invalid"]}.</p>')
    page += '<p>No pooled statistics, independent sample size or diagnostic accuracy is inferred.</p>'
    page += '<div class="table-wrap"><table><caption>Every declared input, including failures</caption><thead><tr>'
    page += ''.join(f'<th scope="col">{v}</th>' for v in ('Order', 'Record', 'Run ID', 'Status', 'Details', 'Artifacts'))
    page += '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
    page += '<h2>Reproduction</h2><p><a href="manifest.json">Manifest JSON</a> records input, configuration and software hashes.</p>'
    page += f'<p>Analysis version: <code>{html.escape(manifest["analysis_version"])}</code>. Configuration file SHA-256: '
    page += f'<code>{manifest["configuration_file_sha256"]}</code>.</p>'
    page += '<ul>' + ''.join(f'<li>{html.escape(v)}</li>' for v in manifest['limitations']) + '</ul></html>'
    (output / "index.html").write_text(page, encoding="utf-8")


def batch(record_paths, config_path, output):
    """Analyze every declared input; keep invalid records in the manifest.

    A batch has one origin/configuration. Duplicate paths, duplicate run IDs and
    origin mismatches are input errors, never silently dropped observations.
    Output must be a new directory. No pooling across runs/sessions is performed.
    """
    paths = [Path(p).resolve() for p in record_paths]
    if not paths:
        raise ValueError("Declare at least one record")
    if len(set(paths)) != len(paths):
        raise ValueError("Duplicate record path in batch")
    config_path = Path(config_path).resolve()
    config = e001.read_json(config_path)
    if not isinstance(config, dict):
        raise ValueError("Configuration must be an object")
    e001.config_check(config, config.get("data_origin"))
    output = Path(output).resolve()
    if output in paths or output == config_path:
        raise ValueError("Batch output must be separate from declared input files")
    if output.exists():
        raise ValueError("Batch output must be a new directory")

    entries = []
    seen = set()
    results = []
    for ordinal, path in enumerate(paths, 1):
        entry = {"ordinal": ordinal, "record_name": path.name,
                 "record_sha256": None, "run_id": None, "status": "invalid",
                 "error": None, "rejection_reasons": [], "analysis_file": None,
                 "waveform_file": None, "analysis_file_sha256": None,
                 "waveform_file_sha256": None}
        try:
            entry["record_sha256"] = sha256(path)
            record = e001.read_json(path)
            # Validate identifiers before they are used as output names.
            e001.validate_schema(record, e001.read_json(e001.HERE / "e001_record.schema.json"))
            entry["run_id"] = record["run_id"]
            if record["run_id"] in seen:
                raise ValueError("Duplicate run_id in batch: " + record["run_id"])
            seen.add(record["run_id"])
            if record["data_origin"] != config["data_origin"]:
                raise ValueError("Mixed data origins/configuration in batch")
        except (ValueError, OSError, TypeError) as error:
            entry["error"] = str(error)
            entries.append(entry)
            continue
        try:
            result, times, values = e001.analyze(path, config)
            entry["status"] = result["quality"]
            entry["rejection_reasons"] = result["rejection_reasons"]
            entry["analysis_file"] = f"analysis/{ordinal:04d}_{record['run_id']}_analysis.json"
            entry["waveform_file"] = f"analysis/{ordinal:04d}_{record['run_id']}_waveform.svg"
            results.append((entry, result, times, values))
        except (ValueError, OSError, KeyError, TypeError, OverflowError, csv.Error) as error:
            entry["error"] = str(error)
        entries.append(entry)

    # Validate serializability before writing anything. Failures stay visible.
    for entry, result, times, values in results[:]:
        try:
            json.dumps(result, allow_nan=False)
        except (ValueError, TypeError) as error:
            entry.update(status="invalid", error="Non-serializable analysis: " + str(error),
                         analysis_file=None, waveform_file=None)
            results.remove((entry, result, times, values))
    manifest = {
        "manifest_version": "1.0", "analysis_version": e001.VERSION,
        "data_origin": config["data_origin"],
        "claim_status": "synthetic software checks only" if config["data_origin"] == "synthetic"
                        else "unvalidated non-biological phantom research; not clinical evidence",
        "configuration_file_sha256": sha256(config_path),
        "configuration_sha256": hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest(),
        "software_sha256": {name: sha256(e001.HERE / name)
                            for name in ("e001.py", "e001_batch.py", "e001_record.schema.json")},
        "environment": {"python": platform.python_version(), "platform": platform.system()},
        "counts": {key: sum(e["status"] == key for e in entries)
                   for key in ("accepted", "rejected", "invalid")},
        "declared_records": len(paths), "records": entries,
        "limitations": ["Accepted means software quality checks passed, not measurement validation.",
                        "No pooled statistics or independent experimental-unit count is inferred.",
                        "Invalid and rejected records remain in the denominator.",
                        "A manifest proves file identity, not instrument calibration or acquisition authenticity."]}
    output.mkdir(parents=True, exist_ok=False)
    (output / "analysis").mkdir()
    for entry, result, times, values in results:
        (output / entry["analysis_file"]).write_text(
            json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        e001.write_plot(output / entry["waveform_file"], times, values, result)
        entry["analysis_file_sha256"] = sha256(output / entry["analysis_file"])
        entry["waveform_file_sha256"] = sha256(output / entry["waveform_file"])
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    write_report(output, manifest)
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+")
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        manifest = batch(args.records, args.config, args.out)
    except (ValueError, OSError, TypeError) as error:
        parser.exit(1, "Batch input error: " + str(error) + "\n")
    print(json.dumps(manifest["counts"], sort_keys=True))
    print("No physical or clinical validation. See manifest.json for all declared inputs.")
    return 1 if manifest["counts"]["invalid"] else 2 if manifest["counts"]["rejected"] else 0


if __name__ == "__main__":
    sys.exit(main())
