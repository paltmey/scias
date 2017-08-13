# coding=utf-8
import os
import cv2
import math
import rethinkdb as r

PAGE_LENGTH = 20


class KeyFrameRepository(object):
    """
    Die Klasse ist für die Speicherung von Keyframes und Keyframe-Predictions
    sowie die Abfrage von Keyframe-Metadaten aus der Datenbank zuständig
    """

    def __init__(self, key_frame_directory, db_host, db_port):
        """
        Konstruktor zum Erzeugen eines neuen KeyFrameRepository.
        :param db_host: Datenbank Host Adresse
        :param db_port: Datenbank Port
        :param key_frame_directory: Pfad des Ordners, in dem Keyframes gespeichert werden
        """
        self.key_frame_directory = key_frame_directory
        self.db_host = db_host
        self.db_port = db_port

    def insert_key_frames(self, video_id, key_frames, times):
        """
        Erzeugt für jeden Keyframe einen Datenbankeintrag und speichert die Keyframes auf der Festplatte.
        :param video_id: id des Videos, aus dem die Keyframes extrahiert wurden
        :param key_frames: Extrahierte Frames
        :param times: Timecode des Keyframes im Video
        :return: aus der Datenbank generierte ids
        """
        entries = [dict(time=time, video_id=video_id) for time in times]

        res = r.table('key_frames').insert(entries).run(r.connect(self.db_host, self.db_port, 'vor'))

        generated_keys = res['generated_keys']

        for key, frame in zip(generated_keys, key_frames):
            path = os.path.join(self.key_frame_directory, key) + '.png'
            cv2.imwrite(path, frame)

        return generated_keys

    def insert_key_frame_predictions(self, key_frame_ids, predictions):
        """
        Fügt die übergebenen Predictions in die Datenbank ein.
        :param key_frame_ids: ids der Keyframes
        :param predictions: Predictions
        """
        entries = [dict(prediction_entry, key_frame_id=key_frame_id) for key_frame_id, prediction in
                   zip(key_frame_ids, predictions) for prediction_entry in prediction]

        res = r.table('key_frame_predictions').insert(entries).run(r.connect(self.db_host, self.db_port, 'vor'))

    def get_key_frames(self, weighted_nodes, page, include_total_pages=False):
        """
        Holt zu den übergebenen Konzepten die Keyframe-Metadaten aus der Datenbank.
        :param weighted_nodes: übergebene Konzepte mit Gewichtung
        :param page: Seite die abgefragt werden soll
        :return: Keyframe-Metadaten
        """

        total_pages = None

        nodes = weighted_nodes.map(lambda item: item[0])
        weighted_nodes_dict = weighted_nodes.to_dict()

        if include_total_pages:
            total_count = (
                r.table('key_frame_predictions')
                .get_all(r.args(nodes), index='node')
                .group('key_frame_id')
                .ungroup()
                .count()
                .run(r.connect(self.db_host, self.db_port, 'vor'))
            )

            total_pages = math.ceil(float(total_count)/PAGE_LENGTH)

        key_frames = (
            r.table('key_frame_predictions')
            .get_all(r.args(nodes), index='node')  # alle Keyframe-Predictions holen, die einem übergebenen Konzept zugeordnet sind
            .map(lambda row: {
                'key_frame_id': row['key_frame_id'],
                'weighted_score': r.expr(weighted_nodes_dict)[row['node']].mul(row['score'].coerce_to('number'))  # die übergebenen Gewicht und Scores der Keyframes multiplizieren
            })
            .group('key_frame_id').reduce(lambda left, right: {  # nach Keyframe gruppieren
                'weighted_score': left['weighted_score'].add(right['weighted_score'])  # den Score für mehrere Konzepte addieren
            })
            .ungroup()
            .map(lambda row: {
                'key_frame_id': row['group'],
                'weighted_score_sum': row['reduction']['weighted_score']
            })
            .order_by(r.desc('weighted_score_sum'))  # absteigend sortieren
            .slice(*KeyFrameRepository.__pagination(page))  # zur entsprechenden Page skippen
            .eq_join('key_frame_id', r.table('key_frames'))  # die Metadaten aus der Keyframe-Tabelle holen
            .without({'right': 'id'})
            .zip()
            .order_by(r.desc('weighted_score_sum'))  # erneut sortieren, da join die Reihenfolge verändert
            .run(r.connect(self.db_host, self.db_port, 'vor'))
        )

        return key_frames, total_pages

    @staticmethod
    def __pagination(page):
        begin = PAGE_LENGTH*page
        end = begin+PAGE_LENGTH
        return begin, end
