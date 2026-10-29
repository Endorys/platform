# E001 acquisition and readiness checklist

Physical status: **not executed**. Empty boxes and TBD values are unresolved requirements, not completed work.

## Equipment inventory to complete

| Item | Model/revision | Relevant ratings/settings | Calibration/reference | Available? |
|---|---|---|---|---|
| Source/pulser and transmit transducer | TBD | TBD | TBD | TBD |
| Receiver and analogue front end | TBD | TBD | TBD | TBD |
| Digitizer and trigger reference | TBD | TBD | TBD | TBD |
| Fixture and path measurement tool | TBD | TBD | TBD | TBD |
| Non-biological reference/changed phantom | TBD | TBD | TBD | TBD |
| Coupling preparation and temperature measurement | TBD | TBD | TBD | TBD |

## Before acquisition

- [ ] Protocol question, comparator, estimator and version frozen after pilot.
- [ ] Numerical limits and analysis config completed; toy thresholds excluded.
- [ ] Instrument compatibility, ratings and source output reviewed by lab personnel.
- [ ] Fixture drawing, coordinate frame and measured geometry recorded.
- [ ] Calibration lineage and timing offsets available.
- [ ] Randomized run order, seed, independent units and sample counts recorded.
- [ ] Raw export and conversion procedure recorded; no personal/clinical data.

## Every run

- [ ] Run/session/specimen IDs and pilot/confirmatory status recorded.
- [ ] Hardware/software revisions, source, gain/filter and clock settings recorded.
- [ ] Actual coupling, pose/load if relevant and temperature context recorded.
- [ ] Native raw trace preserved; converted data and checksums linked.
- [ ] QC flags and operator observations recorded, including failed runs.
- [ ] No plausible values substituted for missing measurements.

## Before sharing a result

- [ ] Structural validation and checksum checks passed, or failure documented.
- [ ] Estimator limitations and complete uncertainty assessment reviewed.
- [ ] Reference drift and between-session/reseating variability reported.
- [ ] Negative findings, all exclusions and deviations disclosed.
- [ ] Protocol/config/analysis versions and immutable dataset manifest included.
- [ ] Dataset provenance, release authorization and dataset-specific license settled.
- [ ] Independent reviewer/operator reproduction recorded where available.

See [protocol](e001_PROTOCOL.md), [results template](e001_RESULTS_TEMPLATE.md) and [license scope](e001_LICENSE.md).
