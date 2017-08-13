#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides a color correlogram feature extraction.

@copyright: Copyright 2010 Deutsches Forschungszentrum fuer Kuenstliche
            Intelligenz GmbH or its licensors, as applicable.
@license: This is free software: you can redistribute it and/or modify it under
          the terms of the GNU General Public License as published by the Free
          Software Foundation, either version 3 of the License, or (at your
          option) any later version. You should have received a copy of the
          GNU General Public License along with this software (COPYING).
          If not, see <http://www.gnu.org/licenses/>.
"""
from core.feature.colorcorrelogram.calculateDescriptors_cython import calculateDescriptors_cython
from core.feature.featureextraction import ImageFeatureExtraction
from numpy import concatenate


class ColorCorrelogramExtraction(ImageFeatureExtraction):
    """
    This class implements color correlogram feature extraction from images.
    The feature was developed by Johan Hofmann from Netclean Technologies
    and used in the FIVES project.
    Concatenation of 300-dimensional color histogram and 300-dimensional
    color correlogram to a 600-dimensional feature.
    The module was implemented in cython for speedup purposes.
    """

    def __init__(self):
        """
        Initialize the ColorCorrelogramExtraction.
        """
        ImageFeatureExtraction.__init__(self)


    def extract_feature(self, pil_image, **kwargs):
        """ Extracts the color correlogram feature for the given image.

        @type pil_image: L{PIL image}
        @param pil_image: The image to extract color the histogram from.
        @return: color histogram
        @rtype: numpy.ndarray
        """
        (ac, ch, sv) = calculateDescriptors_cython(pil_image)
        ac = ac.reshape(300)
        ch = ch.reshape(300)
        f = concatenate((ac, ch))
        return f.astype('float32')
