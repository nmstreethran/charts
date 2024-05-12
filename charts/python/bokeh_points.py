#!/usr/bin/env python
# coding: utf-8

# # Interactive plot of simple vector features (points) with Bokeh and GeoPandas
#
# Data used: Pilgrim Paths in Ireland (<https://data.gov.ie/dataset/pilgrim-paths>)

# import libraries
import os
from zipfile import ZipFile

import geopandas as gpd
import pooch
import xyzservices.providers as xyz
from bokeh.io import output_notebook
from bokeh.models import CategoricalColorMapper, GeoJSONDataSource
from bokeh.palettes import Category20b
from bokeh.plotting import figure, show

# set inline plots
output_notebook()

# pilgrims paths dataset
URL = (
    "http://www.heritagecouncil.ie/content/files/Pilgrim-Paths-Shapefiles.zip"
)
KNOWN_HASH = None
FILE_NAME = "Pilgrim-Paths-Shapefiles.zip"
SUB_DIR = os.path.join("data", "Pilgrim-Paths")
DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)

# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    os.makedirs(SUB_DIR, exist_ok=True)
    pooch.retrieve(
        url=URL, known_hash=KNOWN_HASH, fname=FILE_NAME, path=SUB_DIR
    )

# list of files in the ZIP archive
ZipFile(DATA_FILE).namelist()

# read shapefile data
pilgrim_paths = gpd.read_file(
    f"zip://{DATA_FILE}!"
    + [x for x in ZipFile(DATA_FILE).namelist() if x.endswith(".shp")][0]
)

# view data
pilgrim_paths.head()

pilgrim_paths.shape

list(pilgrim_paths)

pilgrim_paths.crs

# reproject to web mercator
data = pilgrim_paths.to_crs(3857)

# convert data source to GeoJSON
geo_source = GeoJSONDataSource(geojson=data.to_json())

# generate unique colours for each point
const = list(set(data["Object_Typ"]))
palette = Category20b[len(const)]
color_map = CategoricalColorMapper(factors=const, palette=palette)

# define title and tooltips
TITLE = "Pilgrim Paths in Ireland. © Heritage Council."

TOOLTIPS = [
    ("Name", "@Object_Typ"),
    ("County", "@County"),
    ("Townland", "@Townland"),
    ("Start point", "@Start_Poin"),
    ("Length", "@Length_1"),
    ("Difficulty", "@Level_of_D"),
]

# configure plot
p = figure(
    title=TITLE,
    tools="wheel_zoom, pan, reset, hover, save",
    tooltips=TOOLTIPS,
    x_axis_type="mercator",
    y_axis_type="mercator",
)

p.grid.grid_line_color = "lightgrey"

p.hover.point_policy = "follow_mouse"

# add data points
p.scatter(
    "x",
    "y",
    source=geo_source,
    size=15,
    marker="square_pin",
    line_width=0.5,
    line_color="darkslategrey",
    fill_color={"field": "Object_Typ", "transform": color_map},
    fill_alpha=0.7,
)

# add basemap
p.add_tile(xyz.CartoDB.Voyager)

show(p)
