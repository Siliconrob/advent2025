import math
from collections import Counter
from operator import mul
from typing import Tuple
from urllib.response import addinfo

import more_itertools
import networkx
import shapely
from aocd.models import Puzzle
from icecream import ic
from dotenv import load_dotenv
import numpy as np
from more_itertools import peekable, strip
from more_itertools.recipes import flatten, pairwise, unique
from itertools import cycle, combinations
import copy
from functools import reduce, cache
from collections import deque

from shapely import LineString
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve
from shapely.geometry.polygon import Polygon, LinearRing
from scipy import ndimage
from heapq import heappop, heappush
from dataclasses import dataclass, field
from itertools import pairwise

load_dotenv()


@dataclass
class Point:
    x: int
    y: int


def parse_coords(input_lines: list[str]) -> list[Point]:
    points = []
    for line in input_lines:
        x, y = line.split(',')
        points.append(Point(int(x), int(y)))
    return points


def part1_solve(input_lines: list[str]) -> int:
    coords = parse_coords(input_lines)
    max_size = None
    for combo in combinations(coords, 2):
        point1, point2 = combo
        width = abs(point1.x - point2.x) + 1
        height = abs(point1.y - point2.y) + 1
        new_area = width * height
        if max_size is None or new_area > max_size:
            max_size = new_area
    return max_size

def part2_solve(input_lines: list[str]) -> int:
    coords = parse_coords(input_lines)


    max_x = 0
    max_y = 0
    for input_line in input_lines:
        x, y = input_line.split(',')
        if int(x) > max_x:
            max_x = int(x)
        if int(y) > max_y:
            max_y = int(y)
    grid = np.zeros((max_y + 2, max_x+2))
    # set points
    for point in coords:
        grid[point.y, point.x] = 1

    # Fill the columns
    # for current_col in range(max_x+2):
    #     column = grid[:,current_col]
    #     col_coords = np.where(column == 1)[0]
    #     if len(col_coords) > 0:
    #         for col_coord in range(min(col_coords), max(col_coords) + 1):
    #             grid[col_coord, current_col] = 1

    for current_col in range(max_x + 2):
        column = grid[:, current_col]
        col_coords = np.where(column == 1)[0]
        if col_coords.size:
            grid[min(col_coords):max(col_coords) + 1, current_col] = 1

    # # Fill the rows
    # for row_index, row in enumerate(grid):
    #     row_coords = np.where(row == 1)[0]
    #     if len(row_coords) > 0:
    #         for row_coord in range(min(row_coords), max(row_coords) + 1):
    #             grid[row_index, row_coord] = 1

    max_size = None

    all_combos = list(combinations(coords, 2))

    sorted_combos = sorted(all_combos, key=lambda x: (abs(x[0].x - x[1].x) + 1) * (abs(x[0].y - x[1].y) + 1), reverse=True)
    for combo_index, combo in enumerate(sorted_combos):
        # if combo_index % 5000 == 0:
        #     ic(combo_index)
        point1, point2 = ic(combo)

        width = abs(point1.x - point2.x) + 1
        height = abs(point1.y - point2.y) + 1
        expected_area = width * height

        start_x = min(point1.x, point2.x)
        end_x = max(point1.x, point2.x)
        start_y = min(point1.y, point2.y)
        end_y = max(point1.y, point2.y)

        # if max_size is not None and expected_area < max_size:
        #     continue

        valid_rows = 0
        for row_index in range(start_y, end_y + 1):
            grid_row = grid[row_index]
            col_coords = np.where(grid_row == 1)[0]
            if min(col_coords) <= start_x and max(col_coords) >= end_x:
                valid_rows += 1
            else:
                break
        if valid_rows == end_y - start_y + 1:
            max_size = expected_area
            break
            # if max_size is None or expected_area > max_size:
            #     max_size = ic(expected_area)

    return max_size



def main() -> None:
    puzzle = Puzzle(year=2025, day=9)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    # ic(part1_solve(example_data))
    # ic(part1_solve(puzzle.input_data.splitlines()))
    #
    #ic(part2_solve(example_data))
    ic(part2_solve(puzzle.input_data.splitlines()))


if __name__ == '__main__':
    main()
