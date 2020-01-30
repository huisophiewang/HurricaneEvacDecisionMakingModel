library(bnlearn)
library(Rgraphviz)

data <- read.csv("C:/Users/Sophie/workspace/Hurricane/Ivan/data/Ivan_common.csv", header=TRUE)
data <- lapply(data, as.numeric)
X <- as.data.frame(data)
#sapply(data, class)

#demo <- c("age", "male","r_white", "r_black", "r_hispanic", "r_asian", "r_native")
#personal <- c("househd_size", "have_child", "have_elder", "income_above_4k", "college_edu", "owner", "pets")
#house <- c("ht_single_fam", "ht_mobile", "ht_condo", "hm_wood", "hm_brick_cement")
# geo <- c("close_to_coast", "elevation")
# order_issued <- c("issued_mandatory", "issued_voluntary")
# order_heard <- c("heard_order", "od_voluntary", "od_mandatory", "know_evac_zone", "ez_in_zone", "ez_not_in_zone")
# src <- c("src_local_radio", "src_local_tv", "src_cable_cnn", "src_cable_weather_channel", "src_cable_other", "src_internet", "importance_nhc", "importance_local_media", "trust_local_media")
# concern <- c("concern_wind", "concern_fld_surge", "concern_fld_rainfall", "concern_tornado")
# risk <- c("sf_cat4_water", "sf_cat4_wind_water", "sf_cat3_water", "sf_cat3_wind_water", "sf_cat2_water", "sf_cat2_wind_water")


demo <- c("age", "male","r_white")
personal <- c("income_above_4k", "college_edu")
house <- c("ht_single_fam", "ht_mobile")
geo <- c("close_to_coast", "elevation")
order <- c("heard_order", "od_voluntary", "od_mandatory")
risk <-("sf_cat3_wind_water")




X_sub <- X[c(demo, personal, house, geo, order, risk)]
#X_sub <- X[c("issued_mandatory", "issued_voluntary", "heard_order", "od_voluntary", "od_mandatory")]
#blklist <- list(c("issued_mandatory", "issued_voluntary"), c("heard_order", "od_voluntary", "od_mandatory"))
blklist <- list(c(demo, personal, house, geo, order), risk)

#res <- gs(X, alpha=0.01, blacklist = tiers2blacklist(list(c(demo, personal, house, geo, order_issued),c(order_heard, src, concern, risk), evac)))
#res <- gs(X_sub, alpha=0.01, blacklist = tiers2blacklist(list(demo, c(personal, house, geo), concern)))
#res <- gs(X_sub, alpha=0.01, blacklist = tiers2blacklist(blacklist))
res <- gs(X_sub, alpha=0.01, blacklist = tiers2blacklist(blklist))

graphviz.plot(res, shape="rectangle")



######################################################################################################
# with only objective variables

data <- read.csv("C:/Users/Sophie/workspace/Hurricane/BayesianNet/Ivan_common_test3.csv", header=TRUE)

# replace_val <- function(df, col_name){
#   df$col_name[df$col_name == 0] <- "a"
#   df$col_name[df$col_name == 1] <- "b" 
# }

col_names <- names(data)
# note: data[,'evac'] is vector, data['evac'] is dataframe
for(name in names(data)){
  data[,name][data[,name] == 0] <- "a"
  data[,name][data[,name] == 1] <- "b"
  data[,name] <- as.factor(data[,name])
}



c1 <- c("issued_order", "have_elder",
        "issued_order", "have_child",
        "issued_order", "pets",
        "issued_order", "college_edu",
        "issued_order", "income_above_4k",
        "close_to_coast", "have_elder",
        "close_to_coast", "have_child",
        "close_to_coast", "pets",
        "high_elev", "have_elder",
        "high_elev", "have_child",
        "high_elev", "pets",
        "income_above_4k", "have_elder",
        "income_above_4k", "have_child",
        "income_above_4k", "pets",
        "income_above_4k", "college_edu",
        "income_above_4k", "issued_order",
        "college_edu", "have_elder",
        "college_edu", "have_child",
        "college_edu", "pets",
        "college_edu", "issued_order",
        "owner", "have_elder",
        "owner", "have_child",
        "owner", "pets",
        "owner", "college_edu",
        "owner", "issued_order",
        "pets", "have_elder",
        "pets", "have_child",
        "pets", "owner",
        "pets", "college_edu",
        "pets", "income_above_4k",
        "pets", "hm_brick_cement",
        "pets", "ht_mobile",
        "pets", "high_elev",
        "pets", "close_to_coast",
        "pets", "issued_order",
        "have_child", "have_elder",
        "have_child", "pets",
        "have_child", "owner",
        "have_child", "college_edu",
        "have_child", "income_above_4k",
        "have_child", "hm_brick_cement",
        "have_child", "ht_mobile",
        "have_child", "high_elev",
        "have_child", "close_to_coast",
        "have_child", "issued_order",
        "have_elder", "have_child",
        "have_elder", "pets",
        "have_elder", "owner",
        "have_elder", "college_edu",
        "have_elder", "income_above_4k",
        "have_elder", "hm_brick_cement",
        "have_elder", "ht_mobile",
        "have_elder", "high_elev",
        "have_elder", "close_to_coast",
        "have_elder", "issued_order",
        "evac", "have_elder",
        "evac", "have_child",
        "evac", "pets",
        "evac", "owner",
        "evac", "college_edu",
        "evac", "income_above_4k",
        "evac", "hm_brick_cement",
        "evac", "ht_mobile",
        "evac", "high_elev",
        "evac", "close_to_coast",
        "evac", "issued_order"
        )

c2 <- c("issued_order", "have_elder",
        "issued_order", "have_child",
        "issued_order", "pets",
        "issued_order", "college_edu",
        "issued_order", "income_above_4k",
        # issue order is targeted to people live close to coast, and low lying area,
        # what's the direction of the edge should be?
        "close_to_coast", "have_elder",
        "close_to_coast", "have_child",
        "close_to_coast", "pets",
        "high_elev", "have_elder",
        "high_elev", "have_child",
        "high_elev", "pets",
        "income_above_4k", "have_elder",
        "income_above_4k", "have_child",
        "income_above_4k", "pets",
        #"income_above_4k", "college_edu",
        "income_above_4k", "issued_order",
        "college_edu", "have_elder",
        "college_edu", "have_child",
        "college_edu", "pets",
        "college_edu", "issued_order",
        "owner", "have_elder",
        "owner", "have_child",
        "owner", "pets",
        #"owner", "college_edu",
        "owner", "issued_order",
        "pets", "have_elder",
        "pets", "have_child",
        "pets", "owner",
        "pets", "college_edu",
        "pets", "income_above_4k",
        "pets", "hm_brick_cement",
        "pets", "ht_mobile",
        "pets", "high_elev",
        "pets", "close_to_coast",
        "pets", "issued_order",
        "have_child", "have_elder",
        "have_child", "pets",
        "have_child", "owner",
        "have_child", "college_edu",
        "have_child", "income_above_4k",
        "have_child", "hm_brick_cement",
        "have_child", "ht_mobile",
        "have_child", "high_elev",
        "have_child", "close_to_coast",
        "have_child", "issued_order",
        "have_elder", "have_child",
        "have_elder", "pets",
        "have_elder", "owner",
        "have_elder", "college_edu",
        "have_elder", "income_above_4k",
        "have_elder", "hm_brick_cement",
        "have_elder", "ht_mobile",
        "have_elder", "high_elev",
        "have_elder", "close_to_coast",
        "have_elder", "issued_order",
        "evac", "have_elder",
        "evac", "have_child",
        "evac", "pets",
        "evac", "owner",
        "evac", "college_edu",
        "evac", "income_above_4k",
        "evac", "hm_brick_cement",
        "evac", "ht_mobile",
        "evac", "high_elev",
        "evac", "close_to_coast",
        "evac", "issued_order"
)

c_from <- c1[seq(1, length(c1), 2)]
c_to <- c1[seq(1, length(c1), 2)+1]
bl <- data.frame(from=c_from, to=c_to) 

# bl <- data.frame(from="issued_order", to="have_elder", stringsAsFactors=FALSE) 
# bl <- rbind(bl, c("issued_order", "have_child"))

#####################################################################
# loss="logl"
#   negated expected loglikelihood; lower values are better.
#   loss function 'logl' may be used with discrete data only.
# loss="pred"
#   prediction error
#   loss function 'pred' may be used with discrete data only.

res0 <- hc(data)
graphviz.plot(res0, shape="rectangle")
bn.cv(data, 'hc', loss = "pred", loss.args = list(target = "evac"), runs=10)


res1 <- hc(data, blacklist = bl)
res1 <- tabu(data, blacklist = bl)
graphviz.plot(res1, shape="rectangle")
bn.cv(data, 'hc', algorithm.args = list(blacklist = bl), loss = "pred", loss.args = list(target = "evac"), runs=10)
bn.cv(data, 'hc', algorithm.args = list(blacklist = bl), loss = "logl")
bn.cv(data, 'tabu', algorithm.args = list(blacklist = bl), loss = "pred", loss.args = list(target = "evac"), runs=10)

res2 <- iamb(data, blacklist=bl)
plot(res2)

res3 <- gs(data, blacklist = bl)
plot(res3)







