import unittest

import pyximport
pyximport.install()

import test_cython

print(test_cython.primes(1000))
