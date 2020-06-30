# import libraries
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from pyproj import Transformer
import json

"""

# download weather station GeoJSON data from German meteorological service
# warning! this step utilises the dwdweather2 library (Python 2)
# https://pypi.org/project/dwdweather2/
# create and activate new virtual environment for this library alone
# ... and then install dwdweather2 (recommended)
pip install dwdweather2

# download GeoJSON
dwdweather stations --type geojson > dwd_stations.geojson
"""

# load the data
# German meteorological stations
with open('data/dwd_stations.geojson') as src:
    data = json.load(src)

# create empty lists to store data
# latitudes, longitudes, station ids and station names
lats = []
lons = []
ids = []
names = []

# extract GeoJSON data and input into lists
for feature in data['features']:
    for idx, coord in enumerate(feature['geometry']['coordinates']):
        if idx == 0:
            lons.append(coord)
        else:
            lats.append(coord)
    ids.append(feature['properties']['id'])
    names.append(feature['properties']['name'])

# transform latitudes and longitudes from wgs84 to Web Mercator projection
transformer = Transformer.from_crs(
    'epsg:4326', 'epsg:3857', always_xy=True)
xm, ym = transformer.transform(lons, lats)

# create dictionary of source data for geo map
geo_source = ColumnDataSource(
    {
        'x': xm,
        'y': ym,
        'name': names,
        'id': ids,
        'lats': lats,
        'lons': lons,
        }
    )

# define map tooltips
TOOLTIPS = [
    ('Station', '@name'), ('id', '@id'), ('(Lon, Lat)', '(@lons, @lats)')
]

# set figure title, tooltips and axis types
# set axis types to mercator so that latitudes and longitudes are used
# in the figure
p = figure(title='German Meteorological Stations. Data: dwd.de.',
    x_axis_type='mercator', y_axis_type='mercator', tooltips=TOOLTIPS)

# set OpenStreetMap overlay
p.add_tile(get_provider(Vendors.CARTODBPOSITRON_RETINA))

# add data points
p.circle(source=geo_source, x='x', y='y')

# output the geo map and save to a custom path
output_file('archive/geomap.html')
# open the map
show(p)

# to export script and div components
script, div = components(p)
# remove script HTML tags to save as JavaScript file
script = script.replace('<script type="text/javascript">', '')
script = script.replace('</script>', '')

# export script as JavaScript file
with open('charts/bokeh/geomap-geojson.js', 'w') as f:
    print(script, file=f)
# export div as HTML file
with open('charts/bokeh/geomap-geojson-div.html', 'w') as f:
    print(div, file=f)
# export div as JavaScript file
# (so that it can be read by geomap-geojson.html)
with open('charts/bokeh/geomap-geojson-div.js', 'w') as f:
    print('document.write(`' + div + '\n`);', file=f)
