"""Mapping pollen concentration across Great Britain

See: https://nithiya.gitlab.io/post/pollen-concentration-maps-qgis/

"""

import geopandas as gpd
# import libraries
import pandas as pd

# read data
pollen = pd.read_csv("data/qPCR_copy_number_abundance_data_aerial_DNA.csv")

# create well known text from coordinates
pollen["wkt"] = (
    "POINT ("
    + pollen["Long"].astype(str)
    + " "
    + pollen["Lat"].astype(str)
    + ")"
)

# drop cells with no value
pollen = pollen.dropna(subset=["Lat", "Long", "MaxPoaceaeConc", "year-month"])

# use full pollen monitoring site name
pollen = pollen.replace(
    {
        "EXE": "Exeter",
        "EastR": "East Riding",
        "ESK": "Eskdalemuir",
        "LEIC": "Leicester",
        "CAR": "Cardiff",
        "IOW": "Isle of Wight",
        "IPS": "Ipswich",
        "BNG": "Bangor",
        "WOR": "Worcester",
        "KCL": "King's College London",
        "YORK": "York",
        "ING": "Invergowrie",
        "BEL": "Belfast",
    }
)

# create a geo data frame
pollen = gpd.GeoDataFrame(
    pollen, geometry=gpd.GeoSeries.from_wkt(pollen["wkt"]), crs="EPSG:4326"
)

# drop unnecessary columns
pollen = pollen.drop(columns=["Lat", "Long", "wkt"])

# reproject to BNG
pollen = pollen.to_crs("epsg:27700")

# get list of months with available data
monthList = list(pollen["year-month"].str[0:3].unique())

# get list of pollen monitoring sites
pollen_sites = pollen[["Site", "geometry"]].drop_duplicates()

# aggregate monthly data for each site and save as GeoPackage layers
for m in monthList:
    pollen_month = pollen[pollen["year-month"].str.contains(m)]
    pollen_month = pollen_month.groupby(["Site"]).mean("MaxPoaceaeConc")
    pollen_month = pd.merge(pollen_month, pollen_sites, on="Site")
    pollen_month.to_file("data/pollen-data.gpkg", layer=m)
