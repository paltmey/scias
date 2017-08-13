import falcon
from controllers import InferenceController
from services import InferenceService

"""
Einstiegspunkt in den Inference Server. Die Anwendung muss mit einem WSGI-Server gestartet werden.
"""


api = application = falcon.API()

inference_service = InferenceService()
inference_controller = InferenceController(inference_service)

api.add_route('/classify_image', inference_controller)
