"""
ENDORYS Platform — Automated Quality Gating & Enterprise Data Manager Engine (Task #68B)

Implements an autonomous diagnostic workflow rule engine that pairs DICOM
Modality Worklist (MWL) accession orders with CQI-gated quantitative ultrasound
acquisitions, automatically releasing high-confidence scans (CQI >= 0.80) to
PACS/LIS, flagging borderline scans (0.65 <= CQI < 0.80), quarantining poor
coupling frames (CQI < 0.65), and emitting SHA-256 audit trail records.

License: Apache-2.0 (Software) — Hardware & closed-loop CQI gating patent rights
reserved under Indian Patent Application No. 202641134091 (Patent Pending).
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

from research.dicom_sr_exporter import (
    QUSMeasurementPacket,
    build_dicom_tid1500_json,
)


@dataclass(frozen=True)
class WorklistOrder:
    accession_number: str
    patient_or_phantom_id: str
    operator_id: str
    protocol_code: str = "E001-QUS-CURVED"


@dataclass(frozen=True)
class DataManagerDisposition:
    accession_number: str
    disposition: str  # AUTO_RELEASED | SUPERVISOR_REVIEW | QUARANTINED_RESCAN
    cqi_score: float
    action_message: str
    audit_sha256: str
    dicom_sr_payload: dict[str, Any] | None


def evaluate_and_route_study(
    order: WorklistOrder,
    packet: QUSMeasurementPacket,
    auto_release_threshold: float = 0.80,
) -> DataManagerDisposition:
    """Applies deterministic CQI auto-validation rules and generates an audit digest."""
    if packet.cqi_score < packet.cqi_threshold:
        disposition = "QUARANTINED_RESCAN"
        action = (
            f"BLOCKED FROM PACS/LIS: CQI={packet.cqi_score:.2f} < {packet.cqi_threshold:.2f}. "
            "Re-seat conformal array / verify ~1.50 MRayl coupling interface and rescan."
        )
        sr_payload = None
    elif packet.cqi_score < auto_release_threshold:
        disposition = "SUPERVISOR_REVIEW"
        action = (
            f"HELD FOR REVIEW: Borderline CQI={packet.cqi_score:.2f} "
            f"(between {packet.cqi_threshold:.2f} and {auto_release_threshold:.2f})."
        )
        sr_payload = build_dicom_tid1500_json(packet, enforce_cqi_gate=True)
    else:
        disposition = "AUTO_RELEASED"
        action = (
            f"AUTO-VALIDATED & ROUTED TO PACS/LIS: CQI={packet.cqi_score:.2f} >= "
            f"{auto_release_threshold:.2f} (SoS={packet.sos_m_s:.1f} m/s)."
        )
        sr_payload = build_dicom_tid1500_json(packet, enforce_cqi_gate=True)

    audit_canonical = json.dumps(
        {
            "accession": order.accession_number,
            "subject_id": order.patient_or_phantom_id,
            "operator_id": order.operator_id,
            "study_uid": packet.study_uid,
            "series_uid": packet.series_uid,
            "cqi_score": packet.cqi_score,
            "sos_m_s": packet.sos_m_s,
            "disposition": disposition,
            "timestamp_utc": packet.timestamp_utc,
        },
        sort_keys=True,
    )
    audit_hash = hashlib.sha256(audit_canonical.encode("utf-8")).hexdigest()

    return DataManagerDisposition(
        accession_number=order.accession_number,
        disposition=disposition,
        cqi_score=packet.cqi_score,
        action_message=action,
        audit_sha256=audit_hash,
        dicom_sr_payload=sr_payload,
    )
