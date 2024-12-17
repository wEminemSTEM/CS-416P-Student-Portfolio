
# Butterfly Waveform Visualizer

## Overview
The **Butterfly Waveform Visualizer** is a Python program that generates a synchronized visual representation of audio input, forming a beautiful butterfly-shaped animation. The visualizer maps audio waveform data to a dynamic butterfly curve while applying vibrant, shifting colors to circles drawn in real time.

The visualization runs as the audio plays, with features such as adjustable circle counts and smooth color gradients that rotate across the spectrum over time.

---

## Features
- **Butterfly-Shaped Visualization**: The audio waveform data is visualized in a butterfly curve shape.
- **Dynamic Color Gradients**: Circles change color smoothly over time using HSV interpolation, cycling through the spectrum every 10 seconds.
- **Adjustable Circle Count**: Users can specify the number of circles displayed, ranging from 1 (default) to a maximum of 20.
- **Audio Playback Synchronization**: The visualization dynamically reacts to audio data during playback.
- **Window Fit**: The butterfly shape automatically scales to fit within 85% of the program window size.
- **Command-Line Options**: Flexible controls for circle count and help display.

---

## Requirements
- Python 3.9 or higher
- Required libraries:
  - `pygame`
  - `numpy`
  - `scipy`
  - `sounddevice`

You can install the dependencies using the following command:
pip install pygame numpy scipy sounddevice


---

## Usage
To run the program, navigate to the directory containing the `butterfly_visualizer.py` file and execute it using Python.

### Basic Command:
python butterfly_visualizer.py

This will run the program with the default circle count of **1**.

### Specify Number of Circles:
To change the number of circles (maximum 20), use the `-c` or `--circles` option:
python butterfly_visualizer.py -c 5

This will display **5 circles** in the visualization.

### Display Maximum Circle Limit:
To display the maximum number of circles allowed, use the `--max` option:
python butterfly_visualizer.py --max

The program will print:
>$ The maximum number of circles is 20.


---

## How It Works
1. **Audio Analysis**:
   - The program reads the specified WAV file and processes the audio data to extract waveform samples.
2. **Butterfly Curve**:
   - The waveform data is mapped onto a polar coordinate system, following the mathematical butterfly curve:
     ```
     r = e^cos(\theta) - 2cos(4\theta) + sin^5(\theta / 12)
     ```
3. **Dynamic Visualization**:
   - Multiple circles are drawn using the butterfly curve, with each circle slightly staggered and rotating in alternating directions.
   - Color gradients smoothly interpolate over time, creating a visually striking effect.
4. **Audio Synchronization**:
   - The visualization reacts to the peaks and amplitudes of the audio waveform data in real time.

---

## File Structure
- `butterfly_visualizer.py`: Main program file.
- `Boa - Duvet.wav`: Example audio file (replace with your own WAV file).

---

## Example
To visualize an audio file with **10 circles**, run the following command:
python butterfly_visualizer.py -c 10

The program will:
- Play the specified audio file.
- Display a synchronized butterfly waveform animation with 10 circles.

---

## Notes
- Only **WAV files** are supported as input. Replace the default file path with your own audio file in the program.
- For the best experience, ensure the program window is fully visible on your screen.
