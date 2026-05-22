#!/usr/bin/env python3
"""Demo: Exploring dissonance with partials."""

from partials import dissonance_interval, dissonance_spectrum, Partial
import math

print("=== Partials Demo ===\n")

# Demo 1: Interval dissonance
print("1. Interval Dissonance (A4 = 440 Hz):")
print("-" * 40)
intervals = [
    ("Unison", 440.0, 440.0),
    ("Minor 2nd", 440.0, 466.16),
    ("Major 2nd", 440.0, 493.88),
    ("Major 3rd", 440.0, 554.37),
    ("Perfect 4th", 440.0, 587.33),
    ("Perfect 5th", 440.0, 660.0),
    ("Octave", 440.0, 880.0),
]

for name, f1, f2 in intervals:
    d = dissonance_interval(f1, f2)
    print(f"{name:12s}: {d:.4f}")

# Demo 2: Custom spectrum
print("\n2. Custom Spectrum Dissonance:")
print("-" * 40)
# Inharmonic spectrum
partials_inharmonic = [
    Partial(440.0, 1.0),
    Partial(900.0, 0.5),   # Not a harmonic
    Partial(1400.0, 0.25), # Not a harmonic
]
d_inh = dissonance_spectrum(partials_inharmonic)
print(f"Inharmonic spectrum: {d_inh:.4f}")

# Harmonic spectrum
partials_harmonic = [
    Partial(440.0, 1.0),
    Partial(880.0, 0.5),   # 2nd harmonic
    Partial(1320.0, 0.25), # 3rd harmonic
]
d_harm = dissonance_spectrum(partials_harmonic)
print(f"Harmonic spectrum:   {d_harm:.4f}")

# Demo 3: Dissonance curve visualization (text-based)
print("\n3. Dissonance vs Frequency Separation:")
print("-" * 40)
print("Showing dissonance for 440 Hz + Δf:")
for df in [1, 5, 10, 20, 50, 100, 200]:
    d = dissonance_interval(440.0, 440.0 + df)
    bar = "█" * int(d * 20)
    print(f"  Δf={df:3d} Hz: {bar} ({d:.4f})")

print("\n=== Done ===")
