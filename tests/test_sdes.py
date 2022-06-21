import sys
sys.path.append('../')

import unittest
from src.scripts.sdes import SDES

class TestSDES(unittest.TestCase):
  def test_encrypt_method(self):
    response = SDES.encrypt('01010101', '1000000000')

    assert response == '00101011'

  def test_encrypt_when_goes_wrong(self):
    response = SDES.encrypt('01010101', '')

    assert response == '01010101'

  def test_decrypt_method(self):
    response = SDES.decrypt('00101011', '1000000000')

    assert response == '01010101'

  def test_decrypt_when_goes_wrong(self):
    response = SDES.decrypt('00101011', '')

    assert response == '00101011'
