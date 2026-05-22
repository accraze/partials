"""
Visualization tools for spectral analysis.

Provides text-based and plot-ready visualizations for:
- Dissonance curves
- Spectrum analysis
- Inharmonicity visualization
- Morphing trajectories
"""

from __future__ import annotations

from typing import Callable, Iterable

from .dissonance import Partial, dissonance_interval, dissonance_spectrum


def plot_dissonance_curve(
    fundamental: float = 440.0,
    max_ratio: float = 2.0,
    steps: int = 100,
    width: int = 60,
    height: int = 20,
) -> str:
    """
    Generate ASCII art dissonance curve.

    Shows how dissonance varies as a function of frequency ratio.

    Args:
        fundamental: Base frequency.
        max_ratio: Maximum frequency ratio (2.0 = octave).
        steps: Number of steps to evaluate.
        width: Character width of output.
        height: Character height of output.

    Returns:
        ASCII art string of the dissonance curve.

    Example:
        >>> print(plot_dissonance_curve(440.0, max_ratio=2.0))
    """
    # Sample the dissonance curve
    ratios = [1.0 + (max_ratio - 1.0) * i / steps for i in range(steps + 1)]
    dissonances = [dissonance_interval(fundamental, fundamental * r) for r in ratios]

    # Normalize
    max_d = max(dissonances) if dissonances else 1.0
    if max_d > 0:
        dissonances = [d / max_d for d in dissonances]

    # Create ASCII plot
    lines = []
    for row in range(height):
        line = "|"
        threshold = 1.0 - (row + 0.5) / height
        for i, d in enumerate(dissonances):
            col_steps = steps + 1
            if d >= threshold:
                line += "█" * (width // col_steps + 1)
            else:
                line += " " * (width // col_steps + 1)
        lines.append(line[:width])

    # Add x-axis
    lines.append("+" + "-" * width)

    # Add labels
    lines.append(f" 1.0{' ' * (width // 2 - 4)}ratio{' ' * (width // 2 - 4)}{max_ratio:.1f}")

    return "\n".join(lines)


def spectrum_text(
    partials: Iterable[Partial],
    max_freq: float | None = None,
    width: int = 80,
) -> str:
    """
    Generate ASCII visualization of a spectrum.

    Args:
        partials: List of partials to visualize.
        max_freq: Maximum frequency to display. Auto-detected if None.
        width: Character width.

    Returns:
        ASCII spectrum visualization.

    Example:
        >>> partials = [Partial(440, 1.0), Partial(880, 0.5)]
        >>> print(spectrum_text(partials))
    """
    partial_list = sorted(list(partials), key=lambda p: p.freq)

    if not partial_list:
        return "No partials"

    if max_freq is None:
        max_freq = max(p.freq for p in partial_list)

    # Build frequency bins
    bins = [0.0] * width
    bin_width = max_freq / width if max_freq > 0 else 1.0

    for partial in partial_list:
        bin_idx = min(int(partial.freq / bin_width), width - 1)
        bins[bin_idx] = max(bins[bin_idx], partial.amp)

    # Normalize amplitudes
    max_amp = max(bins) if bins else 1.0
    if max_amp > 0:
        bins = [b / max_amp for b in bins]

    # Create visualization
    max_height = 10
    lines = []
    for row in range(max_height, 0, -1):
        threshold = row / max_height
        line = "|"
        for amp in bins:
            if amp >= threshold:
                line += "█"
            else:
                line += " "
        lines.append(line)

    # Add x-axis
    lines.append("+" + "-" * width)

    # Add labels
    lines.append(f" 0 Hz{' ' * (width - 20)}{max_freq:.0f} Hz")

    return "\n".join(lines)


def morph_trajectory(
    source: list[Partial],
    target: list[Partial],
    steps: int = 10,
) -> str:
    """
    Visualize a spectral morph as text.

    Shows dissonance at each step of the morph.

    Args:
        source: Source spectrum.
        target: Target spectrum.
        steps: Number of steps.

    Returns:
        Text visualization of the morph trajectory.
    """
    from .morph import SpectralMorph

    morph = SpectralMorph(source, target, steps)
    lines = ["Spectral Morph Trajectory", "=" * 40]

    for i, partials in enumerate(morph.interpolate()):
        d = dissonance_spectrum(partials)
        bar_len = int(d * 50)
        bar = "█" * bar_len
        t = i / steps if steps > 0 else 1.0
        lines.append(f"t={t:.2f}: {bar} ({d:.4f})")

    return "\n".join(lines)


def compare_spectra(
    spectra: list[tuple[str, list[Partial]]],
    width: int = 60,
) -> str:
    """
    Compare multiple spectra side by side.

    Args:
        spectra: List of (name, partials) tuples.
        width: Width per spectrum.

    Returns:
        Side-by-side ASCII comparison.
    """
    lines = ["Spectrum Comparison", "=" * 60]

    for name, partials in spectra:
        lines.append(f"\n{name}:")
        lines.append(spectrum_text(partials, width=min(width, 40)))
        d = dissonance_spectrum(partials)
        lines.append(f"Dissonance: {d:.4f}")

    return "\n".join(lines)
