# Plotting vector data with GeoPandas and Matplotlib
# Data used: Boundary-Line™
# (<https://osdatahub.os.uk/downloads/open/BoundaryLine>)

# import libraries
import geopandas as gpd
import matplotlib.pyplot as plt

# alter style of plots
plt.style.use("Solarize_Light2")
plt.rcParams["font.family"] = "Source Sans Pro"
plt.rcParams["figure.dpi"] = 96
plt.rcParams["axes.grid"] = False
plt.rcParams["text.color"] = "darkslategrey"
plt.rcParams["axes.titlesize"] = "14"
plt.rcParams["axes.labelsize"] = "10"
plt.rcParams["axes.titleweight"] = "700"

# import data
data = gpd.read_file(
    "data/os_bdline/data/bdline_gb.gpkg", layer="country_region"
)

# choropleth map
base = data.plot(
    cmap="Set2",
    figsize=(5, 15),
    legend=True,
    column="Name",
    legend_kwds={"loc": "upper left"}
)
plt.title("Countries in Great Britain")
plt.text(0, 0, "Contains OS data \n© Crown copyright and database right 2021")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
base.set_aspect("equal", "box")
plt.show()

# choropleth map - labels directly on plot
base = data.plot(
    cmap="Set2",
    figsize=(5, 15),
    column="Name"
)
countries = data.dissolve(by="Name")
countries.centroid.plot(ax=base, markersize=0)
map_labels = zip(
    zip(countries.centroid.x, countries.centroid.y), countries.index
)
for xy, lab in map_labels:
    base.annotate(text=lab, xy=xy, textcoords="data")
plt.title("Countries in Great Britain")
plt.text(0, 0, "Contains OS data \n© Crown copyright and database right 2021")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
base.set_aspect("equal", "box")
plt.show()

# import county data
county = gpd.read_file("data/os_bdline/data/bdline_gb.gpkg", layer="county")

# boundary overlay
base = countries[countries.index.isin(["England"])].plot(
    cmap="Set2", figsize=(5, 15)
)
county.boundary.plot(ax=base, color="darkslategrey", linewidth=.5)
plt.title("Boundaries of Counties in England")
plt.text(
    100000, 0, "Contains OS data \n© Crown copyright and database right 2021"
)
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
base.set_aspect("equal", "box")
plt.show()

# points overlay
base = countries[countries.index.isin(["England"])].plot(
    cmap="Set2", figsize=(5, 15)
)
county.centroid.plot(ax=base, color="darkslategrey")
plt.title("Centroids of Counties in England")
plt.text(
    100000, 0, "Contains OS data \n© Crown copyright and database right 2021"
)
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
base.set_aspect("equal", "box")
plt.show()
