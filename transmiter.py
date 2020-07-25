import matplotlib.pylab as pyl
import sounddevice as sd

# bits to send
bits = [2, 0, -2, 0, 0, 2, 2, 0]
# time between samples
sampling_period = 1/44100
# Time period
final_time = len(bits)/2
ts = pyl.arange(0, final_time, sampling_period)
lenghtChunk = 0
# Carrier Frecuency
fc = 800

def get_4PAM_modulation(ts, fc, bits):
    lenghtBits = len(bits)
    lenghtChunk = 2 * len(ts)//lenghtBits    # Chunks now are double sized
    A = []  # Amplitudes
    currentBit = 0
    while (currentBit < lenghtBits):
        oneBit = bits[currentBit]
        currentBit += 1
        anotherBit = bits[currentBit]
        currentBit += 1
        for j in range(lenghtChunk):
            A_for_current_bits = 0
            if (oneBit == 0 and anotherBit == 0):   # 00
                A_for_current_bits = 0
            elif (oneBit == 0 and anotherBit == 1): # 01
                A_for_current_bits = 0.5
            elif (oneBit == 1 and anotherBit == 0): # 10
                A_for_current_bits = 2
            else:                                   # 11
                A_for_current_bits = 4
            A.append(A_for_current_bits)
    return A * pyl.sin(2.0 * pyl.pi * fc * ts)

def getOOKModulation(ts, fc, bits):
    lenghtBits = len(bits)
    lenghtChunk = int(len(ts)/lenghtBits)
    A = []
    for i in range(lenghtBits):
        for j in range(lenghtChunk):
            A_for_Bit_i = bits[i]
            A.append(A_for_Bit_i)
    return A * pyl.sin(2.0 * pyl.pi * fc * ts)

def custom_modulation(fc, bits, add_first_bit):
    # this custom ASK modulation (amplitude-shift modulation) is for support
    # for CDMA, in this case: 0, -2, 2. Each number will have certain amplitude
    lenghtBits = len(bits)
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

ym = getOOKModulation(ts, fc, bits)
y_paso2 = get_4PAM_modulation(ts, fc, bits)
y_final = custom_modulation(fc, bits, add_first_bit=True)

#TODO: Need to transmit signal with sound
fs = 44100
sd.play(y_final, fs, blocking=True)

# Plotting results
pyl.plot(ts, y_final)
pyl.xlabel("tiempo (s)")
pyl.ylabel("Nivel de senal")
pyl.title("Senal enviada por transmisor")
pyl.show()