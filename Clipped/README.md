
# Clipped Project

## Author
Kris Cooper

## Description
This project demonstrates the generation, manipulation, and playback of WAV audio files using Python. Specifically, the program:
1. Creates a pure sine wave (`sine.wav`).
2. Creates a clipped sine wave (`clipped.wav`).
3. Plays the clipped sine wave directly on the system's audio output.

## Features
- **Sine Wave Generation**: A single-channel sine wave with 16-bit signed samples, 440Hz frequency, 48kHz sample rate, and 1/4 maximum amplitude.
- **Clipped Wave Generation**: A sine wave with clipping applied at +/- 1/4 maximum amplitude, resulting in distortion.
- **Audio Playback**: Direct playback of the clipped sine wave using the `sounddevice` library.
- **Pause Functionality**: Includes a 2-second pause in the program for better user experience.

## Technologies Used
- **Python 3.9 or later**
- **Libraries**:
  - `numpy`: For mathematical operations and wave generation.
  - `scipy.io.wavfile`: For writing WAV files.
  - `sounddevice`: For audio playback.

## Installation
Install the required libraries using pip:
```bash
pip install numpy scipy sounddevice
```

## How to Run
1. Save the project files to your local machine.
2. Run the program using Python:
```bash
python audio_system.py
```
3. Outputs will include two WAV files:
   - `sine.wav`: Pure sine wave.
   - `clipped.wav`: Clipped sine wave.

## Usage Example
- The generated WAV files can be opened in audio editing tools like Audacity for inspection.
- The clipped sine wave will also play directly after program execution.

## Known Issues
- None identified at this time.

## Future Enhancements
- Implement real-time audio manipulation.
- Allow user-defined parameters (frequency, amplitude, duration) through a command-line interface.

