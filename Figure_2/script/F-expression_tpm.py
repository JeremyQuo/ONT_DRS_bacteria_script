import pandas as pd

gene_bed = "../ref/gene.bed"
gene_bed = pd.read_csv(gene_bed,sep='\t',header=None)
gene_bed['length']=gene_bed.apply(lambda x: x[2] - x[1],axis=1)
gene_bed=gene_bed[[3,'length']]
gene_bed.columns=['gene','length']


result_df=pd.DataFrame()
df = pd.read_csv('../data/count_gene_merged.csv')
df_group = df.groupby('group')
for key, value in df_group:
    print(key)
    # if "IVT" in key:
    #     continue
    temp_df = pd.merge(value,gene_bed,on='gene',how='left')
    temp_df = temp_df[(temp_df['type']=='mRNA')]
    # calculate tpm
    temp_df['count'] = temp_df.apply(lambda x: x['coverage'] / x['length'],axis=1)
    sum_gene_count=temp_df['count'].sum()
    temp_df['normalized'] =temp_df.apply(lambda x: x['count']/sum_gene_count * 1000000, axis=1)
    temp_df=temp_df[['gene','normalized']]
    # temp_df=temp_df[['gene','coverage']]
    temp_df.columns=['gene',key]
    if result_df.shape[0] == 0:
        result_df = temp_df
    else:
        result_df = pd.merge(result_df, temp_df,on='gene',how='outer')
result_df.fillna(0,inplace=True)
# result_df.to_csv('gene_expression.csv',index=None)
# result_df = result_df.drop('NGS',axis=1)
correlation_matrix = result_df.drop('gene',axis=1).corr(method='spearman')
print(correlation_matrix)
result_df = pd.merge(result_df,gene_bed,on='gene',how='left')
result_df.to_csv('gene_expression_tpm.csv',index=None)

# then use hiplot
print(1)