# Plotting matrices using the `lattice` R package

# import required libraries
library("lattice")
library("colorspace")

# set plot resolution
options(repr.plot.res = 200)

# set seed to generate reproducible examples
set.seed(999)

# generate 5 by 5 matrix, with values between 0 and 100
m1 <- matrix(sample(1:100, 5 * 5, replace = TRUE), 5, 5)

# view the matrix
m1

# plot the matrix
levelplot(
    t(m1),
    col.regions = divergingx_hcl("PiYG", n = 100),
    cuts = 99,
    xlab = "column",
    ylab = "row"
)

# do the same with a larger matrix
m2 <- matrix(sample(1:100, 50 * 50, replace = TRUE), 50, 50)

m2

levelplot(
    t(m2),
    col.regions = divergingx_hcl("PuOr", n = 100),
    cuts = 99,
    xlab = "column",
    ylab = "row"
)
