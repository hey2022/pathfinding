import pygame
import sys


class Graph:
    def __init__(self, width: int, height: int, block_size: int, grid_thickness: int):
        self.width = width * block_size
        self.height = height * block_size
        self.block_size = block_size
        self.grid_thickness = grid_thickness
        self.surface = pygame.display.set_mode((self.width, self.height))

    def create_node(self, x: int, y: int) -> pygame.Rect:
        return pygame.Rect(
            x // self.block_size * self.block_size,
            y // self.block_size * self.block_size,
            self.block_size,
            self.block_size,
        )

    def draw_node(self, color: int, node: pygame.Rect) -> pygame.Rect:
        if node == self.source:
            self.source = None
        if node == self.target:
            self.target = None
        pygame.draw.rect(
            self.surface,
            color,
            node,
        )
        pygame.display.update(node)
        return node

    def add_wall(self, wall: pygame.Rect):
        if wall not in self.walls:
            self.walls.append(wall)

    def add_visited(self, visited: pygame.Rect):
        if visited not in self.visited:
            self.visited.append(visited)

    def clear_node(self, node: pygame.Rect):
        if node == self.source:
            self.source = None
        if node == self.target:
            self.target = None
        if node in self.walls:
            self.walls.remove(node)
        pygame.draw.rect(
            self.surface,
            BACKGROUND_COLOR,
            node,
        )
        pygame.draw.rect(self.surface, FOREGROUND_COLOR, node, self.grid_thickness)
        pygame.display.update(node)

    def update_target(self, node: pygame.Rect):
        if self.target == node:
            return
        if node in self.walls:
            self.walls.remove(node)
        if self.target is not None:
            self.clear_node(self.target)
        self.target = self.draw_node(0xFF0000, node)

    def update_source(self, node: pygame.Rect):
        if self.source == node:
            return
        if node in self.walls:
            self.walls.remove(node)
        if self.source is not None:
            self.clear_node(self.source)
        self.source = self.draw_node(0x99FFCC, node)

    def clear_board(self):
        self.source = None
        self.target = None
        self.walls = []
        self.visited = []
        self.surface.fill(BACKGROUND_COLOR)
        pygame.display.update()
        for x in range(0, self.width, self.block_size):
            for y in range(0, self.height, self.block_size):
                node = self.create_node(x, y)
                pygame.draw.rect(
                    self.surface, FOREGROUND_COLOR, node, self.grid_thickness
                )
        pygame.display.update()

    def is_valid_node(self, node: pygame.Rect):
        x, y = node.left, node.top
        in_bounds = x >= 0 and x < self.width and y >= 0 and y < self.height
        not_wall = node not in self.walls
        return in_bounds and not_wall

    def dfs(self, clock: pygame.time.Clock, x: int, y: int):
        clock.tick(120)
        for direction in DIRECTIONS:
            new_x = x + direction[0] * self.block_size
            new_y = y + direction[1] * self.block_size
            node = self.create_node(new_x, new_y)
            if node == self.target:
                return 1
            if self.is_valid_node(node) and node not in self.visited:
                self.visited.append(node)
                self.draw_node(0x99FFCC, node)
                if self.dfs(clock, new_x, new_y):
                    self.clear_node(node)
                    return 1
                self.clear_node(node)
        return 0


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
        node = graph.create_node(x, y)
        graph.update_source(node)

    if key_press(event, pygame.K_t):
        x, y = pygame.mouse.get_pos()
        node = graph.create_node(x, y)
        graph.update_target(node)

    if key_press(event, pygame.K_c):
        graph.clear_board()

    if key_press(event, pygame.K_RETURN):
        if graph.source is not None and graph.target is not None:
            graph.visited = [graph.source]
            graph.dfs(
                clock,
                graph.source.left,
                graph.source.top,
            )


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
            wall = graph.create_node(x, y)
            graph.draw_node(FOREGROUND_COLOR, wall)
            graph.add_wall(wall)

        if right_mouse_drag():
            x, y = pygame.mouse.get_pos()
            node = graph.create_node(x, y)
            graph.clear_node(node)

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
