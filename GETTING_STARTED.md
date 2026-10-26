# Get started with Endorys

## Understand the project in ten minutes

1. Read the [current status](docs/STATUS.md).
2. Follow the [architecture](research/ARCHITECTURE.md) and [branch map](docs/BRANCHES.md).
3. Review the [proof register](research/EVIDENCE_REGISTER.md) before interpreting concept images as capabilities.
4. Read [Experiment 001](research/EXPERIMENT_001.md) to see the immediate research priority.

## Run the synthetic example

Prerequisites: Git and Python 3. The example uses only the Python standard library; no package install, hardware, account or patient data is required.

~~~sh
git clone https://github.com/Endorys/platform.git
cd platform/research
python synthetic_acoustic_demo.py
~~~

On systems where Python 3 is named differently, use python3 or py -3 in place of python.

Expected terminal output:

~~~text
Four synthetic conditions generated; timing and absent-signal checks passed. No physical validation.
~~~

The script creates synthetic_output/ in the working directory: four waveform CSVs and summary.json. The conditions are reference, changed simulated speed, reduced simulated coupling and disconnected signal. It uses a fixed random seed. Its amplitude threshold is chosen only for this toy generator.

Inspect [the script](research/synthetic_acoustic_demo.py), [data specification](research/DATA_SPECIFICATION.md) and [software plan](research/SOFTWARE_PLAN.md). Passing checks confirms this simple implementation behaves as intended; it does not establish acoustic hardware feasibility, tissue identification or clinical performance.

## Choose a first contribution

- Evidence reviewer: verify one primary citation and its exact claim.
- Engineer: propose a measured error budget for E001.
- Software contributor: improve a reproducible example with explicit assumptions.
- Domain specialist: define one application decision and its independent reference.

Use the [contribution guide](CONTRIBUTING.md). Hardware specifications, physical datasets and licensing are unresolved; do not assume a complete buildable device is available.
