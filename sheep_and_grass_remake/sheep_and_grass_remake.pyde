# Sheep Simulator
# 
#
#
# Blake Freer
# February 2020

from Grass import *
from Sheep import *
from Statistics import *
from Settings import *

def setup():
    frameRate(frame_rate)
    size(SIZE,SIZE+dataPanelHeight)
    Stats.numGrass = makeGrass()


# White family is the general
sheeps.append(Sheep(SIZE/4,SIZE/4,1.0, "WHITE"))
# Red is slow
sheeps.append(Sheep(SIZE/4,SIZE/4*3,0.9,"RED"))
# Purple is fast
sheeps.append(Sheep(SIZE/4*3,SIZE/4,1.1,"PURPLE"))
# Blue is very fast
sheeps.append(Sheep(SIZE/4*3,SIZE/4*3,1.3,"BLUE"))






def draw():
    Stats.grassPercentAvail = updateGrass(grassGrid)*100.0/Stats.numGrass

    updateSheep()
        
    # Show grass population graph
    if frameCount%logUpdateRate==0 :
        grassGraph.append(Stats.grassPercentAvail)
            
                
    drawStats()
    
