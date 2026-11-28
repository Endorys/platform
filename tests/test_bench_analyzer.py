"""Unit tests for physical oscilloscope bench CSV analyzer (#20-#22)."""

from pathlib import Path
import tempfile
import unittest

from research.bench_oscilloscope_analyzer import (
    analyze_rf_csv_trace,
    summarize_repeatability,
)


class TestBenchOscilloscopeAnalyzer(unittest.TestCase):
    def test_conformal_coupled_csv_traces_yield_low_cv(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            results = []
            for idx, peak_t in enumerate([38.9, 39.0, 39.1], start=1):
                csv_file = Path(tmpdir) / f"trial_{idx}.csv"
                lines = ["time_us,voltage_v"]
                for step in range(100):
                    t = step * 0.5
                    if step < 6:
                        v = 0.04 if step % 2 == 0 else -0.04
                    elif abs(t - peak_t) < 0.6:
                        v = 0.42
                    else:
                        v = 0.005
                    lines.append(f"{t:.2f},{v:.4f}")
                csv_file.write_text("\n".join(lines), encoding="utf-8")
                results.append(
                    analyze_rf_csv_trace(
                        csv_path=csv_file,
                        trial_id=f"T0{idx}",
                        coupling_state="CONFORMAL_COUPLED",
                    )
                )

            summary = summarize_repeatability(results)
            self.assertEqual(summary["accepted_trials"], 3)
            self.assertLess(summary["cv_percent"], 2.0)


if __name__ == "__main__":
    unittest.main()
