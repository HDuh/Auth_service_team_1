from gevent import monkey

from app.core.config import Config

monkey.patch_all()

from dotenv import load_dotenv  # noqa

load_dotenv()

from gevent.pywsgi import WSGIServer
from main import app, main

http_server = WSGIServer(("", Config.FLASK_PORT), main(app))
http_server.serve_forever()
