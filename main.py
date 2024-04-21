import pygame
import sys

from pathfinding.graph import Graph
from pathfinding.algorithm import (
    a_star_euclidian_distance,
    a_star_manhattan_distance,
    bfs,
    dfs,
    Result,
    draw_path,
)


def key_press(event: pygame.event.Event, key: int) -> bool:
    return event.type == pygame.KEYDOWN and event.key == key


def main() -> None:
    graph = Graph(10, FOREGROUND_COLOR, BACKGROUND_COLOR)
    result = Result()
    clock = pygame.time.Clock()

    algorithms = [a_star_manhattan_distance, a_star_euclidian_distance, bfs, dfs]
    current_algorithm_index = 0
    print(algorithms[current_algorithm_index].__name__)
    while True:
        # left mouse pressed
        if pygame.mouse.get_pressed()[0]:
            graph.add_wall(pygame.mouse.get_pos())

            graph.clear_pos(pygame.mouse.get_pos())
        # right mouse pressed
        if pygame.mouse.get_pressed()[2]:

        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()
            if (
                event.type == pygame.KEYDOWN or any(pygame.mouse.get_pressed())
            ) and result:
                for node in result.path:
                    if graph.is_empty_node(node):
                        graph.clear_node(node)
                for node in result.explored:
                    if graph.is_empty_node(node):
                        graph.clear_node(node)
                graph.display_nodes(result.path)
                graph.display_nodes(result.explored)
                result = Result()

            if key_press(event, pygame.K_s):
                graph.update_source(pygame.mouse.get_pos())

            if key_press(event, pygame.K_t):
                graph.update_target(pygame.mouse.get_pos())

            if key_press(event, pygame.K_c):
                graph.setup_board()

            if key_press(event, pygame.K_TAB):
                current_algorithm_index = (current_algorithm_index + 1) % len(
                    algorithms
                )
                print(algorithms[current_algorithm_index].__name__)

            if key_press(event, pygame.K_RETURN):
                if graph.source and graph.target:
                    result = algorithms[current_algorithm_index](graph)
                    draw_path(graph, result.path, PATH_COLOR)
            pygame.event.get()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1000, 1000))

    FPS = 60
    FOREGROUND_COLOR = 0xC0CAF5
    BACKGROUND_COLOR = 0x1A1B26
    PATH_COLOR = 0x7AA2F7
    main()
