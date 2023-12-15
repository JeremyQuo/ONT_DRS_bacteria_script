setwd("E:/PycharmProjects/local_script/R_scrpits")
library(ggplot2)
data <- read.csv("data/estimate_info/length_Q.csv")
data <- data[sample(nrow(data), size=round(nrow(data)*0.05)),]
data <- data[data$Sample != "S rd+ss RNA", ]
data$Samples <- factor(data$Sample,
                            levels = rev(c("ss&rd_RNA","rd_RNA_2","rd_RNA_1", "tot_RNA")))
plot <- ggplot(data, aes(x = Read_length, y = Q_value,color= Samples)) +
  geom_point(size = 0.000001) +
  geom_density_2d(color='black', size=0.1)+
  scale_color_manual(values = c('#FAF1E4',  '#CEDEBD',  '#CEDEBD', '#9EB384'))+
  facet_grid(Samples ~ . )+
  theme_bw()+
  xlim(0,3500)+
  ylim(0,25)+
  labs(y='Q score',x='Read length (bps)')+
  theme(
    strip.background = element_blank(),
    legend.position = 'none',
    text = element_text(size = 12),
    panel.grid.minor =element_blank(),
  )

ggsave("panel_C.pdf", plot, width = 6, height = 6)