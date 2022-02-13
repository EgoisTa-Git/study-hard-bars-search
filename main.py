import json
import os

from flask import Flask
import folium
from geopy import distance

import geolocator

APIKEY = os.environ['API_KEY']


def get_map():
    with open('index.html', 'r', encoding='UTF-8') as file:
        return file.read()


def get_ways(nearest_cafes):
    return nearest_cafes['distance']


def main():
    with open('coffee.json', 'r', encoding='CP1251') as coffee:
        cafes = json.loads(coffee.read())
    location = geolocator.fetch_coordinates(
        APIKEY,
        input('Где Вы находитесь? '),
    )
    cafes_to_go = []
    for cafe in cafes:
        way = distance.distance(
            (location[1], location[0]),
            (cafe['Latitude_WGS84'], cafe['Longitude_WGS84']),
        ).km
        cafes_to_go.append(dict(zip([
            'title',
            'distance',
            'latitude',
            'longitude',
        ], [
            cafe['Name'],
            way,
            cafe['Latitude_WGS84'],
            cafe['Longitude_WGS84'],
        ])))
    cafe_map = folium.Map(
        location=[location[1], location[0]],
        zoom_start=16,
    )
    for nearest in sorted(cafes_to_go, key=get_ways)[:5]:
        folium.Marker(
            location=[nearest['latitude'], nearest['longitude']],
            popup=nearest['title'],
            icon=folium.Icon(color='red', icon='info-sign'),
        ).add_to(cafe_map)
    cafe_map.save('index.html')
    app = Flask(__name__)
    app.add_url_rule('/', 'hello', get_map)
    app.run('0.0.0.0')


if __name__ == '__main__':
    main()
