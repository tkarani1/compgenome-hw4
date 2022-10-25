
# def parse_fastq(fh):
#     """ Parse reads from a FASTQ filehandle.  For each read, we
#         return a name, nucleotide-string, quality-string triple. """
#     reads = []
#     while True:
#         first_line = fh.readline()
#         if len(first_line) == 0:
#             break  # end of file
#         name = first_line[1:].rstrip()
#         seq = fh.readline().rstrip()
#         fh.readline()  # ignore line starting with +
#         qual = fh.readline().rstrip()
#         reads.append((name, seq, qual))
#     return reads

def parse_fastq(fh):
    """ Parse reads from a FASTQ filehandle.  For each read, we
        return a name, nucleotide-string, quality-string triple. """
    reads = {}
    names = []
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()
        reads[name] = seq
        names.append(name)
    return reads, names

# only get k-mers from prefix and suffix?
def make_kmer_table(seqs, k):
    """ Given read dictionary and integer k, return a dictionary that
        maps each k-mer to the set of names of reads containing the k-mer. """
    table = {}
    for name, seq in seqs.items():
        for i in range(0, len(seq) - k + 1):
            kmer = seq[i:i+k]
            if kmer not in table:
                table[kmer] = set()
            table[kmer].add(name)
    return table

def make_kmer_table1(seqs, k):
    """ Given read dictionary and integer k, return a dictionary that
        maps each k-mer to the set of names of reads containing the k-mer. """
    table = {}
    for name, seq in seqs.items():
        for i in range(0, len(seq) - k + 1):
            kmer = seq[i:i+k]
            if kmer not in table:
                table[kmer] = set()
            table[kmer].add(name)

    return table

def make_prefix_kmer_table(seqs, k):
    """ Given read dictionary and integer k, return a dictionary that
        maps each k-mer to the set of names of reads containing the k-mer. """
    table = {}
    for name, seq in seqs.items():
       kmer_first = seq[0:0+k]
       
       if kmer_first not in table:
            table[kmer_first] = set()
       table[kmer_first].add(name) 

    return table


def suffix_prefix_match(str1, str2, min_overlap):
    if len(str2) < min_overlap:
        return 0
    str2_prefix = str2[:min_overlap]
    str1_pos = -1
    while True:
        str1_pos = str1.find(str2_prefix, str1_pos + 1)
        if str1_pos == -1:
            return 0
        str1_suffix = str1[str1_pos:]
        if str2.startswith(str1_suffix):
            return len(str1_suffix)


from io import StringIO
import sys
import numpy as np
import json


# get command line inputs
program_name = sys.argv[0]
arguments = sys.argv[1:]
count = len(arguments)
input_fname = arguments[0]
K = int(arguments[1])
output_fname = arguments[2]

# get text from input file
input_fp = open(input_fname, 'r')
reads, names = parse_fastq(input_fp)
input_fp.close()

prefixes = make_prefix_kmer_table(reads, K)
kmer_table = make_kmer_table(reads, K)
read_len = -1
output_txt = ''
for i, name in enumerate(names): 
    if i == 0: 
        read_len = len(reads[name])
    suffix = (reads[name])[read_len - K: read_len]

    if suffix not in kmer_table: # no match exists
        continue

    matches = kmer_table[suffix]
    max_match_len = 0
    max_match_name = ''
    tie_val = 0
    
    for match in matches:
        if match == name: # do not compare to same read
            continue
        this_match_len = suffix_prefix_match(reads[name], reads[match], K)
        if (this_match_len == max_match_len): # tie exists
            tie_val = this_match_len
        if (this_match_len >  max_match_len and this_match_len > tie_val): # does not tie
            max_match_len = this_match_len
            max_match_name = match
            tie_val = 0

    if (max_match_len > 0 and tie_val == 0): # unique match exists
        output_txt += name + ' ' + str(max_match_len) + ' ' + max_match_name + '\n'

output_fp = open(output_fname, 'w')
output_fp.write(output_txt)
output_fp.close()