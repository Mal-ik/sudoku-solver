import sys
import pygame
import requests  # gets html
from bs4 import BeautifulSoup  # allows us to manipulate html
from settings import *
from buttonClass import *
from solver import solve, valid
import time
from datetime import timedelta


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('sudoku')
        self.window = pygame.display.set_mode(
            (WIDTH, HEIGHT))  # creates display window
        self.running = True  # checks whether game is running
        self.selected = None  # when something selected
        self.mousePos = None  # mouse pos
        self.state = "playing"  # determines state of board
        self.cellChanged = False
        self.font = pygame.font.SysFont('Arial', cellSize // 2)
        # make ids to pull cells from sudoku solver
        self.ids = [f'f{j // 9}{j % 9}' for j in range(81)]
        self.getPuzzle("2")

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
                if selected and not self.finished:
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

        if self.cellChanged and not self.finished:
            self.incorrectCells = []
            self.validCells = []
            # if all cells are done and there are no incorrect cells then puzzle is finished
            if self.allCellsDone():
                self.checkAllCells()
                if not self.incorrectCells:
                    self.finished = True

    # draws board in play state
    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playingButtons:
            button.draw(self.window)

        self.shadeIncorrectCells(self.window, self.lockedCells)

        self.shadeValidCells(self.window, self.lockedCells)

        if self.selected:
            # dont need window but good for redundancy
            self.drawSelection(self.window, self.selected)

        self.shadeLockedCells(self.window, self.lockedCells)

        self.drawNumbers(self.window)

        self.drawGrid(self.window)

        # Used button class as a quick way to show finished
        if self.finished:
            finish = Button(131, 280, 340, 40, function=self.playing_events(), colour=(
                255, 255, 255), text="Finished in " + str(self.banner) + ". Congrats!")
            finish.draw(self.window)
        else:
            self.drawTimer(self.window)

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
                    elif [ridx, cidx] not in self.validCells:
                        self.validCells.append([ridx, cidx])

##### HELPER FUNCTIONS #####
    def getPuzzle(self, difficulty):
        self.finished = False
        self.difficulty = int(difficulty)
        # difficulty must be passed in as string ("1"-"4")
        self.startTime = time.time()
        html_doc = requests.get(
            f"https://nine.websudoku.com/?level={difficulty}").content
        soup = BeautifulSoup(html_doc, features="html.parser")
        data = []
        for cid in self.ids:
            data.append(soup.find('input', id=cid))
        board = [[0 for x in range(9)] for x in range(9)]
        for index, cell in enumerate(data):
            try:
                board[index//9][index % 9] = int(cell['value'])
            except:
                pass
        self.grid = board
        # creates a cop to pass on to solver
        self.copy = [x[:]for x in self.grid]
        self.load()

    def drawTimer(self, window):
        font = pygame.font.SysFont("arial", 20, bold="1")
        elapsed = time.time() - self.startTime
        self.banner = str(timedelta(seconds=elapsed))[:-7]
        text = font.render(
            self.banner, False, (0, 0, 0))
        width, height = text.get_size()
        x = 450
        y = 550
        window.blit(text, (x, y))

    def drawSelection(self, window, pos):
        pygame.draw.rect(
            window, LIGHTBLUE, (pos[1]*cellSize + gridPos[0], pos[0] * cellSize + gridPos[1], cellSize, cellSize))

    def shadeIncorrectCells(self, window, locked):
        for cell in self.incorrectCells:
            pygame.draw.rect(window, INCORRECTCELLCOLOUR, (
                cell[1]*cellSize + gridPos[0], cell[0]*cellSize + gridPos[1], cellSize, cellSize))

    def shadeValidCells(self, window, locked):
        for cell in self.validCells:
            pygame.draw.rect(window, VALIDCOLOUR, (
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
            40, 20, WIDTH//6, 40, function=self.getPuzzle, params="1",  colour=(117, 172, 112), text="Easy"))
        self.playingButtons.append(Button(
            180, 20, WIDTH//6, 40, function=self.getPuzzle, params="2",  colour=(204, 197, 110), text="Medium"))
        self.playingButtons.append(Button(
            320, 20, WIDTH//6, 40, function=self.getPuzzle, params="3",  colour=(199, 129, 48), text="Hard"))
        self.playingButtons.append(Button(
            460, 20, WIDTH//6, 40, function=self.getPuzzle, params="4",  colour=(207, 68, 67), text="Evil"))
        self.playingButtons.append(Button(
            180, 540, WIDTH//6, 40, function=self.checkAllCells, colour=(27, 142, 207), text="Check"))
        self.playingButtons.append(Button(
            320, 540, WIDTH//6, 40, function=self.solving, params=self.copy, colour=(27, 142, 207), text="Solve"))

    def solving(self, copy):
        self.grid = copy
        self.incorrectCells = []
        self.validCells = []
        solve(self.grid, self.playing_draw,
              self.incorrectCells, self.validCells, len(self.validCells), self.difficulty - 1)
        self.cellChanged = True
        self.playing_update()

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
        self.validCells = []
        self.banner = 0
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
