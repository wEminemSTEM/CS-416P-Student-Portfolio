# popgen: play a pop music loop
Bart Massey 2024

This Python program generates a pseudo-melody using chord
and bass notes from the [Axis
Progression](https://en.wikipedia.org/wiki/axis_progression).

Right now, the controls are limited and the output is pretty
terrible.

A sample is available in [`demo.wav`](demo.wav).

# License

This work is licensed under the "MIT License". Please see the file
`LICENSE.txt` in this distribution for license terms.

# Updates by Kris Cooper

This project has been extended to support a variety of new features and enhancements:
## New Features

1. **Waveform Options**:
   - Added support for sine, square, triangle, and sawtooth waveforms.
   - The waveform is chosen randomly by default or specified using the `--waveform` argument (e.g., `--waveform square`).

2. **Custom and Randomized Chord Progressions**:
   - Specify custom chord progressions using the `--chord-loop` argument (e.g., `--chord-loop 1,5,6,4`).
   - If no progression is provided, the program randomly generates a new one.

3. **Dynamic Time Signatures**:
   - Supports custom time signatures specified via `--time-signature` (e.g., `--time-signature 3/4` or `--time-signature 5/8`).
   - Automatically adjusts the melody and bass to match the specified beats per measure and note duration.

## Tips for Running the Program

- Install dependencies:
  pip install numpy sounddevice
  
- Example command to generate a 5/4 loop with a sawtooth waveform:
  python popgen.py --time-signature 5/4 --waveform sawtooth --chord-loop 1,4,5,2

- To play a random chord progression with a default time signature (4/4):
  python popgen.py

- Save output to a WAV file:
  python popgen.py --output output.wav
