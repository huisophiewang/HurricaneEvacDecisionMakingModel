library(pcalg)

# pc algorithm, structure learning, based on CI tests
data(gmG)
suffStat <- list(C = cor(gmG$x), n = nrow(gmG$x))
pc.fit <- pc(suffStat, indepTest = gaussCItest, p = ncol(gmG$x), alpha = 0.01)
require(Rgraphviz)
par(mfrow = c(1,2))
plot(gmG$g, main = "True DAG")
plot(pc.fit, main = "Estimated DAG")

# ges algorithm, structure learning, score-based
score <- new("GaussL0penObsScore", gmG8$x)
ges.fit <- ges(score)
par(mfrow=1:2)
plot(gmG8$g, main = "")
plot(ges.fit$essgraph, main = "")


# fci algorithm, build on PC algorithm, can include hidden variables
data(gmL)
suffStat1 <- list(C = cor(gmL$x), n = nrow(gmL$x))
pag.est <- fci(suffStat1, indepTest= gaussCItest, p = ncol(gmL$x), alpha = 0.01)
par(mfrow = c(1,2))
plot(gmL$g, main = "True DAG")
plot(pag.est, main = "Estimated PAG")

# rfci algorithm, faster, 
data(gmL)
suffStat1 <- list(C = cor(gmL$x), n = nrow(gmL$x))
pag.est <- rfci(suffStat1, indepTest = gaussCItest, p = ncol(gmL$x), alpha = 0.01, labels = as.character(2:5))
par(mfrow = c(1,2))
plot(gmL$g, main = "True DAG")
plot(pag.est, main = "Estimated PAG")


# ida algorithm
ida(1, 6, cov(gmG$x), pc.fit@graph)

#######################################################################################
mydata <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels.csv", header=TRUE)
suffStat <- list(C = cor(mydata), n = nrow(mydata))
pc.fit <- pc(suffStat, indepTest = gaussCItest, alpha = 0.01, labels = colnames(mydata))
require(Rgraphviz)
plot(pc.fit)

mydata <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels.csv", header=TRUE)
suffStat <- list(C = cor(mydata), n = nrow(mydata))
pag.est <- fci(suffStat, indepTest= gaussCItest, alpha = 0.01, labels = colnames(mydata))
require(Rgraphviz)
plot(pag.est)

