from application.core import Config
from application.extensions import app, db


def init_api():
    from application.api.v1.auth.routes import bp_auth
    from application.api.v1.role.routes import bp_role

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_role)


def init_permissions():
    from application.models import Permission

    base_role_permissions = [Permission(permission_name=permission) for permission in Config.BASE_PERMISSIONS]
    db.session.bulk_save_objects(base_role_permissions)
    db.session.commit()


if __name__ == '__main__':
    init_api()
    db.create_all()
    init_permissions()
    app.run(debug=True, host='0.0.0.0', port=5001)
