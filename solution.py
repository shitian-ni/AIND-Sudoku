def cross(a,b):
    return [s+t for s in a for t in b]

assignments  = []

all_digits   = "123456789"
rows         = "ABCDEFGHI"
cols         = "123456789"

cols_rev     = cols[::-1]
boxes        = cross(rows,cols)     
row_units    = [cross(r,cols) for r in rows]
column_units = [cross(rows,c) for c in cols]
square_units = [cross(rs,cs) for rs in ("ABC","DEF","GHI") for cs in ("123","456","789")]
diag_units   = [[rows[i]+cols[i] for i in range(9)]]
diag2_units  = [[rows[i]+cols_rev[i] for i in range(9)]]
unit_list    = row_units+column_units+square_units+diag_units+diag2_units

units        = dict((s,[u for u in unit_list if s in u]) for s in boxes)
peers        = dict((s,set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    boxes = [box for box in values.keys() if len(values[box])==2]
    naked_twins = [[box1,box2] for box1 in boxes for box2 in peers[box1] if values[box1]==values[box2]]
    for i in range(len(naked_twins)):
        box1 = naked_twins[i][0]
        box2 = naked_twins[i][1]
        peer1 = peers[box1]
        peer2 = peers[box2]
        p_interval = peer1 & peer2
        for peer in p_interval:
            for to_rm in values[box1]:
                values = assign_value(values,peer,values[peer].replace(to_rm,""))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values=[]
    for c in grid:
        if c==".":
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    return dict(zip(boxes,values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values==False:
        print("Unsolvable")
        return
    for key,value in values.items():
        print(value,end=" ")
        if key[1]=='9':
            print()

def eliminate(values):
    """
        if only 1 value in box, eliminate the value in peers
    """
    solved_boxes = [box for box in values.keys() if len(values[box])==1]
    for solved_box in solved_boxes:
        digit = values[solved_box]
        peers_to_update = peers[solved_box]
        for peer in peers_to_update:
            values = assign_value(values,peer,values[peer].replace(digit,""))
    return values

def only_choice(values):
    """
        if only one box has the digit, eliminate all other values in the box
    """
    for unit in unit_list:
        for digit in all_digits:
            digit_boxes=[box for box in unit if digit in values[box]]
            if len(digit_boxes) == 1:
                values = assign_value(values,digit_boxes[0],digit)
    return values

def reduce_puzzle(values):
    """
        continue until no more eliminated
    """
    stalled = False
    while not stalled:
        before  = len([box for box in values.keys() if len(values[box])==1])
        values  = eliminate(values)
        values  = only_choice(values)
        values  = naked_twins(values)
        after   = len([box for box in values.keys() if len(values[box])==1])
        stalled = before==after
        if len([box for box in values.keys() if len(values[box])==0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values==False:
        return False
    if all(len(values[s])==1 for s in boxes):
        return values

    # start the search from the box with the minimum possibilities
    n,s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    print("----------Solved----------")
    display(values)
    print("--------------------------")
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
