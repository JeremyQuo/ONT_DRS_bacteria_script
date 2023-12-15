setwd("E:/PycharmProjects/local_script/R_scrpits")
library(ggplot2)
library(tidyr)
library(ggpattern)
data <- read.csv("data/aligned_num.csv")
data <- data[, -c(1:2)]
data$aligned_read <- round(data$aligned_read / 1000,2)
data$not_aligned_read <- round(data$not_aligned_read / 1000,2)
data$aligned_base <- round(data$aligned_base / 1000000, 2)
data$not_aligned_base <- round(data$not_aligned_base / 1000000, 2)

# data <- data[data$group != "S rd+ss RNA", ]
data_long <- gather(data, key = "variable", value = "value", -group)
data_long$type <- ifelse(substr(data_long$variable, 1, 3) == "not", "unmap", data_long$group)
data_long$group <- factor(data_long$group,
                            levels = c( "ss&rd_RNA","rd_RNA_2","rd_RNA_1", "tot_RNA" ))
data_long$type <- factor(data_long$type,
                            levels = c('unmap' , "ss&rd_RNA","rd_RNA_1","rd_RNA_2", "tot_RNA" ))
data_long$variable <- ifelse(substr(data_long$variable,nchar(data_long$variable)-3, nchar(data_long$variable)) == "base", "Base number (Mb)", 'Read number (K)')
data_long$variable <- factor(data_long$variable,
                            levels = rev(c("Base number (Mb)", 'Read number (K)')))
plot <- ggplot(data_long, aes(x = group, y = value,fill=type)) +
  geom_bar(stat= 'identity', width = 0.5,color='black') +
  scale_fill_manual(values =(c('tot_RNA'='#FAF1E4',
                               'rd_RNA_1'='#CEDEBD',
                               'rd_RNA_2'='#CEDEBD',
                               'ss&rd_RNA'='#9EB384',
                               'S rd+ss RNA'='#A1E086',
                               'unmap'="#D7D7D7")))+
  facet_grid(. ~ variable, scales = "free_x")+
  theme_bw()+
  coord_flip()+
  labs(x='',y='')+
  theme(
    strip.background = element_blank(),
    legend.position = 'none',
    text = element_text(size = 12),
    panel.grid.minor =element_blank(),
  )

ggsave("panel_B.pdf", plot, width = 6, height = 3)