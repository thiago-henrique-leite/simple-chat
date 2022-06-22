import math

class CBC:
  P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
  P8 = [6, 3, 7, 4, 8, 5, 10, 9]
  IP = [2, 6, 3, 1, 4, 8, 5, 7]
  PI = [4, 1, 3, 5, 7, 2, 8, 6]
  EX = [4, 1, 2, 3, 2, 3, 4, 1]
  P4 = [2, 4, 3, 1]

  S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2],
  ]

  S1 = [
    [1, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3],
  ]


  def __init__(self, message, key):
    self.message = message
    self.key = key

  def encrypt(message, key):
    try:
      return CBC(message, key).perform_encrypt()
    except:
      return message

  def decrypt(message, key):
    try:
      return CBC(message, key).perform_decrypt()
    except:
      return message

  def perform_encrypt(self):
    p10 = self.permuttation(self.key, self.P10)

    left, rigth = self.rotate(p10[0:5], 1), self.rotate(p10[5:10], 1)

    k1 = self.permuttation(left + rigth, self.P8)
    k2 = self.permuttation(self.rotate(left, 2) + self.rotate(rigth, 2), self.P8)

    msg_binary = self.convert_binary_to_array(self.convert_message_to_binary(self.message))

    message = self.xor(msg_binary[0], '10101010')

    msg_encrypted = self.permuttation(self.f_function(self.swap(self.f_function(self.permuttation(message, self.IP), k1)), k2), self.PI)
    msg_encrypted = [msg_encrypted]

    for i in range(1, len(msg_binary)):
      message = self.xor(msg_binary[i], msg_encrypted[i-1])

      msg_encrypted.append(self.permuttation(self.f_function(self.swap(self.f_function(self.permuttation(message, self.IP), k1)), k2), self.PI))

    return ''.join(msg_encrypted)

  def perform_decrypt(self):
    p10 = self.permuttation(self.key, self.P10)

    left, rigth = self.rotate(p10[0:5], 1), self.rotate(p10[5:10], 1)

    k1 = self.permuttation(left + rigth, self.P8)
    k2 = self.permuttation(self.rotate(left, 2) + self.rotate(rigth, 2), self.P8)

    msg_encrypted = self.convert_binary_to_array(self.message)
    msg_decrypted = self.xor(self.permuttation(self.f_function(self.swap(self.f_function(self.permuttation(msg_encrypted[0], self.IP), k2)), k1), self.PI), '10101010')
    msg_decrypted = [msg_decrypted]

    for i in range(1, len(msg_encrypted)):
        msg_decrypted.append(self.xor(self.permuttation(self.f_function(self.swap(self.f_function(self.permuttation(msg_encrypted[i], self.IP), k2)), k1), self.PI), msg_encrypted[i-1]))

    return self.convert_binary_to_string(''.join(msg_decrypted))

  def xor(self, bits, key):
    response = ''

    for i in range(len(bits)):
      if bits[i] == '1' and key[i] == '0' or bits[i] == '0' and key[i] == '1':
        response += '1'
      else:
        response += '0'

    return response

  def convert_message_to_binary(self, text):
    char_number, response = [], []

    for character in text: char_number.append(ord(character))
    for i in char_number: response.append(str(bin(i)[2:])[::-1].ljust(8, "0")[::-1])

    return ''.join(response)

  def convert_binary_to_array(self, binary):
    _bytes, i = [], 0

    while i < len(binary):
        _bytes.append(binary[i:i+8])
        i += 8

    return _bytes

  def permuttation(self, bits, indexes):
    size = len(indexes)
    response = list(range(size))

    for i in range(size): response[i] = bits[indexes[i] - 1]

    return ''.join(response)

  def rotate(self, bits, displacement):
    size = len(bits)
    first_bits = list(range(displacement))
    response = list(range(size))

    for i in range(displacement):
      first_bits[i] = bits[i]

    for i in range(size - displacement):
      response[i] = bits[i + displacement]

    k = 0

    for i in range((size - displacement), size):
      response[i] = first_bits[k]
      k += 1

    return response

  def expand(self, bits):
    response = list(range(8))

    for i in range(8):
      response[i] = bits[self.EX[i] - 1]

    return response

  def binary_to_integer(self, a, b):
    if a == '0' and b == '0':
      return 0

    if a == '0' and b == '1':
      return 1

    if a == '1' and b == '0':
      return 2

    if a == '1' and b == '1':
      return 3

    return -1

  def swap(self, bits):
    size = len(bits)
    limit = int(size / 2)

    return bits[limit:size] + bits[0:limit]


  def integer_to_binary(self, num):
    if num == 0:
      return '00'

    if num == 1:
      return '01'

    if num == 2:
      return '10'

    if num == 3:
      return '11'

    return ''

  def blocks(self, bits):
    left = bits[0:4]
    right = bits[4:8]

    s0_row = self.binary_to_integer(left[0], left[3])
    s0_col = self.binary_to_integer(left[1], left[2])

    s1_row = self.binary_to_integer(right[0], right[3])
    s1_col = self.binary_to_integer(right[1], right[2])

    return self.integer_to_binary(self.S0[s0_row][s0_col]) + self.integer_to_binary(self.S1[s1_row][s1_col])

  def f_function(self, bits, key):
    left, right = bits[0:4], bits[4:8]

    return self.xor(self.permuttation(self.blocks(self.xor(self.expand(right), key)), self.P4), left) + right

  def convert_binary_to_string(self, text):
    char_number = []
    _bytes = self.convert_binary_to_array(text)
    response = ''

    for i in _bytes:
        aux, char = 0, 0
        i = int(i)
        k = int(math.log10(i)) + 1

        for j in range(k):
            aux = ((i % 10) * (2**j))
            i = i // 10
            char = char + aux

        char_number.append(char)

    for char in char_number: response += chr(char)

    return response

CBC.decrypt('10001011011000110001011100001101000010111100010101100101001010110110110110110111', '1000000000')