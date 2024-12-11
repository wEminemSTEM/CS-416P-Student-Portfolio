# Kris Cooper 2024

import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import time

# Constants
SAMPLE_RATE = 48000  # 48 kHz sample rate
DURATION = 1  # 1 second
FREQUENCY = 440  # 440 Hz (A4 note)
AMPLITUDE = 8192  # Amplitude for sine wave (1/4 max of 16-bit range)
CLIPPED_AMPLITUDE = 16384  # 1/2 max amplitude for clipped wave
CLIP_THRESHOLD = 8192  # Clipping threshold

# Step 1: Generate  & save sine wave to sine.wav
def generate_sine_wave(frequency, duration, amplitude, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine_wave.astype(np.int16)

# 2: Generate & save clipped sine wave to clipped.wav
def generate_clipped_wave(frequency, duration, amplitude, sample_rate, clip_threshold):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    clipped_wave = np.clip(sine_wave, -clip_threshold, clip_threshold)
    return clipped_wave.astype(np.int16)

# 3: Play the clipped sine wave directly
def play_audio(audio_data, sample_rate):
    sd.play(audio_data, samplerate=sample_rate)
    sd.wait()


def main():
    try:
        sine_wave = generate_sine_wave(FREQUENCY, DURATION, AMPLITUDE, SAMPLE_RATE)
        write("sine.wav", SAMPLE_RATE, sine_wave)
        clipped_wave = generate_clipped_wave(FREQUENCY, DURATION, CLIPPED_AMPLITUDE, SAMPLE_RATE, CLIP_THRESHOLD)
        write("clipped.wav", SAMPLE_RATE, clipped_wave)

        print("Playing sine_wave...")
        play_audio(sine_wave, SAMPLE_RATE)
        time.sleep(1)

        print("Playing clipped_wave...")
        play_audio(clipped_wave, SAMPLE_RATE)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
