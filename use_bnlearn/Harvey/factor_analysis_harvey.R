library(corrplot)

d <- read.csv("hurricane/Harvey/MTurk_Harvey_var_cluster_v2.csv", header=TRUE)
corrplot(cor(d), order = "hclust", tl.col='black', tl.cex=.75) 

res1b <- factanal(d, factors = 11, rotation = "varimax", na.action = na.omit)
res1b$loadings

library(psych)
require(ggplot2)
require(reshape2)
scree(d)