from collections import Counter
from typing import Tuple
import more_itertools
import networkx
from aocd.models import Puzzle
from icecream import ic
from dotenv import load_dotenv

load_dotenv()


def is_palindrome(input: str) -> bool:
    mid_point = len(input) // 2
    first_half = input[:mid_point]
    second_half = input[mid_point:]
    return first_half == second_half


def part1_solve(id_ranges: list[str]) -> int:
    invalid_ids = []
    for id_range in id_ranges:
        start, end = id_range.split('-')
        for current_number in range(int(start), int(end)+1):
            if is_palindrome(str(current_number)):
                invalid_ids.append(current_number)
    return sum(invalid_ids)
    # zero_counts = 0
    # current_pos = start_pos
    # for instruction in instructions:
    #     results = ic(parse_instruction(instruction))
    #     current_pos = (current_pos + results[0] * results[1]) % 100
    #     current_pos = abs(current_pos)
    #     if current_pos == 0:
    #         zero_counts += 1
    # return zero_counts


def part2_solve(start_pos: int, instructions: list[str]) -> int:
    zero_counts = 0
    current_pos = start_pos
    for instruction in instructions:
        results = ic(parse_instruction(instruction))
        move = results[0] * results[1]
        if move + current_pos < 0 and current_pos != 0:
            q, r = divmod(abs(move) + current_pos, 100)
            if q == 0:
                q = 1
            zero_counts += q
        if move + current_pos > 100:
            q, r = divmod(move + current_pos, 100)
            zero_counts += q
        next_pos = (current_pos + move) % 100
        current_pos = abs(next_pos)
        if current_pos == 0:
            zero_counts += 1
    return zero_counts


def main() -> None:
    puzzle = Puzzle(year=2025, day=2)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.split(",")


    #ic(part1_solve(example_data))
    ic(part1_solve(puzzle.input_data.split(",")))
    #
    # ic(part2_solve(start_position, example_data))
    # ic(part2_solve(start_position, puzzle.input_data.splitlines()))

if __name__ == '__main__':
    main()
