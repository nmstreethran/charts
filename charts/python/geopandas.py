#!/usr/bin/env python
# coding: utf-8

# # Plotting vector data with GeoPandas and Matplotlib
#
# Data used:
#
# - <https://data.gov.ie/dataset/pilgrim-paths>
# - <https://ec.europa.eu/eurostat/web/nuts/background>

# In[ ]:


import os
from zipfile import BadZipFile, ZipFile

import cartopy.crs as ccrs
import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import pooch
from matplotlib_scalebar.scalebar import ScaleBar

# In[ ]:


# basemap cache directory
cx.set_cache_dir(os.path.join("data", "basemaps"))


# ## Data

# ### Pilgrim Paths

# In[ ]:


URL = (
    "http://www.heritagecouncil.ie/content/files/Pilgrim-Paths-Shapefiles.zip"
)
KNOWN_HASH = None
FILE_NAME = "Pilgrim-Paths-Shapefiles.zip"
SUB_DIR = os.path.join("data", "Pilgrim-Paths")
DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)
os.makedirs(SUB_DIR, exist_ok=True)


# In[ ]:


# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL, known_hash=KNOWN_HASH, fname=FILE_NAME, path=SUB_DIR
    )


# In[ ]:


# list of files in the ZIP archive
ZipFile(DATA_FILE).namelist()


# In[ ]:


pilgrim_paths = gpd.read_file(
    f"zip://{DATA_FILE}!"
    + [x for x in ZipFile(DATA_FILE).namelist() if x.endswith(".shp")][0]
)


# In[ ]:


# view data
pilgrim_paths.head()


# In[ ]:


list(pilgrim_paths)


# In[ ]:


pilgrim_paths.crs


# ### NUTS boundaries

# In[ ]:


URL = (
    "https://gisco-services.ec.europa.eu/distribution/v2/nuts/download/"
    "ref-nuts-2021-01m.shp.zip"
)
FILE_NAME = "ref-nuts-2021-01m.shp.zip"
SUB_DIR = os.path.join("data", "NUTS")
DATA_FILE = os.path.join(SUB_DIR, FILE_NAME)
os.makedirs(SUB_DIR, exist_ok=True)


# In[ ]:


# download data if necessary
if not os.path.isfile(os.path.join(SUB_DIR, FILE_NAME)):
    pooch.retrieve(
        url=URL, known_hash=KNOWN_HASH, fname=FILE_NAME, path=SUB_DIR
    )


# In[ ]:


# list of files in the ZIP archive
ZipFile(DATA_FILE).namelist()


# In[ ]:


# extract the archive
try:
    z = ZipFile(DATA_FILE)
    z.extractall(SUB_DIR)
except BadZipFile:
    print("There were issues with the file", DATA_FILE)


# In[ ]:


DATA_FILE = os.path.join(SUB_DIR, "NUTS_RG_01M_2021_4326_LEVL_1.shp.zip")


# In[ ]:


ZipFile(DATA_FILE).namelist()


# In[ ]:


nuts = gpd.read_file(f"zip://{DATA_FILE}!NUTS_RG_01M_2021_4326_LEVL_1.shp")


# In[ ]:


nuts.head()


# In[ ]:


# filter for Ireland
nuts = nuts[nuts["NUTS_ID"].isin(["IE0", "UKN"])]


# In[ ]:


nuts


# In[ ]:


nuts.crs


# ## Plots

# In[ ]:


# get map bounds
xmin, ymin, xmax, ymax = nuts.to_crs(pilgrim_paths.crs).total_bounds


# In[ ]:


ax = (
    nuts.dissolve()
    .to_crs(pilgrim_paths.crs)
    .plot(
        color="navajowhite",
        edgecolor="darkslategrey",
        linewidth=0.5,
        alpha=0.5,
        figsize=(6.5, 6.5),
    )
)

pilgrim_paths.plot(
    column="Object_Typ",
    marker="d",
    cmap="tab20b",
    ax=ax,
    legend=True,
    legend_kwds={"loc": "upper right", "bbox_to_anchor": (1.45, 0.725)},
    edgecolor="darkslategrey",
    linewidth=0.5,
)

for legend_handle in ax.get_legend().legend_handles:
    legend_handle.set_markeredgewidth(0.5)
    legend_handle.set_markeredgecolor("darkslategrey")

plt.title("Pilgrim Paths in Ireland")
plt.text(xmax - 180000, ymin - 10000, "© EuroGeographics; Heritage Council")
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()


# In[ ]:


# label directly on plot
ax = (
    nuts.dissolve()
    .to_crs(pilgrim_paths.crs)
    .plot(
        color="navajowhite",
        edgecolor="darkslategrey",
        linewidth=0.5,
        alpha=0.5,
        figsize=(6.5, 6.5),
    )
)

pilgrim_paths.plot(
    column="Object_Typ",
    marker="X",
    cmap="viridis",
    ax=ax,
    edgecolor="darkslategrey",
    linewidth=0.5,
)

map_labels = zip(
    zip(pilgrim_paths.centroid.x + 5000, pilgrim_paths.centroid.y - 2500),
    pilgrim_paths["Object_Typ"],
)
for xy, lab in map_labels:
    ax.annotate(text=lab, xy=xy, textcoords="data", rotation=5)

plt.title("Pilgrim Paths in Ireland")
plt.text(xmax - 180000, ymin - 10000, "© EuroGeographics; Heritage Council")
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()


# In[ ]:


# get map bounds in web mercator projection
CRS = 3857
xmin, ymin, xmax, ymax = nuts.to_crs(CRS).total_bounds


# In[ ]:


# with gridlines, scalebar, and basemap
plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.epsg(CRS))

pilgrim_paths.to_crs(CRS).plot(
    ax=ax,
    column="Object_Typ",
    marker="o",
    cmap="tab20b",
    legend=True,
    edgecolor="darkslategrey",
    linewidth=0.5,
)

plt.ylim(ymin - 50000, ymax + 50000)
plt.xlim(xmin - 50000, xmax + 250000)

for legend_handle in ax.get_legend().legend_handles:
    legend_handle.set_markeredgewidth(0.5)
    legend_handle.set_markeredgecolor("darkslategrey")

cx.add_basemap(ax, source=cx.providers.CartoDB.Voyager)

ax.gridlines(
    draw_labels={"bottom": "x", "left": "y"}, alpha=0.25, color="darkslategrey"
)

ax.add_artist(
    ScaleBar(1, box_alpha=0, location="lower right", color="darkslategrey")
)

plt.title("Pilgrim Paths in Ireland")
plt.text(xmin - 45000, ymin - 30000, "© Heritage Council")
plt.tight_layout()
plt.show()
