from collections import deque
from dataclasses import dataclass, field

from aocd.models import Puzzle
from dotenv import load_dotenv
from icecream import ic

load_dotenv()



@dataclass
class LightInputs:
    input_data: str
    target_pattern: int = 0
    toggle_commands: list[list[int]] = field(default_factory=list)
    jolts: list[int] = field(default_factory=list)
    dest_length: int = 0

    def initialize(self):
        temp = self.input_data.replace("]", '|')
        temp = temp.replace("{", '|')
        segments = temp.split("|")
        target_light_input = segments[0].replace("[", '').strip()
        command_input = segments[1].strip()
        jolt_input = segments[2].replace("}", '').strip()

        target_light_input = target_light_input.strip()
        self.dest_length = len(target_light_input)

        target_light_input = target_light_input.replace("#", "1").strip()
        target_light_input = target_light_input.replace(".", "0").strip()
        self.target_pattern = int(target_light_input[::-1], 2)
        for command in command_input.split(" "):
            current = command.replace("(", "").replace(")", "").strip()
            self.toggle_commands.append([int(index) for index in current.split(",")])
        for jolt in jolt_input.split(","):
            self.jolts.append(int(jolt))

@dataclass
class LightMachine:
    current_lights: int = 0
    commands: list[list[int]] = field(default_factory=list)
    last_command: list[int] = field(default_factory=list)


def parse_line_input(input_line) -> LightInputs:
    inputs = LightInputs(input_line)
    inputs.initialize()
    return inputs


def part1_solve(input_lines: list[str]) -> None:
    light_inputs = [parse_line_input(line) for line in input_lines]
    completed_lights = {}
    for light_index, light_input in enumerate(light_inputs):
        runs = 0
        machine_paths = deque([(0, 0)])
        visited = {0}
        while len(machine_paths) > 0:
            in_progress_lights, commands = machine_paths.popleft()
            if light_input.target_pattern == in_progress_lights:
                completed_lights[light_index] = commands
                break
            runs += 1
            for command in light_input.toggle_commands:
                buttons = ['0'] * light_input.dest_length
                for index in command:
                    buttons[index] = '1'
                number_mask = "".join(buttons[::-1])
                masking_number = int(number_mask, 2)
                current_lights = in_progress_lights ^ masking_number
                if current_lights not in visited:
                    visited.add(current_lights)
                    machine_paths.append((current_lights, commands + 1))

    totals = 0
    for light_index, steps in completed_lights.items():
        totals += steps

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