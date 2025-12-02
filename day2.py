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


def find_longest_substring(input: str) -> str:
    seen = []
    for element in input:
        if element in seen:
            break
        seen.append(element)
    return "".join(seen)


def part2_solve(id_ranges: list[str]) -> int:
    invalid_ids = []
    for id_range in id_ranges:
        start, end = id_range.split('-')
        for current_number in range(int(start), int(end)+1):
            number_text = str(current_number)
            counts = Counter(number_text)
            if len(counts) == 1:
                invalid_ids.append(current_number)
                continue
            if len(counts) < len(number_text):
                for key, value in counts.items():
                    if value > 1:
                        number_text = number_text.replace(key, '', value)
                if number_text == "":
                    if is_palindrome(str(current_number)):
                        invalid_ids.append(current_number)
                        continue
                    part = find_longest_substring(str(current_number))
                    removed = str(current_number).replace(part, '')
                    if removed == "":
                        invalid_ids.append(current_number)

    return sum(invalid_ids)

def main() -> None:
    puzzle = Puzzle(year=2025, day=2)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.split(",")


    # ic(part1_solve(example_data))
    # ic(part1_solve(puzzle.input_data.split(",")))
    #
    ic(part2_solve(example_data))
    ic(part2_solve(puzzle.input_data.split(",")))

if __name__ == '__main__':
    main()
