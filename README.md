# Auth service team 1
https://github.com/HDuh/Auth_service_team_1

## Схема БД:

![](db_schema.jpg)

Запуск проекта
> docker-compose up -d

Swagger документация API
> http://localhost/swagger-ui/

Миграции и команды
 - Инициализация базовых ролей и пермишенов: `flask fill-db`
 - Создание суперпользователя: `flask create-root password`
 - Создать файл с миграцией: `flask db migrate -m "migration massage"`
 - Применить миграцию: `flask db upgrade`

Запуск контейнеров необходимых для разработки
> docker-compose -f docker-compose.dev.yml up -d 

Запуск тестов
> docker-compose -f docker-compose.tests.yml up --abort-on-container-exit tests
