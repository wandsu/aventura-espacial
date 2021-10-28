import pygame
from pygame.locals import *
import os

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

screen_width=800
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText

white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

font = "fonts\Retro.ttf"

bg = pygame.image.load("imagens\menu.jpg")
bg = pygame.transform.scale(bg, (800, 600))

menu_music = 'Sounds\Take-on-me.ogg'

clock = pygame.time.Clock()
FPS=30

def main_menu():

    menu=True
    selected="Iniciar"
    pygame.mixer.init()
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play() 
    menu_estados = 0
    som = ["Som: on","Som: off"]
    i = 0
    som_menu = som[0]
    

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    menu_estados -= 1
                elif event.key==pygame.K_DOWN:
                    menu_estados += 1
                if event.key==pygame.K_RETURN:
                    if selected=="Iniciar":
                        print("Iniciar")
                    if selected == som_menu:
                        i+=1
                        print(i)
                        som_menu = som[i%2]
                        if i%2 == 0:
                            pygame.mixer.music.play() 
                        else:
                            pygame.mixer.music.pause()
                    if selected=="Rank":
                        print("Rank")
                    if selected=="Sair":
                        pygame.quit()
                        quit()

        screen.blit(bg, (0, 0))
        if menu_estados < 0:
            menu_estados = 3
        if menu_estados > 3:
            menu_estados = 0
        if menu_estados ==0:
            selected = "Iniciar"
        elif menu_estados == 3:
            selected = "Sair"
        elif menu_estados ==1:
            selected = som_menu
        elif menu_estados == 2:
            selected = "Rank"


        if selected=="Iniciar":
            text_start=text_format("Iniciar", font, 75, red)
        else:
            text_start = text_format("Iniciar", font, 75, white)
        if selected==som_menu:
            text_sound=text_format(som_menu, font, 75, red)
        else:
            text_sound = text_format(som_menu, font, 75, white)    
        if selected=="Sair":
            text_quit=text_format("Sair", font, 75, red)
        else:
            text_quit = text_format("Sair", font, 75, white)
        if selected=="Rank":
            text_rank=text_format("Rank", font, 75, red)
        else:
            text_rank = text_format("Rank", font, 75, white)

        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
        rank_rect=text_rank.get_rect()
        sound_rect=text_sound.get_rect()

        screen.blit(text_start, (screen_width/2 - (-180), 200))
        screen.blit(text_quit, (screen_width/2 - (-180), 350))
        screen.blit(text_sound, (screen_width/2 - (-180), 250))
        screen.blit(text_rank, (screen_width/2 - (-180), 300))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Uma Aventura Espacial")

main_menu()
pygame.quit()
quit()
