"""
Combination tone calculator for sum and difference frequencies.

When two or more frequencies interact (in the ear, analog circuits, or
nonlinear systems), they produce sum and difference frequencies:
- f1 - f2 (difference tone, often most audible)
- f1 + f2 (sum tone)
- 2f1 - f2, 2f2 - f1 (higher-order combination tones)

This module recursively generates these emergent frequencies, creating
"pitch clouds" useful for ring modulation design and drone analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .dissonance import Partial


@dataclass
class CombinationResult:
    """Results of combination tone analysis."""

    original_partials: list[Partial]
    """Original input partials."""

    combination_partials: list[Partial]
    """Generated combination tones (sum/difference)."""

    all_partials: list[Partial]
    """Combined original and combination tones."""

    max_order: int
    """Maximum recursion order reached."""

    total_generated: int
    """Total number of combination tones generated."""


def generate_combination_tones(
    partials: Iterable[Partial],
    max_order: int = 2,
    amplitude_decay: float = 0.5,
    min_amplitude: float = 0.001,
    min_frequency: float = 20.0,
    max_frequency: float = 20000.0,
) -> CombinationResult:
    """
    Generate combination tones from interacting frequencies.

    Recursively computes sum and difference tones up to the specified order.
    For frequencies f1 and f2, generates:
    - Order 1: f1 ± f2
    - Order 2: f1 ± f2 ± f3, 2f1 ± f2, etc.
    - Higher orders: increasingly complex combinations

    Args:
        partials: Input partials (frequencies with amplitudes).
        max_order: Maximum recursion order (1 = simple, 3+ = complex clouds).
        amplitude_decay: Amplitude reduction per order (e.g., 0.5 = -6dB/order).
        min_amplitude: Minimum amplitude threshold (filters quiet tones).
        min_frequency: Minimum frequency to include (Hz).
        max_frequency: Maximum frequency to include (Hz).

    Returns:
        CombinationResult with all generated tones.

    Example:
        >>> # Simple difference tone (Tartini tone)
        >>> partials = [Partial(1000), Partial(1200)]
        >>> result = generate_combination_tones(partials, max_order=1)
        >>> # Will include 200 Hz difference tone
    """
    partial_list = list(partials)

    if not partial_list:
        return CombinationResult(
            original_partials=[],
            combination_partials=[],
            all_partials=[],
            max_order=0,
            total_generated=0,
        )

    # Track all generated partials (use frequency as key to avoid duplicates)
    all_freqs: dict[float, Partial] = {p.freq: p for p in partial_list}
    new_partials: list[Partial] = list(partial_list)
    combination_partials: list[Partial] = []

    for order in range(1, max_order + 1):
        if not new_partials:
            break

        next_order_partials: list[Partial] = []
        current_amplitude = amplitude_decay ** order

        # Generate combinations between original and all existing partials
        for p1 in partial_list:
            for p2 in new_partials:
                # Difference tone (most important)
                diff_freq = abs(p1.freq - p2.freq)
                if diff_freq > 0:
                    _add_partial(
                        diff_freq,
                        p1.amp * p2.amp * current_amplitude,
                        all_freqs,
                        next_order_partials,
                        min_amplitude,
                        min_frequency,
                        max_frequency,
                    )

                # Sum tone
                sum_freq = p1.freq + p2.freq
                _add_partial(
                    sum_freq,
                    p1.amp * p2.amp * current_amplitude,
                    all_freqs,
                    next_order_partials,
                    min_amplitude,
                    min_frequency,
                    max_frequency,
                )

        new_partials = next_order_partials
        combination_partials.extend(new_partials)

    # Sort by frequency
    all_partials = sorted(all_freqs.values(), key=lambda p: p.freq)
    combination_partials = sorted(combination_partials, key=lambda p: p.freq)

    return CombinationResult(
        original_partials=partial_list,
        combination_partials=combination_partials,
        all_partials=all_partials,
        max_order=max_order,
        total_generated=len(combination_partials),
    )


def _add_partial(
    freq: float,
    amp: float,
    all_freqs: dict[float, Partial],
    next_order_partials: list[Partial],
    min_amplitude: float,
    min_frequency: float,
    max_frequency: float,
) -> None:
    """Add a partial if it meets criteria."""
    if amp < min_amplitude:
        return
    if freq < min_frequency or freq > max_frequency:
        return
    if freq in all_freqs:
        # Add amplitudes if same frequency already exists
        existing = all_freqs[freq]
        all_freqs[freq] = Partial(freq, existing.amp + amp)
    else:
        new_partial = Partial(freq, amp)
        all_freqs[freq] = new_partial
        next_order_partials.append(new_partial)


def difference_tone(f1: float, f2: float) -> float:
    """
    Calculate the primary difference tone (f2 - f1).

    This is the most audible combination tone, also called the Tartini tone.

    Args:
        f1: First frequency (Hz).
        f2: Second frequency (Hz).

    Returns:
        Difference frequency (always positive).

    Example:
        >>> difference_tone(1000, 1200)
        200.0
    """
    return abs(f2 - f1)


def analyze_combination_density(
    partials: Iterable[Partial],
    max_order: int = 2,
    bins: int = 100,
    frequency_range: tuple[float, float] | None = None,
) -> list[tuple[float, float]]:
    """
    Analyze the density of combination tones across frequency spectrum.

    Useful for visualizing where combination tones cluster.

    Args:
        partials: Input partials.
        max_order: Maximum combination order.
        bins: Number of frequency bins.
        frequency_range: (min_freq, max_freq) tuple. Auto-detected if None.

    Returns:
        List of (center_freq, density) tuples.
    """
    result = generate_combination_tones(partials, max_order=max_order)

    if not result.all_partials:
        return []

    if frequency_range is None:
        freqs = [p.freq for p in result.all_partials]
        min_freq = min(freqs)
        max_freq = max(freqs)
    else:
        min_freq, max_freq = frequency_range

    if min_freq == max_freq:
        return [(min_freq, 0.0)]

    bin_width = (max_freq - min_freq) / bins
    density = [0.0] * bins

    for partial in result.all_partials:
        bin_idx = min(int((partial.freq - min_freq) / bin_width), bins - 1)
        density[bin_idx] += partial.amp

    # Normalize
    max_density = max(density) if density else 1.0
    if max_density > 0:
        density = [d / max_density for d in density]

    centers = [min_freq + (i + 0.5) * bin_width for i in range(bins)]
    return list(zip(centers, density))


def ring_modulation_spectrum(
    carrier: float,
    modulator: float,
    harmonics: int = 6,
    include_original: bool = True,
) -> list[Partial]:
    """
    Generate the spectrum of a ring modulator.

    Ring modulation produces sum and difference frequencies:
    output = carrier × modulator → (carrier ± modulator)

    Args:
        carrier: Carrier frequency (Hz).
        modulator: Modulator frequency (Hz).
        harmonics: Number of harmonics to consider for each.
        include_original: Include original carrier and modulator.

    Returns:
        List of Partials representing the output spectrum.

    Example:
        >>> # Classic ring mod: 1000 Hz carrier, 200 Hz modulator
        >>> spectrum = ring_modulation_spectrum(1000, 200)
        >>> # Produces: 800 Hz, 1200 Hz, and harmonics
    """
    partials: list[Partial] = []

    if include_original:
        partials.append(Partial(carrier, 0.5))
        partials.append(Partial(modulator, 0.5))

    # Generate harmonics
    for n in range(1, harmonics + 1):
        carrier_harm = carrier * n
        mod_harm = modulator * n

        # Sum frequencies
        sum_freq = carrier_harm + mod_harm
        partials.append(Partial(sum_freq, 1.0 / n))

        # Difference frequencies
        diff_freq = abs(carrier_harm - mod_harm)
        if diff_freq > 0:
            partials.append(Partial(diff_freq, 1.0 / n))

    # Sort by frequency
    partials.sort(key=lambda p: p.freq)
    return partials
