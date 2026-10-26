# Acquisition and timing

A measurement record must identify the source, selected path, receiver channels, trigger event, clock domain, sample interval and calibration revision. Schedule source selection and mechanical loading explicitly; switching transients must settle before an accepted acquisition.

## State sequence
Safe idle → select source → select path → verify/settle → trigger → receive window → integrity check → store raw record → deselect → safe idle. Timeouts, invalid paths and storage failures return to a defined safe state and produce a failed-run record.

## Clock integrity
A shared clock is preferred where feasible, but must still be measured for channel skew and drift. If devices have independent clocks, record synchronization events and estimated offset/drift uncertainty. Do not infer simultaneous sampling from matching software timestamps. Preserve raw timing rather than resampling away discrepancies.

## Bandwidth budget
Derive analogue bandwidth, anti-alias filtering and ADC rate from the acoustic waveform. Distinguish RF acquisition from envelope, mechanical and physiological channels. State any decimation and its filters. Record trigger delay and source ringdown, dropped samples, saturation and incomplete channel sets.

## Prototype acceptance
Compare observed timing with an independent reference, repeat after restart and temperature changes, and retain failure traces. Numerical limits depend on the intended measurement and are not established here. A dashboard animation is not evidence of acquisition latency.
