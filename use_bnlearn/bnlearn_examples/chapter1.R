### R code from vignette source '/home/fizban/book-pratiqueR/english/chap1/chapter1.rnw'

###################################################
### code chunk number 1: chapter1.rnw:103-104
###################################################
library(bnlearn)


###################################################
### code chunk number 2: chapter1.rnw:108-109
###################################################
dag <- empty.graph(nodes = c("A", "S", "E", "O", "R", "T"))


###################################################
### code chunk number 3: chapter1.rnw:115-116
###################################################
dag


###################################################
### code chunk number 4: chapter1.rnw:126-127
###################################################
dag <- set.arc(dag, from = "A", to = "E")


###################################################
### code chunk number 5: chapter1.rnw:132-133
###################################################
dag <- set.arc(dag, from = "S", to = "E")


###################################################
### code chunk number 6: chapter1.rnw:139-141
###################################################
dag <- set.arc(dag, from = "E", to = "O")
dag <- set.arc(dag, from = "E", to = "R")


###################################################
### code chunk number 7: chapter1.rnw:148-150
###################################################
dag <- set.arc(dag, from = "O", to = "T")
dag <- set.arc(dag, from = "R", to = "T")


###################################################
### code chunk number 8: chapter1.rnw:157-158
###################################################
dag


###################################################
### code chunk number 9: chapter1.rnw:167-168
###################################################
modelstring(dag)


###################################################
### code chunk number 10: chapter1.rnw:187-189
###################################################
nodes(dag)
arcs(dag)


###################################################
### code chunk number 11: chapter1.rnw:195-205
###################################################
dag2 <- empty.graph(nodes = c("A", "S", "E", "O", "R", "T"))
arc.set <- matrix(c("A", "E",
                    "S", "E",
                    "E", "O",
                    "E", "R",
                    "O", "T",
                    "R", "T"),
             byrow = TRUE, ncol = 2,
             dimnames = list(NULL, c("from", "to")))
arcs(dag2) <- arc.set


###################################################
### code chunk number 12: chapter1.rnw:208-209
###################################################
all.equal(dag, dag2)


###################################################
### code chunk number 13: chapter1.rnw:232-238
###################################################
A.lv <- c("young", "adult", "old")
S.lv <- c("M", "F")
E.lv <- c("high", "uni")
O.lv <- c("emp", "self")
R.lv <- c("small", "big")
T.lv <- c("car", "train", "other")


###################################################
### code chunk number 14: chapter1.rnw:281-287
###################################################
A.prob <- array(c(0.30, 0.50, 0.20), dim = 3,
            dimnames = list(A = A.lv))
A.prob
S.prob <- array(c(0.60, 0.40), dim = 2,
            dimnames = list(S = S.lv))
S.prob


###################################################
### code chunk number 15: chapter1.rnw:294-300
###################################################
O.prob <- array(c(0.96, 0.04, 0.92, 0.08), dim = c(2, 2),
            dimnames = list(O = O.lv, E = E.lv))
O.prob
R.prob <- array(c(0.25, 0.75, 0.20, 0.80), dim = c(2, 2),
            dimnames = list(R = R.lv, E = E.lv))
R.prob


###################################################
### code chunk number 16: chapter1.rnw:307-309
###################################################
R.prob <- matrix(c(0.25, 0.75, 0.20, 0.80), ncol = 2,
            dimnames = list(R = R.lv, E = E.lv))


###################################################
### code chunk number 17: chapter1.rnw:311-312
###################################################
R.prob


###################################################
### code chunk number 18: chapter1.rnw:319-326
###################################################
E.prob <- array(c(0.75, 0.25, 0.72, 0.28, 0.88, 0.12, 0.64,
            0.36, 0.70, 0.30, 0.90, 0.10), dim = c(2, 3, 2),
            dimnames = list(E = E.lv, A = A.lv, S = S.lv))

T.prob <- array(c(0.48, 0.42, 0.10, 0.56, 0.36, 0.08, 0.58,
            0.24, 0.18, 0.70, 0.21, 0.09), dim = c(3, 2, 2),
            dimnames = list(T = T.lv, O = O.lv, R = R.lv))


###################################################
### code chunk number 19: chapter1.rnw:340-341
###################################################
dag3 <- model2network("[A][S][E|A:S][O|E][R|E][T|O:R]")


###################################################
### code chunk number 20: chapter1.rnw:345-346
###################################################
all.equal(dag, dag3)


###################################################
### code chunk number 21: chapter1.rnw:351-354
###################################################
cpt <- list(A = A.prob, S = S.prob, E = E.prob, O = O.prob, 
        R = R.prob, T = T.prob)
bn <- custom.fit(dag, cpt)


###################################################
### code chunk number 22: chapter1.rnw:359-360
###################################################
nparams(bn)


###################################################
### code chunk number 23: chapter1.rnw:367-368
###################################################
arcs(bn)


###################################################
### code chunk number 24: chapter1.rnw:373-374
###################################################
bn$R


###################################################
### code chunk number 25: chapter1.rnw:377-378
###################################################
R.cpt <- coef(bn$R)


###################################################
### code chunk number 26: chapter1.rnw:381-382 (eval = FALSE)
###################################################
## bn


###################################################
### code chunk number 27: chapter1.rnw:398-399
###################################################
setwd("/Users/sophie/Documents/Statistics/hurricane/bnlearn_examples/chapter1")
survey <- read.table("survey.txt", header = TRUE)


###################################################
### code chunk number 28: chapter1.rnw:403-404
###################################################
head(survey)


###################################################
### code chunk number 29: chapter1.rnw:427-428
###################################################
options(digits = 3)


###################################################
### code chunk number 30: chapter1.rnw:430-431
###################################################
bn.mle <- bn.fit(dag, data = survey, method = "mle")


###################################################
### code chunk number 31: chapter1.rnw:439-440
###################################################
prop.table(table(survey[, c("O", "E")]), margin = 2)


###################################################
### code chunk number 32: chapter1.rnw:443-444
###################################################
bn.mle$O


###################################################
### code chunk number 33: chapter1.rnw:454-456
###################################################
bn.bayes <- bn.fit(dag, data = survey, method = "bayes", 
              iss = 10)


###################################################
### code chunk number 34: chapter1.rnw:503-504
###################################################
bn.bayes$O


###################################################
### code chunk number 35: chapter1.rnw:526-529
###################################################
bn.bayes <- bn.fit(dag, data = survey, method = "bayes", 
              iss = 20)
bn.bayes$O


###################################################
### code chunk number 36: chapter1.rnw:629-631
###################################################
(nlevels(survey[, "T"]) - 1) * (nlevels(survey[, "E"]) - 1) * 
  (nlevels(survey[, "O"]) * nlevels(survey[, "R"]))


###################################################
### code chunk number 37: chapter1.rnw:643-644
###################################################
ci.test("T", "E", c("O", "R"), test = "mi", data = survey)


###################################################
### code chunk number 38: chapter1.rnw:647-648
###################################################
ci.test("T", "E", c("O", "R"), test = "x2", data = survey)


###################################################
### code chunk number 39: chapter1.rnw:664-665
###################################################
ci.test("T", "O", "R", test = "x2", data = survey)


###################################################
### code chunk number 40: chapter1.rnw:669-670
###################################################
options(digits = 2)


###################################################
### code chunk number 41: chapter1.rnw:676-677
###################################################
arc.strength(dag, data = survey, criterion = "x2")


###################################################
### code chunk number 42: chapter1.rnw:734-736
###################################################
set.seed(456)
options(digits = 6)


###################################################
### code chunk number 43: chapter1.rnw:738-740
###################################################
score(dag, data = survey, type = "bic")
score(dag, data = survey, type = "bde", iss = 10)


###################################################
### code chunk number 44: chapter1.rnw:748-749
###################################################
score(dag, data = survey, type = "bde", iss = 1)


###################################################
### code chunk number 45: chapter1.rnw:761-764
###################################################
dag4 <- set.arc(dag, from = "E", to = "T")
nparams(dag4, survey)
score(dag4, data = survey, type = "bic")


###################################################
### code chunk number 46: chapter1.rnw:775-778
###################################################
rnd <- random.graph(nodes = c("A", "S", "E", "O", "R", "T"))
modelstring(rnd)
score(rnd, data = survey, type = "bic")


###################################################
### code chunk number 47: chapter1.rnw:790-793
###################################################
learned <- hc(survey)
modelstring(learned)
score(learned, data = survey, type = "bic")


###################################################
### code chunk number 48: chapter1.rnw:797-798
###################################################
learned2 <- hc(survey, score = "bde")


###################################################
### code chunk number 49: chapter1.rnw:807-808
###################################################
options(digits=3)


###################################################
### code chunk number 50: chapter1.rnw:811-812
###################################################
arc.strength(learned, data = survey, criterion = "bic")


###################################################
### code chunk number 51: chapter1.rnw:816-817
###################################################
arc.strength(dag, data = survey, criterion = "bic")


###################################################
### code chunk number 52: chapter1.rnw:824-825
###################################################
options(digits = 3)


###################################################
### code chunk number 53: chapter1.rnw:880-882
###################################################
dsep(dag, x = "S", y = "R")
dsep(dag, x = "O", y = "R")


###################################################
### code chunk number 54: chapter1.rnw:890-891
###################################################
path(dag, from = "S", to = "R")


###################################################
### code chunk number 55: chapter1.rnw:895-896
###################################################
dsep(dag, x = "S", y = "R", z = "E")


###################################################
### code chunk number 56: chapter1.rnw:908-909
###################################################
dsep(dag, x = "O", y = "R", z = "E")


###################################################
### code chunk number 57: chapter1.rnw:919-921
###################################################
dsep(dag, x = "A", y = "S")
dsep(dag, x = "A", y = "S", z = "E")


###################################################
### code chunk number 58: chapter1.rnw:1012-1013
###################################################
library(gRain)


###################################################
### code chunk number 59: chapter1.rnw:1019-1020
###################################################
junction <- compile(as.grain(bn))


###################################################
### code chunk number 60: chapter1.rnw:1032-1033
###################################################
options(digits = 4)


###################################################
### code chunk number 61: chapter1.rnw:1035-1038
###################################################
querygrain(junction, nodes = "T")$T
jsex <- setEvidence(junction, nodes = "S", states = "F")
querygrain(jsex, nodes = "T")$T


###################################################
### code chunk number 62: chapter1.rnw:1064-1066
###################################################
jres <- setEvidence(junction, nodes = "R", states = "small")
querygrain(jres, nodes = "T")$T


###################################################
### code chunk number 63: chapter1.rnw:1085-1089
###################################################
jedu <- setEvidence(junction, nodes = "E", states = "high")
SxT.cpt <- querygrain(jedu, nodes = c("S", "T"),
             type = "joint")
SxT.cpt


###################################################
### code chunk number 64: chapter1.rnw:1094-1095
###################################################
querygrain(jedu, nodes = c("S", "T"), type = "marginal")


###################################################
### code chunk number 65: chapter1.rnw:1102-1103
###################################################
querygrain(jedu, nodes = c("S", "T"), type = "conditional")


###################################################
### code chunk number 66: chapter1.rnw:1129-1130
###################################################
dsep(bn, x = "S", y = "T", z = "E")


###################################################
### code chunk number 67: chapter1.rnw:1137-1138
###################################################
SxT.ct = SxT.cpt * nrow(survey)


###################################################
### code chunk number 68: chapter1.rnw:1144-1145
###################################################
chisq.test(SxT.ct)


###################################################
### code chunk number 69: chapter1.rnw:1178-1179
###################################################
set.seed(123)


###################################################
### code chunk number 70: chapter1.rnw:1181-1183
###################################################
cpquery(bn, event = (S == "M") & (T == "car"), 
          evidence = (E == "high"))


###################################################
### code chunk number 71: chapter1.rnw:1191-1193
###################################################
cpquery(bn, event = (S == "M") & (T == "car"), 
            evidence = (E == "high"), n = 10^6)


###################################################
### code chunk number 72: chapter1.rnw:1206-1207
###################################################
set.seed(567)


###################################################
### code chunk number 73: chapter1.rnw:1209-1211
###################################################
cpquery(bn, event = (S == "M") & (T == "car"),
            evidence = list(E = "high"), method = "lw")


###################################################
### code chunk number 74: chapter1.rnw:1229-1230
###################################################
set.seed(123)


###################################################
### code chunk number 75: chapter1.rnw:1232-1234
###################################################
cpquery(bn, event = (S == "M") & (T == "car"),
  evidence = ((A == "young") & (E == "uni")) | (A == "adult"))


###################################################
### code chunk number 76: chapter1.rnw:1244-1247
###################################################
SxT <- cpdist(bn, nodes = c("S", "T"),
         evidence = (E == "high"))
head(SxT)


###################################################
### code chunk number 77: chapter1.rnw:1255-1256
###################################################
options(digits = 3)


###################################################
### code chunk number 78: chapter1.rnw:1258-1259
###################################################
prop.table(table(SxT))


###################################################
### code chunk number 79: chapter1.rnw:1295-1296
###################################################
graphviz.plot(dag)


###################################################
### code chunk number 80: chapter1.rnw:1318-1320
###################################################
hlight <- list(nodes = nodes(dag), arcs = arcs(dag), 
                  col = "grey", textCol = "grey")


###################################################
### code chunk number 81: chapter1.rnw:1325-1326
###################################################
pp <- graphviz.plot(dag, highlight = hlight)


###################################################
### code chunk number 82: chapter1.rnw:1332-1335
###################################################
edgeRenderInfo(pp) <- 
  list(col = c("S~E" = "black", "E~R" = "black"),
       lwd = c("S~E" = 3, "E~R" = 3))


###################################################
### code chunk number 83: chapter1.rnw:1347-1351
###################################################
nodeRenderInfo(pp) <- 
  list(col = c("S" = "black", "E" = "black", "R" = "black"),
    textCol = c("S" = "black", "E" = "black", "R" = "black"),
    fill = c("E" = "grey"))


###################################################
### code chunk number 84: chapter1.rnw:1355-1356
###################################################
renderGraph(pp)


###################################################
### code chunk number 85: chapter1.rnw:1392-1394
###################################################
bn.fit.barchart(bn.mle$T, main = "Travel", 
  xlab = "Pr(T | R,O)", ylab = "")


###################################################
### code chunk number 86: chapter1.rnw:1418-1427
###################################################
Evidence <- 
  factor(c(rep("Unconditional",3), rep("Female", 3), 
           rep("Small City",3)),
         levels = c("Unconditional", "Female", "Small City"))
Travel <- factor(rep(c("car", "train", "other"), 3),
           levels = c("other", "train", "car"))
distr <- data.frame(Evidence = Evidence, Travel = Travel,
           Prob = c(0.5618, 0.2808, 0.15730, 0.5620, 0.2806,
                    0.1573, 0.4838, 0.4170, 0.0990))


###################################################
### code chunk number 87: chapter1.rnw:1432-1433
###################################################
head(distr)


###################################################
### code chunk number 88: chapter1.rnw:1437-1448
###################################################
barchart(Travel ~ Prob | Evidence, data = distr,
   layout = c(3, 1), xlab = "probability",
   scales = list(alternating = 1, tck = c(1, 0)),
   strip = strip.custom(factor.levels =
     c(expression(Pr(T)),
       expression(Pr({T} * " | " * {S == F})),
       expression(Pr({T} * " | " * {R == small})))),
   panel = function(...) {
     panel.barchart(...)
     panel.grid(h = 0, v = -1)
   })


