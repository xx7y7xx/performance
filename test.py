#!/usr/bin/python2.7

from encrypt import encryption
from encrypt import decryption

en = encryption("abc", "0123456789abcdef")

decryption(en, "0123456789abcdef")
