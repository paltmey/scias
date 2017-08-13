# coding=utf-8
import falcon
import json
from numpy import lib


class InferenceController(object):
    """
    Diese Klasse ist der REST-Endpunkt für die Bilderkennung.
    """

    def __init__(self, inference_service):
        """
        Konstruktor zum Erzeugen eines neuen InferenceController.
        :param inference_service: InferenceService, der zur Bilderkennung verwendet wird
        """

        self.inference_service = inference_service

    def on_post(self, req, resp):
        """
        Liefert zu einer Anfrage mit Bilder als numpy-Arrays die Erkannten ImageNet-Konzepte und Scores.
        :param req: falcon Request-Objekt
        :param resp: falcon Response-Objekt
        """

        images = lib.format.read_array(req.stream, allow_pickle=False)

        predictions = self.inference_service.run_inference(images)

        resp.body = json.dumps(predictions)
        resp.status = falcon.HTTP_200