# coding=utf-8
import logging
from multiprocessing import Pool
import concurrent.futures

PROCESSES = 1


def video_recognition_alias(*args, **kwargs):
    """
    Alias-Methode; weil Instanzmethoden nicht in einem neuen Thread gestartet werden können.
    """
    VideoObjectRecognitionService.video_recognition(*args, **kwargs)


class VideoObjectRecognitionService(object):
    """
    Diese Klasse ist für die Videoanalyse zuständig.
    Für die Keyframe-Erkennung wird der KeyframeExtraktionService genutzt.
    Für die Erkennung wird der InferenceClient verwendet.
    """

    def __init__(self, interference_service, key_frame_extraction_service, key_frame_repository, video_repository):
        """
        Konstruktor zum Erzeugen eines neuen VideoObjectRecognitionService.
        :param interference_service: InferenceService
        :param key_frame_extraction_service:  KeyFrameExtractionService
        :param key_frame_repository: KeyFrameRepository
        :param video_repository: VideoRepository
        """
        self.interference_service = interference_service
        self.key_frame_extraction_service = key_frame_extraction_service
        self.key_frame_repository = key_frame_repository
        self.video_repository = video_repository
        self.pool = concurrent.futures.ProcessPoolExecutor(PROCESSES)

    def start(self, video_id):
        """
        Startet den Prozess der Videoanalyse.
        :param video_id: die id der zu analysierenden Videos
        """

        video_path = self.video_repository.get_video_path(video_id)
        self.pool.submit(video_recognition_alias, self.key_frame_extraction_service, self.key_frame_repository, self.interference_service, video_id, video_path)


    @staticmethod
    def video_recognition(key_frame_extractoion_service, key_frame_repository, interference_client, video_id, video_path):
        batch_count = 0

        logging.info("begin processing: \n\tvideo_id: {} \n\tvideo_path: {}".format(video_id, video_path))
        for key_frames, times in key_frame_extractoion_service.extract_keyframes(video_path):  # Keyframes extrahieren
            key_frame_ids = key_frame_repository.insert_key_frames(video_id, key_frames, times)  # Keyframes speichern

            predictions = interference_client.run_interference_on_images(key_frames)  # Keyframes zum Inference Server senden
            key_frame_repository.insert_key_frame_predictions(key_frame_ids, predictions)  # Predictions speichern

            batch_count += 1

        logging.info("finished processing: \n\tvideo_id: {} \n\tvideo_path: {}\n\tnumber of batches: {}".format(video_id, video_path, batch_count))

    def close(self):
        self.pool.close()
