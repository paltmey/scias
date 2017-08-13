# coding=utf-8
import cv2
import numpy as np

IMAGE_HEIGHT = 300

class KeyFrameExtractionService(object):
    """
    Diese Klasse implementiert die Extraktion von Keyframes aus einem Video.
    Für die Erkennung der Keyframes wird ein KeyframeExtraktor verwende.
    """

    def __init__(self, key_frame_extractor, batch_size, frame_span=(1000, 10000), show_frames=False):
        """
        Konstruktor zum Erzeugen eines neuen KeyFrameExtractionService.
        :param key_frame_extractor: KeyframeExtraktor zum Erkennen der Keyframes
        :param batch_size: Anzahl von Keyframes, die bei einem yield zurückgeliefert werden
        :param frame_span: Minimale und maximale Zeit, nach der ein Frame als Keyframe genommen werden kann
        :param show_frames: Gibt an, ob während der Extraktion die Keyframes angezeigt werden sollen
        """

        self.key_frame_extractor = key_frame_extractor
        self.batch_size = batch_size
        self.min_frame_span = frame_span[0]
        self.max_frame_span = frame_span[1]
        self.show_frames = show_frames

    def extract_keyframes(self, video_path):
        """
        Generator zum extrahieren von Keyframes aus dem Video mit dem übergebenem Pfad. Die Keyframes werden in Batches zurückgegben.
        :param video_path:
        """

        key_frame_count = 0
        key_frame_ms = 0
        key_frames = []
        times = [0]

        cap = cv2.VideoCapture()
        cap.open(video_path)

        is_new_keyframe = False

        if cap.isOpened():

            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            aspect_ratio = float(width)/height
            resize_width = int(aspect_ratio * IMAGE_HEIGHT)

            # ersten Frame als ersten Keyframe speichern
            ret, key_frame = cap.read()

            if ret:
                key_frame_feature = feature = self.key_frame_extractor.calculate_feature(key_frame)

                resized_frame = cv2.resize(key_frame, (resize_width, IMAGE_HEIGHT), interpolation=cv2.INTER_AREA)
                key_frames.append(resized_frame)
                key_frame_count += 1

            else:
                raise EOFError
        else:
            raise EOFError

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            if self.show_frames:
                self.__show_frames(frame, key_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            current_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            delta_ms = current_ms - key_frame_ms

            if delta_ms >= self.min_frame_span:
                feature = self.key_frame_extractor.calculate_feature(frame)
                distance = self.key_frame_extractor.calculate_distance(feature, key_frame_feature)

                if self.key_frame_extractor.is_above_threshold(distance):
                    is_new_keyframe = True

            elif delta_ms >= self.max_frame_span:
                feature = self.key_frame_extractor.calculate_feature(frame)
                is_new_keyframe = True

            if is_new_keyframe:
                resized_frame = cv2.resize(frame, (resize_width, IMAGE_HEIGHT), interpolation=cv2.INTER_AREA)

                key_frames.append(resized_frame)
                times.append(current_ms)

                key_frame = frame
                key_frame_feature = feature
                key_frame_count += 1
                key_frame_ms = current_ms
                is_new_keyframe = False

                if key_frame_count % self.batch_size == 0:
                    yield (key_frames, times)
                    key_frames = []
                    times = []

        if key_frames:  # falls die Anzahl der Keyframes nicht durch die Batchgröße teilbar ist
            yield (key_frames, times)

        cap.release()
        cv2.destroyAllWindows()

        return

    @staticmethod
    def __show_frames(frame, key_frame):
        both = np.hstack((key_frame, frame))
        cv2.imshow('frame', both)
