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


df = pd.read_csv('../data/Ecoli_comp_combined.csv')
# df = df[df['base']=='A']
df['val_num']= 0

df.drop_duplicates(subset='1',inplace=True)
df.loc[df['tombo_-logPval']>2 , 'val_num'] += 1
df.loc[(df['differr_-logFDR']>1.3) & (df['differr_LogOddRatio']>1) , 'val_num'] += 1
df.loc[(df['ELIGOS2_-logPval']>3) & (df['ELIGOS2_LogOddRatio']>0.26) , 'val_num'] += 1
df.loc[(df['DRUMMER_-logPval']>1.3) & (df['DRUMMER_LogOddRatio'].abs()>0.58), 'val_num'] += 1
df.loc[(df['nanocompore_-logPval']>2) & (df['nanocompore_LogOddRatio'].abs()>0.5), 'val_num'] += 1
df = df[df['val_num']>0]

grouped = df.groupby('val_num')

# 统计每个组的元素数量
group_sizes = grouped.size()
for key,item in grouped:
    print(key,'\t',item.shape[0])
# 打印结果
print("每个组的元素数量：")
print(group_sizes)

# then use hiplot
