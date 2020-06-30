# import libraries
from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
from bokeh.io import output_file, show
from bokeh.embed import components
from bokeh.palettes import viridis
from pyproj import Transformer
import pandas as pd

"""

# download weather station CSV data from German meteorological service
# Warning! this step utilises the dwdweather2 library (Python 2)
# https://pypi.org/project/dwdweather2/
# create and activate new virtual environment for this library alone
# ... and then install dwdweather2 (recommended)
pip install dwdweather2

# download CSV
dwdweather stations --type csv > dwd_stations.csv
"""

# load the data
# German meteorological stations
data = pd.read_csv('data/dwd_stations.txt')

# transform latitudes and longitudes from wgs84 to web mercator projection
lons = tuple(data['longitude'])
lats = tuple(data['latitude'])
transformer = Transformer.from_crs(
    'epsg:4326', 'epsg:3857', always_xy=True)
xm, ym = transformer.transform(lons, lats)
data['mercator_x'] = xm
data['mercator_y'] = ym

# generate unique colours for each state
states = list(set(data['state']))
palette = viridis(len(states))
color_map = CategoricalColorMapper(factors=states,
    palette=palette)

# create dictionary of source data for geo map
geo_source = ColumnDataSource(data)

# define map tooltips
TOOLTIPS = [
    ('Station', '@name'), ('id', '@id'), ('Height', '@height'),
    ('State', '@state'), ('(Lon, Lat)', '(@longitude, @latitude)')
]

# set figure title, tooltips and axis types
# set axis types to mercator so that latitudes and longitudes are used
# in the figure
p = figure(title='German Meteorological Stations. Data: dwd.de.',
    x_axis_type='mercator', y_axis_type='mercator', tooltips=TOOLTIPS)

# set OpenStreetMap overlay
p.add_tile(get_provider(Vendors.CARTODBPOSITRON_RETINA))

# add data points
p.circle(source=geo_source, x='mercator_x', y='mercator_y',
    color={'field': 'state', 'transform': color_map})

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
with open('charts/bokeh/geomap.js', 'w') as f:
    print(script, file=f)
# export div as HTML file
with open('charts/bokeh/geomap-div.html', 'w') as f:
    print(div, file=f)
# export div as JavaScript file (so that it can be read by geomap.html)
with open('charts/bokeh/geomap-div.js', 'w') as f:
    print('document.write(`' + div + '\n`);', file=f)
