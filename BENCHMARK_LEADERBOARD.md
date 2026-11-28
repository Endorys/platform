# Protocol E001 — Open Curved-Surface Coupling Quality Index (CQI) Benchmark Leaderboard

Reproducible reference benchmark tracking multi-operator Speed-of-Sound (`SoS`) repeatability (`CV%`) and boundary reflection suppression (`~1.50 MRayl`) across curved tissue-mimicking phantoms (`R = 35 mm, 60 mm, 90 mm` at `1.70 MHz`).

| Rank | Submission ID | Acquisition Setup | Curvature `R` | Coupling Interface | Mean `CQI` | `SoS` `CV%` | Verification Status |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :---: |
| **1** | `E001-SYN-01` | 6-Element Conformal Array + `CQI` Gate (`k-Wave` FDTD) | `45 mm` | `~1.50 MRayl` Hydrogel (`3 mm`) | **0.84** | **1.4%** | Baseline Reference (`DOI: 10.5281/zenodo.24555614`) |
| **2** | `E001-SYN-02` | Rigid Planar Array + Standard Aqueous Gel (`Unassisted`) | `45 mm` | Standard Gel (`Edge Air Void`) | **0.22** | **8.6%** | Baseline Control (`Rejected by CQI < 0.65`) |
| *Open* | *Pending Lab* | *Verasonics Vantage / un0rick Physical Phantom Capture* | *35–90 mm* | *Open Submission (`v0.2.0`)* | *TBD* | *TBD* | *Awaiting Empirical Lab Dataset* |

## How External Labs Can Submit Results
1. Print the reference curved phantom mold (`hardware/phantoms/endorys_curved_phantom.scad`) or use a calibrated `CIRS 040GSE` curved target (`research/phantom_presets.py`).
2. Capture `N >= 10` multi-operator acquisitions at `1.70 MHz` and evaluate via `research/adapters/verasonics_un0rick_adapter.py` and `research/dicom_sr_exporter.py`.
3. Open a Pull Request updating this table with raw `.uff` / `.csv` waveforms and `TID 1500` JSON logs.
