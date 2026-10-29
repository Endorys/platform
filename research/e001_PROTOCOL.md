# E001 protocol implementation worksheet

Status: draft, unexecuted physical protocol. Version 0.1.0. Scope: non-biological phantoms only. See [software package](e001_README.md).

## Question and primary observable

Candidate question for review: can a conventional fixed-path through-transmission arrangement repeatedly distinguish a predefined phantom/path condition from the reference while recognizing coupling and acquisition failures?

Before a confirmatory experiment, freeze: primary observable; effect/difference of interest; reference method; specimen and session definitions; geometry; estimator; exclusions; numerical acceptance limits; uncertainty budget; randomization; analysis version; and reviewer/date. Peak-transit analysis in the software is illustrative and may need replacement by a validated estimator. No diagnostic endpoint or organ-specific performance is implied.

## Three stages

1. **Characterization/pilot:** select compatible instruments and an independently characterized reference phantom, measure fixture geometry and electronic delay, locate ringdown/usable windows, assess noise and sensitivity to coupling. Pilot data are labelled pilot and excluded from confirmatory claims.
2. **Protocol freeze:** use pilot information and reviewer input to set the detection target, tolerances, sample count and exclusions. Store an immutable dated configuration and its hash. Unset entries block readiness.
3. **Confirmatory acquisition:** use new, randomized runs under the frozen setup; retain all traces and exclusions. Repeat across separate sessions, including removal/reseating. Changes after freeze require a new version and a declared analysis status.

## Conditions and controls

| Condition | Purpose | Must document |
|---|---|---|
| Reference fixture/phantom | Baseline repeatability | Geometry, calibration, source/gain/filter settings, coupling and temperature |
| Predefined changed condition | Test the primary hypothesis | Independent characterization; change one factor at a time |
| Reduced coupling | Sensitivity to contact variation | Actual preparation, not merely a label |
| Removal and reseating | Between-application variability | Operator, geometry measurement and setup sequence |
| Measured path perturbation | Geometry sensitivity | Measured displacement and uncertainty |
| Rated blank/disconnected condition | Acquisition failure control | Instrument-approved procedure; no unsafe electrical fault injection |

Generate and retain the randomized run order using a recorded seed before acquisition. Do not randomize unsafe instrument states without the lab's operating procedure. The plan must specify independent sessions/specimens and within-session repeats; adjacent waveform samples are not independent experimental units. Sample size remains TBD pending the target difference and pilot variance.

## Acquisition sequence

Record readiness and instrument limits → establish reference configuration → acquire calibration/blank records as appropriate → execute randomized run → preserve native raw data → record contact/geometry/temperature/operator observations → verify file integrity → register exclusions without deleting failed runs. Compare reference before/after the sequence for drift. Keep raw exports separate from converted CSV and record conversion software/version and hashes.

Start with a conventional direct source. Routed source/passive-contact comparison is a later experiment requiring matched drive/settings and measurement of loss, bandwidth, dispersion, leakage, settling and repeatability. Added sensors, conformity, therapy and people are outside this protocol.

## Uncertainty and acceptance

Quantify distance, timing, trigger, electronic delay, calibration, source/receive response, temperature, coupling/reseating and estimator/model effects as relevant. Record correlations and distinguish standard uncertainty from expanded uncertainty. The software's partial budget cannot substitute for this review.

Numerical targets: **TBD before confirmatory collection**. Proceed only if the prespecified difference can be interpreted relative to uncertainty and nuisance variation. A failed result triggers revise/stop, not retrospective threshold adjustment. Report quality-control false acceptance and rejection against the known control conditions.

## Required review questions

- Is through-transmission the appropriate geometry for the chosen target and available equipment?
- Is the estimator suitable for the waveform, and how is its bias established?
- Which confounders could reproduce the expected change?
- Are controls, independent units and uncertainty sufficient for the claimed conclusion?
- Are source settings, instrument ratings and laboratory procedures documented?

Deliver using [the results template](e001_RESULTS_TEMPLATE.md), including failed runs. This worksheet does not establish equipment readiness or authorize human experiments.
