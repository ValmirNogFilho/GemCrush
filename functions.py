import random
from gem import *
import pickle
from pygame import mouse
SLOT_SQUARE = 60

class Button:
    def __init__(self, pos, size, txt):
        self.pos_button = pos
        self.size_button = size
        self.txt = txt

    def mouse_sobre_botao(self):
        mouse_pos = mouse.get_pos()
        return mouse_pos[0] in range(self.pos_button[0], self.size_button[0]) and \
            mouse_pos[1] in range(self.pos_button[1], self.size_button[1])
        # if  self.pos_button[0] < mouse_pos[0] <  self.pos_button[0] + self.size_button[0] and \
        #     self.pos_button[1] < mouse_pos[1] <  self.pos_button[1] + self.size_button[1]:
        #     return True
        # return False


class Data:
    points = 0
    victories = 0
    fails = 0
    
    def getPoints(self):
        return self.points
    
    def getVictories(self):
        return self.victories
    
    def getFails(self):
        return self.fails
    
    def addPoints(self, pts):
        self.points += pts
    
    def addVictories(self, vic):
        self.victories += vic
    
    def addFails(self, fails):
        self.fails += fails
    
    def transformIn(self, obj):
        self.addPoints(obj.getPoints())
        self.addFails(obj.getFails())
        self.addVictories(obj.getVictories())
    
    def loadFile(self):
        try:
            with open("data.dat", "rb") as data:
                dt = pickle.load(data)
                self.transformIn(dt)
        except: pass
    def saveOnFile(self):
        with open("data.dat", "wb") as data:
            pickle.dump(self, data)

class Point:
    linha = 0
    coluna = 0
    def __init__(self, linha, coluna) -> None:
        self.linha = linha
        self.coluna = coluna


def choice(x, y):
    gems = [Emerald(x, y), Diamond(x, y), Amethist(x, y), Ruby(x, y), Saphire(x, y)]
    return random.choice(gems)

def generatesTable():
    table = []
    for i in range(6):
        linha = []
        for j in range(6):
            gem = choice(j*SLOT_SQUARE+5, i*SLOT_SQUARE+5)
            linha.append(gem)
        table.append(linha)
    return table

def sequenceCoordinates(l: list):
    counter = 1
    previous = Void(0, 0)
    sequence = (0, 0, previous)
    for obj in l:

        if type(obj) == type(previous): #se 2 adjacentes são iguais, incrementa em counter
            counter += 1
        else:
            if counter >= 3: # pelo menos 3 adjacentes são iguais. se a sequência para no meio
                          # da lista e houve pelo menos 3 adjacentes, retorna a tupla

                sequence = (l.index(previous), counter, previous) #a tupla informa a posição do último
                                                #elemento da sequência e o tamanho dela
                break
            counter = 1
        previous = obj

    if counter >= 3:
        sequence = (l.index(previous), counter, previous)
    return sequence


def changeGemToVoid(l, index, quantity):
    for i in range(index, index-quantity, -1):
        l[i] = Void(l[i].x, l[i].y)

def sequenceFounded(l):
    counter = 1
    
    for i in range(len(l)-1):
        if type(l[i]) == type(l[i+1]) and not(isinstance(l[i], Void)):
            counter += 1
            if counter == 3:
                return True
        else: counter = 1
    return False

def SequencesFoundedOnTable(table):
    sequences = []
    for i in range(len(table)):
        if sequenceFounded(table[i]): sequences.append(("row", i))
        col = getListOfColumns(table, i)
        if sequenceFounded(col): sequences.append(("col", i))    
    return sequences

#voidSort foi transferida para o arquivo game, para evitar problemas relativos a circular imports

        
def refeedList(l): #substitui todos elementos da classe Void por novas gemas aleatórias
    for i in range(len(l)):
        if isinstance(l[i], Void):
            x = l[i].x
            y = l[i].y #passa coordenadas do objeto anterior para o novo
            l[i] = choice(x, y)
        else: return

def point(pos_x, pos_y):
    coluna = pos_x //SLOT_SQUARE
    linha = pos_y //SLOT_SQUARE

    return Point(linha, coluna)

def canswap(A : Point, B : Point):
    ax, ay = A.linha, A.coluna 
    bx, by = B.linha, B.coluna

    return abs(ax - bx) <= 1 and (ay - by) == 0 or abs(ay - by) <= 1 and (ax - bx) == 0

def getListOfColumns(table, x):
    return [table[i][x] for i in range(len(table))]

def setColumnOnTable(table, l, x):
    for i in range(len(table)):
        table[i][x] = l[i]

def swap(A : Point, B : Point, table):
    aL, aC = A.linha, A.coluna
    bL, bC = B.linha, B.coluna
    swap_in(table, A, B)
    if aL == bL:
        colunaA = getListOfColumns(table, aC)
        colunaB = getListOfColumns(table, bC)

        if not(sequenceFounded(table[aL]) or sequenceFounded(colunaA) or sequenceFounded(colunaB)):
            swap_in(table, A, B)
        else:
            table[aL][aC].x, table[bL][bC].x = table[bL][bC].x, table[aL][aC].x
            table[aL][aC].y, table[bL][bC].y = table[bL][bC].y, table[aL][aC].y

    elif aC == bC:            
        coluna = getListOfColumns(table, aC)
        if not(sequenceFounded(coluna) or sequenceFounded(table[aL]) or sequenceFounded(table[bL])):
            swap_in(table, A, B)
        else:
            table[aL][aC].x, table[bL][bC].x = table[bL][bC].x, table[aL][aC].x
            table[aL][aC].y, table[bL][bC].y = table[bL][bC].y, table[aL][aC].y

def swap_in(table, A : Point, B : Point):
    table[A.linha][A.coluna], table[B.linha][B.coluna] = table[B.linha][B.coluna], table[A.linha][A.coluna]

def sequenceTips(table):
    tips = []
    size = len(table)
    for i in range(size-1):
        for j in range(size):
            A = Point(i, j)
            B = Point(i+1, j)
            swap_in(table, A, B)
            if sequenceFounded(table[i]):
                tips.append((A, B))
            swap_in(table, A, B)

    for i in range(size):
        for j in range(size-1):
            A = Point(i, j)
            B = Point(i, j+1)
            swap_in(table, A, B)
            if sequenceFounded(getListOfColumns(table, j)):
                tips.append((A, B))
            swap_in(table, A, B)

    return tips