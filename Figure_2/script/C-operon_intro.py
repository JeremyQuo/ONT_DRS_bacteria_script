import pandas as pd
import plotnine as p9
from matplotlib import pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
df = pd.read_csv('../data/operon_introduction.csv')
# coverage_num_cate=['957','545','534','476','236','121','56','20','16','13','8','4']
# df =df[df['coverage']>4]
# coverage_num_cate_text=['933','505','499','419','235','103','53','19','13','11','8','4','4']
# coverage_num_cate = df['coverage'].drop_duplicates().sort_values(ascending=False).astype(str).tolist()

sorted_df = df.sort_values('coverage', ascending=False)


# 对 Column2 列进行去重
deduplicated_df = sorted_df.drop_duplicates(subset='operon')

# 将每个元素转换为字符串，并输出为列表
coverage_num_cate = deduplicated_df['operon'].astype(str).tolist()
coverage_num_cate_index = deduplicated_df['coverage'].astype(str).tolist()
i=len(coverage_num_cate)
index_range=list(range(1,i+1))

index_dict={}

for item in coverage_num_cate:
    index_dict[item] = i
    i=i-1
colors=['#FFFFFF','#B95D3A']
df['ymin'] = df['operon'].apply(lambda x:index_dict[str(x)])
df['ymax'] = df['ymin'] + 0.25
df['ymin'] = df['ymin'] - 0.25
coverage_num_cate_index.reverse()
# background-image: linear-gradient(to right, #051937, #004d7a, #008793, #00bf72, #a8eb12);
plot = p9.ggplot(df, p9.aes(xmin='start', ymin='ymin',ymax='ymax', xmax='end',fill='ratio'))\
       + p9.geom_rect(color='black') \
       + p9.theme_bw()\
       + p9.xlim(189700,193500)\
       + p9.labs(x='',y='Detected transcripts units')\
       + p9.scale_fill_gradientn(colors=colors)\
       + p9.theme(
        figure_size=(8, 4),
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
plot.save("panel_C.pdf",dpi=300)
print(1)