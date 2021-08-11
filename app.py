import random
import pandas as pd
import folium
from folium import IFrame
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_table_experiments as dt
import webbrowser
from PIL import Image
import requests

# Define popup
encoded = base64.b64encode(requests.get('https://gamingtrend.com/wp-content/uploads/2020/05/feature-2-e1589992535441.jpg', stream=True).raw.read())
html = '<img src="data:image/png;base64,{}">'.format

iframe1 = IFrame(html(encoded.decode('UTF-8')), width=200, height=200)
popup1 = folium.Popup(iframe1, max_width=250)

iframe2 = IFrame(html(encoded.decode('UTF-8')), width=200, height=200)
popup2 = folium.Popup(iframe2, max_width=250)

iframe3 = IFrame(html(encoded.decode('UTF-8')), width=200, height=200)
popup3 = folium.Popup(iframe3, max_width=250)

# Assets
cities = [dict(name="Aalborg", lat=57.0268172, lon=9.837735, popup=popup1),
          dict(name="Aarhus", lat=56.1780842, lon=10.1119354, popup=popup2),
          dict(name="Copenhagen", lat=55.6712474, lon=12.5237848, popup=popup3)]

cities_pd = pd.DataFrame.from_dict(cities)

# Basemap
m = folium.Map(location=[45.5236, 0], tiles='https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>', zoom_start=2.5)

# Create markers with popup
for i in range(0,len(cities_pd)):
    folium.Marker(location=[cities_pd.iloc[i]['lat'], cities_pd.iloc[i]['lon']],
       icon=folium.Icon(color = 'blue'),
       tooltip=cities_pd.iloc[i]['name'], popup=cities_pd.iloc[i]['popup']).add_to(m)

loc = '<br>Fantastic Urban Life Series'
title_html = '''
             <h3 align="center" style="font-size:30px; color: white; background-size : 600px 300px ; background-image: url('https://c4.wallpaperflare.com/wallpaper/131/578/547/pixel-art-town-city-waneella-hd-wallpaper-preview.jpg'); margin : 0; height: 90px"><b>{}</b></h3>
             '''.format(loc)   

m.get_root().html.add_child(folium.Element(title_html))
html_string = m.get_root().render()

import dash_html_components as html
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(style={
    #'background-image': 'url("assets/pic.png")',
    'backgroundColor' : 'grey',
    'background-repeat': 'no-repeat',
    'background-position': 'top',
    'background-size': '150px 100px'},
    children=[html.Iframe(id = 'map', srcDoc = html_string, width='100%', height='900')])

if __name__ == '__main__':
    app.run_server()
