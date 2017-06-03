import struct
import pyaudio
import numpy as np


class BeatGenerator(object):
    def __init__(self, vol=0.5, carrier=400, beat_freq=15.0, duration=10, sampling_rate=44100):
        """`vol` is self-explanatory. `carrier` is the frequency (in Hz) played through the 
        left channel; the frequency played through the right is equivalent to `carrier + beat_freq`.
        `sampling_rate` probably will never be needed."""
        self.vol = vol
        self.duration = duration
        self.carrier = carrier
        self.beat_freq = beat_freq
        self.sampling_rate = sampling_rate

        self.frequencies = (self.carrier, self.carrier + self.beat_freq)

        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=pyaudio.paFloat32, channels=2,
            rate=self.sampling_rate, output=1)

    def create_chunk(self, channel):
        """Makes a `chunk` (audio data in byte format) based on the given channel.
        Takes a char as arg, returns an np.array (char must be in ('l', 'r'))"""
        if channel == 'l':
            freq = self.frequencies[0]
        elif channel == 'r':
            freq = self.frequencies[1]
        else:
            raise AttributeError("Invalid channel.")

        scale = float(freq) * 2 * np.pi / self.sampling_rate
        waveform = np.sin(np.arange(self.sampling_rate * self.duration) * scale)
        chunks = [waveform]
        chunk = np.concatenate(chunks)

        return chunk

    def write_stream(self, stream):
        """Relatively self-explanatory function. `stream` must be a pyaudio stream."""
        try:
            left = self.create_chunk('l')
            right = self.create_chunk('r')

            for i in range(len(left)):
                stereo = struct.pack("2f", left[i] * self.vol, right[i] * self.vol)
                stream.write(stereo)
        except OSError:
        ## This try-except block is to keep the program from throwing errors when the stop button is pressed, 
        ## as doing so produces a totally harmless OSError (still not something you want the end user seeing,
        ## though.
            pass

    def play(self):
        """Plays the binaural beat with which the class was instantiated."""
        self.write_stream(self.stream)
        self.stream.stop_stream()

    def pause(self):
        self.stream.stop_stream()
