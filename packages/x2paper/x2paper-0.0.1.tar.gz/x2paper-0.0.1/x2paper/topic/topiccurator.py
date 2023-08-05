#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes of TopicCurator.
"""

import numpy as np


class TopicCurator(object):
    """
    Base TopicCurator class
    """

    def __init__(self, name=None, seed=0, **kwargs):
        self.name = name
        self.seed = seed
        np.random.seed(seed)
