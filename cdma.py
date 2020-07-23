def toAnalogic(array):
    for i in range(len(array)):
        if (array[i] == 0):
            array[i] = -1

def getSequence(bits, key):
    sequence = []
    for b in bits:
        for j in key:
            partialResult = b*j
            sequence.append(partialResult)
    return sequence

def decodeData(bits, key):
    result = []
    partialResult = 0
    indexKey = 0
    for i in range(len(bits)):
        partialResult += (bits[i] * key[indexKey])
        indexKey += 1
        if (indexKey > len(key) - 1):
            indexKey = 0
            result.append(partialResult)
            partialResult = 0
    return result

def toDigital(bits):
    for i in range(len(bits)):
        if bits[i] > 0:
            bits[i] = 1
        elif bits[i] < 0:
            bits[i] = 0
        else:
            print("ERROR: llaves deben ser ortogonales")

#---------Codificar bits a emitir---------#
def from_bits_to_CDMA(b1, b2):
    # Tenemos 2 usuarios con una llave de 2 chips cada uno
    # (llaves ortogonales)
    k1 = [0, 1]
    k2 = [1, 1]

    # Secuencias de bits de cada usuarios
    # lo dejaremos en largo 8 por conveniencia
    #b1 = [0, 1, 1, 1, 0, 0, 1, 0]
    #b2 = [1, 0, 0, 1, 0, 1, 0, 1]

    # Transformamos todo a analógico
    toAnalogic(k1)
    toAnalogic(k2)
    toAnalogic(b1)
    toAnalogic(b2)

    # Obtenemos secuencia transmitida multiplicando por la llave
    s1 = getSequence(b1, k1)
    s2 = getSequence(b2, k2)

    # Luego, las señales se mezclan:
    sT = []
    for i in range(len(s1)):    # se puede usar s1 o s2
        bit = s1[i] + s2[i]
        sT.append(bit)
    
    return sT

#---------Recepción y decodificación---------#5
def from_CDMA_to_bits(sT):
    # Cada receptor tiene su propia llave (k1, k2),
    # con la que se decodifican los datos
    result1 = decodeData(sT, k1)
    result2 = decodeData(sT, k2)

    # Pasamos a digital:
    #   Si bit es mayor a cero -> 1 
    #   Si es menor a cero -> 0
    #   Si es cero -> ERROR
    toDigital(result1)
    toDigital(result2)

    print(result1)
    print(result2)