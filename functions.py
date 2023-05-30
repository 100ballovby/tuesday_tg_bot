from jinja2 import Template
import requests as r
import os
import random
import datetime as dt


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


def get_weather(lat, lon):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'lat': lat,
        'lon': lon,
        'appid': os.environ.get('WEATHER_KEY'),
        'units': 'metric',
        'lang': 'ru',
    }
    response = r.get(url, params=params).json()
    text = '🗓️<strong>{}</strong> <i>{}</i>:\n{}°C, {}\n\n'
    resp = ''
    for data in response['list']:
        date = dt.datetime.fromtimestamp(data['dt'])
        date_res = date.strftime('%d.%m.%Y')
        temp = data['main']['temp']
        weather = data['weather'][0]['description']

        if date.hour == 12:
            daytime = 'днём'
            resp += text.format(date_res, daytime, temp, weather)
        elif date.hour == 21:
            daytime = 'вечером'
            resp += text.format(date_res, daytime, temp, weather)
    return resp


def get_horo(sign):
    url = f"https://horoscopes-ai.p.rapidapi.com/get_horoscope_en/{sign}/tomorrow/general"
    print(url)
    headers = {
        "X-RapidAPI-Key": "4b3d784309msh1a54be2ab333712p1f580cjsn967b22d81802",
        "X-RapidAPI-Host": "horoscopes-ai.p.rapidapi.com"
    }
    response = r.get(url, headers=headers)
    res = response.json()
    return res['general'][0]

