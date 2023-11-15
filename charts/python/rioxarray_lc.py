#!/usr/bin/env python
# coding: utf-8

# # Plotting land cover raster data with rioxarray and Matplotlib
#
# Data used:
#
# Abera, Temesgen Alemayheu; Vuorinne, Ilja; Munyao, Martha; Pellikka, Petri;
# Heiskanen, Janne (2021), "Taita Taveta County, Kenya - 2020 Land cover map
# and reference database", Mendeley Data, V2, doi:
# [10.17632/xv24ngy2dz.2](https://doi.org/10.17632/xv24ngy2dz.2) - CC-BY-4.0

# import libraries
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from zipfile import BadZipFile, ZipFile

import cartopy.crs as ccrs
import contextily as cx
import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pooch
import rioxarray as rxr
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib_scalebar.scalebar import ScaleBar

# basemap cache directory
cx.set_cache_dir(os.path.join("data", "basemaps"))
os.makedirs(os.path.join("data", "basemaps"), exist_ok=True)

print("Last updated:", datetime.now(tz=timezone.utc))

KNOWN_HASH = None
URL = (
    "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/"
    "xv24ngy2dz-2.zip"
)
FILE_NAME = "kenya_land_cover.zip"
SUB_DIR = os.path.join("data", "kenya_land_cover")
DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)
os.makedirs(SUB_DIR, exist_ok=True)

# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL, known_hash=KNOWN_HASH, fname=FILE_NAME, path=SUB_DIR
    )

    with open(
        os.path.join(SUB_DIR, f"{FILE_NAME[:-4]}.txt"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

with open(f"{DATA_FILE[:-4]}.txt") as f:
    print(f.read())

# list of files in the ZIP archive
ZipFile(DATA_FILE).namelist()

# extract the archive
try:
    z = ZipFile(DATA_FILE)
    z.extractall(SUB_DIR)
except BadZipFile:
    print("There were issues with the file", DATA_FILE)

# define paths to the TIF and QML files
for i in ZipFile(DATA_FILE).namelist():
    if i.endswith(".tif"):
        raster_file = os.path.join(SUB_DIR, i)
    elif i.endswith(".qml"):
        style_file = os.path.join(SUB_DIR, i)

landcover = rxr.open_rasterio(raster_file, chunks=300, masked=True)

landcover

landcover.rio.resolution()

landcover.rio.bounds()

landcover.rio.crs

# get unique value count for the raster
uniquevals = pd.DataFrame(np.unique(landcover, return_counts=True)).transpose()

# assign column names
uniquevals.columns = ["value", "count"]

# drop row(s) with NaN
uniquevals.dropna(inplace=True)

# convert value column to string (this is required for merging later)
uniquevals["value"] = uniquevals["value"].astype(int).astype(str)

uniquevals

# read the QGIS style file containing the legend entries
tree = ET.parse(style_file)
root = tree.getroot()

# extract colour palette
pal = {}

for palette in root.iter("paletteEntry"):
    pal[palette.attrib["value"]] = palette.attrib

# generate data frame from palette dictionary
legend = pd.DataFrame.from_dict(pal).transpose()
legend = pd.DataFrame(legend)

# drop alpha column
legend.drop(columns="alpha", inplace=True)

# convert value column to string (this is required for merging later)
legend["value"] = legend["value"].astype(str)

legend

# merge unique values data frame with legend
uniquevals = uniquevals.merge(legend, on="value")

# calculate percentage based on count
uniquevals["percentage"] = (
    uniquevals["count"] / uniquevals["count"].sum() * 100
)
uniquevals["percentage"] = uniquevals["percentage"].astype(int)

# sort by count
uniquevals.sort_values("count", ascending=False, inplace=True)

uniquevals

# plot the major land cover types, i.e. percentage > 0
mask = uniquevals["percentage"] > 0
uniquevals_sig = uniquevals[mask]

ax = uniquevals_sig.plot.barh(
    x="label",
    y="percentage",
    legend=False,
    figsize=(9, 5),
    color=uniquevals_sig["color"],
)

ax.bar_label(ax.containers[0], padding=3)
plt.title(
    "Major land cover types for Taita Taveta County, Kenya - 2020"
    + "\n[Data: Abera et al. 2021 (CC-BY-4.0)]"
)
plt.ylabel("")
plt.xlabel("Land cover (%)")
plt.tight_layout()
plt.show()

# convert values to integer and sort
uniquevals["value"] = uniquevals["value"].astype(int)
uniquevals.sort_values("value", inplace=True)

# create a continuous colourmap for the plot
colours = list(uniquevals["color"])
nodes = np.array(uniquevals["value"])
# normalisation
nodes = (nodes - min(nodes)) / (max(nodes) - min(nodes))
colours = LinearSegmentedColormap.from_list("LCM", list(zip(nodes, colours)))
colours

# create a discrete colourmap for the legend
col_discrete = ListedColormap(list(uniquevals["color"]))
col_discrete

xmin, ymin, xmax, ymax = landcover.rio.bounds()

# create a dummy plot for the discrete colour map as the legend
img = plt.figure(figsize=(15, 15))
img = plt.imshow(np.array([[0, len(uniquevals)]]), cmap=col_discrete)
img.set_visible(False)

# assign the legend's tick labels
ticks = list(np.arange(0.5, len(uniquevals) + 0.5, 1))
cbar = plt.colorbar(ticks=ticks)
cbar.ax.set_yticklabels(list(uniquevals["label"]))

landcover.plot(add_colorbar=False, cmap=colours)

plt.axis("equal")
plt.xlim(xmin - 0.01, xmax + 0.01)
plt.ylim(ymin - 0.01, ymax + 0.01)

plt.title(
    "Taita Taveta County, Kenya - 2020 Land cover map. "
    "Data: © Abera et al. 2021 (CC-BY-4.0)."
)

plt.show()

# clip data into a smaller subset to demonstrate further plotting capabilities
# use web mercator projection
CRS = 3857

# 20k meter buffer at the centre
mask = gpd.GeoSeries(
    gpd.points_from_xy(
        [xmin + (xmax - xmin) / 2],
        [ymin + (ymax - ymin) / 2],
        crs=landcover.rio.crs,
    )
    .to_crs(CRS)
    .buffer(20000)
    .to_crs(landcover.rio.crs)
)

mask

mask.total_bounds

mask.crs

landcover.rio.clip(mask)

# use legend handles for better legends
fig, ax = plt.subplots(figsize=(10, 10))
landcover.rio.clip(mask).plot(add_colorbar=False, cmap=colours, ax=ax)

legend_handles = []
for color, label in zip(list(uniquevals["color"]), list(uniquevals["label"])):
    legend_handles.append(mpatches.Patch(facecolor=color, label=label))

ax.legend(handles=legend_handles, loc="lower right", bbox_to_anchor=(1.21, 0))

plt.title(
    "Taita Taveta County, Kenya - 2020 Land cover map. "
    "Data: © Abera et al. 2021 (CC-BY-4.0)."
)

plt.show()

xmin, ymin, xmax, ymax = landcover.rio.reproject(CRS).rio.bounds()

# with better legends, basemap, scalebar, and gridlines
plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.epsg(CRS))
landcover.rio.clip(mask).rio.reproject(CRS).plot(
    add_colorbar=False, cmap=colours, ax=ax
)

plt.ylim(ymin, ymax)
plt.xlim(xmin, xmax)

cx.add_basemap(ax, source=cx.providers.CartoDB.VoyagerNoLabels)
cx.add_basemap(ax, source=cx.providers.CartoDB.VoyagerOnlyLabels)

legend_handles = []
for color, label in zip(list(uniquevals["color"]), list(uniquevals["label"])):
    legend_handles.append(mpatches.Patch(facecolor=color, label=label))

ax.legend(handles=legend_handles)

ax.gridlines(
    draw_labels={"bottom": "x", "left": "y"}, alpha=0.25, color="darkslategrey"
)

ax.add_artist(
    ScaleBar(1, box_alpha=0, location="lower right", color="darkslategrey")
)

plt.title(
    "Taita Taveta County, Kenya - 2020 Land cover map. "
    "Data: © Abera et al. 2021 (CC-BY-4.0)."
)

plt.show()
