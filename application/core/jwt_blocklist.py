import os

import redis

from application.extensions import jwt

jwt_redis_blocklist = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    db=0,
    decode_responses=True
)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(_, decrypted_token):
    jti = decrypted_token['jti']
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
