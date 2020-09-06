setwd("/Users/jisunan/myRepository/code-demographical-differences/demo-validation/05_crowdflower")
library(ggplot2)
get_median <- function(x) quantile(x, 0.5)

infilename <- sprintf("2nd_compare_conf.txt")
original_data <- read.table(infilename, sep="\t", header=T)
summary(original_data)
cor.test(original_data$facepp_race_conf, original_data$cf_race_conf, method="pearson")
cor.test(original_data$facepp_race_conf, original_data$cf_race_conf, method="spearman")
nrow(original_data)
summary(original_data)

for (myrace in c("white", "black", "asian", "hispanic")) {  
  data <- original_data[which(original_data$cf_race==myrace),]
  #summary(data)
  p_result <- cor.test(data$facepp_race_conf, data$cf_race_conf, method="pearson")
  myprint <- sprintf("   %s:, r = %.5f, N = %d, p = %.5f", myrace, p_result$estimate, nrow(data), p_result$p.value)
  print(myprint)
  s_result <- cor.test(data$facepp_race_conf, data$cf_race_conf, method="spearman") 
  myprint <- sprintf("   %s:, rho = %.5f, N = %d, p = %.5f", myrace, s_result$estimate, nrow(data), s_result$p.value)
  print(myprint)
}


for (city in c("NY", "Texas")) {
  print(city)
  for (myrace in c("white", "black", "asian", "hispanic")) {
    infilename <- sprintf("compare_conf_%s.txt", city)
    #print(myrace)
    original_data <- read.table(infilename, sep="\t", header=T)
    data <- original_data[which(original_data$cf_race==myrace),]
    #summary(data)
    p_result <- cor.test(data$facepp_race_conf, data$cf_race_conf, method="pearson")
    myprint <- sprintf("   %s:, r = %.5f, N = %d, p = %.5f", myrace, p_result$estimate, nrow(data), p_result$p.value)
    print(myprint)
    s_result <- cor.test(data$facepp_race_conf, data$cf_race_conf, method="spearman") 
    myprint <- sprintf("   %s:, rho = %.5f, N = %d, p = %.5f", myrace, s_result$estimate, nrow(data), s_result$p.value)
    print(myprint)
  }
}
    
city <- "NY"
myrace <- "black"
for (city in c("NY", "Texas")) {
  print(city)
  for (myrace in c("white", "black", "asian", "hispanic")) {
    infilename <- sprintf("2nd_compare_conf_%s.txt", city)
    print(infilename)
    print(myrace)
    original_data <- read.table(infilename, sep="\t", header=T)
    
    data <- original_data[which(original_data$cf_race==myrace),]
    data$cf_race_group_2 <- as.factor(data$cf_race_group_2)
    data$facepp_group_3 <- as.factor(data$facepp_group_3)
    data$facepp_group_5 <- as.factor(data$facepp_group_5)
    data$facepp_group_10 <- as.factor(data$facepp_group_10)
    summary(data)
    
    data$facepp_group_91 <- with(data, reorder(data$facepp_group_91, data$cf_race_conf, mean))
    ggplot(data, aes(x=factor(facepp_group_91), y=cf_race_conf)) + geom_boxplot(aes(fill=facepp_group_91)) +
      guides(fill=FALSE) +
      stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
      ylab("CF confidence value") +
      xlab("Face++ confidence value") +
      #scale_x_discrete(labels=c("1" = "[0.33,0.66)", "2" = "[0.66,1.00)")) + 
      ggtitle(sprintf("%s, %s",city, myrace)) +
      # ylim(c(0,20000))+  
      # coord_flip() + 
      theme_bw() +
      theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
      theme(text = element_text(colour="black", size = 18, face = "bold")) 
    
    ggsave(sprintf("plots_new/byrace_compare_fpp2cf_group82_%s_%s.png", city, myrace), height=8, width=5)
    ggsave(sprintf("plots_new/byrace_compare_fpp2cf_group82_%s_%s.pdf", city, myrace), height=8, width=5)
    
    data$cf_race_group_2 <- with(data, reorder(data$cf_race_group_2, data$facepp_race_conf, mean))
    
    ggplot(data, aes(x=factor(cf_race_group_2), y=facepp_race_conf)) + geom_boxplot(aes(fill=cf_race_group_2)) +
      guides(fill=FALSE) +
      stat_summary(fun.y=mean, geom="point", shape=5, size=4) +  
      xlab("CF confidence value") +
      ylab("Face++ confidence value") +
      scale_x_discrete(limits=c("0","1","2"), breaks=c("0","1","2"),
                       labels=c("[0.0,0.4)", "[0.4,0.7)", "[0.7,1]")) + 
      # ylim(c(0,20000))+  
      # coord_flip() + 
      theme_bw() +
      ggtitle(sprintf("%s, %s",city, myrace)) +
      theme(legend.position="none", axis.text.x=element_text(angle=0, hjust=0)) +
      theme(text = element_text(colour="black", size = 18, face = "bold")) 
    
    ggsave(sprintf("plots_new/byrace_compare_cf2fpp_group3_%s_%s.png",city,myrace), height=8, width=5)
    ggsave(sprintf("plots_new/byrace_compare_cf2fpp_group3_%s_%s.pdf",city,myrace), height=8, width=5)
  }
}




