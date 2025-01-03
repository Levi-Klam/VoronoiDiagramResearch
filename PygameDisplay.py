import pygame
from GUI import Button, Slider

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (215, 252, 212)


class DisplayMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Voronoi Generator")

        self.BLACK = (0, 0, 0)

        self.menu_font = pygame.font.SysFont('arial', 100)
        self.button_font = pygame.font.SysFont('arial', 75)
        self.caption_font = pygame.font.SysFont('arial', 25)

        self.size = 1024
        self.voronoi_selection = "Schools"
        self.heat_map_check = 0
        self.heat_multiplier = 1
        self.heat_weights = [1, 1, 1, 1, 1, 1]

        self.close_display = False
        self.buttons_init()
        self.main_menu()

    def buttons_init(self):
        self.play_button = Button(None, (640, 250), "Run Generator", self.button_font, GREEN, True)
        self.options_button = Button(None, (640, 400), "Options", self.button_font, GREEN, True)
        self.quit_button = Button(None, (640, 550), "Quit", self.button_font, GREEN, True)

        self.options_back = Button(None, (640, 675), "Back", self.button_font, GREEN, True)
        self.choose_voronoi = Button(None, (640, 150), "Choose Seed Set", self.button_font, GREEN, True)

        self.heat_map_yes = Button(None, (500, 300), "Heatmap", self.button_font, WHITE, True)
        self.heat_map_no = Button(None, (800, 300), "Diagram", self.button_font, GREEN, True)
        self.weighted_heat_map = Button(None, (650, 400), "Weighted Heatmap", self.button_font, GREEN, True)
        self.heat_multiplier_slider = Slider((500, 450), 300, 0, 20, 1, .1, GREEN, WHITE, self.caption_font, "Heat Multiplier", (0, 40))

        self.voronoi_back = Button(None, (640, 675), "Back", self.button_font, WHITE, True)
        self.schools = Button(None, (25, 100), "Schools", self.button_font, WHITE, False)
        self.churches = Button(None, (25, 175), "Churches", self.button_font, GREEN, False)
        self.bus_stops = Button(None, (25, 250), "Bus Stops", self.button_font, GREEN, False)
        self.restaurants = Button(None, (25, 325), "Restaurants", self.button_font, GREEN, False)
        self.groceries = Button(None, (25, 400), "Grocery Stores", self.button_font, GREEN, False)
        self.social_facilities = Button(None, (25, 475), "Social Facilities", self.button_font, GREEN, False)
        # self.parks = Button(None, (25, 400), "Parks", self.button_font, GREEN, False)
        self.seed_sets = [self.voronoi_back, self.schools, self.churches, self.bus_stops, self.restaurants, self.groceries, self.social_facilities] #  , self.parks]

        self.schools_slider = Slider((640, 100), 300, 0, 1, 1, .05, GREEN, WHITE, self.caption_font, "Heat", (310, 20))
        self.church_slider = Slider((640, 175), 300, 0, 1, 1, .05, GREEN, WHITE, self.caption_font, "Heat", (310, 20))
        self.bus_slider = Slider((640, 250), 300, 0, 1, 1, .05, GREEN, WHITE, self.caption_font, "Heat", (310, 20))
        self.restaurant_slider = Slider((640, 325), 300, 0, 1, 1, .05, GREEN, WHITE, self.caption_font, "Heat", (310, 20))
        self.groceries_slider = Slider((640, 400), 300, 0, 1, 1, .05, GREEN, WHITE, self.caption_font, "Heat", (310, 20))
        self.social_slider = Slider((640, 475), 300, 0, 1, 1, .05, GREEN, WHITE, self.caption_font, "Heat", (310, 20))

    def update_heatmap(self):
        if self.heat_map_check == 0:
            self.heat_map_yes.color = WHITE
            self.heat_map_no.color = GREEN
            self.weighted_heat_map.color = GREEN
        elif self.heat_map_check == 1:
            self.heat_map_yes.color = GREEN
            self.heat_map_no.color = WHITE
            self.weighted_heat_map.color = GREEN
        elif self.heat_map_check == 2:
            self.heat_map_yes.color = GREEN
            self.heat_map_no.color = GREEN
            self.weighted_heat_map.color = WHITE

    def update_seed_set(self, selection):
        for i in self.seed_sets:
            if i == selection:
                i.color = WHITE
            else:
                i.color = GREEN

    def main_menu(self):
        running = True
        while running:
            self.screen.fill(self.BLACK)
            menu_text = self.menu_font.render("Voronoi Generator", True, WHITE)
            menu_rect = menu_text.get_rect(center=(640, 100))
            self.screen.blit(menu_text, menu_rect)

            self.play_button.update(self.screen)
            self.options_button.update(self.screen)
            self.quit_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.checkForInput(event.pos):
                        loading_text = self.caption_font.render("Loading...", True, WHITE)
                        loading_rect = loading_text.get_rect(center=(50, 700))
                        self.screen.blit(loading_text, loading_rect)
                        running = False
                    elif self.options_button.checkForInput(event.pos):
                        self.options()
                    elif self.quit_button.checkForInput(event.pos):
                        pygame.quit()
                        quit()

            pygame.display.flip()

    def options(self):
        self.update_heatmap()
        while True:
            self.screen.fill(self.BLACK)

            options_text = self.menu_font.render("Options", True, WHITE)
            options_rect = options_text.get_rect(center=(640, 50))
            self.screen.blit(options_text, options_rect)

            self.options_back.update(self.screen)
            self.choose_voronoi.update(self.screen)
            self.heat_map_yes.update(self.screen)
            self.heat_map_no.update(self.screen)
            self.weighted_heat_map.update(self.screen)
            self.heat_multiplier_slider.update(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.options_back.checkForInput(event.pos):
                        return
                    elif self.choose_voronoi.checkForInput(event.pos):
                        self.choose_voronoi_screen()
                    elif self.heat_map_yes.checkForInput(event.pos):
                        self.heat_map_check = 0
                        self.update_heatmap()
                    elif self.heat_map_no.checkForInput(event.pos):
                        self.heat_map_check = 1
                        self.update_heatmap()
                    elif self.weighted_heat_map.checkForInput(event.pos):
                        self.heat_map_check = 2
                        self.update_heatmap()
                self.heat_multiplier_slider.handleEvent(event)
                self.heat_multiplier = self.heat_multiplier_slider.value

    def choose_voronoi_screen(self):
        while True:
            self.screen.fill(self.BLACK)

            voronoi_title = self.menu_font.render("Voronoi Seed Sets", True, (255, 255, 255))
            voronoi_rect = voronoi_title.get_rect(center=(640, 50))
            self.screen.blit(voronoi_title, voronoi_rect)

            self.voronoi_back.update(self.screen)
            self.schools.update(self.screen)
            self.churches.update(self.screen)
            self.bus_stops.update(self.screen)
            self.restaurants.update(self.screen)
            self.groceries.update(self.screen)
            self.social_facilities.update(self.screen)
            # self.parks.update(self.screen)
            self.schools_slider.update(self.screen)
            self.church_slider.update(self.screen)
            self.bus_slider.update(self.screen)
            self.restaurant_slider.update(self.screen)
            self.groceries_slider.update(self.screen)
            self.social_slider.update(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.voronoi_back.checkForInput(event.pos):
                        return
                    elif self.schools.checkForInput(event.pos):
                        self.update_seed_set(self.schools)
                        self.voronoi_selection = self.schools.text_input
                    elif self.churches.checkForInput(event.pos):
                        self.update_seed_set(self.churches)
                        self.voronoi_selection = self.churches.text_input
                    elif self.bus_stops.checkForInput(event.pos):
                        self.update_seed_set(self.bus_stops)
                        self.voronoi_selection = self.bus_stops.text_input
                    elif self.restaurants.checkForInput(event.pos):
                        self.update_seed_set(self.restaurants)
                        self.voronoi_selection = self.restaurants.text_input
                    elif self.groceries.checkForInput(event.pos):
                        self.update_seed_set(self.groceries)
                        self.voronoi_selection = self.groceries.text_input
                    elif self.social_facilities.checkForInput(event.pos):
                        self.update_seed_set(self.social_facilities)
                        self.voronoi_selection = self.social_facilities.text_input
                    # elif self.parks.checkForInput((event.pos)):
                    #     self.update_seed_set(self.parks)
                    #     self.voronoi_selection = self.parks.text_input
                self.schools_slider.handleEvent(event)
                self.heat_weights[0] = self.schools_slider.value
                self.church_slider.handleEvent(event)
                self.heat_weights[1] = self.church_slider.value
                self.bus_slider.handleEvent(event)
                self.heat_weights[2] = self.bus_slider.value
                self.restaurant_slider.handleEvent(event)
                self.heat_weights[3] = self.restaurant_slider.value
                self.groceries_slider.handleEvent(event)
                self.heat_weights[4] = self.groceries_slider.value
                self.social_slider.handleEvent(event)
                self.heat_weights[5] = self.social_slider.value





if __name__ == "__main__":
    display = DisplayMenu()


'''
Pygame GUI Inspiration from https://github.com/baraltech/Menu-System-PyGame/tree/main
'''
