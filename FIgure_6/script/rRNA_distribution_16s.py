import pandas as pd
import numpy as np
import plotnine as p9
import numpy as np
from matplotlib import pyplot as plt
import math
plt.rcParams['pdf.fonttype'] = 42

methylation_list=[1407,
516,
1498,
1402,
967,
966,
1516,
1518,
1519,
527,
1207]
df = pd.read_csv('../data/val_4.bed',sep='\t',header=None)
gene_df = pd.read_csv('../../ref/gene.bed', sep='\t', header=None)
gene_df['length']=gene_df[2]-gene_df[1]
df['Type']=None
df['gene']=None
df['length']=None
df['start']=None
df['strand']=None
for index,line in gene_df.iterrows():
    df.loc[(df[1] >= line[1]) & (df[1] <= line[2]), 'Type'] = line[6]
    df.loc[(df[1] >= line[1]) & (df[1] <= line[2]), "gene"] = line[3]
    df.loc[(df[1] >= line[1]) & (df[1] <= line[2]), "start"] = line[1]
    df.loc[(df[1] >= line[1]) & (df[1] <= line[2]), "length"] = line['length']
    df.loc[(df[1] >= line[1]) & (df[1] <= line[2]), "strand"] = line[5]
df = df[df['Type']=='rRNA']
df = df[df['gene'].isin(['rrsA','rrsB','rrsC','rrsD','rrsE','rrsG','rrsH'])]
grouped = df.groupby('gene')
group_sizes = grouped.size()
print(group_sizes)
df['index'] = df.apply(lambda x: x[1]-x['start'] if x[5]=='+' else (x[1]-x['start']-x['length'])*-1,axis=1)
df['index'] = df['index'].astype(int)

i=0
for item in methylation_list:
    if df[(item>=df['index']-2)&(item<=df['index']+2)].shape[0]>0:
        i=i+1
print(i)

pp = p9.ggplot(df, p9.aes( x='index'))\
    + p9.theme_bw() \
    + p9.labs(x='',y='Count')\
    + p9.geom_histogram(p9.aes(y='stat(count)'),binwidth=10)\
    +p9.xlim(0,1540)\
    + p9.theme(
              figure_size=(6,6),
              axis_text=p9.element_text(size=12,family='Arial'),
              axis_title=p9.element_text(size=12,family='Arial'),
              panel_grid_minor=p9.element_blank(),
              title=p9.element_text(size=12,family='Arial'),
              strip_background=p9.element_rect(alpha=0),
              strip_text=p9.element_text(size=12,family='Arial'),
              legend_position='bottom',
                legend_title=p9.element_blank(),
    )\
    + p9.facet_grid('gene ~ ')

for item in methylation_list:
    pp = pp+p9.geom_vline(xintercept=item,color='red',alpha=0.5,linetype = "dashed")
print(pp)
pp.save("panel_A.pdf",dpi=300)
print(1)