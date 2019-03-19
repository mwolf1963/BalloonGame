#Author: Matt Wolf
#Date:3/16/19
#Description:
#Attempt a simple balloon color match game


#works. need to add logic for score and up coming balls
#also need to add logic for balls next to balls

#import modules
import pygame
import math
import random


#init pygame
pygame.init()
bg = pygame.image.load('backGround100.png')

# screen size
screen_Width = 750
screen_Height = 500

#refresh clock
clock = pygame.time.Clock()

#define win as our window
win = pygame.display.set_mode(( screen_Width,  screen_Height))
pygame.display.set_caption('Balloon Breaker')


# and an add new run to the tracker for balloon list
fileout = open("outfile.txt", 'a')
fileout.write("new run" + '_'*48)
fileout.close()

#logger to check balloon positions
def logBalloons(balloons):
    

    try:    
        fileout = open("outfile.txt" , 'a')
        fileout.write('_' *48 + '\n')
        for item in balloons:
                    fileout.write(str(item.x) + ', ' + str(item.y) + '\n')
        fileout.close()
    except IOError:
        print('There has been an IOError')
    except Error as err:
        print('There has been a file error: ', err)
	 


#balloon for game
class balloon(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.balloonImage = balloonImage[random.randint(0, balloonRange)]
        self.isFlying = False
        self.stop = 0
        self.isLive = True
    def draw(self, win):
         win.blit(self.balloonImage, (self.x , self.y))

#images for the balloon
balloonImage = [pygame.image.load("R1.png"),pygame.image.load("O1.png"),pygame.image.load("Y1.png"),pygame.image.load("B1.png"),
          pygame.image.load("P1.png"),pygame.image.load("G1.png"),pygame.image.load("M1.png")]


#variable for which balloons in the list can be called
balloonRange = 5

#player clock for timing game eventually
playerClock = 0

#setup the  init board function
def setupBoard(level):
    for x in range(BORDER, 500, 64):
        for y in range(BORDER, 64 * level + BORDER , 64):
            balloons.append(balloon(x , y ))
    for item in balloons:
        item.draw(win)
    pygame.display.update()

#redraw the game window on refresh
def reDrawGameWindow():
    win.blit(bg, (0,0))
    player.draw(win)
    for item in balloons:
        item.draw(win)
    pygame.display.update()

#establish initial variable values
BORDER = 4
level = 4
balloons = [] #init the balloon list
run = True
playerStep = 64 #based on the size of the picture
setupBoard(level) #run the setup function
playerBall = True #
player = balloon( 260, 400 + BORDER)
player.draw(win)
pygame.display.update()
while run:
    clock.tick(15)
    playerClock += .1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if not (playerBall):
        print("here")
        player.balloonImage = balloonImage[random.randint(0, balloonRange)]
        player.x = 260
        player.y = 388 + BORDER
        playerBall = True
         
        
       
    keys = pygame.key.get_pressed()


     
    if keys[pygame.K_LEFT] and player.x > 0+ BORDER:
        allowMove = True
        for item in balloons:
            if (item.x + playerStep == player.x) and  (item.y + playerStep > player.y):
                allowMove = False
        if allowMove:
            player.x -=  playerStep
    elif keys[pygame.K_RIGHT] and player.x < 520- playerStep*2:
        allowMove = True
        for item in balloons:
            if (item.x  == player.x + playerStep) and  (item.y + playerStep > player.y):
                allowMove = False
        if allowMove:
            player.x += playerStep

     
    if not (player.isFlying):
        
        if keys[pygame.K_SPACE]:
            player.isFlying = True
            

    else:
        player.stop = BORDER
        largestY = BORDER
        for item in balloons:
            if item.x == player.x:
                if item.y >= largestY:
                    largestY = item.y
                    player.stop = largestY + playerStep
                
        print(largestY, '  ', player.stop)     
        if player.y > player.stop:
            player.y -=  playerStep//8
        elif player.y < player.stop:
            player.y = player.stop
            
        else: 
            player.isFlying = False
            playerBall = False
            balloons.append(balloon(player.x,player.y))
            balloons[-1].balloonImage = player.balloonImage
            aboveIndex = -1
            yVal = 0
            i = 0
            while i < len(balloons)-1:
                if round(balloons[i].x) == round(balloons[-1].x):
                    if balloons[i].y > yVal:
                        yVal = balloons[i].y
                        print(yVal)
                        aboveIndex = i
                i +=1
            print(aboveIndex)
            if not aboveIndex == -1:
                if balloons[-1].balloonImage == balloons[aboveIndex].balloonImage:
                    del balloons[-1]
                    del balloons[aboveIndex]
            logBalloons(balloons)          
            
    
    reDrawGameWindow()
pygame.quit()
    
