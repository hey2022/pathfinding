import pygame
from typing import Callable
from pathfinding.graph import Graph
from collections import deque
import math
import heapq

# directions for traversal
DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

# color of explored node
EXPLORED_COLOR = 0x565656


# result of pathfinding algorithm that contains the explored nodes and path found
class Result:
    path = []
    explored = set()

    # empty constructor
    def __init__(self) -> None:
        pass


# get neighbors of current node that can be traversed
def get_neighbors(graph: Graph, node: tuple[int, int]) -> list[tuple[int, int]]:
    neighbors = [
        next_node
        for direction in DIRECTIONS
        if (next_node := (node[0] + direction[0], node[1] + direction[1]))
        and graph.is_empty_node(next_node)
        or next_node == graph.target
    ]
    return neighbors


# traverses from the target node back to source node by going to its parent node
def reconstruct_path(
    node: tuple[int, int], came_from: dict[tuple[int, int], tuple[int, int]]
) -> list[tuple[int, int]]:
    path = [node]
    while node in came_from:
        node = came_from[node]
        path.insert(0, node)
    return path


# calculate Manhattan distance between a node and the target node
def manhattan_distance(node: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(target[0] - node[0]) + abs(target[1] - node[1])


# calculate Euclidean distance between a node and the target node
def euclidian_distance(node: tuple[int, int], target: tuple[int, int]) -> int:
    return ((target[0] - node[0]) ** 2 + (target[1] - node[1]) ** 2) ** 0.5


# A* pathfinding algorithm with Manhattan distance heuristic
def a_star_manhattan_distance(graph: Graph) -> Result:
    return a_star(graph, manhattan_distance)


# A* pathfinding algorithm with Euclidean distance heuristic
def a_star_euclidian_distance(graph: Graph) -> Result:
    return a_star(graph, euclidian_distance)


# runs A* on the graph and returns its results
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
            # visualize explored node
            pygame.display.update(graph.draw_node(node, EXPLORED_COLOR))

        for neighbor in get_neighbors(graph, node):
            # all edge weights are 1
            new_cost = cost[node] + 1
            if new_cost < cost.get(neighbor, math.inf):
                came_from[neighbor] = node
                cost[neighbor] = new_cost
                if (
                    new_cost + heuristic(neighbor, graph.target),
                    neighbor,
                ) not in priority_queue:
                    heapq.heappush(
                        priority_queue,
                        (new_cost + heuristic(neighbor, graph.target), neighbor),
                    )
    result.explored = explored
    return result


# runs BFS on the graph and returns its results
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
            # visualize explored node
            pygame.display.update(graph.draw_node(node, EXPLORED_COLOR))

        for neighbor in get_neighbors(graph, node):
            if neighbor not in explored:
                explored.add(neighbor)
                came_from[neighbor] = node
                queue.append(neighbor)
    result.explored = explored
    return result


# runs DFS on the graph and returns its results
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
            # visualize explored node
            pygame.display.update(graph.draw_node(node, EXPLORED_COLOR))

        for neighbor in get_neighbors(graph, node):
            if neighbor not in explored:
                came_from[neighbor] = node
                queue.append(neighbor)
    result.explored = explored
    return result


# draws the path from the source node to the target node while add a gap between adjacent non-connected nodes
def draw_path(
    graph: Graph,
    path: list[tuple[int, int]],
    color: int,
):
    # the gap on each side from the center of the node
    gap = graph.node_size // 4
    for i in range(1, len(path) - 1):
        (pixel_x, pixel_y) = graph.node_to_pixel(path[i])
        width = graph.node_size - gap * 2

        # draw center of node
        center = pygame.Rect(pixel_x + gap, pixel_y + gap, width, width)
        pygame.draw.rect(graph.surface, color, center)

        # draw connection from node to previous node
        pygame.draw.rect(
            graph.surface, color, draw_path_connection(graph, gap, path[i], path[i - 1])
        )

        # draw connection from node to next node
        pygame.draw.rect(
            graph.surface, color, draw_path_connection(graph, gap, path[i], path[i + 1])
        )
    graph.display_nodes(path)


# returns a rect for the connecting edge from the node to the adjacent node
def draw_path_connection(
    graph: Graph,
    gap: int,
    current_node: tuple[int, int],
    adjacent_node: tuple[int, int],
) -> pygame.Rect:
    (pixel_x, pixel_y) = graph.node_to_pixel(current_node)
    (dx, dy) = (
        adjacent_node[0] - current_node[0],
        adjacent_node[1] - current_node[1],
    )
    match (dx, dy):
        case (1, 0):
            # right edge
            pos_x = pixel_x + graph.node_size - gap
            pos_y = pixel_y + gap
            width = gap
            height = graph.node_size - gap * 2
        case (0, 1):
            # bottom edge
            pos_x = pixel_x + gap
            pos_y = pixel_y + graph.node_size - gap
            width = graph.node_size - gap * 2
            height = gap
        case (-1, 0):
            # left edge
            pos_x = pixel_x
            pos_y = pixel_y + gap
            width = gap
            height = graph.node_size - gap * 2
        case (0, -1):
            # top edge
            pos_x = pixel_x + gap
            pos_y = pixel_y
            width = graph.node_size - gap * 2
            height = gap
    return pygame.Rect(pos_x, pos_y, width, height)
