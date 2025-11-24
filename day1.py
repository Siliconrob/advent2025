from collections import Counter
from typing import Tuple
import more_itertools
import networkx
from aocd.models import Puzzle
from icecream import ic
from dotenv import load_dotenv

load_dotenv()

def part1_solve(list1: list[int], list2: list[int]) -> int:
    pass

def part2_solve(list1: list[int], list2: list[int]) -> int:
    pass

def main() -> None:
    puzzle = Puzzle(year=2025, day=1)
    example = puzzle.examples.pop()
    ic(part1_solve(example))
    ic(part2_solve(example))



if __name__ == '__main__':
    main()