import pygame
import time
import warnings
from algorithms import *

warnings.filterwarnings('ignore')

screenWidth, screenHeight = 800, 600
screenYStart = screenHeight / 4
screenYSize = screenHeight * 3 / 4

window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pathfinding Visualizer')

pygame.init()

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (120, 120, 120)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

def drawText(surface, text, centerX, centerY, fontName = 'Arial', size = 20, color = BLACK):
    font = pygame.font.Font(fontName, size)
    textSurface = font.render(text, True, color)
    textBox = textSurface.get_rect()
    textBox.midtop = (centerX, centerY - size / 2)
    surface.blit(textSurface, textBox)

class Button(object):
    def __init__(self, centerX, centerY, sizeX, sizeY, buttonColor = WHITE, \
        text = None, fontName = None, textSize = None, textColor = BLACK):
        self.centerX = centerX
        self.centerY = centerY
        self.sizeX, self.sizeY = sizeX, sizeY
        self.buttonColor = buttonColor
        self.text = text
        self.fontName = pygame.font.match_font(fontName)
        self.textSize = textSize
        self.textColor = textColor
    
    def pointInButton(self, x, y):
        return ((self.centerX - self.sizeX / 2 <= x <= self.centerX + self.sizeX / 2) and \
            (self.centerY - self.sizeY / 2 <= y <= self.centerY + self.sizeY / 2))

    def drawButton(self):
        pygame.draw.rect(window, self.buttonColor, (self.centerX - self.sizeX/2,\
            self.centerY - self.sizeY/2, self.sizeX, self.sizeY))
        if self.text != None:
            drawText(window, self.text, self.centerX, self.centerY, self.fontName, self.textSize, self.textColor)

class Cell(object):
    def __init__(self, totRows, totCols, row, col, xSize, ySize):
        self.row = row
        self.col = col
        self.xPos = screenWidth / totCols * self.col
        self.yPos = screenYSize / totRows * self.row + screenYStart
        self.xSize = xSize
        self.ySize = ySize
        self.fill = WHITE

    def isInCell(self, x, y):
        return ((self.xPos <= x < self.xPos + self.xSize) and (self.yPos <= y < self.yPos + self.ySize))

    def drawCell(self):
        pygame.draw.rect(window, self.fill, (self.xPos + 1, self.yPos + 1, self.xSize - 2, self.ySize - 2))        

class Visualizer(object):
    def __init__(self, rows = 20, cols = 30):
        self.rows = rows
        self.cols = cols
        self.board = self.getBoard(self.rows, self.cols)
        self.start = (0,0)
        self.end = (self.rows - 1, self.cols - 1)
        self.start, self.end = ((0,0), (self.rows - 1, self.cols - 1))
        self.running = True
        self.visualize = False
        self.clock = pygame.time.Clock()
        self.toFill = None
        self.heading = Button(screenWidth / 2, screenHeight / 8, screenWidth, screenHeight /4, buttonColor = WHITE, \
            text = 'A* Visualizer', fontName = 'Arial', textSize = 50, textColor = BLACK)
        self.solved = False
        self.openList = []
        self.closedList = []
        self.path = []
        self.quit = False

    def getBoard(self, rows, cols):
        board = set()
        for row in range(self.rows):
            for col in range(self.cols):
                board.add(Cell(self.rows, self.cols, row, col, screenWidth / self.cols, screenYSize / self.rows))
        return board

    def get2DList(self):
        board = [['-'] * self.cols for r in range(self.rows)]
        for cell in self.board:
            board[cell.row][cell.col] = cell.fill
        return board

    def drawAll(self):
        pygame.draw.rect(window, GRAY, (0, 0, screenWidth, screenHeight))
        for cell in self.board:
            if (cell.row, cell.col) == self.start:
                cell.fill = RED
            elif (cell.row, cell.col) == self.end:
                cell.fill = GREEN
            cell.drawCell()
        self.heading.drawButton()     

    def showPath(self):
        for cell in self.board:
            if cell.fill == BLUE:
                cell.fill = WHITE
        start = self.start
        board = self.get2DList()
        end = self.end
        path, openList, closedList = aStar(board, start, end)
        if path == None:
            return
        for cell in self.board:
            if (cell.row, cell.col) in path:
                cell.fill = BLUE

    def showStep(self):
        for cell in self.board:
            if cell.fill == BLUE or cell.fill == ORANGE or cell.fill == YELLOW:
                cell.fill = WHITE
        self.visualize = True
        self.solved = False
        while self.visualize:
            self.clock.tick(60)
            if not self.solved:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.visualize = False
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.visualize = False
                        self.openList, self.closedList = [], []
                if len(self.openList) == 0:
                    self.openList = [Node([self.start], 0, self.end)]
                board = self.get2DList()
                path, openList, closedList = getNextStep(board, self.start, self.end, self.openList, self.closedList)
                if path == None:
                    openListLocation = []
                    for node in openList:
                        openListLocation.append((node.row, node.col))
                        if self.end in node.path: 
                            self.solved = True
                            self.showPath()
                    closedListLocation = []
                    for node in closedList:
                        closedListLocation.append((node.row, node.col))
                    for cell in self.board:
                        if (cell.row, cell.col) in closedListLocation:
                            cell.fill = ORANGE
                        if (cell.row, cell.col) in openListLocation:
                            cell.fill = YELLOW
                if len(openList) == 0:
                    self.solved = True
                self.openList = copy.deepcopy(openList)
                self.closedList = copy.deepcopy(closedList)
                self.drawAll()
                pygame.display.update()
                if self.solved:
                    self.openList = []
                    self.closedList = []
                    break

    def run(self):
        drag = False
        dragStart, dragEnd = False, False
        while self.running:
            self.clock.tick(30)
            self.drawAll()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if screenYStart <= y <= screenHeight:
                        for cell in self.board:
                            if cell.isInCell(x, y):
                                if cell.fill == WHITE or cell.fill == BLUE or \
                                    cell.fill == YELLOW or cell.fill == ORANGE:
                                    drag = True
                                    cell.fill = BLACK
                                    self.toFill = BLACK
                                elif cell.fill == BLACK:
                                    drag = True
                                    cell.fill = WHITE
                                    self.toFill = WHITE
                                elif cell.fill == RED:
                                    cell.fill = WHITE
                                    self.start = None
                                    dragStart = True
                                elif cell.fill == GREEN:
                                    cell.fill = WHITE
                                    self.end = None
                                    dragEnd = True
                        if dragEnd or dragStart:
                            for cell in self.board:
                                if cell.fill == BLUE:
                                    cell.fill = WHITE
                elif event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()
                    if drag:
                        for cell in self.board:
                            if cell.isInCell(x, y):
                                if cell.fill == WHITE or cell.fill == BLACK:
                                    cell.fill = self.toFill
                                if (cell.fill == BLUE or cell.fill == YELLOW or cell.fill == ORANGE)\
                                    and self.toFill == BLACK:
                                    cell.fill = BLACK
                elif event.type == pygame.MOUSEBUTTONUP:
                    drag = False
                    self.toFill = None
                    x, y = pygame.mouse.get_pos()
                    if x > screenWidth: x = screenWidth
                    elif x < 0: x = 0
                    if y < screenYStart: y = screenYStart // 1
                    elif y > screenHeight: y = screenHeight // 1
                    if dragStart:
                        for cell in self.board:
                            if cell.isInCell(x, y):
                                cell.fill = RED
                                self.start = (cell.row, cell.col)
                    if dragEnd:
                        for cell in self.board:
                            if cell.isInCell(x, y):
                                cell.fill = GREEN
                                self.end = (cell.row, cell.col) 
                    dragStart, dragEnd = False, False                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not (drag or dragStart or dragEnd):
                            self.showPath()
                    if event.key == pygame.K_r:
                        for cell in self.board:
                            cell.fill = WHITE
                    if event.key == pygame.K_v:
                        self.showStep()
                        self.showPath()
            if dragStart:
                pygame.draw.circle(window, RED, (x // 1,y // 1), int(min(screenWidth / self.cols, screenHeight / self.rows) / 3))
            if dragEnd:
                pygame.draw.circle(window, GREEN, (x,y), int(min(screenWidth / self.cols, screenHeight / self.rows) / 3))
            pygame.display.update()
            
    
visualizer = Visualizer()
visualizer.run()

pygame.quit()