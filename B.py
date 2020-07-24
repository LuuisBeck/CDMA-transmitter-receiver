from transform import bits_to_imageBW
from cdma import from_CDMA_to_bits

## RECEIVER ##

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
        mean = pyl.mean(allDataInCurrentChunk)
        print(mean)
        currentBit = 0

        # WARNING: This values depends on device types 
        #          and volume used.
        minForBit2 = 5
        minForBit_2 = 1
        if (mean >= minForBit2):
            currentBit = 2
        elif (mean >= minForBit_2 and mean < minForBit2):
            currentBit = -2
        else:
            currentBit = 0
        bitsReceived.append(currentBit)
        currentChunk += 1
    return bitsReceived

# This is from: 
#   2 images of 16x16 in one channel = 512
#   bits to know size of each image  = 16 
#                              TOTAL = 272
lenghtBits = 544

duration = 8.0 #seconds
fs = 44100

# Wait until transmiter begin to play sound, its more like 0.3 seconds
# time.sleep(0.2)
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

sampling_period = 1/fs
final = int(lenghtBits/2)
ts = pyl.arange(0, final, sampling_period)

# Plotting received data
pyl.plot(ts, myrecording)
pyl.title("Senal recibida por receiver")
pyl.xlabel("Tiempo (s)")
pyl.ylabel("Nivel de senal")
pyl.show()

# Demodulation of received data
originalBits = custom_demodulation(ts, myrecording)

# split up data
[bits1, bits2] = from_CDMA_to_bits(originalBits)

# converting bits to image
bits_to_imageBW(bits1, "result_1")
bits_to_imageBW(bits2, "result_2")