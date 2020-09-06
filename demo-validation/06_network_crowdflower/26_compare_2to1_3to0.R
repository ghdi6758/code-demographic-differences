setwd("/Users/jisunan/myRepository/code-demographical-differences/demo-validation/06_network_crowdflower")
library(ggplot2)


data <- read.table("./result_all/usonly_CF_aggregated_simple.txt", sep="\t", header=T)

summary(data)

tmp <- data[which(data$cfrace_agreement < 0.9),]
data_2to1 <- tmp[which(tmp$cfrace_agreement > 0.5),]
summary(data_2to1)
nrow(data_2to1)
data_3to0 <- data[which(data$cfrace_agreement >= 0.9),]
summary(data_3to0)
nrow(data_3to0)

ggplot(data_2to1, aes(x=cfrace_selfreported_rating)) + 
  geom_histogram(binwidth=.5) +
  ylab("Count") +
  xlab("CF self-reported rating") +
  ggtitle("CF inter-judge agreement 2 to 1") +
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 
ggsave("plot/hist_cf_self_rating_2to1.png", height=7, width=6)



ggplot(data_3to0, aes(x=cfrace_selfreported_rating)) + 
  geom_histogram(binwidth=.5) +
  ylab("Count") +
  xlab("CF self-reported rating") +
  ggtitle("CF inter-judge agreement 3 to 0") +
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 
ggsave("plot/hist_cf_self_rating_3to0.png", height=7, width=6)

  

  
  
  # Histogram overlaid with kernel density curve
  ggplot(data_2to1, aes(x=cfrace_selfreported_rating)) + 
  geom_histogram(aes(y=..density..),      # Histogram with density instead of count on y-axis
                 binwidth=.5,
                 colour="black", fill="white") +
  geom_density(alpha=.2, fill="#FF6666")  # Overlay with transparent density plot
