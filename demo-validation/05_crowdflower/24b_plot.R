setwd("/Users/jisunan/myRepository/code-demographical-differences/demo-validation/05_crowdflower")
library(ggplot2)


data <- read.table("inter_agreement_check_all.txt", sep="\t", header=T)
data_selected <- data[which(data$linktype=="Selected edges"),]
data_random <- data[which(data$linktype=="Random edges"),]

summary(data)
nrow(data_selected)
nrow(data_random)

sprintf("F++ confidence value & CF inter-judge agreement")
r <- cor.test(data_random$fpp_conf, data_random$cfrace_first_choice_conf, method="pearson")
sprintf("Random edges, %f (p=%f)", r$estimat, r$p.value)
r <- cor.test(data_selected$fpp_conf, data_selected$cfrace_first_choice_conf, method="pearson")
sprintf("Selected edges, %f (p=%f)", r$estimat, r$p.value)

sprintf("F++ confidence value & CF self-reported confidence value")
r <- cor.test(data_random$fpp_conf, data_random$cfrace_first_rating, method="pearson")
sprintf("Random edges, %f (p=%f)", r$estimat, r$p.value)
r <- cor.test(data_selected$fpp_conf, data_selected$cfrace_first_rating, method="pearson")
sprintf("Selected edges, %f (p=%f)", r$estimat, r$p.value)

sprintf("CF inter-judge agreement & CF self-reported confidence value")
r <- cor.test(data_random$cfrace_first_choice_conf, data_random$cfrace_first_rating, method="pearson")
sprintf("Random edges, %f (p=%f)", r$estimat, r$p.value)
r <- cor.test(data_selected$cfrace_first_choice_conf, data_selected$cfrace_first_rating, method="pearson")
sprintf("Selected edges, %f (p=%f)", r$estimat, r$p.value)



data_selected_white <- data_selected[which(data_selected$cfrace_first_choice=="White"),]
data_selected_black <- data_selected[which(data_selected$cfrace_first_choice=="Black"),]

data_random_white <- data_random[which(data_random$cfrace_first_choice=="White"),]
data_random_black <- data_random[which(data_random$cfrace_first_choice=="Black"),]

sprintf("F++ confidence value & CF inter-judge agreement")
r <- cor.test(data_random_white$fpp_conf, data_random_white$cfrace_first_choice_conf, method="pearson")
sprintf("Random, White, %f (p=%f)", r$estimat, r$p.value)
r <- cor.test(data_random_black$fpp_conf, data_random_black$cfrace_first_choice_conf, method="pearson")
sprintf("Random, Black, %f (p=%f)", r$estimat, r$p.value)

r <- cor.test(data_selected_white$fpp_conf, data_selected_white$cfrace_first_choice_conf, method="pearson")
sprintf("Selected, White, %f (p=%f)", r$estimat, r$p.value)
r <- cor.test(data_selected_black$fpp_conf, data_selected_black$cfrace_first_choice_conf, method="pearson")
sprintf("Selected, Black, %f (p=%f)", r$estimat, r$p.value)




get_median <- function(x) quantile(x, 0.5)

p <- ggplot(data, aes(x=factor(cfrace_first_choice), y=cfrace_first_choice_conf)) + geom_boxplot(aes(fill=cfrace_first_choice)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF inter-judge agreement") +
  xlab("") +
  #scale_x_discrete(labels=c("1" = "[0.33,0.66)", "2" = "[0.66,1.00)")) + 
  ggtitle("NY+Texas") +
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

p + facet_grid(. ~ linktype)

ggsave("plots_confidence/cfrace_inter_agreement_rate.png", height=7, width=5)



p <- ggplot(data, aes(x=factor(cfrace_first_choice), y=cfrace_first_rating)) + geom_boxplot(aes(fill=cfrace_first_choice)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF self-reported condidence level") +
  xlab("") +
  #scale_x_discrete(labels=c("1" = "[0.33,0.66)", "2" = "[0.66,1.00)")) + 
  ggtitle("NY+Texas") +
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

p + facet_grid(. ~ linktype)

ggsave("plots_confidence/cfrace_self_reported_confidence.png", height=7, width=5)






p <- ggplot(data, aes(fpp_conf, cfrace_first_choice_conf)) + 
  geom_point() +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("CF inter-judge agreement") +
  xlab("Face++ Confidence Score") +
  #scale_x_discrete(labels=c("1" = "[0.33,0.66)", "2" = "[0.66,1.00)")) + 
  ggtitle("NY+Texas") +
  # ylim(c(0,20000))+  
  # coord_flip() + 
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

p + facet_grid(cfrace_first_choice ~ linktype)

ggsave("plots_confidence/cfrace_agreement_vs_fpp_conf.png", height=7, width=7)


