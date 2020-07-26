import matplotlib.pylab as pyl
from transform import imageBW_to_bits
from cdma import from_bits_to_CDMA
import sounddevice as sd
import time

# time between samples
sampling_period = 1/44100
# Time period
final_time = 0
ts = pyl.arange(0, final_time, sampling_period)
lenghtChunk = 0

## TRANSMITTER  ##
start = time.time()
def custom_modulation(fc, bits, add_first_bit):
    # this custom ASK modulation (amplitude-shift modulation) is for support
    # for CDMA, in this case: 0, -2, 2. Each number will have certain amplitude
    lenghtBits = len(bits)
    print(lenghtBits)
    final_time = lenghtBits / 2
    global ts
    ts = pyl.arange(0, final_time, sampling_period)
    global lenghtChunk
    lenghtChunk = int(len(ts)/lenghtBits)
    print(len(ts))
    global A
    A = []
    if (add_first_bit):
        # When add_first_bit is activated, a "2" bit is added
        # at the beginning of the data
        ts = pyl.arange(0, final_time + 0.5, sampling_period)
        for j in range(lenghtChunk):
            A.append(5)
    for i in range(lenghtBits):
        for j in range(lenghtChunk):
            A_for_Bit_i = 0
            if (bits[i] == 0):
                A_for_Bit_i = 0
            elif (bits[i] == 2):
                A_for_Bit_i = 5
            elif (bits[i] == -2):
                A_for_Bit_i = 1
            A.append(A_for_Bit_i)
    return A * pyl.sin(2.0 * pyl.pi * fc * ts)

#-----Transform images to bits-----#
# due to restrictions with cdma,
# images must be squared and 16x16
file1 = 'f.png'
file2 = 'invader.png'
bits1 = imageBW_to_bits(file1)
bits2 = imageBW_to_bits(file2)
print(bits1)
print(bits2)

#-----bits to CDMA-----#
cdma = from_bits_to_CDMA(bits1, bits2)

#-----Transmit CDMA via AM and custom modulation-----#
# time between samples
sampling_period = 1/44100
# Time period (2 "bits" per second)
final = int(len(cdma)/2)
ts = pyl.arange(0, final, sampling_period)
# Carrier Frecuency
fc = 800

y = custom_modulation(fc, cdma, True)

# Transmission of data
fs = 44100
end = time.time()
print(f"elasped time before sound transmission: {end - start} seconds")
sd.play(y, fs, blocking=True)

# Plotting results
pyl.plot(ts, y)
pyl.xlabel("tiempo (s)")
pyl.ylabel("Nivel de senal")
pyl.title("Senal enviada por transmisor")
pyl.show()


