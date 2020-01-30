library(bnlearn)
library(plyr)

######################################################################################################




data <- read.csv("hurricane/Irma/Irma_11clusters.csv", header=TRUE)
# cluster1: race, pets
# cluster2: finance
# cluster3: children
# cluster4: elders, special_needs
# cluster5: house_type, insurance
# cluster6: house_material, type
# cluster7: evac_notice, friends, neighbors
# cluster8: tv_radio
# cluster9: social_media
# cluster10: evac_notice
# cluster11: risk
X <- rename(data, c("cluster1"="Race_Pets", "cluster2"="Finance",
                    "cluster3"="Children", "cluster4"="Elders_SpecialNeeds",
                    "cluster5"="HouseType_Insurance", "cluster6"="HouseMaterial_Type",
                    "cluster7"="EvacNotice_Friends_Neighbors","cluster8"="TVRadio",
                    "cluster9"="SocialMedia", "cluster10"="VolutaryEvacNotice",
                    "cluster11"="Risk", "evac_decision"="Evac"))

X <- discretize(X[,1:11], method='interval', breaks=3, ordered=TRUE)
X$Evac = data$evac_decision
X$Evac <- as.ordered(X$Evac)
blklist <- list(c("Race_Pets","Finance","Elders_SpecialNeeds","Children",
                  "HouseType_Insurance","HouseMaterial_Type","VolutaryEvacNotice",
                  "EvacNotice_Friends_Neighbors","TVRadio","SocialMedia"),
                c("Risk"),
                c("Evac"))

res <- inter.iamb(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
#res <- inter.iamb(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
#res <- si.hiton.pc(X, alpha=0.05, blacklist = tiers2blacklist(blklist))
graphviz.plot(res, shape="rectangle")