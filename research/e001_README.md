# Experiment 001: runnable research package

Version 0.2.0 · 30 October 2026 · Sadhu Shobab Bollipo / Endorys

**Immediate goal: a reproducible acoustic phantom experiment.** This package implements an offline software workflow and planning templates. No physical experiment, integrated prototype or clinical capability is established by this release.

## Run something now

Requires Python 3.11 or newer, with no third-party runtime packages. From this directory (the repository's `research/` folder):

```sh
python e001_demo.py --out e001_demo_output
python -m unittest e001_tests e001_batch_tests -v
python e001.py validate e001_demo_output/synthetic_inputs/e001_reference.json
python e001.py analyze e001_demo_output/synthetic_inputs/e001_reference.json --config e001_demo_output/synthetic_inputs/e001_demo_config.json --out e001_single_result
```

Open `e001_demo_output/index.html` in a browser. The report links to raw-waveform SVG plots and provides a JSON summary. All inputs are generated locally and labelled synthetic. The generator uses Gaussian pulses plus noise, not an acoustic tissue simulator. It demonstrates two accepted toy conditions, five rejected records and a deliberately incomplete record that fails validation.

## Files and interfaces

| File | Purpose |
|---|---|
| [e001_PROTOCOL.md](e001_PROTOCOL.md) | Draft physical protocol, pilot/freeze/confirmation stages and review questions |
| [e001_CHECKLIST.md](e001_CHECKLIST.md) | Equipment inventory, acquisition and release checklist |
| [e001_RESULTS_TEMPLATE.md](e001_RESULTS_TEMPLATE.md) | Report template including failures, uncertainty and next decision |
| [e001_record.schema.json](e001_record.schema.json) | Versioned JSON Schema for non-biological phantom metadata |
| [e001.py](e001.py) | Validation, checksum/sampling checks, peak estimator and partial uncertainty |
| [e001_generate_demo.py](e001_generate_demo.py) | Deterministic synthetic fixture generator |
| [e001_demo.py](e001_demo.py) | Runnable HTML/JSON/SVG demonstration |
| [e001_tests.py](e001_tests.py) | Software failure and provenance tests |
| [e001_batch.py](e001_batch.py) | Declared-record batch audit, failure-preserving manifest and HTML report |
| [e001_batch_tests.py](e001_batch_tests.py) | Duplicate, invalid-input, provenance and raw-preservation checks |
| [e001_REPLICATION.md](e001_REPLICATION.md) | Independent software reproduction commands and expected results |
| [e001_REVIEW_BRIEF.md](e001_REVIEW_BRIEF.md) | Bounded acoustic protocol review request |
| [e001_check_links.py](e001_check_links.py) | Local Markdown file-link check; no external URL or anchor validation |
| [e001_physical_config.template.json](e001_physical_config.template.json) | Intentionally unset physical-analysis configuration; cannot run unchanged |
| [e001_LICENSE.md](e001_LICENSE.md) | Explicit licenses for this package |

The generated records include complete, operator-rejected and structurally incomplete examples. A rejected measurement can be structurally valid; an incomplete record is not silently repaired. Raw CSV requires exactly `time_s,amplitude`; physical amplitudes are volts, synthetic amplitudes use `synthetic_arb`. Only fixed-path through-transmission is represented in this first schema. Pulse-echo requires a separate geometry/estimator update and review.

## What the pipeline checks

- Required metadata, supported schema/version and no unexpected fields.
- Data origin and amplitude units; raw-file SHA-256 and path containment.
- Finite samples, monotonic time, sample-interval consistency and window coverage.
- Configured low signal, peak/noise ratio, rail saturation, ambiguous peaks and boundary peaks.
- Declared operator rejection, contact/trigger faults and nonpositive corrected transit.
- Duplicate JSON keys are refused rather than silently taking the last value.

Rejected records retain metrics and reasons; apparent speed and its uncertainty are withheld. A software quality pass is not evidence that coupling is physically correct or that a measurement is valid. Plausible-looking but wrong traces can still pass these limited checks.

## Audit a declared group of records

```sh
python e001_batch.py e001_reference.json e001_changed.json e001_reduced.json e001_incomplete.json --config e001_demo_config.json --out e001_batch_output
```

Expected: **4 declared, 2 accepted, 1 rejected, 1 invalid; exit code 1**. Open
`e001_batch_output/index.html` or inspect `manifest.json`. Use a new output
directory each time. The batch records input, configuration and code hashes,
preserves invalid records in the denominator and does not pool measurements
across sessions. It does not infer independent sample size. Exit 0 means all
records passed software checks; exit 2 means quality rejections without invalid
records; exit 1 means invalid records or a batch-level input error. The latter
may prevent creating a manifest. See [reproduction details](e001_REPLICATION.md).

## Estimator and uncertainty limitations

This example finds the absolute peak in a prespecified time window after subtracting the noise-window mean. It subtracts supplied trigger time and electronic delay and divides supplied path length by the resulting peak transit time. It is **not a validated time-of-flight, attenuation, elastography or tissue classifier**. Oscillatory RF, multipath, ringing and changed pulse shape can bias the peak substantially. Do not report its output as calibrated sound speed without validating an appropriate estimator.

The reported **partial standard uncertainty** combines sample quantization (`dt/sqrt(12)`), supplied trigger/delay standard uncertainties and supplied path standard uncertainty, assuming independence. It excludes estimator bias, coupling, temperature dependence, correlation and model error. Zero values in toy inputs express generator assumptions, not perfect instrumentation. No full error budget, between-session confidence interval or diagnostic accuracy is claimed.

Noise/peak/rail thresholds are unit- and instrument-dependent. Toy thresholds cannot analyze a record labelled physical. Fill the physical configuration only after equipment characterization and protocol review, then freeze it before confirmatory acquisition. Do not relabel generated data as physical.

## Physical experiment readiness

Use the protocol and checklist first. Equipment, exposure settings, material properties, sample size, numerical tolerances and the full uncertainty budget remain unresolved until documented and reviewed. There is no hardware driver or human-testing procedure in this package. Do not use it to control an instrument or make medical decisions.

Invitation: **independent acoustic protocol review**. Review the fixed-path baseline, estimator choice, coupling/reseating controls and uncertainty budget. Open an issue titled `E001 independent protocol review`, identifying the specific protocol section and proposed correction.

## Relationship to existing material

This executable package operationalizes the existing Experiment 001 outline; it does not supersede its unexecuted physical status. Source architecture, evidence register and programme remain in the repository's research library. Original software is Apache-2.0; original documentation and synthetic example records are CC BY 4.0 as scoped in [e001_LICENSE.md](e001_LICENSE.md). No physical dataset is included.
