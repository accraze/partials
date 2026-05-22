"""Tests for spectral morphing."""

import pytest
from partials import Partial, SpectralMorph, morph_dissonance


class TestSpectralMorph:
    """Tests for SpectralMorph class."""

    def test_morph_basic(self):
        """Basic morph between two spectra."""
        source = [Partial(440.0, 1.0)]
        target = [Partial(880.0, 1.0)]
        morph = SpectralMorph(source, target, steps=5)

        result = list(morph.interpolate())
        assert len(result) == 6  # steps + 1

    def test_morph_preserves_count(self):
        """Morph should preserve number of partials."""
        source = [Partial(440.0, 1.0), Partial(880.0, 0.5)]
        target = [Partial(440.0, 0.5), Partial(660.0, 1.0)]
        morph = SpectralMorph(source, target, steps=3)

        for partials in morph.interpolate():
            assert len(partials) == 2

    def test_morph_endpoints(self):
        """Morph should start at source and end at target."""
        source = [Partial(440.0, 1.0)]
        target = [Partial(880.0, 0.5)]
        morph = SpectralMorph(source, target, steps=5)

        result = list(morph.interpolate())
        # First should be close to source
        assert abs(result[0][0].freq - 440.0) < 1.0
        # Last should be close to target
        assert abs(result[-1][0].freq - 880.0) < 1.0

    def test_morph_different_lengths(self):
        """Morph should handle spectra with different partial counts."""
        source = [Partial(440.0, 1.0)]
        target = [Partial(440.0, 1.0), Partial(880.0, 0.5)]
        morph = SpectralMorph(source, target, steps=3)

        result = list(morph.interpolate())
        assert len(result) == 4

    def test_morph_logarithmic(self):
        """Logarithmic morph should work."""
        source = [Partial(440.0, 1.0)]
        target = [Partial(880.0, 1.0)]
        morph = SpectralMorph(source, target, steps=5, method="logarithmic")

        result = list(morph.interpolate())
        assert len(result) == 6


class TestMorphDissonance:
    """Tests for morph_dissonance function."""

    def test_morph_dissonance_basic(self):
        """Basic morph dissonance computation."""
        source = [Partial(440.0, 1.0)]
        target = [Partial(880.0, 1.0)]

        result = morph_dissonance(source, target, steps=5)
        assert len(result) == 6  # steps + 1

    def test_morph_dissonance_values(self):
        """Morph dissonance should return reasonable values."""
        source = [Partial(440.0, 1.0), Partial(660.0, 0.5)]
        target = [Partial(440.0, 1.0), Partial(880.0, 0.5)]

        result = morph_dissonance(source, target, steps=10)
        assert all(d >= 0 for d in result)
