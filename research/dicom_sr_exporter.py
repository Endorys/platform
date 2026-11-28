"""
ENDORYS Platform — Protocol E001 DICOM Quantitative Measurement SR (TID 1500) Exporter

Formats CQI-gated quantitative ultrasound biomarkers (Speed of Sound, Attenuation,
and Coupling Quality Index telemetry) into a DICOMweb JSON Structured Report
payload aligned with DICOM PS3.16 TID 1500 (Measurement Report) and AIUM-RSNA
QIBA Pulse-Echo Quantitative Ultrasound (PEQUS) conventions.

License: Apache-2.0 (Software) — Hardware & closed-loop CQI gating patent rights
reserved under Indian Patent Application No. 202641134091 (Patent Pending).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
import uuid


DEFAULT_CQI_THRESHOLD = 0.65


class CouplingQualityGateError(ValueError):
    """Raised when an unvalidated acquisition below CQI threshold is exported."""


@dataclass(frozen=True)
class QUSMeasurementPacket:
    """Represents a single CQI-evaluated curved-surface quantitative ultrasound frame."""

    study_uid: str
    series_uid: str
    sos_m_s: float
    attenuation_db_cm_mhz: float
    cqi_score: float
    curvature_radius_mm: float
    center_frequency_mhz: float = 1.70
    coupling_impedance_mrayl: float = 1.50
    cqi_threshold: float = DEFAULT_CQI_THRESHOLD
    operator_id: str = "E001-BENCH"
    timestamp_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S.%f")
    )

    @property
    def is_cqi_accepted(self) -> bool:
        """Returns True only when acoustic coupling meets deterministic CQI threshold."""
        return 0.0 <= self.cqi_score <= 1.0 and self.cqi_score >= self.cqi_threshold


def _coded_concept(code_value: str, scheme: str, meaning: str) -> dict[str, Any]:
    return {
        "00080100": {"vr": "SH", "Value": [code_value]},
        "00080102": {"vr": "SH", "Value": [scheme]},
        "00080104": {"vr": "LO", "Value": [meaning]},
    }


def _numeric_measurement_item(
    concept: tuple[str, str, str],
    value: float,
    unit: tuple[str, str, str],
) -> dict[str, Any]:
    return {
        "0040A010": {"vr": "CS", "Value": ["CONTAINS"]},
        "0040A040": {"vr": "CS", "Value": ["NUM"]},
        "0040A043": {"vr": "SQ", "Value": [_coded_concept(*concept)]},
        "0040A300": {
            "vr": "SQ",
            "Value": [
                {
                    "0040A30A": {"vr": "DS", "Value": [f"{value:.4f}"]},
                    "004008EA": {"vr": "SQ", "Value": [_coded_concept(*unit)]},
                }
            ],
        },
    }


def build_dicom_tid1500_json(
    packet: QUSMeasurementPacket,
    enforce_cqi_gate: bool = True,
) -> dict[str, Any]:
    """
    Constructs a DICOMweb PS3.18 JSON Representation of a TID 1500 Measurement Report.

    If enforce_cqi_gate is True (default), packets with cqi_score < cqi_threshold
    are rejected with CouplingQualityGateError to prevent corrupted biomarkers from
    propagating downstream to PACS or AI inference pipelines.
    """
    if enforce_cqi_gate and not packet.is_cqi_accepted:
        raise CouplingQualityGateError(
            f"Frame rejected by CQI gate: score={packet.cqi_score:.2f} < "
            f"threshold={packet.cqi_threshold:.2f}."
        )

    sop_instance_uid = f"2.25.{uuid.uuid4().int}"
    gate_status = "ACCEPTED" if packet.is_cqi_accepted else "REJECTED_OVERRIDE"

    measurement_items = [
        _numeric_measurement_item(
            concept=("121071", "DCM", "Speed of Sound"),
            value=packet.sos_m_s,
            unit=("m/s", "UCUM", "meters per second"),
        ),
        _numeric_measurement_item(
            concept=("E001-ATT", "99ENDORYS", "Acoustic Attenuation Coefficient"),
            value=packet.attenuation_db_cm_mhz,
            unit=("dB/(cm.MHz)", "UCUM", "decibels per centimeter megahertz"),
        ),
        _numeric_measurement_item(
            concept=("E001-CQI", "99ENDORYS", "Coupling Quality Index"),
            value=packet.cqi_score,
            unit=("1", "UCUM", "no units"),
        ),
        _numeric_measurement_item(
            concept=("E001-RAD", "99ENDORYS", "Surface Curvature Radius"),
            value=packet.curvature_radius_mm,
            unit=("mm", "UCUM", "millimeter"),
        ),
        _numeric_measurement_item(
            concept=("E001-ZAC", "99ENDORYS", "Effective Coupling Acoustic Impedance"),
            value=packet.coupling_impedance_mrayl,
            unit=("MRayl", "99ENDORYS", "megarayl"),
        ),
    ]

    return {
        "00080016": {"vr": "UI", "Value": ["1.2.840.10008.5.1.4.1.1.88.33"]},
        "00080018": {"vr": "UI", "Value": [sop_instance_uid]},
        "00080023": {"vr": "DA", "Value": [packet.timestamp_utc[:8]]},
        "00080033": {"vr": "TM", "Value": [packet.timestamp_utc[8:]]},
        "00080060": {"vr": "CS", "Value": ["SR"]},
        "00080070": {"vr": "LO", "Value": ["M/s Endorys (Protocol E001)"]},
        "0020000D": {"vr": "UI", "Value": [packet.study_uid]},
        "0020000E": {"vr": "UI", "Value": [packet.series_uid]},
        "0040A040": {"vr": "CS", "Value": ["CONTAINER"]},
        "0040A043": {
            "vr": "SQ",
            "Value": [_coded_concept("126000", "DCM", "Imaging Measurement Report")],
        },
        "0040A491": {"vr": "CS", "Value": ["COMPLETE"]},
        "0040A493": {"vr": "CS", "Value": ["VERIFIED" if packet.is_cqi_accepted else "UNVERIFIED"]},
        "0040A504": {
            "vr": "SQ",
            "Value": [
                {
                    "0040DB00": {"vr": "CS", "Value": ["TID 1500"]},
                    "0040DB0D": {"vr": "UI", "Value": ["1.2.840.10008.8.1.1"]},
                }
            ],
        },
        "0040A730": {
            "vr": "SQ",
            "Value": [
                {
                    "0040A010": {"vr": "CS", "Value": ["CONTAINS"]},
                    "0040A040": {"vr": "CS", "Value": ["TEXT"]},
                    "0040A043": {
                        "vr": "SQ",
                        "Value": [
                            _coded_concept("E001-GATE", "99ENDORYS", "CQI Acquisition Gate Status")
                        ],
                    },
                    "0040A160": {"vr": "UT", "Value": [gate_status]},
                },
                *measurement_items,
            ],
        },
    }


def export_tid1500_file(
    packet: QUSMeasurementPacket,
    output_path: str | Path,
    enforce_cqi_gate: bool = True,
) -> Path:
    """Validates CQI gating and writes the TID 1500 DICOMweb JSON payload to disk."""
    payload = build_dicom_tid1500_json(packet, enforce_cqi_gate=enforce_cqi_gate)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target


if __name__ == "__main__":
    sample = QUSMeasurementPacket(
        study_uid="2.25.100000000000000000000000000001",
        series_uid="2.25.100000000000000000000000000002",
        sos_m_s=1542.4,
        attenuation_db_cm_mhz=0.54,
        cqi_score=0.84,
        curvature_radius_mm=45.0,
    )
    print(json.dumps(build_dicom_tid1500_json(sample), indent=2))
