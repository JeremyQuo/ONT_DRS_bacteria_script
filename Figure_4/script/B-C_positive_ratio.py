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
df = pd.read_csv('../data/Ecoli_comp_combined.csv')
# df = df[df['base']=='A']
# xpore_pos=df[df['xPore_-logPval']>3 ]['1'].drop_duplicates().values
df['test'] = df['0'].astype(str)+df['1'].astype(str)+df['5'].astype(str)
result_dict['Tombo'] = [df[~df['tombo_-logPval'].isna()].shape[0],df[df['tombo_-logPval']>2 ]['test'].drop_duplicates().shape[0]]
result_dict['differr'] = [df[~df['differr_-logFDR'].isna()].shape[0],df[(df['differr_-logFDR']>1.3) & (df['differr_LogOddRatio']>1)]['test'].drop_duplicates().shape[0]]
result_dict['ELIGOS2'] = [df[~df['ELIGOS2_-logPval'].isna()].shape[0],df[(df['ELIGOS2_-logPval']>3) & (df['ELIGOS2_LogOddRatio']>0.26)]['test'].drop_duplicates().shape[0]]
result_dict['DRUMMER'] = [df[~df['DRUMMER_-logPval'].isna()].shape[0],df[(df['DRUMMER_-logPval']>1.3) & (df['DRUMMER_LogOddRatio'].abs()>0.58)]['test'].drop_duplicates().shape[0]]
result_dict['nanocompore'] = [df[~df['nanocompore_-logPval'].isna()].shape[0],df[(df['nanocompore_-logPval']>2) & (df['nanocompore_LogOddRatio'].abs()>0.5)]['1'].drop_duplicates().shape[0]]

df = pd.DataFrame.from_dict(result_dict).transpose()
# df['ratio'] =df[1]/df[0]
df[0] = df[0] - df[1]
df.reset_index(inplace=True)
df.columns=['Methods','Negative number','Positive number']

df = pd.melt(df,id_vars='Methods')

name_list=["differr","DRUMMER","ELIGOS2","nanocompore","Tombo"]
name_list.reverse()
# name_list=["Total RNA","rRNA dep","rRNA dep+SS", 'IVT_neg',"IVT_pos"]
category = pd.api.types.CategoricalDtype(categories=name_list, ordered=True)
df['Methods'] = df['Methods'].astype(category)

name_list=['Negative number','Positive number']
name_list.reverse()
# name_list=["Total RNA","rRNA dep","rRNA dep+SS", 'IVT_neg',"IVT_pos"]
category = pd.api.types.CategoricalDtype(categories=name_list, ordered=True)
df['variable'] = df['variable'].astype(category)

pp = p9.ggplot(df, p9.aes(x='Methods',y='value',fill='variable'))\
 + p9.geom_bar(stat='identity',width=0.5,alpha=1)\
 + p9.theme_bw() \
 + p9.labs(y="", x='')\
 + p9.scale_fill_manual(values=['#FC8B79','#D7D7D7'])\
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

pp.save("Panel_B.pdf",dpi=300)
print(pp)