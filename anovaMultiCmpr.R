#========================================
# random data and groups:
testValue <- runif(35) # not normal data
testValue <- rnorm(35) # normal data
groupName = factor(rep(c("A", "B", "C"), 35))

data<- data.frame(testValue, groupName)
#========================================
# normality test ========================
# before we do ANOVA, is data normal (p>0.05)?
# - if p>0.05, do ANOVA. - if p<0.05, consider other options (Kruskaltest?)
shapiro.test(data$testValue)
qqnorm(data$testValue) # qunatile plot

#========================================
# equal variance test ===================
levene.test(data$testValue,data$groupName)

#========================================
# ANOVA test ============================
anovadata <- lm(data$testValue ~ data$groupName )
summary(anovadata)
anova(anovadata)

#========================================
# pairwise comparisons ==================
a1 <- aov(data$testValue ~ data$groupName)
posthoc <- TukeyHSD(x=a1,conf.level=0.95)
posthoc





#========================================
#========================================
# other options... ==================
# kruskal wallis for all groups

library(agricolae)

padjVal <- "bonferroni" # type of p-value adjustment
alphaVal <- 0.05 # alpha value to test

kruskal.test(data$testValue ~ data$groupName)
statsKruskal = kruskal(data$testValue,data$groupName, p.adj=padjVal,alpha=0.05)
statsKruskal
