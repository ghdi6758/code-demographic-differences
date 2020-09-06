setwd("/Users/jisunan/myRepository/code-demographical-differences/crawl-tweets/04_manual_check")

# Load the necessary packages.
library("reshape2")
library("plyr")
library("ggplot2")

data <- read.table("./validation_Age_diff.txt", sep = "\t", header = FALSE)
summary(data)

hist(data$V1)

ggplot(data, aes(V1)) +
  geom_histogram(binwidth=1) +
  xlab("Difference of two results (years)") +
  ylab("Frequency") +
  ggtitle("Bio-matching vs. Face++") +
  theme_bw() + 
  xlim(c(0,60)) +
  theme(axis.title = element_text(size=18), legend.text=element_text(size=14), axis.text  = element_text(size=14), strip.text = element_text(size=14)) 

outfile <- sprintf("./comparison_bio_face.pdf")
ggsave(outfile, width=8,height=4)
