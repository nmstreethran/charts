# Plotting vector data with `sf` in R
# Data used: Boundary-Line™
# (<https://osdatahub.os.uk/downloads/open/BoundaryLine>)

# import libraries
library("sf")

# set plot resolution
options(repr.plot.res = 200)

data <- st_read("data/os_bdline/data/bdline_gb.gpkg", "country_region")

plot(
    data["Name"],
    key.pos = 1,
    border = FALSE,
    main = "Countries in Great Britain",
    pal = hcl.colors(3, palette = "viridis")
)
mtext("Contains OS data © Crown copyright and database right 2021", side = 1)
