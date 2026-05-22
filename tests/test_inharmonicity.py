"""Tests for inharmonicity analysis."""

import pytest
from partials import (
    Partial,
    analyze_inharmonicity,
    generate_inharmonic_series,
    harmonic_deviation_score,
    InharmonicityResult,
)


class TestAnalyzeInharmonicity:
    """Tests for analyze_inharmonicity function."""

    def test_perfectly_harmonic(self):
        """Perfect harmonic series should have zero inharmonicity."""
        # Perfect harmonic series
        partials = [Partial(440.0 * n, 1.0 / n) for n in range(1, 6)]
        result = analyze_inharmonicity(partials)

        assert result.b_factor >= 0
        assert result.rms_deviation < 1.0  # Very small deviation

    def test_inharmonic_series(self):
        """Inharmonic series should have positive B-factor."""
        # Stretched series (piano-like)
        partials = [
            Partial(440.0 * 1 * 1.001, 1.0),  # Slightly sharp
            Partial(440.0 * 2 * 1.002, 0.5),  # More sharp
            Partial(440.0 * 3 * 1.003, 0.33), # Even more sharp
        ]
        result = analyze_inharmonicity(partials)

        assert result.b_factor > 0

    def test_empty_partials(self):
        """Empty partial list should return zero values."""
        result = analyze_inharmonicity([])

        assert result.b_factor == 0.0
        assert result.rms_deviation == 0.0
        assert result.total_partials == 0

    def test_single_partial(self):
        """Single partial should have minimal inharmonicity."""
        result = analyze_inharmonicity([Partial(440.0)])

        assert result.total_partials == 1

    def test_result_structure(self):
        """Result should have all expected fields."""
        partials = [Partial(440.0), Partial(880.0)]
        result = analyze_inharmonicity(partials)

        assert isinstance(result, InharmonicityResult)
        assert hasattr(result, "b_factor")
        assert hasattr(result, "rms_deviation")
        assert hasattr(result, "harmonic_partial_count")
        assert hasattr(result, "total_partials")
        assert hasattr(result, "inharmonicity_ratio")


class TestGenerateInharmonicSeries:
    """Tests for generate_inharmonic_series function."""

    def test_basic_generation(self):
        """Basic inharmonic series generation."""
        partials = generate_inharmonic_series(440.0, num_partials=12)

        assert len(partials) == 12
        assert all(p.freq > 0 for p in partials)

    def test_b_factor_effect(self):
        """B-factor should affect frequencies."""
        harmonic = generate_inharmonic_series(440.0, 12, 0.0)
        inharmonic = generate_inharmonic_series(440.0, 12, 0.001)

        # Frequencies should differ
        for h, i in zip(harmonic, inharmonic):
            assert h.freq != i.freq

    def test_zero_b_factor(self):
        """Zero B-factor should produce harmonic series."""
        partials = generate_inharmonic_series(440.0, 12, 0.0)

        # Check harmonic relationships
        for i, p in enumerate(partials):
            expected = 440.0 * (i + 1)
            assert abs(p.freq - expected) < 0.001  # Very close

    def test_amplitude_rolloff(self):
        """Amplitudes should decrease with harmonic number."""
        partials = generate_inharmonic_series(440.0, 6, 0.0)

        for i in range(len(partials) - 1):
            assert partials[i].amp >= partials[i + 1].amp


class TestHarmonicDeviationScore:
    """Tests for harmonic_deviation_score function."""

    def test_perfect_harmonic_zero(self):
        """Perfect harmonic series should have near-zero score."""
        partials = [Partial(440.0 * n, 1.0) for n in range(1, 6)]
        score = harmonic_deviation_score(partials)

        assert score < 1.0  # Very small

    def test_inharmonic_positive_score(self):
        """Inharmonic series should have positive score."""
        # Detuned series
        partials = [
            Partial(440.0 * 1 * 1.05, 1.0),  # 5% sharp
            Partial(440.0 * 2 * 0.95, 0.5),  # 5% flat
        ]
        score = harmonic_deviation_score(partials)

        assert score > 0
