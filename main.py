import pygame
import sys

from pathfinding.graph import *
from pathfinding.algorithm import *


def quit() -> None:
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





def main() -> None:
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((1000, 1000))
    graph = Graph(10, FOREGROUND_COLOR, BACKGROUND_COLOR)
    graph.clear_board()
    result = Result([], set())

    algorithms = [a_star, bfs, dfs]
    current_algorithm = 0
    print(algorithms[current_algorithm].__name__)
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
            ) and result:
                for node in result.path:
                    graph.clear_node(node)
                graph.display_nodes(result.path)
                for node in result.explored:
                    if node != graph.source and node != graph.target:
                        graph.clear_node(node)
                graph.display_nodes(result.explored)
                result = Result([], set())

            if key_press(event, pygame.K_s):
                graph.update_source(pygame.mouse.get_pos())

            if key_press(event, pygame.K_t):
                graph.update_target(pygame.mouse.get_pos())

            if key_press(event, pygame.K_c):
                graph.clear_board()

            if key_press(event, pygame.K_TAB):
                current_algorithm += 1
                current_algorithm %= len(algorithms)
                print(algorithms[current_algorithm].__name__)

            if key_press(event, pygame.K_RETURN):
                if graph.source and graph.target:
                    result = algorithms[current_algorithm](graph)
                    path = result.path[:]
                    path.insert(0, graph.source)
                    path.append(graph.target)
                    for i in range(1, len(path)-1):
                        graph.draw_path(2, PATH_COLOR, path[i-1], path[i], path[i+1])
                    graph.display_nodes(path)
            pygame.event.get()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    FOREGROUND_COLOR = 0xC0CAF5
    BACKGROUND_COLOR = 0x1A1B26
    PATH_COLOR = 0x7AA2F7
    FONT = pygame.font.Font(None, 50)
    sys.setrecursionlimit(1000000)
    main()
