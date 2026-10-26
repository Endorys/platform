# Software development plan

## Proposed modules
1. Instrument adapters expose capabilities and preserve raw device output.
2. Scheduler implements explicit source/path states and fault handling.
3. Calibration registry ties results to hardware and reference revisions.
4. Storage preserves immutable raw records and derived-file lineage.
5. Geometry/registration retains transforms and associated uncertainty.
6. Reference estimators provide transparent baselines before complex inversion.
7. Quality controls detect missing, clipped, disconnected and mistimed records.
8. Reporting displays estimates with uncertainty, assumptions and rejection reasons.

Each module should accept versioned inputs and expose reproducible outputs. Hardware drivers and diagnostic models have not been implemented in this documentation release.

## Runnable example
[synthetic_acoustic_demo.py](synthetic_acoustic_demo.py) generates deterministic toy waveforms and checks a simple peak-based transit-time estimator. Run with Python 3 using only its standard library. Its output directory is created locally. This illustrates data provenance and a fault flag; it does not model transducer physics, scattering, realistic coupling, clinical tissue or an Endorys device.

## Verification priorities
Test clock/sample integrity, file round-trips, calibration lineage, explicit fault states and independent-session evaluation when hardware exists. Do not treat passing software checks as physical validation.
