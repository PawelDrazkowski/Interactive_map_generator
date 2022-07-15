import folium 
import pandas as pd
import numpy as np

# Population layer
fgp = folium.FeatureGroup(name = "Population")

# polygon color determination based on country's population
polygon_style = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
else 'red'}

# extraction world data from json file
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=polygon_style))

# Volcanoes layer
fgv = folium.FeatureGroup(name = "Volcanoes")

data = pd.read_csv("Volcanoes.txt")

# data extraction
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

# marker popup link definition
html_format = """
Volcano name: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

# color determination based on elevation value
def color(el):
    if el < 2000: 
        return 'green'
    elif 2000 <= el < 3000: 
        return 'orange'
    elif el >= 3000:
        return 'red' 

# markers generator
for lt, ln, el, nm in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html = html_format % (nm, nm, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, color=color(el), 
    fill=True, fill_color=color(el), popup=folium.Popup(iframe)))

# map definition
map = folium.Map(location = [np.mean(lat), np. mean(lon)], zoom_start = 6, tiles = 'Stamen Terrain')
map.add_child(fgv)
map.keep_in_front(fgv)
map.add_child(fgp)

# layer control panel
map.add_child(folium.LayerControl())

map.save("Map.html")