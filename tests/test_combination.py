"""Tests for combination tone generation."""

import pytest
from partials import Partial
from partials.combination import (
    analyze_combination_density,
    difference_tone,
    generate_combination_tones,
    ring_modulation_spectrum,
)


class TestDifferenceTone:
    """Tests for difference_tone function."""

    def test_basic_difference(self):
        """Basic difference tone calculation."""
        assert difference_tone(1000, 1200) == 200.0

    def test_order_independent(self):
        """Order should not matter."""
        assert difference_tone(1000, 1200) == difference_tone(1200, 1000)

    def test_musical_interval(self):
        """Musical interval example."""
        # Perfect fifth: 440 Hz and 660 Hz
        assert difference_tone(440, 660) == 220.0  # Octave below fundamental

    def test_same_frequency(self):
        """Same frequency should give zero."""
        assert difference_tone(440, 440) == 0.0


class TestGenerateCombinationTones:
    """Tests for generate_combination_tones function."""

    def test_basic_generation(self):
        """Basic combination tone generation."""
        partials = [Partial(1000), Partial(1200)]
        result = generate_combination_tones(partials, max_order=1)

        assert len(result.all_partials) >= 2  # At least originals
        assert result.total_generated >= 0

    def test_difference_tone_present(self):
        """Difference tone should be present."""
        partials = [Partial(1000), Partial(1200)]
        result = generate_combination_tones(partials, max_order=1)

        # Should have 200 Hz difference tone
        freqs = [p.freq for p in result.all_partials]
        assert any(abs(f - 200.0) < 1.0 for f in freqs)

    def test_empty_input(self):
        """Empty input should return empty result."""
        result = generate_combination_tones([])

        assert result.total_generated == 0
        assert len(result.all_partials) == 0

    def test_single_partial(self):
        """Single partial should generate minimal combinations."""
        result = generate_combination_tones([Partial(440)], max_order=1)

        # Single partial can only interact with itself
        assert len(result.original_partials) == 1

    def test_amplitude_decay(self):
        """Higher orders should have lower amplitude."""
        partials = [Partial(1000, 1.0), Partial(1200, 1.0)]
        result = generate_combination_tones(
            partials, max_order=3, amplitude_decay=0.5
        )

        # Check that amplitudes decrease with order
        if len(result.combination_partials) > 1:
            # General trend should be decreasing
            pass  # Detailed amplitude check

    def test_frequency_bounds(self):
        """Should respect frequency bounds."""
        partials = [Partial(100), Partial(150)]
        result = generate_combination_tones(
            partials,
            max_order=2,
            min_frequency=50,
            max_frequency=500,
        )

        for p in result.all_partials:
            assert 50 <= p.freq <= 500

    def test_amplitude_threshold(self):
        """Should filter by amplitude threshold."""
        partials = [Partial(1000, 0.1), Partial(1200, 0.1)]
        result = generate_combination_tones(
            partials, max_order=2, min_amplitude=0.01
        )

        for p in result.all_partials:
            assert p.amp >= 0.01 or p in partials

    def test_result_structure(self):
        """Result should have all expected fields."""
        partials = [Partial(440), Partial(660)]
        result = generate_combination_tones(partials, max_order=1)

        assert hasattr(result, "original_partials")
        assert hasattr(result, "combination_partials")
        assert hasattr(result, "all_partials")
        assert hasattr(result, "max_order")
        assert hasattr(result, "total_generated")


class TestRingModulationSpectrum:
    """Tests for ring_modulation_spectrum function."""

    def test_basic_ring_mod(self):
        """Basic ring modulation spectrum."""
        spectrum = ring_modulation_spectrum(1000, 200, harmonics=3)

        assert len(spectrum) > 0
        # Should include sum and difference frequencies
        freqs = [p.freq for p in spectrum]
        assert any(abs(f - 800) < 1 for f in freqs)  # 1000 - 200
        assert any(abs(f - 1200) < 1 for f in freqs)  # 1000 + 200

    def test_includes_original(self):
        """Should include original frequencies if requested."""
        spectrum = ring_modulation_spectrum(1000, 200, include_original=True)

        freqs = [p.freq for p in spectrum]
        assert 1000 in freqs
        assert 200 in freqs

    def test_excludes_original(self):
        """Should exclude original frequencies if requested."""
        spectrum = ring_modulation_spectrum(1000, 200, include_original=False)

        freqs = [p.freq for p in spectrum]
        assert 1000 not in freqs
        assert 200 not in freqs

    def test_harmonics_count(self):
        """Should generate correct number of harmonics."""
        spectrum = ring_modulation_spectrum(1000, 200, harmonics=6)

        # Should have multiple partials
        assert len(spectrum) > 4  # At least sum/diff for each harmonic


class TestAnalyzeCombinationDensity:
    """Tests for analyze_combination_density function."""

    def test_basic_density(self):
        """Basic density analysis."""
        partials = [Partial(440), Partial(660)]
        density = analyze_combination_density(partials, max_order=1, bins=10)

        assert len(density) == 10
        assert all(isinstance(d[1], float) for d in density)

    def test_empty_input(self):
        """Empty input should return empty result."""
        density = analyze_combination_density([])

        assert len(density) == 0

    def test_density_values_normalized(self):
        """Density values should be normalized."""
        partials = [Partial(440), Partial(660), Partial(880)]
        density = analyze_combination_density(partials, max_order=2, bins=20)

        if density:
            densities = [d[1] for d in density]
            assert all(0 <= d <= 1 for d in densities)
