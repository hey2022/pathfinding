from typing import Callable
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

EXPLORED_COLOR = 0x565656


class Result:
    path = []
    explored = set()

    def __init__(self) -> None:
        pass


def get_neighbours(graph: Graph, node: tuple[int, int]) -> list[tuple[int, int]]:
    next_nodes = [
        (node[0] + direction[0], node[1] + direction[1]) for direction in DIRECTIONS
    ]
    valid_nodes = list(
        filter(
            lambda node: graph.is_empty_node(node) or node == graph.target, next_nodes
        )
    )
    return valid_nodes


def reconstruct_path(
    node: tuple[int, int], came_from: dict[tuple[int, int], tuple[int, int]]
) -> list[tuple[int, int]]:
    path = [node]
    while node in came_from:
        node = came_from[node]
        path.insert(0, node)
    return path


def manhattan_distance(node: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(target[0] - node[0]) + abs(target[1] - node[1])


def euclidian_distance(node: tuple[int, int], target: tuple[int, int]) -> int:
    return ((target[0] - node[0]) ** 2 + (target[1] - node[1]) ** 2) ** 0.5


def a_star_manhattan_distance(graph: Graph) -> Result:
    return a_star(graph, manhattan_distance)


def a_star_euclidian_distance(graph: Graph) -> Result:
    return a_star(graph, euclidian_distance)


def a_star(graph: Graph, heuristic: Callable) -> Result:
    result = Result()
    explored = set()
    came_from = {}
    cost = {graph.source: 0}

    priority_queue = []
    heapq.heappush(
        priority_queue, (heuristic(graph.source, graph.target), graph.source)
    )

    while priority_queue:
        node = heapq.heappop(priority_queue)[1]
        explored.add(node)

        if node == graph.target:
            result.path = reconstruct_path(node, came_from)
            result.explored = explored
            return result
        if graph.is_empty_node(node):
            pygame.display.update(graph.draw_node(node, EXPLORED_COLOR))

        for neighbour in get_neighbours(graph, node):
            new_cost = cost[node] + 1
            if new_cost < cost.get(neighbour, math.inf):
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
    result.explored = explored
    return result


def bfs(graph: Graph) -> Result:
    result = Result()
    explored = set()
    came_from = {}

    queue = deque()
    queue.append(graph.source)

    while queue:
        node = queue.popleft()

        if node == graph.target:
            result.path = reconstruct_path(node, came_from)
            result.explored = explored
            return result
        if graph.is_empty_node(node):
            pygame.display.update(graph.draw_node(node, EXPLORED_COLOR))

        for neighbour in get_neighbours(graph, node):
            if neighbour not in explored:
                explored.add(neighbour)
                came_from[neighbour] = node
                queue.append(neighbour)
    result.explored = explored
    return result


def dfs(graph: Graph) -> Result:
    result = Result()
    explored = set()
    came_from = {}

    queue = deque()
    queue.append(graph.source)

    while queue:
        node = queue.pop()
        explored.add(node)

        if node == graph.target:
            result.path = reconstruct_path(node, came_from)
            result.explored = explored
            return result
        if graph.is_empty_node(node):
            pygame.display.update(graph.draw_node(node, EXPLORED_COLOR))

        for neighbour in get_neighbours(graph, node):
            if neighbour not in explored:
                came_from[neighbour] = node
                queue.append(neighbour)
    result.explored = explored
    return result


def path_route(
    graph: Graph, gap: int, node: tuple[int, int], to: tuple[int, int]
) -> pygame.Rect:
    (x, y) = graph.index_to_pos(node)
    (dy, dx) = (node[0] - to[0], node[1] - to[1])
    match (dx):
        case 1:
            route_x = x
        case 0:
            route_x = x + gap
        case -1:
            route_x = x + graph.block_size - gap
    match (dy):
        case 1:
            route_y = y
        case 0:
            route_y = y + gap
        case -1:
            route_y = y + graph.block_size - gap
    if dx == 0:
        return pygame.Rect(route_x, route_y, graph.block_size - gap * 2, gap)
    else:
        return pygame.Rect(route_x, route_y, gap, graph.block_size - gap * 2)


def draw_path(
    graph: Graph,
    gap: int,
    color: int,
    pre: tuple[int, int],
    node: tuple[int, int],
    next: tuple[int, int],
):
    (x, y) = graph.index_to_pos(node)
    width = graph.block_size - gap * 2
    center = pygame.Rect(x + gap, y + gap, width, width)
    pygame.draw.rect(graph.surface, color, center)
    pygame.draw.rect(graph.surface, color, path_route(graph, gap, node, pre))
    pygame.draw.rect(graph.surface, color, path_route(graph, gap, node, next))
