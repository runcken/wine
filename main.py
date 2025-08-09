import argparse
import os
import datetime
from collections import defaultdict
from dotenv import load_dotenv
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


if __name__ == '__main__':
    foundation_date = 1920
    now = datetime.datetime.now()
    time_period = now.year - foundation_date

    time_period = int(time_period)

    last_two = time_period % 100
    last_digit = time_period % 10
    if 11 <= last_two <= 14:
        time_period_text = f'{time_period} лет'
    elif last_digit == 1:
        time_period_text = f'{time_period} год'
    elif 2 <= last_digit <= 4:
        time_period_text = f'{time_period} года'
    else:
        time_period_text = f'{time_period} лет'

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
        '--xlsx_file_name',
        type=str,
        default=xlsx_file,
        help=f'id запуска(по умолчанию: {xlsx_file})'
        )
    args = parser.parse_args()
    xlsx_file_name = args.xlsx_file_name

    wines = pandas.read_excel(
        xlsx_file_name,
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
        time_period=time_period_text
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
