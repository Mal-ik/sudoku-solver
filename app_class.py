import sys
import pygame
from settings import *
from buttonClass import *
from solver import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(
            (WIDTH, HEIGHT))  # creates display window
        self.running = True  # checks whether game is running
        self.grid = finishedBoard
        self.selected = None  # when something selected
        self.mousePos = None  # mouse pos
        self.state = "playing"  # determines state of board
        self.cellChanged = False
        self.finished = False
        self.incorrectCells = []
        self.playingButtons = []  # stores buttons for the play state
        self.menuButtons = []
        self.endButtons = []
        self.lockedCells = []
        self.font = pygame.font.SysFont('Arial', cellSize // 2)
        self.load()  # to keep init function neater

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
                    print('not on grid')
                    self.selected = None

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
                    print('Congratulations')

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
        self.playingButtons.append(Button(20, 40, 100, 40))

    def textToScreen(self, window, text, pos, color=BLACK):
        font = self.font.render(text, False, color)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth) // 2
        pos[1] += (cellSize - fontHeight) // 2
        window.blit(font, pos)

    def load(self):
        self.loadButtons()

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
