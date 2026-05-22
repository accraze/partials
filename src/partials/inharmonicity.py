"""
Inharmonicity analysis tools.

Provides methods for quantifying how far a spectrum deviates from
a perfect harmonic series, including B-factor analysis for piano-like
inharmonicity and general inharmonicity metrics.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from .dissonance import Partial


@dataclass
class InharmonicityResult:
    """Results of inharmonicity analysis."""

    b_factor: float
    """B-factor: inharmonicity coefficient (0 = perfectly harmonic)."""

    rms_deviation: float
    """RMS deviation from harmonic series (in cents)."""

    harmonic_partial_count: int
    """Number of partials successfully matched to harmonics."""

    total_partials: int
    """Total number of partials analyzed."""

    inharmonicity_ratio: float
    """Ratio of inharmonic energy to total energy."""


def analyze_inharmonicity(
    partials: Iterable[Partial],
    fundamental: float | None = None,
    max_harmonic: int = 12,
) -> InharmonicityResult:
    """
    Analyze how inharmonic a spectrum is.

    Computes the B-factor (inharmonicity coefficient) by fitting partial
    frequencies to a harmonic series with inharmonicity:

    f_n = f_0 * n * sqrt(1 + B * n^2)

    Where:
        - f_n is the frequency of the nth partial
        - f_0 is the fundamental frequency
        - B is the inharmonicity coefficient

    Args:
        partials: List of partials to analyze.
        fundamental: Known fundamental frequency. If None, uses the lowest
                     frequency as an estimate.
        max_harmonic: Maximum harmonic number to consider.

    Returns:
        InharmonicityResult with B-factor and related metrics.

    Example:
        >>> # Piano-like inharmonicity
        >>> partials = [
        ...     Partial(27.5),
        ...     Partial(55.1),  # Slightly sharp
        ...     Partial(82.8),  # More sharp
        ... ]
        >>> result = analyze_inharmonicity(partials)
        >>> result.b_factor
        0.0...
    """
    partial_list = list(partials)

    if not partial_list:
        return InharmonicityResult(0.0, 0.0, 0, 0, 0.0)

    # Estimate fundamental if not provided
    if fundamental is None:
        fundamental = min(p.freq for p in partial_list)

    # Sort partials by frequency
    sorted_partials = sorted(partial_list, key=lambda p: p.freq)

    # Fit B-factor using least squares
    b_sum = 0.0
    count = 0
    deviations = []
    inharmonic_energy = 0.0
    total_energy = 0.0

    for i, partial in enumerate(sorted_partials):
        if i >= max_harmonic:
            break

        n = i + 1  # Harmonic number (1-indexed)
        expected_harmonic = fundamental * n
        actual_freq = partial.freq

        # Calculate deviation from perfect harmonic
        deviation_cents = 1200 * math.log2(actual_freq / expected_harmonic)
        deviations.append(deviation_cents)

        # Estimate B from this partial: f_n ≈ f_0 * n * (1 + B * n^2 / 2)
        # B ≈ 2 * ((f_n / (f_0 * n)) - 1) / n^2
        if n > 0 and expected_harmonic > 0:
            ratio = actual_freq / expected_harmonic
            b_estimate = 2 * (ratio - 1) / (n * n)
            if b_estimate > 0:  # Only count positive inharmonicity
                b_sum += b_estimate
                count += 1

        # Track energy
        total_energy += partial.amp ** 2
        if abs(deviation_cents) > 10:  # More than 10 cents = inharmonic
            inharmonic_energy += partial.amp ** 2

    # Compute results
    b_factor = b_sum / count if count > 0 else 0.0
    rms_dev = math.sqrt(sum(d * d for d in deviations) / len(deviations)) if deviations else 0.0
    inharmonicity_ratio = inharmonic_energy / total_energy if total_energy > 0 else 0.0

    return InharmonicityResult(
        b_factor=b_factor,
        rms_deviation=rms_dev,
        harmonic_partial_count=count,
        total_partials=len(sorted_partials),
        inharmonicity_ratio=inharmonicity_ratio,
    )


def harmonic_deviation_score(
    partials: Iterable[Partial],
    fundamental: float | None = None,
) -> float:
    """
    Compute a single score for how much a spectrum deviates from harmonic.

    Higher scores indicate more deviation (less harmonic).
    Score is in cents RMS deviation from perfect harmonic series.

    Args:
        partials: List of partials to analyze.
        fundamental: Known fundamental frequency.

    Returns:
        Deviation score in cents (0 = perfectly harmonic).
    """
    result = analyze_inharmonicity(partials, fundamental)
    return result.rms_deviation


def generate_inharmonic_series(
    fundamental: float,
    num_partials: int = 12,
    b_factor: float = 0.001,
) -> list[Partial]:
    """
    Generate an inharmonic series with specified B-factor.

    Uses the formula: f_n = f_0 * n * sqrt(1 + B * n^2)

    Args:
        fundamental: Fundamental frequency (f_0).
        num_partials: Number of partials to generate.
        b_factor: Inharmonicity coefficient (0 = harmonic, >0 = inharmonic).

    Returns:
        List of Partials with inharmonic frequencies.

    Example:
        >>> # Generate piano-like inharmonicity (B ≈ 0.001)
        >>> partials = generate_inharmonic_series(220.0, 12, 0.001)
    """
    partials = []
    for n in range(1, num_partials + 1):
        freq = fundamental * n * math.sqrt(1 + b_factor * n * n)
        # Amplitude decreases with harmonic number
        amp = 1.0 / n
        partials.append(Partial(freq, amp))
    return partials
