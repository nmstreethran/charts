# import libraries
import geopandas as gpd
import matplotlib.pyplot as plt

# alter style of plots
plt.style.use("Solarize_Light2")
plt.rcParams["font.family"] = "Source Sans Pro"
plt.rcParams["figure.dpi"] = 96
plt.rcParams["axes.grid"] = False
plt.rcParams["axes.titlesize"] = "11"
plt.rcParams["axes.labelsize"] = "10"

# import data
data = gpd.read_file("os_bdline/data/bdline_gb.gpkg", layer="country_region")

# choropleth map
base = data.plot(
    cmap="Set2",
    figsize=(5, 15),
    legend=True,
    column="Name",
    legend_kwds={"loc": "upper left"}
)
plt.title("OS Boundary-Line - Countries in Great Britain")
plt.xlabel("Eastings (m)")
plt.ylabel("Northings (m)")
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
plt.title("OS Boundary-Line - Countries in Great Britain")
plt.xlabel("Eastings (m)")
plt.ylabel("Northings (m)")
base.set_aspect("equal", "box")
plt.show()

# import county data
county = gpd.read_file("os_bdline/data/bdline_gb.gpkg", layer="county")

# boundary overlay
base = countries[countries.index.isin(["England"])].plot(
    cmap="Set2", figsize=(5, 15)
)
county.boundary.plot(ax=base, color="darkslategrey", linewidth=.5)
plt.title("OS Boundary-Line - Counties in England")
plt.xlabel("Eastings (m)")
plt.ylabel("Northings (m)")
base.set_aspect("equal", "box")
plt.show()

# points overlay
base = countries[countries.index.isin(["England"])].plot(
    cmap="Set2", figsize=(5, 15)
)
county.centroid.plot(ax=base, color="darkslategrey")
plt.title("OS Boundary-Line - Counties in England")
plt.xlabel("Eastings (m)")
plt.ylabel("Northings (m)")
base.set_aspect("equal", "box")
plt.show()
