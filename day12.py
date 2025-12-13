import functools
import math
import re
from collections import Counter
from operator import mul
from typing import Tuple
from urllib.response import addinfo

import more_itertools
import networkx
import networkx as nx
import pydapper
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

from networkx.algorithms.operators.binary import difference
from networkx.algorithms.simple_paths import all_simple_paths
from networkx.readwrite import adjlist
from networkx.readwrite.json_graph.adjacency import adjacency_data
from shapely import LineString
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve
from shapely.geometry.polygon import Polygon, LinearRing
from scipy import ndimage
from heapq import heappop, heappush
from dataclasses import dataclass, field
from itertools import pairwise
from frozendict import frozendict

load_dotenv()


@dataclass
class Shape:
    index: int = 0
    points: list[list[str]] = field(default_factory=list)

    def empty_points(self) -> list[tuple[int, int]]:
        empty_locations = []
        for row_index, row in enumerate(self.points):
            for column_index, column in enumerate(row):
                if column == ".":
                    empty_locations.append((row_index, column_index))
        return empty_locations


@dataclass
class Region:
    size: tuple[int, int] = (0, 0)
    shapes_index: list[int] = field(default_factory=list)


def part1_solve(input_data: str) -> int:
    all_shapes = []
    all_regions = []

    data_inputs = deque(input_data.splitlines())
    shape_index = 0
    current_shape = Shape()

    while data_inputs:
        line = data_inputs.popleft()
        if line == "":
            all_shapes.append(current_shape)
            shape_index += 1
            current_shape = Shape(index=shape_index)
        if "#" in line:
            current_shape.points.append(line)
            continue
        if "x" in line:
            size, presents = line.split(":")
            width, height = size.split("x")
            shape_index = [int(present) for present in presents.split()]
            all_regions.append(Region(size=(int(width), int(height)), shapes_index=shape_index))

    valid_regions = {}
    for region_index, region in enumerate(all_regions):
        ic(region)
        shapes_to_fit = []
        for index, count in enumerate(region.shapes_index):
            while count > 0:
                shapes_to_fit.append(all_shapes[index])
                count -= 1
        total_points = sum(9 - len(shape.empty_points()) for shape in shapes_to_fit)
        area_to_fit = region.size[0] * region.size[1]
        if total_points > area_to_fit:
            # too small an area
            continue
        # I don't know exactly why this works, but reddit tips was count the shapes
        # they are always the same bounding box of 9
        # and then Total Area - Bounding Box area if it's less than 0 invalid
        # I guess it makes sense if you think of it as a puzzle and each piece is a square ?!
        spaces = area_to_fit - total_points
        if spaces < 0:
            continue
        if spaces > 0:
            valid_regions[region_index] = 1
    return len(valid_regions.items())


def main() -> None:
    puzzle = Puzzle(year=2025, day=12)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data

    # The example input is the general case, extremely difficult to solve at scale
    ic(part1_solve(example_data))
    # The actual input is all the blocks either fit loosely or don't
    ic(part1_solve(puzzle.input_data))


if __name__ == '__main__':
    main()
