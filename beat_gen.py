# Copyright (c) 2017, Albert Brox III
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
