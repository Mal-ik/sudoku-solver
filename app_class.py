import sys
import pygame
import requests  # gets html
from bs4 import BeautifulSoup  # allows us to manipulate html
from settings import *
from buttonClass import *
from solver import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(
            (WIDTH, HEIGHT))  # creates display window
        self.running = True  # checks whether game is running
        self.selected = None  # when something selected
        self.mousePos = None  # mouse pos
        self.state = "playing"  # determines state of board
        self.cellChanged = False
        self.finished = False
        self.incorrectCells = []
        self.playingButtons = []  # stores buttons for the play state
        self.lockedCells = []
        self.font = pygame.font.SysFont('Arial', cellSize // 2)
        self.getPuzzle("3")

    # runs game functions while its running
    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()
        sys.exit()

##### PLAYING STATE FUNCTIONS #####
    # checks for events and acts appropriately
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # User clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playingButtons:
                        if button.highlighted:
                            button.click()

            # User types
            if event.type == pygame.KEYDOWN:
                if self.selected and self.selected not in self.lockedCells:
                    # not using isinstance() or type() becvause python uses Duck Typing
                    if self.isInt(event.unicode):
                        self.grid[self.selected[0]][self.selected[1]] = int(
                            event.unicode)
                        self.cellChanged = True

    # updates thigns every frame for play state
    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)

        if self.cellChanged:
            self.incorrectCells = []
            if self.allCellsDone():
                self.finished = True
                self.checkAllCells()
                if not self.incorrectCells:
                    self.finished = True

    # draws board in play state
    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playingButtons:
            button.draw(self.window)

        if self.selected:
            # dont need window but good for redundancy
            self.drawSelection(self.window, self.selected)

        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeIncorrectCells(self.window, self.lockedCells)

        self.drawNumbers(self.window)

        self.drawGrid(self.window)
        pygame.display.update()

        self.cellChanged = False

##### CHECK FUNCTIONS #####
    def allCellsDone(self):
        for row in self.grid:
            for num in row:
                if not num:
                    return False
        return True

    def checkAllCells(self):
        for ridx, row in enumerate(self.grid):
            for cidx, num in enumerate(row):
                if [ridx, cidx] not in self.lockedCells and [ridx, cidx] not in self.incorrectCells:
                    if not valid(self.grid, ridx, cidx, num):
                        self.incorrectCells.append([ridx, cidx])

##### HELPER FUNCTIONS #####
    def getPuzzle(self, difficulty):
        # difficulty must be passed in as string ("1"-"4")
        html_doc = requests.get(
            f"https://nine.websudoku.com/?level={difficulty}").content
        soup = BeautifulSoup(html_doc, features="html.parser")
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f10', 'f11',
               'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f20', 'f21', 'f22', 'f23',
               'f24', 'f25', 'f26', 'f27', 'f28', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35',
               'f36', 'f37', 'f38', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47',
               'f48', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f60',
               'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f70', 'f71', 'f72',
               'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f80', 'f81', 'f82', 'f83', 'f84',
               'f85', 'f86', 'f87', 'f88']
        data = []
        for cid in ids:
            data.append(soup.find('input', id=cid))
        board = [[0 for x in range(9)] for x in range(9)]
        for index, cell in enumerate(data):
            try:
                board[index//9][index % 9] = int(cell['value'])
            except:
                pass
        self.grid = board
        self.load()

    def drawSelection(self, window, pos):
        pygame.draw.rect(
            window, LIGHTBLUE, (pos[1]*cellSize + gridPos[0], pos[0] * cellSize + gridPos[1], cellSize, cellSize))

    def shadeIncorrectCells(self, window, locked):
        for cell in self.incorrectCells:
            pygame.draw.rect(window, INCORRECTCELLCOLOUR, (
                cell[1]*cellSize + gridPos[0], cell[0]*cellSize + gridPos[1], cellSize, cellSize))

    def shadeLockedCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, LOCKEDCELLCOLOUR, (
                cell[1]*cellSize + gridPos[0], cell[0]*cellSize + gridPos[1], cellSize, cellSize))

    def drawNumbers(self, window):
        # changes color of selected cell
        for ridx, row in enumerate(self.grid):
            for cidx, num in enumerate(row):
                if num:
                    pos = [cidx*cellSize + gridPos[0],
                           ridx*cellSize + gridPos[1]]
                    self.textToScreen(window, str(num), pos)

    def drawGrid(self, window):
        # draw black rectangle on window in gridPos w thickness = 2
        pygame.draw.rect(
            window, BLACK, (gridPos[0], gridPos[1], WIDTH - 150, HEIGHT - 150), 2)  # goes width - 150 right and height - 150 down from starting pos
        for x in range(9):
            # every 3 steps draw a thicker line
            pygame.draw.line(window, BLACK,
                             (gridPos[0], gridPos[1] + x*cellSize), (gridPos[0] + 450, gridPos[1] + x * cellSize), 2 if x % 3 == 0 else 1)
            pygame.draw.line(window, BLACK,
                             (gridPos[0] + x*cellSize, gridPos[1]), (gridPos[0] + x*cellSize, gridPos[1] + 450), 2 if x % 3 == 0 else 1)

    def mouseOnGrid(self):
        # checks if mouse out of grid
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1] or self.mousePos[0] > gridPos[0] + gridSize or self.mousePos[1] > gridPos[1] + gridSize:
            return False
        # else returns selected box
        return [(self.mousePos[1] - gridPos[1])//cellSize, (self.mousePos[0]-gridPos[0])//cellSize]

    # creates all buttons
    def loadButtons(self):
        self.playingButtons.append(Button(
            20, 40, WIDTH//7, 40, function=self.checkAllCells, colour=(27, 142, 207), text="Check"))
        self.playingButtons.append(Button(
            140, 40, WIDTH//7, 40, function=self.getPuzzle, params="1",  colour=(117, 172, 112), text="Easy"))
        self.playingButtons.append(Button(
            260, 40, WIDTH//7, 40, function=self.getPuzzle, params="2",  colour=(204, 197, 110), text="Medium"))
        self.playingButtons.append(Button(
            380, 40, WIDTH//7, 40, function=self.getPuzzle, params="3",  colour=(199, 129, 48), text="Hard"))
        self.playingButtons.append(Button(
            500, 40, WIDTH//7, 40, function=self.getPuzzle, params="4",  colour=(207, 68, 67), text="Evil"))

    def textToScreen(self, window, text, pos, color=BLACK):
        font = self.font.render(text, False, color)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth) // 2
        pos[1] += (cellSize - fontHeight) // 2
        window.blit(font, pos)

    def load(self):
        self.playingButtons = []
        self.loadButtons()
        self.lockedCells = []
        self.incorrectCells = []
        self.finshed = False

        # setting locked cells from original board
        for ridx, row in enumerate(self.grid):
            for cidx, num in enumerate(row):
                if num:
                    self.lockedCells.append([ridx, cidx])

    # In duck typing, an object's suitability is determined by the presence of certain methods and properties, rather than the type of the object itself.
    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False
