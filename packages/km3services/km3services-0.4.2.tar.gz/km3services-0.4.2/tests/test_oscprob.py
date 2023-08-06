#!/usr/bin/env python3

import unittest

import numpy as np

from km3services.oscprob import OscProb


class TestOscProb(unittest.TestCase):
    def test_init(self):
        oscprob = OscProb()
        assert oscprob.url == "http://131.188.161.12:30000"

    def test_oscillationprobabilities(self):
        oscprob = OscProb()

        n = 100
        energies = np.random.randint(1, 50, n)
        cos_zeniths = 1 - np.random.rand(n) * 2
        probabilities = oscprob.oscillationprobabilities(12, 14, energies, cos_zeniths)
        assert np.all(probabilities <= 1)
