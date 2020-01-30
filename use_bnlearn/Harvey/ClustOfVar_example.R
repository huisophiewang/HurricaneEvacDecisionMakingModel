library("ClustOfVar")


# example 1
data("decathlon")
head(decathlon[, 1:4])

tree <- hclustvar(decathlon[, 1:10])
plot(tree)

stab <- stability(tree, B = 40)
plot(stab, main = "Stability of the partitions")
boxplot(stab$matCR, main = "Dispersion of the adjusted Rand index")

P3 <- cutreevar(tree, 3, matsim = TRUE)
cluster <- P3$cluster
X <- decathlon[, 1:10]
princomp(X[, which(cluster==1)], cor = TRUE)$sdev^2
princomp(X[, which(cluster==2)], cor = TRUE)$sdev^2
princomp(X[, which(cluster==3)], cor = TRUE)$sdev^2

print(P3)

P3$cluster
P3$var
P3$scores


# example 2
data("wine")
head(wine)

X.quanti <- wine[, 3:29]
X.quali <- wine[, 1:2]
tree <- hclustvar(X.quanti, X.quali)
plot(tree)

part_hier <- cutreevar(tree, 6)
part_hier$var