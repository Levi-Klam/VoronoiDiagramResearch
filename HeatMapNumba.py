import time
from numba import njit
import numpy as np
import pygame


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
def fill_area(canvas, heat_map, size, p1, p2, p3, p4, color, array_of_seeds):
    for x in range(p1[0], p2[0] + 1):
        for y in range(p1[1], p4[1] + 1):
            canvas[y * size + x] = color
            heat_map[y * size + x] = distance_to_this_seed = (x - int(array_of_seeds[2 * color + 0])) ** 2 + (
                    y - int(array_of_seeds[2 * color + 1])) ** 2


@njit
def recursive_quad(canvas, heat_map, size, p1, p2, p3, p4, array_of_seeds=np.array([])):
    closestSeedP1 = find_closest_seed(p1, array_of_seeds)
    closestSeedP2 = find_closest_seed(p2, array_of_seeds)
    closestSeedP3 = find_closest_seed(p3, array_of_seeds)
    closestSeedP4 = find_closest_seed(p4, array_of_seeds)

    if (closestSeedP1 == closestSeedP2) and (closestSeedP2 == closestSeedP3) and (closestSeedP3 == closestSeedP4):
        fill_area(canvas, heat_map, size, p1, p2, p3, p4, closestSeedP1, array_of_seeds)
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

        recursive_quad(canvas, heat_map, size, quad1p1, quad1p2, quad1p3, quad1p4, array_of_seeds)
        recursive_quad(canvas, heat_map, size, quad2p1, quad2p2, quad2p3, quad2p4, array_of_seeds)
        recursive_quad(canvas, heat_map, size, quad3p1, quad3p2, quad3p3, quad3p4, array_of_seeds)
        recursive_quad(canvas, heat_map, size, quad4p1, quad4p2, quad4p3, quad4p4, array_of_seeds)


class VoronoiGenerator:
    def __init__(self):
        self.array_of_seeds = []
        self.size = 1024
        self.array_of_seeds = np.array(self.array_of_seeds, dtype=np.float64)
        self.canvas_original = [-1] * (self.size * self.size)
        self.canvas = np.array(self.canvas_original, dtype=np.int32)
        self.heat_map = np.array(self.canvas_original, dtype=np.int32)

        self.n = input()
        for i in range(int(self.n)):
            x, y = input().split()
            self.array_of_seeds = np.append(self.array_of_seeds, [int(x), int(y)], axis=None)

        for i in self.array_of_seeds:
            print(i)

    def generate_voronoi(self):
        p1 = np.array([0, 0], dtype=np.int32)
        p2 = np.array([self.size - 1, 0], dtype=np.int32)
        p3 = np.array([self.size - 1, self.size - 1], dtype=np.int32)
        p4 = np.array([0, self.size - 1], dtype=np.int32)

        start_time = time.time()

        recursive_quad(self.canvas, self.heat_map, self.size, p1, p2, p3, p4, self.array_of_seeds)
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        print(f"{round(duration, 5)}")

    def draw_voronoi_heat_map(self):

        max_heat = int(max(self.heat_map))

        pygame.init()

        window_size = (self.size/2, self.size/2)
        window = pygame.display.set_mode(window_size)
        surface = pygame.Surface((self.size, self.size))

        for x in range(self.size):
            for y in range(self.size):
                heat = int(self.heat_map[y * self.size + x]/max_heat * 255)
                surface.set_at((x,y), (heat, 0, 0))

        scaled_surface = pygame.transform.scale(surface, window_size)
        window.blit(scaled_surface, (0, 0))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


def main():
    generator = VoronoiGenerator()

    print("While Compiling:")
    generator.generate_voronoi()
    print("Already Compiled:")
    generator.generate_voronoi()

    generator.draw_voronoi_heat_map()


if __name__ == "__main__":
    main()
