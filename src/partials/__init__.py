"""
Partials — Psychoacoustic tools for working with the physical reality of sound.

Partials provides tools for analyzing partial series, timbral dissonance,
and inharmonic spectra using the Sethares dissonance model.
"""

from .dissonance import (
    dissonance_two_partial,
    dissonance_spectrum,
    dissonance_interval,
    DissonanceCurve,
    Partial,
)

__version__ = "0.1.0"
__all__ = [
    "dissonance_two_partial",
    "dissonance_spectrum",
    "dissonance_interval",
    "DissonanceCurve",
    "Partial",
]
