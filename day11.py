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

def part2_solve(input_lines: list[str], begin_range: int, end_range: int) -> int:
    pass



def main() -> None:
    puzzle = Puzzle(year=2025, day=11)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    ic(part1_solve(example_data))
    # ic(part1_solve(puzzle.input_data.splitlines()))
    #
    # ic(part2_solve(example_data, 20, 50))
    # ic(part2_solve(puzzle.input_data.splitlines(), 1_400_000_000, 1_500_000_000))



if __name__ == '__main__':
    main()
