from Settings import *
from Statistics import *

class Sheep:
    def __init__(self, x, y, moveSpeed, col):
        self.x = x
        self.y = y
        self.col = col
        self.moveSpeed = moveSpeed
        # Initialize a sheep with 20 energy
        self.energy = sheepInitialEnergy
        
        if self.col not in sheepCount:
            # If the sheep is the first one of its family, add a key to the sheep dictionary
            sheepCount[self.col] = 1
            sheepCountLog[self.col] = []
        else:
            # If the sheep is not the first of its family, increment the counter for its sheep
            sheepCount[self.col] += 1
    
    def update(self):
        # Move the sheep a random distance vertically and horizontally
        self.x+=random(-self.moveSpeed, self.moveSpeed)*grassSize
        self.y+=random(-self.moveSpeed, self.moveSpeed)*grassSize
        
        # Ensure that the sheep is on the screen by qrapping the edges
        self.x = self.x%SIZE
        self.y = self.y%SIZE
        self.checkGrass()
        
        # Decrease the sheep's energy in proportion to its speed
        self.energy -= (1.0*self.moveSpeed*grassSize)**hungerExponent/(grassSize**hungerExponent)
        
        # Draw the sheep
        stroke(0)
        strokeWeight(1)
        fill(sheepColors[self.col])
        ellipse(self.x, self.y, grassSize, grassSize)
        
        if self.energy <= 0:
            # If the sheep's energy is below 0, it dies
            self.die()
        if self.energy >= reproductionEnergy:
            # The sheep reproduces when it has enough energy
            self.birth()
    
    def birth(self):
        # Create a new sheep at the same location
        sheeps.append(Sheep(self.x, self.y, self.moveSpeed, self.col))
        # Decrease the parent's energy
        self.energy -= reproductionCost

    def checkGrass(self):
        posX = int(self.x / grassSize)
        posY = int(self.y / grassSize)
        
        if grassGrid[posX][posY].eaten == False:
            self.energy += grassGrid[posX][posY].energy
            grassGrid[posX][posY].die()
    
    def die(self):
        sheepCount[self.col] -= 1
        sheeps.remove(self)
        
def updateSheep():
    for s in sheeps:
        s.update() # Update all of the sheep
