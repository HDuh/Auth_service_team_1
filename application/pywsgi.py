from gevent import monkey
from gevent.pywsgi import WSGIServer

from app import create_app
from core import PROJECT_CONFIG
from extensions import app

monkey.patch_all()

http_server = WSGIServer(("", PROJECT_CONFIG.API_PORT), create_app(app))
http_server.serve_forever()
