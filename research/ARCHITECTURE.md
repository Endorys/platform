# Endorys architecture

Status: proposed research architecture, 26 October 2026. No integrated physical performance is established by these documents.

## Central idea
Endorys investigates whether ultrasound-led, controlled tissue interrogation can produce repeatable measurements of tissue response. Matrix is the conformal sensor interface; Insight is external acquisition analysis and interpretation. Additional modalities are hypotheses whose incremental value must be measured, not assumed.

## Acoustic chain
A selectable source bank drives one active source at a time. A programmable physical path connects that source to a selected passive transmit contact. Distributed receive elements measure the resulting acoustic response. A passive contact is not an independently powered transmitter. Every path introduces insertion loss, dispersion, reflections, settling time and possible leakage; these require measurement before scaling the array.

The acquisition sequence is: enter safe state, select source, select path, settle and verify, trigger excitation, acquire the receive window, preserve raw signals and metadata, deselect. Timing errors and coupling changes must be distinguished from tissue changes. A conventional direct transducer arrangement is a necessary baseline against which the routed concept is compared.

## Branch responsibilities
| Branch | Responsibility | Required interface |
|---|---|---|
| Matrix | Contact, receiving elements, geometry and local sensing | Raw samples, location, contact state, calibration IDs |
| Interface | Controlled mechanical interrogation and application-specific interfaces, including disposable concepts | Applied load, displacement, geometry, time and contact conditions |
| Insight | Signal processing, registration, estimation and uncertainty | Versioned inputs, assumptions, outputs and rejection reasons |
| Continuum | Integration and longitudinal memory | Comparable sessions, calibration lineage and change history |
| Evidence | Measurement and claim validation | Protocols, controls, references, data and negative findings |
| Bench | Reproducible laboratory development | Hardware revisions, fixtures and instrument records |
| Challenge | Stress testing and alternative explanations | Fault injection and confounder reports |
| Explore | Clinical opportunity discovery and materials/NDT research | Specific decision, specimen, comparator and evidence gap |
| Therapy | Proposed treatment-related investigations | Separate exposure, control, safety and efficacy validation |
| Surgical | Proposed intraoperative assistance | Sterile workflow, access, registration and clinical validation |
| Vascular | Vascular application programme | Anatomy-specific measurement and clinical endpoints |

See the [canonical branch register](../BRANCH_REGISTER.md). Research programmes overlap; they are not independent proven products.

## Other sensor streams
Force/strain can establish loading context. Bioimpedance can measure electrical response within electrode-dependent sensitivity volumes. Motion sensing can help track pose but does not automatically recover accurate transducer geometry. Optical, temperature and surface EMG channels are optional and sample different depths and spatial supports. A common timestamp does not make these channels spatially equivalent. Each needs calibration, registration and an explicit reason to exist.

## Frequency and timing
Acoustic carrier frequency, mechanical loading frequency, ADC sampling frequency, pulse repetition frequency and displayed frame rate are different quantities. Their specifications must be derived from the experiment. A controller such as an ESP32 may coordinate states; it is not evidence of sufficient analogue bandwidth or synchronized RF digitization.

## First implementation boundary
Begin with tethered, fixed-geometry, non-biological phantoms and external instruments. Establish an acoustic baseline before adding switching, conformal geometry, mechanics or sensor fusion. Wearability, self-calibration, diagnostic accuracy, digital-twin fidelity and real-time visualization remain separate validation questions.
