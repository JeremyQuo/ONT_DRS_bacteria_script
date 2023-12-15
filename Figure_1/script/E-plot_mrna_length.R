setwd("E:/PycharmProjects/local_script/R_scrpits")
library(ggplot2)
library(tidyr)
library(ggpattern)
library(see)
data <- read.csv("data/mRNA_length.csv")
# data <- data[data$Sample != "S rd+ss RNA", ]
data <- data[, -c(1)]
data <- data[, -c(2:3)]
data_long <- gather(data, key = "variable", value = "value", -group)
data_long$group <- factor(data_long$group,
                            levels = rev(c("ss&rd_RNA","rd_RNA_2","rd_RNA_1", "tot_RNA")) )
data_long <- data_long[data_long$value <= 2500, ]
plot <- ggplot(data_long, aes(x = group,fill=group,y=value)) +
  geom_violin(width=1) +
  geom_boxplot(width=0.08,outlier.shape = NA)+
  scale_fill_manual(values =(c('tot_RNA'='#FAF1E4',
                               'rd_RNA_1'='#CEDEBD',
                               'ss&rd_RNA'='#9EB384',
                               'rd_RNA_2'='#CEDEBD',
                               'unmap'="#D7D7D7")))+
  theme_bw()+
  labs(x='',y='')+
  facet_wrap(. ~ variable, scales = "free_y",ncol = 2)+
  theme(
    strip.background = element_blank(),
    legend.position = 'none',
    text = element_text(size = 12),
    panel.grid.minor =element_blank(),
    axis.text.x = element_text(angle = 45, hjust = 1,vjust = 1)
  )

ggsave("panel_E.pdf", plot, width =6, height =3.5)