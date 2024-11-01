from heapq import heapify, heappush, heappop 
# Positions where each number should be in during the goal state
cPos0 = [2,2]
cPos1 = [0,0]
cPos2 = [0,1]
cPos3 = [0,2]
cPos4 = [1,0]
cPos5 = [1,1]
cPos6 = [1,2]
cPos7 = [2,0]
cPos8 = [2,1]

class EightPuzzle:
    def __init__(self, initial_state):
        self.state = initial_state      
        # traverse via state[row][col]
        #   [0][0]  [0][1]  [0][2]
        #   [1][0]  [1][1]  [1][2]
        #   [2][0]  [2][1]  [2][2]
        
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def findBlank(self):
        # Find the coordinates of the blank (represented by 0)
        row = -1
        col = -1
        for r, enumRow in enumerate(self.state):
            for c, elem in enumerate(enumRow):
                if elem == 0:
                    row = r
                    col = c
                    break
            if(row != -1):  # row, col of 0 identified
                break
        
        if(row == -1 or col == -1): 
            print("Blank not included in state")
        return (row, col)

    def is_goal(self):
        return self.state == self.goal_state

    def can_swipe_left(self):
        # Find the coordinates of the blank at current state (represented by 0)
        blankCoord = self.findBlank()
        row = blankCoord[0]
        col = blankCoord[1]
        if (col <= 0):
                return False
        return True
    
    def can_swipe_right(self):
        # Find the coordinates of the blank at current state (represented by 0)
        blankCoord = self.findBlank()
        row = blankCoord[0]
        col = blankCoord[1]
        if (col >= len(self.state[0]) - 1): 
                return False
        return True
    
    def can_swipe_up(self):
        # Find the coordinates of the blank at current state (represented by 0)
        blankCoord = self.findBlank()
        row = blankCoord[0]
        col = blankCoord[1]
        if (row <= 0):
                return False
        return True
    
    def can_swipe_down(self):
        # Find the coordinates of the blank at current state (represented by 0)
        blankCoord = self.findBlank()
        row = blankCoord[0]
        col = blankCoord[1]
        if (row >= len(self.state) - 1):
                return False
        return True

    # simulate finger sliding in specified direction
    def swipe(self, direction):
        # Find the coordinates of the blank (represented by 0)
        blankCoord = self.findBlank()
        row = blankCoord[0]
        col = blankCoord[1]
                
        if direction == "left":
            if (self.can_swipe_left() == False):
                print("swipe left is not possible.")
            if (col > 0 and col <= 2):
                self.state[row][col], self.state[row][col - 1] = self.state[row][col - 1], self.state[row][col]
                col -= 1
            
        elif direction == "right":
            if (self.can_swipe_right() == False): 
                print("swipe right is not possible.")
            elif (col < len(self.state[0]) - 1):
                self.state[row][col], self.state[row][col + 1] = self.state[row][col + 1], self.state[row][col]
                col += 1

        elif direction == "up":
            if (self.can_swipe_up() == False):
                print("swipe up is not possible.")
            elif (row > 0):
                self.state[row][col], self.state[row - 1][col] = self.state[row - 1][col], self.state[row][col]
                row -= 1
                
        elif direction == "down":
            if (self.can_swipe_down() == False):
                print("swipe down is not possible.")
            elif (row < len(self.state) - 1):
                self.state[row][col], self.state[row + 1][col] = self.state[row + 1][col], self.state[row][col]
                row += 1
                            
        else:
            print("Invalid direction.")

    def display(self):
        for row in self.state:
            print(row)
        print("Is goal:", self.is_goal())
    
    def createChildren(self):
        children = []
        if (self.can_swipe_right()):
            newState = [list(row) for row in self.state]
            newPuzzle = EightPuzzle(newState)
            newPuzzle.swipe("right")
            children.append(newPuzzle)
        if (self.can_swipe_left()):
            newState = [list(row) for row in self.state]
            newPuzzle = EightPuzzle(newState)
            newPuzzle.swipe("left")
            children.append(newPuzzle)
        if (self.can_swipe_down()):
            newState = [list(row) for row in self.state]
            newPuzzle = EightPuzzle(newState)
            newPuzzle.swipe("down")
            children.append(newPuzzle)
        if (self.can_swipe_up()):
            newState = [list(row) for row in self.state]
            newPuzzle = EightPuzzle(newState)
            newPuzzle.swipe("up")
            children.append(newPuzzle)
        return children

class Node:
    def __init__(self, puzzle: EightPuzzle, parent = None, g=0, h=0):
        self.puzzle = puzzle  
        self.state = puzzle.state
        self.g = g           
        self.h = h            
        self.f = g + h
        self.parent = parent

    def is_root(self):
        return self.parent is None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.state == other.state
    
    def __ne__(self, other):
        return self.state != other.state
    
    def get_parent(self):
        # if(self.parent == None):
        #     return -1
        return self.parent
    
    def get_g(self):
        return self.g
    
# Search Functions

def uniformCostSearch(puzzle):
    heap = []
    g = 0
    h = 0
    
    numExpandedNodes = 0
    maxNodesInQueue = 0
    goalNodeDepth = -1
    heappush(heap, Node(puzzle, None, g=g, h=h))
    visitedNodes = set()
    firstExpansion = True
    while heap:
        if(len(heap) > maxNodesInQueue): maxNodesInQueue = len(heap)        # stat count var
        currNode = heappop(heap)
        print("parent: " + str(currNode.get_parent()))
        if firstExpansion:
            print("Expanding state")
            currNode.puzzle.display()
            print("\n")
            firstExpansion = False
            numExpandedNodes += 1       # stat count var
        else:
            print(f"The best state to expand with g(n) = {currNode.g:.2f} and h(n) = {currNode.h:.2f} is:")
            currNode.puzzle.display()
            print("Expanding this node...\n")
            numExpandedNodes += 1       # stat count var
        if currNode.puzzle.is_goal():
            print("Goal state found")
            goalNodeDepth = currNode.g
            print("To solve this problem the search algorithm expanded a total of " + str(numExpandedNodes) + " nodes.")
            print("The maximum number of nodes in the queue at any one time: " + str(maxNodesInQueue) + ".")
            print("The depth of the goal node was " + str(goalNodeDepth) + ".")
            return currNode
        visitedNodes.add(tuple(map(tuple, currNode.state)))
        children = currNode.puzzle.createChildren()
        foundChildren = []
        for child in children:
            childStateTuple = tuple(map(tuple, child.state))
            if childStateTuple in visitedNodes:
                # print("Already visited this node: ")
                # child.display()
                # print("\n")
                pass
            else:
                g = currNode.g + 1
                h = 0
                heappush(heap, Node(child, currNode,g=g, h=h))
                foundChildren.append(child)
        # functionality to print the children nodes that we found
        # if foundChildren:
        #     print("Found children:")
        #     for i, child in enumerate(foundChildren):
        #         print(f"Child {i + 1}:")
        #         child.display()
        #         print("\n")

    return False 
    

def aStarTile(state):
    pass

def aStarEuclidean(puzzle):
    heap = []
    g = 0
    h = calcHn(puzzle.state)
    heappush(heap, Node(puzzle,g=g, h=h))
    visitedNodes = set()
    firstExpansion = True
    while heap:
        currNode = heappop(heap)
        if firstExpansion:
            print("Expanding state")
            currNode.puzzle.display()
            print("\n")
            firstExpansion = False
        else:
            print(f"The best state to expand with g(n) = {currNode.g:.2f} and h(n) = {currNode.h:.2f} is:")
            currNode.puzzle.display()
            print("Expanding this node...\n")
        if currNode.puzzle.is_goal():
            print("Goal state found")
            return currNode
        visitedNodes.add(tuple(map(tuple, currNode.state)))
        children = currNode.puzzle.createChildren()
        foundChildren = []
        for child in children:
            childStateTuple = tuple(map(tuple, child.state))
            if childStateTuple in visitedNodes:
                # print("Already visited this node: ")
                # child.display()
                # print("\n")
                pass
            else:
                g = currNode.g + 1
                h = calcHn(child.state)
                heappush(heap, Node(child, g=g, h=h))
                foundChildren.append(child)
        # functionality to print the children nodes that we found
        # if foundChildren:
        #     print("Found children:")
        #     for i, child in enumerate(foundChildren):
        #         print(f"Child {i + 1}:")
        #         child.display()
        #         print("\n")
    return False 
def calcHn(state):
    h = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            tile = state[i][j]
            currentPos = (i, j)
            match(tile):
                case 1:
                    h += eDistance(currentPos, cPos1)
                case 2:
                    h += eDistance(currentPos, cPos2)
                case 3:
                    h += eDistance(currentPos, cPos3)
                case 4:
                    h += eDistance(currentPos, cPos4)
                case 5:
                    h += eDistance(currentPos, cPos5)
                case 6:
                    h += eDistance(currentPos, cPos6)
                case 7:
                    h += eDistance(currentPos, cPos7)
                case 8:
                    h += eDistance(currentPos, cPos8)
    return h

def eDistance(p1,p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def printPath(solution):
    path = []
    n = solution
    i = solution.get_g() + 1    # length = depth + root
    while i > 0:
        path.insert(0, n)
        n = n.get_parent()
        i -= 1
    
    print("\nFinal solution path:")
    for elem in path:
        elem.puzzle.display()



if __name__ == "__main__":
    print("Welcome to XXX (change this to your student ID) 8 puzzle solver. Type “1” to use a default puzzle, or “2” to enter your own puzzle.")
    inp = input("")
    validated_int = int(inp[0])     # expect 1 or 2
    
    if(validated_int == 1):     # default puzzle
        # print("Initial State")
        initial_state = [[1, 2, 3], [0, 5, 6], [4, 7, 8]]   # arbitrary initial state
        puzzle = EightPuzzle(initial_state)
        # puzzle.display()
        # print("\n")
        
        # solution = aStarEuclidean(puzzle)
        # test swipe function. remove lines 133-159 after completing search functions
        # print("can swipe up? " + str(puzzle.can_swipe_up())) 
        # print("swipe up. expect to not be able to swipe up")
        # puzzle.swipe("up")
        # puzzle.display()

        
        # print("swipe right")
        # puzzle.swipe("right")
        # puzzle.display()
        
        # print("swipe down")
        # puzzle.swipe("down")
        # puzzle.display()
        
        # print("swipe up")
        # puzzle.swipe("up")
        # puzzle.display()
        
        # print("swipe left. expect to be goal state")
        # puzzle.swipe("left")
        # puzzle.display()  
        
        # test can_swipe_DIRECTION functions
        # print("can swipe right? " + str(puzzle.can_swipe_right()))
        # print("can swipe left? " + str(puzzle.can_swipe_left()))
        # print("can swipe down? " + str(puzzle.can_swipe_down()))
        # print("can swipe up? " + str(puzzle.can_swipe_up())) 
        
        # print("swipe up")
        # puzzle.swipe("up")
        # puzzle.display()
        
        # test can_swipe_DIRECTION functions
        # print("can swipe right? " + str(puzzle.can_swipe_right()))
        # print("can swipe left? " + str(puzzle.can_swipe_left()))
        # print("can swipe down? " + str(puzzle.can_swipe_down()))
        # print("can swipe up? " + str(puzzle.can_swipe_up()))
        
        # Uniform Cost Solution
        solution = uniformCostSearch(puzzle)
        # Print path
        printPath(solution)
            
            
        
        # A* with the Misplaced Tile heuristic.
        
        
        
        # A* with the Euclidean Distance heuristic
        
    elif(validated_int == 2):   # self-designed puzzle
        print("Enter your puzzle, use a zero to represent the blank")
        row0inp = input("Enter the first row, use space or tabs between numbers: ")
        row1inp = input("Enter the second row, use space or tabs between numbers: ")
        row2inp = input("Enter the third row, use space or tabs between numbers: ")
        
        row0 = row0inp.split(' ')
        row1 = row1inp.split(' ')
        row2 = row2inp.split(' ')
        
        row0 = [int(x) for x in row0]
        row1 = [int(x) for x in row1]
        row2 = [int(x) for x in row2]
        
        # print("Initial State")
        initial_state = [row0, row1, row2]   # arbitrary initial state
        puzzle = EightPuzzle(initial_state)
        # puzzle.display()
        # print("\n")
        
        print("Enter your choice of algorithm")
        print("1. Uniform Cost Search")
        print("2. A* with the Misplaced Tile heuristic.")
        print("3. A* with the Euclidean distance heuristic")
        choice = int(input("")[0])
        
        if(choice == 1): # Uniform Cost Solution
            solution = uniformCostSearch(puzzle)
        elif(choice == 2): # A* with the Misplaced Tile heuristic.
            pass
        elif(choice == 3): # A* with the Euclidean Distance heuristic
            solution = aStarEuclidean(puzzle)
        
    
