#!/usr/bin/env python

# Merge count tsv file into one table. Modify COMMON_COLUMNS and UNIQUE_COLUMNS for another type of output file.
# author: Jeongbin Park (j.park@dkfz.de)
# input: tsv files generated by 'feqtureCounts_2_FpkmTpm' script
# usage: merge_featurecounts_tables.py TSV [TSV ...]

import sys, os, glob
from collections import OrderedDict

COMMON_COLUMNS = OrderedDict([("gene_id", 3), ("gene_name", 6) ])
UNIQUE_COLUMNS = OrderedDict([("count", 8), ("fpkm", 11), ("tpm", 14), ])

def extract_cell_id_from_filename(fn):
    return '_'.join(os.path.splitext(os.path.basename(fn))[0].split("_")[-5:-2])

def main(argv):
    tsvs = []
    for fn in argv[1:]:
        tsvs += [open(gfn) for gfn in glob.glob(fn)]

    header = '\t'.join(list(COMMON_COLUMNS.keys()) + [extract_cell_id_from_filename(tsv.name) for tsv in tsvs])
    fos = [open("%s_%s_featureCounts.%s.tsv"%(os.environ['SAMPLE'], os.environ['PID'], e), "w") for e in UNIQUE_COLUMNS.keys()]
    for fo in fos:
        fo.write("#" + header + '\n')

    # Discard header line
    for tsv in tsvs:
        tsv.readline()

    while True:
        lines = [tsv.readline().split('\t') for tsv in tsvs]
        if all(line[0] == '' for line in lines):
            break
        elif any(line[0] == '' for line in lines):
            # This should not happen!
            print("Error: number of lines in the input files does not match.")
            exit(1)

        for i, col_idx in enumerate(UNIQUE_COLUMNS.values()):
            entries = [lines[0][common_col_idx] for common_col_idx in COMMON_COLUMNS.values()]
            entries += [line[col_idx] for line in lines]
            fos[i].write('\t'.join(entries) + '\n')

    for fo in fos:
        fo.close()
    for tsv in tsvs:
        tsv.close()

if __name__ == "__main__":
    main(sys.argv)