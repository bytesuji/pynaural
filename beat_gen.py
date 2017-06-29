import time
import sounddevice as sd
import numpy as np


class BeatGenerator(object):
    def __init__(self, vol=0.5, carrier=400, beat_freq=15.0, duration=10, sampling_rate=44100):
        self.vol = vol
        self.duration = duration
        self.carrier = carrier
        self.beat_freq = beat_freq
        self.sampling_rate = sampling_rate

        self.frequencies = (self.carrier, self.carrier + self.beat_freq)

    def create_chunk(self, channel):
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
        left = self.create_chunk('l')
        right = self.create_chunk('r')
        stereo = np.array([left, right]).transpose()
        stereo *= self.vol

        sd.default.channels = 2

        sd.play(stereo, self.sampling_rate, loop=True)
        if self.duration is not -1:
            try: time.sleep(self.duration)
            except ValueError:
                self.duration = abs(self.duration)
                self.play()
            sd.stop()

    def pause(self):
        sd.stop()
