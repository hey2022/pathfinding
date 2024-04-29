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

    # list of pathfinding algorithms
    algorithms = [a_star_manhattan_distance, a_star_euclidian_distance, bfs, dfs]
    current_algorithm_index = 0
    print(algorithms[current_algorithm_index].__name__)

    while True:
        # add wall at mouse position when left mouse pressed
        if pygame.mouse.get_pressed()[0]:
            graph.add_wall(pygame.mouse.get_pos())

        # clear wall at mouse position when right mouse pressed
        if pygame.mouse.get_pressed()[2]:
            graph.clear_pixel(pygame.mouse.get_pos())

        for event in pygame.event.get():
            # quit game
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

            # clear visualizations after running pathfinding algorithms
            if (
                event.type == pygame.KEYDOWN or any(pygame.mouse.get_pressed())
            ) and result:
                # remove path visualizations
                for node in result.path:
                    # don't remove source and target node
                    if graph.is_empty_node(node):
                        graph.clear_node(node)
                # remove visited visualizations
                for node in result.explored:
                    if graph.is_empty_node(node):
                        graph.clear_node(node)
                # update display
                graph.display_nodes(result.path)
                graph.display_nodes(result.explored)
                result = Result()

            # update position of source node
            if key_press(event, pygame.K_s):
                graph.update_source(pygame.mouse.get_pos())

            # update position of target node
            if key_press(event, pygame.K_t):
                graph.update_target(pygame.mouse.get_pos())

            # clear board
            if key_press(event, pygame.K_c):
                graph.setup_board()

            # cycle pathfinding algorithm to use
            if key_press(event, pygame.K_TAB):
                current_algorithm_index = (current_algorithm_index + 1) % len(
                    algorithms
                )
                print(algorithms[current_algorithm_index].__name__)

            # run pathfinding algorithm
            if key_press(event, pygame.K_RETURN):
                if graph.source and graph.target:
                    result = algorithms[current_algorithm_index](graph)
                    draw_path(graph, result.path, PATH_COLOR)

            # ignore extra events received while pathfinding algorithm is running
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
