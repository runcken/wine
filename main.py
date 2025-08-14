import argparse
import datetime
import os
from collections import defaultdict
from dotenv import load_dotenv
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


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


def get_rendered_page(path, template):
    wines = pandas.read_excel(
        path,
        sheet_name='Лист1',
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )

    grouped_wines = defaultdict(list)

    for row in wines.to_dict('records'):
        category = row[wines.columns[0]]
        grouped_wines[category].append(row)

    rendered_page = template.render(
        grouped_wines=grouped_wines,
        winery_age=get_winery_age_text()
    )

    return rendered_page


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    load_dotenv()
    xlsx_file = os.getenv('PRODUCT_FILE')

    parser = argparse.ArgumentParser(
        description='Вывод списка продукции на сайте'
    )

    parser.add_argument(
        '--path',
        type=str,
        default=xlsx_file,
        help=f'путь к файлу(по умолчанию: {xlsx_file})'
    )

    args = parser.parse_args()
    path = args.path

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(get_rendered_page(path, template))

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
