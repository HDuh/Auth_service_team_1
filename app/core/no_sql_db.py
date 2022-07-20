import redis

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
redis_db = redis.Redis()

