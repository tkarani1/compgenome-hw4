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

def has_unique_match(id, t1, t2): 
    t2_matches = t1[id]
    if len(t2_matches) > 1: 
        return ''
    t2_match, match_len = (t2_matches[0])[0], (t2_matches[0])[1]

    t1_matches_t2 = t2[t2_match]
    if len(t1_matches_t2) > 1: 
        return ''
    
    t1_match = (t1_matches_t2[0])[0]

    if (id == t1_match): 
        return t2_match, match_len

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

all_ids = set(BMR.keys()) | set(BML.keys())
print(all_ids)

for id in all_ids: 
    if id in BMR: 
        # check if unambiguous match?
        bmr = has_unique_match(id, BMR, BML)
        if (bmr == ''): # no unambiguous match 
            unitigs[id] = [id]
            last_first[id] = id
            continue

        # has unambiguous match

        # Prepend existing unitig
            # bml matches a key of existing unitig
        if (bmr in unitigs): 
            seq = unitigs[bmr]
            del unitigs[bmr]
            seq = [id] + seq    # seq = [id] + [bmr, seq]
            unitigs[id] = seq

            final = (unitigs[id])[-1]
            last_first[final] = id  # final element of unitig stays same, change first element associated w it
            continue
  
        # Append existing unitig
            # id is final element of existing unitig
        if (id in last_first):
            start = last_first[id]
            seq = unitigs[start]
            seq = seq + [bmr]      # seq = [seq, id] + [bmr] 
            unitigs[start] = seq
        
            del last_first[id]
            last_first[bmr] = start
            continue
        
        # Make new unitig
            # no existing unitig match 
        unitigs[id] = [id, bmr]
        last_first[bmr] = id
        continue
    
    else: # id is not in bmr
        

    
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

