# IS KEEPING THE WHOLE STRING OKAY (too much data?)
# HOW TO GET RID OF SOME?

def parse_suf_pref_record(fh): 
    records = []
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        first_line = first_line.rstrip()
        left, nt, right = first_line.split(' ')
        records.append((left, int(nt), right))
    return records

# COMBINE W PREVIOUS FUNCTION?
def make_BMR_BML(records): 
    BMR = {}
    BML = {}

    # TIES?!?!
    for (left, nt, right) in records: 
        if left in BMR: 
            BMR[left] = (right, nt) if nt > (BMR[left])[1] else BMR[left]
        else: 
            BMR[left] = (right, nt)

        if right in BML: 
            BML[right] = (left, nt) if nt > (BML[right])[1] else BML[right]
        else: 
            BML[right] = (left, nt)
    return BMR, BML

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

BMR, BML = make_BMR_BML(records)

unitigs = {}
unitig_output = {}
last_first = {} # key: final character in unitig, val: first character in unitig

sorted_BMR = sorted(BMR.items())

for (left, (right, nt)) in sorted_BMR: 
    # RIGHT NOT IN BML?!?!?
    # if (right not in BML):
    #     unitigs[left] = ''
    #     continue

    if (BML[right])[0] != left:  # not a mutual best match
        del BMR[left]
        continue

    # Left and Right are mutual best matches

    # Case 1: New Unitig
        # if right is not a key of a unitig, and left is not a final char of a unitig 
        # make a new unitig
    if (right not in unitigs and left not in last_first): 
        unitigs[left] = [left, right]
        unitig_output[left] = left + '\n' + str(nt) + ' ' + right + '\n'
        last_first[right] = left
        continue

    # Case 2: Prepend
        # if right is the key of a unitig, concatenate strings
    if (right in unitigs): 
        seq = unitigs[right]
        del unitigs[right]
        seq = [left] + seq
        unitigs[left] = seq

        # seq_str = unitig_output[right]
        # del unitig_output[right]
        # seq_str = left + '\n' + str(nt) + ' ' + right + '\n' + seq_str[2:] <-- WONT WORK BC ID IS LONGER!
        # unitig_output[left] = seq_str

        final = (unitigs[left])[-1]
        last_first[final] = left

    # Case 3: Append
        # the rightmost character is the final character in another unitig
    if (left in last_first):
        start = last_first[left]
        seq = unitigs[start]
        seq = seq + [right]
        unitigs[start] = seq
        
        del last_first[left]
        last_first[right] = start

print(str(len(unitigs.keys())))
# format output
sorted_output = sorted(unitig_output.items())
output_txt = ''

for i, (first, str) in enumerate(sorted_output): 
    output_txt += str
output_txt = output_txt.rstrip()

# output to file
output_fp = open(output_fname, 'w')
output_fp.write(output_txt)
output_fp.close()

