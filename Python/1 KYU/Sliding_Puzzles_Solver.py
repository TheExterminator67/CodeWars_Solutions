import numpy as np
import queue


def compare(a, b):
    if a == b:
        return 0
    if a > b:
        return 1
    if a < b:
        return -1


class Puzzle:
    def __init__(self, puzzle):
        self.puzzle = np.array(puzzle, dtype=np.object)
        self.solved = np.zeros_like(self.puzzle, dtype=int)
        self.height, self.width = self.puzzle.shape
        self.steps = []

        # Build puzzle & solution to compare against:
        for i, row in enumerate(self.puzzle):
            for j, value in enumerate(row):
                self.puzzle[i, j] = Case(value)
                self.puzzle[i, j].y, self.puzzle[i, j].x = i, j
                self.solved[i, j] = 1 + j + self.width*i
        self.solved[-1, -1] = 0

        for row in self.puzzle:
            [case.get_paths(self.puzzle) for case in row]

    def clear(self):
        [case.clear() for case in np.ravel(self.puzzle)]

    def find_number(self, n):
        for row in self.puzzle:
            for node in row:
                if node.value == n:
                    return node
        return None

    def solve_number(self, destination, number, ignore=None, solve=True):
        while destination.value != number:

            hole = self.find_number(0)
            goto = self.find_number(number)
            adjacent = goto.best_adjacent(self.puzzle, relative_to=destination)
            path = hole.astar(self, adjacent, goto, ignore)
            for one, two in zip(path, path[1:]):
                self.steps.append(two.value)
                one.swap(two)
            else:
                self.steps.append(goto.value)
                path[-1].swap(goto)

        if solve:
            destination.solved = True
        return True

    def solve_line(self, line, solutions, helper_cases):
        for case, solution in zip(line[:-2], solutions[:-2]):
            self.solve_number(case, solution)


        self.solve_number(helper_cases[2], solutions[-1], solve=False)
        self.solve_number(helper_cases[3], solutions[-2], solve=False)

        self.solve_number(line[-1], solutions[-2], solve=False)
        self.solve_number(helper_cases[0], solutions[-1], solve=False)

        if line[-2] != self.find_number(0):
            self.solve_number(helper_cases[1], line[-2].value,
                              ignore=[helper_cases[0], line[-1]], solve=False)

        self.solve_number(line[-2], solutions[-2])
        self.solve_number(line[-1], solutions[-1])

        return True

    def smol_solve(self):
        smallest = 2

        for i in range(self.height-smallest):
            helper_cases = (self.puzzle[i+1, -1], self.puzzle[i+1, -2],
                            self.puzzle[i+2, -1], self.puzzle[i+2, -2])
            self.solve_line(self.puzzle[i, :], self.solved[i, :], helper_cases)
            helper_cases = (self.puzzle[-1, i+1], self.puzzle[-2, i+1],
                            self.puzzle[-1, i+2], self.puzzle[-2, i+2])
            self.solve_line(self.puzzle[i+1:, i], self.solved[i+1:, i], helper_cases)

        return True

    def final_solve(self, fragment, solution):

        for i in range(24):
            solution = self.puzzle[-3:, -3:].ravel().tolist()[:-1]
            solution = [s.value for s in solution]
            if sorted(solution) == solution:
                return True

            hole = self.find_number(0)
            if i < 12:
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-2, -2]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-1, -1]
            if i >= 12:
                if hole.y == self.height-1 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -2]
                if hole.y == self.height-2 and hole.x == self.width-1:
                    guy = self.puzzle[-1, -1]
                if hole.y == self.height-2 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -1]
                if hole.y == self.height-1 and hole.x == self.width-2:
                    guy = self.puzzle[-2, -2]
            self.steps.append(guy.value)
            hole.swap(guy)
        self.steps = None

    def solve(self):
        self.smol_solve()
        self.final_solve(self.puzzle[-3:, -3:].ravel().tolist(),
                         self.solved[-3:, -3:].ravel().tolist())
        print(self.puzzle)


class Case:
    def __init__(self, value):
        self.value = value
        self.solved = False
        self.paths = []
        self.distance = np.Infinity
        self.back = None

    def __gt__(self, other):
        return self.distance > other.distance

    def __repr__(self):
        return str(self.value)

    @property
    def info(self):
        return f'Case w/ value {self.value} at ({self.y}, {self.x}).'

    def clear(self):
        self.distance = np.Infinity
        self.back = None

    def swap(self, other):
        self.value, other.value = other.value, self.value
        self.solved, other.solved = other.solved, self.solved

    def get_paths(self, puzzle):
        height, width = puzzle.shape
        if self.y > 0:
            self.paths.append(puzzle[self.y-1, self.x])
        if self.y < height-1:
            self.paths.append(puzzle[self.y+1, self.x])
        if self.x > 0:
            self.paths.append(puzzle[self.y, self.x-1])
        if self.x < width-1:
            self.paths.append(puzzle[self.y, self.x+1])

    def best_adjacent(self, puzzle, relative_to):
        possible_paths = []
        for path in self.paths:
            if not path.solved:


                possible_paths.append((relative_to.distance_to(path), path))

        if not possible_paths:
            print(f'Could not find any good adjacent cases for {self.y}, {self.x}')
            for path in self.paths:
                print(f'({path.y}, {path.x}), solved = {path.solved}')
            print(puzzle.puzzle)

        solution = sorted(possible_paths, key=lambda x: x[0])[0]

        return solution[1]

    def dijkstra(self, puzzle, destination, number, ignore=None):
        '''A* is way more efficient on big maps! Use it instead'''

        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore:
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance, posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def astar(self, puzzle, destination, number, ignore=None):

        ignore = ignore or []
        q = queue.PriorityQueue()
        self.distance = 0
        q.put((0, self))

        while not q.empty():
            _, case = q.get()
            if case == destination:
                break
            for posib in case.paths:
                if posib.back != case:
                    if posib != number and not posib.solved and posib not in ignore: 
                        if posib.distance > 1+case.distance:
                            posib.distance = 1+case.distance
                            posib.back = case
                            q.put((posib.distance_to(destination), posib))

        node = destination
        path = []
        while node.back:
            path.append(node)
            node = node.back
        path.append(node)

        puzzle.clear()
        return list(reversed(path))

    def distance_to(self, other):
        return abs(self.y-other.y)+abs(self.x-other.x)


def slide_puzzle(array):
    puzzle = Puzzle(array)
    puzzle.solve()
    return puzzle.steps




array = [
        [4, 1, 3],
        [2, 8, 0],
        [7, 6, 5],
        ]

print(slide_puzzle(array))