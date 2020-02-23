# Grass Settings
grassSize = 10
regenRate = 0.0035 #0.0035


# Sheep Settings
sheepInitialEnergy = 20 # 20
reproductionEnergy = 50 # 50
reproductionCost = 30   # 30
hungerExponent = 1.3

# Colors
sheepColors = {"WHITE":color(255),
               "BLUE":color(100, 100, 200),
               "RED":color(230, 70, 50),
               "PURPLE":color(200, 70, 180)}
GREEN = color(0, 150, 0)
BROWN = color(100, 100, 10)

# Display Settings
frame_rate = 100
SIZE = 600 # Length and width of the sheep area
dataPanelHeight = 250 # Height of the data pane at the bottom
textLeftMargin = 20
textTopMargin = 70

# Population - Time graph settings
graphWidth = 380
graphHeight = 200
graphLeftPos = 180
graphTopPos = 25
minimumGraphScale = 50 # The lowest population that the graph will set as the maximum (must be >= 1)
logUpdateRate = 1 # How often is the log at the bottom of the screen updated?
scaleGrassDisplay = False # does the grass line on the time graph adjust its height?
