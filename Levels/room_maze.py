import random


class Cell:
    """
    an individual square in the maze
    """
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

    def __str__(self):
        return str(self.index)

    def __repr__(self):
        return str(self.index)

    def createOutLink(self, cells):
        self.visited = True
        try:
            relativeOutLink = random.choice(self.getUnvisitedNeighbours(cells))
            self.relativeOutLinks.append(relativeOutLink)
        except IndexError:
            relativeOutLink = None
        return relativeOutLink



class Room:
    """
    a group of cells representing a room in the maze
    """
    def __init__(self, topLeft, bottomRight, maze):
        self.topLeft = topLeft
        self.bottomRight = bottomRight
        self.cells = [row[topLeft[0]: bottomRight[0]+1]
                      for row in maze.cells[topLeft[1]: bottomRight[1]+1]]
        self.edgeCells = self.cells[0] + self.cells[-1]+[row[i] for row in self.cells[1:-1] for i in (0,-1)]
        self.setVisitedCells()
        self.doorwayCells = self.setDoorwayCells()

    def setVisitedCells(self):
        for row in self.cells:
            for cell in row:
                cell.visited = True

    def setDoorwayCells(self, doorwayNumber=None):
        doorwayCells = random.choices(self.edgeCells, k=doorwayNumber if doorwayNumber else random.randint(1, 4))
        for cell in doorwayCells:
            cell.visited = False
        return doorwayCells

    def intersects(self, room):
        return room.topLeft[0] <= self.bottomRight[0] and \
               room.topLeft[1] <= self.bottomRight[1] and \
               room.bottomRight[0] >= self.topLeft[0] and \
               room.bottomRight[1] >= self.topLeft[1]

    def __str__(self):
        return str(self.topLeft)

    def __repr__(self):
        return str(self.topLeft)


class Maze:

    def __init__(self, width, height):
        self.cells = [[Cell((i, j)) for j in range(width)] for i in range(height)]
        self.rooms = []
        self.width = width
        self.height = height

    def createRooms(self, attempts, maxWidth=5, maxHeight=5):
        for _ in range(attempts):
            width = random.randint(2, maxWidth)
            height = random.randint(2, maxHeight)
            topLeft = (random.randint(0, self.height-height), random.randint(0, self.width-width))
            newRoom = Room(topLeft, (topLeft[0]+height, topLeft[1]+width), self)
            for room in self.rooms:
                if newRoom.intersects(room):
                    break

            else:
                self.rooms.append(newRoom)

    def createPaths(self):
        unvisitedCells = [cell for row in self.cells for cell in row if not cell.visited]
        while unvisitedCells:
            print(unvisitedCells)
            self._createPath(unvisitedCells[0])
            unvisitedCells = [cell for cell in unvisitedCells if not cell.visited]

    def _createPath(self, cell):
        link = cell.createOutLink(self.cells)
        while link:
            newCell = self.cells[cell.index[0] + link[0]][cell.index[1] + link[1]]
            self._createPath(newCell)
            link = cell.createOutLink(self.cells)

    def __str__(self):
        newi = lambda x: x*2+1
        maze = [["#" for _ in range(self.width*2+1)] for __ in range(self.height*2+1)]

        for row in self.cells:
            for cell in row:
                maze[newi(cell.index[0])][newi(cell.index[1])] = " "
                for link in cell.relativeOutLinks:
                    maze[newi(cell.index[0])+link[0]][newi(cell.index[1])+link[1]] = " "
        for room in self.rooms:
            for i in range(newi(room.topLeft[0]), newi(room.bottomRight[0])+1):
                for j in range(newi(room.topLeft[1]), newi(room.bottomRight[1])+1):
                    maze[i][j] = " "

        return str(maze).replace("],", "],\n")


test = Maze(15, 15)
test.createRooms(10)
test.createPaths()
print(test)
