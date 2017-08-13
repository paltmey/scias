# coding=utf-8
from functional import seq

PRECISION = 4


class SearchService(object):
    """
    Diese Klasse ist für die Suche von Keyframes zu einem übergebenen Query zuständig.
    """

    def __init__(self, imagenet_node_service, key_frame_repository, nlp):
        """
        Konstruktor zum Erzeugen eines neuen SearchService.
        Beim Aufruf wird das spaCy Word-Vektor-Modell geladen.
        :param imagenet_node_service: ImagenetNodeService
        :param key_frame_repository: Keyframe Repository
        :param nlp: spaCy Modell
        """
        self.imagenet_node_service = imagenet_node_service
        self.key_frame_repository = key_frame_repository
        self.nlp = nlp

    def get_key_frames(self, query, page, include_total_pages=False, include_matching_nodes=False, labeled_prediction_limit=None):
        """
        Findet zu einem übergebenen Query die am besten passenden Keyframes.
        Dabei werden Stopwords mit dem spaCy-NLP-Modell aus dem Query entfernt.
        :param query: Suchquery
        :param page: zu ladende Seite
        :param include_matching_nodes: Gibt an, ob auch die am besten passenden ImageNet-Konzepte zurückgegeben werden sollen
        :param labeled_prediction_limit: Limit für die Liste von ImageNet-Konzepten
        :return: Keyframe-Metadaten und ImageNet-Konzepte
        """

        labeled_predictions = None

        keyword_set = self.__create_keyword_set(query)
        weighted_nodes = self.__get_weighted_nodes(keyword_set)
        key_frames, total_pages = self.key_frame_repository.get_key_frames(weighted_nodes, page, include_total_pages)

        if include_matching_nodes:
            labeled_predictions = self.__get_matching_nodes(weighted_nodes, labeled_prediction_limit)

        return key_frames, total_pages, labeled_predictions

    def __create_keyword_set(self, query):
        doc = self.nlp(query)

        keyword_set = (
            seq(doc)
            .filter_not(lambda token: token.is_stop)  # stopwords entfernen
            .set()
        )
        return keyword_set

    def __get_weighted_nodes(self, keyword_set):
        weighted_nodes = (
            seq(keyword_set)
            .filter(lambda keyword: keyword.has_vector)
            .map(lambda keyword: keyword.vector)  # Word-Vektor aus Modell holen
            .flat_map(self.imagenet_node_service.get_nearest_nodes)  # ImageNet-Konzepte finden
            .reduce_by_key(lambda x, y: x + y)  # gefunde Konzepte addieren
        )
        return weighted_nodes

    def __get_matching_nodes(self, weighted_nodes, limit):
        self.i = 4
        labeled_predictions = (
            seq(weighted_nodes)
            .sorted(lambda weighted_node: weighted_node[1], reverse=True)
            .map(lambda weighted_node: {
                'node': weighted_node[0],
                'human_string': self.imagenet_node_service.get_human_string(weighted_node[0]),
                'weight': str(round(weighted_node[1], PRECISION))
            })
            .list(limit)
        )
        return labeled_predictions
