"""
Package initialization for chiplet multi-physics reliability engine.
Exposes core physics functions directly under `src.engine`.
"""

from .physics import (
    # Electromigration
    compute_joule_heating,
    compute_blacks_mttf,
    # Thermo-Mechanical Stress
    compute_plastic_shear_strain,
    compute_coffin_manson_cycles,
    # Signal Integrity
    compute_interconnect_parasitics,
    compute_50_percent_rc_delay,
)
from .signal_integrity import (
    generate_prbs_signal,
    apply_channel_filter,
    extract_eye_metrics,
)

__all__ = [
    "compute_joule_heating",
    "compute_blacks_mttf",
    "compute_plastic_shear_strain",
    "compute_coffin_manson_cycles",
    "compute_interconnect_parasitics",
    "compute_50_percent_rc_delay",
    "generate_prbs_signal",
    "apply_channel_filter",
    "extract_eye_metrics",
]
