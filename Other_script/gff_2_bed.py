import pandas as pd
from temp_utils import read_gff_file,reverse_fasta,read_fasta_to_dic

def find_gene_name(line):
    result_dict={}
    transcript_list=line.split(';')
    for item in transcript_list:
        item=item.split("=")
        result_dict[item[0]]=item[1]
    if 'gene' not in result_dict:
        result_dict['gene']=result_dict['Name']
    #     result_dict['gene']=result_dict['gene_synonym']
    if result_dict['gene_biotype'] == "protein_coding":
        result_dict['gene_biotype'] ="mRNA"
    return pd.Series([result_dict['gene'], result_dict['gene_biotype']])

gff_file_path = "/t1/zhguo/Data/Ecoli_RNA/ref/genomic.gff"
gff_df=read_gff_file(gff_file_path)
gff_df=gff_df[gff_df[2]=='gene']

gff_df[[9,10]]=gff_df[8].apply(find_gene_name)
gff_df[3]=gff_df[3]-1
result_df=gff_df[[0,3,4,9,7,6,10]]
result_df[3]=result_df[3].astype(int)
result_df[4]=result_df[4].astype(int)
duplicates = result_df[9].duplicated()
result_df[9] += result_df.groupby(9).cumcount().astype(str).replace('0', '')
result_df.to_csv("/t1/zhguo/Data/Ecoli_RNA/ref/gene.bed",header=None,sep='\t',index=None)