# Interactive plot of simple vector features (points) with Bokeh and
# GeoPandas
# Data used: Properties in Care in Scotland
# (<https://portal.historicenvironment.scot/downloads/propertiesincare>)

# import libraries
import geopandas as gpd
from bokeh.io import output_notebook
from bokeh.models import CategoricalColorMapper, GeoJSONDataSource
from bokeh.palettes import viridis
from bokeh.plotting import figure, show
from bokeh.tile_providers import CARTODBPOSITRON_RETINA, get_provider

# set inline plots
output_notebook()

# specify map tile provider
tile_provider = get_provider(CARTODBPOSITRON_RETINA)

# import data
data = gpd.read_file("data/pic/properties_in_care.shp")

# reproject to web mercator
data = data.to_crs(3857)

# convert data source to GeoJSON
geo_source = GeoJSONDataSource(geojson=data.to_json())

# generate unique colours for each local authority
const = list(set(data["LOCAL_AUTH"]))
palette = viridis(len(const))
color_map = CategoricalColorMapper(factors=const, palette=palette)

# define title and tooltips
TITLE = (
    "Properties in Care in Scotland. © Historic Environment Scotland 2021."
)

TOOLTIPS = [
    ("NAME", "@PIC_NAME"),
    ("LOCAL_AUTH", "@LOCAL_AUTH"),
    ("COORDINATES", "(@X, @Y)"),
    ("ID", "@PIC_ID")
]

# configure plot
p = figure(
    title=TITLE,
    tools="wheel_zoom, pan, reset, hover, save",
    x_axis_location=None,
    y_axis_location=None,
    tooltips=TOOLTIPS,
    x_axis_type="mercator",
    y_axis_type="mercator"
)

p.grid.grid_line_color = None

p.hover.point_policy = "follow_mouse"

p.circle(
    "x",
    "y",
    source=geo_source,
    size=5,
    line_width=0,
    fill_color={"field": "LOCAL_AUTH", "transform": color_map}
)

p.add_tile(tile_provider)

# display plot
show(p)
