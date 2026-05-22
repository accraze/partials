#!/usr/bin/env python3
"""Demo: Combination tones and emergent pitch clouds."""

from partials import (
    Partial,
    difference_tone,
    generate_combination_tones,
    ring_modulation_spectrum,
    analyze_combination_density,
)
from partials.viz import spectrum_text
from partials.dissonance import dissonance_spectrum

print("=" * 70)
print("COMBINATION TONES: Emergent Pitch Clouds")
print("=" * 70)

# =============================================================================
# 1. Basic Difference Tones (Tartini Tones)
# =============================================================================
print("\n" + "=" * 70)
print("1. DIFFERENCE TONES (Tartini Tones)")
print("=" * 70)

print("\nWhen two frequencies interact, you hear a third tone at f2 - f1:")
print("-" * 70)

examples = [
    ("Perfect Fifth", 440, 660),
    ("Perfect Fourth", 440, 587.33),
    ("Major Third", 440, 554.37),
    ("Minor Second", 440, 466.16),
]

for name, f1, f2 in examples:
    diff = difference_tone(f1, f2)
    print(f"{name:15s}: {f1:6.1f} Hz + {f2:6.1f} Hz → {diff:6.1f} Hz difference")

# =============================================================================
# 2. Recursive Combination Tones
# =============================================================================
print("\n" + "=" * 70)
print("2. RECURSIVE COMBINATION TONES")
print("=" * 70)

print("\nTwo drones at 400 Hz and 500 Hz, order 1-3:")
print("-" * 70)

partials = [Partial(400, 1.0), Partial(500, 1.0)]

for order in range(1, 4):
    result = generate_combination_tones(partials, max_order=order)
    print(f"\nOrder {order} ({result.total_generated} combination tones):")
    freqs = [(p.freq, p.amp) for p in result.all_partials]
    freqs.sort(key=lambda x: x[0])
    for freq, amp in freqs[:15]:  # Show first 15
        bar = "█" * int(amp * 20)
        print(f"  {freq:7.1f} Hz: {bar} (amp: {amp:.3f})")
    if len(freqs) > 15:
        print(f"  ... and {len(freqs) - 15} more")

# =============================================================================
# 3. Ring Modulation Spectrum
# =============================================================================
print("\n" + "=" * 70)
print("3. RING MODULATION SPECTRUM")
print("=" * 70)

print("\nRing mod: 1000 Hz carrier × 200 Hz modulator")
print("-" * 70)

spectrum = ring_modulation_spectrum(1000, 200, harmonics=6)
print(spectrum_text(spectrum, width=60))

print("\nFrequencies present:")
for p in spectrum[:12]:
    print(f"  {p.freq:7.1f} Hz (amp: {p.amp:.3f})")

# =============================================================================
# 4. Drone Interaction Analysis
# =============================================================================
print("\n" + "=" * 70)
print("4. DRONE INTERACTION ANALYSIS")
print("=" * 70)

print("\nAnalyzing two drones: 220 Hz and 330 Hz (perfect fifth)")
print("-" * 70)

drone_partials = [
    Partial(220, 1.0),
    Partial(440, 0.5),
    Partial(660, 0.25),
    Partial(330, 1.0),
    Partial(660, 0.5),
    Partial(990, 0.25),
]

result = generate_combination_tones(drone_partials, max_order=2, min_amplitude=0.01)

print(f"\nOriginal partials: {len(result.original_partials)}")
print(f"Combination tones generated: {result.total_generated}")
print(f"Total in spectrum: {len(result.all_partials)}")

print("\nResulting spectrum (first 20 partials):")
for i, p in enumerate(result.all_partials[:20]):
    in_original = any(abs(p.freq - op.freq) < 1 for op in result.original_partials)
    marker = "*" if in_original else " "
    bar = "█" * int(p.amp * 30)
    print(f"{marker} {p.freq:7.1f} Hz: {bar} (amp: {p.amp:.3f})")

# Calculate dissonance of the emergent spectrum
d_original = dissonance_spectrum([p for p in result.original_partials])
d_all = dissonance_spectrum(result.all_partials)

print(f"\nDissonance - Original only: {d_original:.4f}")
print(f"Dissonance - With combinations: {d_all:.4f}")

# =============================================================================
# 5. Combination Density Analysis
# =============================================================================
print("\n" + "=" * 70)
print("5. COMBINATION DENSITY ACROSS SPECTRUM")
print("=" * 70)

print("\nWhere do combination tones cluster? (220 Hz + 330 Hz)")
print("-" * 70)

density = analyze_combination_density(drone_partials, max_order=2, bins=20)

# Show density peaks
sorted_density = sorted(density, key=lambda x: x[1], reverse=True)
print("\nTop 5 frequency regions with most combination activity:")
for freq, dens in sorted_density[:5]:
    bar = "█" * int(dens * 40)
    print(f"  {freq:7.1f} Hz: {bar} (density: {dens:.3f})")

print("\n" + "=" * 70)
print("Demo complete!")
print("=" * 70)
