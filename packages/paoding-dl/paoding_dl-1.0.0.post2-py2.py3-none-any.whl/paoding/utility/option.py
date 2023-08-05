#!/usr/bin/python3
__author__ = "Mark H. Meng"
__copyright__ = "Copyright 2021, National University of S'pore and A*STAR"
__credits__ = ["G. Bai", "H. Guo", "S. G. Teo", "J. S. Dong"]
__license__ = "MIT"

from enum import Enum


class ModelType(Enum):
    XRAY = 1
    KDD = 10
    MRI = 11
    CREDIT = 2
    MNIST = 3
    CIFAR = 4
    OTHER = -1

class SamplingMode(Enum):
    BASELINE = 1
    IMPACT = 2
    # STOCHASTIC is working in progress now
    STOCHASTIC = 3
    SCALE = 0
    OTHER = -1

class AttackAlogirithm(Enum):
    FGSM = 1
    OTHER = -1
