import pygame
from pygame.math import Vector2
from pygame.draw import rect
import random

pygame.mixer.init()
# jump_sound = pygame.mixer.Sound('Sounds/Jump.ogg')

#gravidade
color = lambda: tuple([random.randint(0, 255) for i in range(3)])  # lambda function for random color, not a constant.
GRAVITY = Vector2(0, 1) 
alpha_surf = pygame.Surface((800,600), pygame.SRCALPHA)

class Player(pygame.sprite.Sprite):

    def __init__(self, platforms, pos, *groups):
        super().__init__(*groups)
        self.sprites = []
        self.sprites.append(pygame.image.load('Imagens/Mark1.png'))
        self.sprites.append(pygame.image.load('Imagens/Mark2.png'))
        self.sprites.append(pygame.image.load('Imagens/Mark3.png'))
        self.sprites.append(pygame.image.load('Imagens/Mark2.png'))

        self.jumping = pygame.image.load('Imagens/Mark4.png')

        self.platforms = platforms
        self.onGround = False
        self.isRunning = False
        self.atual = 0
        self.coins = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (64,64)) 

        self.rect = self.image.get_rect(center=pos)
        self.jump_amount = 15  
        # self.jump_sound = jump_sound
        self.isjump = False 
        self.vel = Vector2(0, 0) 
        self.win = False
        self.died = False
    
    def jump(self):
        # self.jump_sound.play()
        self.vel.y = -self.jump_amount  
        self.image = self.jumping
        self.image = pygame.transform.scale(self.image, (64,64)) 

    #Adicionei essa função para separar a atualização do sprite do movimento do jogador
    def sprite_update(self):
        self.atual = self.atual +1
        self.image = self.sprites[self.atual%4]
        self.image = pygame.transform.scale(self.image, (64,64)) 


    def update(self):
        if self.isjump:
            if self.onGround:
                self.jump()

        if not self.onGround:  
            self.vel += GRAVITY  

            
        if self.vel.y > 100: self.vel.y = 100

        self.collide(0, self.platforms)

        self.rect.top += self.vel.y

        self.onGround = False

        self.collide(self.vel.y, self.platforms)
    
    def collide(self, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, End):
                    self.win = True

                if isinstance(p, Lava):
                    self.died = True

                if isinstance(p, Coin):
                    self.coins += 1
                    p.rect.x = 0
                    p.rect.y = 0

                if isinstance(p, Platform1):

                    if yvel > 0:
                        self.rect.bottom = p.rect.top 
                        self.vel.y = 0  

                        self.onGround = True

                        self.isjump = False
                    elif yvel < 0:
                        self.rect.top = p.rect.bottom
                    else:
                        self.vel.x = 0
                        self.rect.right = p.rect.left 
                        self.died = True
                if isinstance(p, Platform2):
                    continue
                        

class Draw(pygame.sprite.Sprite):
    def __init__(self, image, pos, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

class Platform1(Draw):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)

class Platform2(Draw):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)

class Lava(Draw):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)

class Coin(Draw):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)

class End(Draw):
    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)



