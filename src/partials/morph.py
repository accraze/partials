"""
Spectral morphing tools for transforming between timbres.

Provides interpolation methods for smoothly transitioning between
different spectral configurations while preserving psychoacoustic properties.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from .dissonance import Partial


@dataclass
class SpectralMorph:
    """
    Morph between two spectra over interpolated steps.

    Example:
        >>> source = [Partial(440, 1.0), Partial(880, 0.5)]
        >>> target = [Partial(440, 0.5), Partial(660, 1.0)]
        >>> morph = SpectralMorph(source, target, steps=10)
        >>> for step in morph.interpolate():
        ...     print(step)
    """

    source: list[Partial]
    """Source spectrum (starting point)."""

    target: list[Partial]
    """Target spectrum (ending point)."""

    steps: int = 10
    """Number of interpolation steps."""

    method: str = "linear"
    """Interpolation method: 'linear' or 'logarithmic'."""

    def interpolate(self) -> Iterator[list[Partial]]:
        """
        Generate intermediate spectra between source and target.

        Yields:
            List of Partials at each interpolation step.
        """
        for i in range(self.steps + 1):
            t = i / self.steps if self.steps > 0 else 1.0
            yield self._interpolate_spectrum(t)

    def _interpolate_spectrum(self, t: float) -> list[Partial]:
        """Interpolate to a specific point in the morph."""
        if self.method == "logarithmic":
            return self._log_interpolate(t)
        return self._linear_interpolate(t)

    def _linear_interpolate(self, t: float) -> list[Partial]:
        """Linear interpolation of frequency and amplitude."""
        result: list[Partial] = []
        max_len = max(len(self.source), len(self.target))

        for i in range(max_len):
            src_partial = self.source[i] if i < len(self.source) else Partial(0, 0)
            tgt_partial = self.target[i] if i < len(self.target) else Partial(0, 0)

            # Skip if both are zero
            if src_partial.freq == 0 and tgt_partial.freq == 0:
                continue

            freq = src_partial.freq + (tgt_partial.freq - src_partial.freq) * t
            amp = src_partial.amp + (tgt_partial.amp - src_partial.amp) * t

            if amp > 0 and freq > 0:
                result.append(Partial(freq, amp))

        return result

    def _log_interpolate(self, t: float) -> list[Partial]:
        """Logarithmic interpolation (better for frequency perception)."""
        import math

        result: list[Partial] = []
        max_len = max(len(self.source), len(self.target))

        for i in range(max_len):
            src_partial = self.source[i] if i < len(self.source) else Partial(0, 0)
            tgt_partial = self.target[i] if i < len(self.target) else Partial(0, 0)

            if src_partial.freq == 0 and tgt_partial.freq == 0:
                continue

            # Log interpolation for frequency (perceptually uniform)
            if src_partial.freq > 0 and tgt_partial.freq > 0:
                freq = math.exp(
                    math.log(src_partial.freq)
                    + (math.log(tgt_partial.freq) - math.log(src_partial.freq)) * t
                )
            else:
                freq = src_partial.freq + (tgt_partial.freq - src_partial.freq) * t

            # Linear for amplitude
            amp = src_partial.amp + (tgt_partial.amp - src_partial.amp) * t

            if amp > 0 and freq > 0:
                result.append(Partial(freq, amp))

        return result


def morph_dissonance(
    source: list[Partial],
    target: list[Partial],
    steps: int = 10,
) -> list[float]:
    """
    Compute dissonance at each step of a spectral morph.

    Useful for analyzing how consonance changes during timbral transformation.

    Args:
        source: Source spectrum.
        target: Target spectrum.
        steps: Number of interpolation steps.

    Returns:
        List of dissonance values at each step.
    """
    from .dissonance import dissonance_spectrum

    morph = SpectralMorph(source, target, steps)
    return [dissonance_spectrum(partials) for partials in morph.interpolate()]
