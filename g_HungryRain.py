# Hungry_Rain.py by K.G. Orphanides, version 1.5
# A tiny survival game for the Raspberry Pi Pico Game Boy
# Find food. Hide from the flood.

from PicoGameBoy import PicoGameBoy
import time
from random import randint, choice
import machine

pgb = PicoGameBoy()

#sprites
apple_green_bg_14x15=bytearray(b'\x06 \x06 \x06 \x06 \x06 \xb3\xc8\xb3\xc8\x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \xb3\xc8\xb3\xc8\x8cjL\xc9\x14G\x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x06 \x9c\x07\x14\x85\x1c\x88\x1c\x88\x06 \x06 \x06 \x06 \x06 \x06 \xec\xab\xec\xab\xec\xab\x06 \x84H\x1c\xa7\xa4j\xac\xcb\xec\xab\xec\xab\x06 \x06 \x06 \xeci\xeb\xa5\xebc\xeb\xc6\xecI\xec\x8a\xec\x8a\xecI\xeb\xe6\xebc\xeb\xa5\xeci\x06 \xeci\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xeci\xeb\xe6\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebC\xf3\xa4\xf3\xa4\xeb\x83\xebB\xeb\xc6\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xf3\xa4\xf3\xa4\xf3\xa4\xebB\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xf3\x84\xf3\xa4\xf3\xa4\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xebC\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \x06 \xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \x06 \x06 \xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \x06 \x06 \x06 \x06 \xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x06 \x06 \x06 ')
apple_blue_bg_14x15=bytearray(b'\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\xb3\xc8\xb3\xc8\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\xb3\xc8\xb3\xc8\x8cjL\xc9\x14G\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x9c\x07\x14\x85\x1c\x88\x1c\x88\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\xec\xab\xec\xab\xec\xab\x00\x1b\x84H\x1c\xa7\xa4j\xac\xcb\xec\xab\xec\xab\x00\x1b\x00\x1b\x00\x1b\xeci\xeb\xa5\xebc\xeb\xc6\xecI\xec\x8a\xec\x8a\xecI\xeb\xe6\xebc\xeb\xa5\xeci\x00\x1b\xeci\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xeci\xeb\xe6\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebC\xf3\xa4\xf3\xa4\xeb\x83\xebB\xeb\xc6\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xf3\xa4\xf3\xa4\xf3\xa4\xebB\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xf3\x84\xf3\xa4\xf3\xa4\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xebC\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\x00\x1b\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\x00\x1b\x00\x1b\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\x00\x1b\x00\x1b\x00\x1b\x00\x1b\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x1b\x00\x1b\x00\x1b')
dot_14x14=bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x95)\x959\x94QtatqtyS\x81S\x893\x912\x99\x12\xa1\x11\x00\x00\x00\x00)\x95A\x94YtatqtyS\x81S\x912\x912\x99\x12\xa1\x11\xa8\xf1\x00\x00\x00\x00A\x94YtitqsyS\x81S\x912\x992\x99\x12\xa1\x11\xa8\xf1\xb0\xd1\x00\x00\x00\x00YtitqSyS\x81S\x912\x992\xa1\x12\xa1\x11\xa8\xf1\xb0\xd1\xb8\xd0\x00\x00\x00\x00itqs\x81S\x81S\x912\x992\xa1\x12\xa9\x11\xa8\xf1\xb0\xf0\xb8\xd0\xc0\xb0\x00\x00\x00\x00qsyS\x89S\x912\x992\xa1\x12\xa1\x11\xa8\xf1\xb0\xd0\xb8\xd0\xc0\xb0\xc0\x8f\x00\x00\x00\x00\x81S\x89S\x912\x99\x12\xa1\x12\xa9\x11\xa8\xf1\xb0\xd0\xb8\xb0\xc0\xb0\xc0\x8f\xc8o\x00\x00\x00\x00\x89S\x912\x992\xa1\x12\xa9\x11\xa8\xf1\xb0\xd0\xb8\xb0\xc0\xb0\xc0\x8f\xc8o\xd0N\x00\x00\x00\x00\x912\x992\xa1\x11\xa8\xf1\xa8\xf1\xb0\xd0\xb8\xd0\xc0\xaf\xc8\x8f\xc8O\xd0N\xd0\x0e\x00\x00\x00\x00\x99\x12\xa1\x12\xa8\xf1\xb0\xf1\xb8\xd0\xb8\xd0\xc0\xaf\xc8\x8f\xc8o\xd0.\xd0\x0e\xd8\r\x00\x00\x00\x00\xa1\x11\xa8\xf1\xb0\xf1\xb8\xd0\xb8\xb0\xc0\xaf\xc8\x8f\xc8o\xd0.\xd8\r\xd8\r\xd8\r\x00\x00\x00\x00\xa9\x11\xb0\xf1\xb8\xd0\xb8\xb0\xc0\x8f\xc8\x8f\xc8N\xd0.\xd8\r\xd8\r\xd8\r\xd8\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
apple_black_bg_14x15=bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb3\xc8\xb3\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb3\xc8\xb3\xc8\x8cjL\xc9\x14G\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9c\x07\x14\x85\x1c\x88\x1c\x88\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xec\xab\xec\xab\xec\xab\x00\x00\x84H\x1c\xa7\xa4j\xac\xcb\xec\xab\xec\xab\x00\x00\x00\x00\x00\x00\xeci\xeb\xa5\xebc\xeb\xc6\xecI\xec\x8a\xec\x8a\xecI\xeb\xe6\xebc\xeb\xa5\xeci\x00\x00\xeci\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xeci\xeb\xe6\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebC\xf3\xa4\xf3\xa4\xeb\x83\xebB\xeb\xc6\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xf3\xa4\xf3\xa4\xf3\xa4\xebB\xebc\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xf3\x84\xf3\xa4\xf3\xa4\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebc\xebC\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\x00\x00\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\x00\x00\x00\x00\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xebB\xebB\xebB\xebB\xebB\xebB\xebB\xebB\x00\x00\x00\x00\x00\x00')
shelter_stone_30x5=bytearray(b'k\xcfk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xefk\xcfk\xcfk\xefc.c.c.c.c.k\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xefk\xcfk\xcfk\xefc.c.c.k\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfc.c.c.k\xcfk\xefk\xcfk\xcfk\xefk\xcfk\xcfc.k\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfc.k\xcfk\xefk\xcfk\xcfk\xefk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xcfk\xefk\xcf')

pgb.add_sprite(apple_green_bg_14x15,14,15) # sprite 0
pgb.add_sprite(apple_blue_bg_14x15,14,15) # sprite 1
pgb.add_sprite(dot_14x14,14,14) # sprite 2
pgb.add_sprite(apple_black_bg_14x15,14,15) # sprite 3
pgb.add_sprite(shelter_stone_30x5,30,5) # sprite 4

#settings
intro = True
game = False
gameover = False
BACKGROUND_COLOR = PicoGameBoy.color(0,197,0)
BOX_COLOR = PicoGameBoy.color(255,255,255)

#define dot's starting x and y cordinates
x = 113
y = 113
#save last position for collisions
last_x = 113
last_y = 113

#what does dot look like?
dot_width = 14
dot_height = 14

#define and initialise food 
food_width = 14
food_height = 15
food_available = False

#initialise hunger timer and food meter
reference_time = time.ticks_ms()
food = 100

#initialise flood
antediluvian_time = time.ticks_ms()
flood = False
flood_y = 3
flood_delay = 15000
flood_duration = 10000
FLOOD_COLOR = PicoGameBoy.color(0,0,220)

#define shelter positions
SHELTER_COLOR = PicoGameBoy.color(0,0,0)
shelter1_width = 30  #width
shelter1_height = 5   #height
shelter1_pos_x = choice([i for i in range(10,210) if i not in (105,121)]) #excluding positions that will cause shelter to spawn on dot
shelter1_pos_y = choice([i for i in range(10,230) if i not in (105,121)])
shelter1_overhang = 233 - shelter1_pos_y

shelter2_width = 30
shelter2_height = 5
shelter2_pos_x = choice([i for i in range(10,210) if i not in (106,134)]) #excluding positions that will cause shelter to spawn on dot
shelter2_pos_y = choice([i for i in range(10,230) if i not in (106,134)])
shelter2_overhang = 233 - shelter2_pos_y

shelter3_width = 30
shelter3_height = 5
shelter3_pos_x = choice([i for i in range(10,210) if i not in (106,134)]) #excluding positions that will cause shelter to spawn on dot
shelter3_pos_y = choice([i for i in range(10,230) if i not in (106,134)])
shelter3_overhang = 233 - shelter3_pos_y

# collision detection function - feed it the x, y, width and height of dot and the x, y, width and height of the thing to check collision against
def collision(x1,y1,w1,h1,x2,y2,w2,h2):
        
    if x1+w1 < x2:
        return False        
    if x2+w2 < x1:
        return False        
    if y1+h1 < y2:
        return False              
    if y2+h2 < y1:
        return False 
    else:
        return True

#instructions
while intro:
        pgb.text("HUNGRY RAIN",80,25,PicoGameBoy.color(255,255,255))
        pgb.text("You are dot.",20,40,PicoGameBoy.color(255,255,255))
        pgb.sprite(2,20,50)
        pgb.text("Find food.",20,70,PicoGameBoy.color(255,255,255))
        pgb.sprite(3,20,80)
        pgb.text("Hide from the flood.",20,100,PicoGameBoy.color(255,255,255))
        pgb.fill_rect(20,110,12,12,FLOOD_COLOR)
        pgb.text("Shelter beneath the stones.",20,128,PicoGameBoy.color(255,255,255))
        pgb.sprite(4,20,140)
        pgb.text("Press A or B to start",38,180,PicoGameBoy.color(255,255,255))
        pgb.show()
        if pgb.button_A() or pgb.button_B():
            game = True
            intro = False
            antediluvian_time = time.ticks_ms() #so intro doesn't result in shorter flood delay on first round

# game loop
while game:       
        
    #gameover screen 
    if gameover==True:
        time.sleep_ms(100) # let them see how they died
        pgb.fill_rect(10,40,220,100,PicoGameBoy.color(0,0,0))
        pgb.text("GAME OVER",85,75,PicoGameBoy.color(255,255,255))
        pgb.text("Press A or B to restart",30,100,PicoGameBoy.color(255,255,255))
        pgb.show()
        if pgb.button_A() or pgb.button_B():
            machine.reset() #restart game, the hard way
     
    elif gameover is not True:
        #run the hunger timer
        if time.ticks_ms() > reference_time + 1000:
            reference_time = time.ticks_ms()
            food = food - 1
        
        #run the flood timers
        if time.ticks_ms() > antediluvian_time + flood_delay: 
            flood = True
                
        if time.ticks_ms() > antediluvian_time + flood_delay + flood_duration:
            flood = False
            antediluvian_time = time.ticks_ms()
        
        #draw the game scene:
        
        #the background    
        if flood:
            pgb.fill(FLOOD_COLOR)
        else:
            pgb.fill(BACKGROUND_COLOR)    

        #the box
        pgb.rect(1,1,238,238,BOX_COLOR)
               
        #shelters' protective shadows in a flood
        pgb.fill_rect(shelter1_pos_x,shelter1_pos_y + 5,shelter1_width,shelter1_overhang,BACKGROUND_COLOR)
        pgb.fill_rect(shelter2_pos_x,shelter2_pos_y + 5,shelter2_width,shelter2_overhang,BACKGROUND_COLOR)
        pgb.fill_rect(shelter3_pos_x,shelter3_pos_y + 5,shelter3_width,shelter3_overhang,BACKGROUND_COLOR)
        
        #the shelters
        pgb.sprite(4,shelter1_pos_x,shelter1_pos_y)
        pgb.sprite(4,shelter2_pos_x,shelter2_pos_y)
        pgb.sprite(4,shelter3_pos_x,shelter3_pos_y)

        #draw dot
        pgb.sprite(2,x,y)
        
        #move dot
        if pgb.button_left():
            last_x = x            #record last known position in case we need to call it upon hitting a solid object
            x = x - 1
        if pgb.button_right():
            last_x = x
            x = x + 1
        if pgb.button_up():
            last_y = y
            y = y - 1
        if pgb.button_down():
            last_y = y
            y = y + 1    
                
        #you're not allowed past the walls
        if x < 3:
            x = last_x
        if x > 224:
            x = last_x
        if y < 3:
            y = last_y
        if y > 224:
            y = last_y
        
        #check for collisions with shelter 1
        if collision(x,y,dot_width,dot_height,shelter1_pos_x,shelter1_pos_y,shelter1_width,shelter1_height):
            x = last_x
            y = last_y
        
        #check for collisions with shelter 2
        if collision(x,y,dot_width,dot_height,shelter2_pos_x,shelter2_pos_y,shelter2_width,shelter2_height):
            x = last_x
            y = last_y
   
        #check for collisions with shelter 3
        if collision(x,y,dot_width,dot_height,shelter3_pos_x,shelter3_pos_y,shelter3_width,shelter3_height):
            x = last_x
            y = last_y
         
        # water is deadly
        if flood:
            if collision(x,y,dot_width,dot_height,shelter1_pos_x,shelter1_pos_y,shelter1_width,shelter1_overhang):
                gameover = False
            elif collision(x,y,dot_width,dot_height,shelter2_pos_x,shelter2_pos_y,shelter2_width,shelter2_overhang):
                gameover = False
            elif collision(x,y,dot_width,dot_height,shelter3_pos_x,shelter3_pos_y,shelter3_width,shelter3_overhang):
                gameover = False
            else:
                gameover = True
        
        #food! (generate random position for food)
        if food_available==False:
            foodSpawn_x = randint(15,215)
            foodSpawn_y = randint(15,215)
            food_available = True
     
        if food_available==True and flood==False:   
            pgb.sprite(0,foodSpawn_x,foodSpawn_y)
        
        elif food_available==True and flood==True:
            #make sure we have the right background colour
            if collision(foodSpawn_x,foodSpawn_y,food_width,food_height,shelter1_pos_x,shelter1_pos_y,shelter1_width,shelter1_overhang):
                pgb.sprite(0,foodSpawn_x,foodSpawn_y)
            elif collision(foodSpawn_x,foodSpawn_y,food_width,food_height,shelter2_pos_x,shelter2_pos_y,shelter2_width,shelter2_overhang):
                pgb.sprite(0,foodSpawn_x,foodSpawn_y)
            elif collision(foodSpawn_x,foodSpawn_y,food_width,food_height,shelter3_pos_x,shelter3_pos_y,shelter3_width,shelter3_overhang):
                pgb.sprite(0,foodSpawn_x,foodSpawn_y)
            else:
                pgb.sprite(1,foodSpawn_x,foodSpawn_y)
             
        #dot eats food
        if collision(x,y,dot_width,dot_height,foodSpawn_x,foodSpawn_y,food_width,food_height):
            pgb.fill_rect(foodSpawn_x,foodSpawn_y,food_width,food_height,BACKGROUND_COLOR)
            food = food + 10 #get less hungry
            food_available = False 

        #die of starvation
        if food==0:
            gameover = True

        #hunger
        pgb.text("Food:"+ str(food),170,5)
        
        #debug tools
        #pgb.text("position:"+ str(x) + "," + str(y),5,15)
        
        #flood countdown
        if flood:
            pgb.text("Flood count: NOW",5,5)
          
        else:
            flood_countdown = time.ticks_diff(antediluvian_time + flood_delay,time.ticks_ms())
            pgb.text("Flood count:"+ str(round(flood_countdown/1000,1)),5,5)        
                
        #transfer all this from the framebuffer to the screen          
        pgb.show()

# Credits
# Apple and stone images modified from Kenney Game Assets (https://kenney.itch.io/)
# Pico Game Boy libraries by Vincent Mistler of YouMakeTech
# AABB collision detection code adapted from a function by Matthieu Mistler

# License
# The MIT License (MIT)
# Copyright (c) 2013-2017 Damien P. George, and others
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

