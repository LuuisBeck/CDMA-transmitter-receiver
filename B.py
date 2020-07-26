from transform import bits_to_imageBW
from cdma import from_CDMA_to_bits
import matplotlib.pylab as pyl
import sounddevice as sd
import time

## RECEIVER ##
def cut_unused_data(data):
    # cut recording until first bit appers
    initial = 0
    result = []
    first_bit = False
    while(not first_bit):
        currentData = data[initial]
        if (currentData > 0.09):
            first_bit = True
            result = myrecording[initial:]
        else:
            initial += 1
    return result

def custom_demodulation(ts, myrecording, lenghtBits):
    # this custom ASK modulation (amplitude-shift modulation)
    # is to support CDMA, in this case: 0, -2, 2. Each number will have certain amplitude
    lenghtOneChunk = int(len(ts)/ lenghtBits)
    bitsReceived = []
    currentChunk = 0

    for i in range(lenghtBits):
        allDataInCurrentChunk = []
        for j in range(lenghtOneChunk):
            currentData = myrecording[j + (currentChunk * lenghtOneChunk)]
            positiveValue = abs(currentData)
            allDataInCurrentChunk.append(positiveValue)
        median = pyl.median(allDataInCurrentChunk)
        currentBit = 0

        # WARNING: This values depends on device types
        #          and volume used.
        minForBit2 = 0.09
        minForBit_2 = 0.03
        if (median >= minForBit2):
            currentBit = 2
        elif (median >= minForBit_2 and median < minForBit2):
            currentBit = -2
        else:
            currentBit = 0
        bitsReceived.append(currentBit)
        currentChunk += 1
    return bitsReceived

# This is from: 
# first bit to get when data start   = 1
#   2 images of 16x16 in one channel = 512
#   bits to know size of each image  = 16 
#                              TOTAL = 272
lenghtBits = 545

duration = 280 #seconds
fs = 44100

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

sampling_period = 1/fs
final = lenghtBits/2
ts = pyl.arange(0, final, sampling_period)

data = cut_unused_data(myrecording)
plot_x = pyl.arange(0, len(data)*sampling_period, sampling_period)

# Demodulation of received data
originalBits = custom_demodulation(ts, data, lenghtBits)

# Plotting received data
pyl.plot(plot_x, data)
pyl.title("Senal recibida por receiver")
pyl.xlabel("Tiempo (s)")
pyl.ylabel("Nivel de senal")
pyl.show()

# delete first bit
originalBits = originalBits[1:]

# split up data
[bits1, bits2] = from_CDMA_to_bits(originalBits)
print(bits1)
print(bits2)


# converting bits to image
bits_to_imageBW(bits1, "result_1")
bits_to_imageBW(bits2, "result_2")