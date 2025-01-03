import pygame
from CoordBuilder import Coords

class VoronoiWeightedDisplay:
    def __init__(self, size, final_array, heat_multiplier):
        self.size = size
        self.heat_map = final_array
        self.heat_multiplier = heat_multiplier
        self.coords = Coords(size)

        self.landmarks = {'Pew Campus': [42.9645619511, -85.67985959953], 'Gerald R Ford Airport': [42.885762089162, -85.525930170048],
                          '196 meets 131': [42.973029244286, -85.678160370308], '131 meets 96': [43.01486632967, -85.677313444134],
                          '196 meets 96': [42.9767152583242, -85.604123679628], "M6 meets 196": [42.86220738433159, -85.8179164575949],
                          "M6 meets 131": [42.84875409314281, -85.67874753122842], "Allendale Campus": [42.96460527002176, -85.88919971843376]}
        landmarks = Coords(self.size)
        for coords in self.landmarks.values():
            landmarks.latlongs.append(coords)
        self.fixed_landmarks = landmarks.fix_coords()

    def display_voronoi(self):
        # Reinit pygame to change display size and such
        pygame.init()
        pygame.display.set_caption("Diagram")
        window_size = (self.size / 2, self.size / 2)
        window = pygame.display.set_mode(window_size)
        surface = pygame.Surface((self.size, self.size))

        # Set a max distance in the matrix, and create a multiplier to 'lower' the max distance
        max_heat = int(max(self.heat_map))
        heat_multiplier = max_heat // self.heat_multiplier

        for x in range(self.size):
            for y in range(self.size):
                # If the multiplier makes a point go out of bounds, fix it.
                heat_scale = int((self.heat_map[y * self.size + x] * 255) / heat_multiplier)
                if heat_scale > 255:
                    heat_scale = 255

                surface.set_at((x, y), (heat_scale, 255 - heat_scale, 0))

        light_blue = (125, 249, 255)
        dark_blue = (50, 50, 255)
        bigger_radius = 10
        # for coord in self.fixed_landmarks:
        #     pygame.draw.circle(surface, light_blue, (coord[0], coord[1]), bigger_radius)

        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Give coordinates of mouse click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    print(f"\nMouse clicked at ({mouse_x * 2}, {mouse_y * 2})")

                    local_coords = [mouse_x*2, mouse_y*2]
                    print(f"Coordinates: {self.coords.to_latlong_1D(local_coords)}")

                    for points in range(len(self.fixed_landmarks)):
                        dist_squared = (local_coords[0] - self.fixed_landmarks[points][0]) ** 2 + (local_coords[1] - self.fixed_landmarks[points][1]) ** 2
                        if dist_squared <= bigger_radius ** 2:
                            print(f"Landmark: {list(self.landmarks.keys())[points]}")



            # Scale the 2048x2048 surface down to preferred screen viewing, then display the new surface
            scaled_surface = pygame.transform.scale(surface, window_size)
            window.blit(scaled_surface, (0, 0))
            pygame.display.update()

        pygame.quit()
