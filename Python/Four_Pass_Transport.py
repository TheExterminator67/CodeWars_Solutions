from itertools import permutations, chain, product

def bfs(start, is_goal, neighbors, ret_visited=False):
    nodes = [(start, None)]
    visited = set([start])
    while nodes:
        next_nodes = []
        for node, prev in nodes:
            if is_goal(node):
                path = [node]
                while prev:
                    node, prev = prev
                    path.append(node)
                return list(reversed(path))
            for n in (x for x in neighbors(node) if x not in visited):
                visited.add(n)
                next_nodes.append((n, (node, prev)))
        nodes = next_nodes
    return visited if ret_visited else None

def four_pass(stations):
    stations = [divmod(p, 10) for p in stations]
    def connect(grid, a, b, flag):
        dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)] if flag else [(-1, 0), (1, 0), (0, -1), (0, 1)]
        def neighbors(pos):
            i, j = pos
            for di, dj in dirs:
                i1, j1 = i + di, j + dj
                if (i1, j1) == stations[b] or (0 <= i1 < 10 and 0 <= j1 < 10 and not grid[i1][j1]):
                    yield i1, j1
        path = bfs(stations[a], lambda p: p == stations[b], neighbors)
        if not path:
            return None
        for (i, j) in path:
            grid[i][j] = 1
        return path

    min_path = None
    for flags in product([False, True], repeat=3):
        for p in permutations([(0, 1), (1, 2), (2, 3)]):
            grid = [[0] * 10 for _ in range(10)]
            for (i, j) in stations:
                grid[i][j] = 1
            result = [None] * 3
            for a, b in p:
                path = connect(grid, a, b, flags[a])
                if not path:
                    break
                result[a] = path[1:]
            else:
                result = list(chain(*result))
                if not min_path or len(result) < len(min_path):
                    min_path = result

    return [10 * i + j for i, j in [stations[0]] + min_path] if min_path else None