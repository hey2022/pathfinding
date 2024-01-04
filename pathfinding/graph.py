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
        self.walls = [[False for _ in range(self.columns)] for _ in range(self.rows)]

    def pos_to_index(self, pos: tuple[int, int]) -> tuple[int, int]:
        (column, row) = map(lambda x: x // self.block_size, pos)
        return (row, column)

    def index_to_pos(self, index: tuple[int, int]) -> tuple[int, int]:
        (y, x) = map(lambda x: x * self.block_size, index)
        return (x, y)

    def create_node(self, index: tuple[int, int]) -> pygame.Rect:
        (x, y) = self.index_to_pos(index)
        return pygame.Rect(
            x,
            y,
            self.block_size,
            self.block_size,
        )

    def draw_index(self, color: int, index: tuple[int, int]) -> pygame.Rect:
        node = self.create_node(index)
        pygame.draw.rect(self.surface, color, node)
        pygame.display.update(node)
        return node

    def clear_index(self, index: tuple[int, int]):
        (row, column) = index
        if self.source == index:
            self.source = None
        if self.target == index:
            self.target = None
        self.walls[row][column] = False
        self.draw_index(self.background_color, index)

    def clear_pos(self, pos: tuple[int, int]):
        index = self.pos_to_index(pos)
        self.clear_index(index)

    def clear_board(self):
        self.setup()
        self.surface.fill(self.background_color)
        pygame.display.update()

    def add_wall(self, pos):
        index = self.pos_to_index(pos)
        (row, column) = index
        if self.source == index:
            self.source = None
        if self.target == index:
            self.target = None
        self.walls[row][column] = True
        self.draw_index(self.foreground_color, index)

    def update_target(self, pos: tuple[int, int]):
        index = self.pos_to_index(pos)
        (row, column) = index
        self.walls[row][column] = False
        if self.target is not None:
            self.clear_index(self.target)
        self.target = index
        self.draw_index(0xFF0000, index)

    def update_source(self, pos: tuple[int, int]):
        index = self.pos_to_index(pos)
        (row, column) = index
        self.walls[row][column] = False
        if self.source is not None:
            self.clear_index(self.source)
        self.source = index
        self.draw_index(0x99FFCC, index)
