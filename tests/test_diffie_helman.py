import sys
sys.path.append('../')

import unittest
from src.scripts.diffie_helman import DiffieHelman

class TestDiffieHelman(unittest.TestCase):
    def test_get_public_1(self):
        private_key = 63
        public_key = 13
        response = DiffieHelman.get_public(private_key)

        assert response == public_key

    def test_get_public_2(self):
        private_key = 79
        public_key = 12
        response = DiffieHelman.get_public(private_key)

        assert response == public_key

    def test_get_key_1(self):
        public_key = 12
        private_key = 63
        response = DiffieHelman.get_key(public_key, private_key)

        assert response == 8

    def test_get_key_2(self):
        public_key = 13
        private_key = 79
        response = DiffieHelman.get_key(public_key, private_key)

        assert response == 8

    def test_happy_path(self):
        a_private_key, b_private_key = 63, 79

        a_public_key = DiffieHelman.get_public(a_private_key)
        b_public_key = DiffieHelman.get_public(b_private_key)

        a_final_key = DiffieHelman.get_key(a_public_key, b_private_key)
        b_final_key = DiffieHelman.get_key(b_public_key, a_private_key)

        assert a_public_key == 13
        assert b_public_key == 12
        assert a_final_key == 8
        assert a_final_key == b_final_key
