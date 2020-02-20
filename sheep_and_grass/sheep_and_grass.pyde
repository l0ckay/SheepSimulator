#Sheep simulator

sheepColors = {"WHITE":color(255),
               "BLUE":color(100, 100, 200),
               "RED":color(230, 70, 50),
               "PURPLE":color(200, 70, 180)}

GREEN = color(0, 150, 0)
BROWN = color(100, 100, 10)


# GRASS VARIABLES
grassSize = 15
grassAvail = 0
regenRate = 0.0035 #0.0035
scaleGraphDisplay = False # does the grass line on the time graph adjust its height?

# SHEEP VARIABLES
reproductionEnergy = 50
reproductionCost = 30
hungerExponent = 1.3

# DISPLAY VARIABLES
_size = 600
dataPanelHeight = 250
logUpdateRate = 1 # How often is the log at the bottom of the screen updated?
textLeftMargin = 20
textTopMargin = 70

graphWidth = 380
graphHeight = 200
graphLeftPos = 180
graphTopPos = 20

def setup():
    frameRate(200)
    size(_size,_size+dataPanelHeight)

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
sheepCountLog = {}
grassGrid = []

grassGraph = []

class Sheep:
    def __init__(self, x, y, moveSpeed, col):
        global sheepCount, sheepCountLog
        self.x = x
        self.y = y
        self.col = col
        self.moveSpeed = moveSpeed
        self.energy = 20
        if self.col not in sheepCount:
            sheepCount[self.col] = 1
            sheepCountLog[self.col] = []
        else:
            sheepCount[self.col] += 1
    
    def update(self):
        global sheepColors, reproductionEnergy, reproductionCost, hungerExponent, grassSize
        
        self.x+=random(-self.moveSpeed, self.moveSpeed)*grassSize
        self.y+=random(-self.moveSpeed, self.moveSpeed)*grassSize
        self.x = self.x%_size
        self.y = self.y%_size
        self.checkGrass()
        self.energy -= (1.0*self.moveSpeed*grassSize)**hungerExponent/(grassSize**hungerExponent)
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
sheeps.append(Sheep(_size/4,_size/4,1.0, "WHITE"))
# Red is slow
sheeps.append(Sheep(_size/4,_size/4*3,0.9,"RED"))
# Purple is fast
sheeps.append(Sheep(_size/4*3,_size/4,1.1,"PURPLE"))
# Blue is very fast
sheeps.append(Sheep(_size/4*3,_size/4*3,1.3,"BLUE"))

for g in range(_size/grassSize):
    row = []
    for g2 in range(_size/grassSize):
        row.append(Grass(g,g2))
    grassGrid.append(row)
    

numGrass = len(grassGrid)*len(grassGrid[0])

maxSheepPop = 0

def draw():
    global maxSheepPop
    if len(sheeps)==0:
        pass
        #noLoop()
        
    global sheepCount
    
    grassAvail = 0
    
    for gc in grassGrid:
        for g in gc:
            grassAvail += g.update()
            
    grassPercentAvail = grassAvail*100.0/numGrass
            
    for s in sheeps:
        s.update()
    
    fill(40)
    noStroke()
    rect(0, _size, _size, dataPanelHeight)
    
    fill(230)
    text("Day number "+str(frameCount),textLeftMargin, _size+textTopMargin)
    text("Available grass "+str(round(grassPercentAvail,2))+" %", textLeftMargin, _size+textTopMargin+20)
    for index, co in enumerate(sheepCount.keys()):
        # Show populations of each species in the list
        fill(230)
        text(co, textLeftMargin, _size+textTopMargin+40+20*index)
        text(sheepCount[co], textLeftMargin+100, _size+textTopMargin+40+20*index)
        if frameCount%logUpdateRate==0:
            # Add the populations to the sheepCountLog
            sheepCountLog[co].append(sheepCount[co])
        
    # Show grass population graph
    if frameCount%logUpdateRate==0 :
        grassGraph.append(grassPercentAvail)
        
        
    maxSheepPop = 0
    for pops in sheepCountLog.values():
        if len(pops)>0:
            maxi = max(pops[-graphWidth:])
            if maxi > maxSheepPop:
                maxSheepPop = maxi    
            if maxSheepPop == 0:
                maxSheepPop = 1
                
    # Mark "height" of top line
    fill(230)
    text(maxSheepPop, graphLeftPos - 30, _size+graphTopPos+5)
    text("0", graphLeftPos - 10, _size+graphTopPos+graphHeight+5)
    # Draw graph lines
    stroke(230)
    strokeWeight(2)
    line(graphLeftPos, _size+graphTopPos+graphHeight, graphLeftPos+graphWidth, _size+graphTopPos+graphHeight) # Bottom line
    line(graphLeftPos, _size+graphTopPos, graphLeftPos+graphWidth, _size+graphTopPos)   # Top line
    stroke(200)
    strokeWeight(1)
    #line(graphLeftPos, _size+graphTopPos+graphHeight/2, graphLeftPos+graphWidth, _size+graphTopPos+graphHeight/2) # Middle line
    
    # Draw grass population points
    for i,val in enumerate(grassGraph[-graphWidth:]):
        stroke(GREEN)
        strokeWeight(2)
        #point(graphLeftPos+i, _size+graphTopPos+graphHeight-val/max(grassGraph[-graphWidth:])*graphHeight)
        divisor = 100
        if scaleGraphDisplay:
            divisor = max(grassGraph[-graphWidth:])
        if i > 0:
            line(graphLeftPos+i, _size+graphTopPos+graphHeight-val/divisor*graphHeight,
                 graphLeftPos+i-1, _size+graphTopPos+graphHeight-lastVal/divisor*graphHeight)
        lastVal = val
        
    
            
    for col in sheepCountLog.keys():
        stroke(sheepColors[col])
        for i, val in enumerate(sheepCountLog[col][-graphWidth:]):
            strokeWeight(2)
            if lastVal > 0 and i > 0:
                line(graphLeftPos+i, _size+graphTopPos+graphHeight-1.0*val/maxSheepPop*graphHeight,
                     graphLeftPos+i-1, _size+graphTopPos+graphHeight-1.0*lastVal/maxSheepPop*graphHeight)
            lastVal = val
        fill(sheepColors[col])
        try:
            if lastVal > 0:
                text(lastVal, graphLeftPos+graphWidth+4, _size+graphTopPos+graphHeight-1.0*lastVal/maxSheepPop*graphHeight+3)
        except:
            pass
