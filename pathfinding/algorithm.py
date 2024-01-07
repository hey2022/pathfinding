from pathfinding.graph import *
from collections import deque


DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


class Result:
    def __init__(
        self, path: list[tuple[int, int]], explored: set[tuple[int, int]]
    ) -> None:
        self.path = path
        self.explored = explored


def get_neighbours(node: tuple[int, int]) -> list[tuple[int, int]]:
    next_nodes = [
        (node[0] + direction[0], node[1] + direction[1]) for direction in DIRECTIONS
    ]
    return next_nodes


def valid_node(
    graph: Graph, node: tuple[int, int], explored: set[tuple[int, int]]
) -> bool:
    (row, column) = node
    if row < 0 or row >= graph.rows or column < 0 or column >= graph.columns:
        return False
    if node in graph.walls or node in explored or node == graph.source:
        return False
    return True


def reconstruct_path(
    node: tuple[int, int], came_from: dict[tuple[int, int], tuple[int, int]]
) -> list[tuple[int, int]]:
    total_path = [node]
    while node in came_from:
        node = came_from[node]
        total_path.insert(0, node)
    return total_path[1::]


def bfs(graph: Graph) -> Result:
    queue = deque()
    explored = set()
    came_from = {}
    queue.append(graph.source)
    while queue:
        node = queue.popleft()
        neighbours = get_neighbours(node)
        for neighbour in neighbours:
            if valid_node(graph, neighbour, explored):
                if neighbour == graph.target:
                    return Result(reconstruct_path(node, came_from), explored)
                graph.draw_node(neighbour, 0x565656)
                explored.add(neighbour)
                came_from[neighbour] = node
                queue.append(neighbour)
        graph.display_nodes(neighbours)
    return Result([], explored)


