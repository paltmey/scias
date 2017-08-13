# coding=utf-8
import mimetypes
import os

import falcon

STATIC_FILE_PATH = '/Users/philippaltmeyer/Downloads/Uploaded Videos'


class StaticController(object):
    """
    Die Klasse ist für das Ausliefern von statischen Resourcen zuständig.
    """

    @staticmethod
    def on_get(req, resp, filename):
        """
        Liefert eine Datei mit dem zugehörigen Dateinamen im Request-Body zurück.
        :param req: falcon Request-Objekt
        :param resp: falcon Response-Objekt
        :param filename: Dateiname
        """

        resp.status = falcon.HTTP_200
        resp.content_type = mimetypes.guess_type(filename)[0]

        path = os.path.join(STATIC_FILE_PATH, filename)

        with open(path, 'r') as f:
            resp.body = f.read()
