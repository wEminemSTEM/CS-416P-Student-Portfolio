11/04/24
Lets make some sounds!? The first project assignment is titled "Clipped". Notes from the assignment description contain a description of the WAVE (Waveform) or WAV audio file format. 
Per Wikipedia, published in 1991 by iBM and microsoft and can contain compressed or uncompressed audio.
Heres a breakdown of the WAV file format:
  1. Header:
    1.  Sample size and format
    2.  Number of channels
    3.  Sample rate
    4.  Number of frames in the file
    5.  Some other useful stuff
  2.  Audio Samples
  3.  "Some sort of checksum to check data integrity" - What the heck does this mean?
    -  Checksum - block of data obtained from another block of data used for the purpose of determining if data has somehow been altered during transmission/storage.

Assignment suggests using an existing library for reading and writting WAV files (As it's apparently very error prone) 
What are some libraries that can achieve this? Conviniently, python has a Wave module for doing exactly that. I guess I'll start there. 

Assignment objective:
Write a program that writes a sine wave to a wav file "sine.wav" with the following specifications:
  Channels per frame: 1 (mono)
  Sample format: 16 bit signed (values in the range -32767..32767)
  Amplitude: ¼ maximum possible 16-bit amplitude (values in the range -8192..8192)
  Duration: one second
  Frequency: 440Hz (440 cycles per second)
  Sample Rate: 48000 samples per second
