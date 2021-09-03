# Interactive plot of simple vector features (polygons) with Bokeh and
# GeoPandas
# Data used: Boundary-Line™
# (<https://osdatahub.os.uk/downloads/open/BoundaryLine>)

# import libraries
import geopandas as gpd
from bokeh.io import output_notebook
from bokeh.models import (
    CategoricalColorMapper, LogColorMapper, GeoJSONDataSource
)
from bokeh.palettes import viridis
from bokeh.plotting import figure, show
from bokeh.tile_providers import CARTODBPOSITRON_RETINA, get_provider

# set inline plots
output_notebook()

# specify map tile provider
tile_provider = get_provider(CARTODBPOSITRON_RETINA)

# import data
data = gpd.read_file(
    "data/os_bdline/data/bdline_gb.gpkg", layer="greater_london_const"
)
data["Name"] = data["Name"].str.slice(stop=-18)

# view data
data.head(5)

# reproject to web mercator
data = data.to_crs(3857)

# convert data source to GeoJSON
geo_source = GeoJSONDataSource(geojson=data.to_json())

# Categorical
# generate unique colours for each constituency
const = list(set(data["Name"]))
palette = viridis(len(const))
color_map = CategoricalColorMapper(factors=const, palette=palette)

# define plot title
TITLE = (
    "Greater London Constituencies. Contains OS Data" +
    " © Crown copyright and database right 2021."
)

# configure plot
p = figure(
    title=TITLE,
    tools="wheel_zoom, pan, reset, hover, save",
    x_axis_location=None,
    y_axis_location=None,
    tooltips=[("Name", "@Name"), ("Hectares", "@Hectares")],
    x_axis_type="mercator",
    y_axis_type="mercator"
)

p.grid.grid_line_color = None

p.hover.point_policy = "follow_mouse"

p.patches(
    "xs",
    "ys",
    source=geo_source,
    fill_color={"field": "Name", "transform": color_map},
    line_color="white",
    line_width=.5,
    fill_alpha=.7
)

p.add_tile(tile_provider)

# display plot
show(p)

# Choropleth
color_map = LogColorMapper(palette=palette)

# configure plot
p = figure(
    title=TITLE,
    tools="wheel_zoom, pan, reset, hover, save",
    x_axis_location=None,
    y_axis_location=None,
    tooltips=[("Name", "@Name"), ("Hectares", "@Hectares")],
    x_axis_type="mercator",
    y_axis_type="mercator"
)

p.grid.grid_line_color = None

p.hover.point_policy = "follow_mouse"

p.patches(
    "xs",
    "ys",
    source=geo_source,
    fill_color={"field": "Hectares", "transform": color_map},
    line_color="white",
    line_width=.5,
    fill_alpha=.7
)

p.add_tile(tile_provider)

# display plot
show(p)
