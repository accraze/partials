#!/usr/bin/env python3
"""
partials-av-prototype.py — Image → Spectrum → Audio (Phase 1)

Loads an image, extracts luminance-based partials, synthesizes audio
using the partials library, and exports a WAV file.

Usage:
    python partials-av-prototype.py path/to/image.jpg [--duration 10] [--output out.wav]

Dependencies:
    pip install partials numpy pillow soundfile
"""

import argparse
import numpy as np
from PIL import Image
from scipy.io.wavfile import write as write_wav
from partials import Partial

# ============================================================================
# Config
# ============================================================================
SAMPLE_RATE = 44100
DURATION = 10  # seconds
NUM_PARTIALS = 20  # how many partials to extract from image
BASE_FREQ = 110.0  # A2 — base frequency for mapping
FREQ_RANGE = 880.0  # frequency range (A2 to A4 = 110-990 Hz)

# ============================================================================
# Image → Spectrum
# ============================================================================
def image_to_partials(image_path: str, num_partials: int = NUM_PARTIALS):
    """
    Extract partials from an image by analyzing column-wise luminance.

    Returns a list of (frequency, amplitude) tuples.
    """
    img = Image.open(image_path).convert('L')  # grayscale
    img_array = np.array(img)
    
    # Get image dimensions
    height, width = img_array.shape
    
    # Calculate luminance per column (average brightness across rows)
    column_luminance = np.mean(img_array, axis=0)  # shape: (width,)
    
    # Normalize to 0-1
    column_luminance = column_luminance / 255.0
    
    # Select num_partials evenly-spaced columns as frequency bins
    indices = np.linspace(0, width - 1, num_partials, dtype=int)
    
    partials = []
    for i, idx in enumerate(indices):
        # Map column index to frequency (linear mapping)
        freq = BASE_FREQ + (i / num_partials) * FREQ_RANGE
        
        # Use luminance as amplitude (0-1 scale)
        amp = column_luminance[idx]
        
        # Skip silent partials
        if amp > 0.01:
            partials.append((freq, amp))
    
    print(f"Extracted {len(partials)} partials from {image_path}")
    print(f"Frequency range: {partials[0][0]:.1f} Hz - {partials[-1][0]:.1f} Hz")
    print(f"Amplitude range: {min(p[1] for p in partials):.3f} - {max(p[1] for p in partials):.3f}")
    
    return partials

# ============================================================================
# Synthesis
# ============================================================================
def synthesize_partials(partials: list, duration: float = DURATION, sample_rate: int = SAMPLE_RATE):
    """
    Synthesize audio from partials using additive synthesis.
    
    partials: list of (frequency, amplitude) tuples
    duration: seconds
    sample_rate: Hz
    
    Returns: numpy array of audio samples (float32, -1 to 1)
    """
    n_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, n_samples, dtype=np.float32)
    
    audio = np.zeros(n_samples, dtype=np.float32)
    
    # Additive synthesis: sum of sine waves
    for freq, amp in partials:
        # Apply simple amplitude envelope (fade in/out to avoid clicks)
        envelope = np.ones_like(t)
        fade_samples = int(0.01 * sample_rate)  # 10ms fade
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        # Generate sine wave
        sine = amp * np.sin(2 * np.pi * freq * t) * envelope
        audio += sine
    
    # Normalize to prevent clipping
    max_amp = np.max(np.abs(audio))
    if max_amp > 0:
        audio = audio / max_amp * 0.9  # Leave 10% headroom
    
    print(f"Synthesized {duration}s audio at {sample_rate} Hz ({len(audio)} samples)")
    
    return audio

# ============================================================================
# Main
# ============================================================================
def main():
    parser = argparse.ArgumentParser(description="Image → Spectrum → Audio prototype")
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("--duration", type=float, default=DURATION, help=f"Duration in seconds (default: {DURATION})")
    parser.add_argument("--output", default="output.wav", help="Output WAV file (default: output.wav)")
    parser.add_argument("--partials", type=int, default=NUM_PARTIALS, help=f"Number of partials (default: {NUM_PARTIALS})")
    
    args = parser.parse_args()
    
    print(f"=== partials A/V Prototype ===")
    print(f"Input: {args.image}")
    print(f"Duration: {args.duration}s")
    print(f"Output: {args.output}")
    print()
    
    # Step 1: Extract partials from image
    partials = image_to_partials(args.image, num_partials=args.partials)
    
    if not partials:
        print("ERROR: No partials extracted. Try a different image or lower --partials threshold.")
        return 1
    
    # Step 2: Synthesize audio
    audio = synthesize_partials(partials, duration=args.duration)
    
    # Step 3: Export WAV
    write_wav(args.output, SAMPLE_RATE, (audio * 32767).astype(np.int16))
    print(f"✅ Wrote {args.output}")
    
    return 0

if __name__ == "__main__":
    exit(main())