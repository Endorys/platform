# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Sadhu Shobab Bollipo
"""One-command synthetic demonstration; never runs hardware."""
import argparse
import html
import json
from pathlib import Path

import e001
from e001_generate_demo import generate


def demo(output):
    output=Path(output)
    inputs=generate(output/"synthetic_inputs")
    config=inputs/"e001_demo_config.json"
    results=[]
    for name in ("reference","changed","reduced","disconnected","clipped","ambiguous","operator_rejected"):
        results.append(e001.run(inputs/("e001_"+name+".json"),config,output/"analysis"))
    (output/"summary.json").write_text(json.dumps(results,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    rows=[]
    for r in results:
        speed="withheld" if r["apparent_speed_m_per_s"] is None else f"{r['apparent_speed_m_per_s']:.2f}"
        rows.append(f"<tr><td>{html.escape(r['run_id'])}</td><td>{r['quality']}</td><td>{speed}</td><td>{html.escape(', '.join(r['rejection_reasons']))}</td><td><a href='analysis/{r['run_id']}_waveform.svg'>waveform</a></td></tr>")
    page="""<!doctype html><html lang="en"><meta charset="utf-8"><title>Endorys E001 synthetic demonstration</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px;color:#153044}table{border-collapse:collapse;width:100%}td,th{padding:12px;border:1px solid #b7c7d1;text-align:left}.notice{background:#fff1c9;padding:18px}</style><h1>Endorys E001 — synthetic demonstration</h1><p class="notice">Toy data only. No hardware, phantom, tissue or clinical performance was measured. These are software workflow checks, not physics simulations.</p><p>The estimator finds an absolute peak in a configured window. Apparent speed and partial uncertainty are illustrative; they are not validated sound-speed or elasticity measurements.</p><table><tr><th>Condition</th><th>Quality</th><th>Toy apparent speed (m/s)</th><th>Reasons</th><th>Plot</th></tr>"""+"".join(rows)+"</table><p>Each JSON output retains data origin, input checksum, configuration hash and uncertainty limitations. The deliberately incomplete example fails validation. No pooled clinical statistics are produced.</p></html>"
    (output/"index.html").write_text(page,encoding="utf-8")
    return results


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",required=True)
    results=demo(parser.parse_args().out)
    print(f"Synthetic demo complete: {sum(r['quality']=='accepted' for r in results)} accepted toy traces; {sum(r['quality']=='rejected' for r in results)} rejected. No physical validation.")
