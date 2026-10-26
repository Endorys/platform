# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Sadhu Shobab Bollipo
"""Synthetic illustration only. No hardware, tissue or diagnostic validation."""
import csv, json, math, random
from pathlib import Path


def main():
    rng = random.Random(20261026)
    output = Path('synthetic_output')
    output.mkdir(exist_ok=True)
    summary = []
    for name, speed, coupling in [('reference', 1500.0, 1.0), ('changed', 1560.0, 1.0), ('reduced_coupling', 1500.0, 0.5), ('disconnected', 1500.0, 0.0)]:
        expected = 0.04 / speed
        samples = []
        for i in range(601):
            time = i * 1e-7
            value = coupling * math.exp(-0.5 * ((time-expected)/4e-7)**2) + rng.uniform(-0.002, 0.002)
            samples.append((time, value))
        peak_time, peak = max(samples, key=lambda row: row[1])
        valid = peak > 0.1
        # Threshold is chosen for this toy generator only.
        if coupling:
            assert valid and abs(peak_time-expected) <= 1.1e-7
        else:
            assert not valid
        with (output / (name + '.csv')).open('w', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['time_s', 'synthetic_amplitude'])
            writer.writerows(samples)
        summary.append(dict(condition=name, data_origin='synthetic', expected_transit_s=expected, peak_time_s=peak_time if valid else None, quality='toy_signal_present' if valid else 'toy_signal_absent'))
    (output/'summary.json').write_text(json.dumps(summary, indent=2))
    print('Four synthetic conditions generated; timing and absent-signal checks passed. No physical validation.')

if __name__ == '__main__':
    main()
