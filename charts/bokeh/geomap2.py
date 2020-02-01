# %%
# import libraries
from bokeh import plotting, models
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
lons_m = []
lats_m = []
lons = tuple(data['longitude'])
lats = tuple(data['latitude'])
wgs84 = Proj('epsg:26915')
web = Proj('epsg:3857')
lons, lats = wgs84(lons, lats)
lons_m, lats_m = transform(wgs84, web, lons, lats)
data['longitude_m'] = lons_m
data['latitude_m'] = lats_m

# %%
# generate unique colours for each state
states = data['state'].values.tolist()
palette = viridis(len(list(set(states))))
color_map = models.CategoricalColorMapper(factors=list(set(states)),
    palette=palette)

# %%
# create dictionary of source data for geo map
geo_source = plotting.ColumnDataSource(data)

# %%
# define map tooltips
TOOLTIPS = [
    ('Station', '@name'), ('id', '@id'), ('Height', '@height'),
    ('(Long, Lat)', '(@longitude, @latitude)')
]

# %%
# set figure title, tooltips and axis types
# set axis types to mercator so that latitudes and longitudes are used
# in the figure
p = plotting.figure(title='German Meteorological Stations. Data: dwd.de.',
    x_axis_type='mercator', y_axis_type='mercator', tooltips=TOOLTIPS)

# set openstreetmaps overlay
p.add_tile(get_provider(Vendors.CARTODBPOSITRON_RETINA))

# add data points
p.circle(source=geo_source, x='longitude_m', y='latitude_m',
    color={'field': 'state', 'transform': color_map})

# %%
# output the geomap and save the html file
output_file('charts/bokeh/geomap2.html')
save(p)

# %%
# to export script and div components
script, div = components(p)

with open('archive/geomap2_script.html', 'w') as f:
    print(script, file=f)
with open('archive/geomap2_div.html', 'w') as f:
    print(div, file=f)
