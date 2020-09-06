setwd("/Users/jisunan/myRepository/code-demographical-differences/demo-validation/05_crowdflower")
library(ggplot2)



data <- read.table("compare_conf_NY.txt", sep="\t", header=T)
data$cf_race_group_3 <- as.factor(data$cf_race_group_3)
data$facepp_group_3 <- as.factor(data$facepp_group_3)
data$facepp_group_5 <- as.factor(data$facepp_group_5)
data$facepp_group_10 <- as.factor(data$facepp_group_10)
data$facepp_group_82 <- as.factor(data$facepp_group_82)
summary(data)
nrow(data)

cor.test(data$facepp_race_conf, data$cf_race_conf, method="pearson")
cor.test(data$facepp_race_conf, data$cf_race_conf, method="spearman")


get_median <- function(x) quantile(x, 0.5)

data$facepp_group_82 <- with(data, reorder(data$facepp_group_82, data$cf_race_conf, mean))
, outlier.shape=NA

ggplot(data, aes(x=factor(facepp_group_82), y=cf_race_conf)) + geom_boxplot(aes(fill=facepp_group_82)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF confidence value") +
  xlab("Face++ confidence value") +
  #scale_x_discrete(labels=c("1" = "[0.33,0.66)", "2" = "[0.66,1.00)")) + 
  ggtitle("NY") +
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_fpp2cf_group82_NY.png", height=8, width=5)
ggsave("plots/compare_fpp2cf_group82_NY.pdf", height=8, width=5)

data$facepp_group_3 <- with(data, reorder(data$facepp_group_3, data$cf_race_conf, mean))
, outlier.shape=NA

ggplot(data, aes(x=factor(facepp_group_3), y=cf_race_conf)) + geom_boxplot(aes(fill=facepp_group_3)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF confidence value") +
  xlab("Face++ confidence value") +
  scale_x_discrete(labels=c("1" = "[0.33,0.66)", "2" = "[0.66,1.00)")) + 
  ggtitle("NY") +
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_fpp2cf_group3_NY.png", height=8, width=5)
ggsave("plots/compare_fpp2cf_group3_NY.pdf", height=8, width=5)

data$facepp_group_5 <- with(data, reorder(data$facepp_group_5, data$cf_race_conf, mean))

ggplot(data, aes(x=factor(facepp_group_5), y=cf_race_conf)) + geom_boxplot(aes(fill=facepp_group_5)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF confidence value") +
  xlab("Face++ confidence value") +
  #scale_x_discrete(limits=c("1","2","3","4"), breaks=c("1","2","3", "4"),
                       #labels=c("[0.2,0.4)", "[0.4,0.6)", "[0.6,0.8)", "[0.8,1]")) + 
  scale_x_discrete(limits=c("2","3","4"), breaks=c("2","3", "4"),
                   labels=c("[0.4,0.6)", "[0.6,0.8)", "[0.8,1]")) + 
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  ggtitle("NY") +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_fpp2cf_group5_NY.png", height=8, width=5)
ggsave("plots/compare_fpp2cf_group5_NY.pdf", height=8, width=5)

data$facepp_group_10 <- with(data, reorder(data$facepp_group_10, data$cf_race_conf, mean))
ggplot(data, aes(x=factor(facepp_group_10), y=cf_race_conf)) + geom_boxplot(aes(fill=facepp_group_10)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  geom_text(aes(y = max,label = length(facepp_group_10)),vjust = 0) + 
  ylab("CF confidence value") +
  xlab("Face++ confidence value") +
  #scale_x_discrete(limits=c("3","4","5","6","7","8","9"), breaks=c("3","4","5","6","7","8","9"),
                   #labels=c("[0.3,0.4)", "[0.4,0.5)", "[0.5,0.6)", "[0.6,0.7)", "[0.7,0.8)", "[0.8,0.9)", "[0.9,1]")) + 
  scale_x_discrete(limits=c("5","6","7","8","9"), breaks=c("5","6","7","8","9"),
                   labels=c("[0.5,0.6)", "[0.6,0.7)", "[0.7,0.8)", "[0.8,0.9)", "[0.9,1]")) + 
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  ggtitle("NY") +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_fpp2cf_group10_NY.png", height=8, width=5)
ggsave("plots/compare_fpp2cf_group10_NY.pdf", height=8, width=5)



data$cf_race_group_3 <- with(data, reorder(data$cf_race_group_3, data$facepp_race_conf, mean))

ggplot(data, aes(x=factor(cf_race_group_3), y=facepp_race_conf)) + geom_boxplot(aes(fill=cf_race_group_3)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  xlab("CF confidence value") +
  ylab("Face++ confidence value") +
  scale_x_discrete(limits=c("0","1","2"), breaks=c("0","1","2"),
                   labels=c("[0.0,0.4)", "[0.4,0.7)", "[0.7,1]")) + 
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  ggtitle("NY") +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_cf2fpp_group3_NY.png", height=8, width=5)
ggsave("plots/compare_cf2fpp_group3_NY.pdf", height=8, width=5)



-----------------------
  
data <- read.table("compare_conf_texas.txt", sep="\t", header=T)
data$cf_race_group_3 <- as.factor(data$cf_race_group_3)
data$facepp_group_3 <- as.factor(data$facepp_group_3)
data$facepp_group_5 <- as.factor(data$facepp_group_5)
data$facepp_group_10 <- as.factor(data$facepp_group_10)
summary(data)

cor.test(data$facepp_race_conf, data$cf_race_conf, method="pearson")
cor.test(data$facepp_race_conf, data$cf_race_conf, method="spearman")


get_median <- function(x) quantile(x, 0.5)

data$facepp_group_82 <- with(data, reorder(data$facepp_group_82, data$cf_race_conf, mean))
, outlier.shape=NA

ggplot(data, aes(x=factor(facepp_group_82), y=cf_race_conf)) + geom_boxplot(aes(fill=facepp_group_82)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF confidence value") +
  xlab("Face++ confidence value") +
  #scale_x_discrete(labels=c("1" = "[0.33,0.66)", "2" = "[0.66,1.00)")) + 
  ggtitle("Texas") +
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_fpp2cf_group82_Texas.png", height=8, width=5)
ggsave("plots/compare_fpp2cf_group82_Texas.pdf", height=8, width=5)



data$facepp_group_3 <- with(data, reorder(data$facepp_group_3, data$cf_race_conf, mean))
, outlier.shape=NA

ggplot(data, aes(x=factor(facepp_group_3), y=cf_race_conf)) + geom_boxplot(aes(fill=facepp_group_3)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF confidence value") +
  xlab("Face++ confidence value") +
  scale_x_discrete(labels=c("1" = "[0.33,0.66)", "2" = "[0.66,1.00)")) + 
  ggtitle("Texas") +
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_fpp2cf_group3_Texas.png", height=8, width=5)
ggsave("plots/compare_fpp2cf_group3_Texas.pdf", height=8, width=5)

data$facepp_group_5 <- with(data, reorder(data$facepp_group_5, data$cf_race_conf, mean))

ggplot(data, aes(x=factor(facepp_group_5), y=cf_race_conf)) + geom_boxplot(aes(fill=facepp_group_5)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF confidence value") +
  xlab("Face++ confidence value") +
  #scale_x_discrete(limits=c("1","2","3","4"), breaks=c("1","2","3", "4"),
  #labels=c("[0.2,0.4)", "[0.4,0.6)", "[0.6,0.8)", "[0.8,1]")) + 
  scale_x_discrete(limits=c("2","3","4"), breaks=c("2","3", "4"),
                   labels=c("[0.4,0.6)", "[0.6,0.8)", "[0.8,1]")) + 
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  ggtitle("Texas") +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_fpp2cf_group5_Texas.png", height=8, width=5)
ggsave("plots/compare_fpp2cf_group5_Texas.pdf", height=8, width=5)

data$facepp_group_10 <- with(data, reorder(data$facepp_group_10, data$cf_race_conf, mean))
ggplot(data, aes(x=factor(facepp_group_10), y=cf_race_conf)) + geom_boxplot(aes(fill=facepp_group_10)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF confidence value") +
  xlab("Face++ confidence value") +
  #scale_x_discrete(limits=c("3","4","5","6","7","8","9"), breaks=c("3","4","5","6","7","8","9"),
  #labels=c("[0.3,0.4)", "[0.4,0.5)", "[0.5,0.6)", "[0.6,0.7)", "[0.7,0.8)", "[0.8,0.9)", "[0.9,1]")) + 
  scale_x_discrete(limits=c("5","6","7","8","9"), breaks=c("5","6","7","8","9"),
                   labels=c("[0.5,0.6)", "[0.6,0.7)", "[0.7,0.8)", "[0.8,0.9)", "[0.9,1]")) + 
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  ggtitle("Texas") +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_fpp2cf_group10_Texas.png", height=8, width=5)
ggsave("plots/compare_fpp2cf_group10_Texas.pdf", height=8, width=5)



data$cf_race_group_3 <- with(data, reorder(data$cf_race_group_3, data$facepp_race_conf, mean))

ggplot(data, aes(x=factor(cf_race_group_3), y=facepp_race_conf)) + geom_boxplot(aes(fill=cf_race_group_3)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  xlab("CF confidence value") +
  ylab("Face++ confidence value") +
  scale_x_discrete(limits=c("0","1","2"), breaks=c("0","1","2"),
                   labels=c("[0.0,0.4)", "[0.4,0.7)", "[0.7,1]")) + 
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  ggtitle("Texas") +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

ggsave("plots/compare_cf2fpp_group3_Texas.png", height=8, width=5)
ggsave("plots/compare_cf2fpp_group3_Texas.pdf", height=8, width=5)