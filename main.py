import pygame
import sys
from enum import Enum, auto


class Graph:
    def __init__(self, cols: int, rows: int, block_size: int, grid_thickness: int):
        self.width = cols * block_size
        self.height = rows * block_size
        self.block_size = block_size
        self.grid_thickness = grid_thickness
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.matrix = Matrix(cols, rows)

    def pixel_to_index(self, pos: (int, int)):
        (x, y) = pos
        return (x // self.block_size, y // self.block_size)

    def index_to_pixel(self, pos: (int, int)):
        (x, y) = pos
        return (x * self.block_size, y * self.block_size)

    def create_node(self, pos: (int, int)) -> pygame.Rect:
        (x, y) = pos
        return pygame.Rect(
            x // self.block_size * self.block_size,
            y // self.block_size * self.block_size,
            self.block_size,
            self.block_size,
        )

    def draw_node(self, color: int, node: pygame.Rect) -> pygame.Rect:
        pygame.draw.rect(
            self.surface,
            color,
            node
        )
        pygame.display.update(node)
        return node

    def add_wall(self, pos):
        (x, y) = self.pixel_to_index(pos)
        if self.matrix.source == (x, y):
            self.matrix.source = None
        if self.matrix.target == (x, y):
            self.matrix.targer = None
        self.matrix.add_wall(self.pixel_to_index(pos))
        self.draw_node(FOREGROUND_COLOR, self.create_node(pos))

    def update_target(self, pos: (int, int)):
        (x, y) = self.pixel_to_index(pos)
        if self.matrix.target == (x, y):
            return
        self.matrix.walls[x][y] = False
        if self.matrix.target is not None:
            self.clear_node(self.index_to_pixel(self.matrix.target))
        self.matrix.target = (x, y)
        self.draw_node(0xFF0000, self.create_node(pos))

    def update_source(self, pos: (int, int)):
        (x, y) = self.pixel_to_index(pos)
        if self.matrix.source == (x, y):
            return
        self.matrix.walls[x][y] = False
        if self.matrix.source is not None:
            self.clear_node(self.index_to_pixel(self.matrix.source))
        self.matrix.source = (x, y)
        self.draw_node(0x99FFCC, self.create_node(pos))

    def clear_node(self, pos: (int, int)):
        (x, y) = self.pixel_to_index(pos)
        if self.matrix.source == (x, y):
            self.matrix.source = None
        if self.matrix.target == (x, y):
            self.matrix.targer = None
        self.matrix.walls[x][y] = False
        self.draw_node(BACKGROUND_COLOR, self.create_node(pos))

    def clear_board(self):
        self.matrix.reset()
        self.surface.fill(BACKGROUND_COLOR)
        pygame.display.update()


class EventType(Enum):
    VISIT = auto()
    LEAVE = auto()


class Event:
    def __init__(self, typ: EventType, pos: (int, int)):
        self.typ = typ
        self.pos = pos


class Matrix:
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.reset()

    def reset(self):
        self.source = None
        self.target = None
        self.init_walls()
        self.init_visited()
        self.init_events()

    def init_walls(self):
        self.walls = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def init_visited(self):
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def init_events(self):
        self.events = []

    def add_wall(self, pos: (int, int)):
        (x, y) = pos
        if self.walls[x][y]:
            return False
        self.walls[x][y] = True
        return True

    def dfs(self, graph: Graph):
        if self.events.empty():
            return
        event = self.events.top()
        self.events.pop()
        if event.typ == EventType.LEAVE:
            pass
        else:
            pass


def quit():
    pygame.quit()
    sys.exit()


def key_press(event: pygame.event.Event, key: int) -> bool:
    return event.type == pygame.KEYDOWN and event.key == key


def display_message(surface: pygame.Surface, message: str, x: int, y: int):
    text = FONT.render(message, True, 0xFFFFFFFF)
    rect = surface.blit(text, (x, y))
    pygame.display.update(rect)


def event_handler(
    graph: Graph,
    surface: pygame.Surface,
    clock: pygame.time.Clock,
    event: pygame.event.Event,
):
    if (
        event.type == pygame.QUIT
        or event.type == pygame.KEYDOWN
        and event.key == pygame.K_ESCAPE
    ):
        quit()

    if key_press(event, pygame.K_s):
        x, y = pygame.mouse.get_pos()
        graph.update_source((x, y))

    if key_press(event, pygame.K_t):
        x, y = pygame.mouse.get_pos()
        graph.update_target((x, y))

    if key_press(event, pygame.K_c):
        graph.clear_board()

    if key_press(event, pygame.K_RETURN):
        pass


def left_mouse_drag() -> bool:
    return pygame.mouse.get_pressed()[0]


def right_mouse_drag() -> bool:
    return pygame.mouse.get_pressed()[2]


def main():
    clock = pygame.time.Clock()
    graph = Graph(50, 50, 20, -1)
    surface = graph.surface
    graph.clear_board()
    while True:
        if left_mouse_drag():
            x, y = pygame.mouse.get_pos()
            graph.add_wall((x, y))

        if right_mouse_drag():
            x, y = pygame.mouse.get_pos()
            graph.clear_node((x, y))

        for event in pygame.event.get():
            event_handler(graph, surface, clock, event)
            pygame.event.get()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    FOREGROUND_COLOR = 0xC0CAF5
    BACKGROUND_COLOR = 0x1A1B26
    FONT = pygame.font.Font(None, 50)
    sys.setrecursionlimit(1000000)
    DIRECTIONS = [
        [0, -1],
        [1, 0],
        [0, 1],
        [-1, 0],
    ]
    main()
