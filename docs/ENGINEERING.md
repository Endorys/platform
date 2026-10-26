# Engineering and reproduction guide

[Documentation home](README.md) · [Quick start](../GETTING_STARTED.md)

## System contracts

| Engineering question | Canonical document |
|---|---|
| How does the proposed system connect? | [Architecture](../research/ARCHITECTURE.md) |
| Which hardware choices remain open? | [Hardware plan](../research/HARDWARE_PLAN.md), [BOM template](../research/BOM_TEMPLATE.csv) |
| What happens during an acquisition? | [Timing and state sequence](../research/ACQUISITION_AND_TIMING.md) |
| How are references and uncertainty recorded? | [Calibration](../research/CALIBRATION.md) |
| What must every measurement contain? | [Data specification](../research/DATA_SPECIFICATION.md), [example record](../research/observation_example.json) |
| Which software modules are proposed? | [Software plan](../research/SOFTWARE_PLAN.md) |
| What is runnable now? | [Synthetic acoustic example](../research/synthetic_acoustic_demo.py) |
| What physical work comes first? | [E001](../research/EXPERIMENT_001.md) |

## Reproduction package for a future experiment

Include protocol revision, hardware/fixture revisions, instrument settings, calibrations, specimen/session identifiers, raw-file checksums, analysis command and environment, results and failed runs. Raw files should remain unchanged; derived files need lineage.

No device build instructions or native manufacturing files are available yet. The BOM is an unselected template. The synthetic example requires no hardware and is not a realistic acoustic simulator.

## Expansion rule

Add a new implementation folder only when it contains actual maintained implementation. Do not create empty hardware/firmware/clinical-model trees to imply maturity. For large future datasets, publish a versioned manifest and appropriate storage/provenance rather than filling Git history with unreviewed binaries.
