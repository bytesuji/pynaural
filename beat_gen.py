import time
import sounddevice as sd
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
        waveform = np.sin(np.arange(self.sampling_rate) * scale) ## generate a one-second snippet

        chunks = [waveform]
        chunk = np.concatenate(chunks)

        return chunk

    def play(self):
        """Plays the binaural beat according to the settings with which the class was instantiated. 
        Instead of generating a chunk which is the same duration as the user requested, this method
        generates a one-second snippet w/ the requested frequencies and then plays that snippet 
        in an infinite loop, time.sleeps for the requested duration, then stops all audio output."""

        left = self.create_chunk('l')
        right = self.create_chunk('r')
        stereo = np.array([left, right]).transpose()
        stereo *= self.vol

        sd.default.channels = 2

        if self.duration is -1:
            sd.play(stereo, self.sampling_rate, loop=True)
        else:
            sd.play(stereo, self.sampling_rate, loop=True)
            try:
                time.sleep(self.duration)
            except ValueError:
                self.duration = abs(self.duration)
                self.play()
            sd.stop()

    def pause(self):
        sd.stop()
