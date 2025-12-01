from collections import Counter
from typing import Tuple
import more_itertools
import networkx
from aocd.models import Puzzle
from icecream import ic
from dotenv import load_dotenv

load_dotenv()

def parse_instruction(instruction: str) -> Tuple[int, int]:
    direction = -1 if instruction[0:1] == 'L' else 1
    return (
        direction,
        int(instruction[1:])
    )

def part1_solve(start_pos: int, instructions: list[str]) -> int:
    zero_counts = 0
    current_pos = start_pos
    for instruction in instructions:
        results = ic(parse_instruction(instruction))
        current_pos = (current_pos + results[0] * results[1]) % 100
        current_pos = abs(current_pos)
        if current_pos == 0:
            zero_counts += 1
    return zero_counts

def part2_solve(list1: list[int], list2: list[int]) -> int:
    pass

def main() -> None:
    puzzle = Puzzle(year=2025, day=1)
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()
    start_position = 50
    ic(part1_solve(start_position, example_data))
    ic(part1_solve(start_position, puzzle.input_data.splitlines()))



if __name__ == '__main__':
    main()