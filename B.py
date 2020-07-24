from transform import bits_to_imageBW

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
        if (mean > 0.1):
            currentBit = 1
        else:
            currentBit = 0
        bitsReceived.append(currentBit)
        currentChunk += 1
    return bitsReceived

# This is the from: 
#   2 images of 16x16 in one channel = 256
#   bits to know size of images      = 16 
#                              TOTAL = 272
lenghtBits = 272

duration = 8.0 #seconds
fs = 44100

# Wait until transmiter begin to play sound, its more like 0.3 seconds
# time.sleep(0.2)
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

ts = pyl.arange(0, 8, 1/fs)

originalBits = getOriginalBits_4PAM(ts, myrecording)
print(originalBits)

pyl.plot(ts, myrecording)
pyl.title("Senal recibida por receiver")
pyl.xlabel("Tiempo (s)")
pyl.ylabel("Nivel de senal")
pyl.show()


bits_to_imageBW(bits1, "result_1")
bits_to_imageBW(bits2, "result_2")