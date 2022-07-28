class SDES:
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

    def __init__(self, message, key, action):
        self.message = message
        self.key = key
        self.action = action

    def encrypt(message, key):
        try:
            return SDES(message, key, 'encrypt').crypt()
        except:
            return message

    def decrypt(message, key):
        try:
            return SDES(message, key, 'decrypt').crypt()
        except:
            return message

    def crypt(self):
        p10 = self.permuttation(self.key, self.P10)

        left, rigth = self.rotate(p10[0:5], 1), self.rotate(p10[5:10], 1)

        k1 = self.permuttation(left + rigth, self.P8)
        k2 = self.permuttation(self.rotate(left, 2) + self.rotate(rigth, 2), self.P8)

        if self.action == 'encrypt':
            response = self.crypt_function(k1, k2)
        else:
            response = self.crypt_function(k2, k1)

        return ''.join(response)

    def permuttation(self, bits, indexes):
        size = len(indexes)
        response = list(range(size))

        for i in range(size): response[i] = bits[indexes[i] - 1]

        return response

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

    def swap(self, bits):
        size = len(bits)
        limit = int(size / 2)

        return bits[limit:size] + bits[0:limit]

    def xor(self, bits, key):
        response = list(range(len(bits)))

        for i in range(len(bits)):
            if bits[i] == '1' and key[i] == '0' or bits[i] == '0' and key[i] == '1':
                response[i] = '1'
            else:
                response[i] = '0'

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

    def crypt_function(self, key1, key2):
        return self.permuttation(self.f_function(self.swap(self.f_function(self.permuttation(self.message, self.IP), key1)), key2), self.PI)
