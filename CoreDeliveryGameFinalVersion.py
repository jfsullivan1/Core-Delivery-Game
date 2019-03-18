"""cdSpaceship.py
    John Sullivan
    This is the final version of the Core Delivery Game!
    Coded by John Sullivan
"""

import pygame
import random
pygame.init()

screen = pygame.display.set_mode((640, 800))
pygame.display.set_caption("cdSpaceship.py")
myFont = pygame.font.SysFont("Comic Sans MS", 20)
if not pygame.mixer:
    print ("problem with sound")
else:
    pygame.mixer.init()



class Spaceship(pygame.sprite.Sprite):
    def __init__(self,laserGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Spaceship.jpg")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.laserGroup = laserGroup
        self.sndShip = pygame.mixer.Sound("ship.wav")
        self.sndCore = pygame.mixer.Sound("core.wav")
        self.sndCrash = pygame.mixer.Sound("crash.wav")
        self.sndLaser = pygame.mixer.Sound("laser.wav")
        if not pygame.mixer:
            print ("problem with sound")
        else:
            self.sndShip.play(-1)

    def update(self):
        shipx, shipy = pygame.mouse.get_pos()
        self.rect.center = (shipx, 680)

    def fire(self):
        laser = Laser(self.rect.centerx, self.rect.top, self.laserGroup)
        self.laserGroup.add(laser)

class EnemyOne(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemyShip1.gif")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        
        self.reset()

        self.dy = random.randrange(6, 13)

    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()

    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        
class EnemyTwo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemyShip2.gif")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centery += self.dy
        self.rect.centerx += self.dx
        if self.rect.top > screen.get_height():
            self.reset()

    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(9, 17)
        self.dx = random.randrange(-2, 2)

class Space(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("outerSpace.jpg")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.dy = 5
        self.reset()
        
    def update(self):
        self.rect.bottom += self.dy
        if self.rect.top >= 0:
            self.reset()
    
    def reset(self):
        self.rect.bottom = screen.get_height()
        
class Core(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("powerCore.jpg")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.dy = 7
        self.reset()

    def update(self):
        self.rect.centery += self.dy
        
        if self.rect.top > screen.get_height():
            self.reset()
    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())

class Laser(pygame.sprite.Sprite):
    def __init__(self,startingX,startingY,laserGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4,12))
        self.image = self.image.convert()
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = startingX
        self.rect.centery = startingY
        self.dy = -12
        self.laserGroup=laserGroup

    def update(self):
        self.rect.centery += self.dy
        if self.rect.bottom < 0:
            self.dy = 0
            self.laserGroup.remove(self)

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.score = 0
        self.font = myFont
        
    def update(self):
        self.text = "Health: %d, Score: %d" % (self.health, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("heart.jpg")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.sndHealth = pygame.mixer.Sound("heart.wav")
        self.dy = 10
        self.reset()

    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > (screen.get_height()* 2):
            self.reset()

    def reset(self):
        self.rect.bottom = -3000
        self.rect.centerx = random.randrange(0, screen.get_width())
        
def instructions(score):
    
    space = Space()
    
    allSprites = pygame.sprite.Group(space)

    instructions = (
    "Core Collector!     Last score: %d" % score ,
    "Instructions:  You are an astronaut,",
    "being attacked by enemies.",
    "",
    "Fly over a core to boost your score,",
    "if you crash into an enemy, you lose health",    
    "and eventually you will die.",
    "",
    "Press spacebar to shoot your lasers at",
    "enemy ships and increase your score.",
    "",
    "Collect hearts to increase your health!",
    "",
    "Use the mouse to move your ship!",
    "",
    "Every 30 seconds, more ships will be sent to attack you.",
    "",
    "Happy flying!",
    "",
    "click to start, escape to quit..."
    )

    insLabels = []    
    for line in instructions:
        tempLabel = myFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    
    pygame.mouse.set_visible(True)
    return donePlaying
        
def game():
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    
    laserGroup=pygame.sprite.Group()
    spaceship = Spaceship(laserGroup)
    enemyOne = []
    enemyTwo = []
    space = Space()
    heart = Heart()
    core = Core()
    scoreBoard = Scoreboard()
    for i in range(5):
        enemy1 = EnemyOne()
        enemyOne.append(enemy1)
        enemy2 = EnemyTwo()
        enemyTwo.append(enemy2)

    scoreGroup = pygame.sprite.Group(scoreBoard)
    shipGroup = pygame.sprite.Group(spaceship)
    coreGroup = pygame.sprite.Group(core)
    friendlyGroup = pygame.sprite.Group(space)
    enemyGroup = pygame.sprite.Group(enemyOne, enemyTwo)
    heartGroup = pygame.sprite.Group(heart)
    thirtySecRespawn = 0
    multiplierRespawn = 1

        
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        thirtySecRespawn += 1
    
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    spaceship.sndLaser.play()
                    spaceship.fire()

        if thirtySecRespawn == 900:
            thirtySecRespawn = 0
            multiplierRespawn += 1   
            for i in range(multiplierRespawn * 2):
                enemy1 = EnemyOne()
                enemyOne.append(enemy1)
                enemyGroup.add(enemy1)
                enemy2 = EnemyTwo()
                enemyTwo.append(enemy2)
                enemyGroup.add(enemy2)
                    
                
                             
        lasersCollided = pygame.sprite.groupcollide(enemyGroup, laserGroup, False, True)   
        if lasersCollided:
            scoreBoard.score += 10
            for e in lasersCollided:
                e.reset()

        shipCollided = pygame.sprite.groupcollide(enemyGroup, shipGroup, False, False)
        if shipCollided:
            scoreBoard.health -= 10
            spaceship.sndCrash.play()
            if scoreBoard.health <= 0:
                keepGoing = False
            for e in shipCollided:
                e.reset()
                
        coreCollided = pygame.sprite.groupcollide(coreGroup, shipGroup, False, False)
        if coreCollided:
            spaceship.sndCore.play()
            scoreBoard.score += 50
            for core in coreCollided:
                core.reset()

        heartCollided = pygame.sprite.groupcollide(heartGroup, shipGroup, False, False)
        if heartCollided:
            scoreBoard.health += 10
            heart.sndHealth.play()
            for h in heartCollided:
                h.reset()
                
                
        friendlyGroup.clear(screen, background)
        shipGroup.clear(screen,background)
        coreGroup.clear(screen,background)
        enemyGroup.clear(screen,background)
        scoreGroup.clear(screen, background)    
        laserGroup.clear(screen,background)
        heartGroup.clear(screen,background)
  
        friendlyGroup.update()
        shipGroup.update()
        coreGroup.update()
        enemyGroup.update()
        scoreGroup.update()  
        laserGroup.update()
        heartGroup.update()

        friendlyGroup.draw(screen)
        coreGroup.draw(screen)
        shipGroup.draw(screen)
        enemyGroup.draw(screen)
        scoreGroup.draw(screen)  
        laserGroup.draw(screen)
        heartGroup.draw(screen)

        pygame.display.flip()

    spaceship.sndShip.stop()
    pygame.mouse.set_visible(True)
    return scoreBoard.score

def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()
        elif donePlaying == True:
            pygame.quit()
            
if __name__ == "__main__":
    main()
    
    
