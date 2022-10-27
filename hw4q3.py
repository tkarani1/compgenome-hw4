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

def make_BMR_BML(records): 
    BMR = {}
    BML = {}

    for (left, nt, right) in records: 
        if left in BMR: 
            best_id, best_nt = (BMR[left])[0]
            if nt > best_nt: 
                BMR[left] = [(right, nt)]
            elif nt == best_nt: 
                BMR[left] = [(right, nt)] + BMR[left]
        else: 
            BMR[left] = [(right, nt)]

        if right in BML: 
            best_id, best_nt = (BML[right])[0]
            if nt > best_nt: 
                BML[right] = [(left, nt)]
            elif nt == best_nt: 
                BML[right] = [(left, nt)] + BML[right]
            # BML[right] = (left, nt) if nt > (BML[right])[1] else BML[right]
        else: 
            BML[right] = [(left, nt)]
    return BMR, BML

def make_best_pairs(BMR, BML): 
    match_pairs = {}
    for (left, right) in BMR.items(): 
        if (len(right) > 1): 
            continue

        nt = right[0][1]
        right = right[0][0]
        
        if (len(BML[right]) > 1): 
            continue 

        if (BML[right])[0][0] != left:  # not a mutual best match
            continue

        match_pairs[(left, right)] = nt

    return match_pairs

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
pairs = make_best_pairs(BMR, BML)

unitigs = {} # key: first id in the unitig, value: a list of the unitigs
unitig_output = {}
last_first = {} # key: final id in unitig, val: first character in unitig


for ((left, right), nt) in pairs.items(): 
    # RIGHT NOT IN BML?!?!?
    # if (right not in BML):
    #     unitigs[left] = ''
    #     continue

    # Left and Right are mutual best matches

    # DOES THIS SAVE COMPUTATION
    # prepend = 1 if right in unitigs else 0
    # append = 1 if left in last_first else 0

    # Case 1: New Unitig
        # if right is not a key of a unitig, and left is not a final char of a unitig 
        # make a new unitig

    if (right not in unitigs and left not in last_first): 
        unitigs[left] = [left, right]
        last_first[right] = left
        continue

    # Case 2: Prepend
        # if right is the key of a unitig, concatenate strings
    if (right in unitigs): 
        seq = unitigs[right]
        del unitigs[right]
        seq = [left] + seq
        unitigs[left] = seq

        final = (unitigs[left])[-1]
        last_first[final] = left

    # Case 3: Append
        # the rightmost character is the final character in another unitig
    elif (left in last_first):
        start = last_first[left]
        seq = unitigs[start]
        seq = seq + [right]
        unitigs[start] = seq
        
        del last_first[left]
        last_first[right] = start

    # merge two instances in unitigs
    if (left in unitigs and left in last_first): 
        new_right = last_first[left]
        seq = unitigs[new_right]
        del unitigs[new_right]
        del last_first[left]
        seq = seq[:-1] + unitigs[left]
        del unitigs[left]
        unitigs[new_right] = seq
        last_first[seq[-1]] = new_right


# format output summary

sorted_unitigs = sorted(unitigs.items())
output_str = ''
for i, (f, unitig) in enumerate(sorted_unitigs): 
    for i in range(len(unitig) - 1): 
        output_str += unitig[i] + '\n' + str(pairs[(unitig[i], unitig[i+1])]) + ' '
    output_str += unitig[-1]
    output_str += '\n'
output_str = output_str.rstrip()


# output to file
output_fp = open(output_fname, 'w')
output_fp.write(output_str)
output_fp.close()

