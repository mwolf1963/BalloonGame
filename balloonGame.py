#Author: Matt Wolf
#Date:3/16/19,
#3-19 --notes
#working on adding the logic for game over. needs scores. balloons to come. start screen, instructions
#pause, level up options etc
#very rough between classes (or during)
#Description:
#Attempt a simple balloon color match game


#works. need to add logic for score and up coming balls
#also need to add logic for balls next to balls

#import modules
import pygame
import math
import random

#####################################
#init pygame and window variables
#####################################
pygame.init()
#refresh clock
clock = pygame.time.Clock()
#screen size
screen_Width = 750
screen_Height = 500
#define win as our window
win = pygame.display.set_mode(( screen_Width,  screen_Height))
pygame.display.set_caption('Balloon Breaker')
#assign all pictures variables
bg100 = pygame.image.load('backGround100.png')
bg80 = pygame.image.load('backGround80.png')
bg60 = pygame.image.load('backGround60.png')
bg40 = pygame.image.load('backGround40.png')
bg40F = pygame.image.load('backGround40Flash.png')
bg20 = pygame.image.load('backGround20.png')
bg20F = pygame.image.load('backGround20Flash.png')
gameover = pygame.image.load('game over.png')
bg = bg100
###################################################
# init all variables for game play
###################################################
#border width ## not setable constant
BORDER = 4
level = 4
balloons = [] #init the balloon list
run = True
playerStep = 64 #based on the size of the picture
playerBall = True 
restart = True
#images for the balloon
balloonImage = [pygame.image.load("R1.png"),pygame.image.load("O1.png"),pygame.image.load("Y1.png"),pygame.image.load("B1.png"),
          pygame.image.load("P1.png"),pygame.image.load("G1.png"),pygame.image.load("M1.png")]
#variable for which balloons in the list can be called
balloonRange = 5
#player clock for timing game eventually
playerClock = 0
#############################################
#this is a logger to show the position of all
#ballons in the sequence after each move
#############################################
fileout = open("outfile.txt", 'a')
fileout.write("new run" + '_'*48)
fileout.close()
#logger to check balloon positions
def logBalloons(balloons):
    #takes the balloon list as input
    #outputs the file outfile.txt
    #each run of the game is "new run"
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
    if not restart:
        win.blit(gameover, (57,50))
    pygame.display.update()



def moveLeft():
    allowMove = True
    for item in balloons:
        if (item.x + playerStep == player.x) and  (item.y + playerStep > player.y):
            allowMove = False
    if allowMove:
        player.x -=  playerStep

def moveRight():
    allowMove = True
    for item in balloons:
        if (item.x  == player.x + playerStep) and  (item.y + playerStep > player.y):
            allowMove = False
    if allowMove:
        player.x += playerStep

################################################
#setup functions
################################################
setupBoard(level) #run the setup function
player = balloon( 260, 400 + BORDER)
player.draw(win)
pygame.display.update()


################################################
#main game loop
################################################
while run:
    clock.tick(15)
    playerClock += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if not (playerBall):
        #print("here")
        player.balloonImage = balloonImage[random.randint(0, balloonRange)]
        player.x = 260
        player.y = 388 + BORDER
        playerBall = True
    #print(playerClock , bg)
        
    #set bg image attempted to refactor into a function that would take input of playerClock and
    #background did not update. and game play was extremely laggy. leave this as part of the
    #main game loop! 3/24/19
    if playerClock  >= 0 and playerClock  < 15:
        bg = bg100
    elif playerClock > 15 and playerClock  < 30: 
        bg = bg80         
    elif playerClock  > 30 and playerClock < 45: 
        bg = bg60
    elif playerClock  > 45 and playerClock  < 60: 
        bg = bg40
    elif playerClock  > 60 and playerClock  < 80:
        if playerClock % 5 == 0:
            bg = bg20F
        else:
            bg = bg20
    elif playerClock > 75 :
        bg = bg100
        playerClock = 0
        player.isFlying = True
    # leave the above as part of the main game loop
    
    #get keys pressed        
    keys = pygame.key.get_pressed()
    #if player can move they do
    if keys[pygame.K_LEFT] and player.x > 0+ BORDER:
       moveLeft()
    elif keys[pygame.K_RIGHT] and player.x < 520- playerStep*2:
        moveRight()     
    if not (player.isFlying):        
        if keys[pygame.K_SPACE]:
            player.isFlying = True         

    if player.isFlying:
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
                elif yVal > 323:                 
                    restart = False   
                    while not restart:
                            #print('gameover')
                            
                            reDrawGameWindow()
            logBalloons(balloons)          
            
    
    reDrawGameWindow()
pygame.quit()
    
