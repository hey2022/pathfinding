import pygame
import sys

from pathfinding.graph import *
from pathfinding.algorithm import *


def quit():
    pygame.quit()
    sys.exit()


def key_press(event: pygame.event.Event, key: int) -> bool:
    return event.type == pygame.KEYDOWN and event.key == key


def display_message(surface: pygame.Surface, message: str, x: int, y: int):
    text = FONT.render(message, True, 0xFFFFFFFF)
    rect = surface.blit(text, (x, y))
    pygame.display.update(rect)


def left_mouse_drag() -> bool:
    return pygame.mouse.get_pressed()[0]


def right_mouse_drag() -> bool:
    return pygame.mouse.get_pressed()[2]


def main():
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((1000, 1000))
    graph = Graph(10, -1, FOREGROUND_COLOR, BACKGROUND_COLOR)
    graph.clear_board()
    result = None
    while True:
        if left_mouse_drag():
            graph.add_wall(pygame.mouse.get_pos())

        if right_mouse_drag():
            graph.clear_pos(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                quit()

            if (
                event.type == pygame.KEYDOWN or any(pygame.mouse.get_pressed())
            ) and result is not None:
                for node in result.path:
                    graph.clear_node(node)
                graph.display_nodes(result.path)
                for node in result.explored:
                    graph.clear_node(node)
                graph.display_nodes(result.explored)
                result = None

            if key_press(event, pygame.K_s):
                graph.update_source(pygame.mouse.get_pos())

            if key_press(event, pygame.K_t):
                graph.update_target(pygame.mouse.get_pos())

            if key_press(event, pygame.K_c):
                graph.clear_board()

            if key_press(event, pygame.K_RETURN):
                if graph.source is not None and graph.target is not None:
                    result = bfs(graph)
                    for node in result.path:
                        graph.draw_node(node, 0x0000FF)
                    graph.display_nodes(result.path)
            pygame.event.get()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    FOREGROUND_COLOR = 0xC0CAF5
    BACKGROUND_COLOR = 0x1A1B26
    FONT = pygame.font.Font(None, 50)
    sys.setrecursionlimit(1000000)
    main()
