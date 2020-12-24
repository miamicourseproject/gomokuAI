import pygame

# Generating screen
w_scr = 640
h_scr = 480
size_scr = (w_scr, h_scr)
screen = pygame.display.set_mode(size_scr)

# Define color
COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

class DropDown():

    def __init__(self, colorMenu, colorOption, x, y, w, h, font, main, options):
        self.colorMenu = colorMenu
        self.colorOption = colorOption
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.drawMenu = False
        self.menuActive = False
        self.activeOption = -1
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def draw(self, surf, outline = None):
        if outline:
            pygame.draw.rect(surf, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(surf, self.colorMenu[self.menuActive], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.drawMenu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.colorOption[1 if i == self.activeOption else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))

    def update(self, event_list, pos):
        self.menuActive = self.rect.collidepoint(pos)
        
        self.activeOption = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(pos):
                self.activeOption = i
                break

        if not self.menuActive and self.activeOption == -1:
            self.drawMenu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menuActive:
                    self.drawMenu = not self.drawMenu
                elif self.drawMenu and self.activeOption >= 0:
                    self.drawMenu = False
                    return self.activeOption
        return -1