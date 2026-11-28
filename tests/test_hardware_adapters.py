"""Unit tests for Verasonics & un0rick hardware acquisition adapters (#9)."""

import unittest

from research.adapters.verasonics_un0rick_adapter import (
    ingest_un0rick_adc_buffer,
    ingest_verasonics_rf_frame,
)


class TestHardwareAdapters(unittest.TestCase):
    def test_verasonics_well_coupled_frame_passes_cqi(self) -> None:
        # Low boundary reflection (0.05 V), strong bulk echo (0.45 V)
        rf = [0.05, -0.04, 0.03, -0.02] + [0.01] * 40 + [0.45, -0.42, 0.20] + [0.01] * 53
        pkt = ingest_verasonics_rf_frame(
            rf_samples_v=rf,
            sampling_rate_hz=25e6,
            study_uid="2.25.1001",
            series_uid="2.25.1002",
            curvature_radius_mm=60.0,
        )
        self.assertTrue(pkt.is_cqi_accepted)
        self.assertGreaterEqual(pkt.cqi_score, 0.85)

    def test_un0rick_air_gap_frame_rejected_by_cqi(self) -> None:
        # Strong boundary reflection (counts near 950 -> ~0.85 V), weak bulk echo (counts near 540 -> ~0.05 V)
        adc = [950, 100, 900, 120] + [512] * 40 + [540, 490] + [512] * 54
        pkt = ingest_un0rick_adc_buffer(adc_counts=adc, curvature_radius_mm=35.0)
        self.assertFalse(pkt.is_cqi_accepted)
        self.assertLess(pkt.cqi_score, 0.30)


if __name__ == "__main__":
    unittest.main()
