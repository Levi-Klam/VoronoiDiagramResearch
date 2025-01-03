import pygame

class VoronoiDisplay:
    def __init__(self, size, index_heat, canvas, colors, coords, landmarks, fixed_landmarks, heat_map_check, heat_multiplier):
        self.size = size
        self.heat_map = index_heat
        self.canvas = canvas
        self.colors = colors
        self.coords = coords
        self.landmarks = landmarks
        self.fixed_landmarks = fixed_landmarks
        self.heat_map_check = heat_map_check
        self.heat_multiplier = heat_multiplier

    def display_voronoi(self):
        # Check if the user wants to make a heatmap or a normal Voronoi.
        pygame.init()
        pygame.display.set_caption("Diagram")
        window_size = (self.size / 2, self.size / 2)
        window = pygame.display.set_mode(window_size)
        surface = pygame.Surface((self.size, self.size))

        # The calculations for both of these is already done, so we could theoretically display both
        if self.heat_map_check == 0:
            # Find the largest distance on the canvas, and apply a desired multiplier to it for more/less red
            max_heat = int(max(self.heat_map))
            heat_multiplier = max_heat // self.heat_multiplier

            for x in range(self.size):
                for y in range(self.size):
                    # If the multipler makes a point go out of bounds, fix it.
                    heat_scale = int((self.heat_map[y * self.size + x] * 255) / heat_multiplier)
                    if heat_scale > 255:
                        heat_scale = 255

                    surface.set_at((x, y), (heat_scale, 255 - heat_scale, 0))

        elif self.heat_map_check == 1:
            for x in range(self.size):
                for y in range(self.size):
                    color = self.colors[self.canvas[y * self.size + x]]

                    # rect = pygame.Rect(x, y, 1, 1)
                    surface.set_at((x, y), color)


        # Labels every landmark in self.landmarks with a pink circle
        # pink = (255, 105, 180)
        light_blue = (125, 249, 255)
        bigger_radius = 10
        # for coord in self.fixed_landmarks:
        #     pygame.draw.circle(surface, light_blue, (coord[0], coord[1]), bigger_radius)

        # This labels every seed location with a white circle
        white = (255, 255, 255)
        black = (0, 0, 0)
        radius = 4
        for seed in self.coords.resized_coords:
            pygame.draw.circle(surface, white, (seed[0], seed[1]), radius)

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
                    print(f"Estimated Distance to Nearest Seed: {self.heat_map[local_coords[0] * self.size + local_coords[1]]}")
                    print(f"Canvas color: {self.canvas[local_coords[0] * self.size + local_coords[1]]}")

                    # This is horrible code. However, when clicking on landmarks, it prints out their name.
                    for points in range(len(self.fixed_landmarks)):
                        dist_squared = (local_coords[0] - self.fixed_landmarks[points][0]) ** 2 + (local_coords[1] - self.fixed_landmarks[points][1]) ** 2
                        if dist_squared <= bigger_radius ** 2:
                            print(f"Landmark: {list(self.landmarks.keys())[points]}")

            # Scale the 2048x2048 surface down to preferred screen viewing, then display the new surface
            scaled_surface = pygame.transform.scale(surface, window_size)
            window.blit(scaled_surface, (0, 0))
            pygame.display.update()

        pygame.quit()
