"""
Sethares Dissonance Model.

Implements William A. Sethares' psychoacoustic dissonance model based on
the work of Plomp, Levelt, and Kameoka & Kuriyagawa. The model computes
the sensory dissonance between pairs of sinusoidal components (partials)
based on their frequency separation and amplitude.

References:
    - Sethares, W.A. "Tuning, Timbre, Spectrum, Scale" (1998, 2005)
    - Plomp, R. & Levelt, W.J.M. "Tonal Consonance and Critical Bandwidth"
      J. Acoust. Soc. Am. 38, 548-560 (1965)
    - Kameoka, A. & Kuriyagawa, M. "Consonance Theory Part I & II"
      J. Acoust. Soc. Am. 45, 1451-1459 (1969)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Partial:
    """A single partial (sinusoidal component) with frequency and amplitude."""

    freq: float
    """Frequency in Hz."""

    amp: float = 1.0
    """Amplitude (linear, not dB). Defaults to 1.0."""


@dataclass
class DissonanceCurve:
    """
    Parameters for the Sethares dissonance curve.

    The default values are derived from Plomp & Levelt's experimental data
    and are parameterized in Sethares' model.
    """

    a1: float = 1.0
    """Base scaling factor."""

    a2: float = 1.0
    """Secondary scaling (typically same as a1 for normalization)."""

    b1: float = 3.5
    """Decay rate for the first exponential term (controls peak position)."""

    b2: float = 5.75
    """Decay rate for the second exponential term (controls falloff)."""

    min_separation: float = 0.0
    """Minimum frequency separation (as fraction of critical bandwidth) for dissonance."""


def dissonance_two_partial(
    f1: float,
    f2: float,
    a1: float = 1.0,
    a2: float = 1.0,
    curve: DissonanceCurve | None = None,
) -> float:
    """
    Compute the dissonance between two partials.

    Based on Sethares's implementation of the Plomp-Levelt curve, which models
    the sensory dissonance between two sine waves as a function of their
    frequency separation relative to the critical bandwidth.

    Args:
        f1: Frequency of the first partial in Hz.
        f2: Frequency of the second partial in Hz.
        a1: Amplitude of the first partial (linear).
        a2: Amplitude of the second partial (linear).
        curve: Dissonance curve parameters. Uses defaults if None.

    Returns:
        Dissonance value (higher = more dissonant).

    Example:
        >>> dissonance_two_partial(440.0, 441.0)  # Close frequencies = high dissonance
        0.03...
        >>> dissonance_two_partial(440.0, 880.0)  # Octave = low dissonance
        0.0...
    """
    if curve is None:
        curve = DissonanceCurve()

    if f1 == f2:
        return 0.0

    if f1 > f2:
        f1, f2 = f2, f1
        a1, a2 = a2, a1

    # Frequency difference
    df = f2 - f1

    # Critical bandwidth at f1 (Hartmann 1993 approximation)
    # CB(f) = 24.7 * (4.37 * f / 1000 + 1)
    cb = 24.7 * (4.37 * f1 / 1000 + 1)

    # Normalized frequency separation (in units of critical bandwidth)
    x = df / cb if cb > 0 else 0

    # Sethares/Plomp-Levelt dissonance curve:
    # D(x) = a * (exp(-b1 * x) - exp(-b2 * x))
    # This gives a curve that starts at 0, rises to a peak around x=0.25, then decays
    d = a1 * a2 * curve.a1 * (
        math.exp(-curve.b1 * x) - math.exp(-curve.b2 * x)
    )

    return max(0.0, d)


def dissonance_spectrum(
    partials: Iterable[Partial],
    curve: DissonanceCurve | None = None,
) -> float:
    """
    Compute total dissonance of a spectrum (multiple partials).

    Sums the pairwise dissonance between all partials in the spectrum.
    This models the sensory dissonance of a complex tone or chord.

    Args:
        partials: Iterable of Partial objects (freq, amp pairs).
        curve: Dissonance curve parameters. Uses defaults if None.

    Returns:
        Total dissonance of the spectrum.

    Example:
        >>> # Major triad C4-E4-G4
        >>> partials = [
        ...     Partial(261.63),  # C4
        ...     Partial(329.63),  # E4
        ...     Partial(392.00),  # G4
        ... ]
        >>> dissonance_spectrum(partials)
        0.0...
    """
    partial_list = list(partials)
    total = 0.0

    for i, p1 in enumerate(partial_list):
        for p2 in partial_list[i + 1:]:
            total += dissonance_two_partial(
                p1.freq, p2.freq, p1.amp, p2.amp, curve
            )

    return total


def dissonance_interval(
    freq1: float,
    freq2: float,
    harmonics: int = 6,
    curve: DissonanceCurve | None = None,
) -> float:
    """
    Compute dissonance of an interval between two fundamental frequencies.

    Models each fundamental as a harmonic series and computes the total
    dissonance between all partial pairs. This is the core function for
    analyzing interval consonance in musical contexts.

    Args:
        freq1: Fundamental frequency of the first tone in Hz.
        freq2: Fundamental frequency of the second tone in Hz.
        harmonics: Number of harmonics to include for each tone.
        curve: Dissonance curve parameters. Uses defaults if None.

    Returns:
        Dissonance of the interval.

    Example:
        >>> # Perfect fifth (3:2 ratio)
        >>> dissonance_interval(440.0, 660.0)
        0.0...
        >>> # Minor second (high dissonance)
        >>> dissonance_interval(440.0, 466.16)
        0.0...
    """
    if curve is None:
        curve = DissonanceCurve()

    # Generate harmonic series for each fundamental
    # Amplitudes decrease with harmonic number (1/n rolloff)
    partials: list[Partial] = []

    for n in range(1, harmonics + 1):
        partials.append(Partial(freq1 * n, 1.0 / n))
        partials.append(Partial(freq2 * n, 1.0 / n))

    return dissonance_spectrum(partials, curve)
