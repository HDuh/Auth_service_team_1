from application.api.v1.auth.auth import SignUp
from application.core import Config
from application.extensions import app, db, cache, docs


def init_api():
    from application.api.v1.auth.routes import bp_auth
    from application.api.v1.role.routes import bp_role

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_role)

    docs.register(SignUp, blueprint='auth')


if __name__ == '__main__':
    db.init_app(app)
    init_api()
    db.create_all()
    from application.services.permissions import init_permissions, init_default_role, cache_db

    init_permissions(db, Config)
    init_default_role(db, Config)

    cache_db(db, cache)
    app.run(debug=True, host='0.0.0.0', port=5001)
    cache.flushdb()
