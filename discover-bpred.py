#!/usr/bin/env python
import branchpredictor
import math

# You might want to store the BHR size here to help figure out
# subsequent predictor parameters. (Optional!)
BHR_SIZE = None

# Constants that bound the parameter space.
MAX_BHR_SIZE = 12
MAX_SC_BITS = 4 # Saturating Counter
MAX_PC_BITS = 10 # how many bits of the Program Counter (Branch Address) are used for indexing.

# ex. (m, n) predictor
# m is the number of last branches to look at
# n is the number bits the predictor uses for each branch
# 2^m * n * Number of predictions entries selected by the branch address


def find_branch_history_register_size(bpred):
    # register -> the sequence of past outcomes
    # BHR is usually a shift register

    global BHR_SIZE # (You need "global" in Python to be able to write to
                    # variables outside of function scope.)

    BHR_SIZE = None # (See above.)

    for i in range(12):
        bpred.actual(0, True)
        if bpred.predict(0) == True:
            BHR_SIZE = i
            return i

    return None

def find_saturating_counter_bits(bpred):
    # TODO: your code here

    for i in range(19):
        bpred.actual(0, False)

    sat_count = 0
    while bpred.predict(0) == False:
        bpred.actual(0, True)
        for i in range(BHR_SIZE):
            bpred.actual(1, False)
        sat_count+=1

    sat_count = math.log(sat_count * 2, 2)

    return sat_count

def find_pc_bits_used(bpred):
    # TODO: your code here
    # bpred.actual(8, True)
    # for i in range(BHR_SIZE):
    #     bpred.actual(1, False)
    # print bpred.predict(0)

    index = 2
    while True:
        bpred.actual(index, True)
        for i in range(BHR_SIZE):
            bpred.actual(1, False)

        if bpred.predict(0) == True:
            return math.log(index, 2)
        bpred.reset()
        index *= 2

    return None

def find_branch_history_table_entries(bpred):
    # table -> predictions (aka likelihood of the next outcome)
    # BHT is a larger structure (memory array) that holds the prediction bits (database of behaviors)
    # each entry is a saturating counter

    # TODO: your code here

    pc_bits = find_pc_bits_used(bpred)

    return 2 ** (pc_bits + BHR_SIZE)

def discover(bpred):
    # This function collects your results and returns them in a
    # dictionary. You can add/remove reset() calls or reorder the
    # calls to your functions if you wish, but please keep the
    # structure of the returned dictionary the same for our grading
    # scripts.
    results = {}
    bpred.reset()
    results['bhr size'] = find_branch_history_register_size(bpred)
    bpred.reset()
    results['saturating counter bits'] = find_saturating_counter_bits(bpred)
    bpred.reset()
    results['bht entries'] = find_branch_history_table_entries(bpred)
    return results

if __name__ == '__main__':
    # When run as a script, we'll analyze each of the provided branch
    # predictors.
    for name, bpred in branchpredictor.mystery_predictors:
        results = discover(bpred)
        print '%s:' % name
        for k, v in results.items():
            print '  %s: %s' % (k, v)
        print
