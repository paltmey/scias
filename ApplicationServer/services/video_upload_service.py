# coding=utf-8


class VideoUploadService(object):
    """
    Diese Klasse ist für den Videoupload zuständig.
    """

    def __init__(self, video_object_recognition_service, video_repository):
        """
        Konstruktor zum Erzeugen eines neuen VideoUploadService.
        :param video_object_recognition_service: VideoObjectRecognitionService
        :param video_repository: VideoRepository
        """

        self.video_object_recognition_service = video_object_recognition_service
        self.video_repository = video_repository

    def process_video(self, tmp_file_path, orig_filename, extension):
        video_id = self.video_repository.insert_video(tmp_file_path, orig_filename, extension)
        self.video_object_recognition_service.start(video_id)

        return video_id
