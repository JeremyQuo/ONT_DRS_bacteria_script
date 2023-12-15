import pandas as pd
import plotnine as p9
import numpy as np
from matplotlib import pyplot as plt
import math
plt.rcParams['pdf.fonttype'] = 42

df = pd.read_csv('peak_count.count')

peak_df = pd.read_csv('../data/peak_exomepeak_with_map.bed',sep='\t',header=None)
gene_df = pd.read_csv('../../ref/gene.bed',sep='\t',header=None)

peak_df['Type']=None
for index,line in gene_df.iterrows():
    peak_df.loc[(peak_df[1] >= line[1]) & (peak_df[2] <= line[2]), 'Type'] = line[6]

peak_df = peak_df[[3,13,'Type']]
peak_df.columns=['peak_name','In_ONT','Type']
df = pd.merge(df,peak_df,on='peak_name')
df = df[(df['Type']=='mRNA')|(df['Type']=='rRNA')]
df['class'] = df.apply(lambda x:x['Type']+'('+ ('in_ONT' if x['In_ONT'] else 'out_ONT')+')',axis=1)
# pp = p9.ggplot(df, p9.aes( x='count',fill='class'))\
#     + p9.theme_bw() \
#     + p9.xlim(0,1000)\
#     + p9.geom_density(alpha=0.7)\
#     + p9.theme(
#               figure_size=(6,4),
#               axis_text=p9.element_text(size=12,family='Arial'),
#               axis_title=p9.element_text(size=12,family='Arial'),
#               panel_grid_minor=p9.element_blank(),
#               title=p9.element_text(size=12,family='Arial'),
#               strip_background=p9.element_rect(alpha=0),
#               strip_text=p9.element_text(size=12,family='Arial'),
#               legend_position='bottom',
#                 legend_title=p9.element_blank(),
#     )\
#     + p9.facet_grid('group ~ ', scales='free')
name_list = ['rRNA(in_ONT)','mRNA(in_ONT)','mRNA(out_ONT)']
name_list.reverse()
color_list=['#9DF8FF','#20B2AA']
category = pd.api.types.CategoricalDtype(categories=name_list, ordered=True)
df['class'] = df['class'].astype(category)
pp = p9.ggplot(df, p9.aes( y='count',x='class',fill='In_ONT'))\
    + p9.theme_bw() \
    + p9.scale_fill_manual(values=color_list)\
    + p9.scale_y_log10()\
    + p9.geom_boxplot()\
    + p9.theme(
              figure_size=(6,3),
              axis_text=p9.element_text(size=12,family='Arial'),
              axis_title=p9.element_text(size=12,family='Arial'),
              panel_grid_minor=p9.element_blank(),
              title=p9.element_text(size=12,family='Arial'),
              strip_background=p9.element_rect(alpha=0),
              strip_text=p9.element_text(size=12,family='Arial'),
              legend_position='none',
                legend_title=p9.element_blank(),
    )\
    + p9.facet_grid('group ~ ', scales='free')\
    + p9.labs(x='',y='Coverage')\
    + p9.coord_flip()
pp.save("panel_F.pdf",dpi=300)

print(pp)