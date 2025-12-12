import functools
import math
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
    points: list[str] = field(default_factory=list)


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

    for region in all_regions:
        ic(region)
        grid = np.zeros(region.size)
        shapes_to_fit = []
        for index, count in enumerate(region.shapes_index):
            while count > 0:
                shapes_to_fit.append(all_shapes[index])
                count -= 1
        ic(shapes_to_fit)





def part2_solve(input_lines: list[str], begin_range: int, end_range: int) -> int:
    pass



def main() -> None:
    puzzle = Puzzle(year=2025, day=12)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data

    ic(part1_solve(example_data))
    # ic(part1_solve(puzzle.input_data.splitlines()))
    #
    # ic(part2_solve(example_data, 20, 50))
    # ic(part2_solve(puzzle.input_data.splitlines(), 1_400_000_000, 1_500_000_000))



if __name__ == '__main__':
    main()
