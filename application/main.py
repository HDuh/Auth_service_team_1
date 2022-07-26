from application import create_app, app

if __name__ == '__main__':
    create_app()

    from application.core.restful_api import init_api
    init_api()

    from application.core.database import init_db
    init_db()

    app.run(debug=True, port=5001)
