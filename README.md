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

## API

### `dissonance_interval(freq1, freq2, harmonics=6, curve=None)`

Compute dissonance of an interval between two fundamentals.

### `dissonance_spectrum(partials, curve=None)`

Compute total dissonance of a spectrum (multiple partials).

### `dissonance_two_partial(f1, f2, a1=1.0, a2=1.0, curve=None)`

Compute dissonance between two individual partials.

### `DissonanceCurve`

Dataclass for customizing the dissonance curve parameters.

## Theory

The Sethares model is based on Plomp & Levelt's experimental work on sensory consonance, which found that dissonance between two tones depends on their frequency separation relative to the **critical bandwidth** of the ear.

Key insights:
- Two tones are most dissonant when separated by ~1/4 of a critical bandwidth
- Consonance occurs when partials align (simple ratios) or are widely separated
- The model explains why certain timbres sound consonant in some tunings but not others

## License

MIT
