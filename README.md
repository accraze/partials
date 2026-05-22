# partials

**Psychoacoustic tools for working with the physical reality of sound.**

Partials implements the Sethares dissonance model for analyzing timbral dissonance, partial series, and inharmonic spectra. Built for composers, researchers, and sound designers working with the physical basis of musical perception.

## Installation

```bash
uv add partials
```

Or from source:

```bash
git clone https://github.com/accraze/partials.git
cd partials
uv install
```

## Quick Start

```python
from partials import dissonance_interval, dissonance_spectrum, Partial

# Dissonance of a perfect fifth (440 Hz and 660 Hz)
d = dissonance_interval(440.0, 660.0)
print(f"Perfect fifth dissonance: {d:.4f}")

# Dissonance of a minor second (high dissonance)
d = dissonance_interval(440.0, 466.16)
print(f"Minor second dissonance: {d:.4f}")

# Custom spectrum dissonance
partials = [
    Partial(440.0, 1.0),    # Fundamental
    Partial(880.0, 0.5),    # 2nd harmonic
    Partial(1320.0, 0.25),  # 3rd harmonic
]
d = dissonance_spectrum(partials)
print(f"Custom spectrum dissonance: {d:.4f}")
```

## Features

### 1. Sethares Dissonance Model
- Compute sensory dissonance between partials
- Analyze intervals and chords
- Custom dissonance curves

### 2. Spectral Morphing
- Smooth interpolation between timbres
- Linear and logarithmic morphing
- Track dissonance during transformation

```python
from partials import SpectralMorph, Partial

source = [Partial(440, 1.0), Partial(880, 0.5)]
target = [Partial(440, 1.0), Partial(660, 1.0)]

morph = SpectralMorph(source, target, steps=10)
for step in morph.interpolate():
    print(dissonance_spectrum(step))
```

### 3. Inharmonicity Analysis
- B-factor estimation (piano-style inharmonicity)
- Harmonic deviation scoring
- Generate inharmonic series

```python
from partials import analyze_inharmonicity, generate_inharmonic_series

# Analyze piano-like inharmonicity
partials = generate_inharmonic_series(220.0, b_factor=0.001)
result = analyze_inharmonicity(partials)
print(f"B-factor: {result.b_factor}")
```

### 4. Visualization
- ASCII spectrum plots
- Dissonance curves
- Morph trajectory visualization

```python
from partials.viz import plot_dissonance_curve, spectrum_text

print(plot_dissonance_curve(440.0, max_ratio=2.0))
print(spectrum_text(my_partials))
```

## API Reference

### Core Functions
- `dissonance_two_partial(f1, f2, a1, a2, curve)` - Two-partial dissonance
- `dissonance_spectrum(partials, curve)` - Multi-partial dissonance
- `dissonance_interval(freq1, freq2, harmonics, curve)` - Interval dissonance

### Morphing
- `SpectralMorph(source, target, steps, method)` - Morph between spectra
- `morph_dissonance(source, target, steps)` - Dissonance during morph

### Inharmonicity
- `analyze_inharmonicity(partials, fundamental, max_harmonic)` - B-factor analysis
- `generate_inharmonic_series(fundamental, num_partials, b_factor)` - Generate series
- `harmonic_deviation_score(partials, fundamental)` - Deviation in cents

### Classes
- `Partial(freq, amp)` - Single partial
- `DissonanceCurve(a1, a2, b1, b2, min_separation)` - Curve parameters
- `InharmonicityResult` - Analysis results

## Theory

The Sethares model is based on Plomp & Levelt's experimental work on sensory consonance, which found that dissonance between two tones depends on their frequency separation relative to the **critical bandwidth** of the ear.

Key insights:
- Two tones are most dissonant when separated by ~1/4 of a critical bandwidth
- Consonance occurs when partials align (simple ratios) or are widely separated
- The model explains why certain timbres sound consonant in some tunings but not others
- Inharmonic spectra (bells, drums) have different consonance properties than harmonic ones

## Examples

Run the included demos:

```bash
# Basic demo
python examples/demo.py

# Advanced features
python examples/advanced_demo.py
```

## License

MIT
