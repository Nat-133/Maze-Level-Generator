import json
import random
import os

class Cell:
    def __init__(self, index):
        self.index = index
        self.visited = False
        self.relativeOutLinks = []
    
    def getUnvisitedNeighbours(self, cells):
        neighbours = []
        i = self.index[0]
        j = self.index[1]
        if not cells[self.index[0] - 1][self.index[1]].visited and i > 0:
            neighbours.append((-1, 0))
        
        try:
            if not cells[self.index[0] + 1][self.index[1]].visited:
                neighbours.append((1, 0))
        except IndexError:
            pass
        
        if not cells[self.index[0]][self.index[1] - 1].visited and j > 0:
            neighbours.append((0, -1))
        
        try:
            if not cells[self.index[0]][self.index[1] + 1].visited:
                neighbours.append((0, 1))
        except IndexError:
            pass
        
        return neighbours
    
    def createOutLink(self, cells):
        try:
            relativeOutLink = random.choice(self.getUnvisitedNeighbours(cells))
            self.relativeOutLinks.append(relativeOutLink)
        except IndexError:
            relativeOutLink = None
        self.visited = True
        return relativeOutLink
    
    def __repr__(self):
        return str(self.index)


def generateCells(width, height):
    return [[Cell((i, j)) for j in range(width)] for i in range(height)]


def generateMaze(width, height):
    cells = generateCells(width, height)
    cellVisitedStack = [cells[0][0]]
    while len(cellVisitedStack) != 0:
        currentCell = cellVisitedStack[-1]
        if currentCell.index != (len(cells)-1, len(cells[0])-1):
            relativeIndex = currentCell.createOutLink(cells)
        else:
            currentCell.visited = True
            relativeIndex = None
        if relativeIndex is None:
            cellVisitedStack.pop()
        else:
            absIndex = (currentCell.index[0] + relativeIndex[0], currentCell.index[1] + relativeIndex[1])
            cellVisitedStack.append(cells[absIndex[0]][absIndex[1]])
    return cells


def newIndex(oldIndex):
    return oldIndex * 2 + 1


def createListMaze(cells):
    maze = [["#" for j in range((len(cells[0])) * 2 + 1)] for i in range((len(cells)) * 2 + 1)]
    for _ in cells:
        for cell in _:
            maze[newIndex(cell.index[0])][newIndex(cell.index[1])] = " "
            for link in cell.relativeOutLinks:
                maze[newIndex(cell.index[0]) + link[0]][newIndex(cell.index[1]) + link[1]] = " "
    maze[-2][-2] = "E"
    return maze

def getLevelNum(maxCheck = len(os.listdir()))
