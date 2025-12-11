import math
from collections import Counter
from operator import mul
from typing import Tuple
from urllib.response import addinfo

import more_itertools
import networkx
import networkx as nx
import shapely
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

from networkx.algorithms.simple_paths import all_simple_paths
from shapely import LineString
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve
from shapely.geometry.polygon import Polygon, LinearRing
from scipy import ndimage
from heapq import heappop, heappush
from dataclasses import dataclass, field
from itertools import pairwise

load_dotenv()


@dataclass
class ServerNode:
    id: str
    outputs: list[str]



def parse_paths(input_lines: list[str]) -> list[ServerNode]:
    nodes = []
    end_node_ids = []
    current_end_node_id = 0
    for line in input_lines:
        segments = line.split(":")
        output_nodes = []
        for item in segments[1].strip().split(" "):
            current = item.strip()
            if current == "you":
                continue
            if current == "out":
                current = f"{current}{current_end_node_id}"
                end_node_ids.append(current)
                current_end_node_id += 1
            output_nodes.append(f"{current}")
        new_server_node = ServerNode(segments[0].strip(), output_nodes)
        nodes.append(new_server_node)
    return nodes, end_node_ids


def part1_solve(input_lines: list[str]) -> int:
    parsed_nodes, end_nodes = parse_paths(input_lines)

    start_node = None
    G = nx.DiGraph()
    current_output_id = 0
    for node in parsed_nodes:
        G.add_node(node.id, id=node.id)
        if node.id == "you":
            start_node = node.id
        for output in node.outputs:
            if output not in G.nodes:
                G.add_node(output, id=output)
            G.add_edge(node.id, output)
    paths = []
    for end_node in end_nodes:
        for path in all_simple_paths(G, start_node, end_node):
            ic(path)
            paths.append(tuple(path))
    return len(paths)

def part2_solve(input_lines: list[str], begin_range: int, end_range: int) -> int:
    pass



def main() -> None:
    puzzle = Puzzle(year=2025, day=11)
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
