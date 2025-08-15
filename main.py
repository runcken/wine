import argparse
import datetime
import os
from collections import defaultdict
from dotenv import load_dotenv
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_path(filename):
    parser = argparse.ArgumentParser(
        description='Вывод списка продукции на сайте'
    )

    parser.add_argument(
        '--path',
        type=str,
        default=filename,
        help=f'путь к файлу(по умолчанию: {filename})'
    )

    args = parser.parse_args()
    path = args.path
    return path


def get_winery_age_text():
    foundation_date = 1920
    now = datetime.datetime.now()
    winery_age = now.year - foundation_date

    last_two = winery_age % 100
    last_digit = winery_age % 10
    if 11 <= last_two <= 14:
        winery_age_text = f'{winery_age} лет'
    elif last_digit == 1:
        winery_age_text = f'{winery_age} год'
    elif 2 <= last_digit <= 4:
        winery_age_text = f'{winery_age} года'
    else:
        winery_age_text = f'{winery_age} лет'
    return winery_age_text


def get_rendered_page(wines, template, winery_age):
    grouped_wines = defaultdict(list)

    for row in wines.to_dict('records'):
        category = row[wines.columns[0]]
        grouped_wines[category].append(row)

    rendered_page = template.render(
        grouped_wines=grouped_wines,
        winery_age=winery_age
    )

    return rendered_page


def main():
    load_dotenv()
    filename = os.getenv('INPUT_FILE')

    wines = pandas.read_excel(
        get_path(filename),
        sheet_name='Лист1',
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )

    winery_age = get_winery_age_text()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(get_rendered_page(wines, template, winery_age))

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
