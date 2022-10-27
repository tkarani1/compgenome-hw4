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

unitigs = {} # key: first id in the unitig, value: a list of the unitigs
unitig_output = {}
last_first = {} # key: final id in unitig, val: first character in unitig


sorted_BMR = sorted(BMR.items())


for (left, right) in sorted_BMR: 
    # RIGHT NOT IN BML?!?!?
    # if (right not in BML):
    #     unitigs[left] = ''
    #     continue
        

    if (len(right) > 1): 
        del BMR[left]
        continue

    right = right[0][0]
    
    if (len(BML[right]) > 1): 
        del BMR[left]
        continue 

    if (BML[right])[0][0] != left:  # not a mutual best match
        del BMR[left]
        continue

    # if (left == '0130/1'): 
    #     with open("files/unitigs_here1.txt", 'w') as f: 
    #         for key, value in unitigs.items(): 
    #             f.write('%s:%s\n' % (key, value))

    #     with open("files/BMR_here1.txt", 'w') as f: 
    #         for key, value in BMR.items(): 
    #             f.write('%s:%s\n' % (key, value))

    #     with open("files/BML_here1.txt", 'w') as f: 
    #         for key, value in BML.items(): 
    #             f.write('%s:%s\n' % (key, value))

    #     with open("files/LF_here1.txt", 'w') as f: 
    #         for key, value in last_first.items(): 
    #             f.write('%s:%s\n' % (key, value))

    # Left and Right are mutual best matches

    # DOES THIS SAVE COMPUTATION
    # prepend = 1 if right in unitigs else 0
    # append = 1 if left in last_first else 0

    # Case 1: New Unitig
        # if right is not a key of a unitig, and left is not a final char of a unitig 
        # make a new unitig

    if (right not in unitigs and left not in last_first): 
        if (left == '0130/1'): 
            print('1')
        unitigs[left] = [left, right]
        last_first[right] = left
        continue

    if (right in unitigs and left in last_first): 

        # choose to prepend
        seq = unitigs[right]
        del unitigs[right]
        seq = [left] + seq
        unitigs[left] = seq

        final = (unitigs[left])[-1]
        last_first[final] = left

        # prepend the left sequence
        if (left in unitigs): 
            new_right = last_first[left]
            seq = unitigs[new_right]
            del unitigs[new_right]
            del last_first[left]
            seq = seq[:-1] + unitigs[left]
            del unitigs[left]
            unitigs[new_right] = seq
            last_first[seq[-1]] = new_right
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

        # if (left == '0130/1'): 
        #     with open("files/unitigs_here2.txt", 'w') as f: 
        #         for key, value in unitigs.items(): 
        #             f.write('%s:%s\n' % (key, value))

        #     with open("files/BMR_here2.txt", 'w') as f: 
        #         for key, value in BMR.items(): 
        #             f.write('%s:%s\n' % (key, value))

        #     with open("files/BML_here2.txt", 'w') as f: 
        #         for key, value in BML.items(): 
        #             f.write('%s:%s\n' % (key, value))

        #     with open("files/LF_here2.txt", 'w') as f: 
        #         for key, value in last_first.items(): 
        #             f.write('%s:%s\n' % (key, value))

    # Case 3: Append
        # the rightmost character is the final character in another unitig
    if (left in last_first):
        print('hi')
        start = last_first[left]
        seq = unitigs[start]
        seq = seq + [right]
        unitigs[start] = seq
        
        del last_first[left]
        last_first[right] = start
        continue



#print(unitigs)
print(str(len(unitigs.keys())))

with open("files/unitigs_f.txt", 'w') as f: 
    for key, value in unitigs.items(): 
        f.write('%s:%s\n' % (key, value))

with open("files/BMR_f.txt", 'w') as f: 
    for key, value in BMR.items(): 
        f.write('%s:%s\n' % (key, value))

with open("files/BML_f.txt", 'w') as f: 
    for key, value in BML.items(): 
        f.write('%s:%s\n' % (key, value))

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

