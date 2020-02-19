#Sheep simulator

sheepColors = {"WHITE":color(255),
               "BLUE":color(100, 100, 200),
               "RED":color(230, 70, 50),
               "PURPLE":color(200, 70, 180)}

GREEN = color(0, 150, 0)
BROWN = color(100, 100, 10)

_size = 600

def setup():
    frameRate(200)
    size(_size,_size+200)

# GRASS VARIABLES
grassSize = 10
grassAvail = 0
regenRate = 0.0035 #0.0035

# SHEEP VARIABLES
reproductionEnergy = 50
reproductionCost = 30
hungerExponent = 1.3

class Grass:
    global regenRate
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gen()
    
    def update(self):
        if self.eaten:
            fill(BROWN)
        else:
            fill(GREEN)
        noStroke()
        rect(self.x*grassSize, self.y*grassSize, grassSize, grassSize)
        if(random(0,1) < regenRate):
            self.gen()
        if self.eaten:
            return 0
        else:
            return 1
        
    def die(self):
        self.eaten = True
    
    def gen(self):
        self.energy = 10.0
        self.eaten = False
        
        
sheeps = []
sheepCount = {}
grassGrid = []


class Sheep:
    def __init__(self, x, y, moveSpeed, col):
        global sheepCount
        self.x = x
        self.y = y
        self.col = col
        self.moveSpeed = moveSpeed
        self.energy = 20
        if self.col not in sheepCount:
            sheepCount[self.col] = 1
        else:
            sheepCount[self.col] += 1
    
    def update(self):
        global sheepColors, reproductionEnergy, reproductionCost, hungerExponent
        
        self.x+=random(-self.moveSpeed, self.moveSpeed)
        self.y+=random(-self.moveSpeed, self.moveSpeed)
        self.x = self.x%_size
        self.y = self.y%_size
        self.checkGrass()
        self.energy -= (1.0*self.moveSpeed)**hungerExponent/(10.0**hungerExponent)
        #stroke(0)
        noStroke()
        fill(sheepColors[self.col])
        ellipse(self.x, self.y, grassSize, grassSize)
        
        if self.energy <= 0:
            self.die()
        if self.energy >= reproductionEnergy:
            self.birth()
    
    def birth(self):
        global sheeps, reproductionCost
        sheeps.append(Sheep(self.x, self.y, self.moveSpeed, self.col))
        self.energy -= reproductionCost

    def checkGrass(self):
        posX = int(self.x / grassSize)
        posY = int(self.y / grassSize)
        
        if grassGrid[posX][posY].eaten == False:
            self.energy += grassGrid[posX][posY].energy
            grassGrid[posX][posY].die()
    
    def die(self):
        global sheepCount
        sheepCount[self.col] -= 1
        sheeps.remove(self)

# White family is the general
sheeps.append(Sheep(_size/4,_size/4,10, "WHITE"))
# Red is slow
sheeps.append(Sheep(_size/4,_size/4*3,9,"RED"))
# Purple is fast
sheeps.append(Sheep(_size/4*3,_size/4,11,"PURPLE"))
# Blue is very fast
sheeps.append(Sheep(_size/4*3,_size/4*3,13,"BLUE"))

for g in range(_size/grassSize):
    row = []
    for g2 in range(_size/grassSize):
        row.append(Grass(g,g2))
    grassGrid.append(row)
    

numGrass = len(grassGrid)*len(grassGrid[0])


def draw():
    if len(sheeps)==0:
        noLoop()
        
    global sheepCount
    
    grassAvail = 0
    
    for gc in grassGrid:
        for g in gc:
            grassAvail += g.update()
    for s in sheeps:
        s.update()
    
    
    fill(255)
    noStroke()
    rect(0, _size, _size, 200)
    
    fill(20)
    text("Day number "+str(frameCount), 50, _size+20)
    text("Available grass "+str(round(100.0*grassAvail/numGrass,2))+" %", 50, _size+40)
    
    for index, co in enumerate(sheepCount.keys()):
        fill(20)
        text(co, 50, _size+60+20*index)
        text(sheepCount[co], 150, _size+60+20*index)
    
