import sys
sys.path.append('../')

import unittest
from src.scripts.cbc import CBC

class TestCBC(unittest.TestCase):
  def test_encrypt_method_1(self):
    response = CBC.encrypt('1000000000', '1000000000')

    assert response == '10001011011000110001011100001101000010111100010101100101001010110110110110110111'

  def test_encrypt_when_goes_wrong(self):
    response = CBC.encrypt('1000000000', '')

    assert response == '1000000000'

  def test_decrypt_method_1(self):
    response = CBC.decrypt('10001011011000110001011100001101000010111100010101100101001010110110110110110111', '1000000000')

    assert response == '1000000000'

  def test_decrypt_when_goes_wrong(self):
    response = CBC.decrypt('1000000000', '')

    assert response == '1000000000'
