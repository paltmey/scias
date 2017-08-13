# coding=utf-8
import json

import falcon
from functional import seq


class SearchController(object):
    """
    Diese Klasse ist der REST-Endpunkt für die Suche.
    """

    def __init__(self, search_service):
        """
        Konstruktor zum Erzeugen eines neuen SearchController.
        :param search_service: SearchService
        """
        self.search_service = search_service

    def on_get(self, req, resp):
        """
        Liefert zu einer Anfrage mit dem Query-Parameter q die Keyframe-Metadaten.

        :param req: falcon Request-Objekt
        :param resp: falcon Response-Objekt
        """

        query = req.get_param('q', required=True)
        page = req.get_param_as_int('page', min=0)
        page = page if page else 0
        include_total_pages = req.get_param_as_bool('include_total_pages')
        include_total_pages = include_total_pages if include_total_pages is not None else True
        include_predictions = req.get_param_as_bool('include_predictions')
        include_predictions = include_predictions if include_predictions is not None else True

        key_frames, total_count, labeled_predictions = self.search_service.get_key_frames(unicode(query), page,
                                                                                          include_total_pages=include_total_pages,
                                                                                          include_matching_nodes=include_predictions,
                                                                                          labeled_prediction_limit=10)

        if not key_frames:
            resp.body = '{"error":"No matching key frames found"}'
            resp.status = falcon.HTTP_NOT_FOUND
            return

        key_frames_view_model = seq(key_frames).map(
            lambda key_frame: dict(
                key_frame, thumbnail='/images/{}.png'.format(key_frame['key_frame_id']),
                time=key_frame['time']/1000.0)
        ).list()

        res = {'key_frames': key_frames_view_model}

        if include_total_pages:
            res['total_pages'] = total_count

        if include_predictions:
            res['labeled_predictions'] = labeled_predictions

        resp.status = falcon.HTTP_OK
        resp.body = json.dumps(res)
