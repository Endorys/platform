# Research data specification

Status: proposed schema. No patient or physical measurement dataset is included.

## Minimum record
- Identity: experiment, run, specimen/session pseudonym, protocol version and data origin (synthetic/physical).
- Timing: trigger, clock domain, sampling interval, channel offsets and synchronization uncertainty.
- Excitation: source/path IDs and configured waveform settings.
- Geometry/contact: coordinate system, measured positions, coupling preparation and uncertainty.
- Context: temperature, loading history and relevant environmental conditions.
- Instrumentation: hardware revision, channel map, gain/filter settings and calibration IDs.
- Files: raw path, format, units, sample shape and checksum.
- Quality: missing data, saturation, timing/contact faults and exclusion reasons.
- Analysis: code/version, parameters, estimator assumptions, outputs and uncertainty.

Use SI units with explicit unit fields. Preserve original sensor sampling and native spatial support. Derived or registered arrays must link to source records. Split evaluation by specimen/session to avoid leakage. Never substitute absent values with plausible-looking measurements.

Public examples must be synthetic or appropriately authorized and de-identified. Do not upload names, medical records, identifiers or private device exports. A new dataset requires its own provenance, permissions and reuse terms.
