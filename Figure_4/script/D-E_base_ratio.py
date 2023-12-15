import pandas as pd
import numpy as np
from upsetplot import from_contents
from upsetplot import UpSet

from matplotlib import pyplot as plt
from collections import OrderedDict
import plotnine as p9
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['pdf.fonttype'] = 42

result_dict={}
df = pd.read_csv('../data/Saureus_comp_combined.csv')
df.drop_duplicates(subset='1',inplace=True)
# df = df[df['base']=='A']
# xpore_pos=df[df['xPore_-logPval']>3 ]['1'].drop_duplicates().values
df['test'] = df['0'].astype(str)+df['1'].astype(str)+df['5'].astype(str)
result_dict={}
result_dict['differr']=df[(df['differr_-logFDR']>1.3) & (df['differr_LogOddRatio']>1)]
result_dict['DRUMMER']=df[(df['DRUMMER_-logPval']>1.3) & (df['DRUMMER_LogOddRatio'].abs()>0.58)]
result_dict['ELIGOS2']=df[(df['ELIGOS2_-logPval']>3) & (df['ELIGOS2_LogOddRatio']>0.26)]
result_dict['nanocompore']=df[(df['nanocompore_-logPval']>2) & (df['nanocompore_LogOddRatio'].abs()>0.5)]
result_dict['Tombo']=df[df['tombo_-logPval']>2]

result_df=pd.DataFrame()
for key, value in result_dict.items():
    counts = value["base"].value_counts().to_frame()
    counts.reset_index(inplace=True)
    counts['Methods'] = key
    result_df = pd.concat([result_df,counts],axis=0)

name_list=["differr","DRUMMER","ELIGOS2","nanocompore","Tombo"]
name_list.reverse()
# name_list=["Total RNA","rRNA dep","rRNA dep+SS", 'IVT_neg',"IVT_pos"]
category = pd.api.types.CategoricalDtype(categories=name_list, ordered=True)
result_df['Methods'] = result_df['Methods'].astype(category)

name_list=["A","T","C","G"]
name_list.reverse()

category = pd.api.types.CategoricalDtype(categories=name_list, ordered=True)
result_df['base'] = result_df['base'].astype(category)
pp = p9.ggplot(result_df, p9.aes(x='Methods',y='count',fill='base'))\
 + p9.geom_bar(stat='identity',position='fill',width=0.5,alpha=1)\
 + p9.theme_bw() \
 + p9.labs(y="", x='')\
 + p9.geom_text(p9.aes(label="count"),position=p9.position_fill(0.5),size=8,family='Arial')\
 + p9.scale_fill_manual(values={"A":'#95B989',
                          "T":'#C88776',
                          "G":'#FFF4C2',
                          "C":"#7CB3C5"})\
 + p9.theme(
            figure_size=(4,3.5),
            axis_text=p9.element_text(size=12,family='Arial'),
            axis_title=p9.element_text(size=12,family='Arial'),
            panel_grid_minor=p9.element_blank(),
            title=p9.element_text(size=12,family='Arial'),
            legend_title=p9.element_blank(),
            legend_position='bottom',
            legend_text=p9.element_text(size=10,family='Arial')
                      )\
    +p9.coord_flip()

pp.save("Panel_D.pdf",dpi=300)
print(pp)