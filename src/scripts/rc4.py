import re

class RC4:
    def encrypt(message, key):
        try:
            return RC4.crypt(message, key, 'encrypt')
        except:
            return message

    def decrypt(message, key):
        try:
            return RC4.crypt(message, key, 'decrypt')
        except:
            return message

    def crypt(message, key, action):
        BYTES = 256
        key = [ord(element) for element in key]

        if action == 'encrypt':
            message = [ord(element) for element in message]
        else:
            message = [int(element, 16) for element in re.sub('0x', ' ', message).split()]

        s = list(range(BYTES))
        r = list(range(len(message)))

        for i in range(BYTES): s[i] = i

        j = 0

        for i in range(BYTES):
            j = (j + s[i] + key[i % len(key)]) % BYTES

            s[i], s[j] = s[j], s[i]

        i = j = 0

        for k in range(len(message)):
            i = (i + 1) % BYTES
            j = (j + s[i]) % BYTES

            s[i], s[j] = s[j], s[i]

            if action == 'encrypt':
                r[k] = hex(s[(s[i] + s[j]) % BYTES] ^ message[k])
            else:
                r[k] = chr(s[(s[i] + s[j]) % BYTES] ^ message[k])

        return ''.join(r)
