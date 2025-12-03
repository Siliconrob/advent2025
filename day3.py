from collections import Counter
from typing import Tuple
import more_itertools
import networkx
from aocd.models import Puzzle
from icecream import ic
from dotenv import load_dotenv

load_dotenv()


def part1_solve(batteries: list[str]) -> int:
    max_volts = []
    for battery in batteries:
        digits = [int(elem) for elem in list(battery)]
        first_digit = max(digits)
        first_pos = digits.index(first_digit)
        if first_pos < len(digits) - 1:
            second_digit = max(digits[first_pos + 1:])
        else:
            second_digit = first_digit
            first_digit = max(digits[:first_pos])
        max_volts.append(int(f'{first_digit}{second_digit}'))
    return sum(max_volts)



def part2_solve(batteries: list[str]) -> int:
    max_volts = []
    for battery in batteries:
        digits = [int(elem) for elem in list(battery)]

        while len(digits) > 12:
            removed = False
            for i in range(len(digits) - 1):
                if digits[i] < digits[i + 1]:
                    del digits[i]
                    removed = True
                    break
            if not removed:
                digits = digits[:-1]

        max_volts.append(int("".join(str(x) for x in digits)))

    return sum(max_volts)

def main() -> None:
    puzzle = Puzzle(year=2025, day=3)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    ic(part1_solve(example_data))
    ic(part1_solve(puzzle.input_data.splitlines()))

    ic(part2_solve(example_data))
    ic(part2_solve(puzzle.input_data.splitlines()))

if __name__ == '__main__':
    main()
