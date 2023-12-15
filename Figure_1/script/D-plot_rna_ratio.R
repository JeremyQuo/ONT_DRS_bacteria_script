setwd("E:/PycharmProjects/local_script/R_scrpits")
library(ggplot2)
library(tidyr)
library(ggpattern)
data <- read.csv("data/genomic_cov.count")
data$coverage_num <- round(data$coverage_num / 1000000, 2)

data$group <- factor(data$group,
                            levels =  c("ss&rd_RNA","rd_RNA_2","rd_RNA_1", "tot_RNA") )
data$type <- factor(data$type,
                            levels = rev(c('tRNA','ncRNA','mRNA','rRNA','Others',"Unmap")))

plot <- ggplot(data , aes(x = group, y = coverage_num,fill=type)) +
  geom_bar(stat= 'identity',position = 'fill', width = 0.5,color='black') +
  geom_text(aes(label=coverage_num),position=position_fill(0.5),size=3)+
  scale_fill_manual(values =c('tRNA'='#FC8B79',
                               'ncRNA'='#E3BC3D',
                               'mRNA'='#E18256',
                               'rRNA'='#F7D98F',
                               'Others'='#D7D7D7',
                               'Unmap'='white'))+
  theme_bw()+
  labs(x='',y='')+
  theme(
    strip.background = element_blank(),
    legend.position = 'bottom',
        legend.title = element_blank(),
    text = element_text(size = 12),
    panel.grid.minor =element_blank(),
  )+
  coord_flip()

ggsave("panel_D.pdf", plot, width = 6, height = 3)