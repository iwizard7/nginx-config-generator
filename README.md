## Генератор конфигурации NGINX ⚙️

Этот скрипт на Python генерирует конфигурационные файлы для NGINX на основе заданного формата входных данных. Он поддерживает динамическое подставление переменных, заданных в секции `vars`, в пути локейшенов, создавая соответствующие регулярные выражения.

## Установка

1. Убедитесь, что у вас установлен Python 3.x. Вы можете проверить это, выполнив следующую команду:

```bash
   python --version
```
Клонируйте этот репозиторий на свой компьютер:
```bash
git clone https://github.com/iwizard7/nginx-config-generator.git
cd nginx-config-generator
```
## Использование

Сохраните входной файл с локейшенами в нужном формате. Пример формата:
```yaml
server_name:example.com
---
vars:
{envname1}=5902b97c-e5cc
{envname2}=5902b97c-e5dd
---
POST api/account/signinstage
GET api/account/current/{envname1}
```
Запустите скрипт, указав полный путь к файлу с локейшенами и путь для сохранения конфигурации:
```bash
python generate_nginx_config.py
```
Введите полный путь к файлу с локейшенами и путь для сохранения конфигурации NGINX, когда скрипт запросит это.
## Как работает скрипт

Чтение входных данных: Скрипт считывает файл, содержащий настройки сервера, переменные и конечные точки.
Парсинг переменных: Все переменные из секции vars парсятся и сохраняются в словарь.
Генерация регулярных выражений: На основе значений переменных создаются соответствующие регулярные выражения.
Генерация конфигурации: На основе методов и путей, указанных в секции конечных точек, создаются блоки location для NGINX с подставленными регулярными выражениями.
Пример конфигурации NGINX

После выполнения скрипта, сгенерированная конфигурация может выглядеть следующим образом:

```nginx
server {
    server_name example.com;

    location ~ ^/api/account/signinstage {
        proxy_pass http://backend;
    }

    location ~ ^/api/account/current/(?P<agreementId>[^/]+) {
        proxy_pass http://backend;
    }
}
```
## Лицензия

Этот проект лицензируется под лицензией MIT. Пожалуйста, смотрите файл LICENSE для подробностей.

