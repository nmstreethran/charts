# Plotting vector data with GeoPandas and Matplotlib
# Data used: Boundary-Line™
# (<https://osdatahub.os.uk/downloads/open/BoundaryLine>)

# import libraries
import geopandas as gpd
import matplotlib.pyplot as plt

# configure plot styles
plt.style.use("Solarize_Light2")
plt.rcParams["font.family"] = "Source Sans Pro"
plt.rcParams["figure.dpi"] = 96
plt.rcParams["axes.grid"] = False
plt.rcParams["text.color"] = "darkslategrey"
plt.rcParams["axes.labelcolor"] = "darkslategrey"
plt.rcParams["xtick.labelcolor"] = "darkslategrey"
plt.rcParams["ytick.labelcolor"] = "darkslategrey"
plt.rcParams["axes.titlesize"] = "12"
plt.rcParams["axes.labelsize"] = "10"
plt.rcParams["axes.titleweight"] = "semibold"

# import data
data = gpd.read_file(
    "data/os_bdline/data/bdline_gb.gpkg", layer="greater_london_const"
)
data["Name"] = data["Name"].str.slice(stop=-18)

# view data
data.head(5)

# Categorical
base = data.plot(
    cmap="tab20b",
    figsize=(7, 7),
    legend=True,
    column="Name",
    legend_kwds={"loc": "upper right", "bbox_to_anchor": (1.4, .86)}
)

data.boundary.plot(color="white", ax=base, linewidth=.5)

plt.title("Greater London Constituencies")
plt.text(
    501000,
    154000,
    "Contains OS data © Crown copyright and database right 2021"
)
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
base.set_aspect("equal", "box")

plt.show()

# categorical map - labels directly on plot
base = data.plot(cmap="tab20b", figsize=(7, 7), column="Name", alpha=.45)

data.boundary.plot(color="white", ax=base, linewidth=.5)

data.centroid.plot(ax=base, color="darkslategrey", markersize=5)

map_labels = zip(zip(data.centroid.x+500, data.centroid.y-300), data["Name"])
for xy, lab in map_labels:
    base.annotate(text=lab, xy=xy, textcoords="data", rotation=10)

plt.title("Greater London Constituencies")
plt.text(
    501000,
    154000,
    "Contains OS data © Crown copyright and database right 2021"
)
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
base.set_aspect("equal", "box")

plt.show()

# Choropleth
# choropleth map - continuous symbology
base = data.plot(
    column="Hectares",
    legend=True,
    cmap="RdYlGn_r",
    figsize=(10, 7),
    legend_kwds={"label": "Hectares"}
)

data.boundary.plot(color="white", ax=base, linewidth=.5)

plt.title("Greater London Constituencies")
plt.text(
    501000,
    154000,
    "Contains OS data © Crown copyright and database right 2021"
)
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
base.set_aspect("equal", "box")

plt.show()

# choropleth map - discrete symbology
base = data.plot(
    column="Hectares",
    legend=True,
    cmap="copper",
    scheme="QUANTILES",
    figsize=(10, 7),
    legend_kwds={"title": "Hectares", "loc": "lower right", "fmt": "{:.0f}"}
)

data.boundary.plot(color="white", ax=base, linewidth=.5)

plt.title("Greater London Constituencies")
plt.text(
    501000,
    154000,
    "Contains OS data © Crown copyright and database right 2021"
)
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
base.set_aspect("equal", "box")

plt.show()
