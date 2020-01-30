library("ClustOfVar")


data <- read.csv("hurricane/Harvey/MTurk_Harvey_var_cluster_v2.csv", header=TRUE)
col_names <- names(data)
dnorm <- apply(data, 2, scale)
apply(dnorm, 2, mean)
apply(dnorm, 2, sd)
X <- as.data.frame(dnorm, col.names=col_names)

tree <- hclustvar(X)
plot(tree)

stab <- stability(tree)
stab$meanCR
plot(stab, main = "Stability of the partitions")
#######################################################################
p6 <- cutreevar(tree, 6)
print(p6)
write.csv(p6$scores, 'hurricane/Harvey/harvey_6clusters.csv')
# cluster1: demo, house, difficulty
# cluster2: children, elders, special_needs, 
# cluster3: evac_notice, friends, neighbors
# cluster4: tv
# cluster5: social media
# cluster6: risk
#######################################################################
p7 <- cutreevar(tree, 7)
write.csv(p7$scores, 'hurricane/Harvey/harvey_7clusters.csv')
# cluster1: demo, house, difficulty
# cluster2: children, elders, special_needs, 
# cluster3: pets, race
# cluster4: evac_notice, friends, neighbors
# cluster5: tv
# cluster6: social media
# cluster7: risk
#######################################################################
p8 <- cutreevar(tree, 8)
write.csv(p8$scores, 'hurricane/Harvey/harvey_8clusters.csv')
# cluster1: house, money
# cluster2: children, elders, special_needs, 
# cluster3: pets, race
# cluster4: house_material
# cluster5: evac_notice, friends, neighbors
# cluster6: tv
# cluster7: social media
# cluster8: risk
#######################################################################
p9 <- cutreevar(tree, 9)
write.csv(p9$scores, 'hurricane/Harvey/harvey_9clusters.csv')
# cluster1: house, money
# cluster2: elders, special_needs
# cluster3: children
# cluster4: pets, race
# cluster5: house_material
# cluster6: evac_notice, friends, neighbors
# cluster7: tv
# cluster8: social media
# cluster9: risk

# test variance
# normalize first
# the percentage of total variance explained by the first component
#princomp


#X <- as.data.frame(data)
#colMeans(data)
#vars <- lapply(data, var)








