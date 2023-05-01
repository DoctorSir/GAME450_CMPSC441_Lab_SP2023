import sys
import pygame
import random
import numpy as np
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg, elevation_to_rgba
from pygame_ai_player import PyGameAIPlayer
from journal import get_journal_entry

from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes
from lab3.travel_cost import get_route_cost
from lab5.landscape import get_elevation
from lab7.ga_cities import game_fitness, setup_GA, solution_to_cities


pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def get_landscape_surface(elevation):
    landscape = elevation_to_rgba(elevation)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])


def convert_to_coordinates(values, grid_size):
    """
    Converts a list of int32 values into tuples of coordinate pairs based on a passed in grid size.
    
    Args:
        values (list[int]): List of int32 values to convert.
        grid_size (tuple[int, int]): Tuple of width and height for the grid used to create the coordinate pairs.
    
    Returns:
        list[tuple[int, int]]: List of coordinate pairs in the form of tuples.
    """
    width, height = grid_size
    coordinates = []
    for value in values:
        x = value % width
        y = value // width
        coordinates.append((x, y))
    return coordinates


def route_exists(start_city, end_city, routes):
    """
    Checks whether a direct route exists between two cities using a list of tuples containing pairs of cities representing the routes between them.
    
    Args:
        start_city (tuple[int, int]): Tuple representing the coordinates of the starting city.
        end_city (tuple[int, int]): Tuple representing the coordinates of the ending city.
        routes (list[tuple[tuple[int, int], tuple[int, int]]]): List of tuples containing pairs of cities representing the routes between them.
    
    Returns:
        bool: True if a direct route exists, False otherwise.
    """
    # Check if there is a direct route between the start and end city
    for city1, city2 in routes:
        if ((city1 == start_city and city2 == end_city) or 
            (city1 == end_city and city2 == start_city)):
            return True
    
    # If no direct route is found, return False
    return False


class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes


if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1

    screen = setup_window(width, height, "Game World Gen Practice")

    elevation = get_elevation(size)
    landscape_surface = get_landscape_surface(elevation)
    # normalize landscape
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

    combat_surface = get_combat_surface(size)

    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    # setup fitness function and GA
    fitness = lambda ga_instance, cities, idx: game_fitness(
        cities, idx, elevation=elevation, size=size
    )
    fitness_function, ga_instance = setup_GA(fitness, len(city_names), size)

    ga_instance.run()
    cities = ga_instance.best_solution()[0]
    cities = convert_to_coordinates(cities, size)

    #cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]

    player_sprite = Sprite(sprite_path, cities[start_city])

    player = PyGameHumanPlayer(1000)

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""

    # player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    while True:
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                if route_exists(cities[state.current_city], cities[int(chr(action))], routes):
                    start = cities[state.current_city]
                    state.destination_city = int(chr(action))
                    destination = cities[state.destination_city]
                    player_sprite.set_location(cities[state.current_city])
                    state.travelling = True
                    print(
                        "Travelling from", city_names[state.current_city], "to", city_names[state.destination_city]
                    )
                else:
                    print("Route does not exist!")

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', city_names[state.destination_city])
                player.money -= 2 * get_route_cost((cities[state.current_city], cities[state.destination_city]), elevation)
                print("Money left:", player.money)
                get_journal_entry(city_names[state.current_city])

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            if run_pygame_combat(combat_surface, screen, player_sprite) < 1:
                print("You died in battle. GAME OVER!")
                break
            state.encounter_event = False
            player.money += random.randint(50, 200)
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
        elif player.money < 1:
            print("You ran out of money. GAME OVER!")
            break