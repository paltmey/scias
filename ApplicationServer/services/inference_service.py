# coding=utf-8
import json
from cStringIO import StringIO

import cv2
import numpy as np
import requests


class InferenceService(object):
    """
    Die Klasse ist für das Senden von Bildern zum Inferece Server zuständig.
    """

    def __init__(self, interference_server_address):
        """
        Konstruktor zum Erzeugen eines neuen InferenceService.
        :param interference_server_address: URL des Inference Servers
        """
        self.interference_server_address = interference_server_address

    def run_interference_on_images(self, images):
        """
        Sendet die übergebenen Bilder an den Inference Server und gibt die erkannten ImageNet-Knoten mit Score zurück.
        :param images: zu erkennenden Bilder als numpy-Matrix im BGR-Format.
        :return: vom Inference Server gelieferten Predictions mit ImageNet-Knoten und Score
        """

        converted_images = []

        for image in images:
            cv2_rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            converted_images.append(cv2_rgb_img)

        stacked_images = np.stack(images)

        memory_file = StringIO()  # erzeugt eine in-memory datei, die für np.save verwendet wird
        np.save(memory_file, stacked_images, allow_pickle=False)

        memory_file.seek(0)

        res = requests.post(self.interference_server_address, data=memory_file)

        if res.ok:
            predictions = json.loads(res.content)

            return predictions
