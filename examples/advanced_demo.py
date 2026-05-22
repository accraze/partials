#!/usr/bin/env python3
"""Advanced demo: Spectral morphing, inharmonicity, and visualization."""

from partials import (
    Partial,
    SpectralMorph,
    morph_dissonance,
    analyze_inharmonicity,
    generate_inharmonic_series,
    harmonic_deviation_score,
)
from partials.viz import plot_dissonance_curve, spectrum_text, morph_trajectory, compare_spectra
from partials.dissonance import dissonance_spectrum

print("=" * 70)
print("PARTIALS: Advanced Psychoacoustic Analysis")
print("=" * 70)

# =============================================================================
# 1. Inharmonicity Analysis
# =============================================================================
print("\n" + "=" * 70)
print("1. INHARMONICITY ANALYSIS")
print("=" * 70)

print("\n--- Piano-like Inharmonicity (B = 0.001) ---")
piano_partials = generate_inharmonic_series(220.0, num_partials=12, b_factor=0.001)
result = analyze_inharmonicity(piano_partials)
print(f"B-factor: {result.b_factor:.6f}")
print(f"RMS Deviation: {result.rms_deviation:.2f} cents")
print(f"Inharmonic Energy Ratio: {result.inharmonicity_ratio:.2%}")

print("\n--- Bell-like Inharmonicity (B = 0.01) ---")
bell_partials = generate_inharmonic_series(220.0, num_partials=12, b_factor=0.01)
result = analyze_inharmonicity(bell_partials)
print(f"B-factor: {result.b_factor:.6f}")
print(f"RMS Deviation: {result.rms_deviation:.2f} cents")
print(f"Inharmonic Energy Ratio: {result.inharmonicity_ratio:.2%}")

print("\n--- Perfect Harmonic Series ---")
harmonic_partials = [Partial(220.0 * n, 1.0/n) for n in range(1, 13)]
result = analyze_inharmonicity(harmonic_partials)
print(f"B-factor: {result.b_factor:.6f}")
print(f"RMS Deviation: {result.rms_deviation:.2f} cents")
print(f"Harmonic Partial Count: {result.harmonic_partial_count}/{result.total_partials}")

# =============================================================================
# 2. Spectrum Visualization
# =============================================================================
print("\n" + "=" * 70)
print("2. SPECTRUM VISUALIZATION")
print("=" * 70)

print("\n--- Harmonic Spectrum ---")
print(spectrum_text(harmonic_partials[:6], width=60))

print("\n--- Inharmonic Spectrum (Bell-like) ---")
print(spectrum_text(bell_partials[:6], width=60))

# =============================================================================
# 3. Spectral Morphing
# =============================================================================
print("\n" + "=" * 70)
print("3. SPECTRAL MORPHING")
print("=" * 70)

source = [Partial(440.0, 1.0), Partial(880.0, 0.5), Partial(1320.0, 0.25)]
target = [Partial(440.0, 1.0), Partial(900.0, 0.5), Partial(1400.0, 0.25)]

print("\n--- Morph Trajectory (Harmonic → Inharmonic) ---")
print(morph_trajectory(source, target, steps=10))

print("\n--- Dissonance During Morph ---")
dissonances = morph_dissonance(source, target, steps=10)
for i, d in enumerate(dissonances):
    t = i / 10
    bar = "█" * int(d * 50)
    print(f"t={t:.1f}: {bar} ({d:.4f})")

# =============================================================================
# 4. Compare Multiple Spectra
# =============================================================================
print("\n" + "=" * 70)
print("4. SPECTRUM COMPARISON")
print("=" * 70)

spectra = [
    ("Harmonic (B=0)", harmonic_partials[:6]),
    ("Piano (B=0.001)", piano_partials[:6]),
    ("Bell (B=0.01)", bell_partials[:6]),
]

print(compare_spectra(spectra, width=40))

# =============================================================================
# 5. Dissonance Curve
# =============================================================================
print("\n" + "=" * 70)
print("5. DISSONANCE CURVE")
print("=" * 70)

print("\nDissonance vs Frequency Ratio (440 Hz base):")
print(plot_dissonance_curve(440.0, max_ratio=2.0, steps=50, width=60, height=15))

# =============================================================================
# 6. Practical Application: Tuning Optimization
# =============================================================================
print("\n" + "=" * 70)
print("6. APPLICATION: Finding Consonant Intervals")
print("=" * 70)

fundamental = 220.0
print(f"\nSearching for consonant intervals above {fundamental} Hz...")

intervals = []
for ratio in [1.0, 1.125, 1.2, 1.25, 1.333, 1.5, 1.6, 1.875, 2.0]:
    freq = fundamental * ratio
    d = dissonance_spectrum([Partial(fundamental), Partial(freq)])
    intervals.append((ratio, freq, d))

print("\nInterval Ratios and Dissonance:")
print("-" * 50)
for ratio, freq, d in sorted(intervals, key=lambda x: x[2], reverse=True):
    bar = "█" * int(d * 100)
    print(f"{ratio:5.3f} ({freq:6.1f} Hz): {bar} ({d:.4f})")

print("\n" + "=" * 70)
print("Demo complete!")
print("=" * 70)
