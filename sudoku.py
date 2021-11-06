from optilog.formulas.modelling import *
from optilog.formulas import CNF
from optilog.sat import Glucose41
from sudoku_base import read_sudoku, var, visualize
import sys


def at_most_one(lits):
    clauses = []
    for i in range(len(lits) - 1):
        for j in range(i + 1, len(lits)):
            v1 = lits[i]
            v2 = lits[j]
            clauses.append([~v1, ~v2])
    return clauses

def at_least_one(lits):
    clauses = [[x for x in lits]]
    return clauses

def exactly_one(lits):
    return at_least_one(lits) + at_most_one(lits)

def solve(path):
    cnf = CNF()
    sudoku = read_sudoku(path)
    SUBGROUP_LENGTH = sudoku.subgroup_length
    SUBGROUP_HEIGHT = sudoku.subgroup_height
    VALUES = (SUBGROUP_HEIGHT *  SUBGROUP_LENGTH)

    # ---- Variables ---

    # We have a Boolean for each cell j,i and value v.
    # Where j is the row
    # and i is the column
    # Function var(j,i,v) returns Boolean variable Bool('Cell_{:d}_{:d}_{:d}'.format(j, i, v))
    #
    # Ex: A call to var(1,1,2) returns Bool('Cell_1_1_2')
    # The intended meaning is: 
    # Cell_1_1_2 is True iff Cell 1,1 is assigned to value 3.
    
    # Notice that all the values are 0-indexed!
    # This means that the upper left cell with value 1 is
    # represented by the boolean variable var(0, 0, 0) ==> Cell_0_0_0
    

    # --- Clauses ----

    # Fixed: Fixed values must appear in their corresponding cell.
    for j in range(VALUES):
        for i in range(VALUES):
            v = sudoku.cells[i][j]
            if v is not None:
                # - YOUR CODE HERE - 
                cnf.add_clause([var(j,i,v)])

    # Cells: Each Cell contains exactly one value.
    # - YOUR CODE HERE -
    for j in range(VALUES):
        for i in range(VALUES):
            lits = []
            for v in range(VALUES):
                lits.append(var(j,i,v))
                #cnf.add_clauses(at_least_one(lits))
                #cnf.add_clauses(at_most_one(lits))
                    
            cnf.add_clauses(exactly_one(lits))
    # Row: Each value appears exactly once in each row.
    # - YOUR CODE HERE -
    for j in range(VALUES):
        for v in range(VALUES):
            lits = []
            for i in range(VALUES):

                lits.append(var(j,i,v))
            cnf.add_clauses(exactly_one(lits))
            
        #cnf.add_clauses(exactly_one(lits))
        

            

    # Column: Each value appears exactly once in each column.
    # - YOUR CODE HERE -
    for i in range(VALUES):
        for v in range(VALUES):
            lits = []
            for j in range(VALUES):

                lits.append(var(j,i,v))
            cnf.add_clauses(exactly_one(lits))



    # Subgroup: Each value appears exactly once in each subgroup.
    # - YOUR CODE HERE -
    p = 0
    q = 0 
    for k in range(SUBGROUP_HEIGHT):
        for l in range(SUBGROUP_LENGTH):
            for v in range(VALUES):
                lits = [] 
                for j in range(p,SUBGROUP_HEIGHT + p):
                    for i in range(q,SUBGROUP_LENGTH + q):
                        lits.append(var(j,i,v))
                cnf.add_clauses(exactly_one(lits))
            p += SUBGROUP_HEIGHT
        q += SUBGROUP_LENGTH
        p = 0
    
    s = Glucose41()
    s.add_clauses(cnf.clauses)
    has_solution = s.solve()
    print('Has solution?', has_solution)

    if has_solution:
        interp = s.model()
        visualize(cnf.decode_dimacs(interp), sudoku)

if __name__ == '__main__':
    #solve(sys.argv[1])
    solve("exH.txt")
