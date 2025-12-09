import math
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
from more_itertools.recipes import flatten, pairwise, unique
from itertools import cycle, combinations
import copy
from functools import reduce, cache
from collections import deque
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve
from shapely.geometry.polygon import Polygon, LinearRing
from scipy import ndimage
from heapq import heappop, heappush
from dataclasses import dataclass, field
from itertools import pairwise

load_dotenv()


@dataclass
class Location:
    x: int
    y: int
    z: int

    def key(self, other: Location) -> str:
        return f'{self.x},{self.y},{self.z}-{other.x},{other.y},{other.z}'

    def distance(self, other: Location) -> float:
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2) + math.pow(self.z - other.z, 2))


def parse_locations(input_lines: list[str]) -> list[Location]:
    locations = []
    for line in input_lines:
        x, y, z = line.split(',')
        locations.append(Location(int(x), int(y), int(z)))
    return locations


def part1_solve(input_lines: list[str], connection_runs: int) -> int:
    all_locations = parse_locations(input_lines)

    distances = {}

    items = len(all_locations)
    for i in range(items):
        for j in range(i + 1, items):
            distances[frozenset([i, j])] = all_locations[i].distance(all_locations[j])

    sorted_by_distances = sorted(distances.items(), key=lambda x: x[1])
    run_times = 0
    connections = {i: {i} for i in range(len(sorted_by_distances))}
    for id, distance in dict(sorted_by_distances).items():
        if run_times > connection_runs:
            break
        run_times += 1
        start, end = id
        matched_connections = connections[start] | connections[end]
        for match in matched_connections:
            connections[match] = matched_connections

        # Nope doesn't work on full data set
        # items = pair.split('-')
        # next_connection = set([items[0], items[1]])
        # if len(connections) == 0:
        #     connections[0] = next_connection
        #     continue
        # new_circuit = 0
        # for id, junctions in connections.items():
        #     item1 = items[0] in junctions
        #     item2 = items[1] in junctions
        #     if item1 and item2:
        #         break
        #     if item1 == True or item2 == True:
        #         junctions.add(items[0])
        #         junctions.add(items[1])
        #         break
        #     else:
        #         new_circuit += 1
        # if new_circuit == len(connections):
        #     connections[len(connections)] = next_connection
    unique_components = {frozenset(z) for z in connections.values()}
    conn_sets = sorted([len(z) for z in unique_components], reverse=True)
    # conn_set_sizes = sorted([len(connection_set) for connection_set in connections.values()], reverse=True)[:3]
    return reduce(mul, conn_sets[:3])



def part2_solve(input_lines: list[str], connection_runs: int) -> int:
    all_locations = parse_locations(input_lines)
    distances = {}

    items = len(all_locations)
    for i in range(items):
        for j in range(i + 1, items):
            distances[frozenset([i, j])] = all_locations[i].distance(all_locations[j])

    sorted_by_distances = sorted(distances.items(), key=lambda x: x[1])
    connections = {i: {i} for i in range(len(sorted_by_distances))}

    run_times = 0
    for id, distance in dict(sorted_by_distances).items():
        if run_times > connection_runs:
            break
        run_times += 1
        start, end = id
        matched_connections = connections[start] | connections[end]
        for match in matched_connections:
            connections[match] = matched_connections

    sorted_by_distances = sorted(distances.items(), key=lambda x: x[1])
    all_connected = False
    last_merge_index_start = None
    last_merge_index_end = None

    # this is really slow (takes 20 minutes to run), brute force way to look at every single distance pair
    # and keep merging as a unique sets until all are connected
    # it sucks but just want to be done
    while not all_connected:
        connected_sets = set()
        for component in matched_connections.values():
            connected_sets.add(id(component))
        circuits = len(connected_sets)
        if circuits > 1:
            current_pair = sorted_by_distances.pop()
            start, end = current_pair[0]
            component = matched_connections[start] | matched_connections[end]
            for x in component:
                matched_connections[x] = component
                last_merge_index_start = start
                last_merge_index_end = end
        else:
            all_connected = True
    return all_locations[last_merge_index_start].x * all_locations[last_merge_index_end].x



def main() -> None:
    puzzle = Puzzle(year=2025, day=8)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    ic(part1_solve(example_data, 10))
    ic(part1_solve(puzzle.input_data.splitlines(), 1000))
    
    ic(part2_solve(example_data, 10))
    ic(part2_solve(puzzle.input_data.splitlines()))


if __name__ == '__main__':
    main()
