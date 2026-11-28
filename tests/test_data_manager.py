"""Unit tests for autonomous Data Manager auto-validation & routing engine (#68B)."""

import unittest

from research.data_manager_engine import WorklistOrder, evaluate_and_route_study
from research.dicom_sr_exporter import QUSMeasurementPacket


class TestDataManagerEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.order = WorklistOrder(
            accession_number="ACC-2026-E001-01",
            patient_or_phantom_id="PHANTOM-R60-01",
            operator_id="SADHU-BENCH",
        )

    def test_high_cqi_auto_releases_to_pacs(self) -> None:
        pkt = QUSMeasurementPacket(
            study_uid="2.25.501",
            series_uid="2.25.502",
            sos_m_s=1541.2,
            attenuation_db_cm_mhz=0.53,
            cqi_score=0.88,
            curvature_radius_mm=60.0,
        )
        res = evaluate_and_route_study(self.order, pkt)
        self.assertEqual(res.disposition, "AUTO_RELEASED")
        self.assertIsNotNone(res.dicom_sr_payload)
        self.assertEqual(len(res.audit_sha256), 64)

    def test_borderline_cqi_routes_to_supervisor_review(self) -> None:
        pkt = QUSMeasurementPacket(
            study_uid="2.25.503",
            series_uid="2.25.504",
            sos_m_s=1538.5,
            attenuation_db_cm_mhz=0.56,
            cqi_score=0.72,
            curvature_radius_mm=45.0,
        )
        res = evaluate_and_route_study(self.order, pkt)
        self.assertEqual(res.disposition, "SUPERVISOR_REVIEW")
        self.assertIsNotNone(res.dicom_sr_payload)

    def test_low_cqi_quarantines_and_blocks_sr_export(self) -> None:
        pkt = QUSMeasurementPacket(
            study_uid="2.25.505",
            series_uid="2.25.506",
            sos_m_s=1492.0,
            attenuation_db_cm_mhz=1.10,
            cqi_score=0.31,
            curvature_radius_mm=35.0,
        )
        res = evaluate_and_route_study(self.order, pkt)
        self.assertEqual(res.disposition, "QUARANTINED_RESCAN")
        self.assertIsNone(res.dicom_sr_payload)


if __name__ == "__main__":
    unittest.main()
