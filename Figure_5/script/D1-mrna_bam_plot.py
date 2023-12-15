import pandas as pd
import plotnine as p9
import numpy as np
from matplotlib import pyplot as plt
import math
plt.rcParams['pdf.fonttype'] = 42


rips = pd.read_csv('../data/mrna_coverage_merip/wt.txt', sep='\t', header=None)
rips['group']='wt'
input = pd.read_csv('../data/mrna_coverage_merip/input.txt', sep='\t', header=None)
input['group']='input'
total_df = pd.concat([rips,input],axis=0)
total_df = total_df[(total_df[1] >= 779067) & (total_df[1] <= 780389)]
total_df[1] = total_df[1] - 779067

total_df.columns=['chro','pos','coverage','group']
pp = p9.ggplot(total_df, p9.aes(x='pos', y='coverage',fill='group'))\
    + p9.theme_bw() \
    + p9.xlim(0, 780389-779067)\
    + p9.ylim(0, 2080)\
    + p9.labs(x='',y='Coverage')\
    + p9.theme(
              figure_size=(8,2.5),
              axis_text=p9.element_text(size=12,family='Arial'),
              axis_title=p9.element_text(size=12,family='Arial'),
              panel_grid_minor=p9.element_blank(),
              title=p9.element_text(size=12,family='Arial'),
              strip_background=p9.element_rect(alpha=0),
              strip_text=p9.element_text(size=12,family='Arial'),
                legend_position='bottom',
                legend_text=p9.element_text(size=10,family='Arial')
    )\
    + p9.geom_col(width=1,alpha=0.7,position='identity')\
    + p9.scale_fill_manual(values={'wt' : '#9EB384',
                                   'input' : '#D7D7D7',
                                   'ivt' : '#FFD08F'})
# + p9.facet_grid('Sample ~ ', scales='free_y') \
print(pp)
pp.save("panel_D1.pdf",dpi=300)
