library(bnlearn)
library(Rgraphviz)

data(learning.test)


res = gs(learning.test)
res1 = set.arc(gs(learning.test), "A", "B")
res2 = set.arc(gs(learning.test), "B", "A")


score(res1, learning.test, type = "loglik")
score(res2, learning.test, type = "loglik")
score(res1, learning.test, type = "bic")
score(res2, learning.test, type = "bic")
score(res1, learning.test, type = "aic")
score(res2, learning.test, type = "aic")

score(res1, learning.test, type = "k2")


blacklist = data.frame(from = c("A", "D"), to = c("D", "A"))
res3 = gs(learning.test, blacklist = blacklist)
plot(res3)


whitelist = data.frame(from = c("E"), to = c("F"))
res4 = gs(learning.test, whitelist = whitelist)
plot(res4)

#bn.fit fits the parameters of a Bayesian network given its structure and a data set; 
#bn.net returns the structure underlying a fitted Bayesian network.
fitted = bn.fit(res1, learning.test)

# discrete Bayesian network from expert knowledge.
net = model2network("[A][B][C|A:B]")
cptA = matrix(c(0.4, 0.6), ncol = 2, dimnames = list(NULL, c("LOW", "HIGH")))
cptB = matrix(c(0.8, 0.2), ncol = 2, dimnames = list(NULL, c("GOOD", "BAD")))
cptC = c(0.5, 0.5, 0.4, 0.6, 0.3, 0.7, 0.2, 0.8)
dim(cptC) = c(2, 2, 2)
dimnames(cptC) = list("C" = c("TRUE", "FALSE"), "A" =  c("LOW", "HIGH"),
                      "B" = c("GOOD", "BAD"))
cfit = custom.fit(net, dist = list(A = cptA, B = cptB, C = cptC))


bn.boot(data = learning.test, R = 2, m = 500, algorithm = "gs",
        statistic = arcs)

res = gs(learning.test)
res = set.arc(res, "A", "B")
arc.strength(res, learning.test)

arcs = boot.strength(learning.test, algorithm = "hc")
arcs[(arcs$strength > 0.85) & (arcs$direction >= 0.5)]
averaged.network(arcs)

res5 = hc(learning.test)
plot(res5)
fitted = bn.fit(res5, learning.test)
coefficients(fitted$E)

cv_res <- bn.cv(learning.test, 'hc', loss = "pred", loss.args = list(target = "F"), runs=100)

cv.bic = bn.cv(alarm, bn = "hc", runs = 10,algorithm.args = list(score = "bic"))
