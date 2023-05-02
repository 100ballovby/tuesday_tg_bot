from jinja2 import Template
import requests as r
import os
import random


def make_template(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        template_text = f.read()
    template = Template(template_text)
    return template


def send_image():
    content = r.get('https://random.dog/woof.json').json()
    img_url = content['url']
    return img_url


def send_meme():
    response = r.get('https://api.imgflip.com/get_memes').json()
    r_meme = random.choice(response['data']['memes'])
    return r_meme['url']
