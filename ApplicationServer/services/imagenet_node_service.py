# coding=utf-8
import math
from functional import seq


class ImagenetNodeService(object):
    """
    Die Klasse ist für die Nearest Neighbour Suche in den ImageNet-Konzepten zuständig.
    """

    def __init__(self, index, annoy_id_to_node, imagenet_labels):
        """
        Konstruktor zum Erzeugen eines neuen ImagenetNodeService.
        :param index: Annoy Index mit den ImageNet-Konzepten
        :param annoy_id_to_node: Mapping von Annoy-Id zu ImageNet-Knoten
        :param imagenet_labels: Mapping von Imagenet-Knoten zu Imagenet-Konzept (human string)
        """

        self.index = index
        self.annoy_id_to_node = annoy_id_to_node
        self.imagenet_labels = imagenet_labels

    @staticmethod
    def __distance_to_vec_norm(distance):
        return 1 - math.pow(distance, 2) / 2

    def get_nearest_nodes(self, word_vector):
        """
        Sucht mit einer Nearest Neigbour Suche die zum übergebenen Word-Vektor nächsten Konzepte.
        :param word_vector: Eingabe Word-Vektor
        :return: die zehn besten Treffer
        """

        classes, distances = self.index.get_nns_by_vector(word_vector, 10, 10000, include_distances=True)
        vector_norms = seq(distances).map(self.__distance_to_vec_norm)
        nodes = seq(classes).map(lambda c: str(self.annoy_id_to_node[str(c)]))
        nodes_with_norms = seq(nodes).zip(vector_norms)

        max_nodes = (
            nodes_with_norms
            .group_by_key()
            .map(lambda group: (group[0], max(group[1])))
        )
        return max_nodes

    def get_human_string(self, imagenet_node):
        """
        Gibt zu einem übergebenen ImageNet-Knoten den human_string, also das Imagenet-Konzept, zurück.
        :param imagenet_node:
        :return: human_string
        """

        if imagenet_node in self.imagenet_labels:
            return self.imagenet_labels[imagenet_node]

        return None
