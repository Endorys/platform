# Protocol E001 — 3D-Printable Curved Phantom & Probe Cradle Fixtures

Open-hardware reference CAD fixtures for evaluating curved-surface acoustic coupling repeatability and **Coupling Quality Index (CQI)** gating under **Protocol E001** (`Zenodo DOI: 10.5281/zenodo.24555614`).

## Included Parametric Geometry (`endorys_curved_phantom.scad`)
* **Curved Tissue-Mimicking Phantom Mold (`R = 35 mm, 60 mm, 90 mm`):** Casts repeatable cylindrical surface profiles with orthogonal `0.5 mm` nylon monofilament ports at `20 mm` and `40 mm` acoustic depth for Speed-of-Sound (`SoS`) time-of-flight calibration.
* **6-Element Conformal Alignment Cradle:** Holds a 6-element `1.7 MHz` linear/living-hinge array over a `3.0 mm` impedance-matched coupling ribbon (`~1.50 MRayl`) at fixed angular pitch.

## Recommended 3D Printing & Phantom Casting Specs
1. **Material:** PETG or PLA (`0.20 mm` layer height, `20%` gyroid infill, watertight perimeter walls `>= 3`).
2. **Tissue-Mimicking Phantom Fill (`~1540 m/s`, `~1.50 MRayl`):**
   * Degassed distilled water (`91.5% w/w`) + food-grade porcine/bovine gelatin (`5.5% w/w`, 250 Bloom) + 1-propanol (`3.0% w/w` for `1540 m/s` SoS tuning).
   * Thread `0.5 mm` monofilament lines through the `20 mm` and `40 mm` ports before pouring, seal ends with silicone, and cure at `4 °C` for `12 hours`.
3. **Exporting STL Files:** Open `endorys_curved_phantom.scad` in OpenSCAD, set `radius_mm` (`35`, `60`, or `90`), press `F6` (Render), and export `.stl`.

## Licensing & Intellectual Property Notice
* **Reference Fixtures (`CC-BY-4.0`):** Free for academic, metrology, and non-commercial research benchmarking.
* **Patent Reservation:** Commercial hardware embodiments and closed-loop CQI frame-gating architectures are covered by Indian Patent Application No. `202641134091` (Patent Pending, M/s Endorys).
