import pysam
import pandas as pd
import numpy as np


def count_fastq(file_path):
    total_reads = 0
    total_bases = 0

    with open(file_path, 'r') as file:
        line_num = 0
        for line in file:
            line_num += 1

            if line_num % 4 == 2:  # 每个read的序列行
                total_reads += 1
                total_bases += len(line.strip())

    return total_reads, total_bases
def count_bam(bam_path):
    bam_file = pysam.AlignmentFile(bam_path, 'rb')
    read_num = 0
    align_num = 0
    read_name_dict = {}
    for read in bam_file.fetch():
        align_num = align_num + read.query_alignment_length
        if read.qname in read_name_dict:
            # print(1)
            read_name_dict[read.qname] = read_name_dict[read.qname] + 1
        else:
            read_name_dict[read.qname] = 1
        read_num = read_num + 1
    return read_num, align_num
input_path="xxxxxxxxxx/"

folder_list = ["tot_RNA","rd_RNA_1","rd_RNA_2","ss_rd_RNA",'IVT_neg','IVT_pos']
# folder_list = ['ss_rd_RNA','IVT']
result_df=[]
for item in folder_list:
    fastq_path = input_path+item+'/'+"final.fastq"
    bam_path=input_path+item+'/'+"final.bam"
    total_read,total_base=count_fastq(fastq_path)
    aligned_read,aligned_base=count_bam(bam_path)
    data_list=[total_read,total_base,aligned_read,aligned_base,total_read-aligned_read,total_base-aligned_base,item]
    print(item,aligned_read/total_read,aligned_base/total_base)
    result_df.append(data_list)

result_df = pd.DataFrame(result_df)
result_df.columns=['total_read','total_base','aligned_read','aligned_num','not_aligned_read','not_aligned_base','group']
result_df.to_csv(input_path+'aligned_num.csv',index=None)
