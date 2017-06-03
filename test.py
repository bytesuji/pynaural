import pyaudio
import struct
import numpy as np


p = pyaudio.PyAudio()

VOL = 0.5 ## in range [0.0, 1.0]
SAMPLING_RATE = 44100
FREQ = 432.0
DURATION = int(input("Duration? "))

samples = (np.sin(2 * np.pi * np.arange(SAMPLING_RATE * DURATION) * FREQ / SAMPLING_RATE))\
    .astype(np.float32)

stream = p.open(format=pyaudio.paFloat32,
    channels=2, 
    rate=SAMPLING_RATE,
    output=True)

left_chunk = (np.sin(np.arange(SAMPLING_RATE * DURATION) * FREQ / SAMPLING_RATE)).astype(np.float32)
right_chunk = (np.sin(np.arange(SAMPLING_RATE * DURATION) * (FREQ + 10) / SAMPLING_RATE)).astype(np.float32)

# print("left_chunk:", left_chunk)
# print("right_chunk:", right_chunk)

# assert len(left_chunk) == len(right_chunk)
# for i in range(len(left_chunk)):
#     stream_data = struct.pack("2f", left_chunk[i] * VOL, right_chunk[i] * VOL)
# 
# print("stream_data:", stream_data)

stereo = pack('<' + 2 * SAMPLING_RATE * 'l', )

stream.write(stereo)
stream.stop_stream()
stream.close()

p.terminate()
