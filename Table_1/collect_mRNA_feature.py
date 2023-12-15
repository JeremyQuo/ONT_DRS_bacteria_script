import pysam
import pandas as pd
import numpy as np
def intersection(a, b):
    start = max(a[0], b[0])
    end = min(a[1], b[1])
    if start <= end:
        return end - start
    else:
        return 0
gene_bed = "../ref/gene.bed"
# gene_bed = "/t1/zhguo/Data/Saureus_data/ref/gene.bed"
gene_bed = pd.read_csv(gene_bed,sep='\t',header=None)
gene_bed=gene_bed[(gene_bed[6]=='mRNA')]
gene_bed['length']=gene_bed[2]-gene_bed[1]

input_path="xxxxxxx/"

folder_list = ["tot_RNA","rd_RNA_1","rd_RNA_2","ss_rd_RNA",'IVT_neg','IVT_pos']

result_list=[]
result_df=pd.DataFrame()
for item in folder_list:

    bam_file=input_path + item +'/'+"final.bam"
    bam_file= pysam.AlignmentFile(bam_file,'rb')
    result_dict={}
    gene_dict={}
    read_set =set()
    gene_num=0
    for idx,line in gene_bed.iterrows():

        chrom = line[0]
        start = line[1]
        end = line[2]
        strand = line[5]
        gene_name = line[3]
        gene_interval = [start, end]
        for read in bam_file.fetch(chrom,start,end):
            if (strand == '+' and read.is_reverse) or (strand == '-' and not read.is_reverse):
                continue
            read_set.add('@'+read.qname)

    input_file = input_path + item + "/results/estimated_quality/final_estimated_accuracy.txt"
    tem_df = pd.read_csv(input_file, sep='\t')
    result=list(read_set)
    df = pd.DataFrame(result)
    df['group']=item
    df.columns = ['ID', 'group']
    df = pd.merge(df, tem_df, on='ID', how='left')
    # df.to_csv(input_path+ key +'/'+"mrna_read_length.count",header=None,index=None)
    result_df=pd.concat([result_df,df],axis=0)

result_df.to_csv(input_path+"/mRNA_length.csv",header=None,index=None)
print(result_df.shape)
