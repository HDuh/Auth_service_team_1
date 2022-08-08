from gevent import monkey

from application.app import create_app
from application.core import Config
from application.extensions import app

monkey.patch_all()
from gevent.pywsgi import WSGIServer

http_server = WSGIServer(("", Config.API_PORT), create_app(app))
http_server.serve_forever()
