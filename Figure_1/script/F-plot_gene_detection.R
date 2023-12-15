
setwd("E:/PycharmProjects/local_script/R_scrpits")
library(ggplot2)
library(tidyr)
library(ggvenn)
df <- read.csv("data/gene_list.csv")

tot_RNA <- df[df$Sample == "tot_RNA", "gene"]
rd_RNA_1 <- df[df$Sample == "rd_RNA_1", "gene"]
rd_RNA_2 <- df[df$Sample == "rd_RNA_2", "gene"]
ss_RNA <- df[df$Sample == "ss&rd_RNA", "gene"]
x <- list(tot_RNA=tot_RNA,
          rd_RNA_1=rd_RNA_1,
          rd_RNA_2=rd_RNA_2,
          'ss&rd_RNA'=ss_RNA)
plot = ggvenn(x,fill=c('tot_RNA'='#FAF1E4',
                               'rd_RNA_1'='#CEDEBD',
                               'ss&rd_RNA'='#9EB384',
                               'rd_RNA_2'='#CEDEBD',
                               'unmap'="#D7D7D7"))


ggsave("panel_F.pdf", plot, width = 4, height = 4)