setwd("/Users/jisunan/myRepository/code-demographical-differences/demo-validation/05_crowdflower")
library(ggplot2)



infilename = sprintf("./cf_results/5th_round_CF_contributors_all.txt")
data <- read.table(infilename, sep="\t", header=T, fill=TRUE)
data$worker_id = as.factor(data$worker_id)
summary(data)
nrow(data)


ggplot(data, aes(x=factor(sample_type), y=withindata_judgments_count)) + geom_boxplot(aes(fill=sample_type)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("Judgments count") +
  xlab("Sample type") +
  # ylim(c(5.8,10)) +
  ggtitle(sprintf("Judgments count")) +
  scale_x_discrete(breaks=c("fr_network", "fr_network_linktype"), labels=c("Random", "Selected"))+
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 
  
plotname = sprintf("plots_judgement/judgement_count.png")
ggsave(plotname, height=7, width=5)


ggplot(data, aes(x=factor(sample_type), y=judgments_count)) + geom_boxplot(aes(fill=sample_type)) +
  guides(fill=FALSE) +
  stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
  ylab("Judgments count") +
  xlab("Sample type") +
  # ylim(c(5.8,10)) +
  ggtitle(sprintf("Judgments count (w/ other datasets")) +
  scale_x_discrete(breaks=c("fr_network", "fr_network_linktype"), labels=c("Random", "Selected"))+
  theme_bw() +
  theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
  theme(text = element_text(colour="black", size = 18, face = "bold")) 

plotname = sprintf("plots_judgement/judgement_count_other_data.png")
ggsave(plotname, height=7, width=5)



for (mysampletype in c("fr_network", "fr_network_linktype")) {
  newdata <- data[which(data$sample_type==mysampletype),]
  nrow(newdata)
  
}
newdata <- data[which(data$sample_type=="fr_network"),]

nrow(newdata)
summary(newdata$withindata_judgments_count)
summary(newdata$judgments_count)
summary(newdata$country)
plot(sorted(newdata$country))

selecteddata <- data[which(data$sample_type=="fr_network"),]
newdata <- selecteddata[selecteddata(data$sample_type=="fr_network"),]
## set the levels in order we want
newdata <- within(newdata, country <- factor(country, levels=names(sort(table(country), decreasing=TRUE))))
## plot
ggplot(newdata,aes(x=country))+geom_bar(binwidth=1)


ggplot(newdata, aes(x = reorder(country, -nrow(newdata$country)), y = Count)) +
  geom_bar(stat = "identity")


newdata <- data[which(data$sample_type=="fr_network_linktype"),]
nrow(newdata)
summary(newdata$withindata_judgments_count)
summary(newdata$judgments_count)
summary(newdata$country)
