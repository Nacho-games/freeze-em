"""
Hello and welcome to the source code of freeze 'em

Warnings:
1. You will see very ugly code and stupid solutions to problems
2. This code couldnt be optimized in a worse way
3. I tried my best

Thank you playing by game and checking out the code.
I hope you like the game!

Also, I am very curious to see if someone will actually got here.
If you do, can you let me know by email: bydrabokin1755@gmail.com
or by sending a comment to the github repost, or anyway you like. 
"""

#importing libraries
import pygame # type: ignore
#the comment on top is because i don't know why vs code doesnt like pygame and it underlines it
import sys
import os
import math
import time
import random
import pygame.surfarray as surfarray
import numpy as np 

#The title
pygame.display.set_caption("freeze 'em")

#for getting files to work in pyinstaller
def resource_path(relative_path):
    
    try:
        
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


#some paramaters
hammerAnimation = -1
totalAngleDeg = 0
accumulativeDgrees = 0

#setting lists
portals = []
powerups = []

#function for generating new powerups
def newpowerup():

    #choice
    poewerupChoice = random.choice(["gun", "snowballs", "freezeball", "hammerPrime"])

    #getting the right sprite for each powerup
    if poewerupChoice == "gun":
        sprite = pygame.transform.scale(gunI, (120, 84))
    elif poewerupChoice == "snowballs":
        croprect = (20, 0, 19, 19)
        sprite = powerupsI.subsurface(croprect)
        sprite = pygame.transform.scale(sprite, (114, 114)) 
    elif poewerupChoice == "freezeball":
        croprect = (0, 15, 15, 15)
        sprite = powerupsI.subsurface(croprect)
        sprite = pygame.transform.scale(sprite, (90, 90)) 
    elif poewerupChoice == "hammerPrime": 
        sprite = pygame.transform.scale(explosionI, (96, 96))

    #random spawn
    spawnx = random.randint(-500, 2000)
    spawny = random.randint(-250, 1000)

    #need a rect for blitting the sprite
    powerupRect = pygame.Rect(spawnx, spawny, sprite.get_width(), sprite.get_height())

    #properties of each powerup
    powerupInfo = {

        "rect":powerupRect,
        "sprite":sprite,
        "type":poewerupChoice
    }

    #add them
    powerups.append(powerupInfo)
    everything.append(powerupRect)


#for generating new portals
def newPortal(x, y, xsize, ysize):
    
    #size depending on the size of the enemy
    portalXsize = xsize
    portalx = x
    portalYsize = portalSize[1] / portalSize[0] * xsize
    portaly = y - (portalYsize - ysize) / 2

    #the sporite and rect
    portalSprite = pygame.transform.scale(portal, (portalXsize, portalYsize))
    portalRect = pygame.Rect(portalx, portaly, portalXsize, portalYsize)

    #properties of each portal including the time for later fadding away
    portalInfo = {

        "sprite":portalSprite,
        "rect":portalRect,
        "time":time.time()
    }

    #add those bitches
    portals.append(portalInfo)
    everything.append(portalRect)




#for rotating points
def rotateHammerAround(x, y, cx, cy, angle):

    #sin and cosin
    s = math.sin(angle)
    c = math.cos(angle)

    x -= cx
    y -= cy

    #formula for rotating points
    newx = x * c - y * s
    newy = x * s + y * c

    #return those bitches
    return (newx + cx, newy + cy)

#list for blood spatters
bloods = []

#function for generating blood spatters
def blood(sizex, sizey, x, y):

    #getting sprite and rect based on the dead enemie
    bloodRect = pygame.Rect(x, (sizey - sizex) / 2 + y, sizex, sizex)
    bloodSprite = pygame.transform.scale(bloodI, (sizex, sizex))

    #properties
    bloodInfo = {
        "rect":bloodRect,
        "sprite":bloodSprite
    }

    #add those bitches
    bloods.append(bloodInfo)
    everything.append(bloodRect)


#generating snowball
def newSnowball(angle=None):

    #mouse position
    mouse_pos = pygame.mouse.get_pos()

    #point of origin based on the mouse
    if angle is None:
        dx = mouse_pos[0] - half_width
        dy = mouse_pos[1] - half_height

    #for powerup 2, I generate snowballs based on angle not from the mouse pos
    else:
        dx = math.cos(math.radians(angle))
        dy = math.sin(math.radians(angle))

    # length of vector
    distance = math.hypot(dx, dy)
    
    #rect for collisions
    snowballRect = pygame.Rect(half_width, half_height, 20, 20)

    if distance != 0:
        dx /= distance
        dy /= distance

    #speed
    xspeed = dx * snowballSpeed
    yspeed = dy * snowballSpeed

    #properties
    snowballInfo = {
        "rect":snowballRect,
        "xspeed":xspeed,
        "yspeed":yspeed,
    }

    #add those biytches
    snowballs.append(snowballInfo)
    everything.append(snowballRect)

enemies = []

def newEnemie():

    #okay all of this shit is for generating and random enemie type with a random orientation in a sprite sheet
    spriteXSize = random.randint(20, 95)
    spriteYBaseSize = spriteXSize *1.125

    #different proportions for different tyypes of enemies
    sprite1YSize = spriteYBaseSize
    sprite2YSize = spriteYBaseSize * 1.125
    sprite3YSize = spriteYBaseSize * 1.25
    sprite4YSize = spriteYBaseSize * 1.375

    #height and width of the actual sprite (random)
    SPRITE_WIDTH = 2 * spriteXSize
    SPRITE_HEIGT = sprite1YSize + sprite2YSize + sprite3YSize + sprite4YSize

    #random sized sprite
    enemiesSprite = pygame.transform.scale(enemiesSpriteOg, (SPRITE_WIDTH, SPRITE_HEIGT))
    

    #getting cordinates until the are good
    spawnx = random.randint(0, 1500)
    spawny = random.randint(0, 1500)
    while half_width - 300 < spawnx < half_width + 300:
        spawnx = random.randint(-500, 2000)
    while half_height - 300 < spawny < half_height + 300:
        spawny = random.randint(0, 750)

    #getting size
    size = random.randint(1, 4)

    #selecting the size
    if size == 1: 
        spritey = 0
        spriteYSize = sprite1YSize
    elif size == 2: 
        spritey = sprite1YSize
        spriteYSize = sprite2YSize
    elif size == 3: 
        spritey = sprite1YSize + sprite2YSize
        spriteYSize = sprite3YSize
    elif size == 4: 
        spritey = sprite1YSize + sprite2YSize + sprite3YSize
        spriteYSize = sprite4YSize

    #for enemies to look right or left    
    if spawnx > half_width: spritex = spriteXSize
    else: spritex = 0
    
    #getting the enemie from the randomly sized sprite
    cropRect = (spritex, spritey, spriteXSize, spriteYSize)
    enemieI = enemiesSprite
    enemieI = enemieI.subsurface(cropRect)

    #rect for collsions
    enemieRect = pygame.Rect(spawnx, spawny, spriteXSize, spriteYSize)

    #properties
    enemieInfo = {
        "rect": enemieRect,
        "surface": enemieI,
        "spawnx": spawnx,
        "spawny": spawny,
        "cropRect":cropRect,
        "spritey": spritey,
        "spriteXSize": spriteXSize,
        "spriteYSize": spriteYSize,
        "SPRITE_WIDTH": SPRITE_WIDTH,
        "enemiesSprite": enemiesSprite,
        "frozen": False


    }

    #add them up
    everything.append(enemieRect)
    enemies.append(enemieInfo)

#for enemies movement
def enemieMove(x, y):

    #random speed
    enemieSpeed = random.random() * 5

    #direction of moving
    dx = half_width - x
    dy = half_height -y

    #distance from player
    distance = math.hypot(dx, dy) 
    
    #if it is next to the player, dont move
    if distance < 0.1:                     
        return 0.0, 0.0

    #what to move
    movex = (dx/distance) * enemieSpeed
    movey = (dy/distance) * enemieSpeed

    #give the amount of movement for x and y
    return movex, movey

#reset everything after death
def reset():
    
    global everything, enemies, snowballs, backgrounds, snowballsLeft, guns, hammerPrimes, freezeballs, snow_balls, powerups, gunning
    
    #lists
    everything.clear()
    enemies.clear()
    snowballs.clear()
    backgrounds.clear()
    bloods.clear()
    powerups.clear()

    #snowballs left
    snowballsLeft = 5

    #powerups
    gunning = False
    guns = 1
    hammerPrimes = 1
    freezeballs = 1
    snow_balls = 1

    #backgrounds
    for x in range(6):
        for y in range(4):
            backgroundRect = pygame.Rect(backgroundSizeX * x, backgroundSizeY * y, backgroundSizeX, backgroundSizeY)
            backgrounds.append(backgroundRect)
            everything.append(backgroundRect)

#init
pygame.init()
pygame.font.init()
pygame.mixer.init()

#menus
running = True
mainScreenRunning = True

# screen
screen_width = 1500
screen_height = 750
half_width = screen_width / 2
half_height = screen_height / 2
screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = pygame.Rect(0, 0, screen_width, screen_height)

#time
clock = pygame.time.Clock()
fps_limit = 30
fps = 0

#colors
Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 255, 0)

#mouse
pygame.mouse.set_visible(False)
mouse_pos = pygame.mouse.get_pos()
mouse_rect_size = 10
mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], mouse_rect_size, mouse_rect_size)
theta = 0

#player
playerSizeX = 155 
playerSizeY = 155 
playerSpeed = 5

#list
everything = []

#enemies
enemieSpeed = 3.5
spawnTimer = 75
spawnCounter = spawnTimer

#snowball 
lastSnowball = time.time()
snowballSpeed = 20
snowballs = []
snowballSize = 25
buffer = 0.3

#score
score = 0
highScore = score

#imports

#snowman
snowmanI = pygame.image.load(resource_path("assets/images/snowman.png"))
snowmanI = pygame.transform.scale(snowmanI, (playerSizeX, playerSizeY))
OGsnowmanI = snowmanI
playerRect = snowmanI.get_rect(topleft=(half_width- playerSizeX/2, half_height - playerSizeY/2))

#snowman with gun
snowmangunI = pygame.image.load(resource_path("assets/images/snowmanwithgun.png"))
snowmangunI = pygame.transform.scale(snowmangunI, (playerSizeX, playerSizeY))
OGsnowmangunI = snowmangunI

#snow ball
snowballI = pygame.image.load(resource_path("assets/images/snow_ball.png"))
snowballI = pygame.transform.scale(snowballI, (snowballSize, snowballSize))

#backgrounds
backgroundSizeX = 320
backgroundSizeY = 352
backgroundI = pygame.image.load(resource_path("assets/images/background.png"))
backgroundI = pygame.transform.scale(backgroundI, (backgroundSizeX, backgroundSizeY))

#enemie
enemiesSpriteOg = pygame.image.load(resource_path("assets/images/enemies.png"))

#main screen
mainScreenI = pygame.image.load(resource_path("assets/images/freeze_them.webp"))
mainScreenBackground = pygame.transform.scale(mainScreenI, (screen_width, screen_height))

#ice in enemies
iceI = pygame.image.load(resource_path("assets/images/ice.png"))
iceI.set_alpha(128) #opacity

#hammer
OGhammer = pygame.image.load(resource_path("assets/images/hammer.png"))
OGhammer = pygame.transform.scale(OGhammer, (115, 140))

#blood spatter
bloodI = pygame.image.load(resource_path("assets/images/blood.png"))
bloodI = pygame.transform.scale(bloodI, (100, 100))

#portal
portal = pygame.image.load(resource_path("assets/images/portal.png")).convert_alpha()
portalSize = portal.get_size()

#powerups images
powerupsI = pygame.image.load(resource_path("assets/images/powerups.png")).convert_alpha()
explosionI = pygame.image.load(resource_path("assets/images/explosion.png")).convert_alpha()
gunI = pygame.image.load(resource_path("assets/images/gun.png")).convert_alpha()

#fonts
font_path = resource_path("assets/fonts/font.ttf")
fontSize1 = 80
font1 = pygame.font.Font(font_path, fontSize1)
fontSize2 = 60
font2 = pygame.font.Font(font_path, fontSize2)
fontSize3 = 50
font3 = pygame.font.Font(font_path, fontSize3)



#audio
flesh = pygame.mixer.Sound(resource_path("assets/audio/flesh.mp3"))
frozen = pygame.mixer.Sound(resource_path("assets/audio/frozen.mp3"))
hammer = pygame.mixer.Sound(resource_path("assets/audio/hammer.mp3"))
mainmenu = pygame.mixer.Sound(resource_path("assets/audio/mainmenu.mp3"))
snowball_hit = pygame.mixer.Sound(resource_path("assets/audio/snowball_hit.mp3"))
snowball_throw = pygame.mixer.Sound(resource_path("assets/audio/snowball_throw.mp3"))
soundtrack = pygame.mixer.Sound(resource_path("assets/audio/soundtrack.mp3"))
deathmp3 = pygame.mixer.Sound(resource_path("assets/audio/death.mp3"))
noleft = pygame.mixer.Sound(resource_path("assets/audio/noleft.mp3"))
beep = pygame.mixer.Sound(resource_path("assets/audio/beep.mp3"))
magic = pygame.mixer.Sound(resource_path("assets/audio/magic.mp3"))
freeze = pygame.mixer.Sound(resource_path("assets/audio/freeze.mp3"))

#adjust volume
mainmenu.set_volume(0.1)
soundtrack.set_volume(0.4)
noleft.set_volume(0.4)


#bouncing message that tells you to play byhitting any key
bounceCounter = 0
messageRectWidth = 200
messageRectWidth2 = 100
messageRectHeight = 200
messageRectHeight2 = 250

#generating backgrounds
backgrounds = []
for x in range(6):
    for y in range(4):
        backgroundRect = pygame.Rect(backgroundSizeX * x, backgroundSizeY * y, backgroundSizeX, backgroundSizeY)
        backgrounds.append(backgroundRect)
        everything.append(backgroundRect)

#def for the main screen
def mainScreen():
    global mainScreenRunning, running, bounceCounter, fontSize2, messageRectHeight, messageRectHeight2, firstTime
    
    #for 1 sec delay after booting so you dont play instantly
    firstTime = True
    
    #booting time
    init = time.time()

    #reset sound
    pygame.mixer.stop()
    pygame.mixer.init()

    #play themeinfinetly
    mainmenu.play(loops=-1)

    #loop
    while mainScreenRunning:

        #exit 
        key = pygame.key.get_pressed()

        #booting
        if firstTime:
            init = time.time()
            firstTime = False

        #input
        for event in pygame.event.get():

            #exeting
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #playing
            if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE and time.time() -1 > init:
                running = True
                game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = True
                game()

        #bounce ogic
        if bounceCounter > 40:
            bounceCounter = 0
        elif bounceCounter < 20:
            fontSize2 -= 2
        elif bounceCounter > 20:
            fontSize2 += 2
        elif bounceCounter == 20:
            fontSize2 = 50

        bounceCounter += 1

        #bounce message logic by adjustinf font size
        font2 = pygame.font.Font(font_path, fontSize2)
        
        #top text
        messageRect = pygame.Rect(half_width - messageRectWidth / 2, half_height - messageRectHeight / 2 + messageRectHeight, messageRectWidth, messageRectHeight)
        message = font2.render(f"Press any", True, White)
        messageTextRect = message.get_rect(center=(messageRect.center))

        #bottom text
        messageRect2 = pygame.Rect(half_width - messageRectWidth2 / 2, half_height - messageRectHeight2 / 2 + messageRectHeight2, messageRectWidth2, messageRectHeight2)
        message2 = font2.render(f"key to play!", True, White)
        messageTextRect2 = message2.get_rect(center=(messageRect2.center))

        #stick them together
        messageTextRect.bottom = messageRectHeight2 + half_height
        messageTextRect2.top = messageRectHeight2 + half_height


        #mouse 
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect.x, mouse_rect.y = mouse_pos
        
        #clean
        screen.fill(Black)

        #draw background
        screen.blit(mainScreenBackground, screen_rect)

        #draw messages
        screen.blit(message, messageTextRect)
        screen.blit(message2, messageTextRect2)

        #highest score message on top-right
        score_suface = font3.render(f"Highest Score: {highScore}", True, White)
        screen.blit(score_suface, (1090, 0))

        #mouse square
        pygame.draw.rect(screen, White, mouse_rect)

        #update
        pygame.display.flip()

        #fps controller
        clock.tick(fps_limit)


#game
def game():
    global running, spawnCounter, spawnTimer, lastSnowball, mainScreenRunning, everything, snowballs, enemies, backgrounds, hammerAnimation, totalAngleDeg, accumulativeDgrees, firstTime, highScore

    #starting hammer collsion point
    thePoint = pygame.math.Vector2(57.5, -127.5)

    #inti time
    gameStarted = time.time()

    #staring bools
    death = False
    gonogo = False
    scoreBuffer = False

    #starting varuables
    tip_rotated = 0, 0
    baseDegrees = 0
    rotatedHammer = OGhammer
    score = 0

    #powerups
    guns = 1
    hammerPrimes = 1
    freezeballs = 1
    snow_balls = 1
    gunning = False

    #reset audio
    pygame.mixer.stop()
    pygame.mixer.init()
    
    #fire sountrack play indefently
    soundtrack.play(loops=-1)

    #snowballs
    snowballsLeft = 5

    #top-right powerup counters
    #guns
    gunCounterI = pygame.transform.scale(gunI, (71.42, 50))

    #snowballs
    croprect = (20, 0, 19, 19)
    snowballsCounterI = powerupsI.subsurface(croprect)
    snowballsCounterI = pygame.transform.scale(snowballsCounterI, (50, 50))
    
    #freezeballs
    croprect = (0, 15, 15, 15)
    freezeballCounterI = powerupsI.subsurface(croprect)
    freezeballCounterI = pygame.transform.scale(freezeballCounterI, (50, 50)) 

    #super hammers
    hammerPrimeCounterI = pygame.transform.scale(explosionI, (50, 50))

    #main loop
    while running:

        #time started
        now = time.time()

        #exit 
        key = pygame.key.get_pressed()

        #events
        for event in pygame.event.get():

            #quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #newsnowball if time has passed, mouse click and enough snowballs
            if event.type == pygame.MOUSEBUTTONDOWN and now - lastSnowball > buffer and now - gameStarted > 1 and snowballsLeft > 0 and not gunning:
                
                #set last snowball time
                lastSnowball = time.time()

                #generate
                newSnowball()

                #play throw sound
                snowball_throw.play()

                #take away snowball
                snowballsLeft -= 1
            
            #if there are no left
            elif event.type == pygame.MOUSEBUTTONDOWN and now - lastSnowball > buffer and now - gameStarted > 1 and snowballsLeft == 0:
                noleft.play()

            #keyboard events
            if event.type == pygame.KEYDOWN:
                
                #hammer animation
                if event.key == pygame.K_SPACE and hammerAnimation == -1:

                    # 0 = True
                    hammerAnimation = 0

                #hammer power up
                if event.key == pygame.K_4 and hammerPrimes > 0:

                    #start hammer animation
                    hammerAnimation = 0

                    #take waya 1 hammer
                    hammerPrimes -= 1

                    #kill frozen enemies nearby
                    for enemie in enemies[:]:

                        #calculate distance
                        distance = math.sqrt((enemie["rect"].x - half_width)**2 + (enemie["rect"].y - half_height)**2)
                        
                        #if they are frozen and close
                        if enemie["frozen"] == True and distance <= 450:
                            
                            #generate blood
                            blood(enemie["rect"].width, enemie["rect"].height, enemie["rect"].x, enemie["rect"].y)
                            
                            #remove them
                            everything.remove(enemie["rect"])
                            enemies.remove(enemie)

                            #play sound
                            flesh.play()
                            hammer.play()

                            #give a random amount of snoeballs left,
                            #3/7%: 0, 3/7%: 1 and 1/7%: 1
                            snowballsLeft += random.choice([0, 0, 0, 1, 1, 1, 2])

                    #plus 15 in the score
                    score += 15

                #freeze ball powerup
                if event.key == pygame.K_3 and freezeballs > 0:
                    
                    #take awya a freezeball
                    freezeballs -= 1

                    #assume no one was frozen until proven otherwise
                    someEnemieWasFrozen = False

                    #for eachn enemie itirate through a copy -> [:]
                    for enemie in enemies[:]:
                        
                        #compute distance
                        distance = math.sqrt((enemie["rect"].x - half_width)**2 + (enemie["rect"].y - half_height)**2)
                        
                        #if they are close
                        if distance <= 450:
                            
                            #were they forzen?
                            wasFrozen = enemie["frozen"]

                            #make them frozen
                            enemie["frozen"] = True

                            # if they wre not frozen, them, someone was frozen in the process
                            if not wasFrozen:
                                someEnemieWasFrozen = True
                    
                    #if someone was actually frozen 
                    if someEnemieWasFrozen:

                        #play sound
                        frozen.play()
                        freeze.play()

                        #add 15 to the score
                        score += 15
                
                #snowball powerup
                if event.key == pygame.K_2 and snow_balls > 0:
                    
                    #take put the powerup used
                    snow_balls -= 1

                    #hammer animation: do not fucking move
                    hammerAnimation = -3
                    
                    #36 balls 
                    for i in range(36):

                        # a ball every 36 degrees
                        theta = i * 10

                        #generate the new snoeball with the angle
                        newSnowball(theta)

                    #make it available again
                    hammerAnimation = -1

                    #add 15 to the score
                    score += 15
                
                #gun powerup
                if event.key == pygame.K_1 and guns >0:

                    #use the power up up
                    guns -= 1

                    #add 15 to the score
                    score += 15

                    #make gunning mode start
                    gunning = True

                    #set time when gunning mode started
                    gunningStart = now

        #quit to the main menu by hitting escape
        if key[pygame.K_ESCAPE]:

            #stop sound
            pygame.mixer.stop()

            #play main theme
            mainmenu.play(loops=-1)

            # no more running
            running = False

        # so the player actually doesnt move, it moves everythng that it is no itself
        # if everythung is moved to the opposite direction, it looks like the plwyer is moving
        for thing in everything:
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                thing.x += playerSpeed
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                thing.x -= playerSpeed
            if key[pygame.K_UP] or key[pygame.K_w]:
                thing.y += playerSpeed
            if key[pygame.K_DOWN] or key[pygame.K_s]:
                thing.y -= playerSpeed
                


        #clean
        screen.fill(Black)

        #backgrpunds
        for background in backgrounds:
            

            #if they go out of the screen, move them to the other side 
            #so there is this endless moving effect of backgrounds without an infinite number of them

            if background.x + backgroundSizeX <= 0:             
                background.x += screen_width + backgroundSizeX      
            if background.x >= screen_width:                    
                background.x -= screen_width + backgroundSizeX      

            if background.y + backgroundSizeY <= 0:             
                background.y += screen_height + backgroundSizeY
            if background.y >= screen_height:                   
                background.y -= screen_height + backgroundSizeY

            #draw them
            screen.blit(backgroundI, background)

        #blood spatters
        for bloodies in bloods:
            
            #draw those bitches up
            screen.blit(bloodies["sprite"], bloodies["rect"])

        #mouse and snowman turning
        #mouse pos
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect.x, mouse_rect.y = mouse_pos

        #relative mouse pos
        mouseX = mouse_rect.x - half_width
        mouseY = mouse_rect.y - half_height
        
        #radians of the mous epos to the player
        radtheta = math.atan2(mouseY, mouseX)

        #radiasn to degrees
        theta = math.degrees(radtheta)

        #if hammer animation is active
        if hammerAnimation == -1:

            #roatate tip
            tip_rotated = thePoint.rotate(theta) 

            #rotate snowman
            snowmanI = pygame.transform.rotate(OGsnowmanI, -theta)

            #roatte snowman with gun
            snowmangunI = pygame.transform.rotate(OGsnowmangunI, -theta)

            #player rect
            roatatedPlayer = snowmanI.get_rect(center=playerRect.center)
            


        #hammer points
        points = [(half_width, half_height-150),  
            (half_width, half_height-105),
            (half_width + 45, half_height-105), 
            (half_width + 45, half_height -10), 
            (half_width+65, half_height-10), 
            (half_width+65, half_height-105), 
            (half_width + 115, half_height-105),
            (half_width + 115, half_height-150)
        ]

        #pos of the tip, (the colliding part)
        tip_screen_pos = pygame.math.Vector2(half_width, half_height) + tip_rotated

        #offset of the hammer from center
        offset = pygame.math.Vector2(57.5, -80)

        #roatte offset
        rotated_offset = offset.rotate_rad(radtheta)
        
        #if hammer animation is active
        if hammerAnimation == -1:

            #the latest angle of the hammer
            baseDegrees = theta

            #roatte hammer
            rotatedHammer = pygame.transform.rotate(OGhammer, -theta)

        #hammer rect
        rotatedHammerRect = rotatedHammer.get_rect(center=(half_width + rotated_offset.x, half_height + rotated_offset.y))
        
        # the hammer pivot
        pivot = pygame.math.Vector2(half_width, half_height)   # center of screen

        #and the pivot when doing the atck
        hammer_tip_offset = pygame.math.Vector2(57.5, -127.5) # tip relative to pivot

        #hammer animation
        if hammerAnimation > -1:
            #lower
            if hammerAnimation < 10:
                angle_deg = 9
            #rest
            elif hammerAnimation < 15:
                angle_deg = 0   
            #elevate
            elif hammerAnimation < 25:
                angle_deg = -9 

            #if it's over, then it is over
            if hammerAnimation >= 25:
                hammerAnimation = -2
                accumulativeDgrees = 0

            #getting hammer sizes
            hammerWidth, hammerHeight = OGhammer.get_size()

            #the angle that the hammer has moved so far
            accumulativeDgrees += angle_deg 

            #the total angle
            totalAngleDeg = accumulativeDgrees + baseDegrees
            
            #next step
            hammerAnimation += 1

            #roatte hammer sprite
            rotatedHammer = pygame.transform.rotate(OGhammer, -totalAngleDeg)

            # Tip position
            tip_rotated = hammer_tip_offset.rotate(baseDegrees + accumulativeDgrees /2)
            tip_screen_pos = pivot + tip_rotated    

        
        #powerups
        for powerup in powerups[:]:
            
            #draw them up
            screen.blit(powerup["sprite"], powerup["rect"])

            #if colide with player
            if powerup["rect"].collidepoint(half_width, half_height):
                
                #add the type to the counter
                if powerup["type"] == "gun":
                    guns += 1
                elif powerup["type"] == "snowballs":
                    snow_balls += 1
                elif powerup["type"] == "freezeball":
                    freezeballs += 1
                elif powerup["type"] == "hammerPrime":
                    hammerPrimes += 1

                #remove the powerup
                everything.remove(powerup["rect"])
                powerups.remove(powerup)

                #and play a little beep
                beep.play()

            #distance from powerup
            distance = math.sqrt((powerup["rect"].x - half_width)**2 + (powerup["rect"].y - half_height)**2)

            #if too far, then the powerup is gone
            if distance > 1500:
                everything.remove(powerup["rect"])
                powerups.remove(powerup)

        
        #eneimes
        for enemie in enemies[:]:


            #draw them
            screen.blit(enemie["surface"], enemie["rect"])

            #lets make the not frozen ones move
            if not enemie["frozen"]:

                #what do i need to move them by?
                move = enemieMove(enemie["rect"].centerx, enemie["rect"].centery)

                #actually move them
                enemie["rect"].centerx += move[0]
                enemie["rect"].centery += move[1]
            
            #if frozen
            else:
                #get ice size
                iceTransformed = pygame.transform.scale(iceI, (enemie["spriteXSize"], enemie["spriteYSize"]))

                #draw the ice on top of the frozen enemie
                screen.blit(iceTransformed, (enemie["rect"].x, enemie["rect"].y))

            #move eyes if the are on the right or left
            #**EVEN WHEN THEY ARE FORZEN**#
            if enemie["rect"].centerx > half_width:
                eyes = enemie["SPRITE_WIDTH"] / 2
            else:
                eyes = 0
            
            #enemie sprite part
            enemie["cropRect"] = (eyes, enemie["spritey"], enemie["spriteXSize"], enemie["spriteYSize"])

            #enemei surface is equal to the sprite
            enemie["surface"] = enemie["enemiesSprite"]

            #and then crop the sprite
            enemie["surface"] = enemie["surface"].subsurface(enemie["cropRect"])
            
            #if they are hit by the hammer
            if enemie["frozen"] == True and enemie["rect"].collidepoint(tip_screen_pos) and hammerAnimation > -1:
                
                #MAKE BLOOOOOD
                blood(enemie["rect"].width, enemie["rect"].height, enemie["rect"].x, enemie["rect"].y)
                
                #remove those bitches up
                everything.remove(enemie["rect"])
                enemies.remove(enemie)

                #wonderful sound
                flesh.play()
                hammer.play()

                #add some score
                score += 7

                #add some snowballs
                snowballsLeft += random.choice([0, 0, 0, 1, 1, 1, 2])

            #if the player gets hit by an enemie
            if enemie["frozen"] == False and enemie["rect"].colliderect((half_width -40, half_height-40, 80, 80)):
                death = True
                deathmp3.play()
            
            #distance from enemie
            distance = math.sqrt((enemie["rect"].x - half_width)**2 + (enemie["rect"].y - half_height)**2)

            #if they are a bt far way, random chance the disapper through a portal
            if distance < 375 and random.randint(1, 300) == 67 and enemie["frozen"] == False:
                
                #new portal
                newPortal(enemie["rect"].x, enemie["rect"].y, enemie["spriteXSize"], enemie["spriteYSize"])
                
                #remove them 
                everything.remove(enemie["rect"])
                enemies.remove(enemie)
                
                #little magic sound
                magic.play()

            #snowballs and enemies
            for snowball in snowballs[:]:
                
                #snowballs hitting enemies
                if snowball["rect"].colliderect(enemie["rect"]):
                    
                    #was he frozen
                    wasFrozen = enemie["frozen"]

                    #lets make him forzen
                    enemie["frozen"] = True

                    # if he was not frozen the...
                    if not wasFrozen:

                        #remove snowball
                        snowballs.remove(snowball)

                        #FROZEN sound
                        frozen.play()

                        #other sounds
                        snowball_hit.play()
                        freeze.play()

                        # add a little score
                        score += 3
        #draw hammer
        screen.blit(rotatedHammer, rotatedHammerRect)

        #for snowballs
        for snowball in snowballs[:]:
            
            #draw them
            screen.blit(snowballI, snowball["rect"])

            #move them
            snowball["rect"].x += snowball["xspeed"]
            snowball["rect"].y += snowball["yspeed"]

            #ifthey are incredibly far...
            if abs(snowball["rect"].x) + abs(snowball["rect"].y) > 6000:

                #remove those bitches up
                snowballs.remove(snowball)

        #for portals
        for portal in portals[:]:
            
            #time passed since the creation
            elapsed = now - portal["time"] 

            #for 1.5 opacity is max
            if elapsed < 1.5:
                opacity = 100

            #the it reudces gradually
            else:
                opacity = 100 - (elapsed-1.5) * ((100/3) * 2)

            #if opacity is not 0...
            if opacity >= 0:   

                #set opcaity (255)
                portal["sprite"].set_alpha(opacity * 255 / 100)
            
            #if opacity is 0...
            else:

                #remove those bitches up
                if portal["rect"] in everything:
                    everything.remove(portal["rect"])

                portals.remove(portal)

            #draw the portal
            screen.blit(portal["sprite"], portal["rect"])



        #draw the snowman with gun or not
        if not gunning:
            screen.blit(snowmanI, roatatedPlayer)
        else:
            screen.blit(snowmangunI, roatatedPlayer)
        

        #dying :(
        if death:
            
            #pixels in creen
            pixels = surfarray.array3d(screen)

            #make them gray
            gray = (pixels[:,:,0]*0.299 +
                pixels[:,:,1]*0.587 +
                pixels[:,:,2]*0.114).astype(np.uint8)

            pixels[:,:,0] = gray
            pixels[:,:,1] = gray
            pixels[:,:,2] = gray

            #draw
            surfarray.blit_array(screen, pixels)    

            #update    
            pygame.display.flip()

            #wait a second
            pygame.time.wait(1000)

            #stop music
            pygame.mixer.stop()

            #play main theme
            mainmenu.play(loops=-1)

            #go back to the main menu
            firstTime = True
            running = False
    

        #fps text
        fps_text_surface = font1.render(f"{round(clock.get_fps())}", True, White)
        pygame.draw.rect(screen, Black, (0, 0, 100, 100))
        screen.blit(fps_text_surface, (15, 0))

        #snowballs left (red if none)
        if snowballsLeft > 0:
            snowballsLeft_surface = font2.render(f"Snowballs: {snowballsLeft}", True, White)
        else: 
            snowballsLeft_surface = font2.render(f"Snowballs: {snowballsLeft}", True, (255, 0, 0))

        #drae the snowballs left and balck rectangle
        pygame.draw.rect(screen, Black, (1125, 0, 500, 80))
        screen.blit(snowballsLeft_surface, (1160, 0))
        
        #draw score bottom right
        score_suface = font2.render(f"Score: {score}", True, White)
        screen.blit(score_suface, (1230, 680))

        #draw each of the powerup counters and images
        screen.blit(gunCounterI, (1350, 100, 71.52, 50))
        gunCounterITextSurface = font2.render(f"(1)      : {guns}", True, White)
        screen.blit(gunCounterITextSurface, (1280, 90))

        screen.blit(snowballsCounterI, (1350, 160, 50, 50))
        snowballsCounterITextSurface = font2.render(f"(2)    : {snow_balls}", True, White)
        screen.blit(snowballsCounterITextSurface, (1280, 145))

        screen.blit(freezeballCounterI, (1350, 220, 50, 50))
        freezeballCounterITextSurface = font2.render(f"(3)    : {freezeballs}", True, White)
        screen.blit(freezeballCounterITextSurface, (1280, 205))

        screen.blit(hammerPrimeCounterI, (1350, 280, 50, 50))
        hammerPrimeCounterITextSurface = font2.render(f"(4)    : {hammerPrimes}", True, White)
        screen.blit(hammerPrimeCounterITextSurface, (1280, 265))


        #draw mouse
        pygame.draw.rect(screen, White, mouse_rect)

        #update
        pygame.display.flip()

        #spawning
        if spawnCounter == spawnTimer:
            newEnemie()
            spawnCounter = 0
            if  spawnTimer > 20:
                spawnTimer -= 1


        spawnCounter += 1

        #new snowball
        if round(gameStarted - now) % 7 == 0 and gonogo == True and snowballsLeft < 4:
            snowballsLeft += 1
            beep.play()
            gonogo = False
        elif round(gameStarted - now) % 7 != 0:
            gonogo = True

        #score
        if round(gameStarted - now) % 2 == 0 and scoreBuffer == True:
            score += 2
            scoreBuffer = False
        elif round(gameStarted - now) % 2 != 0:
            scoreBuffer = True

        #high score
        if score > highScore:
            highScore = score
        
        #new powerup
        if random.randint(1, 200) == 1 and len(powerups) < 8:
            newpowerup()


        #fps
        clock.tick(fps_limit)

        #gunning mode
        if gunning and now - lastSnowball > buffer/5:
            if now - gunningStart < 4:
                lastSnowball = time.time()
                newSnowball()
                snowball_throw.play()
            else: 
                gunning = False

    reset()
    return



if __name__ == '__main__':
    mainScreen()
pygame.quit()
sys.exit()
