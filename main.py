# selection screen for the PicoGameBoy by David Monninger, written for SPE Karlsruhe
import os
from PicoGameBoy import PicoGameBoy
import time

TEXT_DISTANCE = 10
BLACK = PicoGameBoy.color(0, 0, 0)
WHITE = PicoGameBoy.color(255, 255, 255)

games = [f for f in os.listdir("/") if f.startswith("g_")]  # collect all possible games
pgb = PicoGameBoy()

selectedIndex = 0
selectionChanged = True
lastButton = 0  # 0 - None, 1 - Up, 2 - Down

while 1:    # main refresh loop

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
        pgb.fill(BLACK)
        # display list of games
        for i in range(len(games)):
            # the selected game is written black on white, the others white on black
            textColor = WHITE
            bgColor = BLACK
            if i == selectedIndex:
                textColor = BLACK
                bgColor = WHITE
            height = i * TEXT_DISTANCE + 2
            pgb.fill_rect(0, height, pgb.width, TEXT_DISTANCE, bgColor)
            pgb.text(games[i][2:-3], 0, height, textColor)
            print(games[i][2:-3] + str(textColor))
        
        pgb.show()
        print(selectedIndex)
        selectionChanged = False
    time.sleep(0.05)

del pgb  # make room for selected game
print(selectedGame)

# execute the selected game file
__import__(selectedGame)
