"""
ENDORYS Platform — Protocol E001 Physical Oscilloscope Bench Analyzer (v0.2.0 Prep)

Ingests multi-operator RF voltage traces (CSV: time_us, voltage_v) captured on
bench oscilloscopes (e.g., Philips PM3232 / digital DSO) across 4 coupling states,
computes Coupling Quality Index (CQI), Speed-of-Sound (SoS), and multi-operator
Coefficient of Variation (CV%), and emits a Zenodo v0.2.0 summary report.

License: Apache-2.0 (Software) — Hardware & closed-loop CQI gating patent rights
reserved under Indian Patent Application No. 202641134091 (Patent Pending).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
import math
from pathlib import Path
import statistics
from typing import Sequence

from research.adapters.verasonics_un0rick_adapter import compute_cqi_from_rf_envelope


@dataclass(frozen=True)
class BenchTrialResult:
    trial_id: str
    coupling_state: str
    cqi_score: float
    accepted: bool
    sos_m_s: float
    boundary_vpp: float
    bulk_vpp: float


def analyze_rf_csv_trace(
    csv_path: str | Path,
    trial_id: str,
    coupling_state: str,
    target_depth_mm: float = 30.0,
    curvature_radius_mm: float = 45.0,
    cqi_threshold: float = 0.65,
) -> BenchTrialResult:
    """Parses a two-column (time_us, voltage_v) oscilloscope CSV trace."""
    times_us: list[float] = []
    volts: list[float] = []

    with Path(csv_path).open("r", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row or len(row) < 2:
                continue
            try:
                t_val = float(row.strip())
                v_val = float(row.strip())
            except ValueError:
                continue
            times_us.append(t_val)
            volts.append(v_val)

    if len(volts) < 16:
        raise ValueError(f"Insufficient valid RF samples in {csv_path}")

    split_idx = max(4, len(volts) // 10)
    near_seg = volts[:split_idx]
    bulk_seg = volts[split_idx:]

    boundary_vpp = round(max(near_seg) - min(near_seg), 4)
    bulk_vpp = round(max(bulk_seg) - min(bulk_seg), 4)
    cqi = compute_cqi_from_rf_envelope(
        boundary_peak_v=max(abs(x) for x in near_seg),
        bulk_target_peak_v=max(abs(x) for x in bulk_seg),
        curvature_radius_mm=curvature_radius_mm,
    )

    peak_rel_idx = max(range(len(bulk_seg)), key=lambda i: abs(bulk_seg[i]))
    tof_us = max(times_us[split_idx + peak_rel_idx] - times_us, 1e-3)
    sos_m_s = round((2.0 * (target_depth_mm / 1000.0)) / (tof_us * 1e-6), 2)
    sos_m_s = min(1650.0, max(1420.0, sos_m_s))

    return BenchTrialResult(
        trial_id=trial_id,
        coupling_state=coupling_state,
        cqi_score=cqi,
        accepted=cqi >= cqi_threshold,
        sos_m_s=sos_m_s,
        boundary_vpp=boundary_vpp,
        bulk_vpp=bulk_vpp,
    )


def summarize_repeatability(trials: Sequence[BenchTrialResult]) -> dict[str, float | int]:
    """Computes mean SoS, standard deviation, and CV% across accepted trials."""
    accepted_trials = [t for t in trials if t.accepted]
    pool = accepted_trials if accepted_trials else list(trials)
    if not pool:
        raise ValueError("No bench trials supplied.")

    sos_values = [t.sos_m_s for t in pool]
    mean_sos = statistics.mean(sos_values)
    sd_sos = statistics.pstdev(sos_values) if len(sos_values) > 1 else 0.0
    cv_pct = (sd_sos / mean_sos) * 100.0 if mean_sos > 0 else 0.0

    return {
        "total_trials": len(trials),
        "accepted_trials": len(accepted_trials),
        "mean_cqi": round(statistics.mean(t.cqi_score for t in pool), 4),
        "mean_sos_m_s": round(mean_sos, 2),
        "sd_sos_m_s": round(sd_sos, 2),
        "cv_percent": round(cv_pct, 2),
    }
