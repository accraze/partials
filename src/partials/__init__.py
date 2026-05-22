"""
Partials — Psychoacoustic tools for working with the physical reality of sound.

Partials provides tools for analyzing partial series, timbral dissonance,
and inharmonic spectra using the Sethares dissonance model.
"""

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
    # Morphing
    "SpectralMorph",
    "morph_dissonance",
    # Inharmonicity
    "analyze_inharmonicity",
    "generate_inharmonic_series",
    "harmonic_deviation_score",
    "InharmonicityResult",
]
