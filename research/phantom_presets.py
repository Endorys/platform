"""
ENDORYS Platform — Protocol E001 Standardized Phantom Presets (CIRS & QIBA PEQUS)

Provides reference acoustic impedance, Speed-of-Sound (SoS), attenuation slope,
and curved-interface geometry presets aligned with CIRS Model 040GSE and AIUM-RSNA
QIBA Pulse-Echo Quantitative Ultrasound (PEQUS) phantoms.

License: Apache-2.0 (Software) — Hardware & closed-loop CQI gating patent rights
reserved under Indian Patent Application No. 202641134091 (Patent Pending).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AcousticPhantomPreset:
    preset_id: str
    standard_ref: str
    sos_m_s: float
    attenuation_db_cm_mhz: float
    acoustic_impedance_mrayl: float
    curvature_radius_mm: float
    description: str


PHANTOM_PRESETS: dict[str, AcousticPhantomPreset] = {
    "QIBA_PEQUS_LIVER_PLANAR": AcousticPhantomPreset(
        preset_id="QIBA_PEQUS_LIVER_PLANAR",
        standard_ref="AIUM-RSNA QIBA PEQUS Reference",
        sos_m_s=1540.0,
        attenuation_db_cm_mhz=0.50,
        acoustic_impedance_mrayl=1.54,
        curvature_radius_mm=150.0,
        description="Near-planar homogeneous soft-tissue reference (0.50 dB/cm/MHz).",
    ),
    "CIRS_040GSE_CURVED_60MM": AcousticPhantomPreset(
        preset_id="CIRS_040GSE_CURVED_60MM",
        standard_ref="CIRS Model 040GSE / E001 Curved R60",
        sos_m_s=1540.0,
        attenuation_db_cm_mhz=0.70,
        acoustic_impedance_mrayl=1.54,
        curvature_radius_mm=60.0,
        description="Moderate-curvature tissue-mimicking phantom (R=60 mm, 0.70 dB/cm/MHz).",
    ),
    "E001_HIGH_CURVATURE_35MM": AcousticPhantomPreset(
        preset_id="E001_HIGH_CURVATURE_35MM",
        standard_ref="ENDORYS Protocol E001 Stress Benchmark",
        sos_m_s=1540.0,
        attenuation_db_cm_mhz=0.70,
        acoustic_impedance_mrayl=1.54,
        curvature_radius_mm=35.0,
        description="High-curvature peripheral/pediatric geometry stress profile (R=35 mm).",
    ),
}


def get_preset(preset_id: str) -> AcousticPhantomPreset:
    key = preset_id.strip().upper()
    if key not in PHANTOM_PRESETS:
        valid = ", ".join(sorted(PHANTOM_PRESETS.keys()))
        raise KeyError(f"Unknown phantom preset '{preset_id}'. Available: {valid}")
    return PHANTOM_PRESETS[key]
