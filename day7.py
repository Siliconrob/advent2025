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
    start_index: int
    number_length: int
    numbers_text: list[str]

    def add_text(self, new_text: str) -> None:
        self.numbers_text.append(new_text)

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


def part2_solve(input_lines: list[str]) -> int:
    operation_line = input_lines.pop()
    operations = [z.strip() for z in operation_line.split()]
    problems = {}

    current_problem = 0
    number_text = operation_line[0]
    current_index = 1
    for char in operation_line[1:]:
        if char in ['*', '+']:
            problems.setdefault(current_problem, Problem(current_problem, [], operations[current_problem], current_index - len(number_text), len(number_text), []))
            current_problem += 1
            number_text = char
        else:
            number_text += char
        current_index += 1
    problems.setdefault(current_problem,Problem(current_problem, [], operations[current_problem], current_index - len(number_text), len(number_text), []))

    for numbers in input_lines:
        current_problem = 0
        while current_problem < len(problems):
            match = problems.get(current_problem, None)
            extract = numbers[match.start_index:match.start_index + match.number_length]
            match.add_text(extract)
            current_problem += 1

    for key, problem in problems.items():
        items = len(problem.numbers_text)
        for count in range(items + 1):
            extracted_numbers = ''
            for problem_number_text in problem.numbers_text:
                backwards = list(reversed(problem_number_text))
                if count >= len(backwards):
                    continue
                value = backwards[count]
                if value != ' ':
                    extracted_numbers += value
            if extracted_numbers != '':
                problem.numbers.append(int(extracted_numbers))

    results = []
    for key, value in problems.items():
        if value.operation == "*":
            results.append(reduce(mul, value.numbers))
        else:
            results.append(sum(value.numbers))
    return sum(results)



def main() -> None:
    puzzle = Puzzle(year=2025, day=7)
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
