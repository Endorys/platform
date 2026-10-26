# Hardware development plan

Status: specification work, not a manufactured device or verified purchasing list.

| Subsystem | Selection question | Bench verification |
|---|---|---|
| Acoustic source | Required bandwidth, pulse energy and impedance? | Output waveform and repeatability under intended load |
| Path selector | Physical switching principle and passive-contact losses? | Insertion loss, dispersion, leakage and settling |
| Receive chain | Required channels, bandwidth and dynamic range? | Noise, gain, clipping and inter-channel response |
| Digitizer and clock | Required sampling, timing precision and storage? | Trigger latency, skew, drift and dropped records |
| Contact/geometry | How will coupling and positions be measured? | Reseating and independent geometry comparison |
| Mechanical interface | What load and displacement are required? | Calibration, boundary conditions and repeatability |
| Electrical sensing | What electrode arrangement is justified? | Contact dependence and calibrated electrical reference |
| Power and enclosure | What hazards and interference exist? | Qualified review and applicable laboratory checks |

Start with external instruments and a simple fixture. Do not freeze a large array before measuring one source/contact/receiver chain. Record part numbers, revisions, suppliers, calibration status and datasheets when selected. Costs, channel counts and carrier bands remain unspecified. No CAD, Gerbers or electrical schematics are claimed to exist in this release.
