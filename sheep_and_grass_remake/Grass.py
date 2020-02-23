from Settings import *
from Statistics import *

class Grass:

    def __init__(self, x, y):
        # Grass has an x and y position
        self.x = x
        self.y = y
        # Generate itself
        self.gen()
    
    def update(self):
        # Draw the grass as a rectangle with a color to show its state
        if self.eaten:
            fill(BROWN)
        else:
            fill(GREEN)
        noStroke()
        rect(self.x*grassSize, self.y*grassSize, grassSize, grassSize)
        
        # Randomly regenerate the grass
        if(random(0,1) < regenRate):
            self.gen()
        
        if self.eaten:
            return 0
        else:
            return 1
        
    def die(self):
        self.eaten = True
    
    def gen(self):
        # To generate, give the grass 10 energy and make it not eaten
        self.energy = 10.0
        self.eaten = False
        
def makeGrass():
    count = 0
    for g in range(SIZE/grassSize):
        row = []
        for g2 in range(SIZE/grassSize):
            row.append(Grass(g,g2))
            count += 1
        grassGrid.append(row)
    return count

def updateGrass(grid):
    available = 0
    for row in grassGrid:
        for grassOb in row:
            available += grassOb.update()
    return available
