import pygame
import random
from datetime import timedelta, datetime
pygame.init()

class Zombie:
    def __init__(self, pos, health):
        self.pos = pos
        self.health = health

class Chicken:
    def __init__(self, pos):
        self.pos = pos

playerx = 520
playerSpeed = 0
tower1width = 50
tower1height = 50
tower1RBG = 0,160,160
chickens = []
enemys = []
enemyX, enemyY = 525, -50
zombieS = 0.1
lives = 1
spawnzombie = datetime.now() + timedelta(seconds = (random.randint(1, 3)))
endgame = False

win = pygame.display.set_mode((1100,700))

pygame.display.set_caption('cool game')
run = True
while run:
    ###################################
    # Clear the screen for this frame #
    ###################################
    win.fill((230,230,230)) 

    ############################################
    # Handle stuff that the user has done here #
    ############################################
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            chickens.append(Chicken((playerx + 5, 575)))
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerSpeed = 0.5
            if event.key == pygame.K_LEFT:
                playerSpeed = -0.5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if playerSpeed > 0:
                    playerSpeed = 0

            if event.key == pygame.K_LEFT:
                if playerSpeed < 0:
                    playerSpeed = 0

    #########################################
    # Update the position of all the things #
    #########################################
    if datetime.now() > spawnzombie:
        enemys.append(Zombie((random.randint(200, 900), 0), 2))
        spawnzombie = spawnzombie + timedelta(seconds = random.randint(0, 1))

    enemysToDelete = []
    for enemy in enemys:
        enemy.pos = (enemy.pos[0], enemy.pos[1] + zombieS)
        if enemy.pos[1] > 700:
           enemysToDelete.append(enemy)
           lives = lives - 1

    
    chickensToDelete = []
    for chicken in chickens:
        chicken.pos = (chicken.pos[0], chicken.pos[1] - 0.3)
        if chicken.pos[1] < -50:
           chickensToDelete.append(chicken)

    
    for enemy in enemys:
        for chicken in chickens:
            hasHit = False
            if (enemy.pos[1] + 50) > chicken.pos[1] and (enemy.pos[0] < (chicken.pos[0] + 50) and enemy.pos[0] + 50 > chicken.pos[0]):
                hasHit = True

            if hasHit == True:
                if chickensToDelete.__contains__(chicken) == False:
                    chickensToDelete.append(chicken)
                enemy.health = enemy.health - 1
                if enemy.health == 0:
                    if enemysToDelete.__contains__(enemys) == False:
                        enemysToDelete.append(enemy)

    for enemy in enemysToDelete:
        if (enemys.__contains__(enemy)):
            enemys.remove(enemy)

    for chicken in chickensToDelete:
        if (chickens.__contains__(chicken)):
            chickens.remove(chicken)

    playerx = playerx + playerSpeed

    if playerx < 0:
        playerx = 0

    if playerx > 1040:
        playerx = 1040

    #################################
    # Draw stuff on the screen here #
    ################################# 
    for tower in chickens:
        pygame.draw.rect((win), (tower1RBG), (tower.pos[0], tower.pos[1], tower1width, tower1height))

    for enemy in enemys:
        if enemy.health > 1:
            pygame.draw.rect((win), (130,20,20), (enemy.pos[0], enemy.pos[1], tower1width, tower1height)) 
        else:
            pygame.draw.rect((win), (130,100,100), (enemy.pos[0], enemy.pos[1], tower1width, tower1height)) 

    pygame.draw.rect((win), (130,130,130), (playerx, 600, 60, 70)) 
     
    if lives < 1:
        enemys.clear
        endgame = True
            
    #print(lives)

    pygame.display.flip()
