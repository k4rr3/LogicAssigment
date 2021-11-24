from optilog.formulas.modelling import *
from math import sqrt

def var(j, i, v):
    return Bool('Cell_{:d}_{:d}_{:d}'.format(j, i, v))

def visualize(interp, sudoku):
    cells = {
        v.name
        for v in interp
        if not isinstance(v, Not)
    }
    SUBGROUP_LENGTH = sudoku.subgroup_length
    SUBGROUP_HEIGHT = sudoku.subgroup_height
    VALUES = SUBGROUP_HEIGHT * SUBGROUP_LENGTH
    SPACE_VAL = len(str(VALUES))
    GROUPS_HORIZ = VALUES // SUBGROUP_LENGTH
    more_than_one_value_error = False
    for j in range(VALUES):
        if j > 0 and j % SUBGROUP_HEIGHT == 0:
            acc = ''
            for g in range(GROUPS_HORIZ):
                acc += '-' * (SUBGROUP_LENGTH * (SPACE_VAL + 1) - 1)
                if g != GROUPS_HORIZ - 1:
                    acc += '-·-'
            print(acc)
        for i in range(VALUES):
            if i > 0 and i % SUBGROUP_LENGTH == 0:
                print('|', end=' ')
            value_to_print = None
            for v in range(VALUES):
                variable = var(j, i, v)
                if variable.name in cells:
                    if value_to_print is not None:
                        value_to_print = 'E'
                        more_than_one_value_error = True
                    else:
                        value_to_print = v + 1
                    
            if value_to_print is None:
                value_to_print = '-'
            e = str(value_to_print)
            e = ' ' * (SPACE_VAL - len(e)) + e
            print(e, end=' ')
        print()
    if more_than_one_value_error:
        print(f'ERROR! Cell constraints are not correct.')
        print('Cells with more than value set to True represented with letter \'E\'')
        exit(-1)

class Sudoku:
    def __init__(self, cells, subgroup_height=None, subgroup_length=None):
        if subgroup_height is None:
            subgroup_height = int(sqrt(len(cells)))
        if subgroup_length is None:
            subgroup_length = int(sqrt(len(cells[0])))
        
        self.cells = cells
        self.subgroup_height = subgroup_height
        self.subgroup_length = subgroup_length

def read_sudoku(path, print_dim=True):
    cells = []
    with open(path, 'r') as f:
        subgroup_height = None
        subgroup_length = None
        
        for line in f:
            line = line.strip()
            vals = []
            if line.startswith('d'):
                line = line[1:].strip().split()
                subgroup_length, subgroup_height = map(int, line)
                continue
            for c in line.strip().split():
                if c == '-':
                    v = None
                else:
                    v = int(c) - 1
                vals.append(v)
            cells.append(vals)
    if print_dim:
        print('DIMENSIONS REGION', 'Height:', subgroup_height, 'x', 'Length:', subgroup_length)
    return Sudoku(cells, subgroup_height, subgroup_length)
        
