import time
import random
from CoordBuilder import Coords
from numba import njit
import numpy as np
import ArrayBuilder
from DisplayVoronoi import VoronoiDisplay
from PygameDisplay import DisplayMenu
from WeightedDistanceBuilder import Pareto
from WeightedMapDisplay import VoronoiWeightedDisplay


@njit
def find_closest_seed(p, array_of_seeds):
    n = len(array_of_seeds)
    closest_seed = -1
    shortest_distance = np.inf

    for i in range(int(n / 2)):
        distance_to_this_seed = (p[0] - int(array_of_seeds[2 * i + 0])) ** 2 + (
                    p[1] - int(array_of_seeds[2 * i + 1])) ** 2
        if distance_to_this_seed < shortest_distance:
            closest_seed = i
            shortest_distance = distance_to_this_seed

    return closest_seed


@njit
def fill_area(canvas, size, p1, p2, p3, p4, color, array_of_seeds, index_heat):
    for x in range(p1[0], p2[0] + 1):
        for y in range(p1[1], p4[1] + 1):
            # Both arrays are size x size long, so we can just index the points directly
            canvas[y * size + x] = color
            index_heat[y * size + x] = (x - int(array_of_seeds[2 * color+0])) ** 2 + (y - int(array_of_seeds[2 * color+1])) ** 2


@njit
def recursive_quad(canvas, size, p1, p2, p3, p4, index_heat, array_of_seeds=np.array([])):
    closestSeedP1 = find_closest_seed(p1, array_of_seeds)
    closestSeedP2 = find_closest_seed(p2, array_of_seeds)
    closestSeedP3 = find_closest_seed(p3, array_of_seeds)
    closestSeedP4 = find_closest_seed(p4, array_of_seeds)

    if (closestSeedP1 == closestSeedP2) and (closestSeedP2 == closestSeedP3) and (closestSeedP3 == closestSeedP4):
        fill_area(canvas, size, p1, p2, p3, p4, closestSeedP1, array_of_seeds, index_heat)
    else:
        middlePointX = (p1[0] + p2[0]) // 2
        middlePointY = (p1[1] + p4[1]) // 2

        quad1p1 = p1
        quad1p2 = (middlePointX, p1[1])
        quad1p3 = (middlePointX, middlePointY)
        quad1p4 = (p1[0], middlePointY)

        quad2p1 = (middlePointX + 1, p1[1])
        quad2p2 = p2
        quad2p3 = (p2[0], middlePointY)
        quad2p4 = (middlePointX + 1, middlePointY)

        quad3p1 = (middlePointX + 1, middlePointY + 1)
        quad3p2 = (p2[0], middlePointY + 1)
        quad3p3 = p3
        quad3p4 = (middlePointX + 1, p3[1])

        quad4p1 = (p1[0], middlePointY + 1)
        quad4p2 = (middlePointX, middlePointY + 1)
        quad4p3 = (middlePointX, p4[1])
        quad4p4 = p4

        recursive_quad(canvas, size, quad1p1, quad1p2, quad1p3, quad1p4, index_heat, array_of_seeds)
        recursive_quad(canvas, size, quad2p1, quad2p2, quad2p3, quad2p4, index_heat, array_of_seeds)
        recursive_quad(canvas, size, quad3p1, quad3p2, quad3p3, quad3p4, index_heat, array_of_seeds)
        recursive_quad(canvas, size, quad4p1, quad4p2, quad4p3, quad4p4, index_heat, array_of_seeds)


class VoronoiGenerator:
    def __init__(self, size, array_name, arr_of_coords, heat_map_check, heat_multiplier, heat_weights):
        self.array_of_seeds = []
        self.size = size
        self.array_of_seeds = np.array(self.array_of_seeds, dtype=np.float64)
        self.canvas = np.array([-1] * (self.size * self.size), dtype=np.int32)

        self.array_name = array_name
        self.coords = Coords(self.size)
        self.coords.latlongs = arr_of_coords
        self.n = len(self.coords.latlongs)
        self.coords.resized_coords = self.coords.fix_coords()
        for i in self.coords.resized_coords:
            self.array_of_seeds = np.append(self.array_of_seeds, [[i[0], i[1]]], axis=None)

        # Each index's rough distance from the nearest seed
        self.index_heat = np.array([-1] * (self.size * self.size), dtype=np.int32)
        self.heat_map_check = heat_map_check
        self.heat_multiplier = heat_multiplier
        self.heat_weights = heat_weights

        # Add a custom color for each seed
        self.colors = []
        for _ in self.coords.latlongs:
            self.colors.append((random.randint(0, 175), random.randint(0, 175), random.randint(0, 175)))

        # Landmarks were used for verification of longitudge/latitude points.
        self.landmarks = {'Pew Campus': [42.9645619511, -85.67985959953], 'Gerald R Ford Airport': [42.885762089162, -85.525930170048],
                          '196 meets 131': [42.973029244286, -85.678160370308], '131 meets 96': [43.01486632967, -85.677313444134],
                          '196 meets 96': [42.9767152583242, -85.604123679628], "M6 meets 196": [42.86220738433159, -85.8179164575949],
                          "M6 meets 131": [42.84875409314281, -85.67874753122842], "Allendale Campus": [42.96460527002176, -85.88919971843376]}
        landmarks = Coords(self.size)
        for coords in self.landmarks.values():
            landmarks.latlongs.append(coords)
        self.fixed_landmarks = landmarks.fix_coords()

    def generate_voronoi(self):
        p1 = np.array([0, 0], dtype=np.int32)
        p2 = np.array([self.size - 1, 0], dtype=np.int32)
        p3 = np.array([self.size - 1, self.size - 1], dtype=np.int32)
        p4 = np.array([0, self.size - 1], dtype=np.int32)

        start_time = time.time()

        recursive_quad(self.canvas, self.size, p1, p2, p3, p4, self.index_heat, self.array_of_seeds)

        end_time = time.time()
        duration = (end_time - start_time) * 1000
        print(f"Time for quad tree Voronoi: {duration} milliseconds with {self.n} seeds.")  # Change to just milliseconds, easier to pipe into file

        # Save the distances from each point to the nearest seed in csv, this was only used to make the initial Pareto Front
        # np.savetxt(f"distance_arrays/{self.array_name}.csv", self.index_heat)

    def display_voronoi(self):
        display = VoronoiDisplay(self.size, self.index_heat, self.canvas, self.colors, self.coords, self.landmarks, self.fixed_landmarks, self.heat_map_check, self.heat_multiplier)
        display.display_voronoi()


def main():
    # If the user chooses to do the weighted heatmap, there's no reason to generate a single voronoi, so it goes to an entirely different program
    start_menu = DisplayMenu()
    if start_menu.heat_map_check == 2:
        pareto = Pareto(start_menu.heat_weights)
        display = VoronoiWeightedDisplay(start_menu.size, pareto.final, start_menu.heat_multiplier)
        display.display_voronoi()
    else:
        chosen_array = ArrayBuilder.choose(start_menu.voronoi_selection)
        generator = VoronoiGenerator(start_menu.size, start_menu.voronoi_selection, chosen_array, start_menu.heat_map_check, start_menu.heat_multiplier, start_menu.heat_weights) # Array name, array literal, heatmap 0-2

        print("While Compiling:")
        generator.generate_voronoi()
        print("Already Compiled:")
        generator.generate_voronoi()

        generator.display_voronoi()


if __name__ == "__main__":
    main()
