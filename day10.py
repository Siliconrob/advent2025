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
from itertools import cycle, combinations, repeat
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


# @dataclass
# class LightPattern:
#     pattern_length: list[int]
#
#     def current_status(self) -> list[int]:
#         return self.pattern_length


@dataclass
class LightInputs:
    input_data: str
    target_pattern: list[int] = field(default_factory=list)
    toggle_commands: list[list[int]] = field(default_factory=list)
    jolts: list[int] = field(default_factory=list)

    def initialize(self):
        temp = self.input_data.replace("]", '|')
        temp = temp.replace("{", '|')
        segments = temp.split("|")
        target_light_input = segments[0].replace("[", '').strip()
        command_input = segments[1].strip()
        jolt_input = segments[2].replace("}", '').strip()
        for index, light in enumerate(target_light_input):
            if target_light_input[index] == "#":
                self.target_pattern.append(True)
            else:
                self.target_pattern.append(False)
        for command in command_input.split(" "):
            current = command.replace("(", "").replace(")", "").strip()
            self.toggle_commands.append([int(index) for index in current.split(",")])
        for jolt in jolt_input.split(","):
            self.jolts.append(int(jolt))





@dataclass
class LightingDetails:
    input_data: str
    current_lights = set()
    target_lights = set()


    def reset_lights(self):
        self.current_lights = set()


    def initialize_lights(self):
        start_pattern = self.input_data.split(" ")[0]
        start_pattern = start_pattern.replace("[", "")
        start_pattern = start_pattern.replace("]", "")
        self.current_lights = set()
        self.target_lights = set()
        for current_index, current in enumerate(start_pattern.strip()):
            if current == "#":
                self.target_lights.add(current_index)

    def parse(self) -> list[list[int]]:

        temp = self.input_data.replace("]", '|')
        temp = temp.replace("{", '|')

        segments = temp.split("|")
        target_lights = segments[0].replace("[", '').strip()
        commands = segments[1].strip()
        jolts = segments[2].replace("}", '').strip()




        toggle_list = self.input_data.split(" ")[1]
        toggle_operations = toggle_list.strip().split(" ")
        command_set = []
        for toggle_operation in toggle_operations:
            toggle_command = toggle_operation.replace("(", "").replace(")", "")
            commands = [int(toggle_index) for toggle_index in toggle_command.split(",")]
            command_set.append(commands)
        return command_set


    def joltage(self) -> list[int]:
        jolt_list = self.input_data.split(" ")[2]
        jolt_list = jolt_list.replace("{", "").replace("}", "")
        return [int(jolt) for jolt in jolt_list.strip().split(",")]

@dataclass
class LightMachine:
    current_lights: dict[int, bool] = field(default_factory=dict)
    commands: list[list[int]] = field(default_factory=list)
    last_command: list[int] = field(default_factory=list)

    def initialize(self, light_count: int) -> None:
        for index in range(light_count):
            self.current_lights[index] = False

    def run_command(self, toggles: list[int]) -> None:
        for index in toggles:
            self.current_lights[index] = not self.current_lights[index]
        self.commands.append(toggles)
        self.last_command = toggles




def parse_line_input(input_line) -> LightInputs:
    inputs = LightInputs(input_line)
    inputs.initialize()
    return inputs




def part1_solve(input_lines: list[str]) -> None:
    light_inputs = [parse_line_input(line) for line in input_lines]

    completed_lights = {}

    for light_index, light_input in enumerate(light_inputs):
        target_lights = light_input.target_pattern

        machine_paths = deque()
        for index in range(len(light_input.toggle_commands)):
            new_machine = LightMachine()
            new_machine.initialize(len(target_lights))
            machine_paths.append(new_machine)

        searching = True
        commands = cycle(light_input.toggle_commands)
        while searching:
            command = next(commands)
            current_machine = machine_paths.popleft()
            if current_machine.last_command == command:
                command = next(commands)
            current_machine.run_command(command)
            #ic(current_machine)
            if all(x == y for x, y in zip(current_machine.current_lights.values(), target_lights)):
                completed_lights[light_index] = current_machine
                break
            else:
                machine_paths.append(current_machine)

    totals = 0
    for completed_light in completed_lights.values():
        totals += len(completed_light.commands)

    return totals



def part2_solve(input_lines: list[str], begin_range: int, end_range: int) -> int:
    pass


def main() -> None:
    puzzle = Puzzle(year=2025, day=10)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    ic(part1_solve(example_data))
    ic(part1_solve(puzzle.input_data.splitlines()))
    #
    # ic(part2_solve(example_data, 20, 50))
    # ic(part2_solve(puzzle.input_data.splitlines(), 1_400_000_000, 1_500_000_000))



if __name__ == '__main__':
    main()
