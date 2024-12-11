# "Pop Music Generator"
# Bart Massey 2024
# Kris Cooper 2024
#
# This script puts out four bars in the "Axis Progression" chord loop,
# with a melody and bass line.

import argparse, random, re, wave
import numpy as np
import sounddevice as sd

# 11 canonical note names.
names = [ "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", ]
note_names = { s : i for i, s in enumerate(names) }

# Turn a note name into a corresponding MIDI key number.
# Format is name with optional bracketed octave, for example
# "D" or "Eb[5]". Default is octave 4 if no octave is
# specified.
note_name_re = re.compile(r"([A-G]b?)(\[([0-8])\])?")
def parse_note(s):
    m = note_name_re.fullmatch(s)
    if m is None:
        raise ValueError
    s = m[1]
    s = s[0].upper() + s[1:]
    q = 4
    if m[3] is not None:
        q = int(m[3])
    return note_names[s] + 12 * q

# Given a string representing a knob setting between 0 and
# 10 inclusive, return a linear gain value between 0 and 1
# inclusive. The input is treated as decibels, with 10 being
# 0dB and 0 being the specified `db_at_zero` decibels.
def parse_log_knob(k, db_at_zero=-40):
    v = float(k)
    if v < 0 or v > 10:
        raise ValueError
    if v < 0.1:
        return 0
    if v > 9.9:
        return 10
    return 10**(-db_at_zero * (v - 10) / 200)

# Given a string representing a knob setting between 0 and
# 10 inclusive, return a linear gain value between 0 and 1
# inclusive.
def parse_linear_knob(k):
    v = float(k)
    if v < 0 or v > 10:
        raise ValueError
    return v / 10

# Given a string representing an gain in decibels, return a
# linear gain value in the interval (0,1]. The input gain
# must be negative.
def parse_db(d):
    v = float(d)
    if v > 0:
        raise ValueError
    return 10**(v / 20)

# Added functions to generate different types of waves. Default is chosen at random.
def generate_sine_wave(frequency, duration, amplitude, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return amplitude * np.sin(2 * np.pi * frequency * t)

def generate_square_wave(frequency, duration, amplitude, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return amplitude * np.sign(np.sin(2 * np.pi * frequency * t))

def generate_triangle_wave(frequency, duration, amplitude, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return amplitude * (2 * np.abs(2 * ((t * frequency) % 1) - 1) - 1)

def generate_sawtooth_wave(frequency, duration, amplitude, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return amplitude * (2 * ((t * frequency) % 1) - 1)

# added time-sisgnature option to change that up
ap = argparse.ArgumentParser()
ap.add_argument('--bpm', type=int, default=90)
ap.add_argument('--samplerate', type=int, default=48_000)
ap.add_argument('--root', type=parse_note, default="C[5]")
ap.add_argument('--bass-octave', type=int, default=2)
ap.add_argument('--balance', type=parse_linear_knob, default="5")
ap.add_argument('--gain', type=parse_db, default="-3")
ap.add_argument('--output')
ap.add_argument('--waveform', type=str, default=random.choice(["sine", "square", "triangle", "sawtooth"]), choices=["sine", "square", "triangle", "sawtooth"], help="Waveform type (randomly chosen by default)")
ap.add_argument('--chord-loop', type=str, default=None, help="Custom chord progression, comma-separated scale degrees (random by default)")
ap.add_argument('--time-signature', type=str, default="4/4", help="Time signature in the format 'beats/measure' (e.g., '3/4', '5/4')")
ap.add_argument("--test", action="store_true", help=argparse.SUPPRESS)
args = ap.parse_args()

# Tempo in beats per minute.
bpm = args.bpm

# Audio sample rate in samples per second.
samplerate = args.samplerate

# Parse time signature.
time_signature = args.time_signature.split("/")
if len(time_signature) != 2:
    raise ValueError("Invalid time signature format. Use 'beats/measure'.")
beats_per_measure = int(time_signature[0])
measure_division = int(time_signature[1])

# Samples per beat. Changed considering option to swith time signature
beat_samples = int(np.round(samplerate / (bpm / 60)) * (beats_per_measure / measure_division))

# Relative notes of a major scale.
major_scale = [0, 2, 4, 5, 7, 9, 11]

# Major chord scale tones — one-based.
major_chord = [1, 3, 5]

# Given a scale note with root note 0, return a key offset
# from the corresponding root MIDI key.
def note_to_key_offset(note):
    scale_degree = note % 7
    return note // 7 * 12 + major_scale[scale_degree]

# Given a position within a chord, return a scale note
# offset — zero-based.
def chord_to_note_offset(posn):
    chord_posn = posn % 3
    return posn // 3 * 7 + major_chord[chord_posn] - 1

# MIDI key where melody goes.
melody_root = args.root

# Bass MIDI key is below melody root.
bass_root = melody_root - 12 * args.bass_octave

# Generate random chord progression if none is provided.
if args.chord_loop is None:
    chord_loop = random.sample(range(1, 8), 4)
else:
    chord_loop = list(map(int, args.chord_loop.split(",")))

# Initialize the global position variable.
position = 0

def pick_notes(chord_root, n=4):
    global position
    p = position

    notes = []
    for _ in range(n):
        chord_note_offset = chord_to_note_offset(p)
        chord_note = note_to_key_offset(chord_root + chord_note_offset)
        notes.append(chord_note)

        if random.random() > 0.5:
            p = p + 1
        else:
            p = p - 1

    position = p
    return notes

# Given a MIDI key number and an optional number of beats of
# note duration, return a waveform for that note.
def make_note(key, n=1):
    f = 440 * 2 ** ((key - 69) / 12)
    b = beat_samples * n
    duration = b / samplerate

    if args.waveform == "sine":
        return generate_sine_wave(f, duration, 1.0, samplerate)
    elif args.waveform == "square":
        return generate_square_wave(f, duration, 1.0, samplerate)
    elif args.waveform == "triangle":
        return generate_triangle_wave(f, duration, 1.0, samplerate)
    elif args.waveform == "sawtooth":
        return generate_sawtooth_wave(f, duration, 1.0, samplerate)

# Play the given sound waveform using `sounddevice`.
def play(sound):
    sd.play(sound, samplerate=samplerate, blocking=True)
        
# Unit tests, driven by hidden `--test` argument.
if args.test:
    note_tests = [
        (-9, -15),
        (-8, -13),
        (-7, -12),
        (-6, -10),
        (-2, -3),
        (-1, -1),
        (0, 0),
        (6, 11),
        (7, 12),
        (8, 14),
        (9, 16),
    ]

    for n, k in note_tests:
        k0 = note_to_key_offset(n)
        assert k0 == k, f"{n} {k} {k0}"

    chord_tests = [
        (-3, -7),
        (-2, -5),
        (-1, -3),
        (0, 0),
        (1, 2),
        (2, 4),
        (3, 7),
        (4, 9),
    ]

    for n, c in chord_tests:
        c0 = chord_to_note_offset(n)
        assert c0 == c, f"{n} {c} {c0}"

    exit(0)
    
# Stitch together a waveform for the desired music.
sound = np.array([], dtype=np.float64)
for c in chord_loop:
    notes = pick_notes(c - 1)
    melody = np.concatenate(list(make_note(i + melody_root) for i in notes))

    bass_note = note_to_key_offset(c - 1)
    bass = make_note(bass_note + bass_root, n=beats_per_measure)

    # Ensure melody and bass have the same length
    min_length = min(len(melody), len(bass))
    melody = melody[:min_length]
    bass = bass[:min_length]

    melody_gain = args.balance
    bass_gain = 1 - melody_gain

    sound = np.append(sound, melody_gain * melody + bass_gain * bass)

# Save or play the generated "music".
if args.output:
    output = wave.open(args.output, "wb")
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(samplerate)
    output.setnframes(len(sound))

    data = args.gain * 32767 * sound.clip(-1, 1)
    output.writeframesraw(data.astype(np.int16))

    output.close()
else:
    play(args.gain * sound)
