# coding=utf-8
import cv2
import numpy as np
from PIL import Image

from descriptors import calculateDescriptors_cython


class KeyFrameExtractor(object):
    """
    Dieses Interface kann zum Erkennen von Keyframes implementiert werden.
    """

    def __init__(self, threshold):
        """
        Konstruktor zum Erzuegen eines neuen KeyFrameExtractor mit einem übergebenen threshold.
        :param threshold:
        """
        self.threshold = threshold

    def calculate_distance(self, feature, prev_feature):
        """
        Berechnet die Distanz zwischen zwei, mit der calculate_feature Methode berechneten, Features.
        :param feature: das neue Feature
        :param prev_feature: das vorherige Feature
        :return: Distanz der Features
        """
        raise NotImplementedError

    def calculate_feature(self, frame):
        """
        Berechnet ein Feature aus dem übergebenen Frame.
        :param frame: Frame, zu dem das Feature berechnet werden soll
        """
        raise NotImplementedError

    def is_above_threshold(self, distance):
        """
        Prüft, ob die übergebene Distanz den im Konstruktor festgelegten Threshold übersteigt.
        :param distance: zu prüfende Distanz
        """
        raise NotImplementedError


class CvKeyFrameExtractor(KeyFrameExtractor):
    """
    Implementiert einen KeyFrameExtraktor mit einem 8x8x8 RGB-Histogram.
    """

    def __init__(self, threshold=0.89):
        KeyFrameExtractor.__init__(self, threshold)

    def calculate_distance(self, feature, prev_feature):
        return cv2.compareHist(prev_feature, feature, cv2.HISTCMP_CORREL)

    def calculate_feature(self, frame):
        return cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

    def is_above_threshold(self, distance):
        return distance < self.threshold


class CorellogramKeyFrameExtractor(KeyFrameExtractor):
    """
    Implementiert einen KeyFrameExtraktor mit einem Farb-Korrelogramm.
    """

    def __init__(self, threshold=2.5):
        KeyFrameExtractor.__init__(self, threshold)

    def calculate_distance(self, feature, prev_feature):
        return np.linalg.norm(prev_feature - feature)

    def calculate_feature(self, frame):
        cv2_rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(cv2_rgb_img)

        (ac, ch, sv) = calculateDescriptors_cython(pil_img)
        ac = ac.reshape(300)
        ch = ch.reshape(300)
        return np.concatenate((ac, ch))

    def is_above_threshold(self, distance):
        return distance > self.threshold
