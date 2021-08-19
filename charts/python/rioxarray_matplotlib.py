# Plotting raster data with rioxarray and Matplotlib
# Data used: OS Terrain® 50
# (<https://osdatahub.os.uk/downloads/open/Terrain50>)

# import libraries
import matplotlib.pyplot as plt
import rioxarray as rxr
from rioxarray.merge import merge_arrays

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

# read the digital terrain model
# OS Terrain 50
rasters = [
    "data/Terrain50/sn91_OST50GRID_20210507/SN91.asc",
    "data/Terrain50/sn92_OST50GRID_20210507/SN92.asc",
    "data/Terrain50/so01_OST50GRID_20210507/SO01.asc",
    "data/Terrain50/so02_OST50GRID_20210507/SO02.asc"
]
arrays = []

for ras in rasters:
    arrays.append(rxr.open_rasterio(ras, masked=True))

dtm = merge_arrays(arrays)

# view the DTM
dtm

# plot the DTM
dtm.squeeze().plot.imshow(
    cmap="terrain",
    cbar_kwargs={"label": "Elevation (m)"},
    vmax=dtm.max(),
    vmin=dtm.min(),
    figsize=(9, 9)
)
plt.title("50 m Digital Terrain Model of the Brecon Beacons")
plt.text(
    297000,
    208200,
    "Contains OS data © Crown copyright and database right 2021"
)
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.axis("equal")
plt.show()

# plot contours
CS = dtm.squeeze().plot.contour(
    cmap="inferno",
    linewidths=.5,
    add_colorbar=False,
    figsize=(7, 7)
)
plt.title("50 m Digital Terrain Model of the Brecon Beacons")
plt.text(
    296800,
    207600,
    "Contains OS data © Crown copyright and database right 2021"
)
plt.clabel(CS, inline=True)
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.axis("equal")
plt.show()

# contour overlay
dtm.squeeze().plot.imshow(
    cmap="terrain",
    cbar_kwargs={"label": "Elevation (m)"},
    vmax=dtm.max(),
    vmin=dtm.min(),
    figsize=(9, 9)
)

CS = dtm.squeeze().plot.contour(colors="black", linewidths=.5)

plt.title("50 m Digital Terrain Model of the Brecon Beacons")
plt.text(
    297000,
    208200,
    "Contains OS data © Crown copyright and database right 2021"
)
plt.clabel(CS, inline=True)
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.axis("equal")
plt.show()
