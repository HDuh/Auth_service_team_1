## Схема БД:

![изображение](https://user-images.githubusercontent.com/66841202/192105634-dd904822-c824-4242-92d4-e4c6d427d104.png)

Запуск проекта
> make run

Применение миграций и заполнение БД данными(базовые роли и пермишены):
> make init_db 

Создание супер пользователя:
> make create_super_user password="your password"

Swagger документация API
> http://localhost/swagger-ui/

Миграции и команды
 - Инициализация базовых ролей и пермишенов: `flask fill-db`
 - Создание суперпользователя: `flask create-root password`
 - Создать файл с миграцией: `flask db migrate -m "migration massage"`
 - Применить миграцию: `flask db upgrade`
