import sounddevice as sd
import matplotlib.pylab as pyl
import time

def getOriginalBits_OOKMod(ts, myrecording):
    lenghtBits = 8
    lenghtOneChunk = len(ts)/ lenghtBits
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

def getOriginalBits_4PAM(ts, myrecording):
    lenghtBits = 4
    lenghtOneChunk = len(ts) / lenghtBits
    bitsReceived = []
    currentChunk = 0
    for i in range(lenghtBits):
        allDataInCurrentChunk = []
        for j in range(lenghtOneChunk):
            currentData = myrecording[j + (currentChunk * lenghtOneChunk)]
            positiveValue = abs(currentData)
            allDataInCurrentChunk.append(positiveValue)
        '''chunkInsideChunkTofindMean = []
        for z in range(lenghtOneChunk / 3):
            currentData = allDataInCurrentChunk[z + (lenghtOneChunk / 3)]
            chunkInsideChunkTofindMean.append(currentData)
        '''
        mean = pyl.mean(allDataInCurrentChunk)
        print(mean)
        currentBit = 0
        if (mean < 0.05):
            bitsReceived.append(0)
            bitsReceived.append(0)
        elif (mean > 0.05 and mean < 0.1):
            bitsReceived.append(0)
            bitsReceived.append(1)
        elif (mean > 0.1 and mean < 0.2):
            bitsReceived.append(1)
            bitsReceived.append(0)
        elif (mean > 0.2):
            bitsReceived.append(1)
            bitsReceived.append(1)
        currentChunk += 1
    return bitsReceived

# Main code
duration = 8.0 #seconds
fs = 44100

# Wait until transmiter begin to play sound, its more like 0.3 seconds
# time.sleep(0.2)
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

ts = pyl.arange(0, 8, 0.0000226758)

originalBits = getOriginalBits_4PAM(ts, myrecording)
print(originalBits)

pyl.plot(ts, myrecording)
pyl.title("Senal recibida por receiver")
pyl.xlabel("Tiempo (s)")
pyl.ylabel("Nivel de senal")
pyl.show()