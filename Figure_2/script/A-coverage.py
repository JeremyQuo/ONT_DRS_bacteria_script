import pandas as pd
import plotnine as p9
import numpy as np
from matplotlib import pyplot as plt
import math
plt.rcParams['pdf.fonttype'] = 42

def acc2qvalue(acc):
    error=1-acc
    try:
        qvalue = (-10) * math.log10(error)
    except Exception:
        print(1)
    return qvalue
# Sample data ,can be dropped
input_dict={}

total_df = pd.read_csv('../data/coverage.txt', sep='\t', header=None)
total_df = total_df[(total_df[1] >= 189700) & (total_df[1] <= 193500)]

total_df.columns = ['chro', 'pos', 'coverage']
pp = p9.ggplot(total_df, p9.aes(x='pos', y='coverage'))\
    + p9.theme_bw() \
    + p9.labs(y="Normalized Coverage", x='') \
    + p9.xlim(189700, 193500)\
    + p9.theme(
              figure_size=(8, 2.5),
              axis_text=p9.element_text(size=12,family='Arial'),
              axis_title=p9.element_text(size=12,family='Arial'),
              panel_grid_minor=p9.element_blank(),
              title=p9.element_text(size=12,family='Arial'),
              strip_background=p9.element_rect(alpha=0),
              strip_text=p9.element_text(size=12,family='Arial'),
              legend_position='none'
    )\
    + p9.geom_col(width=5,fill='#99AEBB')
# + p9.facet_grid('Sample ~ ', scales='free_y') \
print(pp)
pp.save("panel_A",dpi=300)
