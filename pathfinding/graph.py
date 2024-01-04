import pygame


class Graph:
    def __init__(
        self,
        block_size: int,
        grid_thickness: int,
        foreground_color: int,
        background_color: int,
    ):
        self.block_size = block_size
        self.surface = pygame.display.get_surface()
        self.rows, self.columns = self.pos_to_index(self.surface.get_size())
        self.grid_thickness = grid_thickness
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.setup()

    def setup(self):
        self.source = None
        self.target = None
        self.walls = set()

    def pos_to_index(self, pos: tuple[int, int]) -> tuple[int, int]:
        (column, row) = map(lambda x: x // self.block_size, pos)
        return (row, column)

    def index_to_pos(self, index: tuple[int, int]) -> tuple[int, int]:
        (y, x) = map(lambda x: x * self.block_size, index)
        return (x, y)

    def create_rect(self, index: tuple[int, int]) -> pygame.Rect:
        (x, y) = self.index_to_pos(index)
        return pygame.Rect(
            x,
            y,
            self.block_size,
            self.block_size,
        )

    def draw_node(self, color: int, node: tuple[int, int]) -> pygame.Rect:
        rect = self.create_rect(node)
        pygame.draw.rect(self.surface, color, rect)
        pygame.display.update(rect)
        return rect

    def clear_node(self, node: tuple[int, int]):
        if self.source == node:
            self.source = None
        if self.target == node:
            self.target = None
        self.walls.discard(node)
        self.draw_node(self.background_color, node)

    def clear_pos(self, pos: tuple[int, int]):
        node = self.pos_to_index(pos)
        self.clear_node(node)

    def clear_board(self):
        self.setup()
        self.surface.fill(self.background_color)
        pygame.display.update()

    def add_wall(self, pos):
        node = self.pos_to_index(pos)
        if self.source == node:
            self.source = None
        if self.target == node:
            self.target = None
        self.walls.add(node)
        self.draw_node(self.foreground_color, node)

    def update_target(self, pos: tuple[int, int]):
        node = self.pos_to_index(pos)
        self.walls.discard(node)
        if self.target is not None:
            self.clear_node(self.target)
        self.target = node
        self.draw_node(0xFF0000, node)

    def update_source(self, pos: tuple[int, int]):
        node = self.pos_to_index(pos)
        self.walls.discard(node)
        if self.source is not None:
            self.clear_node(self.source)
        self.source = node
        self.draw_node(0x99FFCC, node)
