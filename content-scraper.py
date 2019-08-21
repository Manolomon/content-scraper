#!./venv/bin/python

import os
import argparse
import requests
from bs4 import BeautifulSoup

def write_index(url, output):
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    #scripts = html.find_all('div', class_='lyrics').get_text()
    open(output + '/index.html', 'wb').write(response.content)
    download_scripts(url, output, html)
    download_images(url, output, html)
    download_styles(url, output, html)

def download_scripts(url, output, html):   
    for script in html.findAll('script', {"src":True}):
        source = script['src']
        path = output + source
        response = requests.get(url + source)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as file:
            file.write(response.content)

def download_images(url, output, html):
    for img in html.findAll('img', {"src":True}):
        source = img['src']
        path = output + source
        response = requests.get(url + source)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as file:
            file.write(response.content)

def download_styles(url, output, html):
    for style in html.findAll('link', {"rel":"stylesheet"}):
        source = style['href']
        path = output + source
        response = requests.get(url + source)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as file:
            file.write(response.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--url', required=True,
        help='El link de la página a descargar')
    parser.add_argument(
        '--output', required=True,
        help='El lugar donde se va a descargar el contenido')
    args = parser.parse_args()
    write_index(args.url, args.output)

