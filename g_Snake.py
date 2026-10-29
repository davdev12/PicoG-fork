import random
from PicoGameBoy import PicoGameBoy
import time
from machine import Timer
import machine

BLACK = PicoGameBoy.color(0, 0, 0)
WHITE = PicoGameBoy.color(255, 255, 255)
RED = PicoGameBoy.color(255, 0, 0)

pgb = PicoGameBoy()

# Konstanten für die Unterteilung des Displays in größere Pixel
PIXEL_FACTOR = 10

GAME_WIDTH = int(pgb.width / PIXEL_FACTOR)
GAME_HEIGHT = int(pgb.height / PIXEL_FACTOR)

# Snake als Liste von Koordinaten, startet in der Mitte des Spielfelds
snake = [[int(GAME_WIDTH / 2), int(GAME_HEIGHT / 2)]]

# Position des Futters
reward = [0, 0]
reward_captured = True

# aktuelle Richtung: 0 ist oben, dann im Uhrzeigersinn durchnummeriert
direction = 0

# Statusvariablen der Taster
button_pressed = False
button_left_previous = True
button_right_previous = True
button_up_previous = True
button_down_previous = True
button_left_time = 0
button_right_time = 0

# Zur Steuerung der regelmäßigen Iteration
timer = Timer()
game_step = False


def game_iteration(t):
    # Funktion zur Aktivierung der nächsten Spieliteration
    global game_step
    game_step = True


timer.init(freq=4, mode=Timer.PERIODIC, callback=game_iteration)

# Hauptschleife
while True:
    # Taster abfragen
    if not button_pressed:  # nur ein Richtungswechsel pro Iteration ist möglich
        button_right = pgb.button_right()
        button_left = pgb.button_left()
        button_down = pgb.button_down()
        button_up = pgb.button_up()
        
        if button_right and direction != 3:
            direction = 1  # Rollover über Modulo
            button_pressed = True

        if button_left and direction != 1:
            # statt einmal nach links wird dreimal nach rechts abgebogen → Rollover mit Modulo funktioniert auch hier
            direction = 3
            button_pressed = True
        
        if button_up and direction != 2:
            # statt einmal nach links wird dreimal nach rechts abgebogen → Rollover mit Modulo funktioniert auch hier
            direction = 0
            button_pressed = True
        
        if button_down and direction != 0:
            # statt einmal nach links wird dreimal nach rechts abgebogen → Rollover mit Modulo funktioniert auch hier
            direction = 2
            button_pressed = True
    # Spieliteration
    if game_step:  # Iteration nur, wenn die entsprechende Zeit abgelaufen ist
        # Richtung in x- und y-Komponenten zerlegen
        if direction == 0:
            dir_x = 0
            dir_y = -1
        elif direction == 1:
            dir_x = 1
            dir_y = 0
        elif direction == 2:
            dir_x = 0
            dir_y = 1
        else:
            dir_x = -1
            dir_y = 0

        # Futter abfragen
        if reward_captured:
            reward = [random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)]
            while reward in snake:
                reward = [random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)]
            reward_captured = False
        else:
            snake.pop(0)

        # neue Koordinaten für Schlangenkopf
        snake_head_x = snake[-1][0] + dir_x
        snake_head_y = snake[-1][1] + dir_y

        if snake_head_x < 0 or snake_head_x >= GAME_WIDTH:
            break

        if snake_head_y < 0 or snake_head_y >= GAME_HEIGHT:
            break

        if [snake_head_x, snake_head_y] in snake:
            break

        # neuen Schlangenkopf ans Ende der Snake hängen
        snake.append([snake_head_x, snake_head_y])

        # Abfrage, ob Futter erreicht
        if [snake_head_x, snake_head_y] == reward:
            reward_captured = True

        # Display aktualisieren
        pgb.fill(BLACK)  # clear
        pgb.fill_rect(reward[0] * PIXEL_FACTOR, reward[1] * PIXEL_FACTOR, PIXEL_FACTOR, PIXEL_FACTOR, RED)
        pgb.rect(0, 0, pgb.width, pgb.height, WHITE)
        for pixel in snake:  # Snake zeichnen
            pgb.fill_rect(pixel[0] * PIXEL_FACTOR + 1, pixel[1] * PIXEL_FACTOR + 1, PIXEL_FACTOR - 2, PIXEL_FACTOR - 2,
                          WHITE)
        pgb.show()  # Alles anzeigen

        game_step = False
        button_pressed = False

# Game Over- Screen anzeigen
time.sleep_ms(100)
pgb.text("GAME OVER", 85, 75, WHITE)
pgb.text("Press A or B to restart", 30, 100, WHITE)
pgb.show()
# auf Input warten
while True:
    if pgb.button_A() or pgb.button_B():
        machine.reset()  # alles zurücksetzen
