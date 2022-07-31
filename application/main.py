from application.extensions import app, db


def init_api():
    from application.api.v1.auth.routes import bp_auth
    from application.api.v1.role.routes import bp_role

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_role)


if __name__ == '__main__':
    init_api()
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
