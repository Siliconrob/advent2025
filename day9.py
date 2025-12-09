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

    #
    #
    #
    #
    # all_locations = parse_locations(input_lines)
    #
    # distances = {}
    #
    # items = len(all_locations)
    # for i in range(items):
    #     for j in range(i + 1, items):
    #         distances[frozenset([i, j])] = all_locations[i].distance(all_locations[j])
    #
    # sorted_by_distances = sorted(distances.items(), key=lambda x: x[1])
    # run_times = 0
    # connections = {i: {i} for i in range(len(sorted_by_distances))}
    # for id, distance in dict(sorted_by_distances).items():
    #     if run_times > connection_runs:
    #         break
    #     run_times += 1
    #     start, end = id
    #     matched_connections = connections[start] | connections[end]
    #     for match in matched_connections:
    #         connections[match] = matched_connections
    # unique_components = {frozenset(z) for z in connections.values()}
    # conn_sets = sorted([len(z) for z in unique_components], reverse=True)
    # # conn_set_sizes = sorted([len(connection_set) for connection_set in connections.values()], reverse=True)[:3]
    # return reduce(mul, conn_sets[:3])



def part2_solve(input_lines: list[str], connection_runs: int) -> int:
    pass



def main() -> None:
    puzzle = Puzzle(year=2025, day=9)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    ic(part1_solve(example_data))
    ic(part1_solve(puzzle.input_data.splitlines()))
    #
    # ic(part2_solve(example_data, 10))
    # ic(part2_solve(puzzle.input_data.splitlines()))


if __name__ == '__main__':
    main()
