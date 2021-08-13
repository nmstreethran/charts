# import libraries
import matplotlib.pyplot as plt
import rioxarray as rxr
from rioxarray.merge import merge_arrays

# alter style of plots
plt.style.use("Solarize_Light2")
plt.rcParams["font.family"] = "Source Sans Pro"
plt.rcParams["figure.dpi"] = 96
plt.rcParams["axes.grid"] = False
plt.rcParams["axes.titlesize"] = "12"

# read the digital terrain model
# OS Terrain 5
rasters = [
    "data/terrain-5-dtm_4015029/nj/NJ06NE.asc",
    "data/terrain-5-dtm_4015029/nj/NJ06NW.asc",
    "data/terrain-5-dtm_4015029/nj/NJ06SE.asc",
    "data/terrain-5-dtm_4015029/nj/NJ06SW.asc"
]
arrays = []

for ras in rasters:
    arrays.append(rxr.open_rasterio(ras, masked=True))

dtm = merge_arrays(arrays)

# view the DTM
dtm

# plot the DTM
dtm.squeeze().plot.imshow(
    cmap=plt.cm.get_cmap("viridis", 60),
    cbar_kwargs={"label": "Elevation (m)"},
    vmax=dtm.max(),
    vmin=dtm.min()
)
plt.title("5 m Digital Terrain Model of Findhorn Bay")
plt.xlabel("Eastings (m)")
plt.ylabel("Northings (m)")
plt.axis("equal")
plt.show()

# plot contours
dtm.squeeze().plot.contour(
    cmap="viridis",
    levels=30,
    linewidths=.5,
    add_colorbar=True,
    cbar_kwargs={"label": "Elevation (m)"},
    vmax=dtm.max(),
    vmin=dtm.min()
)
plt.title("5 m Digital Terrain Model of Findhorn Bay")
plt.xlabel("Eastings (m)")
plt.ylabel("Northings (m)")
plt.axis("equal")
plt.show()
