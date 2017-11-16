from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Weather


# Create your views here.


def get_url(url):
    rep = requests.get(url, timeout=60)
    rep.encoding = 'utf-8'
    return rep.text


def get_data(htmltext):
    content = []
    bs = BeautifulSoup(htmltext, "html.parser")
    body = bs.body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    li = ul.find_all('li')
    for day in li:
        line = []
        date = day.find('h1').string
        line.append(date)
        text = day.find_all('p')
        line.append(text[0].string)
        if text[1].find('span') is None:
            temperature_h = None
        else:
            temperature_h = text[1].find('span').string.replace("℃", '')
        temperature_l = text[1].find('i').\
            string.replace("℃", '')
        line.append(temperature_h)
        line.append(temperature_l)
        content.append(line)
    return content


def index(request):
    url = "http://www.weather.com.cn/weather/101270101.shtml"
    html = get_url(url)
    results = get_data(html)
    Weather.objects.all().delete()
    for result in results:
        cdu = Weather()
        cdu.date = result[0]
        cdu.weather = result[1]
        cdu.temperature_h = result[2]
        cdu.temperature_l = result[3]
        cdu.save()
    weathers = Weather.objects.all()
    categories = []
    temperature_H = []
    temperature_L = []
    for weather in weathers:
        date = weather.date
        climate = weather.weather
        categorie = date + str(climate)
        temperature_1 = weather.temperature_h
        temperature_2 = weather.temperature_l
        categories.append(categorie)
        if temperature_1 is not None:
            temperature_H.append(int(temperature_1))
        else:
            temperature_H.append('')
        temperature_L.append(int(temperature_2))
    return render(request, 'index.html', {
        'categories': categories,
        'temperature_H': temperature_H,
        'temperature_L': temperature_L,
    })
