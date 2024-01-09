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
        if node == graph.target:
            return Result(
                reconstruct_path(came_from[node], came_from), came_from.keys()
            )
        neighbours = get_neighbours(node)
        for neighbour in neighbours:
            if valid_node(graph, neighbour):
                new_cost = cost[node] + 1
                if new_cost < cost.get(neighbour, math.inf):
                    if node != graph.source and neighbour not in came_from:
                        pygame.display.update(graph.draw_node(node, 0x565656))
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
            pygame.display.update(graph.draw_node(node, 0x565656))

        explored.add(node)
        neighbours = get_neighbours(node)

        for neighbour in neighbours:
            if valid_node(graph, neighbour) and neighbour not in explored:
                came_from[neighbour] = node
                queue.append(neighbour)
    return Result([], explored)


def path_route(graph: Graph, gap: int, node: tuple[int, int], to: tuple[int, int]) -> pygame.Rect:
    (x, y) = graph.index_to_pos(node)
    (dy, dx) = (node[0] - to[0], node[1] - to[1])
    match(dx):
        case 1:
            route_x = x
        case 0:
            route_x = x + gap
        case -1:
            route_x = x + graph.block_size - gap
    match(dy):
        case 1:
            route_y = y
        case 0:
            route_y = y + gap
        case -1:
            route_y = y + graph.block_size - gap
    if dx == 0:
        return pygame.Rect(route_x, route_y, graph.block_size - gap*2, gap)
    else:
        return pygame.Rect(route_x, route_y, gap, graph.block_size - gap*2)


def draw_path(graph: Graph, gap: int, color: int, pre: tuple[int, int], node: tuple[int, int], next: tuple[int, int]):
    (x, y) = graph.index_to_pos(node)
    width = graph.block_size - gap * 2
    center = pygame.Rect(x + gap, y + gap, width, width)
    pygame.draw.rect(graph.surface, color, center)
    pygame.draw.rect(graph.surface, color, path_route(graph, gap, node, pre))
    pygame.draw.rect(graph.surface, color, path_route(graph, gap, node, next))
