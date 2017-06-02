import pyaudio
import numpy as np


p = pyaudio.PyAudio()

VOL = 0.5 ## in range [0.0, 1.0]
SAMPLING_RATE = 44100
DURATION = 1.0
FREQ = 432.0

samples = (np.sin(2 * np.pi * np.arrange(SAMPLING_RATE * DURATION) * FREQ / SAMPLING_RATE))\
    .astype(np.float32)

stream = p.open(format=pyaudio.paFloat32,
    channels=1, 
    rate=SAMPLING_RATE,
    output=True)

stream.write(VOL * SAMPLES)
stream.stop_stream()
stream.close()

p.terminate()
