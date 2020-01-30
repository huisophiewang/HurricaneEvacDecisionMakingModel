#######################################################################################
library(bnlearn)
library(Rgraphviz)
data <- read.csv("C:/Users/Sophie/workspace/Hurricane/Lili/data/Lili_BN_labels.csv", header=TRUE)

#data <- d1[,sample(ncol(d1))]
#cor(data)
#data <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels_NotEvac.csv", header=TRUE)
#data <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels_EarlyEvac.csv", header=TRUE)
#data <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels_LateEvac.csv", header=TRUE)
#data <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels_LowIncome.csv", header=TRUE)
#data <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels_HighIncome.csv", header=TRUE)
#data <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels_VeryLowIncome.csv", header=TRUE)
#data <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels_Young.csv", header=TRUE)
#data <- read.csv("C:/Users/Sophie/workspace/LiliModel/Lili_BN_labels_Old.csv", header=TRUE)
#hist(data$Edu)
#hist(data$HouseStruct)

# 1-4
demo <- c("Age", "Gender", "Race", "Marriage")
# 5-8
personal <- c("HouseholdSize", "NumChd", "Edu", "Income")
# 9-12
house <- c("Owner", "HouseStruct", "CloseCoast","CloseWater")
# 13-14
official <- c("OfficialHurricWatch", "OfficialEvac")
# 15-19
info <- c("SrcLocalAuth", "SrcLocalMedia", "SrcNationalMedia", "SrcInternet", "SrcPeers")
#local_info <- c("SrcLocalAuth", "SrcLocalMedia", "SrcPeers")
# 20-22
see <- c("SeeStormCond", "SeeShopClose", "SeePeerEvac")
# 23-24
prev <- c("PrevStormExp", "PrevFalseAlarm")
# 25-29
concern <- c("ProtectFromLooter", "ProtectFromStorm", "LostIncome", "EvacExpense", "Traffic")
# 30
evac <- c("Evac")

X <- data
#X <- data[, c( 20, 21, 22, 28, 30)]

#X <- data[, c(9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 28, 30)]
#X <- data[, c( 11, 13, 14, 15, 19, 22, 30)]

#X <- cbind(close, see, peer, data["OfficialHurricWatch"], data["OfficialEvac"], prev, finance, data["Traffic"], data["Evac"])

#res <- gs(X, alpha=0.01)
#res <- gs(X, alpha=0.05, blacklist = tiers2blacklist(list(c("CloseCoast","CloseWater", sources, "concern"), evac)))
#res1 <- gs(X, alpha=0.01, blacklist = tiers2blacklist(list(c(demo, personal, house),  c(see, "EvacExpense", official),"Evac")))
#res1 <- gs(X, alpha=0.05, blacklist = tiers2blacklist(list(house, c(see, official, local_info, "EvacExpense"), evac)))
#res1 <- inter.iamb(X, alpha=0.01, blacklist = tiers2blacklist(list(c("CloseCoast", "OfficialHurricWatch", "OfficialEvac", "SrcLocalAuth", "SrcPeers", "SeePeerEvac"), evac)))
res1 <- iamb(X, alpha=0.01, blacklist = tiers2blacklist(list(c(demo, personal, house),c(prev, official, info, see, concern), evac)))
#res2 <- hc(X, blacklist = tiers2blacklist(list(reasons, "Evac")))
#compare(res1, res2)
#res <- inter.iamb(X)
#plot(res)

#res1 <- gs(X, alpha=0.01, blacklist = tiers2blacklist(list(c(demo, personal, house),  c(official, see, info, prev, concern),"Evac")))
graphviz.plot(res1, shape="rectangle")

#######################################################################################
library(bnlearn)
library(Rgraphviz)
data <- read.csv("C:/Users/Sophie/workspace/HurricaneLiliModel/Lili_converted.csv", header=TRUE)
#cor(data)
demo <- c('Age', 'Gender', 'r_black', 'r_native', 'r_other')
personal <- c('m_single', 'm_other', "HouseholdSize", "NumChd", "e_someclg", "e_clg", "Income")
house <- c('Owner', 'h_mobile', 'h_other', "CloseCoast", "CloseWater")
official <- c("OfficialHurricWatch", "OfficialEvac")
info <- c("SrcLocalAuth", "SrcLocalMedia", "SrcNationalMedia", "SrcInternet", "SrcPeers")
see <- c("SeeStormCond", "SeeShopClose", "SeePeerEvac")
prev <- c("PrevStormExp", "PrevFalseAlarm")
concern <- c("ProtectFromLooter", "ProtectFromStorm", "LostIncome", "EvacExpense", "Traffic")
evac <- c("Evac")
X <- data
#res1 <- gs(X, alpha=0.01)
res1 <- gs(X, alpha=0.01, blacklist = tiers2blacklist(list(demo, c(personal, house),c(prev, official, info, see, concern),evac)))
graphviz.plot(res1, shape="rectangle")