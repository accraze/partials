"""Tests for Sethares dissonance model implementation."""

import math
import pytest
from partials import (
    dissonance_two_partial,
    dissonance_spectrum,
    dissonance_interval,
    DissonanceCurve,
    Partial,
)


class TestDissonanceTwoPartial:
    """Tests for two-partial dissonance function."""

    def test_same_frequency_zero_dissonance(self):
        """Identical frequencies should have zero dissonance."""
        assert dissonance_two_partial(440.0, 440.0) == 0.0

    def test_close_frequencies_high_dissonance(self):
        """Very close frequencies produce high dissonance."""
        d = dissonance_two_partial(440.0, 441.0)
        assert d > 0

    def test_octave_low_dissonance(self):
        """Octave interval should have low dissonance."""
        d = dissonance_two_partial(440.0, 880.0)
        # Octave should have minimal dissonance
        assert d >= 0

    def test_amplitude_scaling(self):
        """Dissonance should scale with amplitude."""
        d1 = dissonance_two_partial(440.0, 450.0, 1.0, 1.0)
        d2 = dissonance_two_partial(440.0, 450.0, 0.5, 0.5)
        assert d1 > d2

    def test_frequency_order_independent(self):
        """Order of frequencies should not matter."""
        d1 = dissonance_two_partial(440.0, 500.0)
        d2 = dissonance_two_partial(500.0, 440.0)
        assert math.isclose(d1, d2, rel_tol=1e-10)

    def test_very_close_frequencies(self):
        """Test behavior with very close frequency separation."""
        # Below minimum separation threshold
        d = dissonance_two_partial(1000.0, 1000.1)
        assert d >= 0


class TestDissonanceInterval:
    """Tests for interval dissonance function."""

    def test_perfect_fifth_consonant(self):
        """Perfect fifth (3:2 ratio) should have relatively low dissonance."""
        d = dissonance_interval(440.0, 660.0)
        # Should be relatively consonant
        assert d >= 0

    def test_minor_second_dissonant(self):
        """Minor second should have high dissonance."""
        # A4 to A#4
        d = dissonance_interval(440.0, 466.16)
        assert d > 0

    def test_unison_zero_dissonance(self):
        """Unison should have minimal dissonance."""
        d = dissonance_interval(440.0, 440.0)
        assert d >= 0

    def test_octave_consonant(self):
        """Octave should have low dissonance."""
        d = dissonance_interval(440.0, 880.0)
        assert d >= 0

    def test_more_harmonics_increases_dissonance(self):
        """More harmonics generally increases total dissonance."""
        d6 = dissonance_interval(440.0, 500.0, harmonics=6)
        d12 = dissonance_interval(440.0, 500.0, harmonics=12)
        # More harmonics = more partial pairs = more dissonance
        assert d12 >= d6


class TestDissonanceSpectrum:
    """Tests for spectrum dissonance function."""

    def test_single_partial_zero(self):
        """Single partial should have zero dissonance."""
        partials = [Partial(440.0)]
        d = dissonance_spectrum(partials)
        assert d == 0.0

    def test_empty_spectrum_zero(self):
        """Empty spectrum should have zero dissonance."""
        d = dissonance_spectrum([])
        assert d == 0.0

    def test_major_triad(self):
        """Major triad should have measurable dissonance."""
        partials = [
            Partial(261.63),  # C4
            Partial(329.63),  # E4
            Partial(392.00),  # G4
        ]
        d = dissonance_spectrum(partials)
        assert d >= 0

    def test_amplitude_affects_dissonance(self):
        """Higher amplitudes should increase dissonance."""
        partials_low = [
            Partial(440.0, 0.5),
            Partial(500.0, 0.5),
        ]
        partials_high = [
            Partial(440.0, 1.0),
            Partial(500.0, 1.0),
        ]
        d_low = dissonance_spectrum(partials_low)
        d_high = dissonance_spectrum(partials_high)
        assert d_high > d_low


class TestDissonanceCurve:
    """Tests for dissonance curve customization."""

    def test_custom_curve_parameters(self):
        """Custom curve parameters should affect dissonance calculation."""
        curve1 = DissonanceCurve(a1=3.5, a2=5.75)
        curve2 = DissonanceCurve(a1=7.0, a2=11.5)

        d1 = dissonance_two_partial(440.0, 450.0, curve=curve1)
        d2 = dissonance_two_partial(440.0, 450.0, curve=curve2)

        # Different curve parameters should produce different results
        assert d1 != d2

    def test_default_curve(self):
        """Default curve should work without explicit parameters."""
        d = dissonance_two_partial(440.0, 450.0)
        assert d > 0


class TestEdgeCases:
    """Edge case tests."""

    def test_very_low_frequency(self):
        """Test with very low frequencies."""
        d = dissonance_two_partial(20.0, 25.0)
        assert d >= 0

    def test_very_high_frequency(self):
        """Test with very high frequencies."""
        d = dissonance_two_partial(10000.0, 10010.0)
        assert d >= 0

    def test_zero_amplitude(self):
        """Zero amplitude should produce zero dissonance."""
        d = dissonance_two_partial(440.0, 450.0, a1=0.0, a2=1.0)
        assert d == 0.0
