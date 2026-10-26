# Dated literature and prior-art review

Original review: 16 October 2026. Reconciled with the Endorys name on 26 October 2026. This is a bounded research review, not an exhaustive search, patent clearance or fresh verification of every linked page. External demonstrations do not validate Endorys.

# Endorys: prior-art and physical-evidence map

Research date: 16 October 2026. Scope: the 28-item physical-proof checklist, with targeted searches of journal/publisher sites, PubMed/PMC, author/institutional repositories, conference/project publications and selected patent disclosures. This is a bounded evidence review, not an exhaustive systematic review, patentability opinion or freedom-to-operate search. No priority date or detailed Endorys claims were supplied, so references are technical precedents rather than legally determined prior art against a particular filing.

## How to read the findings

- **Physical precedent:** a related capability was measured in a real system, phantom, specimen, animal or human study. It does not validate every implementation or establish independent replication.
- **Partial precedent:** only a subset, constrained geometry, limited sample, or restricted operating condition was demonstrated.
- **Not established here:** no matching physical demonstration identified in this review. This is not evidence that none exists.
- **Implementation proof:** Endorys must still demonstrate its own accuracy, uncertainty, reliability and safety even when the underlying measurement is established.

Evidence access varied: some sources were accessible as full text or manuscript, others as publisher/PubMed abstracts and figure descriptions. Numerical findings below are paper-reported, not independently reproduced. Search-engine crawl labels were not treated as publication dates. In particular, the 2026 EIT-US paper is dated September 4 in PubMed despite its January eCollection label.

## Main finding

Most individual sensing and tissue-mechanics ideas have physical precedents. Several combinations also have precedents: conformal ultrasound with elasticity mapping; ultrasound with EMG; EMG with force and ultrasound timing; ultrasound-guided electrical tomography; simultaneous EMG and multi-frequency impedance; and electrical, thermal and mechanical tissue phenotyping. The full Endorys combination and its proposed parameter accuracy and clinical advantage remain unestablished in the evidence examined.

## All 28 proof items

| # | Item | What has already been physically demonstrated | What remains for Endorys |
|---|---|---|---|
| 1 | Ultrasound signal quality | Flexible/stretched arrays have produced phantom and human images; cardiac and transcranial examples exist [1,2,3]. | Actual element sensitivity, bandwidth, depth, SNR, acoustic field and image quality across operating shapes. |
| 2 | Sparse transmit / dense receive | Single-element transmissions with multi-element reception and sparse synthetic transmit/full synthetic receive acquisition precedents exist [4,5]. | Exact unequal TX/RX layout, small-receiver sensitivity, aperture sampling, grating lobes, motion tolerance, channel/power/data tradeoffs. Sequential multiplexing is not simultaneous dense acquisition. |
| 3 | Array geometry tracking | FLEX used optical tracking on phantoms and cadaveric specimens; direct-wave element localization also has experiments [6,7]. | Tracking a genuinely stretching 3-D sheet during use, with sufficient element-position/orientation accuracy and no confounding with sound speed. |
| 4 | Contact and coupling | Bioadhesive coupling enabled 48-hour organ imaging [8]; acoustically matched EMG electrodes were tested [9]. | Local contact-pressure/coupling maps, air-gap detection and separating contact changes from tissue changes. |
| 5 | Channel phase/timing coherence | Synthetic-aperture RF acquisition and phase-based shear-wave measurements have physical demonstrations [4,10]. | Measured channel skew, phase stability and calibration drift in Endorys electronics, including deformation/temperature effects. |
| 6 | Multimodal synchronization | Ultrasound/EMG/force timing studies [11], synchronized sonomyography/EMG/joint-angle recording [12], and an integrated US/EMG patch [13]. | A measured common-clock error budget for every modality and sequence. Published correlation is not proof of Endorys's timestamp precision. |
| 7 | Interference | Acoustic-transparent EMG electrodes and integrated acoustic/electrochemical sensing show that selected combinations can coexist [9,14]. | Simultaneous ultrasound pulsing, impedance injection and ECG/EMG amplification without saturation, rectification, aliasing or artifacts. |
| 8 | 3-D reconstruction | Conformal transcranial volumetric imaging and stretchable 3-D modulus mapping demonstrated [1,2]. | Accuracy/resolution across Endorys's changing geometry, heterogeneous propagation and claimed anatomical targets. |
| 9 | Multi-angle / anisotropy | Direction-dependent muscle elasticity/viscosity and nonlinear anisotropic muscle measurements have physical studies [10,15]. | Distinguishing intrinsic tissue anisotropy from beam angle, polarization, load and array-shape effects. Multi-angle intensity alone is not a full material tensor. |
| 10 | Multi-frequency response | Acoustic backscatter measured across MHz bands [16]; mechanical shear dispersion across much lower frequencies [10]. | Calibrated frequency response and enough independent bandwidth. Acoustic carrier frequency and mechanical excitation frequency are different axes. |
| 11 | Quantitative acoustic properties | Breast waveform tomography recovers sound-speed maps from human data; calibrated phantom work measures attenuation/backscatter [16,17]. | Joint sound speed/attenuation/scattering inference from the actual limited aperture, including uncertainty and parameter crosstalk. |
| 12 | Displacement / strain | Elastography has longstanding precedent [18]; stretchable arrays mapped displacement and strain in phantoms [2]. | 3-D tracking accuracy, decorrelation limits, out-of-plane motion and dynamic boundary handling. |
| 13 | Stiffness / elasticity | Compression elastography and stretchable modulus mapping demonstrated [2,18]. | Absolute versus relative modulus, known stress/boundaries, model assumptions and comparison with independent mechanics. |
| 14 | Viscoelasticity | SDUV estimated elasticity and viscosity in bovine muscle and swine liver [10]; MUVE measured hydrogel viscoelasticity [19]. | Recovering G-prime/G-double-prime over a specified mechanical frequency band using the actual actuator and inverse model. |
| 15 | Creep / relaxation / hysteresis | MUVE measured creep-derived hydrogel properties [19]; ultrasonic/mechanical skin experiments examined stress effects [20]. | Reliable cyclic loading, relaxation/creep parameter estimation and hysteresis maps; separate tissue dissipation from actuator, adhesive and slip losses. |
| 16 | Nonlinear response | Nonlinear shear-modulus phantom experiments [21] and ex vivo/in vivo anisotropic muscle work [15]. Acoustic B/A imaging also demonstrated in biological specimens [22]. | Distinguish nonlinear mechanical elasticity from acoustic B/A. Calibrate load and waveform distortion; identify the intended coefficient. |
| 17 | Poroelastic response | Controlled fluid-content/flow phantoms physically characterized [23]. Relevant ultrasound inverse-model papers include simulations [24]. | Independently validate permeability/fluid parameters and separate fluid redistribution from viscoelastic relaxation and boundary effects. A long time constant alone is not permeability. |
| 18 | Flow | Conformal transcranial volumetric Doppler work provides a physical flow-imaging precedent [1]. | Accuracy against a flow reference, angle/motion dependence, vessel geometry and regional perfusion claims. Doppler velocity, blood pressure and tissue perfusion are not interchangeable. |
| 19 | Bioimpedance | Physical electrical-standard validation [25]; wearable simultaneous EMG/multi-frequency EIM [26]. | Electrode/contact model, current-source accuracy, phase calibration, motion artifacts and spectral reproducibility in the integrated patch. |
| 20 | Cross-modal spatial registration | Ultrasound-guided EIT has phantom/patient evidence for muscle and prostate [27,28]. | A validated 3-D correspondence and sensitivity-volume model. Interpolating coarse EIT onto fine US voxels does not create fine electrical resolution. Surface EMG is also spatially distributed. |
| 21 | Electrical-mechanical timing | US/EMG/force experiments measured electromechanical delay in humans [11]; very-high-frame-rate ultrasound also studied stimulated muscle timing [29]. | Modality-specific latency, onset definition and physiological repeatability; do not infer cellular activation timing from a surface signal without validation. |
| 22 | Longitudinal repeatability | 48-hour imaging and 72-hour US/EMG wearing demonstrated [8,13]; quantitative-US reproducibility tested across sonographers/probes [30]. | Removal/reapplication, day-to-day alignment, operator variation, recalibration and minimum detectable biological change. Continuous attachment is not repositioning reproducibility. |
| 23 | Added value from fusion | US/EMG patch reported better classification/screening than individual modalities [13]; US/EIT studies provide complementary electrical-anatomical information [27]. | Blinded, held-out, task-specific comparisons against each modality and credible baselines, with uncertainty and effect size. Not universal superiority. |
| 24 | Parameter identifiability | Individual/subset inversions have physical precedents [2,10,17,19,27]. | No matching demonstration identified of Endorys's entire tissue-state vector recovered independently in the same changing 3-D region. Factorial phantoms and sensitivity/identifiability analysis remain essential. |
| 25 | Uncertainty / failure detection | Probe-contact confidence algorithms have phantom/experimental evaluations [31]. | Calibrated uncertainty for all reported parameters under poor contact, channel loss, motion and out-of-distribution tissue. Image confidence is not parameter confidence. |
| 26 | Durability / wearability | Mechanical cycling in cardiac-array work [3], 48-hour attachment [8] and 72-hour US/EMG wearing [13]. | Exact stack's fatigue, electrode corrosion, cleaning, ingress, lead strain, repeated use and calibration stability. |
| 27 | Physical safety | Prior human devices demonstrate that selected designs/protocols can be studied [1,3,8,13]. | No safety evidence for Endorys supplied. Measure acoustic output, temperature, leakage/injected current, isolation, fault conditions and skin-contact compatibility for the actual design and exposure schedule. Other devices' human studies do not transfer safety. |
| 28 | Clinical usefulness | Application-specific early human evidence exists for US/EMG and US/EIT [13,27,28]. | A defined intended use, reference standard, representative cohorts and prospective validation. No evidence identified here for Endorys replacing CT/MRI or universally diagnosing fibrosis/inflammation/edema/cancer. |

## Closest integrated precedents

1. **Stretchable 3-D tissue-modulus mapping (2023) [2].** Particularly close to conformal ultrasound plus controlled deformation and inverse mechanics. It reduces novelty of that broad combination; it does not demonstrate the complete proposed multimodal stack.
2. **Integrated structural-functional US/EMG wearable (2025) [13].** Human/patient demonstrations, prolonged wear and reported fusion gains. Broad synchronized US/EMG claims are already occupied technically.
3. **Ultrasound-coupled EIT for muscle health (2019) [27].** Phantom and patient measurements; ultrasound-defined anatomy used in electrical reconstruction, with anisotropy and healthy/diseased comparisons. Important precedent older than the 2026 layered-tissue fusion study [32].
4. **Wearable EMG plus multi-frequency EIM (2022) [26].** Direct precedent for concurrent electrical activation and electrical tissue response; no ultrasound claimed by that paper.
5. **ThrombUS+ [33,34].** Published project architecture combines compression ultrasound, electrical impedance plethysmography and light reflection rheography, with actuator-controlled pressure. Project documentation and prototypes are evidence of relevant architecture/development, not proof of a completed validated Endorys-like tissue inversion or diagnostic outcome.
6. **Electro-thermo-mechanical biopsy phenotyping (2023) [35].** Electrical spectra, thermal response and mechanical loading/relaxation measured in excised breast samples. Directly challenges a broad claim that combined physical-response tissue fingerprints are unprecedented; it is not a non-invasive wearable tomographic system.
7. **Combined ultrasound/EIT patent family [36].** Discloses an electrode overlay and co-registered electrical/acoustic images, with a 2008 priority claim. Patent disclosure is not physical validation.

## What the search did not establish

- One deforming conformal device delivering spatially resolved acoustic, full viscoelastic, poroelastic, electrical, electrophysiological and flow parameters together at justified common resolution.
- Reliable separation of all those parameters under motion and controlled loading without geometry/contact artifacts.
- A disease-independent tissue fingerprint or validated universal cross-physics response tensor.
- Reliable long-term reapplication with calibrated changes smaller than placement/contact variation.
- Superiority or equivalence to CT/MRI for an identified clinical task at a stated resolution, depth, speed, cost and accuracy.

These are evidence gaps in this bounded search, not findings of patent novelty. A novel combination can still be obvious or previously disclosed; novelty requires claim-by-claim comparison and dates.

## Practical proof programme after accounting for precedent

**First: reproduce a known baseline.** Use one fixed geometry, a calibrated phantom and one mechanical property. Benchmark against [2], [10] or [19] rather than trying to establish elastography from scratch.

**Second: establish a Endorys-specific improvement.** Predefine one advantage: performance while bending, fewer TX channels at a specified image quality, better contact-aware repeatability, or improved estimation after adding one electrical modality. Hold other factors constant.

**Third: run a parameter-separation test.** Independently vary geometry, contact, stiffness, viscosity and conductivity; show that the output changes for the intended cause and stays stable for confounders. Include withheld phantom combinations.

**Fourth: test fusion against strong baselines.** Compare ultrasound alone, the electrical modality alone, simple feature concatenation and Endorys's joint estimator. Match acquisition time and training data. Do not count structural priors that merely make EIT boundaries resemble ultrasound as independent proof of recovered electrical detail.

**Fifth: prove repeatability and failure awareness.** Reattach across days and operators; deliberately add air gaps, channel failures and motion. Report minimum detectable change and calibrated uncertainty.

Clinical validation follows a single justified intended use. No human experimentation is implied by this report.

## Source register

The numbering is for cross-reference, not ranking or exhaustive coverage. Sources contain physical studies unless explicitly identified as simulation, project documentation or patent disclosure.

1. Zhou et al. **Transcranial volumetric imaging using a conformal ultrasound patch.** Nature 629, 810–818 (2024). https://doi.org/10.1038/s41586-024-07381-5
2. Hu et al. **Stretchable ultrasonic arrays for the three-dimensional mapping of the modulus of deep tissue.** Nature Biomedical Engineering 7, 1321–1334 (2023). https://doi.org/10.1038/s41551-023-01038-w . Author manuscript: https://xugroup.eng.ucsd.edu/wp-content/uploads/2024/02/85_NBME.pdf
3. Hu et al. **A wearable cardiac ultrasound imager.** Nature 613, 667–675 (2023). https://doi.org/10.1038/s41586-022-05498-z
4. Trots, Nowicki and Lewandowski. **Laboratory setup for synthetic aperture ultrasound imaging.** Archives of Acoustics (2007). Single-element transmit/multi-element receive wire-phantom experiments. https://acoustics.ippt.gov.pl/index.php/aa/article/view/554
5. **2-D array for 3-D Ultrasound Imaging Using Synthetic Aperture Techniques.** Sparse synthetic transmit / fully sampled synthetic receive architecture. https://pmc.ncbi.nlm.nih.gov/articles/PMC2894032/
6. **FLEX: FLexible transducer with External tracking for ultrasound imaging with patient-specific geometry estimation.** Phantom/cadaveric evaluation. https://pmc.ncbi.nlm.nih.gov/articles/PMC10998498/
7. **A direct wavepath-based element localization algorithm to enable flexible ultrasound array imaging.** Ultrasonics 138, 107228 (2024). https://doi.org/10.1016/j.ultras.2023.107228
8. Wang et al. **Bioadhesive ultrasound for long-term continuous imaging of diverse organs.** Science 377, 517–523 (2022). https://doi.org/10.1126/science.abo2542
9. Botter et al. **Development and testing of acoustically-matched hydrogel-based electrodes for simultaneous EMG-ultrasound detection.** Medical Engineering & Physics 64, 74–79 (2019). Five-subject tests. https://doi.org/10.1016/j.medengphy.2018.12.002
10. Chen et al. **Shearwave dispersion ultrasound vibrometry (SDUV) for measuring tissue elasticity and viscosity.** IEEE TUFFC 56, 55–62 (2009). https://doi.org/10.1109/TUFFC.2009.1005 ; https://pubmed.ncbi.nlm.nih.gov/19213632/
11. **Detection of the electromechanical delay and its components during voluntary isometric contraction of the quadriceps femoris muscle.** Frontiers in Physiology (2014). https://doi.org/10.3389/fphys.2014.00494 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC4274888/
12. **A System for the Synchronized Recording of Sonomyography, Electromyography and Joint Angle.** https://pmc.ncbi.nlm.nih.gov/articles/PMC2701082/
13. **In situ structural-functional synchronous dissection of dynamic neuromuscular system via an integrated multimodal wearable patch.** Science Advances (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC11708901/
14. Sempionatto et al. **An epidermal patch for the simultaneous monitoring of haemodynamic and metabolic biomarkers.** Nature Biomedical Engineering 5, 737–748 (2021). https://doi.org/10.1038/s41551-021-00685-1
15. **Unravelling anisotropic nonlinear shear elasticity in muscles: Towards a non-invasive assessment of stress in living organisms.** Journal of the Mechanical Behavior of Biomedical Materials 150, 106325 (2024). https://doi.org/10.1016/j.jmbbm.2023.106325
16. **Interlaboratory Comparison of Backscatter Coefficient Estimates for Tissue-Mimicking Phantoms.** Physical 1–12 MHz phantom measurements. https://pmc.ncbi.nlm.nih.gov/articles/PMC3132101/
17. **Frequency Domain Ultrasound Waveform Tomography: Breast Imaging Using a Ring Transducer.** Physics in Medicine & Biology (2015). Human breast data and MRI comparison. https://pmc.ncbi.nlm.nih.gov/articles/PMC4902020/
18. Ophir et al. **Elastography: a quantitative method for imaging the elasticity of biological tissues.** Ultrasonic Imaging 13, 111–134 (1991). https://doi.org/10.1177/016173469101300201 ; https://pubmed.ncbi.nlm.nih.gov/1858217/
19. Hong et al. **Multimode ultrasound viscoelastography for three-dimensional interrogation of microscale mechanical properties in heterogeneous biomaterials.** Biomaterials 178, 11–22 (2018). https://doi.org/10.1016/j.biomaterials.2018.05.057 ; https://pubmed.ncbi.nlm.nih.gov/29902533/
20. **Ultrasonic and viscoelastic properties of skin under transverse mechanical stress in vitro.** Ultrasound in Medicine & Biology (1998). https://www.sciencedirect.com/science/article/abs/pii/S0301562998000714
21. **Nonlinear Shear Modulus Estimation with Bi-axial Motion Registered Local Strain.** Physical phantom/mechanical comparison. https://pmc.ncbi.nlm.nih.gov/articles/PMC6684490/
22. Zhang, Gong and Chen. **Experimental imaging of the acoustic nonlinearity parameter B/A for biological tissues via a parametric array.** Ultrasound in Medicine & Biology 27, 1359–1365 (2001). https://doi.org/10.1016/S0301-5629(01)00432-X ; https://pubmed.ncbi.nlm.nih.gov/11731049/
23. **A New Class of Phantom Materials for Poroelastography Imaging Techniques.** Ultrasound in Medicine & Biology 42, 1230–1238 (2016). https://doi.org/10.1016/j.ultrasmedbio.2015.12.013
24. Theodorou et al. **On the Comparative Suitability of Strain Relaxation and Stress Relaxation Compression for Ultrasound Poroelastic Tissue Characterization.** Frontiers in Physics (2021). Analytical/FEM study; do not count its simulated inverse-recovery results as physical proof. https://doi.org/10.3389/fphy.2021.617993
25. **Physical Validation of a Residual Impedance Rejection Method during Ultra-Low Frequency Bio-Impedance Spectral Measurements.** Circuit-phantom instrument validation. https://pmc.ncbi.nlm.nih.gov/articles/PMC7506680/
26. Ngo et al. **A Wearable, Multi-Frequency Device to Measure Muscle Activity Combining Simultaneous Electromyography and Electrical Impedance Myography.** Sensors 22, 1941 (2022). https://doi.org/10.3390/s22051941 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8914780/
27. Murphy et al. **Toward Electrical Impedance Tomography Coupled Ultrasound Imaging for Assessing Muscle Health.** IEEE Transactions on Medical Imaging 38, 1409–1419 (2019), online December 2018. https://doi.org/10.1109/TMI.2018.2886152 ; https://pubmed.ncbi.nlm.nih.gov/30530320/
28. **Transrectal electrical impedance tomography of the prostate: Spatially coregistered pathological findings for prostate cancer detection.** Human US/EIT and pathology comparison. https://pmc.ncbi.nlm.nih.gov/articles/PMC3676380/
29. Nordez et al. **Electromechanical delay revisited using very high frame rate ultrasound.** Journal of Applied Physiology 106 (2009). https://doi.org/10.1152/japplphysiol.00221.2009
30. **A Phantom-based Assessment of Repeatability and Reproducibility of Transvaginal Quantitative Ultrasound.** https://pmc.ncbi.nlm.nih.gov/articles/PMC6774614/
31. **Identifying visible tissue in intraoperative ultrasound: a method and application.** Experimental contact-confidence evaluation. https://pmc.ncbi.nlm.nih.gov/articles/PMC12518381/
32. Sagar, Nipa and Park. **Ultrasound-guided structural fusion enhances the interpretability of electrical impedance tomography for layered tissue imaging.** Journal of Electrical Bioimpedance 17, 95–120 (2026); PubMed article date September 4. Controlled ex vivo chicken-tissue configurations; not broad patient validation. https://doi.org/10.2478/joeb-2026-0013 ; https://pubmed.ncbi.nlm.nih.gov/42732431/
33. **ThrombUS+ Project: Toward Wearable Continuous Point-of-Care Monitoring for Deep Vein Thrombosis of the Lower Limb.** Computational and Structural Biotechnology Journal (2026). Project concept/advances and prototype development. https://doi.org/10.34133/csbj.0082
34. ThrombUS+ consortium. **D6.1 Specifications**, February 28, 2025. Project architecture, not completed clinical proof. https://zenodo.org/records/14930624/files/ThrombUS_D6.1_v1.pdf?download=1 ; project: https://thrombus.eu/
35. **Label-free multimodal electro-thermo-mechanical (ETM) phenotyping as a novel biomarker to differentiate between normal, benign, and cancerous breast biopsy tissues.** (2023). Excised samples from 14 subjects; exploratory, not a general clinical validation. https://doi.org/10.1186/s13036-023-00388-y ; https://pmc.ncbi.nlm.nih.gov/articles/PMC10644568/
36. **US8886291B2 / WO2009089280A1: Systems and methods for combined ultrasound and electrical impedance imaging.** Patent disclosure; priority claim January 9, 2008. https://patents.google.com/patent/US8886291 ; https://patents.google.com/patent/WO2009089280A1/en
37. **CN120078442B: A flexible integrated array for electromyography and ultrasound co-sensing and its fabrication method.** Patent disclosure; no independent physical-validation conclusion drawn. https://patents.google.com/patent/CN120078442B/en
38. **CN120267335A: Flexible wearable patch.** Patent disclosure relevant to flexible US/EMG integration. https://patents.google.com/patent/CN120267335A/en
39. Steiner, Soleimani and Watzenig. **A bio-electromechanical imaging technique with combined electrical impedance and ultrasound tomography.** Physiological Measurement 29, S63–S75 (2008). Simulation-based improvement, not a physical demonstration. https://doi.org/10.1088/0967-3334/29/6/S06 ; https://researchportal.bath.ac.uk/en/publications/a-bio-electromechanical-imaging-technique-with-combined-electrica/

## Search coverage and unfinished work

Search families included conformal/flexible/stretchable ultrasound; sparse synthetic apertures; array-element localization; US/EMG/force synchronization; ultrasound/EIT fusion and muscle imaging; multi-frequency EIM; modulus, viscosity, creep, nonlinear anisotropy and poroelasticity; quantitative acoustic tomography/backscatter; wearable coupling, repeatability and contact-confidence; integrated project and patent precedents.

This review does not establish citation saturation or an exhaustive database export. Remaining due diligence: detailed supplements and sample-size/risk-of-bias extraction; backward/forward citation tracing; patent family/claim/date analysis; preprint and conference coverage; comparison to a frozen Endorys specification and priority date; disease-specific clinical evidence and full safety-standard assessment. Never interpret an absent match as proof of novelty.

