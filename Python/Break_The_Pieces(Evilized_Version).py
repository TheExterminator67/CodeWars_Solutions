USE_BREAK_DISPLAY = True

def break_evil_pieces(shape):
    if not shape.strip():
        return []

    (rows, cols, shape) = interpolate(shape)

    empty_spaces = {(row, col) for row in range(rows) for col in range(cols) if shape[row][col] == ' '}
    regions = []
    while empty_spaces:
        R = {empty_spaces.pop()}
        row_empty_neighbors = R
        while row_empty_neighbors:
            row_empty_neighbors = {j for i in row_empty_neighbors for j in neighbor(i) & empty_spaces} - R
            R.update(row_empty_neighbors)
        empty_spaces = empty_spaces - R

        boundary = {j for i in R for j in neighbor8(i)} - R
        min_row = min(row for row, col in boundary)
        max_row = max(row for row, col in boundary) + 1
        min_col = min(col for row, col in boundary)
        max_col = max(col for row, col in boundary) + 1

        if min_row < 0 or min_col < 0 or max_row > rows or max_col > cols:
            continue

        region = [list(row[min_col:max_col]) for row in shape[min_row:max_row]]

        for row in range(len(region)):
            for col in range(len(region[row])):
                if region[row][col] != ' ' and (row + min_row, col + min_col) not in boundary:
                    region[row][col] = ' '
                elif region[row][col] == '+':
                    c = (row + min_row, col + min_col)
                    if not (horizontal_neightbor(c) & boundary and vertical_neightbor(c) & boundary):
                        region[row][col] = '-' if horizontal_neightbor(c) & boundary else '|'
        regions.append('\n'.join(''.join(row[::2]).rstrip() for row in region[::2]))
    return regions


    
def interpolate(s):
    shape = s.split('\n')
    
    while not shape[0].strip():
        shape = shape[1:]
    while not shape[-1].strip():
        shape = shape[:-1]

    lines = len(shape)
    max_len_line = max(len(shape[line]) for line in range(lines))


    for row in range(lines):
        shape[row] += ' ' * (max_len_line - len(shape[row]))
    

    new_shape = [[]] * (2 * lines - 1)

    for row in range(2 * lines - 1):
        new_shape[row] = [' '] * (2 * max_len_line - 1)
        if row % 2:
            for col in range(max_len_line):
                if shape[row // 2][col] in '|+' and shape[row // 2 + 1][col] in '|+':
                    new_shape[row][2 * col] = '|'
        else:
            for col in range(2 * max_len_line - 1):
                if col % 2:
                    if shape[row // 2] [col // 2] in '-+' and shape[row // 2][col // 2 + 1] in '-+':
                        new_shape[row][col] = '-'
                else:
                    new_shape[row][col] = shape[row // 2][col // 2]
    return 2 * lines - 1, 2 * max_len_line - 1, new_shape

neighbor = lambda col: {(col[0] + 1, col[1]), (col[0] - 1, col[1]), (col[0], col[1] + 1), (col[0], col[1] - 1)}

neighbor8 = lambda c: {(c[0] + i, c[1] + j) for i in {1, -1, 0} for j in {1, -1, 0}}

vertical_neightbor = lambda c: {(c[0] + 1, c[1]), (c[0] - 1, c[1])}

horizontal_neightbor = lambda c: {(c[0], c[1] + 1), (c[0], c[1] - 1)}

'''
name = "3 boxes"
shape = """
+------------+
|            |
|            |
|            |
+------+-----+
|      |     |
|      |     |
+------+-----+
""".strip('\n')

expected = ["""
+------------+
|            |
|            |
|            |
+------------+
""".strip('\n'), """
+------+
|      |
|      |
+------+
""".strip('\n'), """
+-----+
|     |
|     |
+-----+
""".strip('\n'),]

break_evil_pieces(shape)
'''
'''
name = "Lego stuff"
shape = """
+-------------------+--+
|                   |  |
|                   |  |
|  +----------------+  |
|  |                   |
|  |                   |
+--+-------------------+
""".strip('\n')

expected = ["""
+-------------------+
|                   |
|                   |
|  +----------------+
|  |
|  |
+--+
""".strip('\n'), """
                 +--+
                 |  |
                 |  |
+----------------+  |
|                   |
|                   |
+-------------------+
""".strip('\n'),]

break_evil_pieces(shape)
'''

name = "Warming up"
shape = """
+------------+
|            |
|            |
|            |
+------++----+
|      ||    |
|      ||    |
+------++----+
""".strip('\n')

expected = ["""
+------------+
|            |
|            |
|            |
+------------+
""".strip('\n'), """
+------+
|      |
|      |
+------+
""".strip('\n'), """
+----+
|    |
|    |
+----+
""".strip('\n'), """
++
||
||
++
""".strip('\n'),]
print(break_evil_pieces(shape))