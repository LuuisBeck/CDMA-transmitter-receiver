import matplotlib.pylab as pyl
from transform import image_to_bits, bits_to_image
from cdma import from_bits_to_CDMA

def getOOKModulation(ts, fc, bits):
    lenghtBits = len(bits)
    lenghtChunk = int(len(ts)/lenghtBits)
    A = []
    for i in range(lenghtBits):
        for j in range(lenghtChunk):
            A_for_Bit_i = bits[i]   
            A.append(A_for_Bit_i)
    return A * pyl.sin(2.0 * pyl.pi * fc * ts)

## Transmitter code ##

#-----Transform images to bits-----#
# due to restrictions with cdma,
# images must be squared (16x16 or 40x40) and the same size.
file1 = 'f.png'
file2 = 'invader.png'
bits1 = image_to_bits(file1)
bits2 = image_to_bits(file2)

#-----bits to CDMA-----#
cdma = from_bits_to_CDMA(bits1, bits2)

#-----Transmit CDMA via AM and OOK modulation-----#
# time between samples
sampling_period = 0.0000226758
# Time period
final = len(cdma)
ts = pyl.arange(0, final, sampling_period)
# Carrier Frecuency
fc = 800

y = getOOKModulation(ts, fc, cdma)
# Plotting results
pyl.plot(ts, y)
pyl.xlabel("tiempo (s)")
pyl.ylabel("Nivel de senal")
pyl.title("Senal enviada por transmisor")
pyl.show()


