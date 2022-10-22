import pygame
import csv

pygame.init()

screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("Movie Theater Booking System")

def adminMain():
    pass

def cashierMain():
    pass

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.display.update()
pygame.quit()