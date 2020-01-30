library(bnlearn)
library(plyr)

######################################################################################################

data <- read.csv("hurricane/Harvey/harvey_6clusters.csv", header=TRUE)
# cluster1: demo, house
# cluster2: children, elders, special_needs, 
# cluster3: evac_notice, friends, neighbors
# cluster4: tv
# cluster5: social media
# cluster6: risk
X <- rename(data, c("cluster1"="Demo_House_Difficulty", "cluster2"="Children_Elders_SpecialNeeds",
               "cluster3"="EvacNotice_Friends_Neighbors", "cluster4"="TVRadio",
               "cluster5"="SocialMedia", "cluster6"="Risk", "evac_decision"="Evac"))

X <- discretize(X[,1:6], method='interval', breaks=3, ordered=TRUE)
X$Evac = data$evac_decision
X$Evac <- as.ordered(X$Evac)
blklist <- list(c("Demo_House_Difficulty","Children_Elders_SpecialNeeds",
                  "EvacNotice_Friends_Neighbors","TVRadio","SocialMedia"),
                c("Risk"),
                c("Evac"))

prior <- empty.graph(nodes=names(X))
learned_net <- hc(X, score="bic", blacklist=tiers2blacklist(blklist), start=prior)
graphviz.plot(learned_net, shape="rectangle")

#res <- gs(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
res <- inter.iamb(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
#res <- mmpc(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
#res <- si.hiton.pc(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
graphviz.plot(res, shape="rectangle")

######################################################################################################
data <- read.csv("hurricane/Harvey/harvey_7clusters.csv", header=TRUE)
# cluster1: demo, house, difficulty
# cluster2: children, elders, special_needs, 
# cluster3: pets, race
# cluster4: evac_notice, friends, neighbors
# cluster5: tv
# cluster6: social media
# cluster7: risk
X <- rename(data, c("cluster1"="Demo_House_Difficulty", "cluster2"="Children_Elders_SpecialNeeds",
                    "cluster3"="Race_Pets", "cluster4"="EvacNotice_Friends_Neighbors",
                    "cluster5"="TVRadio", "cluster6"="SocialMedia",
                    "cluster7"="Risk", "evac_decision"="Evac"))

X <- discretize(X[,1:7], method='interval', breaks=3, ordered=TRUE)
X$Evac = data$evac_decision
X$Evac <- as.ordered(X$Evac)
blklist <- list(c("Demo_House_Difficulty","Children_Elders_SpecialNeeds","Race_Pets",
                  "EvacNotice_Friends_Neighbors","TVRadio","SocialMedia"),
                c("Risk"),
                c("Evac"))

res <- inter.iamb(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
#res <- mmpc(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
#res <- si.hiton.pc(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
graphviz.plot(res, shape="rectangle")

######################################################################################################
data <- read.csv("hurricane/Harvey/harvey_8clusters.csv", header=TRUE)
# cluster1: house, money
# cluster2: children, elders, special_needs, 
# cluster3: pets, race
# cluster4: house_material
# cluster5: evac_notice, friends, neighbors
# cluster6: tv
# cluster7: social media
# cluster8: risk
X <- rename(data, c("cluster1"="House_Finance", "cluster2"="Children_Elders_SpecialNeeds",
                    "cluster3"="Race_Pets", "cluster4"="HouseMaterial",
                    "cluster5"="EvacNotice_Friends_Neighbors",
                    "cluster6"="TVRadio", "cluster7"="SocialMedia",
                    "cluster8"="Risk", "evac_decision"="Evac"))

X <- discretize(X[,1:8], method='interval', breaks=3, ordered=TRUE)
X$Evac = data$evac_decision
X$Evac <- as.ordered(X$Evac)
blklist <- list(c("House_Finance","Children_Elders_SpecialNeeds","Race_Pets","HouseMaterial",
                  "EvacNotice_Friends_Neighbors","TVRadio","SocialMedia"),
                c("Risk"),
                c("Evac"))

res <- inter.iamb(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
#res <- mmpc(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
#res <- si.hiton.pc(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
graphviz.plot(res, shape="rectangle")

######################################################################################################
data <- read.csv("hurricane/Harvey/harvey_9clusters.csv", header=TRUE)
# cluster1: house, money
# cluster2: elders, special_needs
# cluster3: children
# cluster4: pets, race
# cluster5: house_material
# cluster6: evac_notice, friends, neighbors
# cluster7: tv
# cluster8: social media
# cluster9: risk
X <- rename(data, c("cluster1"="House_Finance", "cluster2"="Elders_SpecialNeeds",
                    "cluster3"="Children", "cluster4"="Race_Pets",
                    "cluster5"="HouseMaterial", "cluster6"="EvacNotice_Friends_Neighbors",
                    "cluster7"="TVRadio","cluster8"="SocialMedia", "cluster9"="Risk", "evac_decision"="Evac"))

X <- discretize(X[,1:9], method='interval', breaks=7, ordered=TRUE)
X$Evac = data$evac_decision
X$Evac <- as.ordered(X$Evac)
blklist <- list(c("House_Finance","Elders_SpecialNeeds","Children","Race_Pets","HouseMaterial",
                  "EvacNotice_Friends_Neighbors","TVRadio","SocialMedia"),
                c("Risk"),
                c("Evac"))

res <- inter.iamb(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
graphviz.plot(res, shape="rectangle")


