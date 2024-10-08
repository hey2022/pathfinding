import pygame

# node is a tuple (x, y) that contains the grid coordinates for a block in the graph


class Graph:
    def __init__(
        self,
        node_size: int,
        foreground_color: int,
        background_color: int,
    ):
        self.node_size = node_size
        self.foreground_color = foreground_color
        self.background_color = background_color

        self.surface = pygame.display.get_surface()
        self.setup_board()
        (self.rows, self.columns) = self.pixel_to_node(self.surface.get_size())

    # clears board
    def setup_board(self) -> None:
        self.source = ()
        self.target = ()
        self.walls = set()
        self.surface.fill(self.background_color)
        pygame.display.update()

    # convert pixel coordinates to grid coordinates
    def pixel_to_node(self, pixel: tuple[int, int]) -> tuple[int, int]:
        node_x = pixel[0] // self.node_size
        node_y = pixel[1] // self.node_size
        return (node_x, node_y)

    # convert grid coordinates to pixel coordinates
    def node_to_pixel(self, node: tuple[int, int]) -> tuple[int, int]:
        pixel_x = node[0] * self.node_size
        pixel_y = node[1] * self.node_size
        return (pixel_x, pixel_y)

    # check if node at position is empty
    def is_empty_node(self, node: tuple[int, int]) -> bool:
        (node_x, node_y) = node
        # outside of boundaries
        if node_y < 0 or node_y >= self.rows or node_x < 0 or node_x >= self.columns:
            return False
        # a wall/source/target node
        if node in self.walls or node == self.source or node == self.target:
            return False
        return True

    # creates a rectangle for node
    def create_rect(self, node: tuple[int, int]) -> pygame.Rect:
        (pixel_x, pixel_y) = self.node_to_pixel(node)
        return pygame.Rect(
            pixel_x,
            pixel_y,
            self.node_size,
            self.node_size,
        )

    # draws a node
    def draw_node(self, node: tuple[int, int], color: int) -> pygame.Rect:
        rect = self.create_rect(node)
        pygame.draw.rect(self.surface, color, rect)
        return rect

    # given a list of nodes, update the display at the node
    def display_nodes(self, nodes):
        nodes = list(nodes)
        rects = []
        for node in nodes:
            rect = self.create_rect(node)
            rects.append(rect)
        pygame.display.update(rects)

    # clears a node
    def clear_node(self, node: tuple[int, int]) -> pygame.Rect:
        if self.source == node:
            self.source = ()
        if self.target == node:
            self.target = ()
        self.walls.discard(node)
        rect = self.draw_node(node, self.background_color)
        return rect

    # clears a node by its pixel coordinates (right mouse press)
    def clear_pixel(self, pixel: tuple[int, int]) -> None:
        node = self.pixel_to_node(pixel)
        pygame.display.update(self.clear_node(node))

    # adds a wall from pixel coordinates (left mouse press)
    def add_wall(self, pixel: tuple[int, int]) -> None:
        node = self.pixel_to_node(pixel)

        # wall is placed on top of source or target node
        if self.source == node:
            self.source = ()
        if self.target == node:
            self.target = ()

        self.walls.add(node)

        rect = self.draw_node(node, self.foreground_color)
        pygame.display.update(rect)

    # updates position of target node to the mouse
    def update_target(self, pixel: tuple[int, int]) -> None:
        # remove previous target node
        if self.target:
            pygame.display.update(self.clear_node(self.target))

        node = self.pixel_to_node(pixel)

        # remove previous node at new target location
        self.walls.discard(node)
        self.clear_node(node)

        self.target = node

        rect = self.draw_node(node, 0xFF0000)
        pygame.display.update(rect)

    # updates position of source node to the mouse
    def update_source(self, pixel: tuple[int, int]) -> None:
        # remove previous source node
        if self.source:
            pygame.display.update(self.clear_node(self.source))

        node = self.pixel_to_node(pixel)

        # remove previous node at new source location
        self.walls.discard(node)
        self.clear_node(node)

        self.source = node

        rect = self.draw_node(node, 0x99FFCC)
        pygame.display.update(rect)
