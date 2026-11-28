"""Unit tests for Protocol E001 DICOM TID 1500 Structured Report exporter."""

import json
from pathlib import Path
import tempfile
import unittest

from research.dicom_sr_exporter import (
    CouplingQualityGateError,
    QUSMeasurementPacket,
    build_dicom_tid1500_json,
    export_tid1500_file,
)


class TestDicomSRExporter(unittest.TestCase):
    def setUp(self) -> None:
        self.study_uid = "2.25.202641134091001"
        self.series_uid = "2.25.202641134091002"

    def test_valid_cqi_packet_exports_tid1500_json(self) -> None:
        packet = QUSMeasurementPacket(
            study_uid=self.study_uid,
            series_uid=self.series_uid,
            sos_m_s=1541.8,
            attenuation_db_cm_mhz=0.52,
            cqi_score=0.84,
            curvature_radius_mm=45.0,
        )
        sr = build_dicom_tid1500_json(packet)

        self.assertEqual(sr["00080060"]["Value"], ["SR"])
        self.assertEqual(sr["00080016"]["Value"], ["1.2.840.10008.5.1.4.1.1.88.33"])
        self.assertEqual(sr["0040A493"]["Value"], ["VERIFIED"])
        content_seq = sr["0040A730"]["Value"]
        self.assertEqual(content_seq[0]["0040A160"]["Value"], ["ACCEPTED"])
        self.assertEqual(len(content_seq), 6)

    def test_low_cqi_packet_rejected_by_default_gate(self) -> None:
        faulty_packet = QUSMeasurementPacket(
            study_uid=self.study_uid,
            series_uid=self.series_uid,
            sos_m_s=1489.0,
            attenuation_db_cm_mhz=1.18,
            cqi_score=0.22,
            curvature_radius_mm=35.0,
        )
        with self.assertRaises(CouplingQualityGateError):
            build_dicom_tid1500_json(faulty_packet)

    def test_file_export_roundtrip(self) -> None:
        packet = QUSMeasurementPacket(
            study_uid=self.study_uid,
            series_uid=self.series_uid,
            sos_m_s=1540.2,
            attenuation_db_cm_mhz=0.50,
            cqi_score=0.91,
            curvature_radius_mm=60.0,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "e001_tid1500_sr.json"
            written = export_tid1500_file(packet, out_file)
            loaded = json.loads(written.read_text(encoding="utf-8"))
            self.assertEqual(loaded["0020000D"]["Value"], [self.study_uid])


if __name__ == "__main__":
    unittest.main()
