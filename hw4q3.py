# IS KEEPING THE WHOLE STRING OKAY (too much data?)
# HOW TO GET RID OF SOME?

def parse_suf_pref_record(fh): 
    records = []
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        first_line = first_line.rstrip()
        tokens = first_line.split(' ')
        records.append((tokens[0], tokens[1], tokens[2]))
    return records

from io import StringIO
import sys
import numpy as np

# get command line inputs
program_name = sys.argv[0]
arguments = sys.argv[1:]
count = len(arguments)
input_fname = arguments[0]
output_fname = arguments[1]

# get text from input file
input_fp = open(input_fname, 'r')
records = parse_suf_pref_record(input_fp)
input_fp.close()

print(records)
unitigs = {}
unitig_output = {}

num_records = len(records) # lol does this actually save computation
for i in range(num_records): 
    left = records[i][0]
    nt = records[i][1]
    right = records[i][2]

    if right in unitigs: 
        # update unitigs
        seq = unitigs[right]
        seq = left + seq
        del unitigs[right]
        unitigs[left] = seq

        # update unitigs_output
        seq = unitig_output[right]
        del unitig_output[right]
        seq = left + '\n' + nt + ' ' + right + '\n' + seq[2:]
        unitig_output[left] = seq

    else: 
        unitigs[left] = left + right
        unitig_output[left] = left + '\n' + nt + ' ' + right + '\n'

# print(unitigs)
# print(unitig_output)

sorted_output = sorted(unitig_output.items())
print(sorted_output)
output_txt = ''
for i, (first, str) in enumerate(sorted_output): 
    output_txt += str
output_txt = output_txt.rstrip()

print(output_txt)

# output to file
output_fp = open(output_fname, 'w')
output_fp.write(output_txt)
output_fp.close()

