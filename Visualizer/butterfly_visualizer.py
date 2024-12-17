#   <Kris Cooper, Portland State University, Fall 24, 962413911>
#   CS416P  Comp, Sound, and Music final proj:
#   Visualizer

import argparse
import scipy.io.wavfile as wavfile
import numpy as np
import pygame
import sounddevice as sd
import os
import math

FILE_NAME = "Boa - Duvet.wav"  # Replace with your WAV file

def analyze_audio(filename, fft_size=1024):
    # Read the audio file
    sample_rate, data = wavfile.read(filename)
    if len(data.shape) > 1:  # If stereo, take one channel
        data = data[:, 0]
    return sample_rate, data

def interpolate_color_hsv(frame_index, total_frames, speed=10):
    # Generate a color from HSV spectrum cycling over time (10-second full rotation)
    hue = (frame_index / (speed * 30)) % 1.0  # 30 FPS, full rotation in 10 seconds
    color = pygame.Color(0)
    color.hsva = (hue * 360, 100, 100, 100)
    return color.r, color.g, color.b

def butterfly_radius(theta, scale):
    # Butterfly curve equation for radius, scaled for window confinement
    return (math.exp(math.cos(theta)) - 2 * math.cos(4 * theta) + math.sin(theta / 12) ** 5) * scale

def music_painter(sample_rate, audio_data, max_circles=1):
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Butterfly Waveform Visualizer")
    clock = pygame.time.Clock()
    center_x, center_y = screen_width // 2, screen_height // 2  # Center of the window

    # Start audio playback
    sd.play(audio_data, samplerate=sample_rate)

    frame_index = 0
    running = True
    total_frames = len(audio_data)
    points = []  # Points to store the butterfly waveform path
    circle_count = min(max_circles, 20)  # Limit circles to a maximum of 20

    # Normalize audio data for visualization
    max_amplitude = np.max(np.abs(audio_data))
    normalized_data = audio_data / max_amplitude

    # Adjust scale to cap the butterfly within 85% of the window dimensions
    scale_factor = min(screen_width, screen_height) * 0.21375  # 85% of the smaller window dimension

    # Rotation direction and stagger offsets for each circle
    rotations = [(-1) ** i for i in range(circle_count)]
    stagger_offsets = [i * (2 * np.pi / circle_count) for i in range(circle_count)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        samples_per_frame = 1024
        start = frame_index * samples_per_frame
        end = start + samples_per_frame

        if end > len(normalized_data):
            break  # Stop if we reach the end of the audio

        current_samples = normalized_data[start:end]

        # Draw each circle following the butterfly curve
        for circle_index in range(circle_count):
            # Gradient color over time (each circle rotates independently)
            current_color = interpolate_color_hsv(frame_index + circle_index * 100, total_frames)

            # Map samples to butterfly polar coordinates with rotation and stagger
            num_samples = len(current_samples)
            points.clear()
            for i, sample in enumerate(current_samples):
                theta = (2 * np.pi * i) / num_samples + stagger_offsets[circle_index] + rotations[circle_index] * (frame_index * 0.01)
                butterfly_r = butterfly_radius(theta, scale_factor)  # Scale for window confinement
                offset_radius = butterfly_r + sample * (scale_factor * 0.2)  # Adjust peaks based on amplitude
                x = center_x + int(offset_radius * math.sin(theta))  # Swap cos and sin to rotate 90 degrees
                y = center_y - int(offset_radius * math.cos(theta))  # Correct orientation for 90-degree rotation
                points.append((x, y))

            # Draw the butterfly-shaped waveform
            if len(points) > 1:
                pygame.draw.lines(screen, current_color, True, points, 2)

        # Update the display
        pygame.display.flip()

        # Update frame index
        frame_index += 1

        # Maintain 30 FPS
        clock.tick(30)

    sd.stop()  # Stop audio playback
    pygame.quit()

def main():
    # Argument parser for command-line options
    parser = argparse.ArgumentParser(description="Butterfly Waveform Visualizer")
    parser.add_argument("-c", "--circles", type=int, default=1, help="Number of circles to display (max 20)")
    parser.add_argument("--max", action="store_true", help="Display the maximum number of circles")
    args = parser.parse_args()

    if args.max:
        print("The maximum number of circles is 20.")
        return

    # Load and analyze the audio file
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILE_NAME)
    sample_rate, audio_data = analyze_audio(file_name)

    # Launch the synchronized visualizer
    music_painter(sample_rate, audio_data, max_circles=args.circles)

if __name__ == "__main__":
    main()
