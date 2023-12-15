import pandas as pd
import numpy as np
import plotnine as p9
from collections import  OrderedDict
from matplotlib import pyplot as plt
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['pdf.fonttype'] = 42
operon_df=pd.read_csv("operon_list.txt")

cutoff=10
i=0

def count_context(line):
    if pd.isna(line['content']):
        item_set= set([line['operon_name']])
    else:
        gene_string = line['content'].replace("'", "").replace('"', '')
        gene_string = gene_string.strip("()")
        # 使用逗号分割字符串
        elements = gene_string.split(', ')
        # 创建一个集合
        item_set = set(elements)
    for item in item_set:
        if item not in result_dict:
            result_dict[item] = 0
        result_dict[item] = result_dict[item] + 1

df=pd.read_csv('../data/operon_num_list.txt')
df = df[df['coverage_num']>10]
df=pd.merge(df,operon_df,on='operon_name',how='left')
df_group = df.groupby("Sample")
result_df = pd.DataFrame()
for key,value in df_group:
    result_dict = {}
    value.apply(count_context,axis=1)
    temp_df = pd.DataFrame.from_dict(result_dict, orient='index').reset_index()
    temp_df.columns = ['operon_name', 'Contexts']
    temp_df['Sample'] = key
    result_df = pd.concat([result_df,temp_df],axis=0)



name_list=[  "tot_RNA","rd_RNA_1","rd_RNA_2","ss&rd_RNA"]
category = pd.api.types.CategoricalDtype(categories=name_list, ordered=True)
result_df['Sample'] = result_df['Sample'].astype(category)


result_df.loc[result_df['Contexts'] >= 6, 'Contexts'] = '6+'
result_df['Contexts'] = result_df['Contexts'].astype(str)

num_list = [ '1','2','3','4','5','6+']
color_list=['#FFEDCB',"#FFD08F", '#b3bc84','#859a6d','#647440',"#3E552C"]
name_list.reverse()
# color_list.reverse()
category = pd.api.types.CategoricalDtype(categories=name_list, ordered=True)
result_df['Sample'] = result_df['Sample'].astype(category)

category = pd.api.types.CategoricalDtype(categories=num_list, ordered=True)
result_df['Contexts'] = result_df['Contexts'].astype(category)

plot = p9.ggplot(result_df, p9.aes(x='Sample', fill='Contexts')) \
       + p9.labs(x='',y='Distribution of transcriptional contexts')\
       + p9.scale_fill_manual(values=color_list) \
       + p9.theme_bw() \
       + p9.geom_bar(stat='count',position='fill',width=0.5,alpha=0.9,color='black') \
       + p9.theme(
    figure_size=(5, 5),
    panel_grid_minor=p9.element_blank(),
    axis_text=p9.element_text(size=12,family='Arial'),
    axis_title=p9.element_text(size=12,family='Arial'),
    title=p9.element_text(size=12,family='Arial'),
    strip_text=p9.element_text(size=12,family='Arial'),
    strip_background=p9.element_rect(alpha=0),
    legend_position='top',
    legend_title=p9.element_text(size=12,family='Arial'),
    legend_text=p9.element_text(size=10,family='Arial'),
    legend_box='vertical',

    )\
    + p9.coord_flip()

print(plot)
plot.save('panel_E.pdf',dpi=300)