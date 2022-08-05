# %% [markdown]
# # Plotting land cover raster data with rioxarray and Matplotlib
# 
# Data used:
# 
# Abera, Temesgen Alemayheu; Vuorinne, Ilja; Munyao, Martha; Pellikka, Petri; Heiskanen, Janne (2021), “Taita Taveta County, Kenya - 2020 Land cover map and reference database ”, Mendeley Data, V2, doi: [10.17632/xv24ngy2dz.2](https://doi.org/10.17632/xv24ngy2dz.2)

# %%
# import libraries
import multiprocessing
import platform
import os
import zipfile
from datetime import datetime, timezone

# Windows
if platform.system() == "Windows":
    import multiprocessing.popen_spawn_win32
# Linux/OSX
else:
    import multiprocessing.popen_spawn_posix

import threading
import xml.etree.ElementTree as ET

import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import rioxarray as rxr
from dask.distributed import Client, LocalCluster, Lock
from dask.utils import SerializableLock

# %%
print("Last updated:", datetime.now(tz=timezone.utc))

# %%
# configure plot styles
plt.style.use("seaborn-whitegrid")
plt.rcParams["font.family"] = "Segoe UI"
plt.rcParams["figure.dpi"] = 96
plt.rcParams["axes.grid"] = False
plt.rcParams["text.color"] = "darkslategrey"
plt.rcParams["axes.labelcolor"] = "darkslategrey"
plt.rcParams["xtick.labelcolor"] = "darkslategrey"
plt.rcParams["ytick.labelcolor"] = "darkslategrey"
plt.rcParams["figure.titleweight"] = "semibold"
plt.rcParams["axes.titleweight"] = "semibold"
plt.rcParams["figure.titlesize"] = "13"
plt.rcParams["axes.titlesize"] = "12"
plt.rcParams["axes.labelsize"] = "10"

# %%
# download data
URL = (
    "https://md-datasets-cache-zipfiles-prod.s3.eu-west-1.amazonaws.com/" +
    "xv24ngy2dz-2.zip"
)
r = requests.get(URL, stream=True)

os.makedirs("data", exist_ok=True)

ZIP_FILE = os.path.join("data", "kenya_land_cover.zip")

if r.status_code == 200:
    with open(ZIP_FILE, "wb") as filedl:
        for chunk in r.iter_content(chunk_size=1048676):
            filedl.write(chunk)
else:
    print("\nStatus code:", r.status_code)

# %%
# list of files in the ZIP archive
zipfile.ZipFile(ZIP_FILE).namelist()

# %%
# extract the archive
DATA_DIR = os.path.join("data", "kenya_land_cover")

try:
    z = zipfile.ZipFile(ZIP_FILE)
    z.extractall(DATA_DIR)
except zipfile.BadZipFile:
    print("There were issues with the file", ZIP_FILE)

# %%
# define paths to the TIF and QML files
for i in zipfile.ZipFile(ZIP_FILE).namelist():
    if i.endswith(".tif"):
        raster_file = os.path.join(DATA_DIR, i)
    elif i.endswith(".qml"):
        style_file = os.path.join(DATA_DIR, i)

# %%
# read the raster
# use Dask for parallel computing
# https://corteva.github.io/rioxarray/stable/examples/dask_read_write.html
with LocalCluster() as cluster, Client(cluster) as client:
    landcover = rxr.open_rasterio(
        raster_file,
        chunks=True,
        cache=False,
        masked=True,
        lock=False,
        # lock=Lock("rio-read", client=client)  # when too many file handles open
    )
    landcover.rio.to_raster(
        os.path.join(DATA_DIR, "dask_multiworker.tif"),
        tiled=True,
        lock=Lock("rio", client=client)
    )

# %%
landcover

# %%
landcover.rio.resolution()

# %%
landcover.rio.bounds()

# %%
landcover.rio.crs

# %%
# get unique value count for the raster
uniquevals = pd.DataFrame(
    np.unique(landcover, return_counts=True)
).transpose()

# assign column names
uniquevals.columns = ["value", "count"]

# drop row(s) with NaN
uniquevals.dropna(inplace=True)

# convert value column to string
uniquevals["value"] = uniquevals["value"].astype(int).astype(str)

# %%
uniquevals

# %%
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

# convert value column to string
legend["value"] = legend["value"].astype(str)

# %%
legend

# %%
# merge unique value dataframe with legend
uniquevals = uniquevals.merge(legend, on="value")

# calculate percentage based on count
uniquevals["percentage"] = (
    uniquevals["count"] / uniquevals["count"].sum() * 100
)
uniquevals["percentage"] = uniquevals["percentage"].astype(int)

# sort by count
uniquevals.sort_values("count", ascending=False, inplace=True)

# %%
uniquevals

# %%
# plot the major land cover types, i.e. percentage > 0
mask = uniquevals["percentage"] > 0
uniquevals_sig = uniquevals[mask]

ax = uniquevals_sig.plot.barh(
    x="label", y="percentage", legend=False, figsize=(9, 5),
    color=uniquevals_sig["color"]
)

ax.bar_label(ax.containers[0], padding=3)
plt.title(
    "Major land cover types for Taita Taveta County, Kenya - 2020" +
    "\n[Data: Abera et al. 2021 (CC-BY-4.0)]"
)
plt.ylabel("")
plt.xlabel("Land cover (%)")
plt.show()

# %%
# convert values to integer and sort
uniquevals["value"] = uniquevals["value"].astype(int)
uniquevals.sort_values("value", inplace=True)

# %%
# create a continuous colourmap for the plot
colours = list(uniquevals["color"])
nodes = np.array(uniquevals["value"])
# normalisation
nodes = (nodes - min(nodes)) / (max(nodes) - min(nodes))
colours = LinearSegmentedColormap.from_list(
    "LCM", list(zip(nodes, colours))
)
colours

# %%
# create a discrete colourmap for the legend
col_discrete = ListedColormap(list(uniquevals["color"]))
col_discrete

# %%
img = plt.figure(figsize=(15, 15))
img = plt.imshow(np.array([[0, len(uniquevals)]]), cmap=col_discrete)
img.set_visible(False)

ticks = list(np.arange(.5, len(uniquevals) + .5, 1))
cbar = plt.colorbar(ticks=ticks)
cbar.ax.set_yticklabels(list(uniquevals["label"]))

landcover.plot(add_colorbar=False, cmap=colours)

plt.title("Taita Taveta County, Kenya - 2020 Land cover map")

plt.axis("equal")
plt.xlim(landcover.rio.bounds()[0] - .01, landcover.rio.bounds()[2] + .01)
plt.ylim(landcover.rio.bounds()[1] - .01, landcover.rio.bounds()[3] + .01)
plt.text(
    38.75, -4.4,
    "Data: © Abera et al. 2021 (CC-BY-4.0)"
)

plt.show()

# %%



