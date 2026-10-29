# Experiment 001: acoustic measurement versus coupling variation

Status: draft bench protocol; not executed. Scope: non-biological phantoms and appropriately rated laboratory instruments.

## Question
Can a fixed-geometry ultrasound arrangement measure a predefined phantom difference consistently while recognizing contact-related and acquisition failures?

## Setup
Use a pulsed acoustic source, receiver, suitable digitizer, trigger reference, measured fixture geometry, temperature measurement and reference phantom. Document source settings, transducer characteristics, analogue chain, sample rate, instrument limits and calibration. Equipment and parameter values have not yet been selected.

## Design
Establish a direct acoustic arrangement before introducing a switched path. If two independently characterized phantom conditions are available, randomize their measurement order across separate sessions. Include normal coupling, reduced coupling and complete removal/reseating; record actual contact conditions rather than assuming them. Include a measured path-length perturbation to test sensitivity to geometry. Independent experimental units are specimens and sessions, not thousands of adjacent waveform samples.

Preserve unprocessed traces and trigger timing. Measure electronic delay, ringdown and the usable acquisition window. Through-transmission travel time uses d/c; pulse-echo geometry uses 2d/c. Do not interchange them. Peak amplitude alone is not calibrated attenuation: source output, coupling, gain, path and receiver response all contribute.

## Analysis and controls
Predefine the measurement, exclusion rules and uncertainty calculation before inspecting condition differences. Separate within-session repeats from between-session variation. Hold out complete sessions or specimens for evaluation. Include instrument-safe disconnected/blank controls; do not create electrical faults outside equipment ratings.

Report timing and amplitude distributions, signal quality, reseating variation, temperature and path uncertainty. A model should be compared with a simple reference estimator. Document every rejection with a reason and retain the original record.

## Advancement criteria
Numerical tolerances are TBD because no intended measurement specification or calibrated equipment inventory is frozen. Set them before collecting confirmatory data. Advance only when the error budget is appropriate to the intended difference and failure controls are reliably recognized. Otherwise fix coupling, geometry or instrumentation before adding machine learning.

## Deliverables
Protocol version; fixture sketch; hardware inventory; calibration files; randomized run list; raw waveform files and checksums; analysis version; complete results including failures; decision to proceed, revise or stop.


## Executable support package — 29 October 2026

The [E001 package](e001_README.md) now provides a runnable offline pipeline, versioned record schema, integrity and quality checks, synthetic valid/rejected/incomplete examples, waveform plots, and software tests. Use the [protocol worksheet](e001_PROTOCOL.md), [acquisition checklist](e001_CHECKLIST.md) and [results template](e001_RESULTS_TEMPLATE.md) to prepare a physical experiment.

The software demonstration is synthetic only. Its peak estimator and partial uncertainty are illustrative. Numerical physical settings, estimator validation, equipment selection and the full uncertainty budget remain unresolved; this experiment is still not executed.
