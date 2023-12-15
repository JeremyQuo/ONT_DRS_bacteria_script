from upsetplot import from_contents
from upsetplot import UpSet
import pandas as pd
from matplotlib import pyplot as plt
from collections import OrderedDict
import plotnine as p9
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['pdf.fonttype'] = 42

# read_num
# (1603546, 1)
# (332250, 1)
# (427934, 1)
name_list=[  "tot_RNA","rd_RNA_1","rd_RNA_2","ss&rd_RNA"]
result_dict=OrderedDict()
cutoff=10
df=pd.read_csv('../data/operon_num_list.txt')
category = pd.api.types.CategoricalDtype(categories=name_list, ordered=True)
df['Sample'] = df['Sample'].astype(category)
df_group=df.groupby("Sample")
for key, value in df_group:
    counts = value[value['coverage_num'] > cutoff]
    print("After  units number filter is ", counts.shape)
    result_dict[key] = counts['operon_name'].values
animals = from_contents(result_dict)
UpSet(animals, subset_size='count',show_counts=True,sort_categories_by='-input').plot()
plt.title("Number of transcriptional units")

plt.savefig('panel_D.pdf')
plt.show()
print(1)