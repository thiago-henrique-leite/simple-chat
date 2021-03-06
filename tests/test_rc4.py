import sys
sys.path.append('../')

import unittest
from src.scripts.rc4 import RC4

class TestRC4(unittest.TestCase):
    def test_encrypt_method_1(self):
        response = RC4.encrypt('batata', 'teste')

        assert response == '0x390xce0xe90xe30x560x36'

    def test_encrypt_method_2(self):
        response = RC4.encrypt('valedoparaiba', '1234')

        assert response == '0x730x280x1d0xca0x970x830x770x6c0x7d0x7a0x690x320x84'

    def test_encrypt_when_goes_wrong(self):
        response = RC4.encrypt('10010101', '')

        assert response == '10010101'

    def test_decrypt_method_1(self):
        response = RC4.decrypt('0x390xce0xe90xe30x560x36', 'teste')

        assert response == 'batata'

    def test_decrypt_method_2(self):
        response = RC4.decrypt('0x730x280x1d0xca0x970x830x770x6c0x7d0x7a0x690x320x84', '1234')

        assert response == 'valedoparaiba'

    def test_decrypt_when_goes_wrong(self):
        response = RC4.decrypt('0x390xce0xe90xe30x560x36', '')

        assert response == '0x390xce0xe90xe30x560x36'
