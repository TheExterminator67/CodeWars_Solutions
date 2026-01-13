# Expanded range to handle larger 'num'
perfectSquares = {x*x for x in range(2, 60)}

def createGraph(vertices):
    graph = {i: [] for i in range(1, vertices + 1)}
    for origin in range(1, vertices + 1):
        for goal in range(origin + 1, vertices + 1):
            if (origin + goal) in perfectSquares:
                graph[origin].append(goal)
                graph[goal].append(origin)
    return graph

def square_sums(num):
    graph = createGraph(num)
    
    # Track visited nodes using a set for O(1) lookup
    visited = [False] * (num + 1)
    path = []

    def backtrack(current):
        path.append(current)
        visited[current] = True
        
        if len(path) == num:
            return path
        
        # WARNSDORFF'S HEURISTIC: 
        # Sort neighbors by how many unvisited neighbors THEY have.
        # This keeps the "tighter" parts of the graph from becoming isolated.
        neighbors = []
        for n in graph[current]:
            if not visited[n]:
                count = sum(1 for nn in graph[n] if not visited[nn])
                neighbors.append((count, n))
        
        neighbors.sort() # Smallest degree first

        for _, next_pt in neighbors:
            result = backtrack(next_pt)
            if result:
                return result
        
        # Backtrack
        path.pop()
        visited[current] = False
        return None

    
    start_nodes = sorted(range(1, num + 1), key=lambda x: len(graph[x]))
    for i in start_nodes:
        final_path = backtrack(i)
        if final_path:
            return final_path
    return False

# Testing with values
print(f"n=15: {square_sums(15)}")
print(f"n=23: {square_sums(23)}")
print(f"n=37: {square_sums(37)}")