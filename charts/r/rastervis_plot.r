# import libraries
library("rasterVis")

# read the digital terrain model
# OS Terrain 5
dtm <- merge(
    raster("data/terrain-5-dtm_4015029/nj/NJ06NE.asc"),
    raster("data/terrain-5-dtm_4015029/nj/NJ06NW.asc"),
    raster("data/terrain-5-dtm_4015029/nj/NJ06SE.asc"),
    raster("data/terrain-5-dtm_4015029/nj/NJ06SW.asc"),
    ext = c(300000, 307000, 860000, 867000)
)

# view the DTM
dtm

# plot the DTM
levelplot(
    dtm, xlab = "Easting (m)", ylab = "Northing (m)",
    main = "5 m Digital Terrain Model of Findhorn Bay",
    colorkey = list(title = "Elevation (m)"),
    cuts = 37, col.regions = hcl.colors(n = 38, palette = "Temps")
) +
layer({
    # add a north arrow
    SpatialPolygonsRescale(
        layout.north.arrow(), offset = c(301050, 866250), scale = 600
    )
    xs <- seq(300450, 300450 + 1500, by = 500)
    # draw a scale bar
    grid.rect(
        x = xs, y = 866250 - 450, width = 500, height = 50,
        gp = gpar(fill = rep(c("white", "black"), 2)),
        default.units = "native"
    )
    # add scale bar labels
    grid.text(
        x = xs - 250, y = 866000, seq(0, 2500, by = 500),
        gp = gpar(cex = .6), default.units = "native"
    )
    # add scale bar unit
    grid.text(
        x = 302250, y = 866000, "m",
        gp = gpar(cex = .6), default.units = "native"
    )
    # add projection info
    grid.text(
        x = 300450 + 750, y = 865650, "British National Grid",
        gp = gpar(cex = .6), default.units = "native"
    )
    # add copyright info
    grid.text(
        x = 304900, y = 860160,
        "Map data Crown copyright Ordnance Survey 2021",
        gp = gpar(cex = .6), default.units = "native"
    )
})
