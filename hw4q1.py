def edDistRecursiveMemo(x, y, memo=None):
    ''' A version of edDistRecursive with memoization.  For each x, y we see, we
        record result from edDistRecursiveMemo(x, y).  In the future, we retrieve
        recorded result rather than re-run the function. '''
    if memo is None: memo = {}
    if len(x) == 0: return len(y)
    if len(y) == 0: return len(x)
    if (len(x), len(y)) in memo:
        return memo[(len(x), len(y))]
    delt = 1 if (x[-1] != y[-1] and x[-1] != '.' and y[-1] != '.') else 0
    diag = edDistRecursiveMemo(x[:-1], y[:-1], memo) + delt
    vert = edDistRecursiveMemo(x[:-1], y, memo) + 1
    horz = edDistRecursiveMemo(x, y[:-1], memo) + 1
    ans = min(diag, vert, horz)
    memo[(len(x), len(y))] = ans
    return ans

from io import StringIO
import sys
import numpy as np


# get command line inputs
program_name = sys.argv[0]
arguments = sys.argv[1:]
count = len(arguments)

# get text from input file
input_fp = open(arguments[0], 'r')
T = input_fp.readline().rstrip()
P = input_fp.readline().rstrip()
input_fp.close()


# SOMETHING BETTER THAN ITERATING??
min_ed = edDistRecursiveMemo(T, P)
for s in range(len(T) -1): 
    print(T[:-(s+1)])
    ed = edDistRecursiveMemo(T[:-(s+1)], P)
    if ed < min_ed: 
        min_ed = ed
print(edDistRecursiveMemo(T, P))
print(min_ed)

output_fp = open(arguments[1], 'w')
output_fp.write(str(min_ed))