import pandas as pd
import plotnine as p9
from matplotlib import pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
df = pd.read_csv('../data/start_end.csv')
df=df.melt(id_vars='Sample', value_vars=['start','end'])
df = df[df['Sample']=='E rd+ss RNA']
plot = p9.ggplot(df, p9.aes(x='value',fill='variable',width=3))\
        + p9.geom_histogram(binwidth=1)\
        + p9.theme_bw() \
        + p9.xlim(189700,193500)\
        + p9.labs(y="Reads num", x='') \
        + p9.scale_fill_manual(values={'start':'#B95D3A',
                                       'end':'#BABE89'})\
        + p9.theme(
                  figure_size=(8,2.5),
                  axis_text=p9.element_text(size=12,family='Arial'),
                  axis_title=p9.element_text(size=12,family='Arial'),
                  panel_grid_minor=p9.element_blank(),
                  title=p9.element_text(size=12,family='Arial'),
                  strip_background=p9.element_rect(alpha=0),
                  strip_text=p9.element_text(size=12,family='Arial'),
                  legend_position='none',
                  legend_text=p9.element_text(size=10,family='Arial'),
                    legend_title=p9.element_text(size=12,family='Arial')
        )\
        # + p9.facet_grid('Sample ~ ',scales='free_y')
print(plot)
plot.save("panel_B.pdf",dpi=300)