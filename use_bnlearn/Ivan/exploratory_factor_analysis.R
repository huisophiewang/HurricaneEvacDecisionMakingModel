
library(plyr)
require(ggplot2)
require(reshape2)

# data <- read.csv("C:/Users/Sophie/workspace/Hurricane/Ivan/data/Ivan_common_state_county.csv", header=TRUE)
# t = count(data, 'state')
# 
# counts <- table(data$samp)
# barplot(counts)
# 
# melted <- melt(data, measure.vars=c("samp", "q1110"))
# colnames(melted)
# levels(melted$variable)
# levels(melted$value)
# head(melted)
# tail(melted)
# 
# counts <- table()
# 
# counts <- ddply(melted, c("group", "variable"), summarise,
#       mean=mean(value))
# 
# t <- table(data$samp, data$q1110)
# levels(data$q1110)
# 
# data <- read.csv("C:/Users/Sophie/workspace/Hurricane/Ivan/Ivan_test.csv", header=TRUE)
# data <- apply(data,2,max,na.rm=TRUE)




# factor analysis example
# https://blog.dominodatalab.com/how-to-do-factor-analysis/
library(psych)
describe(bfi)
df<-bfi[1:25]
scree(df)
fa.parallel(bfi)
res <- fa(r = df, nfactors = 5, rotate = 'oblimin', fm = 'minres')
print(res$loadings)



# factor analysis example
# https://web.stanford.edu/class/psych253/tutorials/FactorAnalysis.html
library(corrplot)
d = read.table("C:/Users/Sophie/Documents/Statistics/hurricane/IvanKatrinaStudies/personality0.txt")
head(d)
corrplot(cor(d))
corrplot(cor(d), order = "hclust",tl.col='black')
d_stan = as.data.frame(scale(d))
res1b = factanal(d_stan, factors = 10, rotation = "none", na.action = na.omit)
res1b$loadings
load = res1b$loadings[,1:2]
plot(load, type="n") # set up plot 
text(load,labels=names(d_stan)) # add variable names
### with rotation
res1a = factanal(d_stan, factors = 5, rotation = "varimax", na.action = na.omit)
res1a$loadings
load = res1a$loadings[,4:5]
plot(load, type="n") # set up plot 
text(load,labels=names(d_stan)) # add variable names

#############
# try on Ivan
d = read.csv("C:/Users/Sophie/workspace/Hurricane/Ivan/data/Ivan_common.csv")
head(d)
df = d[-51]
head(df)
corrplot(cor(df), order = "hclust",tl.col='black')

scree(df)
fa.parallel(df)
res <- fa(r = df, nfactors = 6, rotate = 'oblimin', fm = 'minres')
print(res$loadings)


# error if matrix is singular
res1b <- factanal(df, factors = 7, rotation = "varimax", na.action = na.omit)
res1b$loadings




     
