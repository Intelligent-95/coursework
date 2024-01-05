import os
import re
import sqlite3
import base64
import random
from routes import routes
from mimes import get_mime
from views import View
from template_engine import render_template

def get_random_product():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT product_name, description, price, photo, category FROM Products ORDER BY RANDOM() LIMIT 1")
    product = cursor.fetchone()

    cursor.close()
    conn.close()

    return product  # Возвращает кортеж

random_item = get_random_product()

photo_data = random_item[3] 
photo_base64 = base64.b64encode(photo_data).decode('utf-8')

data = {
    'product_name': random_item[0],
    'description': random_item[1],
    'price': random_item[2],
    'photo': f"data:image/jpeg;base64,{photo_base64}",  
    'category': random_item[4]
}



with open('templates/index.html', 'r', encoding='utf-8') as file:
    html_template = file.read()


rendered_html = render_template(html_template, **data)


with open('templates/main_index.html', 'w', encoding='utf-8') as file:
    file.write(rendered_html)










def load(file_name):
    f = open(file_name, encoding='utf-8')
    data = f.read()
    f.close()
    return data

def app(environ, start_response):
    """
    (dict, callable( status: str,
                     headers: list[(header_name: str, header_value: str)]))
                  -> body: iterable of strings_
    """
    url = environ['REQUEST_URI']
    for key in routes.keys():
        print('url', url, 'key', key)
        if re.match(key, url) is not None:
            view = routes[key](url)
    resp = view.response()
    # Возвращаем HTTP-ответ с сгенерированной страницей
    status = resp.status#'200 OK'
    #file_name = route(environ['REQUEST_URI'])
    response_headers = resp.headers
    start_response(status, response_headers)
    return [bytes(resp.data, "utf-8")]
   
 