library(bnlearn)

#source("https://bioconductor.org/biocLite.R")
#biocLite("Rgraphviz")
library(Rgraphviz)

data <- read.csv("hurricane/Harvey/MTurk_Harvey_bn_v3.csv", header=TRUE)
#data <- lapply(data, as.numeric)
data <- lapply(data, as.ordered)
X <- as.data.frame(data)

demo1 <- c("age", "is_male","is_white", "is_black", "is_asian", "is_hispanic", "is_native")

demo2 <- c("edu", "income", "househd_size", "has_children", "has_elders", "has_special_needs", "has_pets")

house <- c("is_owner", "has_insurance", "coast_dist", "house_brick", "house_wood", "house_single_fam", "house_condo", "house_mobile")

info_tv <- c("use_tv_radio","tv_radio_people_stay","tv_radio_people_leave","tv_radio_road_traffic", "tv_radio_storm_damage", "tv_radio_casualty", "tv_radio_preparation")

info_social_media <- c("use_social_media","social_media_storm_damage", "social_media_storm_strength", "social_media_preparation", "social_media_road_traffic", "social_media_people_leave", "social_media_people_stay")

info_other <- c("friends_suggest_evac", "neighbors_stay", "friends_suggest_stay", "neighbors_evac")

evac_notice <- c("no_stay_notice", "no_evac_notice", "received_evac_notice", "received_mandatory", "received_voluntary", "received_stay_notice")

evac_decision <- c("evac_decision")

blklist <- list(c(demo1), c(demo2, house, info_tv, info_social_media, evac_notice), evac_decision)
#net <- iamb(X, alpha=0.01, blacklist = tiers2blacklist(blklist))
#graphviz.plot(net, shape="rectangle")

# explore
# sapply(X, class)
# sapply(X, levels)
# levels(X$age)
# learned <- hc(X)
# graphviz.plot(learned, shape="rectangle")
# score(learned, data=X, type="bic")
# arc.strength(learned, data=X, criterion="bic")

# random start
# nodes <- names(X)
# start <- random.graph(node=nodes, method="ic-dag", num=1000, every=50)
# netlist <- lapply(start, function(net){hc(X, score="bic", blacklist=tiers2blacklist(blklist), start=net)})
# rnd <- custom.strength(netlist, nodes=nodes)
# rnd[(rnd$strength > 0.85) & (rnd$direction >= 0.5), ]
# avg.start <- averaged.network(rnd, threshold = 0.85)
# graphviz.plot(avg.start, shape="rectangle")






#learned_net <- hc(X, score="bde", iss=15, blacklist=tiers2blacklist(blklist), start=prior)
learned_net <- hc(X, score="bic", blacklist=tiers2blacklist(blklist))
graphviz.plot(learned_net, shape="rectangle")


#learned_net <- gs(X, alpha=0.01, blacklist = tiers2blacklist(blklist), debug=TRUE)

# model averaging
boot <- boot.strength(X, R = 100, algorithm = "hc", algorithm.args = list(score="bic", blacklist=tiers2blacklist(blklist)))
#boot <- boot.strength(X, R = 1000, algorithm = "tabu", algorithm.args = list(score = "bic", blacklist=tiers2blacklist(blklist)))
#boot <- boot.strength(X, R = 100, algorithm = "gs", algorithm.args = list(alpha = 0.05, blacklist=tiers2blacklist(blklist)))
cutoff <- 0.7
boot[(boot$strength > cutoff) & (boot$direction >= 0.5), ]
avg.boot <- averaged.network(boot, threshold=cutoff)
graphviz.plot(avg.boot, shape="rectangle")

