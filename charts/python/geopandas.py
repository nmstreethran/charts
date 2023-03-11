#!/usr/bin/env python
# coding: utf-8

# # Plotting vector data with GeoPandas and Matplotlib
#
# Data used:
#
# - <https://data.gov.ie/dataset/pilgrim-paths>
# - <https://data.gov.ie/dataset/irelands-sheela-na-gigs>
# - <https://ec.europa.eu/eurostat/web/nuts/background>

# import libraries
import os
from datetime import datetime, timezone
import geopandas as gpd
from zipfile import ZipFile, BadZipFile
import matplotlib.pyplot as plt
import pooch

# ## Data

# ### Pilgrim Paths

URL = (
    "http://www.heritagecouncil.ie/content/files/Pilgrim-Paths-Shapefiles.zip"
)
KNOWN_HASH = None
FILE_NAME = "Pilgrim-Paths-Shapefiles.zip"
SUB_DIR = os.path.join("data", "Pilgrim-Paths")
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

# list of files in the ZIP archive
ZipFile(DATA_FILE).namelist()

pilgrim_paths = gpd.read_file(
    f"zip://{DATA_FILE}!Pilgrim Paths Shapefiles/PilgrimPaths.shp"
)

# view data
pilgrim_paths.head()

list(pilgrim_paths)

pilgrim_paths.crs

# ### Sheela-na-Gigs

URL = "http://www.heritagecouncil.ie/content/files/SheelaNaGig.zip"
FILE_NAME = "SheelaNaGig.zip"
SUB_DIR = os.path.join("data", "SheelaNaGig")
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

# list of files in the ZIP archive
ZipFile(DATA_FILE).namelist()

sheela_na_gigs = gpd.read_file(f"zip://{DATA_FILE}!SheelaNaGig.shp")

sheela_na_gigs.head()

sheela_na_gigs["Sheela-na-Gig"] = "Sheela-na-Gig"

sheela_na_gigs.crs

# ### NUTS boundaries

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

    with open(
        os.path.join(SUB_DIR, f"{FILE_NAME[:-8]}.txt"), "w", encoding="utf-8"
    ) as outfile:
        outfile.write(
            f"Data downloaded on: {datetime.now(tz=timezone.utc)}\n"
            f"Download URL: {URL}"
        )

# list of files in the ZIP archive
ZipFile(DATA_FILE).namelist()

# extract the archive
try:
    z = ZipFile(DATA_FILE)
    z.extractall(SUB_DIR)
except BadZipFile:
    print("There were issues with the file", DATA_FILE)

DATA_FILE = os.path.join(SUB_DIR, "NUTS_RG_01M_2021_4326_LEVL_1.shp.zip")

ZipFile(DATA_FILE).namelist()

nuts = gpd.read_file(f"zip://{DATA_FILE}!NUTS_RG_01M_2021_4326_LEVL_1.shp")

nuts.head()

# filter for Ireland and Northern Ireland
nuts = nuts[nuts["NUTS_ID"].isin(["IE0", "UKN"])]

nuts

nuts.crs

# ## Plots

fig = nuts.to_crs(pilgrim_paths.crs).plot(
    color="navajowhite",
    edgecolor="darkslategrey",
    linewidth=0.5,
    alpha=0.5,
    figsize=(6.5, 6.5),
)
pilgrim_paths.plot(
    column="Object_Typ",
    marker="d",
    cmap="tab20b",
    ax=fig,
    legend=True,
    legend_kwds={"loc": "upper right", "bbox_to_anchor": (1.45, 0.725)},
)
for legend_handle in fig.get_legend().legendHandles:
    legend_handle.set_markeredgewidth(0.2)
    legend_handle.set_markeredgecolor("darkslategrey")
plt.title("Pilgrim Paths in Ireland")
plt.text(650000, 505000, "© EuroGeographics; gov.ie")
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()

fig = nuts.to_crs(pilgrim_paths.crs).plot(
    color="navajowhite",
    edgecolor="darkslategrey",
    linewidth=0.5,
    alpha=0.5,
    figsize=(6.5, 6.5),
)
pilgrim_paths.plot(column="Object_Typ", marker="x", cmap="viridis", ax=fig)
map_labels = zip(
    zip(pilgrim_paths.centroid.x + 5000, pilgrim_paths.centroid.y - 2500),
    pilgrim_paths["Object_Typ"],
)
for xy, lab in map_labels:
    fig.annotate(text=lab, xy=xy, textcoords="data", rotation=5)
plt.title("Pilgrim Paths in Ireland")
plt.text(650000, 505000, "© EuroGeographics; gov.ie")
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()

fig = nuts.to_crs(pilgrim_paths.crs).plot(
    color="navajowhite",
    edgecolor="darkslategrey",
    linewidth=0.5,
    alpha=0.5,
    figsize=(6.5, 6.5),
)
sheela_na_gigs.plot(
    column="Sheela-na-Gig", marker="*", cmap="tab20b", ax=fig, legend=True
)
for legend_handle in fig.get_legend().legendHandles:
    legend_handle.set_markeredgewidth(0.2)
    legend_handle.set_markeredgecolor("darkslategrey")
plt.title("Sheela-na-Gigs in Ireland")
plt.text(650000, 505000, "© EuroGeographics; gov.ie")
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()

fig = nuts.to_crs(pilgrim_paths.crs).plot(
    color="navajowhite",
    edgecolor="darkslategrey",
    linewidth=0.5,
    alpha=0.5,
    figsize=(6.5, 6.5),
)
sheela_na_gigs.plot(
    column="ITM_Northi",
    ax=fig,
    legend=True,
    cmap="viridis",
    marker=".",
    legend_kwds={"label": "ITM Northing (m)"},
)
plt.title("Sheela-na-Gigs in Ireland")
plt.text(650000, 505000, "© EuroGeographics; gov.ie")
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()

fig = nuts.to_crs(pilgrim_paths.crs).plot(
    color="navajowhite",
    edgecolor="darkslategrey",
    linewidth=0.5,
    alpha=0.5,
    figsize=(6.5, 6.5),
)
sheela_na_gigs.plot(
    column="ITM_Eastin",
    ax=fig,
    legend=True,
    cmap="copper",
    scheme="equalinterval",
    marker="X",
    legend_kwds={"title": "ITM Easting (m)", "fmt": "{:.0f}"},
)
for legend_handle in fig.get_legend().legendHandles:
    legend_handle.set_markeredgewidth(0.2)
    legend_handle.set_markeredgecolor("darkslategrey")
plt.title("Sheela-na-Gigs in Ireland")
plt.text(650000, 505000, "© EuroGeographics; gov.ie")
plt.tick_params(labelbottom=False, labelleft=False)
plt.tight_layout()
plt.show()
