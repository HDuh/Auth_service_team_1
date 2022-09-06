from flask import url_for,session,redirect
from flask_restful import Resource

from application.extensions import google
from application.models import Client, User


class Google(Resource):
    def get(self):
        redirect_uri = url_for('auth.googleauth', _external=True)
        return google.authorize_redirect(redirect_uri)

class GoogleAuth(Resource):
    def get(self):
        token = google.authorize_access_token()
        userinfo = token['userinfo']
        session['user'] = userinfo
        return redirect('/login')

# TODO: Описать провайдеров в extensions (гугл, яндекс, мейл).
# TODO: Расширить таблицу юзера (добавить флаг регистрации через сторонний сервис)
# TODO: Создать таблицу Провайдеров (id (уникальный идентификатор пользователя из токена SUB), user_id (FK с таблицей юзеров), provider_name)
# TODO: Связать таблицу провайдеров с таблицей юзеров (one-to-many) (user это parent)
# TODO: Проработать пайплайн авторизации:
#   1. получить токен и юзеринфо
#   2. проверить наличие провайдера в БД:
#      2.1 Если провайдер есть в БД, то получить юзера. Отдать токены
#      2.2 Если провайдера нет в БД, получить данные пользователя из токена.
#          Создать пользователя (поставить флаг, что зареган через сторонний сервис.). При смене пароля мы не запрашиваем у пользователя old_password.
#          Добавить провайдера в БД. Авторизовать пользователя (отдать токены).
