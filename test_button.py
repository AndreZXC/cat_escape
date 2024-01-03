import pygame
import os
import sys


pygame.init()
size = width, height = 720, 720
screen = pygame.display.set_mode(size)
tile_width = tile_height = 36


def load_image(name):
    fullname = os.path.join('textures', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


background_image = pygame.transform.smoothscale(load_image('background.png'), (width, height))
button_gr = pygame.sprite.Group()
button = pygame.sprite.Sprite(button_gr)
button.image = pygame.transform.smoothscale(load_image('buttons\\start.png'), (270, 81))
button.rect = button.image.get_rect().move(10, 10)
plaing = True
while plaing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            plaing = False
    pygame.display.flip()
    screen.blit(background_image, (0, 0))
    button_gr.draw(screen)