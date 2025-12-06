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

load_dotenv()


@dataclass
class Problem:
    index: int
    numbers: list[int]
    operation: str

    def add(self, new_number: int) -> None:
        self.numbers.append(new_number)

def part1_solve(input_lines: list[str]) -> int:
    operations = [z.strip() for z in input_lines.pop().split()]
    problems = {}
    for numbers in input_lines:
        line_inputs = [int(z) for z in numbers.split()]
        for index, number in enumerate(line_inputs):
            current_problem = problems.get(index, None)
            if current_problem is None:
                problems[index] = Problem(index, [number], operations[index].strip())
            else:
                current_problem.add(number)
    results = []
    for key, value in problems.items():
        if value.operation == "*":
            results.append(reduce(mul, value.numbers))
        else:
            results.append(sum(value.numbers))
    return sum(results)


def part2_solve(input_ranges: list[str]) -> int:
    pass


def main() -> None:
    puzzle = Puzzle(year=2025, day=6)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    ic(part1_solve(example_data))
    ic(part1_solve(puzzle.input_data.splitlines()))
    #
    # ic(part2_solve(example_data))
    # ic(part2_solve(puzzle.input_data.splitlines()))


if __name__ == '__main__':
    main()
