# selection screen for the PicoGameBoy by David Monninger, written for SPE Karlsruhe
import os
from PicoGameBoy import PicoGameBoy
import time
from time import sleep
from array import array

TEXT_DISTANCE = 17
BLACK = PicoGameBoy.color(0, 0, 0)
WHITE = PicoGameBoy.color(255, 255, 255)
YELLOW = PicoGameBoy.color(218, 172, 6)
LIGHT_GRAY = PicoGameBoy.color(231,231,231)
GRAY = PicoGameBoy.color(125,125,125)
RED = PicoGameBoy.color(184,10,65)
BLUE = PicoGameBoy.color(78,75,168)
GREEN = PicoGameBoy.color(110,177,34)
CYAN = PicoGameBoy.color(0,147,138)

textColors = [RED, BLUE, GREEN, YELLOW, CYAN]

games = [f for f in os.listdir("/") if f.startswith("g_")]  # collect all possible games
pgb = PicoGameBoy()

selectedIndex = 0
selectionChanged = True
lastButton = 0  # 0 - None, 1 - Up, 2 - Down

def draw_arrow(x,y,color):
    #points_array = array("h",[x+30,y+8,x+30,y-16])
    #pgb.poly(x, y, points_array, color, True)
    pgb.vline(x, y + 0, 9, color)  
    pgb.vline(x - 1, y + 1, 7, color)
    pgb.vline(x - 2, y + 2, 5, color)
    pgb.vline(x - 3, y + 3, 3, color)
    pgb.vline(x - 4, y + 4, 1, color)

while 1:    # main refresh loop
   # pgb.add_sprite(game_boy,12,12)
    # check for button presses
    if pgb.button_A() or pgb.button_B():
        # A or B selects the current game and exits the loop
        selectedGame = games[selectedIndex][:-3]
        break
    elif pgb.button_up():
        # only register a new button press if the button was released
        if lastButton != 1:
            lastButton = 1
            selectedIndex -= 1
            if selectedIndex < 0:
                selectedIndex = len(games) - 1
            selectionChanged = True
    elif pgb.button_down():
        # only register a new button press if the button was released
        if lastButton != 2:
            lastButton = 2
            selectedIndex = (selectedIndex + 1) % len(games)
            selectionChanged = True
    else:
        lastButton = 0

    if selectionChanged:    # only update the screen if there is something to update
        pgb.fill(LIGHT_GRAY)
        #pgb.add_sprite(game_boy,0,0)
        # display list of games
        for i in range(len(games)):
            
            # the selected game is written black on white, the others white on black
            textColor = textColors[i % 5]
            bgColor = LIGHT_GRAY
            height = i * TEXT_DISTANCE+98
            
            if i == selectedIndex:
                textColor = BLACK
                bgColor = YELLOW
                draw_arrow(len(games[i]) * 7,height+7,BLACK)
            
            pgb.fill_rect(0, 240, pgb.width, TEXT_DISTANCE, bgColor)   
            pgb.text(games[i][2:-3], 0, height+7, textColor)
        
        print(games[i][2:-3] + str(textColor))
        pgb.load_image("/gameboy_240x98.bin") # load the .bin file into the framebuffer
        pgb.show()
        print(selectedIndex)
        selectionChanged = False
    time.sleep(0.05)

del pgb  # make room for selected game
print(selectedGame)

# execute the selected game file
__import__(selectedGame)

