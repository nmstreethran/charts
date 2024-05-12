#!/usr/bin/env python
# coding: utf-8

# # Interactive plot of simple vector features (polygons) with Bokeh and GeoPandas
#
# Data used: NUTS (<https://ec.europa.eu/eurostat/web/nuts/background>)

# import libraries
import os
from zipfile import BadZipFile, ZipFile

import geopandas as gpd
import pooch
import xyzservices.providers as xyz
from bokeh.io import output_notebook
from bokeh.models import CategoricalColorMapper, GeoJSONDataSource
from bokeh.palettes import inferno
from bokeh.plotting import figure, show

# set inline plots
output_notebook()

# NUTS data
URL = (
    "https://gisco-services.ec.europa.eu/distribution/v2/nuts/download/"
    "ref-nuts-2021-01m.shp.zip"
)
FILE_NAME = "ref-nuts-2021-01m.shp.zip"
SUB_DIR = os.path.join("data", "NUTS")
DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)
os.makedirs(SUB_DIR, exist_ok=True)

# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL, known_hash=KNOWN_HASH, fname=FILE_NAME, path=SUB_DIR
    )

# list of files in the ZIP archive
ZipFile(DATA_FILE).namelist()

# extract the archive
try:
    z = ZipFile(DATA_FILE)
    z.extractall(SUB_DIR)
except BadZipFile:
    print("There were issues with the file", DATA_FILE)

DATA_FILE = os.path.join(SUB_DIR, "NUTS_RG_01M_2021_3857_LEVL_0.shp.zip")

ZipFile(DATA_FILE).namelist()

nuts = gpd.read_file(f"zip://{DATA_FILE}!NUTS_RG_01M_2021_3857_LEVL_0.shp")

nuts.head()

nuts.shape

nuts.crs

# convert data source to GeoJSON
geo_source = GeoJSONDataSource(geojson=nuts.to_json())

# generate unique colours for each point
const = list(set(nuts["NUTS_ID"]))
palette = inferno(len(const))
color_map = CategoricalColorMapper(factors=const, palette=palette)

# define title and tooltips
TITLE = "NUTS Level 0 regions. © EuroGeographics."

TOOLTIPS = [
    ("Name", "@NAME_LATN"),
    ("NUTS Name", "@NUTS_NAME"),
    ("NUTS ID", "@NUTS_ID"),
    ("Country", "@CNTR_CODE"),
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
p.patches(
    "xs",
    "ys",
    source=geo_source,
    line_width=0.5,
    line_color="white",
    fill_color={"field": "NUTS_ID", "transform": color_map},
    fill_alpha=0.7,
)

# add basemap
p.add_tile(xyz.CartoDB.Voyager)

show(p)
