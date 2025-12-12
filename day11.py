import functools
import math
from collections import Counter
from operator import mul
from typing import Tuple
from urllib.response import addinfo

import more_itertools
import networkx
import networkx as nx
import pydapper
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
from networkx.readwrite import adjlist
from networkx.readwrite.json_graph.adjacency import adjacency_data
from shapely import LineString
from sympy import symbols, Function, Eq, Piecewise
from sympy import solve
from shapely.geometry.polygon import Polygon, LinearRing
from scipy import ndimage
from heapq import heappop, heappush
from dataclasses import dataclass, field
from itertools import pairwise
from frozendict import frozendict

load_dotenv()


@dataclass
class ServerNode:
    id: str
    outputs: list[str]


def parse_paths(input_lines: list[str], unique_out: bool = True) -> list[ServerNode]:
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
                if unique_out:
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
            paths.append(tuple(path))
    return len(paths)


@dataclass
class Result:
    target: str
    destination: str
    Path: str


@cache
def all_depth_first_paths(input_graph: frozendict, start_node: str, end_node: str):
    if start_node[:3] == end_node[:3]:
        return 1
    paths = 0
    for child_node in input_graph.get(start_node, []):
        paths += all_depth_first_paths(input_graph, child_node, end_node)
    return paths


# Tried sqlite database
# Tried networkx
# Moved to frozendict with frozenset inside to make it all cacheable by hashing for Depth First Search
def part2_solve(input_lines: list[str]) -> int:
    adjacency_data = {}
    for entry in input_lines:
        node_id, outputs = entry.split(":")
        adjacency_data[node_id] = frozenset(outputs.strip().split())

    locked_adjacency = frozendict(adjacency_data)
    srv_fft_count = all_depth_first_paths(locked_adjacency, "svr", "fft")
    fft_dac_count = all_depth_first_paths(locked_adjacency, "fft", "dac")
    dac_out_count = all_depth_first_paths(locked_adjacency, "dac", "out")
    srv_fft_dac_count = srv_fft_count * fft_dac_count * dac_out_count

    srv_dac_count = all_depth_first_paths(locked_adjacency, "svr", "dac")
    dac_fft_count = all_depth_first_paths(locked_adjacency, "dac", "fft")
    fft_out_count = all_depth_first_paths(locked_adjacency, "fft", "out")
    srv_dac_fft_count = srv_dac_count * dac_fft_count * fft_out_count

    return srv_fft_dac_count + srv_dac_fft_count

    # dsn = "sqlite+sqlite3://my.db"
    #
    # with pydapper.connect("sqlite://pydapper.db") as commands:
    #     commands.execute("CREATE TABLE IF NOT EXISTS connections (target TEXT, destination TEXT);")
    #     commands.execute("DELETE FROM connections;")
    #
    #     for node in parsed_nodes:
    #         start_node = node.id
    #         for output in node.outputs:
    #             commands.execute("insert into connections values (?target?, ?destination?)", param={"target": start_node, "destination": output})
    #     print("d")


#         results = commands.query("""
# WITH DFS AS (
# 	SELECT target, destination, CAST(destination AS TEXT) AS Path
# 	FROM connections
# 	WHERE target = 'svr' -- Starting node
# 	UNION ALL
# 	SELECT g.target, g.destination, d.Path || ',' || g.destination as Path
# 	FROM connections g
# 	INNER JOIN DFS d ON g.target = d.destination
# )
# SELECT target, destination, Path
# FROM DFS
# WHERE PATH LIKE '%out%' AND PATH LIKE '%fft%' and PATH LIKE '%dac%'
# ORDER BY Path;
#         """, model=Result)
#         print(results)

# -- CAST(d.Path + ',' + CAST(g.destination AS TEXT) AS TEXT)


# create_table("CREATE TABLE contacts (contact_id INTEGER PRIMARY KEY, phone TEXT NOT NULL UNIQUE);")

# rowcount = commands.execute(
#     "insert into task (description, due_date, owner_id) values (?description?, ?due_date?, ?owner_id?)",
#     param={"description": "An insert example", "due_date": datetime.date.today(), "owner_id": 1},
# )
# Nope

# start_node = None
# G = nx.DiGraph()
# for node in parsed_nodes:
#     G.add_node(node.id, id=node.id)
#     if node.id == "svr":
#         start_node = node.id
#     for output in node.outputs:
#         if output not in G.nodes:
#             G.add_node(output, id=output)
#         G.add_edge(node.id, output)
#
# A = nx.to_scipy_sparse_array(G).toarray()

# paths = []
#
# must_contain = set(["fft", "dac"])
#
# ic(f'Total nodes: {len(end_nodes)}')
#
# unique_paths = set()
#
# # srv_fft = set()
# # fft_dac = set()
# # dac_out = set()
# #
# # srv_dac = set()
# # dac_fft = set()
# # fft_out = set()
#
# paths = 0
# for dac_fft in all_simple_paths(G, "fft", "dac"):
#     paths += 1
# for fft_dac in all_simple_paths(G, "dac", "fft"):
#     paths += 1
#
#
# Nope
# srv_fft_dac_count = 0
# for end_node in end_nodes:
#     for srv_fft in all_simple_paths(G, start_node, "fft"):
#         fft = 1
#         for dac_fft in all_simple_paths(G, "fft", "dac"):
#             dac = 1
#             for dac_out in all_simple_paths(G, "dac", end_node):
#                if fft == 1 and dac == 1:
#                    srv_fft_dac_count += 1
# srv_dac_fft_count = 0
# for end_node in end_nodes:
#     for srv_dac in all_simple_paths(G, start_node, "dac"):
#         dac = 1
#         for dac_fft in all_simple_paths(G, "dac", "fft"):
#             fft = 1
#             for fft_out in all_simple_paths(G, "fft", end_node):
#                 if fft == 1 and dac == 1:
#                     srv_dac_fft_count += 1
#
#     # srv_dac_fft_count = 0
#     # for srv_fft in all_simple_paths(G, start_node, "dac"):
#     #     for dac_fft in all_simple_paths(G, "dac", "fft"):
#     #         for dac_out in all_simple_paths(G, "fft", end_node):
#     #            srv_dac_fft_count += 1
# return srv_dac_fft_count + srv_fft_dac_count


def main() -> None:
    puzzle = Puzzle(year=2025, day=11)
    data = puzzle.input_data
    example = puzzle.examples.pop()
    example_data = example.input_data.splitlines()

    ic(part1_solve(example_data))
    ic(part1_solve(puzzle.input_data.splitlines()))

    example_data2 = ["svr: aaa bbb",
                     "aaa: fft",
                     "fft: ccc",
                     "bbb: tty",
                     "tty: ccc",
                     "ccc: ddd eee",
                     "ddd: hub",
                     "hub: fff",
                     "eee: dac",
                     "dac: fff",
                     "fff: ggg hhh",
                     "ggg: out",
                     "hhh: out"]

    ic(part2_solve(example_data2))
    ic(part2_solve(puzzle.input_data.splitlines()))


if __name__ == '__main__':
    main()
