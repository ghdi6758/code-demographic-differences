setwd("/Users/jisunan/myRepository/code-demographical-differences/demo-validation/05_crowdflower")
library(ggplot2)
library("gridExtra")
library("cowplot")

data <- read.table("r_overtime.txt", sep="\t", header=T)
summary(data)
nrow(data)

newdata <- data[which(data$cnt_prev_seen<8),]

ggplot(newdata, aes(x=factor(cnt_prev_seen), y=str_prob, group=dataset, colour=dataset)) + 
  geom_point() + geom_line() + 
  ylim(c(0.5,1)) +
  ylab("Probability") +
  xlab("Number of times seen that *race* before (K)") +
  ggtitle("Probability that a user may tag a peron in the image as *race* \n given he has seen that *race* K times previously") +
  facet_grid(. ~ target_race) + 
  background_grid(major = 'y', minor = "none") + # add thin horizontal lines 
  panel_border() + # and a border around each panel
  theme_bw() +
  theme(legend.position="top") + 
  theme(text = element_text(colour="black", size = 16, face = "bold")) +
  scale_fill_manual(values=c("#999999", "#E69F00", "#56B4E9"))


plotname = sprintf("plots_overtime/learning.png")
ggsave(plotname, height=5, width=12)

