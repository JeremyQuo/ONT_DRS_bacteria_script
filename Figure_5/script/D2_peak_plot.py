import pandas as pd
import plotnine as p9
import numpy as np
from matplotlib import pyplot as plt
import math
plt.rcParams['pdf.fonttype'] = 42


rips = pd.read_csv('../data/exomepeak2/rips_peaks.bed', sep='\t', header=None)
rips['group']='wt'
input = pd.read_csv('../data/exomepeak2/ivt_peaks.bed', sep='\t', header=None)
input['group']='ivt'
final = pd.read_csv('../data/exomepeak2/final.bed', sep='\t', header=None)
final['group']='final'

df = pd.concat([rips,input,final],axis=0)
new_row = ['NC_000913.3', 779067, 779588, 'm6a_peak_188', 1150, '.', 2.53620, 117.29400, 115.01600, 112,0,0,0, 'pal']
df.loc[len(df)] = new_row
new_row = ['NC_000913.3', 779598, 780389, 'm6a_peak_188', 1150, '.', 2.53620, 117.29400, 115.01600, 112,0,0,0, 'cpoB']
# 将新行添加到DataFrame
df.loc[len(df)] = new_row

new_row = ['NC_000913.3', 779491, 779492, 'm6a_peak_188', 1150, '.', 2.53620, 117.29400, 115.01600, 112,0,0,0, 'ONT']
# 将新行添加到DataFrame
df.loc[len(df)] = new_row

# 打印更新后的DataFrame
print(df)

df = df[(df[1] >= 779060) & (df[1] <= 780389)]
df[1] = df[1] - 779060
df[2] = df[2] - 779060
df[1]=df[1].apply(lambda x:0 if x< 0 else x)
df['start']=df[1]
df['end']=df[2]
index_dict={
    'pal':5,
    'cpoB':4,
    'wt':3,
    'ivt':2,
    'final':1,
    'ONT':0
}
coverage_num_cate_index=list(index_dict.keys())
coverage_num_cate_index.reverse()
index_range=list(range(1,7))
df['ymin'] = df['group'].apply(lambda x:index_dict[str(x)])
df['ymax'] = df['ymin'] + 0.25
df['ymin'] = df['ymin'] - 0.25
plot = p9.ggplot(df, p9.aes(xmin='start', ymin='ymin',ymax='ymax', xmax='end'))\
       + p9.geom_rect(color='black') \
       + p9.theme_bw()\
       + p9.xlim(0,780389-779060)\
       + p9.labs(x='',y='MeRIP-seq sample')\
       + p9.scale_y_continuous(breaks=index_range,labels=coverage_num_cate_index)\
       + p9.theme(
        figure_size=(8,2.5),
        axis_text=p9.element_text(size=12, family='Arial'),
        axis_title=p9.element_text(size=12, family='Arial'),
        panel_grid_minor=p9.element_blank(),
        title=p9.element_text(size=12, family='Arial'),
        strip_background=p9.element_rect(alpha=0),
        strip_text=p9.element_text(size=12, family='Arial'),
        legend_position='bottom',
        legend_text=p9.element_text(size=8, family='Arial'),
        legend_title=p9.element_blank(),
        legend_key_size=10
        )
print(plot)
plot.save("D2_peak.pdf",dpi=300)
