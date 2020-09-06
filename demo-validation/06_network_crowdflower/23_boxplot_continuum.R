setwd("/Users/jisunan/myRepository/code-demographical-differences/demo-validation/05_crowdflower")
library(ggplot2)

sampling <- "Random"
myusertype <- "following"
for (sampling in c("Random", "Selected")) {
  infilename = sprintf("continuum_check_%s.txt", sampling)
  data <- read.table(infilename, sep="\t", header=T)
  summary(data)
  nrow(data)
  
  data$linktype  = factor(data$linktype, levels=c("w->w", "b->b", "w->b", "b->w"))
  
  ggplot(data, aes(x=factor(linktype), y=conf_value, fill=conf_type)) + 
    geom_boxplot(aes(fill=conf_type)) +
    #stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
    ylab("Confidence values") +
    xlab("Edge type") +
    ggtitle(sprintf("Conf. value by edge types (%s, All)",sampling)) +
    theme_bw() +
    theme(legend.position="top") + 
    theme(text = element_text(colour="black", size = 16, face = "bold")) +
    scale_fill_manual(values=c("#999999", "#E69F00", "#56B4E9"))
  
  plotname = sprintf("plots_continuum/continuum_%s_all.png", sampling)
  ggsave(plotname, height=8, width=7)
  
  for (myusertype in c("following", "followed")) {
    newdata <- data[which(data$usertype==myusertype),]
    nrow(newdata)
    
    ggplot(newdata, aes(x=factor(linktype), y=conf_value, fill=conf_type)) + 
      geom_boxplot(aes(fill=conf_type)) +
      #stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
      ylab("Confidence values") +
      xlab("Edge type") +
      ggtitle(sprintf("Conf. value by edge type (%s,%s)", sampling, myusertype)) +
      theme_bw() +
      theme(legend.position="top") + 
      theme(text = element_text(colour="black", size = 16, face = "bold")) +
      scale_fill_manual(values=c("#999999", "#E69F00", "#56B4E9"))
    
    plotname = sprintf("plots_continuum/continuum_%s_%s.png", sampling, myusertype)
    ggsave(plotname, height=8, width=7)
  }
}

