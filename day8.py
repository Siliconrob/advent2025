from collections import Counter
from operator import mul
from typing import Tuple
from urllib.response import addinfo

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
from itertools import pairwise

load_dotenv()


def create_grid(input_data: list[str]) -> list[list[str]]:
    grid = []
    for row in input_data:
        current_row = []
        for col in row:
            current_row.append(col)
        grid.append(current_row)
    return grid


def next_drop(grid, i, j):
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    directions = [(1, 0)]
    neighbors = []
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            neighbors.append(grid[ni][nj])
    return neighbors


def set_split_positions(grid, i, j):
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    directions = [(1, -1), (1, 1)]
    next_positions = []
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            next_spot = grid[ni][nj]
            if next_spot == '.':
                grid[ni][nj] = '|'
                next_positions.append((ni, nj))
    return next_positions


def get_indices(lst, targets):
    return list(filter(lambda x: lst[x] in targets, range(len(lst))))


def part1_solve(input_lines: list[str]) -> int:
    the_grid = create_grid(input_lines)
    for row_index, row in enumerate(the_grid):
        current_row = the_grid[row_index]
        the_row = "".join(current_row)
        beam_positions = get_indices(current_row, ['S', '|'])
        for beam_position in beam_positions:
            direct_flow_position = next_drop(the_grid, row_index, beam_position)
            if len(direct_flow_position) == 0:
                continue
            if direct_flow_position[0] in ['.', '|']:
                the_grid[row_index + 1][beam_position] = '|'
                continue
            new_splits = set_split_positions(the_grid, row_index, beam_position)

    splits = {0: 0}
    for line_index, line in enumerate(the_grid):
        blocker_positions = get_indices(line, ['^'])
        if len(blocker_positions) == 0:
            continue
        previous_line = the_grid[line_index - 1]
        split_count = 0
        for blocker_position in blocker_positions:
            if previous_line[blocker_position] == '|':
                split_count += 1
        splits[line_index] = split_count

    return sum(splits.values())


def part2_solve(input_lines: list[str]) -> int:
    # Idea from reddit users
    # Create a split positions summation array
    # and then every iteration sums up every possible choice left + right in the iteration beam
    # then sum all the beam runs

    current_beams = [0] * len(input_lines[0])
    current_beams[get_indices(input_lines[0], ['S']).pop()] += 1
    split_positions = []
    for line_index, input_line in enumerate(input_lines):
        split_indexes = get_indices(input_line, ['^'])
        if len(split_indexes) > 0:
            split_positions.append(set(split_indexes))

    for current_split in split_positions:
        new_beams = [0] * len(input_lines[0])
        for i, count in enumerate(current_beams):
            if count > 0:
                if i in current_split:
                    new_beams[i - 1] += count
                    new_beams[i + 1] += count
                else:
                    new_beams[i] += count
        current_beams = new_beams
    return sum(current_beams)


def main() -> None:
    puzzle = Puzzle(year=2025, day=8)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    ic(part1_solve(example_data))
    # ic(part1_solve(puzzle.input_data.splitlines()))
    #
    # ic(part2_solve(example_data))
    # ic(part2_solve(puzzle.input_data.splitlines()))


if __name__ == '__main__':
    main()
