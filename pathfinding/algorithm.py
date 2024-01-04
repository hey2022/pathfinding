from pathfinding.graph import *

# from enum import Enum, auto

DIRECTIONS = [
    [0, -1],
    [1, 0],
    [0, 1],
    [-1, 0],
]


def dfs(graph: Graph):
    if len(self.events) == 0 or self.source is None:
        return -1
    event = self.events.pop()
    if not self.avaliable(event.pos) and event.typ == EventType.VISIT:
        return 0
    if event.typ == EventType.LEAVE:
        graph.draw_visited(event.pos)
    else:
        if event.pos == self.target:
            self.init_events()
            return -1
        graph.draw_visiting(event.pos)
        self.events.append(Event(event.pos, EventType.LEAVE))
        (x, y) = event.pos
        self.visited[y][x] = True
        for dx, dy in DIRECTIONS:
            newpos = (x + dx, y + dy)
            self.events.append(Event(newpos, EventType.VISIT))
    return 1


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

#     def avaliable(self, pos):
#         (x, y) = pos
#         if x < 0 or y < 0 or x > self.rows - 1 or y > self.columns - 1:
#             return False
#         if self.walls[y][x] or self.visited[y][x]:
#             return False
#         return True

#     def add_wall(self, pos: tuple[int, int]):
#         (x, y) = pos
#         if self.walls[y][x]:
#             return False
#         self.walls[y][x] = True
#         return True

# def draw_visited(self, index_pos):
#     pos = self.index_to_pixel(index_pos)
#     self.draw_at_index(0xA7ABC3, pos)

# def draw_visiting(self, index_pos):
#     pos = self.index_to_pixel(index_pos)
#     self.draw_at_index(0x99FFCC, pos)
