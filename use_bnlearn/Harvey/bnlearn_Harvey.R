library(bnlearn)

#source("https://bioconductor.org/biocLite.R")
#biocLite("Rgraphviz")
library(Rgraphviz)

data <- read.csv("hurricane/Harvey/MTurk_Harvey_bn.csv", header=TRUE)
#data <- lapply(data, as.numeric)
data <- lapply(data, as.ordered)
X <- as.data.frame(data)

demo1 <- c("age", "is_white")

demo2 <- c("househd_size", "edu", "income", "has_children", "has_elders", "has_special_needs", "has_pets")

house <- c("house_mobile", "is_owner", "has_insurance", "coast_dist")

info_tv <- c("tv_radio_people_stay", "tv_radio_people_leave")

info_social_media <- c("social_media_people_stay", "social_media_people_leave")

info_other <- c("friends_suggest_evac", "neighbors_evac")

evac_notice <- c("received_evac_notice", "received_stay_notice")

risk <- c("risk_of_stay", "risk_of_evac", "safety_risk", "property_risk")

evac_ability <- c("difficulty_family", "difficulty_means")

evac_decision <- c("evac_decision")

blklist <- list(c(demo1), c(demo2, house, info_tv, info_social_media, info_other, evac_notice), c(risk, evac_ability), evac_decision)
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



prior <- empty.graph(nodes=names(X))

# demo
prior <- set.arc(prior, from="age", to="difficulty_family")
prior <- set.arc(prior, from="househd_size", to="difficulty_family")
prior <- set.arc(prior, from="has_children", to="difficulty_family")
prior <- set.arc(prior, from="has_elders", to="difficulty_family")
prior <- set.arc(prior, from="has_special_needs", to="difficulty_family")
prior <- set.arc(prior, from="has_pets", to="difficulty_family")
prior <- set.arc(prior, from="age", to="difficulty_means")
prior <- set.arc(prior, from="edu", to="difficulty_means")
prior <- set.arc(prior, from="is_white", to="difficulty_means")
prior <- set.arc(prior, from="income", to="difficulty_means")


# house
prior <- set.arc(prior, from="coast_dist", to="risk_of_stay")
prior <- set.arc(prior, from="coast_dist", to="risk_of_evac")
prior <- set.arc(prior, from="coast_dist", to="safety_risk")
prior <- set.arc(prior, from="coast_dist", to="property_risk")
prior <- set.arc(prior, from="house_mobile", to="risk_of_stay")
prior <- set.arc(prior, from="house_mobile", to="safety_risk")
prior <- set.arc(prior, from="house_mobile", to="property_risk")
prior <- set.arc(prior, from="is_owner", to="risk_of_stay")
prior <- set.arc(prior, from="is_owner", to="property_risk")
prior <- set.arc(prior, from="has_insurance", to="risk_of_stay")
prior <- set.arc(prior, from="has_insurance", to="property_risk")

# media
prior <- set.arc(prior, from="tv_radio_people_stay", to="risk_of_stay")
prior <- set.arc(prior, from="tv_radio_people_leave", to="risk_of_stay")
prior <- set.arc(prior, from="social_media_people_stay", to="risk_of_stay")
prior <- set.arc(prior, from="social_media_people_leave", to="risk_of_stay")
prior <- set.arc(prior, from="friends_suggest_evac", to="risk_of_stay")
prior <- set.arc(prior, from="neighbors_evac", to="risk_of_stay")

# evac notice
prior <- set.arc(prior, from="received_evac_notice", to="risk_of_stay")
prior <- set.arc(prior, from="received_stay_notice", to="risk_of_evac")

# 2nd layer
prior <- set.arc(prior, from="difficulty_family", to="evac_decision")
prior <- set.arc(prior, from="difficulty_means", to="evac_decision")
prior <- set.arc(prior, from="risk_of_stay", to="evac_decision")
prior <- set.arc(prior, from="risk_of_evac", to="evac_decision")
prior <- set.arc(prior, from="safety_risk", to="evac_decision")
prior <- set.arc(prior, from="property_risk", to="evac_decision")


### cause error - attempting to create a factor with more than INT_MAX levels.?????
### reason: risk_of_stay has too many parents (8+6+6+7=27)




# prior <- set.arc(prior, from="tv_radio_preparation", to="wind_risk_to_property")
# prior <- set.arc(prior, from="tv_radio_preparation", to="flood_risk_to_property")


#learned_net <- hc(X, score="bde", iss=15, blacklist=tiers2blacklist(blklist), start=prior)
learned_net <- hc(X, score="bic", blacklist=tiers2blacklist(blklist), start=prior)
graphviz.plot(learned_net, shape="rectangle")


#learned_net <- gs(X, alpha=0.01, blacklist = tiers2blacklist(blklist), debug=TRUE)

# model averaging
boot <- boot.strength(X, R = 1000, algorithm = "hc", algorithm.args = list(score="bic", blacklist=tiers2blacklist(blklist), start=prior))
#boot <- boot.strength(X, R = 1000, algorithm = "tabu", algorithm.args = list(score = "bic", blacklist=tiers2blacklist(blklist)))
#boot <- boot.strength(X, R = 100, algorithm = "gs", algorithm.args = list(alpha = 0.05, blacklist=tiers2blacklist(blklist)))
cutoff <- 0.5
boot[(boot$strength > cutoff) & (boot$direction >= 0.5), ]
avg.boot <- averaged.network(boot, threshold=cutoff)
graphviz.plot(avg.boot, shape="rectangle")

