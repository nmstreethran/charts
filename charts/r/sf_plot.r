# Plotting vector data with `sf` in R
# Data used: Boundary-Line™
# (<https://osdatahub.os.uk/downloads/open/BoundaryLine>)

# import libraries
library("sf")
library("stringr")
library("colorspace")

# set plot resolution
options(repr.plot.res = 200)

# load data
data <- st_read("data/os_bdline/data/bdline_gb.gpkg", "greater_london_const")
data$Name <- str_split_fixed(data$Name, " GL Assembly Const", 2)[, 1]

# view data
head(data, 5)

# Categorical
plot(
    data["Name"],
    key.pos = 4,
    border = "white",
    main = "Greater London Constituencies",
    pal = divergingx_hcl("Spectral", n = length(data)),
    key.width = lcm(6.5)
)
mtext("Contains OS data © Crown copyright and database right 2021", side = 1)

# Choropleth
plot(
    data["Hectares"],
    key.pos = 4,
    breaks = "equal",
    border = "white",
    main = "Greater London Constituencies",
    pal = divergingx_hcl("Spectral", n = 10)
)
mtext("Contains OS data © Crown copyright and database right 2021", side = 1)
