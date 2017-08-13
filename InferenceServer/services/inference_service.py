# coding=utf-8
import os
import tensorflow as tf
import sys

sys.path.insert(0, 'tf_models/slim')

from nets import inception
from nets import nets_factory
from preprocessing import preprocessing_factory

slim = tf.contrib.slim
checkpoints_dir = 'checkpoints'
image_size = inception.inception_v3.default_image_size


class InferenceService(object):
    """
    Diese Klasse implementiert die Bilderkennung mit einem TensorFlow-Slim Inception-v3 Modell.
    """

    def __init__(self):
        """ar
        Konsturktor zum Erzeugen eines neuen InferenceService.
        Beim Aufruf wird der Computing-Graph des Modells erzeugt und die trainierten Gewichte in eine Session geladen.
        """

        self.inputs_placeholder, self.num_results, self.values, self.indices = self.__create_graph()
        self.session = self.__create_session(10)

    def __create_graph(self): #Graph mit TensorFlow-Slim erzeugen
        graph = tf.Graph()

        num_results = tf.Variable(5, tf.int32, name='num_results')
        inputs_placeholder = tf.placeholder(tf.uint8, name='inputs_placeholder', shape=[None, None, None, 3])

        image_preprocessing_fn = preprocessing_factory.get_preprocessing('inception_v3', is_training=False)

        processed_images = tf.map_fn(lambda x: image_preprocessing_fn(x, image_size, image_size), inputs_placeholder, dtype=tf.float32)

        network_fn = nets_factory.get_network_fn('inception_v3', 1001)
        logits, _ = network_fn(processed_images)

        probabilities = tf.nn.softmax(logits) # softmax als letzte Schicht des Netzes
        values, indices = tf.nn.top_k(probabilities, k=num_results) # die top k Ergebnisse filtern
        values = tf.squeeze(values)
        indices = tf.squeeze(indices)

        return inputs_placeholder, num_results, values, indices

    def __create_session(self, k): # Session mit den Gewichten aus dem Checkpoint erzeugen
        init_fn = slim.assign_from_checkpoint_fn(
            os.path.join(checkpoints_dir, 'inception_v3.ckpt'),
            slim.get_model_variables('InceptionV3'))

        reassign_num_results = tf.assign(self.num_results, k) # Anzahl k der Ergebnisse im Graph mit übergebenem Wert ersetzen

        session = tf.Session()
        session.run(tf.global_variables_initializer())
        init_fn(session)

        session.run(reassign_num_results)

        return session

    def run_inference(self, images):
        """
        Führt die Bilderkennung mit den übergebenen Bildern aus
        :param images: Bilder als numpy-Array
        :return: Predictions in der Form {'score': score, 'node': node}
        """

        values, indices = self.session.run([self.values, self.indices], feed_dict={self.inputs_placeholder: images})

        res_predictions = []
        # TODO fix only one prediction as output
        for image_indices, image_values in enumerate(values):
            res_predictions.append([])

            for index, value in enumerate(image_values):
                score = str(value)
                node = str(indices[image_indices][index])

                res_predictions[image_indices].append({'score': score, 'node': node})

        return res_predictions
