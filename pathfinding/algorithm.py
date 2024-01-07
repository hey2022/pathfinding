from pathfinding.graph import *
from collections import deque


# from enum import Enum, auto

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


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
    if node in graph.walls or node in explored:
        return False
    return True


def reconstruct_path(
    node: tuple[int, int], came_from: dict[tuple[int, int], tuple[int, int]]
) -> list[tuple[int, int]]:
    total_path = [node]
    while node in came_from:
        node = came_from[node]
        total_path.insert(0, node)
    return total_path


def bfs(graph: Graph) -> List[Tuple[int, int]]:
    queue = deque()
    explored = set()
    came_from = {}
    explored.add(graph.source)
    queue.append(graph.source)
    while queue:
        node = queue.popleft()
        if node == graph.target:
            return reconstruct_path(node, came_from)
        for neighbour in neighbours(node):
            if valid_node(graph, neighbour, explored):
                graph.draw_node(neighbour, 0x565656)
                explored.add(neighbour)
                came_from[neighbour] = node
                queue.append(neighbour)

    # heapq.heappush(open_set, ((0, 0), start))
    # came_from = {}
    # g_score = {start: 0}
    # f_score = {start: self.h_cost(start, goal)}
    #     while len(open_set) > 0:
    #         current = heapq.heappop(open_set)[1]
    #         if current == goal:
    #             return self.reconstruct_path(came_from, current)
    #         neighbors = [(current[0], current[1] - game.block), (current[0] + game.block, current[1]),
    #                      (current[0], current[1] + game.block), (current[0] - game.block, current[1])]
    #         for neighbor in neighbors:
    #             if self.valid(neighbor):
    #                 new_g = g_score.get(current) + game.block
    #                 if new_g < g_score.get(neighbor, math.inf):
    #                     came_from[neighbor] = current
    #                     g_score[neighbor] = new_g
    #                     f_score[neighbor] = new_g + self.h_cost(neighbor, goal)
    #                     if ((f_score[neighbor], self.h_cost(neighbor, goal)), neighbor) not in open_set:
    #                         heapq.heappush(open_set, ((f_score[neighbor], self.h_cost(neighbor, goal)), neighbor))


# def dfs(graph: Graph):
#     if len(graph.events) == 0 or graph.source is None:
#         return -1
#     event = graph.events.pop()
#     if not graph.avaliable(event.pos) and event.typ == EventType.VISIT:
#         return 0
#     if event.typ == EventType.LEAVE:
#         graph.draw_visited(event.pos)
#     else:
#         if event.pos == graph.target:
#             graph.init_events()
#             return -1
#         graph.draw_visiting(event.pos)
#         graph.events.append(Event(event.pos, EventType.LEAVE))
#         (x, y) = event.pos
#         graph.visited[y][x] = True
#         for dx, dy in DIRECTIONS:
#             newpos = (x + dx, y + dy)
#             graph.events.append(Event(newpos, EventType.VISIT))
#     return 1


# class EventType(Enum):
#     VISIT = auto()
#     LEAVE = auto()


# class Event:
#     def __init__(self, pos: tuple[int, int], typ: EventType):
#         self.pos = pos
#         self.typ = typ


# class Matrix:
#     def __init__(self, columns: int, rows: int):
#         self.columns = columns
#         self.rows = rows
#         self.reset()

#     def reset(self):
#         self.source = None
#         self.target = None
#         self.init_walls()
#         self.init_visited()
#         self.init_events()

#     def init_walls(self):
#         self.walls = [[False for _ in range(self.columns)] for _ in range(self.rows)]

#     def init_visited(self):
#         self.visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]

#     def init_events(self):
#         self.events = []

# def draw_visited(self, index_pos):
#     pos = self.index_to_pixel(index_pos)
#     self.draw_at_index(0xA7ABC3, pos)

# def draw_visiting(self, index_pos):
#     pos = self.index_to_pixel(index_pos)
#     self.draw_at_index(0x99FFCC, pos)
