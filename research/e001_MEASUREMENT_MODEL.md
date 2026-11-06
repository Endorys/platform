# E001 measurement-model review: what does the reported quantity mean?

30 October 2026 · Planning note, not a validated physical measurement procedure.

## Decision needed before physical acquisition

Write down **which distance and which propagation time describe the same path**.
The current software reports a toy `apparent_speed_m_per_s = L / tau`, with
`tau = peak_time - trigger_time - electronic_delay`. This can only be interpreted
as a single-medium speed if that distance and corrected time actually isolate
the intended medium and the estimator is reference-checked. For a path containing
water, coupling layers and phantom material, it generally represents an
effective path quantity instead.

This is a model limitation of the current E001 illustration, not a newly
implemented correction or a claim that the estimator is physically validated.

## A simple layered-path counterexample

Consider an idealized one-way, straight, normally incident path. Assume zero
electronic delay, no dispersion, no refraction, no interface delay and a perfect
arrival estimator. If water and a sample occupy distances `Lw` and `Ls`, then:

```text
tau = Lw/cw + Ls/cs
effective_path_speed = (Lw + Ls)/tau
```

Dividing just the sample thickness `Ls` by the whole-path time `tau` does not
recover the sample speed `cs`. Dividing the total path length by `tau` produces
the effective speed, which also need not equal `cs`. Calibration of electronic
delay alone does not remove the water contribution.

For an ideal fixed-separation substitution thought experiment, replacing a
sample-length water segment with the sample gives:

```text
delta_tau = tau_with_sample - tau_water_reference
delta_tau = Ls/cs - Ls/cw
cs = Ls / (delta_tau + Ls/cw)
```

These relations are a direct algebraic illustration under the assumptions
above. They are **not implemented in E001**, do not specify apparatus and are
not a replacement for a reviewed reference procedure. Timing differences,
geometry changes, interfaces, temperature, pulse distortion and peak bias still
need evaluation. Pulse-echo has different travel paths and must not reuse a
one-way expression by changing a label.

Cook, Bouchard and Emelianov's phantom study uses an experimentally specified
echo/reference arrangement and separates sample and water path contributions.
Its setup and equations should be assessed in their own context; they cannot
be substituted into E001 without changing its geometry and estimator contract.
[Primary study, methods §2.1.1](https://pmc.ncbi.nlm.nih.gov/articles/PMC3207386/).

## Partial uncertainty: avoid a complete-looking answer

For the illustrative single-path model `c = L/tau`, first-order propagation with
independent inputs gives the familiar relative terms for distance and time.
The code currently includes sampling quantization plus supplied trigger,
electronic-delay and distance standard uncertainties. That remains a **partial
budget**. It excludes estimator bias, interfaces, coupling/reseating,
temperature/reference variation, geometry-model error and other relevant terms.

A shared clock, reference trace, fixture or calibration may correlate input
quantities. Correlations cannot be dismissed merely because the data fields
have different names. First-order propagation itself also needs review if
nonlinearity is material. See the GUM's separate treatments of independent and
correlated inputs in [JCGM 100:2008, §5](https://www.iso.org/sites/JCGM/GUM/JCGM100/C045315e-html/C045315e_FILES/MAIN_C045315e/05_e.html).
Use the [BIPM guides catalogue](https://www.bipm.org/en/web/guest/publications/guides)
to identify the edition/amendments appropriate to a future procedure.

## Worksheet to complete with the laboratory reviewer

| Question | Required entry before freeze |
|---|---|
| What is the measurand? | Exact quantity, units, conditions and intended interpretation |
| Which path is timed? | Drawing with every medium/interface and one-way or round-trip definition |
| Which distance is measured? | Matching path segment(s), method, uncertainty and fixture revision |
| What reference is used? | Trace/material provenance, conditions, validity and comparison method |
| How is arrival determined? | Estimator, window, independent bias evaluation and failure cases |
| Which corrections apply? | Delay/path/reference terms, signs, uncertainties and dependencies |
| Which nuisance terms remain? | Temperature, coupling, alignment, drift, dispersion and reseating |
| What counts as an independent unit? | Specimen/session/operator definitions and within-unit repeats |
| What prevents false acceptance? | Known-condition controls and prespecified rejection/acceptance criteria |

No numerical acceptance threshold or physical acquisition setting is supplied
by this note. See the [review brief](e001_REVIEW_BRIEF.md) and
[protocol worksheet](e001_PROTOCOL.md). Passing the software checks does not
resolve any of these open measurement-model decisions.

License: original documentation CC BY 4.0; cited third-party works retain their
own terms and are not relicensed by Endorys. See [package scope](e001_LICENSE.md).
