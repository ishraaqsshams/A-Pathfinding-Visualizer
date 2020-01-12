# AStar
import copy

board = [
    [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)], 
    [(255, 255, 255), (0, 0, 0), (255, 255, 255), (0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255)], 
    [(0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (255, 255, 255), (0, 0, 0), (255, 255, 255), (0, 0, 0), (255, 255, 255), (0, 0, 0), (255, 255, 255)], 
    [(0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)], 
    [(0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255)], 
    [(255, 255, 255), (0, 0, 0), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255)], 
    [(255, 255, 255), (0, 0, 0), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (255, 255, 255), (0, 0, 0)], 
    [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (255, 255, 255), (0, 0, 0), (255, 255, 255), (0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0)], 
    [(0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255), (0, 0, 0)], 
    [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

STARTNODE = (2, 4)
ENDNODE = (8, 1)

class Node(object):
    def __init__(self, path, g, endNode):
        self.path = path
        self.location = self.path[-1]
        self.row = self.location[0]
        self.col = self.location[1] 
        self.endNode = endNode
        self.g = g
        self.h = self.getHValue()
        self.f = self.g + self.h
    
    def getHValue(self):
        rDist = abs(self.row - self.endNode[0])
        cDist = abs(self.col - self.endNode[1])
        return rDist + cDist

    def getLegalMoves(self, board, openList, closedList):
        moveList = []
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if (r, c) == (0, 0):
                    continue
                moveList.append((r, c))
        returnList = []     # returns a list of nodes
        for move in moveList:
            seen = False
            path = copy.copy(self.path)
            g = self.g
            newR = self.row + move[0]
            newC = self.col + move[1]
            if (0 <= newR <= len(board) - 1) and (0 <= newC <= len(board[0]) - 1):
                if board[newR][newC] != BLACK:
                    for node in openList + closedList:
                        if node.row == newR and node.col == newC:
                            seen = True
                    if not seen:
                        if (newR, newC) not in self.path:
                            if 0 in move:
                                g += 1
                                path.append((newR, newC))
                                returnList.append(Node(path, g, self.endNode))
        return returnList

def aStar(board, start, end):
    startR, startC = start[0], start[1]
    startNode = Node([(startR, startC)], 0, end)
    openList = [startNode]
    closedList = []
    while len(openList) > 0:
        fValues = []
        for node in openList:
            if end in node.path:
                return (node.path, openList, closedList)
            fValues.append(node.f)
        minF = min(fValues)
        for node in openList:
            if node.f == minF:
                currentNode = node
                break
        openList.remove(currentNode)
        closedList.append(currentNode)
        openList += currentNode.getLegalMoves(board, openList, closedList)
    return (None, openList, closedList)

def getNextStep(board, start, end, openList, closedList):
    if len(openList) > 0:
        for node in openList:
            if end in node.path:
                return (node.path, openList, closedList)
        fValues = []
        for node in openList:
            fValues.append(node.f)
        minF = min(fValues)
        for node in openList:
            if node.f == minF:
                currentNode = node
                break
        openList.remove(currentNode)
        closedList.append(currentNode)
        openList += currentNode.getLegalMoves(board, openList, closedList)
        return (None, openList, closedList)

    