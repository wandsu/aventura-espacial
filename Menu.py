import os
import csv
import pygame
from ranking import *
from pygame.locals import *

from Players import *

pygame.init()

screen_width=800
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))

white=(255, 255, 255)
red=(255, 0, 0)

font = "fonts/Retro.ttf"

bg_menu = pygame.image.load("Imagens/menu.jpg")
bg_menu = pygame.transform.scale(bg_menu, (800, 600))

menu_music = 'Sounds/Take-on-me.ogg'
fase_um_music = 'Sounds/Eletro-hits.ogg'

clock = pygame.time.Clock()
FPS=60

CameraX = 0
attempts = 0
coins = 0
angle = 0

lava = pygame.image.load(os.path.join("Imagens", "Lava.png"))
lava = pygame.transform.smoothscale(lava, (32,32))
end = pygame.image.load(os.path.join("Imagens", "red-end.png"))
coin = pygame.image.load(os.path.join("Imagens", "coin.png"))
coin = pygame.transform.smoothscale(coin, (32, 32))
bloco1 = pygame.image.load(os.path.join("Imagens", "Deserto Sheet 1.png"))
bloco1 = pygame.transform.smoothscale(bloco1, (32, 32))
bloco2 = pygame.image.load(os.path.join("Imagens", "Deserto Sheet 2.png"))
bloco2 = pygame.transform.smoothscale(bloco2, (32, 32))
bloco3 = pygame.image.load(os.path.join("Imagens", "Deserto Sheet 3.png"))
bloco3 = pygame.transform.smoothscale(bloco3, (32, 32))
bloco4 = pygame.image.load(os.path.join("Imagens", "Deserto Sheet 4.png"))
bloco4 = pygame.transform.smoothscale(bloco4, (32, 32))
bloco5 = pygame.image.load(os.path.join("Imagens", "Deserto Sheet 5.png"))
bloco5 = pygame.transform.smoothscale(bloco5, (32, 32))
bloco6 = pygame.image.load(os.path.join("Imagens", "Deserto Sheet 6.png"))
bloco6 = pygame.transform.smoothscale(bloco6, (32, 32))
bloco7 = pygame.image.load(os.path.join("Imagens", "Deserto Sheet 7.png"))
bloco7 = pygame.transform.smoothscale(bloco7, (32, 32))
bloco8 = pygame.image.load(os.path.join("Imagens", "Deserto Sheet 8.png"))
bloco8 = pygame.transform.smoothscale(bloco8, (32, 32))

#definindo elementos do jogo
player_sprite = pygame.sprite.Group()
elements = pygame.sprite.Group()
## definindo sprites do jogador
sprites = pygame.sprite.Group()
jogador = Player(elements, (150, 150), player_sprite)
sprites.add(jogador)

def player():
    player_sprite = pygame.sprite.Group()
    elements = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    jogador = Player(elements, (150, 150), player_sprite)
    sprites.add(jogador)
    return sprites, jogador

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText

#carrega mapa do jogo
def carrega_mapa(map):
    x = 0
    y = 0

    for row in map:
        for col in row:
            if col == "1":
                Platform1(bloco1, (x, y), elements)

            if col == "2":
                Platform2(bloco2, (x,y), elements)

            if col == "3":
                Platform2(bloco3, (x,y), elements)

            if col == "4":
                Platform2(bloco4, (x,y), elements)

            if col == "5":
                Platform2(bloco5, (x,y), elements)

            if col == "6":
                Platform2(bloco6, (x,y), elements)

            if col == "7":
                Platform2(bloco7, (x,y), elements)

            if col == "8":
                Platform2(bloco8, (x,y), elements)

            if col == "Coin":
                Coin(coin, (x, y), elements)

            if col == "L":
                Lava(lava, (x, y), elements)

            if col == "End":
                End(end, (x, y), elements)
            x += 32
        y += 32
        x = 0

def block_map(level_num):
    lvl = []
    with open(level_num, newline='') as csvfile:
        trash = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in trash:
            lvl.append(row)
    return lvl

def reset():
    global jogador, elements, player_sprite, level, sprites

    if level == 1:
        pygame.mixer.music.load(os.path.join("Sounds", "Eletro-hits.ogg"))
    pygame.mixer_music.play()
    player_sprite = pygame.sprite.Group()
    elements = pygame.sprite.Group()
    jogador = Player(elements, (150, 150), player_sprite)
    sprites.add(jogador)
    carrega_mapa(
            block_map(
                    level_num=levels[level]))

def move_map():
    for sprite in elements:
        sprite.rect.x -= CameraX

def game_over():
    reset()

def winner():
    reset()
    main_menu

atualiza_sprite = 0
#inicio do jogo
def level_1():
    # bg image
    pygame.mixer.music.load(fase_um_music)
    pygame.mixer.music.play()
    bg = pygame.image.load(os.path.join("Imagens", "bg.png"))
    bg = pygame.transform.scale(bg,(800,600))
    print('Game init')
    global CameraX
    global atualiza_sprite
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        sprites.draw(screen)

        #atualiza sprite após 4 loops se o jogador não estiver pulando
        atualiza_sprite += 1
        if atualiza_sprite % 5 == 0 and not jogador.isjump:
            jogador.sprite_update()

        sprites.update()

        jogador.vel.x = 10

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            jogador.isjump = True
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()



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

        #Verifica se o jogador morreu
        if jogador.died:
            game_over()
        
        clock.tick(60)
        pygame.display.update()    

def ranking_screen():
    bg = pygame.image.load(os.path.join("Imagens", "fundo_ranking.jpg"))
    bg = pygame.transform.scale(bg,(800,600))

    text_rank=text_format("Ranking", font, 75, red)
    menu=text_format("Menu", font, 65, red)
    
    ranking = True
    fonteLinhas = pygame.font.Font(font, 45)
    dados = CSVReader()

    count = 100
    screen.blit(bg, (0, 0))  
    screen.blit(text_rank, (300, 0))
    screen.blit(menu, (600, 500))
    i = 0
    while i < len(dados) or i <= 10:
        try:
            texto = (dados[i][0])
            numero = (dados[i][1])
            text = fonteLinhas.render(texto, True, white)
            pontos = fonteLinhas.render(numero, True, white)
            screen.blit(text,(150,count))
            screen.blit(pontos,(550,count))
            count += 45
        except(IndexError):
            texto +=('-------------------------\n')
        i += 1
    
    while ranking:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    main_menu()

        pygame.display.update()
        clock.tick(FPS)

#menu
def main_menu():
    menu=True
    selected="Iniciar"
    pygame.mixer.init()
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play() 
    menu_estados = 0
    som = ["Som: on","Som: off"]
    set_som = 0
    som_menu = som[0]
    
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key==pygame.K_UP:
                    menu_estados -= 1
                if event.key==pygame.K_DOWN:
                    menu_estados += 1
                if event.key==pygame.K_RETURN:
                    if selected=="Iniciar":
                        level_1()
                    if selected == som_menu:
                        set_som+=1
                        print(som[set_som%2])
                        som_menu = som[set_som%2]
                        if set_som%2 == 0:
                            pygame.mixer.music.play() 
                        else:
                            pygame.mixer.music.pause()
                    if selected=="Rank":
                        ranking_screen()
                    if selected=="Sair":
                        pygame.quit()
                        quit()

        screen.blit(bg_menu, (0, 0))

        #Defini item selecionado pelo 
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

        #Altera cor do item do menu que está selecionado
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
