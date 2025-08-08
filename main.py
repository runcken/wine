import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


if __name__ == '__main__':
    now = datetime.datetime.now()
    delta = now.year-1920

    delta = int(delta)

    last_two = delta % 100
    last_digit = delta % 10
    if 11 <= last_two <= 14:
        delta_text = f'{delta} лет'
    elif last_digit == 1:
        delta_text = f'{delta} год'
    elif 2 <= last_digit <= 4:
        delta_text = f'{delta} года'
    else:
        delta_text = f'{delta} лет'

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    wines = pandas.read_excel(
        'wine3.xlsx',
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
        time_period=delta_text
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
