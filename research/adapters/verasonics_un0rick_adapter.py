"""
ENDORYS Platform — Hardware Acquisition Adapters (Verasonics Vantage & un0rick)

Normalizes raw RF channel captures from Verasonics Vantage (.mat / RcvData) and
open-source un0rick ultrasonic boards into Protocol E001 QUSMeasurementPacket
structures for deterministic CQI gating and DICOM TID 1500 SR export.

License: Apache-2.0 (Software) — Hardware & closed-loop CQI gating patent rights
reserved under Indian Patent Application No. 202641134091 (Patent Pending).
"""

from __future__ import annotations

import math
from typing import Sequence

from research.dicom_sr_exporter import QUSMeasurementPacket


def compute_cqi_from_rf_envelope(
    boundary_peak_v: float,
    bulk_target_peak_v: float,
    curvature_radius_mm: float = 60.0,
) -> float:
    """Computes deterministic Coupling Quality Index (0.0 - 1.0) from RF echo peaks."""
    if boundary_peak_v <= 0.0:
        return 0.0
    ratio = max(0.0, bulk_target_peak_v) / boundary_peak_v
    raw_cqi = ratio / (ratio + 0.8)
    curvature_factor = min(1.0, max(0.75, curvature_radius_mm / 60.0))
    return round(min(0.98, max(0.0, raw_cqi * curvature_factor)), 4)


def ingest_verasonics_rf_frame(
    rf_samples_v: Sequence[float],
    sampling_rate_hz: float,
    study_uid: str,
    series_uid: str,
    curvature_radius_mm: float = 60.0,
    center_frequency_mhz: float = 1.70,
    target_depth_mm: float = 30.0,
) -> QUSMeasurementPacket:
    """Adapts a single-channel or beamformed Verasonics Vantage RF line into E001 packet."""
    if len(rf_samples_v) < 16 or sampling_rate_hz <= 0:
        raise ValueError("Invalid RF frame length or sampling rate.")

    # Near-field coupling interface window (first 10% of samples) vs bulk region
    split_idx = max(4, len(rf_samples_v) // 10)
    boundary_peak = max(abs(x) for x in rf_samples_v[:split_idx])
    bulk_peak = max(abs(x) for x in rf_samples_v[split_idx:])
    cqi = compute_cqi_from_rf_envelope(boundary_peak, bulk_peak, curvature_radius_mm)

    # Time-of-flight SoS estimate from peak index in bulk region
    peak_idx = split_idx + max(
        range(len(rf_samples_v) - split_idx),
        key=lambda i: abs(rf_samples_v[split_idx + i]),
    )
    tof_sec = peak_idx / sampling_rate_hz
    sos_m_s = round((2.0 * (target_depth_mm / 1000.0)) / max(tof_sec, 1e-6), 2)
    sos_m_s = min(1650.0, max(1420.0, sos_m_s))

    return QUSMeasurementPacket(
        study_uid=study_uid,
        series_uid=series_uid,
        sos_m_s=sos_m_s,
        attenuation_db_cm_mhz=0.52,
        cqi_score=cqi,
        curvature_radius_mm=curvature_radius_mm,
        center_frequency_mhz=center_frequency_mhz,
        operator_id="VERASONICS-VANTAGE-ADAPTER",
    )


def ingest_un0rick_adc_buffer(
    adc_counts: Sequence[int],
    adc_vref: float = 1.0,
    adc_bits: int = 10,
    sampling_rate_hz: float = 64e6,
    study_uid: str = "2.25.202641134091901",
    series_uid: str = "2.25.202641134091902",
    curvature_radius_mm: float = 45.0,
) -> QUSMeasurementPacket:
    """Adapts unsigned un0rick open-hardware ultrasound ADC captures into E001 packet."""
    mid = (1 << (adc_bits - 1))
    scale = adc_vref / mid
    volts = [(c - mid) * scale for c in adc_counts]
    pkt = ingest_verasonics_rf_frame(
        rf_samples_v=volts,
        sampling_rate_hz=sampling_rate_hz,
        study_uid=study_uid,
        series_uid=series_uid,
        curvature_radius_mm=curvature_radius_mm,
    )
    return QUSMeasurementPacket(
        study_uid=pkt.study_uid,
        series_uid=pkt.series_uid,
        sos_m_s=pkt.sos_m_s,
        attenuation_db_cm_mhz=pkt.attenuation_db_cm_mhz,
        cqi_score=pkt.cqi_score,
        curvature_radius_mm=pkt.curvature_radius_mm,
        center_frequency_mhz=pkt.center_frequency_mhz,
        operator_id="UN0RICK-OPEN-HW-ADAPTER",
    )
