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

def parse_ranges(input_ranges: list[str]) -> list[Tuple[int, int]]:
    ranges = []
    for range_str in input_ranges:
        start, end = range_str.split('-')
        ranges.append((int(start), int(end)))
    return ranges

def parse_ingredients(input_ids: list[str]) -> list[int]:
    return [int(id) for id in input_ids]


def part1_solve(input_ranges: list[str], input_ids: list[str]) -> int:
    available_ranges = parse_ranges(input_ranges)
    ingredients = parse_ingredients(input_ids)
    fresh = []
    for ingredient_id in ingredients:
        for available_range in available_ranges:
            start, end = available_range
            if ingredient_id >= start and ingredient_id <= end:
                fresh.append(ingredient_id)
                break
    return len(fresh)


    # grid = []
    # for row in input_grid:
    #     current_row = []
    #     for col in row:
    #         current_row.append(col)
    #     grid.append(current_row)
    # access_points = {}
    # for row_index, row in enumerate(grid):
    #     for col_index, col in enumerate(row):
    #         if col == '@':
    #             adjs = ic(get_neighbors(grid, row_index, col_index))
    #             counts = Counter(adjs)
    #             paper_counts = counts.get('@', 0)
    #             if paper_counts < 4:
    #                 access_points[(row_index, col_index)] = paper_counts
    # return len(access_points)


def part2_solve(input_ranges: list[str]) -> int:
    available_ranges = parse_ranges(input_ranges)
    available_ranges.sort(key=lambda z: z[0])
    merged_ranges = [available_ranges[0]]
    for current_range in available_ranges[1:]:
        last_range = merged_ranges[-1]
        if current_range[0] <= last_range[1] + 1:
            merged_ranges[-1] = (last_range[0], max(last_range[1], current_range[1]))
        else:
            merged_ranges.append(current_range)
    fresh_ingredients = 0
    for current_range in merged_ranges:
        items = current_range[1] - current_range[0] + 1
        fresh_ingredients += items
    return fresh_ingredients





def main() -> None:
    puzzle = Puzzle(year=2025, day=5)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.split("\n\n")
    example_ingredient_ranges = example_data[0].splitlines()
    example_ingredient_ids = example_data[1].splitlines()


    puzzle_data = puzzle.input_data.split("\n\n")
    ingredient_ranges = puzzle_data[0].splitlines()
    ingredient_ids = puzzle_data[1].splitlines()

    ic(part1_solve(example_ingredient_ranges, example_ingredient_ids))
    ic(part1_solve(ingredient_ranges, ingredient_ids))

    ic(part2_solve(example_ingredient_ranges))
    ic(part2_solve(ingredient_ranges))


if __name__ == '__main__':
    main()
