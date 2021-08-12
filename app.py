import random
import pandas as pd
import folium
from folium import IFrame
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_table_experiments as dt
from PIL import Image
import requests
import gunicorn
import geopandas as gpd

# Define popup images
pic1 = base64.b64encode(requests.get('https://static.wixstatic.com/media/c2c01a_059a6f6ff779483d92e163c445931bc2~mv2_d_1536_1536_s_2.png/v1/fill/w_1052,h_1052,al_c,q_90,usm_0.66_1.00_0.01/c2c01a_059a6f6ff779483d92e163c445931bc2~mv2_d_1536_1536_s_2.webp', stream=True).raw.read())
pic2 = base64.b64encode(requests.get('https://static.wixstatic.com/media/c2c01a_38f12a7fdf5243fcb9ef129718cfca8f~mv2_d_1280_1280_s_2.png/v1/fill/w_1052,h_1052,al_c,q_90,usm_0.66_1.00_0.01/c2c01a_38f12a7fdf5243fcb9ef129718cfca8f~mv2_d_1280_1280_s_2.webp', stream=True).raw.read())
pic3 = base64.b64encode(requests.get('https://static.wixstatic.com/media/c2c01a_a24481cf492e4393a62b6cbc1a7d9749~mv2_d_1536_1536_s_2.png/v1/fill/w_1052,h_1052,al_c,q_90,usm_0.66_1.00_0.01/c2c01a_a24481cf492e4393a62b6cbc1a7d9749~mv2_d_1536_1536_s_2.webp', stream=True).raw.read())
html = '<img src="data:image/png;base64,{}" style="width:100%; height:100%;">'.format

popup1 = folium.Popup(IFrame(html(pic1.decode('UTF-8')), width=200, height=200), max_width=250)
popup2 = folium.Popup(IFrame(html(pic2.decode('UTF-8')), width=200, height=200), max_width=250)
popup3 = folium.Popup(IFrame(html(pic3.decode('UTF-8')), width=200, height=200), max_width=250)

# Define stops
cities = [dict(name="Paris - Ile de la cité", lat=48.8534, lon=2.3488, popup=popup1, color='red'),
          dict(name="Arles", lat=43.684986, lon=4.631418, popup=popup2, color='gray'),
          dict(name="Montestruq", lat=43.432742, lon=-0.809565, popup=popup3, color='gray')]

cities_pd = pd.DataFrame.from_dict(cities)

# Define paths
url = "https://raw.githubusercontent.com/alexchunet/bcac_pixart/main/assets/paths.geojson"
paths = gpd.read_file(url)

# Basemap
m = folium.Map(location=[45.5236, 0], tiles='https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>', zoom_start=5)

# Create markers with popup and links
for i in range(0,len(cities_pd)):
    folium.Marker(location=[cities_pd.iloc[i]['lat'], cities_pd.iloc[i]['lon']],
       icon=folium.Icon(color = cities_pd.iloc[i]['color'], icon='glyphicon-record'),
       tooltip=cities_pd.iloc[i]['name'], popup=cities_pd.iloc[i]['popup']).add_to(m)

for i in range(0,len(paths)):
    folium.Choropleth(
        paths.iloc[i]['geometry'],
        line_weight=3,
        line_color=paths.iloc[i]['color']).add_to(m)

# Add title
loc = '<br>Fantastic Urban Life Series'
title_html = '''
             <h3 align="center" style="font-family: Gill Sans; font-size:30px; color: black; -webkit-text-stroke: 1px white; text-shadow: 1px 1px 3px white; background-size : 1000px 300px ; background-image: url('https://c4.wallpaperflare.com/wallpaper/131/578/547/pixel-art-town-city-waneella-hd-wallpaper-preview.jpg'); margin : 0; height: 90px"><b>{}</b></h3>
             '''.format(loc)   

m.get_root().html.add_child(folium.Element(title_html))
html_string = m.get_root().render()

# Configure and run app
import dash_html_components as html
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

app.layout = html.Div(style={
    #'background-image': 'url("assets/pic.png")',
    #'backgroundColor' : 'grey',
    #'background-repeat': 'no-repeat',
    #'background-position': 'top',
    #'background-size': '150px 100px',
    'margin': '0'},
    children=[html.Iframe(id = 'map', srcDoc = html_string, width='100%', height='900')])

if __name__ == '__main__':
    app.run_server()
