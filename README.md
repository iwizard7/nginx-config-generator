# Генератор конфигурации NGINX ⚙️

Этот скрипт генерирует конфигурацию NGINX на основе входного файла, содержащего информацию о переменных и конечных точках API. Скрипт поддерживает использование регулярных выражений для динамической замены переменных и создания блоков `location` с соответствующими методами.

## Описание формата входного файла

Входной файл должен содержать следующие секции, разделенные тройными дефисами (`---`):

1. **Имя сервера**: строка с именем сервера.
2. **Переменные**: переменные в формате `{variable_name}=value`, где `value` может содержать специальные символы.
3. **Конечные точки**: строки, начинающиеся с метода (например, `GET`, `POST`) и содержащие путь к API.

### Пример входного файла
```
server_name: test-server.com
---
vars: 
{envname1}=419863-049523 
{envname2}=5944223432 
{date}=2019-05-12
---
POST api/account/signinstage 
GET api/account/current 
POST api/clients/find GET api/info
```
## Установка

Скрипт написан на Python. Убедитесь, что Python установлен на вашем компьютере. Для проверки версии Python выполните команду:

```bash
python --version
```
## Использование
Скрипт запускается из командной строки с передачей двух аргументов: путь к входному файлу и путь для сохранения выходного файла.
Также можно просто запустить скрипт и использовать в интерактивном режиме, отвечая на вопросы.
## Команда запуска
```bash
python generate_nginx_config.py input_file.txt output_nginx.conf
```
input_file.txt: путь к вашему входному файлу с локейшенами.
output_nginx.conf: путь к выходному файлу, в который будет сохранена сгенерированная конфигурация NGINX.

## Пример использования

### С использованием аргументов командной строки:
```bash
python generate_nginx_config.py input_file.txt output_nginx.conf
```
### Интерактивно (без аргументов):
```bash
python generate_nginx_config.py
```
При запуске без аргументов вас попросят ввести путь к входному и выходному файлам.

```
## Вывод
После успешного выполнения скрипта вы получите сгенерированную конфигурацию NGINX в указанном выходном файле. В консоли также будет выведена информация о количестве созданных блоков location и количестве каждого метода:
```yaml
Создано 5 блоков location.
Метод GET: 2 блок(ов).
Метод POST: 3 блок(ов).
```
## Зависимости

Скрипт использует стандартные библиотеки Python, поэтому дополнительных зависимостей не требуется.

## Лицензия

Этот проект лицензирован под лицензией MIT. Пожалуйста, см. файл LICENSE для получения дополнительной информации.

### Как Пользоваться

1. **Создайте входной файл**: Сформируйте файл с нужной информацией в формате, описанном выше.
2. **Сохраните скрипт**: Убедитесь, что у вас есть скрипт `generate_nginx_config.py` в доступном каталоге.
3. **Запустите скрипт**: Используйте команду в терминале, как указано в разделе "Использование".
4. **Проверьте выходной файл**: Откройте выходной файл, чтобы убедиться, что конфигурация сгенерирована корректно.
