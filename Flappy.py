import pygame
import sys
import random
from pygame.constants import SYSTEM_CURSOR_SIZEALL
from pygame.transform import rotate, smoothscale

# a function to make sure floor is repeated again and again


def draw_floor():
    screen.blit(floorSurface, (floor_x_pos, 700))
    screen.blit(floorSurface, (floor_x_pos + screenWidth, 700))

# function to create pipes


def createPipe():
    randomPipePosition = random.choice(pipeHeight)
    bottomPipe = pipeSurface.get_rect(midtop=(700, randomPipePosition))
    topPipe = pipeSurface.get_rect(midbottom=(700, randomPipePosition-300))
    return bottomPipe, topPipe

# move the pipes on screen


def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5  # takes all the pipes and it moves them to the left by a little bit
    # despawning the pipes
    visiblePipes = [pipe for pipe in pipes if pipe.right > -50]
    return visiblePipes

# Game variables


def drawPipes(pipes):
    # draw pipes on the background
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipeSurface, pipe)
        else:
            # flipping in the x direction not the y direction
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            screen.blit(flipPipe, pipe)


def checkCollision(pipes):
    # check for collisions
    global canScore
    for pipe in pipes:
        if birdieRectangle.colliderect(pipe):
            buhByeSound.play()
            canScore = True  # when game restarts, canScore is True so that the first pipe the bird crosses can give us a point
            return False
    # we use >= becasue pixel measurements are never precise
    if birdieRectangle.top <= -100 or birdieRectangle.bottom >= 700:
        canScore = True
        return False

    return True


def rotateBird(bird):
    # rotate a bird
    newBird = pygame.transform.rotozoom(bird, -birdMovement*3, 1)
    return newBird


def birdAnimation():
    # create a function to animate the bird draw rectangles around the flaps so its the same size
    newBird = birdFrames[birdIndex]
    newBirdRectangle = newBird.get_rect(center=(100, birdieRectangle.centery))
    return newBird, newBirdRectangle


def scoreDisplay(gameState):
    # to recognise the state of the game and display high score automatically, based on if the game is over or not:
    if gameState == 'mainGame':
        # anti-aliasing settings here
        scoreSurface = gameFont.render(
            str(int(score)), True, (255, 255, 255))  # score has to be a string to be displayed, which is why we convert score
        scoreRect = scoreSurface.get_rect(center=(screenWidth/2, 100))
        screen.blit(scoreSurface, scoreRect)
    if gameState == 'gameOver':

        # anti-aliasing settings here
        # score has to be a string to be displayed, which is why we convert score
        # we use an f string to pass the integer as a string here
        # adding overlay
        overlaySize = (screenWidth, screenHeight)
        overlaySurface = pygame.Surface(overlaySize)
        pygame.draw.rect(overlaySurface, pygame.Color(
            0, 0, 0), overlaySurface.get_rect())
        overlaySurface.set_alpha(90)
        screen.blit(overlaySurface, (0, 0))
        # adding score
        scoreSurface = gameFont.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center=(screenWidth/2, 100))
        screen.blit(scoreSurface, scoreRect)
        highScoreSurface = gameFont.render(
            f'High Score: {int(highScore)}', True, (255, 255, 255))
        highScoreRect = highScoreSurface.get_rect(center=(screenWidth/2, 550))
        screen.blit(highScoreSurface, highScoreRect)


def updateHighScore(score, highScore):
    # function to update High Score
    if score > highScore:
        highScore = score
    return highScore


def pipeCheck():
    # check if FLappy Bird has passed the pipes:
    global score, canScore
    # we need to make sure the following line of code is triggered only once.
    # hence we update score once, but then we quickly disable updating score feature
    # we need the x position and the x position of the pipes, which is stored in pipeList
    if pipeList:
        for pipe in pipeList:
            if 95 < pipe.centerx < 105 and canScore:  # change this value when you're changing dimensions
                score += 1
                scoreSound.play()
                canScore = False
            if pipe.centerx < 0:
                canScore = True


pygame.init()
# the resolution of the canvas
# this can be changed and accordingly, the floor and other details also need to be altered
screenWidth = 1500
screenHeight = 820  # do not change this

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

# Font
gameFont = pygame.font.Font(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\CODA\\04B_19.TTF', 40)

# GAME VARIABLES
gravity = 0.25
birdMovement = 0  # used to move the birdieRectangle down
gameActive = True
score = 0
highScore = 0
canScore = True

# background surface: change with a sci-fi background here
backgroundSurface = pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\city_night.gif').convert()  # image to pygame easier file
backgroundSurface = pygame.transform.scale2x(backgroundSurface)

# floor surface
floorSurface = pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floor_x_pos = 0

# pipes

pipeSurface = pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\pipe-green.png').convert()
pipeSurface = pygame.transform.scale2x(pipeSurface)
# pipelist with a lot of rectangles that move left
# using these leftward moving rectangles, we create a game
pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # an event that is triggered every 1.2s
pipeHeight = [400, 600, 800]  # all the possible heights a pipe can have

# flappy bird changed with an electron here
birdDownFlap = pygame.transform.scale2x(pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\bluebird-downflap.png').convert_alpha())
birdMidFlap = pygame.transform.scale2x(pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\bluebird-midflap.png').convert_alpha())
birdUpFlap = pygame.transform.scale2x(pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\bluebird-upflap.png').convert_alpha())
birdFrames = [birdDownFlap, birdMidFlap, birdUpFlap]
birdIndex = 2
birdie = birdFrames[birdIndex]
birdieRectangle = birdie.get_rect(center=(100, screenHeight/2))

# to give the wings an appearance of flapping
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Game Over Surface
gameOverSurface = pygame.image.load(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\message.png').convert_alpha()
gameOverSurface = pygame.transform.scale2x(gameOverSurface)
gameOverRect = gameOverSurface.get_rect(center=(screenWidth/2, screenHeight/2))

# birdie = pygame.image.load(
#     'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\Sprites\\bluebird-midflap.png').convert_alpha()
# birdie = pygame.transform.scale2x(birdie)
# # make a rectangle so that detecting collisions is easier
# birdieRectangle = birdie.get_rect(center=(100, screenHeight/2))


# importing sounds using mixer. mixer can be a lil tricky

flapSound = pygame.mixer.Sound(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\SFX\\sfx_wing.wav')
buhByeSound = pygame.mixer.Sound(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\SFX\\sfx_die.wav')
scoreSound = pygame.mixer.Sound(
    'D:\\Shraze\\The One\\1. Fire\\4. Side Projects\\Flappy Bird\\Assets\\SFX\\sfx_point.wav')
scoreSoundCountdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)

# this is our main event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # check if any key is pressed
            if event.key == pygame.K_SPACE and gameActive:  # check if spacebar is pressed
                birdMovement = 0  # turn this 0 before jumping to prevent unnecessary actions
                birdMovement -= 12  # because it works against the gravity, it is negative
                flapSound.play()  # play the flap sound whenever this loop is run

            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                pipeList.clear()
                birdieRectangle.center = (100, screenHeight/2)
                birdMovement = 0
                score = 0

        if event.type == SPAWNPIPE:
            # we want to create a new pipe each time it updates so we use the function createPipe
            # unpacking the tupe, we change from append to extend
            pipeList.extend(createPipe())

        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0

            birdie, birdieRectangle = birdAnimation()
    # B.A.C.K.G.R.O.U.N.D
    screen.blit(backgroundSurface, (0, 0))

    if gameActive:
        # B.I.R.D
        birdMovement += gravity
        # rotating the bird
        rotatedBird = rotateBird(birdie)
        # rotating makes you lose quality, which is why we employ two surfaces
        # change the position of the birdmovement by the amount specified in the gravuty variable
        birdieRectangle.centery += birdMovement
        # instead of a tuple we put this
        screen.blit(rotatedBird, birdieRectangle)
        gameActive = checkCollision(pipeList)

        # P.I.P.E.S
        pipeList = movePipes(pipeList)
        drawPipes(pipeList)

        # S.C.O.R.E: scoring system: bird scores if it passes a pipe
        pipeCheck()
        scoreDisplay('mainGame')
    else:
        screen.blit(gameOverSurface, gameOverRect)
        highScore = updateHighScore(score, highScore)
        scoreDisplay('gameOver')

    # F.L.O.O.R
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -screenWidth:
        floor_x_pos = 0  # go back to where the floor_x_pos started
    # this will be moved by tiny increments
    # screen.blit(floorSurface, (floor_x_pos, 900))
    pygame.display.update()
    clock.tick(120)

# Next Steps for Shreya
# 1. convert to stern gerlach experiment using SG logic
