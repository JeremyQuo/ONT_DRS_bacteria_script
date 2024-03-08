import argparse
import matplotlib.pyplot as plt
import pandas as pd
# import pysam
import os
import time
plt.rcParams['pdf.fonttype'] = 42

def intersection(a, b):
    start = max(a[0], b[0])
    end = min(a[1], b[1])
    if start <= end:
        return end - start
    else:
        return 0

def build_out_path(results_path):
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    else:
        print("Output file existed! It will be overwrite or add content after 5 secs ...")
        time.sleep(5)
        print("Continue ...")

def extract_TU_per_read(bam_file_name, bed_file_name,drs_mode):
    gene_bed = pd.read_csv(bed_file_name, sep='\t', header=None)
    bam_file = pysam.AlignmentFile(bam_file_name, 'rb')
    read_dict = {}
    for idx, line in gene_bed.iterrows():
        ref_pos = [line[1], line[2]]
        gene_len = line[2] - line[1]

        for read in bam_file.fetch(line[0], line[1], line[2]):

            if drs_mode:
                if (read.is_reverse and line[5] == '-') or (not read.is_reverse and line[5] == '+'):
                    pass
                else:
                    continue
            read_pos = [read.reference_start, read.reference_end]
            inter_len = intersection(ref_pos, read_pos)
            if inter_len > 100 or inter_len / gene_len > 0.5:

                if read.qname not in read_dict:
                    read_dict[read.qname] = set()
                read_dict[read.qname].add(line[3])

    # build operon_dict
    for key, value in read_dict.items():
        gene_list = list(value)
        gene_list.sort()
        read_dict[key] = '|'.join(gene_list)

    result_df = pd.DataFrame.from_dict(read_dict, orient='index')
    result_df.reset_index(inplace=True)
    result_df.columns = ['read_name', 'TU']
    return result_df

def count_context_per_gene(group_counts):
    context_dict = {}
    def count_context(line):
        gene_list = line["TU"].split('|')
        for item in gene_list:
            if item not in context_dict:
                context_dict[item] = 0
            context_dict[item] = context_dict[item] + 1

    group_counts.apply(count_context, axis=1)
    context_df = pd.DataFrame.from_dict(context_dict, orient='index')
    context_df.reset_index(inplace=True)
    context_df.columns = ['gene', 'context_num']
    return context_df

def plot_context_pie(context_df, out_path):
    context_df['context_num'] = context_df['context_num'].apply(lambda x: '6+' if x >= 6 else x)
    distribution = context_df.groupby('context_num').size().reset_index(name='Count')
    Count = distribution['Count'].values
    context_num = distribution['context_num'].values
    plt.figure(figsize=(4, 4))
    colors = ['#FFEDCB', "#FFD08F", '#b3bc84', '#859a6d', '#647440', "#3E552C"]
    plt.pie(Count, labels=context_num, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # 使饼图为圆形
    plt.title(' Transcript contexts of gene (Gene number :' + str(distribution['Count'].sum()) + ')')
    plt.savefig(out_path + '/context_pie.png')

def main(args):
    gene_bed = args.bed
    bam_file_name = args.bam
    out_path = args.output
    coverage_cutoff = args.cutoff
    drs_mode = args.is_drs
    # build operon_dict
    build_out_path(out_path)
    result_df = extract_TU_per_read(bam_file_name, gene_bed,drs_mode)
    result_df.to_csv(out_path + '/read_TU_list.csv', index=False)

    group_counts = result_df.groupby('TU').size().reset_index(name='coverage')
    group_counts.to_csv(out_path + '/TU_coverage_list.csv', index=False)
    group_counts = group_counts[group_counts['coverage'] > coverage_cutoff]

    context_df = count_context_per_gene(group_counts)
    context_df.to_csv(out_path + '/context_num.csv', index=False)

    plot_context_pie(context_df, out_path)
    print("Finished")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--bam", default='/t1/zhguo/Data/bac_dorado_bsaecall/Ecoli/tot_RNA/genomic.bam',
                        help="bam file")
    parser.add_argument("--bed", default="/t1/zhguo/Data/Ecoli_RNA/ref/gene.bed", help="bed file")
    parser.add_argument("--is_drs", action='store_true', help='Turn on the direct RNA sequencing mode ')
    parser.add_argument("--cutoff", default=10, help="coverage cutoff", type=int)
    parser.add_argument("--output", default='/t1/zhguo/Data/bac_dorado_bsaecall/Ecoli/tot_RNA/TU_result', help='result path')
    args = parser.parse_args()
    main(args)