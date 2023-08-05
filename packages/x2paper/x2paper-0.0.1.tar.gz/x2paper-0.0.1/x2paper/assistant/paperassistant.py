#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes of PaperAssistant.
"""

from abc import abstractclassmethod
import numpy as np


class PaperAssistant(object):
    """
    Base PaperAssistant class
    """

    def __init__(self, name=None, seed=0, **kwargs):
        self.name = name
        self.seed = seed
        np.random.seed(seed)
