import pygame
import sys
import math

print("1st player will play the first move")

firstPlayer = input("1st player (X): ")
secondPlayer = input("2nd player (O): ")

print(f"{firstPlayer}'s symbol is X")
print(f"{secondPlayer}'s symbol is O")

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COL = (18, 192, 234)
CROXX = (122, 97, 144)
CR1XX = (113, 131, 83)
CR2XX = (250, 100, 70)

# Set up the display
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Dots Game")


# Font for displaying text
font = pygame.font.SysFont("Arial", 24)

START_POINT = 100
END_POINT = 500
SPACING = 50
DOT_RADIUS = 10

dots = []
dic = {}

for x in range(START_POINT, END_POINT + SPACING, SPACING):
    
    for y in range(START_POINT, END_POINT + SPACING, SPACING):
        
        dots.append((x,y))

for x in range(START_POINT, END_POINT, SPACING):
    
    for y in range(START_POINT, END_POINT, SPACING):
        
        one = (x, y)
        two = (x, y + SPACING)
        three = (x + SPACING, y)
        four =  (x + SPACING, y + SPACING)
        key = frozenset({one, two, three, four})
        dic[key] = [[], None]



def draw_grid():
    
    for dot in dots:
        
        pygame.draw.circle(screen, BLACK, dot, DOT_RADIUS)
    
def isValidPoint(pos, point, radius):
    
    return math.sqrt((pos[0] - point[0])**2 + (pos[1] - point[1])**2) <= radius

def isValidLine(line):
    
    if line == None:

        return False
    
    pointA = line[0]
    pointB = line[1]

    if pointA[0] == pointB[0] and abs(pointA[1] - pointB[1]) == SPACING:

        return True
    
    elif pointA[1] == pointB[1] and abs(pointA[0] - pointB[0]) == SPACING:

        return True
    
    else:
        
        return False


dragging = False
startingPoint = None
lines = []
player = 0
players = (firstPlayer, secondPlayer)
symbols = ('X', 'O')
colors = (CROXX, CR1XX)
lineWidth = 5

def drawLines():
    
    for line in lines:
        
        pygame.draw.line(screen, CR2XX, line[0], line[1], lineWidth)


def drawX(squarePoints):
    
    squarePoints = sorted(squarePoints)
    
    one = (squarePoints[0][0] + 10, squarePoints[0][1] + 10)
    two = (squarePoints[1][0] + 10, squarePoints[1][1] - 10)
    three = (squarePoints[2][0] - 10, squarePoints[2][1] + 10)
    four = (squarePoints[3][0] - 10, squarePoints[3][1] - 10)
    
    color = colors[symbols.index('X')]
    
    pygame.draw.line(screen, color, one, four, lineWidth)  
    pygame.draw.line(screen, color, two, three, lineWidth)  


def drawO(squarePoints):

    squarePoints = sorted(squarePoints)

    one = (squarePoints[0][0], squarePoints[0][1])
    two = (squarePoints[1][0], squarePoints[1][1])
    three = (squarePoints[2][0], squarePoints[2][1])
    four = (squarePoints[3][0], squarePoints[3][1])
    
    center = ((one[0] + four[0]) // 2, (one[1] + four[1]) // 2)
    radius = abs(one[0] - four[0]) / 2.5

    color = colors[symbols.index('O')]
    
    pygame.draw.circle(screen, color, center, radius, lineWidth)




def showScores():
    
    scores = [0, 0]
    
    for key in dic:

        value = dic[key]

        l = value[0]

        if len(l) == 4:
            who = value[1]
            scores[who] += 1

    start_x = 20
    
    start_y = 5

    y_offset = 10

    spacing = 30
    
    for who in range(len(players)):
        
        p = players[who]
        
        score = scores[who]

        color = colors[who]
        
        text = font.render(f"{p}: {score}", True, color)

        screen.blit(text, (start_x, start_y + y_offset))

        y_offset += spacing

    isGameOver = len(dic) == scores[0] + scores[1]
    
    #Show who's turn

    sx, sy = WIDTH // 2 - 60, 30
    
    if isGameOver == False:    

        whosTurn = players[player]
    
        text = font.render(f"{whosTurn}'s turn", True, BLUE)
           
        screen.blit(text, (sx, sy))
        
    else:
        
        text = font.render("Game over!", True, RED)
           
        screen.blit(text, (sx, sy))

    #end of show who's turn

    

    if isGameOver == True:
        
       isDraw = scores[0] == scores[1]
       
       if isDraw == True:
           
           sx, sy = WIDTH // 2 - 60, HEIGHT - 60
           
           text = font.render("It's a draw", True, COL)
           
           screen.blit(text, (sx, sy))
           
       else:
           
           winner = players[0] if (scores[0] > scores[1]) else players[0] 
           
           text = font.render(f"{winner} wins", True, COL)
           
           sx, sy = WIDTH // 2 - 60, HEIGHT - 60
           
           screen.blit(text, (sx, sy))
        
        
def drawSymbols():
    
    for key in dic:
        
        value = dic[key]
        l = value[0]
        who = value[1]

        squarePoints = list(key)
        
        if len(l) == 4:
            
            if symbols[who] == 'X':
                
                drawX(squarePoints)
                
            elif symbols[who] == 'O':
                
                drawO(squarePoints)
            
        
while True:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            pygame.quit()
            
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            for dot in dots:
                
                if(isValidPoint(event.pos, dot, DOT_RADIUS)):
                    
                    dragging = True
                    
                    startingPoint = dot
                    
                    break
                
        elif event.type == pygame.MOUSEBUTTONUP:
            
            if dragging and startingPoint in dots:
                
                line = None
                
                reverse_line = None
                
                for dot in dots:
                    
                    if(dot != startingPoint and isValidPoint(event.pos, dot, DOT_RADIUS)):

                        line = (startingPoint, dot)
                        
                        reverse_line = (dot, startingPoint)

                        dragging = False
                        
                        startingPoint = None
                        
                        break
                    
                isValid = isValidLine(line)
                
                if isValid:
                    
                    if (line not in lines) and (reverse_line not in lines):

                        playerName = players[player]
                        
                        print(f"This line {line} is drawn by {playerName}")
                              
                        lines.append(line)
                        

                        isAgain = False
                        
                        for key in dic:
                            
                            pointA = line[0]
                            
                            pointB = line[1]
                            
                            if (pointA in key) and (pointB in key):
                                
                                value = dic[key]
                                
                                sqr = value[0]
                                
                                who = value[1]

                                sqr.append(line)

                                if len(sqr) == 4:
                                    
                                    who = player

                                    isAgain = True     

                                value[0] = sqr
                                
                                value[1] = who

                                dic[key] = value
                        
                        if isAgain == False:
                            
                            player = 1 - player
                            
                            
    screen.fill(WHITE)
    draw_grid()
    drawLines()
    drawSymbols()
    showScores()
        
    pygame.display.update()
