import pygame
import os


FILE_DIR = os.path.dirname(__file__)
screen = pygame.display.set_mode((500, 500))
level = []

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

    def return_action(self):
        return self.clicked

def loadLevel(num):
    level.clear()

    levelFile = open(f'%s/levels/{num}.txt' % FILE_DIR)
    line = " "
    commands = []
    while line[0] != "/": 
        line = levelFile.readline() 
        if line[0] == "[": 
            while line[0] != "]": 
                line = levelFile.readline() 
                if line[0] != "]": 
                    endLine = line.find("|") 
                    level.append(line[0: endLine])









