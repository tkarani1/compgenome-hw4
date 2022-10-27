def parse_fastq(fh):
    """ Parse reads from a FASTQ filehandle.  For each read, we
        return a name, nucleotide-string, quality-string triple. """
    reads = {}
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()
        reads[name] = seq
    return reads

def write_solution(unitigID, unitigSequence, n, out_fh, per_line=60):
        offset = 0
        out_fh.write(f">{unitigID} {n}\n")
        while offset < len(unitigSequence):
            line = unitigSequence[offset:offset + per_line]
            offset += per_line
            out_fh.write(line + "\n")

from io import StringIO
import sys
import numpy as np

# get command line inputs
program_name = sys.argv[0]
arguments = sys.argv[1:]
count = len(arguments)
fastq_fname = arguments[0]
unitigs_fname = arguments[1]
output_fname = arguments[2]

# get text from input file
fastq_fp = open(fastq_fname, 'r')
reads = parse_fastq(fastq_fp)
fastq_fp.close()

unitigs_fp = open(unitigs_fname, 'r') 
output_fp = open(output_fname, 'w')

id = ''
seq = ''
n = 0
while True:
    first_line = unitigs_fp.readline()
    if len(first_line) == 0:
        break  # end of file
    first_line = first_line.rstrip()
    pieces = first_line.split(' ')
    if (len(pieces) == 1): # first id of a unitig
        if (n > 0): 
            write_solution(id, seq, n, output_fp)
        id = pieces[0]
        seq = reads[id]
        n = 1
        continue
    else:  # part of a unitig
        overlap = int(pieces[0])
        next_id = pieces[1]
        seq = seq + reads[next_id][overlap:]
        n += 1
if (n > 0): 
    write_solution(id, seq, n, output_fp)

unitigs_fp.close()
output_fp.close()







