import dnaio
import pandas as pd
import argparse
import pysam


def analyse_bam(bam_name):
    d = {}
    with pysam.AlignmentFile(bam_name, "rb") as samfile:
        for read in samfile:
            l = int(read.query_length)
            if l in d.keys():
                d[l] += 1
            else:
                d[l] = 1
    return d


def analyse_fq(fq_name):
    d = {}
    with dnaio.open(fq_name) as f:
        for record in f:
            l = len(record.sequence)
            if l in d.keys():
                d[l] += 1
            else:
                d[l] = 1
    return d


def write_dict(d, name, d2={}):
    for_df = {'length': d.keys(), 'n': d.values()}
    df = pd.DataFrame.from_dict(for_df)

    if len(d2.keys()) > 0:  # if there is bam and fastq
        for_df2 = {'length': d2.keys(), 'n_bam': d2.values()}
        df2 = pd.DataFrame.from_dict(for_df2)
        df = pd.merge(df, df2, how="outer", on="length").fillna(0)
        df['fraction_aligned'] = df['n_bam'] / df['n']
    
    df = df.sort_values(by=['length'])
    print("writing to " + name)
    df.to_csv(name, index=False)




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bam", default="None", help="A bam file to analyse")
    parser.add_argument("-f", "--fastq", default="None", help="A fastq to analyse")
    parser.add_argument("-o", "--output", required=True, help="Output filename")
    args = parser.parse_args()

    n_inputs = 2
    if args.bam == "None":
        n_inputs += -1
    if args.fastq == "None":
        n_inputs += -1
    assert n_inputs > 0, "Provide at least one input file!"

    if args.bam != "None":
        print("Reading bam file")
        bam_stats = analyse_bam(args.bam)
        if n_inputs == 1:
            write_dict(bam_stats, args.output)

    if args.fastq != "None":
        print("Reading fastq file")
        fq_stats = analyse_fq(args.fastq)
        if n_inputs == 1:
            write_dict(fq_stats, args.output)

    if n_inputs == 2:
        write_dict(fq_stats, args.output, bam_stats)
    

if __name__ == '__main__':
    main()

# python3 __main__.py -f ~/Desktop/mapping_length_analysis/test_data/ultraplex_demux_fmrp1.fastq.gz -b ~/Desktop/mapping_length_analysis/test_data/fmrp1.Aligned.sortedByCoord.out.bam -o fmrp1