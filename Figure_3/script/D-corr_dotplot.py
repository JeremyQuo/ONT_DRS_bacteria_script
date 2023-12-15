import plotnine as p9
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.neighbors import KernelDensity
import numpy as np
#

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']


col_name=['IVT_pos','IVT_neg']
col2_name='ss_rd_RNA'
df = pd.read_csv('../data/E_count_gene_tpm.csv')
result_df=pd.DataFrame()
for item in col_name:
    temp = df[[col2_name,item,'length']]
    temp.columns=['x','y','length']

    temp["group"] = item
    # 计算核密度估计
    result_df = pd.concat([result_df,temp],axis=0)
# add Saureus data
S_df = pd.read_csv('../data/S_count_gene_tpm.csv')
S_df = S_df[['ss&rd_RNA','IVT_neg','length']]
S_df.columns=['x','y','length']
S_df["group"] = 'S_IVT_neg'
result_df = pd.concat([result_df,S_df],axis=0)
result_df = result_df[~(result_df[['x','y']] <= 0).any(axis=1)]
# add kernel info
df_group = result_df.groupby('group')
df=pd.DataFrame()
for key,item in df_group:
    kde = KernelDensity(bandwidth=10).fit(item[["x", "y"]])
    item["Density"] = np.exp(kde.score_samples(item[["x", "y"]]))
    df = pd.concat([df, item], axis=0)

df['Gene length (Kb)'] = df['length'].apply(lambda x: 1 if x < 1000 else 2 if x<2000 else 3 if x<3000 else 4)
df['x']=np.log10(df['x'])
df['y']=np.log10(df['y'])

pp = p9.ggplot(df, p9.aes(x='y',y='x',fill='Density'))\
 + p9.theme_bw() \
 + p9.geom_point(p9.aes(size='Gene length (Kb)'),stroke=0.3) \
 + p9.scale_fill_gradient(low='#ffffff', high='#1856B6')\
 + p9.ylim(-0.1, 5)\
 + p9.xlim(-0.1, 5)\
 + p9.theme(
            figure_size=(10, 5),
            legend_key_width=8,
            legend_position='bottom',
            axis_text=p9.element_text(size=12,family='Arial'),
            axis_title=p9.element_text(size=12,family='Arial'),
            panel_grid_minor=p9.element_blank(),
            title=p9.element_text(size=12,family='Arial'),
            legend_text=p9.element_text(size=8,family='Arial'),
            strip_background=p9.element_rect(alpha=0),
            strip_text=p9.element_text(size=12,family='Arial')
                      )\
 +p9.facet_grid('~ group')
print(pp)
pp.save("Panel_D.pdf",dpi=300)
print(1)