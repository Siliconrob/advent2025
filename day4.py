from collections import Counter
from typing import Tuple
import more_itertools
import networkx
from aocd.models import Puzzle
from icecream import ic
from dotenv import load_dotenv
import numpy as np
from more_itertools import peekable, strip
from more_itertools.recipes import flatten, pairwise
from itertools import cycle
import copy
from functools import reduce, cache
from collections import deque
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve
from shapely.geometry.polygon import Polygon, LinearRing
from scipy import ndimage
from heapq import heappop, heappush
from dataclasses import dataclass, field

load_dotenv()


def get_neighbors(grid, i, j):
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    neighbors = []
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            neighbors.append(grid[ni][nj])
    return neighbors

def part1_solve(input_grid: list[str]) -> int:

    grid = []
    for row in input_grid:
        current_row = []
        for col in row:
            current_row.append(col)
        grid.append(current_row)

    access_points = {}

    for row_index, row in enumerate(input_grid):
        for col_index, col in enumerate(row):
            if col == '@':
                adjs = ic(get_neighbors(grid, row_index, col_index))
                counts = Counter(adjs)
                paper_counts = counts.get('@', 0)
                if paper_counts < 4:
                    access_points[(row_index, col_index)] = paper_counts
    return len(access_points)


def part2_solve(batteries: list[str]) -> int:
    max_volts = []
    for battery in batteries:
        digits = [int(elem) for elem in list(battery)]

        while len(digits) > 12:
            removed = False
            for i in range(len(digits) - 1):
                if digits[i] < digits[i + 1]:
                    del digits[i]
                    removed = True
                    break
            if not removed:
                digits = digits[:-1]

        max_volts.append(int("".join(str(x) for x in digits)))

    return sum(max_volts)


def main() -> None:
    puzzle = Puzzle(year=2025, day=4)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    ic(part1_solve(example_data))
    ic(part1_solve(puzzle.input_data.splitlines()))

    # ic(part2_solve(example_data))
    # ic(part2_solve(puzzle.input_data.splitlines()))


if __name__ == '__main__':
    main()
