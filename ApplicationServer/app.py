# coding=utf-8
import falcon
import container

"""
Einstiegspunkt für die Anwendung. Die Anwendung muss mit einem WSGI-Server gestartet werden.
"""

api = application = falcon.API()

api.add_route('/videos', container.video_controller)
api.add_route('/search', container.search_controller)
api.add_route('/static/{filename}', container.static_controller)  # {filename} für ein Wildcard-Routing
