from pathfinding.graph import *
from collections import deque
import math
import heapq

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


def valid_node(graph: Graph, node: tuple[int, int]) -> bool:
    (row, column) = node
    if row < 0 or row >= graph.rows or column < 0 or column >= graph.columns:
        return False
    if node in graph.walls:
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


def heuristic(node: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(target[0] - node[0]) + abs(target[1] - node[1])


def a_star(graph: Graph) -> Result:
    priority_queue = []
    came_from = {}
    cost = {graph.source: 0}
    heapq.heappush(
        priority_queue, (heuristic(graph.source, graph.target), graph.source)
    )
    while priority_queue:
        node = heapq.heappop(priority_queue)[1]
        neighbours = get_neighbours(node)
        for neighbour in neighbours:
            if valid_node(graph, neighbour):
                if neighbour == graph.target:
                    return Result(reconstruct_path(node, came_from), came_from.keys())
                new_cost = cost[node] + 1
                if new_cost < cost.get(neighbour, math.inf):
                    graph.draw_node(neighbour, 0x565656)
                    came_from[neighbour] = node
                    cost[neighbour] = new_cost
                    if (
                        new_cost + heuristic(neighbour, graph.target),
                        neighbour,
                    ) not in priority_queue:
                        heapq.heappush(
                            priority_queue,
                            (new_cost + heuristic(neighbour, graph.target), neighbour),
                        )
        graph.display_nodes(neighbours)
    return Result([], came_from.keys())


def bfs(graph: Graph) -> Result:
    queue = deque()
    explored = set()
    came_from = {}
    queue.append(graph.source)
    explored.add(graph.source)
    while queue:
        node = queue.popleft()
        neighbours = get_neighbours(node)
        for neighbour in neighbours:
            if valid_node(graph, neighbour) and neighbour not in explored:
                if neighbour == graph.target:
                    return Result(reconstruct_path(node, came_from), explored)
                graph.draw_node(neighbour, 0x565656)
                explored.add(neighbour)
                came_from[neighbour] = node
                queue.append(neighbour)
        graph.display_nodes(neighbours)
    return Result([], explored)


def dfs(graph: Graph) -> Result:
    queue = deque()
    explored = set()
    came_from = {}
    queue.append(graph.source)
    explored.add(graph.source)
    while queue:
        node = queue.pop()

        if node == graph.target:
            return Result(reconstruct_path(came_from[node], came_from), explored)
        if node != graph.source and node not in explored:
            graph.draw_node(node, 0x565656)
            graph.display_nodes(list(node))

        explored.add(node)
        neighbours = get_neighbours(node)

        for neighbour in neighbours:
            if valid_node(graph, neighbour) and neighbour not in explored:
                came_from[neighbour] = node
                queue.append(neighbour)
    return Result([], explored)
