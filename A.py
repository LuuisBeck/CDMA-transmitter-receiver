import matplotlib.pylab as pyl
from transform import imageBW_to_bits, bits_to_imageBW
from cdma import from_bits_to_CDMA
import sounddevice as sd

def customModulation(ts, fc, bits):
    # this custom ASK modulation (amplitude-shift modulation) is for support
    # for CDMA, in this case: 0, -2, 2. Each number will have certain amplitude
    lenghtBits = len(bits)
    lenghtChunk = int(len(ts)/lenghtBits)
    A = []
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

## Transmitter code ##

#-----Transform images to bits-----#
# due to restrictions with cdma,
# images must be squared (16x16 or 40x40) and the same size.
file1 = 'f.png'
file2 = 'invader.png'
bits1 = imageBW_to_bits(file1)
bits2 = imageBW_to_bits(file2)

#-----bits to CDMA-----#
cdma = from_bits_to_CDMA(bits1, bits2)
print(cdma)

#-----Transmit CDMA via AM and OOK modulation-----#
# time between samples
sampling_period = 1/44100
# Time period
final = len(cdma)
print(final)
ts = pyl.arange(0, final, sampling_period)
# Carrier Frecuency
fc = 800

y = customModulation(ts, fc, cdma)
# Plotting results

fs = 44100
sd.play(y, fs, blocking=True)

pyl.plot(ts, y)
pyl.xlabel("tiempo (s)")
pyl.ylabel("Nivel de senal")
pyl.title("Senal enviada por transmisor")
pyl.show()


