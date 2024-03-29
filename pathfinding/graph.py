import pygame


class Graph:
    def __init__(
        self,
        block_size: int,
        foreground_color: int,
        background_color: int,
    ):
        self.block_size = block_size
        self.foreground_color = foreground_color
        self.background_color = background_color

        self.surface = pygame.display.get_surface()
        self.rows, self.columns = self.pos_to_index(self.surface.get_size())
        self.setup_board()

    def setup_board(self) -> None:
        self.source = ()
        self.target = ()
        self.walls = set()
        self.surface.fill(self.background_color)
        pygame.display.update()

    def pos_to_index(self, pos: tuple[int, int]) -> tuple[int, int]:
        (column, row) = map(lambda x: x // self.block_size, pos)
        return (row, column)

    def index_to_pos(self, index: tuple[int, int]) -> tuple[int, int]:
        (y, x) = map(lambda x: x * self.block_size, index)
        return (x, y)

    def is_empty_node(self, node: tuple[int, int]) -> bool:
        (row, column) = node
        if row < 0 or row >= self.rows or column < 0 or column >= self.columns:
            return False
        if node in self.walls or node == self.source or node == self.target:
            return False
        return True

    def create_rect(self, index: tuple[int, int]) -> pygame.Rect:
        (x, y) = self.index_to_pos(index)
        return pygame.Rect(
            x,
            y,
            self.block_size,
            self.block_size,
        )

    def draw_node(self, node: tuple[int, int], color: int) -> pygame.Rect:
        rect = self.create_rect(node)
        pygame.draw.rect(self.surface, color, rect)
        return rect

    def display_nodes(self, node_list):
        node_list = list(node_list)
        rects = []
        for node in node_list:
            rect = self.create_rect(node)
            rects.append(rect)
        pygame.display.update(rects)

    def clear_node(self, node: tuple[int, int]) -> pygame.Rect:
        if self.source == node:
            self.source = ()
        if self.target == node:
            self.target = ()
        self.walls.discard(node)
        rect = self.draw_node(node, self.background_color)
        return rect

    def clear_pos(self, pos: tuple[int, int]) -> None:
        node = self.pos_to_index(pos)
        pygame.display.update(self.clear_node(node))

    def add_wall(self, pos) -> None:
        node = self.pos_to_index(pos)

        if self.source == node:
            self.source = ()
        if self.target == node:
            self.target = ()

        self.walls.add(node)

        rect = self.draw_node(node, self.foreground_color)
        pygame.display.update(rect)

    def update_target(self, pos: tuple[int, int]) -> None:
        if self.target:
            pygame.display.update(self.clear_node(self.target))

        node = self.pos_to_index(pos)
        self.walls.discard(node)
        self.clear_node(node)
        self.target = node

        rect = self.draw_node(node, 0xFF0000)
        pygame.display.update(rect)

    def update_source(self, pos: tuple[int, int]) -> None:
        if self.source:
            pygame.display.update(self.clear_node(self.source))

        node = self.pos_to_index(pos)
        self.walls.discard(node)
        self.clear_node(node)
        self.source = node

        rect = self.draw_node(node, 0x99FFCC)
        pygame.display.update(rect)
