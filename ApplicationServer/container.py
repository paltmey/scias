# coding=utf-8
from annoy import AnnoyIndex
import json
import logging
import spacy

from controllers import VideoController, SearchController, StaticController
from services import ImagenetNodeService, InferenceService, KeyFrameExtractionService, CvKeyFrameExtractor, \
    CorellogramKeyFrameExtractor, SearchService, VideoObjectRecognitionService, VideoUploadService
from repositories import KeyFrameRepository, VideoRepository

"""
Container zum instanziieren der Klassen.
"""

CONFIG_FILE = 'config.json'

# config laden
with open(CONFIG_FILE) as fp:
    config = json.load(fp)

logging.basicConfig(level=logging.INFO)

# Annoy Index laden
index = AnnoyIndex(config['vector_length'])
index.load(config['annoy_index_path'])

# Mappings laden
with open(config['annoy_id_to_imagenet_node_path']) as fp:
    annoy_id_to_node = json.load(fp)

with open(config['imagenet_labels_path']) as fp:
    imagenet_labels = json.load(fp)

# spaCy model laden
logging.info('begin loading word vectors')
nlp = spacy.load('en_core_web_md')
# Fix für fehlende Stopwords im Modell
nlp.vocab.add_flag(lambda s: s in spacy.en.word_sets.STOP_WORDS, spacy.attrs.IS_STOP)
logging.info('word vectors loaded')

# repositories
key_frame_repository = KeyFrameRepository(config['key_frame_directory'], config['db_host'], config['db_port'])
video_repository = VideoRepository(config['upload_directory'], config['video_directory'], config['db_host'], config['db_port'])

# services
imagenet_node_service = ImagenetNodeService(index, annoy_id_to_node, imagenet_labels)
interference_service = InferenceService(config['inference_server_address'])

key_frame_extractor = CvKeyFrameExtractor()
key_frame_extraction_service = KeyFrameExtractionService(key_frame_extractor, config['batch_size'])

search_service = SearchService(imagenet_node_service, key_frame_repository, nlp)
video_object_recognition_service = VideoObjectRecognitionService(interference_service, key_frame_extraction_service,
                                                                 key_frame_repository, video_repository)
video_upload_service = VideoUploadService(video_object_recognition_service, video_repository)

# controllers
search_controller = SearchController(search_service)
video_controller = VideoController(video_upload_service)
static_controller = StaticController()
