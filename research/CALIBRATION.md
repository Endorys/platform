# Calibration and uncertainty

Calibration links measurements to references and defines where those links remain valid. It does not remove every confounder or prove a clinical interpretation.

| Layer | Reference and record |
|---|---|
| Electronic chain | Known signal, gain/bandwidth, delay, noise and clipping |
| Acoustic source/path | Reference receiver or appropriate reference method; waveform and transfer function |
| Geometry | Independently measured distances/poses and fixture tolerances |
| Contact | Defined coupling preparation, pressure/contact indicators and reseating history |
| Mechanical | Load/displacement references, boundary conditions and loading history |
| Electrical | Known impedance reference, electrode arrangement and contact dependence |
| Registration | Spatial/time transforms with uncertainty and validity bounds |

Every calibration needs an ID, date, operator, hardware revision, raw references, method, uncertainty, environmental conditions and expiry/recheck rule. Store unsuccessful calibration attempts. Propagate uncertainty to reported quantities; correlated errors must not be counted as independent. Report model-dependent assumptions separately from instrument error.

A useful first budget lists geometry, timing, temperature, coupling, repeatability and reference uncertainty. If the proposed tissue difference is smaller than the combined uncertainty, the experiment cannot support that distinction.
