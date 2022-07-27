from application.main import jwt

block_list = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(_, decrypted_token):
    jti = decrypted_token['jti']
    return jti in block_list
