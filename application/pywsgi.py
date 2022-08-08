from gevent import monkey

from app import create_app
from core import Config
from extensions import app

monkey.patch_all()
from gevent.pywsgi import WSGIServer

http_server = WSGIServer(("", Config.API_PORT), create_app(app))
http_server.serve_forever()
