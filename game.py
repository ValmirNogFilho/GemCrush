import pygame
from gem import *
import functions as fnc
import os
#setup
pygame.init()

clock = pygame.time.Clock()
running = False
counter = 0 #conta quantidade de cliques para fazer swap
table = fnc.generatesTable()
points = 0
won = False
game_over = False
help_button_clicked = False

game_state = "start"
data = fnc.Data()
data.loadFile()
BLACK = (0,0,0)
DARK_BLUE = (81, 32, 215)
DIMENSIONS = 360
pos_button_tip = (DIMENSIONS-85, DIMENSIONS-2)
size_button_tip = (68, 27)
pos_button_help = (DIMENSIONS+332, 6)
size_button_help = (25, 24)
source_file_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(source_file_dir)

screen = pygame.display.set_mode((DIMENSIONS*2, DIMENSIONS + 30))
font = pygame.font.Font(None,40)

def startRender():
    font = pygame.font.Font("res/alterebro-pixel-font.ttf", 80)
    pygame.display.set_caption("Pressione ESPAÇO para começar")
    screen.fill(DARK_BLUE)
    text = font.render("Gem Crush++".format(points), True, (0, 0, 0))
    rect = text.get_rect()
    rect.x, rect.y = (DIMENSIONS-text.get_width()/2, DIMENSIONS/2-text.get_height()/2)
    screen.blit(text, rect)

def renderStats():
    global help_button_clicked
    help_button = "help.png" if help_button_clicked else "stats.png"
    stats = pygame.image.load(os.path.join(source_file_dir , "res", help_button))
    rectstats = stats.get_rect()
    rectstats.x, rectstats.y = (DIMENSIONS, 0)
    screen.blit(stats, rectstats)
    if not(help_button_clicked):
        txtwins = font.render("{}".format(data.getVictories()), True, BLACK)
        txtfails = font.render("{}".format(data.getFails()), True, BLACK)
        txtpoints = font.render("{}".format(data.getPoints()), True, BLACK)
        prect = txtpoints.get_rect()
        prect.x, prect.y = (600, 120)
        screen.blit(txtpoints, prect)
        wrect = txtwins.get_rect()
        wrect.x, wrect.y = (520, 175)
        screen.blit(txtwins, wrect)
        frect = txtfails.get_rect()
        frect.x, frect.y = (520, 225)
        screen.blit(txtfails, frect)


def gameRender(table):
    pygame.display.set_caption("Gem Crush++")
    global points
    screen.fill(DARK_BLUE)
    for i in range(6):
        for j in range(6):
            g = table[i][j]
            g.render(screen)
    text = font.render("PONTOS: {}".format(points), True, (0, 0, 0))
    screen.blit(text, (10, DIMENSIONS))
    color = (255, 104, 3)
    
    
    
    tip_text = font.render("DICA", True, BLACK)
    
    rect = pygame.draw.rect(screen, color, ( pos_button_tip[0], pos_button_tip[1],
                                             size_button_tip[0], size_button_tip[1]))
    screen.blit(tip_text, rect)
    renderStats()
  
def render(table, game_state):

    if game_state == "start":
        startRender()
    elif game_state == "game":
        gameRender(table)
    if game_over:
        screen.fill((40, 40, 40))
        
        renderStats()
        game_over_file = "won.png" if won else "lose.png"
        img = pygame.image.load(os.path.join(source_file_dir , "res", game_over_file))
        rect = img.get_rect()
        screen.blit(img, rect)
    
    pygame.display.flip()


def voidSort(table, x, running): #semelhante ao bubble sort, joga todos objetos da classe Void para o começo da coluna x
    size = len(table)
    for i in range(1, size):
        for j in range(size-1, i-1, -1):
            if (isinstance(table[j][x], Void)):
                table[j][x], table[j-1][x] = table[j-1][x], table[j][x]
                table[j][x].x, table[j-1][x].x = table[j-1][x].x, table[j][x].x
                table[j][x].y, table[j-1][x].y = table[j-1][x].y, table[j][x].y
                if running: #para impedir que a etapa de preload seja renderizada
                    pygame.time.wait(250)
                    render(table, game_state)
    

def cleanGems():
    sequences = fnc.SequencesFoundedOnTable(table)
    global points
    while sequences:
        for sqc in sequences:
            
            i = sqc[1]
            if sqc[0] == "row":
                
                index, quantity, typeobj = fnc.sequenceCoordinates(table[i])
                fnc.changeGemToVoid(table[i], index, quantity)
                render(table, game_state)
                pygame.time.wait(250)
                for j in range(len(table)):
                    voidSort(table, j, running)
                    col = fnc.getListOfColumns(table, j)
                    fnc.refeedList(col)
                    fnc.setColumnOnTable(table, col, j)
                
            
            else:
                col = fnc.getListOfColumns(table, i)
                index, quantity, typeobj = fnc.sequenceCoordinates(col)
                fnc.changeGemToVoid(col, index, quantity)
                render(table, game_state)
                fnc.setColumnOnTable(table, col, i)
                voidSort(table, i, running)
                col = fnc.getListOfColumns(table, i)
                fnc.refeedList(col)
                fnc.setColumnOnTable(table, col, i)

            points += typeobj.pts * quantity

            sequences.pop(0)     
        sequences = fnc.SequencesFoundedOnTable(table)

def preload():
    sequences = fnc.SequencesFoundedOnTable(table)
    
    while sequences:
        for sqc in sequences:
            
            i = sqc[1]
            if sqc[0] == "row":
                
                index, quantity, typeobj = fnc.sequenceCoordinates(table[i])
                fnc.changeGemToVoid(table[i], index, quantity)
                for j in range(len(table)):
                    voidSort(table, j, running)
                    col = fnc.getListOfColumns(table, j)
                    fnc.refeedList(col)
                    fnc.setColumnOnTable(table, col, j)
            
            else:
                col = fnc.getListOfColumns(table, i)
                index, quantity, typeobj = fnc.sequenceCoordinates(col)
                fnc.changeGemToVoid(col, index, quantity)
                fnc.setColumnOnTable(table, col, i)
                voidSort(table, i, running)
                col = fnc.getListOfColumns(table, i)
                fnc.refeedList(col)
                fnc.setColumnOnTable(table, col, i)

            

            sequences.pop(0)     
        sequences = fnc.SequencesFoundedOnTable(table)

def mouse_sobre_botao(pos_button, size_button):
    mouse_pos = pygame.mouse.get_pos()
    if  pos_button[0] < mouse_pos[0] <  pos_button[0] + size_button[0] and \
        pos_button[1] < mouse_pos[1] <  pos_button[1] + size_button[1]:
        return True
    return False



preload()
running = True
#Game loop
while running:
    screen.fill(DARK_BLUE)
    if points > 15 and not(game_over):
        game_over = True
        won = True
        data.addVictories(1)
        data.addPoints(points)
        data.saveOnFile()
        points = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "start":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = "game"
                    
        elif game_state == "game" and not(game_over):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do mouse pressionado
                # Obtém as coordenadas do mouse
                pos = pygame.mouse.get_pos()
                pos_x, pos_y = pos
                
                if pos_y < DIMENSIONS and pos_x < DIMENSIONS:
                    if counter < 1:
                        A = fnc.point(pos_x, pos_y)
                        table[A.linha][A.coluna].clicked = True
                        counter += 1
                    else:
                        B = fnc.point(pos_x, pos_y)
                        table[A.linha][A.coluna].clicked = False
                        table[B.linha][B.coluna].clicked = False
                        if fnc.canswap(A, B):
                            fnc.swap(A, B, table)
                            cleanGems()
                        
                        counter = 0
                elif mouse_sobre_botao(pos_button_tip, size_button_tip):
                   
                    tips = fnc.sequenceTips(table)
                    if tips:
                        A, B = tips.pop(0)
                        table[A.linha][A.coluna].clicked = True
                        table[B.linha][B.coluna].clicked = True
                    elif not(tips) and not(game_over): 
                        game_over = True
                        won = False
                        data.addFails(1)
                        data.saveOnFile()
                        points = 0
                elif mouse_sobre_botao(pos_button_help, size_button_help):
                    help_button_clicked = not(help_button_clicked)
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game_state = "game"
                        game_over = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.key == 1:
                    if mouse_sobre_botao(pos_button_help, size_button_help):
                        help_button_clicked = not(help_button_clicked)
    render(table, game_state)    

    clock.tick(30)

pygame.quit()