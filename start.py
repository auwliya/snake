import pygame, sys, os
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
pygame.display.set_caption('snake')
screen = pygame.display.set_mode((500, 500),0,32)
 
font_title = pygame.font.Font('Font/ARCADECLASSIC.ttf',35)
font = pygame.font.Font('Font/ARCADECLASSIC.ttf',25)
font_small = pygame.font.Font('Font/ARCADECLASSIC.ttf',15)
 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
play_button = pygame.image.load('Graphics/play_button.png').convert_alpha()
HTP_button = pygame.image.load('Graphics/HTP.png').convert_alpha()
WASD_button = pygame.image.load('Graphics/WASDexpl.png').convert_alpha()

click = False
 
def main_menu():
    while True:
        screen.fill((175,215,70))
        draw_text('main menu', font_title, (56,74,12), screen, 20, 20)
        draw_text('Snake  made  by  Auwliya', font_small, (56,74,12), screen, 10, 480)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(20, 70, 100, 50)
        screen.blit(play_button, button_1)
        
        button_2 = pygame.Rect(20, 145, 100, 50)
        screen.blit(HTP_button, button_2)
        
        if button_1.collidepoint((mx, my)):
            if click:
                os.system('cmd /k start snake-project.py')
                pygame.quit
                sys.exit
        
        elif button_2.collidepoint((mx, my)):
            if click:
                How_to_play()
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)

def How_to_play():
    running = True
    while running:
        screen.fill((175,215,70))
        draw_text('How  to  play', font_title, (56,74,12), screen, 20, 20)
        draw_text('You  can  move  the  snake  around', font, (56,74,12), screen, 20, 50)
        draw_text('Using  the  arrow  keys  or  WASD', font, (56,74,12), screen, 20, 65)
        draw_text('Eat the apples and lemons to grow', font, (56,74,12), screen, 20, 95)
        draw_text('Apples are 1 point and lemons 2', font, (56,74,12), screen, 20, 125)
        draw_text('If you crash into a wall or  yourself', font, (56,74,12), screen, 20, 155)
        draw_text('You lose the game', font, (56,74,12), screen, 20, 170)
        draw_text('You can use esc to go back', font, (56,74,12), screen, 20, 200)

        explanation = pygame.Rect(20, 225, 200, 200)
        screen.blit(WASD_button,explanation)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)
 
main_menu()