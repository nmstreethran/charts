# %%
# import libraries
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
from bokeh.io import output_file, save
from bokeh.models import ColumnDataSource
from pyproj import Proj, transform
import json
import os

# %%
# download weather station geojson data from german meteorological service
# warning! this step utilises the dwdweather2 library (python 2)
# installation: pip install dwdweather2
# https://pypi.org/project/dwdweather2/
os.system('dwdweather stations --type geojson > data/stations.geojson')

# %%
# load the data
# german meteorological stations
with open('data/stations.geojson') as src:
    data = json.load(src)

# %%
# create empty lists to store data
# latitudes, longitudes, station ids and station names
lats = []
lons = []
ids = []
names = []

# %%
# extract geojson data and input into lists
for feature in data['features']:
    for idx, coord in enumerate(feature['geometry']['coordinates']):
        if idx == 0:
            lats.append(coord)
        else:
            lons.append(coord)
    ids.append(feature['properties']['id'])
    names.append(feature['properties']['name'])

# %%
# transform latitudes and longitudes from wgs84 to web mercator projection
wgs84 = Proj('epsg:4326')
web = Proj('epsg:3857')
lat, lon = transform(wgs84, web, lons, lats)

# %%
# create dictionary of source data for geo map
geo_source = ColumnDataSource(
    {
        'x': lat,
        'y': lon,
        'name': names,
        'id': ids,
        'lat': lats,
        'lon': lons,
        }
    )

# %%
# define map tooltips
TOOLTIPS = [
    ('Station', '@name'), ('id', '@id'), ('(Long, Lat)', '(@lon, @lat)')
]

# %%
# set figure title, tooltips and axis types
# set axis types to mercator so that latitudes and longitudes are used
# in the figure
p = figure(title='German Meteorological Stations. Data: dwd.de.',
    x_axis_type='mercator', y_axis_type='mercator', tooltips=TOOLTIPS)

# set openstreetmaps overlay
p.add_tile(get_provider(Vendors.CARTODBPOSITRON_RETINA))

# add data points
p.circle(source=geo_source, x='x', y='y')

# %%
# output the geomap and save the html file
output_file('charts/bokeh/geomap.html')
save(p)
