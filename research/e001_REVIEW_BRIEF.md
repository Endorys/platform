# E001: request for an independent acoustic protocol review

30 October 2026 · Sadhu Shobab Bollipo / Endorys

## The request

Review the proposed **fixed-path, non-biological through-transmission baseline**
before Endorys obtains physical data. A useful contribution is a specific
correction to the protocol or measurement assumptions. Endorsement, investment
and clinical validation are not being requested.

Read the [protocol worksheet](e001_PROTOCOL.md) and the estimator/uncertainty
limitations in [the runnable package](e001_README.md). Optional: run the
[software reproduction exercise](e001_REPLICATION.md).

## Current evidence

| Available | Still missing |
|---|---|
| Versioned record structure, hash checks and toy waveform examples | Verified physical records and acquisition provenance |
| Absolute-peak illustration and partial uncertainty calculation | Reference-checked estimator and complete uncertainty budget |
| Failure-preserving batch report and software tests | Characterized apparatus, coupling control and independent replication |
| Planned pilot/freeze/confirmation stages | Reviewed numerical acceptance limits and justified independent sample count |

No integrated device, human experiment, validated diagnostic result or validated
elasticity/tomography capability is established by this package.

## Five decisions on which we need help

1. **Baseline geometry:** Is fixed-path through-transmission an appropriate first
   measurement for the stated question? Which fixture/geometry confounder should
   be eliminated before a routed-source comparison is attempted?
2. **Observable and reference:** Which measurable quantity and independently
   characterized reference are feasible with the proposed available equipment?
   A reviewer may recommend narrowing the question to repeatability first.
3. **Arrival estimator:** What waveform features, ringdown and multipath make
   the current absolute peak inappropriate? What reference experiment would
   bound estimator bias before any apparent-speed claim?
4. **Uncertainty and controls:** Which omitted terms dominate? Identify how
   coupling, removal/reseating, path measurement, temperature, trigger and drift
   should be separated. State any correlations that matter.
5. **Go/revise/stop criteria:** What pilot information is needed to freeze
   acceptance limits and sample size? Which negative result should stop the
   proposed next step rather than trigger retrospective threshold tuning?

## Suggested review response

For each correction, provide the protocol section, concern, proposed change,
verification needed, and a primary reference where applicable. Distinguish
mandatory changes from optional improvements. If equipment details are needed,
name the missing specification; do not assume undocumented hardware exists.

Publish a response through the repository's experiment-proposal issue template,
titled **E001 independent protocol review**. State your relationship to the
project and whether your name/affiliation may be quoted. A public comment alone
will not be represented as institutional endorsement.

Success for this review is a narrower, testable protocol and a written list of
remaining blockers. Physical acquisition remains deferred until those blockers
and laboratory procedures are resolved.

License: original documentation CC BY 4.0; see [package scope](e001_LICENSE.md).
