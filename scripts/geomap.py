# %%
# import libraries
from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
from bokeh.io import output_file, save
from bokeh.embed import components
from bokeh.palettes import viridis
from pyproj import Proj, transform
import pandas as pd
import os

# %%
# download weather station data from german meteorological service
# os.system('python scripts/dwd_stations.py')

# %%
# load the data
# german meteorological stations
data = pd.read_csv('data/stations.txt')

# %%
# transform latitudes and longitudes from wgs84 to web mercator projection
lons = tuple(data['longitude'])
lats = tuple(data['latitude'])
wgs84 = Proj('epsg:5243')
web = Proj('epsg:3857')
lons, lats = wgs84(lons, lats)
xm, ym = transform(wgs84, web, lons, lats)
data['mercator_x'] = xm
data['mercator_y'] = ym

# %%
# generate unique colours for each state
states = list(set(data['state']))
palette = viridis(len(states))
color_map = CategoricalColorMapper(factors=states,
    palette=palette)

# %%
# create dictionary of source data for geo map
geo_source = ColumnDataSource(data)

# %%
# define map tooltips
TOOLTIPS = [
    ('Station', '@name'), ('id', '@id'), ('Height', '@height'),
    ('State', '@state'), ('(Lon, Lat)', '(@longitude, @latitude)')
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
p.circle(source=geo_source, x='mercator_x', y='mercator_y',
    color={'field': 'state', 'transform': color_map})

# %%
# output the geomap
output_file('archive/geomap.html')
save(p)

# %%
# to export script and div components
script, div = components(p)
script = script.replace('<script type="text/javascript">', '')
script = script.replace('</script>', '')

with open('charts/bokeh/geomap.js', 'w') as f:
    print(script, file=f)
with open('charts/bokeh/geomap-div.js', 'w') as f:
    print('document.write(`' + div + '\n`);', file=f)
