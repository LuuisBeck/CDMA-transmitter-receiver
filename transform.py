import cv2
from PIL import Image
import numpy as np

def intTo8bitsArray(number):
    result = []
    string = "{0:08b}".format(number)
    for c in string:
        result.append(int(c))
    return result

#-----------Conversion Imagen a bits-----------#
def image_to_bits(name_file):
    # Abrimos imagen
    img = Image.open(name_file)

    # Convertimos el input en un array
    np_img = np.array(img)

    # Obtenemos el width y height a partir del array
    height = len(np_img)
    width = len(np_img[0])
    print(f"{width} x {height}")


    fullArrayBits = []

    # Primeros 16 bits, indican tamano de width y height respectivamente
    # WARNING: El limite del tamano de la imagen debe ser de 255 x 255,
    #          solo asi el programa puede saber el tamano de la imagen al recibir los bits
    arrayWidth = intTo8bitsArray(width)
    arrayHeight = intTo8bitsArray(height)
    fullArrayBits += arrayWidth
    fullArrayBits += arrayHeight

    # Convertimos cada R, G y B en binario con 8 bits cada uno
    for x in range(height):
        for y in range(width):
            value = np_img[x][y]
            r = value[0]
            g = value[1]
            b = value[2]
            r_binary = intTo8bitsArray(r)
            g_binary = intTo8bitsArray(g)
            b_binary = intTo8bitsArray(b)
            fullArrayBits += r_binary
            fullArrayBits += g_binary
            fullArrayBits += b_binary

    return fullArrayBits

def imageBW_to_bits(name_file):
    # Abrimos imagen
    img = Image.open(name_file)

    # Convertimos el input en un array
    np_img = np.array(img)

    # Obtenemos el width y height a partir del array
    height = len(np_img)
    width = len(np_img[0])
    print(f"{width} x {height}")


    fullArrayBits = []

    # Primeros 16 bits, indican tamano de width y height respectivamente
    # WARNING: El limite del tamano de la imagen debe ser de 255 x 255,
    #          solo asi el programa puede saber el tamano de la imagen al recibir los bits
    arrayWidth = intTo8bitsArray(width)
    arrayHeight = intTo8bitsArray(height)
    fullArrayBits += arrayWidth
    fullArrayBits += arrayHeight

    # Convertimos cada R, G y B en binario con 8 bits cada uno
    for x in range(height):
        for y in range(width):
            value = np_img[x][y]
            r = value[0]
            g = value[1]
            b = value[2]
            if (r > 128 and g > 128 and b > 128):
                # white pixel
                fullArrayBits.append(1)
            elif (r <= 128 and g <= 128 and b <= 128):
                # black pixel
                fullArrayBits.append(0) 
    return fullArrayBits
    


#-----------Conversion bits a Imagen-----------#
def bits_to_image(fullArrayBits, name_for_file):
    # Los primeros 16 bits son el tamano en width y height respectivamente
    width = 0
    height = 0
    str_width = ''
    str_height = ''
    for i in range(8):
        str_width += str(fullArrayBits[i])
        str_height += str(fullArrayBits[i + 8])
    width = int(str_width, 2) # Convertimos a int
    height = int(str_height, 2) # Convertimos a int

    # Creamos matriz para guardar valor de RGB de la imagen
    img = np.zeros((height,width,3),np.uint8)
    totalPixeles = width*height
    x = 0
    y = 0

    # Obtenemos cada pixel dentro del array de bits
    for pixel in range(totalPixeles):
        # Cada pixel tendrá 24 bits. 8 para R, 8 para G y 8 para B
        init = 0 + 24*pixel
        final = 8 + 24*pixel
        r = 0
        g = 0
        b = 0
        str_r = ''
        str_g = ''
        str_b = ''
        for i in range(init, final):
            str_r += str(fullArrayBits[i])
            str_g += str(fullArrayBits[i + 8])
            str_b += str(fullArrayBits[i + 16])
        # Convertimos a int los valores de RGB
        r = int(str_r, 2) 
        g = int(str_g, 2)
        b = int(str_b, 2)
        # Guardamos el valor del pixel en su posicion correspondiente en la matriz nueva
        img[x, y] = [r, g, b]
        y += 1
        if (y >= width):
            y = 0
            x += 1

    print(totalPixeles)
    print(f"{width} x {height}")

    # Guardamos imagen recibida en un nuevo archivo
    cv2.imwrite(f"{name_for_file}.png", img)
    result = Image.open(f"{name_for_file}.png")
    result.show()

def bits_to_imageBW(fullArrayBits, name_for_file):
    # Los primeros 16 bits son el tamano en width y height respectivamente
    width = 0
    height = 0
    str_width = ''
    str_height = ''
    for i in range(8):
        str_width += str(fullArrayBits[i])
        str_height += str(fullArrayBits[i + 8])
    width = int(str_width, 2) # Convertimos a int
    height = int(str_height, 2) # Convertimos a int

    # Creamos matriz para guardar valor de RGB de la imagen
    img = np.zeros((height,width,3),np.uint8)
    totalPixeles = width*height
    x = 0
    y = 0

    # Obtenemos cada pixel dentro del array de bits
    for pixel in range(totalPixeles):
        # Cada pixel tiene 1 bit:
        #   1 -> pixel blanco
        #   0 -> pixel negro
        pixel = fullArrayBits[pixel]
        if (pixel > 0):
            # Guardamos el valor del pixel
            img[x, y] = [255, 255, 255]
        else:
            img[x, y] = [0, 0, 0]
        y += 1
        if (y >= width):
            y = 0
            x += 1

    print(totalPixeles)
    print(f"{width} x {height}")

    # Guardamos imagen recibida en un nuevo archivo
    cv2.imwrite(f"{name_for_file}.png", img)
    result = Image.open(f"{name_for_file}.png")
    result.show()