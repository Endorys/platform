# E001 independent reproduction guide

Version 0.2.0 · 30 October 2026 · **Synthetic software reproduction only.**

The immediate goal remains a reproducible acoustic phantom experiment. The
commands below reproduce the software workflow on generated toy records. They
do not demonstrate acoustic propagation, hardware operation, tissue properties,
tomographic reconstruction or diagnostic performance.

## A 10-minute software review

Use Python 3.11+ and a fresh checkout. No third-party Python packages are needed.
Run these commands from `research/`:

```sh
python -m unittest e001_tests e001_batch_tests -v
python e001_demo.py --out reviewer_demo
python e001_batch.py e001_reference.json e001_changed.json e001_reduced.json e001_incomplete.json --config e001_demo_config.json --out reviewer_batch
```

The last command deliberately returns **exit code 1**, because the incomplete
record is invalid. This is an expected failure example, not a successful batch
with a silently omitted input. Use a new output directory on each invocation.

Open `reviewer_demo/index.html` and `reviewer_batch/index.html` locally. The batch
must contain **4 declared records: 2 accepted, 1 rejected and 1 invalid**. Its
`manifest.json` must preserve all four entries. The rejected record has analysis
and a plot but no apparent-speed estimate; the invalid record has an error and
no analysis output. The original JSON/CSV inputs must remain unchanged.

For an all-accepted toy batch, run:

```sh
python e001_batch.py e001_reference.json e001_changed.json --config e001_demo_config.json --out reviewer_accepted
```

Expected: exit code **0**, 2 accepted, 0 rejected, 0 invalid. Exit code **2** means
at least one quality rejection and no invalid record. None of these exit codes
establishes physical validity.

## What the batch manifest establishes

- Every explicitly declared record has an entry in the original argument order.
- Exact input-record and configuration-file SHA-256 hashes are retained.
- A canonical configuration hash matches the single-record analyzer's convention.
- Analyzer, batch-runner and record-schema file hashes identify the code used.
- Python version and operating-system family help explain environment differences.
- Duplicate record paths block the batch before output. A repeated run ID marks
  the later record invalid instead of overwriting a previous result.
- Missing files, invalid JSON, incomplete metadata and failed integrity checks
  remain visible. Their entries stay in the total declared-record count.

An input hash does not prove that acquisition happened as claimed. An arbitrary
filename, calibration ID or `data_origin` value is not independently verified.
The manifest is a provenance aid, not authentication, accreditation or a frozen
physical protocol. The configuration's file hash is sensitive to whitespace;
its canonical hash is not. On identical software, environment and inputs, the
manifest is deterministic. Cross-version/environment differences must be
reported, not hidden by editing the manifest.

## What to send back

Open a reproducibility-report issue and include:

1. Repository commit ID (`git rev-parse HEAD`) and any local modifications.
2. OS family, Python version and exact command used.
3. Test result and batch count summary, including failed records.
4. Manifest hashes and the first unexpected result/error, if any.
5. Whether the discrepancy persists in a new output directory.

Share only non-sensitive test data you have rights to disclose. Do not upload
patient data, private correspondence or confidential employer instrument files.
Do not describe this software exercise as independent replication of a physical
Endorys experiment.

## Before physical reproduction

Use the [protocol](e001_PROTOCOL.md), [checklist](e001_CHECKLIST.md) and
[review brief](e001_REVIEW_BRIEF.md). Physical configuration values are deliberately
unset in [the template](e001_physical_config.template.json). Equipment, estimator
bias, coupling/reseating controls, tolerances and a full error budget still need
independent review. Do not copy synthetic thresholds into a physical study.

License: original documentation CC BY 4.0; see [package scope](e001_LICENSE.md).
