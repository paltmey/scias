# coding=utf-8
import mimetypes

import falcon


class VideoController(object):
    """
    Die Klasse ist für den Videoupload zuständig.
    """

    def __init__(self, video_upload_service):
        """
        Konstruktor zum Erzeugen eines neuen VideoController.
        :param video_upload_service:  VideoUploadService
        """

        self.video_upload_service = video_upload_service

    def on_post(self, req, resp):
        """
        Nimmt einen Filestream entgegen und speichert ihn mit dem VideoUploadService.
        :param req: falcon Request-Objekt
        :param resp: falcon Response-Objekt
        """

        #Todo refuse if content type is not valid
        extension = mimetypes.guess_extension(req.content_type)
        tmp_file_path = req.get_header('X-File-Name', True)
        orig_filename = req.get_header('X-Original-File-Name', True)
        video_id = self.video_upload_service.process_video(tmp_file_path, orig_filename, extension)

        resp.status = falcon.HTTP_201
        resp.location = '/videos/' + video_id
