# coding=utf-8
import os
import rethinkdb as r


class VideoRepository(object):
    """
    Die Klasse ist für die Speicherung von Keyframes und Keyframe-Predictions
    sowie die Abfrage von Keyframe-Metadaten aus der Datenbank zuständig.
    """

    def __init__(self, upload_directory, video_directory, db_host, db_port):
        """
        Konstruktor zum Erzeugen eines neuen VideoRepository.
        :param video_directory: Pfad des Ordners, in dem Videos gespeichert werden
        :param db_host: Datenbank Host Adresse
        :param db_port: Datenbank Port
        """
        self.upload_directory = upload_directory
        self.video_directory = video_directory
        self.db_host = db_host
        self.db_port = db_port

    def insert_video(self, tmp_file_path, orig_filename, extension):
        """
        Erzeugt einen Datenbankeintrag und speichert ein Video in Chunks auf der Festplatte.
        :param tmp_file_path: Pfad der temporären Datei, die der Webserver für den Upload anlegt
        :param orig_filename: Dateiname, der vom Client submitted wird
        :param extension: Dateiendung des Videos
        :return: aus der Datenbank generierte ids
        """

        res = (
            r.table('videos')
            .insert({'name': orig_filename, 'extension': extension})
            .run(r.connect(self.db_host, self.db_port, 'vor'))
        )

        generated_key = res['generated_keys'][0]

        new_file_path = os.path.join(self.video_directory, generated_key + extension)
        os.rename(tmp_file_path, new_file_path)

        return generated_key

    def get_video_path(self, video_id):
        """
        Ruft den Pfad eines Videos zu einer gegebenen id ab.
        :param video_id: id des Videos
        :return: Pfad des Videos
        """

        res = r.table('videos').get(video_id).pluck('extension').run(r.connect(self.db_host, self.db_port, 'vor'))

        extension = res['extension']
        video_path = os.path.join(self.video_directory, video_id + extension)
        return video_path
