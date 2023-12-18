import pygame
import sys


class Graph:
    def __init__(self, width: int, height: int, block_size: int):
        self.width = width * block_size
        self.height = height * block_size
        self.block_size = block_size

    def create_node(self, x: int, y: int) -> pygame.Rect:
        return pygame.Rect(
            x // self.block_size * self.block_size,
            y // self.block_size * self.block_size,
            self.block_size,
            self.block_size,
        )

    def draw_node(
        self, surface: pygame.Surface, color: int, node: pygame.Rect
    ) -> pygame.Rect:
        if node == self.start:
            self.start = None
        if node == self.end:
            self.end = None
        pygame.draw.rect(
            surface,
            color,
            node,
        )
        pygame.display.update(node)
        return node

    def add_wall(self, wall: pygame.Rect):
        if wall not in self.walls:
            self.walls.append(wall)

    def clear_node(self, surface: pygame.Surface, node: pygame.Rect):
        if node == self.start:
            self.start = None
        if node == self.end:
            self.end = None
        if node in self.walls:
            self.walls.remove(node)
        pygame.draw.rect(
            surface,
            BACKGROUND_COLOR,
            node,
        )
        pygame.draw.rect(surface, FOREGROUND_COLOR, node, 1)
        pygame.display.update(node)

    def update_goal(self, surface: pygame.Surface, node: pygame.Rect):
        if self.end == node:
            return
        if node in self.walls:
            self.walls.remove(node)
        if self.end != None:
            self.clear_node(surface, self.end)
        self.end = self.draw_node(surface, 0xFF0000, node)

    def update_start(self, surface: pygame.Surface, node: pygame.Rect):
        if self.start == node:
            return
        if node in self.walls:
            self.walls.remove(node)
        if self.start != None:
            self.clear_node(surface, self.start)
        self.start = self.draw_node(surface, 0x99FFCC, node)

    def clear_board(self, surface):
        self.start = None
        self.end = None
        self.walls = []
        nodes = []
        surface.fill(BACKGROUND_COLOR)
        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                print(x, y)
                node = self.create_node(x, y)
                pygame.draw.rect(surface, FOREGROUND_COLOR, node, 1)
                nodes.append(node)
        pygame.display.update(nodes)


def dfs(x: int, y: int) -> int:
    directions = [[-1, 0], [1, 0], [-1, 0], [1, 0]]
    for direction in directions:
        dfs(x + direction[0], y + direction[1])
    pass


def quit():
    pygame.quit()
    sys.exit()


def key_press(event: pygame.event.Event, key: int) -> bool:
    return event.type == pygame.KEYDOWN and event.key == key


def event_handler(graph: Graph, surface: pygame.Surface, event: pygame.event.Event):
    if (
        event.type == pygame.QUIT
        or event.type == pygame.KEYDOWN
        and event.key == pygame.K_ESCAPE
    ):
        quit()

    if key_press(event, pygame.K_g):
        x, y = pygame.mouse.get_pos()
        node = graph.create_node(x, y)
        graph.update_goal(surface, node)

    if key_press(event, pygame.K_s):
        x, y = pygame.mouse.get_pos()
        node = graph.create_node(x, y)
        graph.update_start(surface, node)

    if key_press(event, pygame.K_c):
        graph.clear_board(surface)


def left_mouse_drag() -> bool:
    return pygame.mouse.get_pressed()[0]


def right_mouse_drag() -> bool:
    return pygame.mouse.get_pressed()[2]


def main():
    pygame.init()
    clock = pygame.time.Clock()
    graph = Graph(20, 20, 50)
    surface = pygame.display.set_mode((graph.width, graph.height))

    graph.clear_board(surface)
    while True:
        if left_mouse_drag():
            x, y = pygame.mouse.get_pos()
            wall = graph.create_node(x, y)
            graph.draw_node(surface, FOREGROUND_COLOR, wall)
            graph.add_wall(wall)

        if right_mouse_drag():
            x, y = pygame.mouse.get_pos()
            node = graph.create_node(x, y)
            graph.clear_node(surface, node)

        for event in pygame.event.get():
            event_handler(graph, surface, event)
        clock.tick(60)


if __name__ == "__main__":
    FOREGROUND_COLOR = 0xC0CAF5
    BACKGROUND_COLOR = 0x1A1B26
    main()
