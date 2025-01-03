import pygame


class Button:
    def __init__(self, image, pos, text_input, font, color, centered):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.color = color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.color)
        if self.image is None:
            self.image = self.text
        if centered:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.x_pos, self.y_pos
            self.text_rect = self.text.get_rect()
            self.text_rect.x, self.text_rect.y = self.x_pos, self.y_pos

    def update(self, screen):
        self.text = self.font.render(self.text_input, True, self.color)

        if self.image is not None:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False


class Slider:
    def __init__(self, pos, width, min_value, max_value, initial_value, increment, slider_color, track_color, font, text_input, text_pos):
        self.pos = pos
        self.width = width
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.slider_color = slider_color
        self.track_color = track_color
        self.font = font
        self.text_input = text_input
        self.text = self.font.render(f'{self.text_input}: {self.value}', True, (255, 255, 255))
        self.text_pos = text_pos
        self.text_rect = self.text.get_rect(topleft=(self.pos[0] + self.text_pos[0], self.pos[1] + self.text_pos[1]))
        self.dragging = False
        self.increment = increment

    def update(self, screen):
        pygame.draw.rect(screen, self.track_color, (self.pos[0], self.pos[1] + 30, self.width, 10)) # Slider track
        slider_pos = self.pos[0] + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width) # Slider pos
        center = (slider_pos, self.pos[1] + 35)
        pygame.draw.circle(screen, self.slider_color, center, 8)

        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        slider_rect = pygame.Rect(self.pos[0], self.pos[1], self.width, 40)
        if slider_rect.collidepoint(position):
            return True
        return False

    def updateValue(self, position):
        if self.dragging:
            new_value = round((position[0] - self.pos[0]) / self.width * (self.max_value - self.min_value) + self.min_value, 2)
            self.value = round(max(self.min_value, min(new_value - (new_value % self.increment), self.max_value)), 2)
            self.text = self.font.render(f"{self.text_input}: {self.value}", True, (255, 255, 255))
            self.text_rect = self.text.get_rect(topleft=(self.pos[0] + self.text_pos[0], self.pos[1] + self.text_pos[1]))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.checkForInput(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.updateValue(event.pos)






'''
Pygame GUI Inspiration from https://github.com/baraltech/Menu-System-PyGame/tree/main
'''
