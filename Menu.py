import pygame
from pygame.locals import *
import os
from Players import *
import csv

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

bg_menu = pygame.image.load("imagens\menu.jpg")
bg_menu = pygame.transform.scale(bg_menu, (800, 600))

menu_music = 'Sounds\Take-on-me.ogg'

clock = pygame.time.Clock()
FPS=30

#  ints
fill = 0
num = 0
CameraX = 0
attempts = 0
coins = 0
angle = 0

# bg image
bg = pygame.image.load(os.path.join("Imagens", "bg.png"))
bg = pygame.transform.scale(bg,(800,600))

#definindo elementos do jogo
player_sprite = pygame.sprite.Group()
elements = pygame.sprite.Group()
lava = pygame.image.load(os.path.join("Imagens", "Lava.png"))
lava = pygame.transform.smoothscale(lava, (32,32))
end = pygame.image.load(os.path.join("Imagens", "red-end.png"))
#end = pygame.transform.smoothscale(end, (290,570))
coin = pygame.image.load(os.path.join("Imagens", "coin.png"))
coin = pygame.transform.smoothscale(coin, (32, 32))
bloco1 = pygame.image.load(os.path.join("Imagens", "Deserto1.png"))
bloco1 = pygame.transform.smoothscale(bloco1, (32, 32))
bloco2 = pygame.image.load(os.path.join("Imagens", "Deserto Sheet 2.png"))
bloco2 = pygame.transform.smoothscale(bloco2, (32, 32))

## definindo sprites do jogador
sprites = pygame.sprite.Group()
jogador = Player(elements, (150, 150), player_sprite)
sprites.add(jogador)


#carrega mapa do jogo
def carrega_mapa(map):
    x = 0
    y = 0

    for row in map:
        for col in row:

            if col == "0":
                Platform1(bloco1, (x, y), elements)
            if col == "1":
                Platform2(bloco2, (x,y), elements)

            if col == "Coin":
                Coin(coin, (x, y), elements)

            if col == "Lava":
                Lava(lava, (x, y), elements)

            if col == "End":
                End(end, (x, y), elements)
            x += 32
        y += 32
        x = 0

def vitoria():
    return 0

def derrota():
    return 1

def block_map(level_num):
    lvl = []
    with open(level_num, newline='') as csvfile:
        trash = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in trash:
            lvl.append(row)
    return lvl

def reset():
    global jogador, elements, player_sprite, level

    if level == 1:
        pygame.mixer.music.load(os.path.join("Sounds", "Eletro-hits.ogg"))
    pygame.mixer_music.play()
    player_sprite = pygame.sprite.Group()
    elements = pygame.sprite.Group()
    jogador = Player(elements, (150, 150), player_sprite)
    carrega_mapa(
            block_map(
                    level_num=levels[level]))

def move_map():
    for sprite in elements:
        sprite.rect.x -= CameraX





#inicio do jogo
def game():
    global CameraX
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        sprites.draw(screen)
        sprites.update()

        #
        jogador.vel.x = 5 

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            jogador.isjump = True


        CameraX = jogador.vel.x  
        move_map()  

        screen.blit(bg, (0, 0))  


        player_sprite.draw(screen)  
        elements.draw(screen) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_2:
                    jogador.jump_amount += 1

                if event.key == pygame.K_1:

                    jogador.jump_amount -= 1


        #
        clock.tick(60)
        pygame.display.update()    


#menu
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
                        game()
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

        screen.blit(bg_menu, (0, 0))
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

#globais

#nivel
level_num = 1
level = 0
levels = ["level_1.csv", "level_2.csv"]
level_list = block_map(levels[level])
level_width = (len(level_list[0]) * 32)
level_height = len(level_list) * 32
carrega_mapa(level_list)

main_menu()
pygame.quit()
quit()
