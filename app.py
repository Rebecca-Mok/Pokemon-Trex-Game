import pygame
import pygame.freetype
from random import randrange
pygame.init()

win = pygame.display.set_mode((800, 350))
pygame.display.update()
pygame.display.set_caption("First Game")

walking = [pygame.image.load('sprites/pikachu1.png'), pygame.image.load('sprites/pikachu2.png'), pygame.image.load('sprites/pikachu3.png'), pygame.image.load('sprites/pikachu4.png')]
enemyMove = pygame.image.load('sprites/pokemonBall1.png')
bg = pygame.image.load('images/background.png')
skyView = pygame.image.load('images/clouds.png')
start = False #True when space is pressed
pygame.time.get_ticks()/1000
font = pygame.font.SysFont("Times New Roman", 30)
font2 = pygame.font.SysFont("Times New Roman", 25)
clock = pygame.time.Clock()


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0  
        self.hitbox = (self.x, self.y, 110, 75) 
        self.score = 0
        self.runCount = 0
        self.score = 0

    def draw(self, win):
        if start:
            if self.walkCount + 1 >= 8:
                self.walkCount = 0
                self.runCount += 1

            if self.isJump:
                win.blit(walking[2], (self.x, self.y))
            else:
                win.blit(walking[self.walkCount//2], (self.x, self.y))
                self.walkCount += 1
        else:
            win.blit(walking[1], (50,250))

        # Hit Box
        self.hitbox = (self.x+30, self.y+5, 80, 60) 
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 50
        self.y = 250
        self.walkCount = 0
        self.runCount = 0
        start = False

        for i in range (3):
            if self.score > topThreeScores[i]:
                topThreeScores.insert(i, self.score)
                break
        self.score = 0

        for attack in enemies:
            enemies.pop(enemies.index(attack))

        for cloud in clouds:
            clouds.pop(clouds.index(cloud))

        enemies.append(enemy(800, 290, 34, 34))
        clouds.append(sky(800,0,800))
        clouds.append(sky(0,0,800))

        i = 0
        while i<100:
            pygame.time.delay(10)
            i += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        

class enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [self.x, self.y]
        self.vel = 8 # velocity will increase with time
        self.hitbox = (self.x, self.y, 35, 35) 
    
    def draw(self, win):
        if start:
            self.move()
            win.blit(enemyMove, (self.x,self.y))
            
            # Hitbox
            self.hitbox = (self.x, self.y, 35, 35) 
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        self.x -= self.vel

class sky(object):
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.path = [self.x, self.y]
        self.vel = 1


    def draw(self, win):
        if start:
            self.move()
            win.blit(skyView, (self.x,self.y))
        else:
            win.blit(skyView,(0,0))

    def move(self):
        self.x -= self.vel


def checkHit(char, enemies):
    for enemy in enemies:
        if char.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and char.hitbox[1] + char.hitbox[3] > enemy.hitbox[1]:
            if char.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2] and char.hitbox[0] + char.hitbox[2] > enemy.hitbox[0]:  
                char.hit()
                for enemy in enemies:
                    enemies.pop(enemies.index(enemy))
                    



def redrawGameWindow():
    win.blit(bg, (0,0))
    char.draw(win)
    for cloud in clouds:
        cloud.draw(win)

    for attack in enemies:
        attack.draw(win)
    if start:
        char.score += 0.5
        
    text = font.render('Score: ' + str(int(char.score)), 1, (0,0,0))
    win.blit(text, (350, 10))


    pygame.draw.rect(win, (255,255,255), (670, 10, 120, 150))
    top = font2.render('TOP SCORE', 1, (0,0,0))
    win.blit(top, (680, 30))
    top = font2.render("1. " + str(int(topThreeScores[0])), 1, (0,0,0))
    win.blit(top, (680, 55))
    top = font2.render("2. " + str(int(topThreeScores[1])), 1, (0,0,0))
    win.blit(top, (680, 80))
    top = font2.render("3. " + str(int(topThreeScores[2])), 1, (0,0,0))
    win.blit(top, (680, 105))

    pygame.display.update()




char = player(50, 250, 64, 64)
enemies = []
clouds = [sky(0,0,800), sky(800,0,800)]
run = True
topThreeScores = [0,0,0]

while run:

    clock.tick(28 + char.runCount/5) #Frames per second
    
    # check if charcter hits block
    if start:
        checkHit(char, enemies)
        rand = randrange(450, 800)
        if char.runCount>8:
            if len(enemies) == 0:
                enemies.append(enemy(800, 290, 34, 34))
            
            elif enemies[-1].x <800-rand:
                num = randrange(3)
                if num == 0:
                    enemies.append(enemy(800, 290, 34, 34))
                elif num == 1:
                    enemies.append(enemy(800, 290, 34, 34))
                    enemies.append(enemy(835, 290, 34, 34))   
                else:
                    enemies.append(enemy(800, 290, 34, 34))
                    enemies.append(enemy(835, 290, 34, 34))        
                    enemies.append(enemy(870, 290, 34, 34))  

        if clouds[-1].x + clouds[-1].width ==795:
            clouds.append(sky(800,0,800))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for attack in enemies:
        if attack.x + attack.width> 0 :
            attack.x -= attack.vel
        else:
            enemies.pop(enemies.index(attack))

    for cloud in clouds:
        if cloud.x + cloud.width > 0:
            cloud.x -= cloud.vel
        else:
            clouds.pop(clouds.index(cloud))
            clouds.append(sky(800,0,800))
       


    keys = pygame.key.get_pressed()
    if not (char.isJump):
        if keys[pygame.K_SPACE]: 
            char.isJump = True
    else:
        start = True
        if char.jumpCount >= -10:
            neg = 1
            if char.jumpCount < 0:
                neg = -1
            char.y -= char.jumpCount ** 2 * 0.3 * neg
            char.jumpCount -= 1
        else:
            char.isJump = False
            char.jumpCount = 10
    
    redrawGameWindow()

pygame.quit()