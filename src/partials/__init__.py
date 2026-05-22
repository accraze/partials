"""
Partials — Psychoacoustic tools for working with the physical reality of sound.

Partials provides tools for analyzing partial series, timbral dissonance,
and inharmonic spectra using the Sethares dissonance model.
"""

from .combination import (
    analyze_combination_density,
    difference_tone,
    generate_combination_tones,
    ring_modulation_spectrum,
    CombinationResult,
)
from .dissonance import (
    dissonance_interval,
    dissonance_spectrum,
    dissonance_two_partial,
    DissonanceCurve,
    Partial,
)
from .inharmonicity import (
    analyze_inharmonicity,
    generate_inharmonic_series,
    harmonic_deviation_score,
    InharmonicityResult,
)
from .morph import morph_dissonance, SpectralMorph

__version__ = "0.1.0"

__all__ = [
    # Core dissonance
    "dissonance_two_partial",
    "dissonance_spectrum",
    "dissonance_interval",
    "DissonanceCurve",
    "Partial",
    # Combination tones
    "difference_tone",
    "generate_combination_tones",
    "ring_modulation_spectrum",
    "analyze_combination_density",
    "CombinationResult",
    # Morphing
    "SpectralMorph",
    "morph_dissonance",
    # Inharmonicity
    "analyze_inharmonicity",
    "generate_inharmonic_series",
    "harmonic_deviation_score",
    "InharmonicityResult",
]
