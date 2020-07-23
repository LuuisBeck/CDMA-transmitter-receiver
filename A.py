from transform import image_to_bits, bits_to_image
from cdma import from_bits_to_CDMA
## Transmitter

# Transform images to bits
# due to restrictions with cdma,
# images must be squared (16x16 or 40x40) and the same size.
file1 = 'winter.png'
file2 = 'animal_crossing.png'
bits1 = image_to_bits(file1)
bits2 = image_to_bits(file2)

# bits to CDMA
cdma = from_bits_to_CDMA(bits1, bits2)

