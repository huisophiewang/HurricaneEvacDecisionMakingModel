###################################################
# read write files
X <- read.csv("C:/Users/Sophie/Statistics/Personality/feature/all_wifi_features.csv", header=TRUE)
write.csv(ivan_data, file = "Statistics/hurricane/IvanKatrinaStudies/IvanExport.csv")


###################################################
# basic statistics
###################################################
library(moments)
lapply(X, mean)
lapply(X, var)
lapply(X, median)
lapply(X, min)
lapply(X, max)
lapply(X, skewness)

###################################################
# correlation 
###################################################
# correlation matrix
cor(X[,14:18])
# correlation plot
pairs(X[,2:8])



###################################################
# plots 
###################################################
# boxplot
boxplot(X$extra, main="extroversion")
# histogram
hist(X$extra)
# qqplot
x <- X$extra
x <- (x-mean(x))/sd(x)
qqnorm(x)
qqline(x)
# plot
plot(price ~ carat, data=diamonds, col="blue")


###################################################
# data types 
###################################################
# check dataframe
is.data.frame(data)
# get the type of a column
class(data$extra)
# numeric, factor, ordered
data <- lapply(data, as.numeric)
X <- as.data.frame(data)
# array (items are the same type)
array(1:18, dim=c(3,3,2))
# matrix (items are the same type)
matrix(1:9, nrow=3, ncol=3)
# list (items can be different types)
y <- list(TRUE, 1, "a")
# dataframe (items can be different types)
# get column names
names(data)
# get dimensions
dim(data)
# select column by name
# data[name] is dataframe
# data[,name] is vector
data[4:9,c(1,3)]



###################################################
# vector 
###################################################

house <- c("is_owner", "coast_dist")
index <- c(2,4,5,6,7,8,9,10,11,12,13,14,15)
index <- c(2:15)




###################################################
# for loop
###################################################
index <- c(2,4,5,6)
for(i in index){
  m1 <- lm(Y ~ X[,3] + X[,i])
  print(summary(m1))
}

###################################################
# function
###################################################
foo <- function(x) {
  x + 1 # functions return the value last evaluated
  }

foo(3)

do.fun <- function(x, f) {
  f(x) # functions can be passed to other functions
  }

do.fun(2, foo)

###################################################
# normalize each column
###################################################
data <- read.csv("hurricane/Harvey/MTurk_Harvey_var_cluster_v2.csv", header=TRUE)
col_names <- names(data)
dnorm <- apply(data, 2, scale)
apply(dnorm, 2, mean)
apply(dnorm, 2, sd)
X <- as.data.frame(dnorm, col.names=col_names)

