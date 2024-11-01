import re
import argparse


def parse_input_file(input_file):
    with open(input_file, 'r') as file:
        data = file.read()

    # Разделяем секции
    sections = data.split('---')
    server_name = sections[0].strip().split(':')[1].strip()  # Извлекаем имя сервера
    proxy_pass = sections[1].strip().split(':', 1)[1].strip()  # Извлекаем значение proxy_pass
    vars_section = sections[2].strip()
    endpoints_section = sections[3].strip()

    # Парсим переменные
    vars_dict = parse_vars(vars_section)

    # Парсим конечные точки
    endpoints = parse_endpoints(endpoints_section)

    return server_name, proxy_pass, vars_dict, endpoints


def parse_vars(vars_section):
    vars_dict = {}
    # Находим переменные по шаблону
    pattern = r'\{([^}]+)\}=(.+)'
    matches = re.findall(pattern, vars_section)

    for key, value in matches:
        vars_dict[key] = value.strip()

    return vars_dict


def parse_endpoints(endpoints_section):
    endpoints = {}
    lines = endpoints_section.splitlines()

    for line in lines:
        line = line.strip()  # Убираем лишние пробелы
        if not line:  # Пропускаем пустые строки
            continue
        if ' ' not in line:  # Пропускаем строки, которые не содержат метода и пути
            print(f"Пропущена некорректная строка: {line}")
            continue
        method, path = line.split(maxsplit=1)
        if method not in endpoints:
            endpoints[method] = []
        endpoints[method].append(path.strip())

    return endpoints


def generate_regex(variable_name, variable_value):
    """Генерирует регулярное выражение на основе значения переменной."""
    if variable_value.endswith('m'):  # Пример: {period}=1m
        return r'\d+m'  # Период в минутах
    elif re.match(r'^\d{4}-\d{2}-\d{2}$', variable_value):  # Пример: {date}=2019-05-12
        return r'\d{4}-\d{2}-\d{2}'  # Дата в формате YYYY-MM-DD
    elif re.match(r'^[a-zA-Z0-9-]+$', variable_value):  # Пример: {security}=GAZP
        return r'[a-zA-Z0-9-]+'  # Алфавитно-цифровое значение
    elif re.match(r'^\d+$', variable_value):  # Пример: {id}=2411
        return r'\d+'  # Целое число
    else:
        return r'.*'  # Любое значение по умолчанию


def replace_vars_with_regex(path, vars_dict):
    # Заменяем переменные на соответствующие регулярные выражения
    pattern = r'\{([^}]+)\}'

    def replacer(match):
        var_name = match.group(1)
        if var_name in vars_dict:
            # Генерируем регулярное выражение на основе значения переменной
            return f"({generate_regex(var_name, vars_dict[var_name])})"
        return match.group(0)  # Если переменная не найдена, возвращаем её как есть

    return re.sub(pattern, replacer, path)


def generate_nginx_config(server_name, proxy_pass, vars_dict, endpoints):
    config_lines = [f"server {{\n    server_name {server_name};\n"]
    location_count = 0
    method_count = {method: 0 for method in endpoints.keys()}

    # Добавляем блоки location для каждого метода и пути
    for method, paths in endpoints.items():
        for path in paths:
            # Заменяем переменные на соответствующие регулярные выражения
            regex_path = replace_vars_with_regex(path, vars_dict)
            # Генерация блока location с директивой limit_except
            location_block = f"    location ~ ^/{regex_path} {{\n"
            location_block += f"        limit_except {method} {{ deny all; }}\n"
            location_block += f"        proxy_pass {proxy_pass};\n"  # Исправлено
            location_block += "    }\n"
            config_lines.append(location_block)

            # Увеличиваем счётчик местоположений и методов
            location_count += 1
            method_count[method] += 1

    config_lines.append("}\n")

    return ''.join(config_lines), location_count, method_count


def main():
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Генерация конфигурации NGINX из файла.')
    parser.add_argument('input_file', nargs='?', type=str, help='Путь к входному файлу с локейшенами.')
    parser.add_argument('output_file', nargs='?', type=str, help='Путь для сохранения конфигурации NGINX.')

    args = parser.parse_args()

    # Если аргументы не переданы, запрашиваем у пользователя
    if not args.input_file:
        args.input_file = input("Введите путь к входному файлу: ")
    if not args.output_file:
        args.output_file = input("Введите путь для сохранения конфигурации NGINX: ")

    server_name, proxy_pass, vars_dict, endpoints = parse_input_file(args.input_file)
    nginx_config, location_count, method_count = generate_nginx_config(server_name, proxy_pass, vars_dict, endpoints)

    with open(args.output_file, 'w') as file:
        file.write(nginx_config)

    # Выводим информацию о созданных блоках
    print(f"Создано {location_count} блоков location.")
    for method, count in method_count.items():
        print(f"Метод {method}: {count} блок(ов).")


if __name__ == "__main__":
    main()
