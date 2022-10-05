from extensions import jwt, cache


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(_, decrypted_token):
    return cache.get(decrypted_token['jti']) is not None
