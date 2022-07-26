from flask_jwt_extended import JWTManager

from application.main import app

jwt = JWTManager(app)

block_list = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(_, decrypted_token):
    jti = decrypted_token['jti']
    return jti in block_list
