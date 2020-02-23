from Settings import *

class Stats:
    # Empty object to hold variables
    pass

def drawStats():
    # Draw the rectangle at the bottom
    fill(40)
    noStroke()
    rect(0, SIZE, SIZE, dataPanelHeight)
    # Write the day number and the grass availability
    fill(230)
    text("Day number "+str(frameCount),textLeftMargin, SIZE+textTopMargin)
    text("Available grass "+str(round(Stats.grassPercentAvail,2))+" %", textLeftMargin, SIZE+textTopMargin+20)
    for index, co in enumerate(sheepCount.keys()):
        # Show populations of each species in the list
        fill(230)
        text(co, textLeftMargin, SIZE+textTopMargin+40+20*index)
        text(sheepCount[co], textLeftMargin+100, SIZE+textTopMargin+40+20*index)
        if frameCount%logUpdateRate==0:
            # Add the populations to the sheepCountLog
            sheepCountLog[co].append(sheepCount[co])
    
    
    drawGraph()
    
            
def drawGraph():
    # Calculate the highest value that must be shown on the population graph
    Stats.maxSheepPop = calculateMaxPop()
    
    # Mark "height" of top line
    fill(230)
    text(Stats.maxSheepPop, graphLeftPos - 30, SIZE+graphTopPos+5)
    text("0", graphLeftPos - 10, SIZE+graphTopPos+graphHeight+5)
    # Draw graph lines
    stroke(230)
    strokeWeight(2)
    line(graphLeftPos, SIZE+graphTopPos+graphHeight, graphLeftPos+graphWidth, SIZE+graphTopPos+graphHeight) # Bottom line
    line(graphLeftPos, SIZE+graphTopPos, graphLeftPos+graphWidth, SIZE+graphTopPos)   # Top line
    stroke(200)
    strokeWeight(1)
    #line(graphLeftPos, SIZE+graphTopPos+graphHeight/2, graphLeftPos+graphWidth, SIZE+graphTopPos+graphHeight/2) # Middle line
    
    # Draw grass population points
    for i,val in enumerate(grassGraph[-graphWidth:]):
        stroke(GREEN)
        strokeWeight(2)
        #point(graphLeftPos+i, SIZE+graphTopPos+graphHeight-val/max(grassGraph[-graphWidth:])*graphHeight)
        divisor = 100
        if scaleGrassDisplay:
            divisor = max(grassGraph[-graphWidth:])
        if i > 0:
            line(graphLeftPos+i, SIZE+graphTopPos+graphHeight-val/divisor*graphHeight,
                 graphLeftPos+i-1, SIZE+graphTopPos+graphHeight-lastVal/divisor*graphHeight)
        lastVal = val
            
    for col in sheepCountLog.keys():
        stroke(sheepColors[col])
        for i, val in enumerate(sheepCountLog[col][-graphWidth:]):
            strokeWeight(2)
            if lastVal > 0 and i > 0:
                line(graphLeftPos+i, SIZE+graphTopPos+graphHeight-1.0*val/Stats.maxSheepPop*graphHeight,
                     graphLeftPos+i-1, SIZE+graphTopPos+graphHeight-1.0*lastVal/Stats.maxSheepPop*graphHeight)
            lastVal = val
        fill(sheepColors[col])
        try:
            if lastVal > 0:
                text(lastVal, graphLeftPos+graphWidth+4, SIZE+graphTopPos+graphHeight-1.0*lastVal/Stats.maxSheepPop*graphHeight+3)
        except:
            pass
            
def calculateMaxPop():
    count = minimumGraphScale
    for pops in sheepCountLog.values():
        if len(pops)>0:
            maxi = max(pops[-graphWidth:])
            if maxi > count:
                count = maxi    
            if count == 0:
                count = 1
    return count

# DO NOT CHANGE
sheepCount = {}
sheepCountLog = {} # Dictionary full of arrays for the number of sheep in each family over every day
grassGrid = [] # Array of the grass objects
grassGraph = [] # Population of grass on each day
sheeps = []
