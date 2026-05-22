"""Tests for visualization tools."""

import pytest
from partials import Partial
from partials.viz import (
    compare_spectra,
    morph_trajectory,
    plot_dissonance_curve,
    spectrum_text,
)


class TestPlotDissonanceCurve:
    """Tests for plot_dissonance_curve function."""

    def test_basic_plot(self):
        """Basic dissonance curve generation."""
        result = plot_dissonance_curve(440.0, max_ratio=2.0, steps=20)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "1.0" in result  # Should have x-axis labels

    def test_custom_parameters(self):
        """Custom parameters should work."""
        result = plot_dissonance_curve(
            fundamental=220.0,
            max_ratio=1.5,
            steps=10,
            width=40,
            height=15,
        )

        assert isinstance(result, str)


class TestSpectrumText:
    """Tests for spectrum_text function."""

    def test_basic_spectrum(self):
        """Basic spectrum visualization."""
        partials = [Partial(440.0, 1.0), Partial(880.0, 0.5)]
        result = spectrum_text(partials)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_empty_spectrum(self):
        """Empty spectrum should return message."""
        result = spectrum_text([])

        assert "No partials" in result

    def test_custom_width(self):
        """Custom width should work."""
        partials = [Partial(440.0, 1.0)]
        result = spectrum_text(partials, width=40)

        assert isinstance(result, str)


class TestMorphTrajectory:
    """Tests for morph_trajectory function."""

    def test_basic_trajectory(self):
        """Basic morph trajectory generation."""
        source = [Partial(440.0, 1.0)]
        target = [Partial(880.0, 1.0)]
        result = morph_trajectory(source, target, steps=5)

        assert isinstance(result, str)
        assert "Spectral Morph Trajectory" in result

    def test_trajectory_steps(self):
        """Trajectory should show all steps."""
        source = [Partial(440.0, 1.0)]
        target = [Partial(880.0, 1.0)]
        result = morph_trajectory(source, target, steps=10)

        lines = result.split("\n")
        # Should have header + steps + 1
        assert len(lines) >= 10


class TestCompareSpectra:
    """Tests for compare_spectra function."""

    def test_basic_comparison(self):
        """Basic spectrum comparison."""
        spectra = [
            ("Harmonic", [Partial(440.0, 1.0), Partial(880.0, 0.5)]),
            ("Inharmonic", [Partial(440.0, 1.0), Partial(900.0, 0.5)]),
        ]
        result = compare_spectra(spectra)

        assert isinstance(result, str)
        assert "Spectrum Comparison" in result
        assert "Harmonic" in result
        assert "Inharmonic" in result

    def test_single_spectrum(self):
        """Single spectrum comparison should work."""
        spectra = [("Test", [Partial(440.0, 1.0)])]
        result = compare_spectra(spectra)

        assert isinstance(result, str)
