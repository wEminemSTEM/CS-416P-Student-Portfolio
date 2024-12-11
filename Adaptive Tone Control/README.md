# Tone Control Audio Processing

## Author
Kris Cooper

## Overview
This project implements a tone control system for audio processing. The program adjusts the volume of sound across three frequency bands (low, mid, high) and applies dynamic range compression and normalization to improve the audio's quality and consistency. The output audio is designed to have smooth transitions and balanced frequency energy across the bands.

---

## Features
1. **Frequency Band Adjustment**:
   - Audio is divided into low (0-300 Hz), mid (300-2000 Hz), and high (2000+ Hz) bands.
   - FFT is used to analyze and adjust the energy of each band dynamically.

2. **Dynamic Smoothing**:
   - Gain adjustments are smoothed using exponential moving averages to prevent abrupt changes.
   - Alpha values are dynamically calculated based on energy differences between bands.

3. **Dynamic Range Compression**:
   - A dynamic threshold for compression is determined based on the RMS level of the audio.
   - Ensures loudness consistency without introducing artifacts.

4. **Overlap-Add Processing**:
   - Handles windowed processing of audio frames with proper overlap and normalization to avoid popping or clipping.

5. **Normalization**:
   - Ensures the final output audio is properly scaled to avoid clipping, with safeguards for very low amplitude signals.

---

## Installation
1. Clone this repository or download the files.
2. Install dependencies:
   ```bash
   pip install numpy scipy librosa soundfile matplotlib
   ```
3. Place the input audio file in the same directory as the script.

---

## Usage
1. Modify the `FILE_NAME` variable in the script to point to your input audio file. (File should be in the same directory)
2. Run the script:
   ```bash
   python tone_control_audio.py
   ```
3. The processed audio will be saved as a new file with `(output)` appended to the original filename.

---

## Technical Notes
1. **Smoothing Gains**:
   - Gain smoothing prevents rapid volume changes that can cause audio artifacts.
   - `smoothed_low_gain`, `smoothed_mid_gain`, and `smoothed_high_gain` use weighted averages for transitions.

2. **Dynamic Threshold for Compression**:
   - The RMS level of the input audio determines the threshold for compression.
   - Prevents over-compression or under-compression based on signal strength.

3. **Error Handling**:
   - Handles edge cases such as silent or low-amplitude signals to avoid unnecessary processing.

---

## Limitations
1. Audible artifacts like popping may still occur in specific scenarios.
2. Further optimization might be needed for real-time applications.

---

## Credits
Developed by **Kris Cooper** as part of an audio processing project.