#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Simple pong demo game
# Based on tutorial by @TokyoEdTech

# Script modified in the following (major) ways.
# 1. Improved performance by splitting object position calculation and object drawing into two seperate processes.
#    The object positions are calculated every 'timer_val' interval (default 30FPS). The draw function is constantly 
#    invoked, but only performs an action if the objects locations have changed (again at 30FPS).
# 2. Improved keyboard inputs. Original script moved paddles only on keyboard presses. This leads to a behavior where
#    the paddle moves initially, pauses, then moves continuously. Additionally multiple keys being pressed are not
#    detected - ie moving one paddle prevents the other moving. This has been addressesd by setting movement variables 
#    on key presses and releases. The value of the movement variables is checked each loop ('timer_val' interval) and
#    the y-coordinate is adjusted accordingly.
# 3. Minor gameplay changes. Starting velocity of ball is randomized (up-left, up-right, down-left, down-right). Ball
#    moves slightly faster each time it is hit by a paddle. After scoring ball is served back at the winner of the point
#    and its initial y location lies within (-150, 150) pixels of centre.



import turtle #basic graphics
import numpy as np 

##import ipyturtle 
import os
from playsound import playsound #cross platform sound playing module

window = turtle.Screen()
window.title("Pong")
window.bgcolor("black")
window.setup(width=800, height=600)
# Note window dimensions are -400:400, -300:300
window.tracer(0) #stops window size updating

# Scores
score_l = 0
score_r = 0

# Constants
FPS = 30
timer_val = 1000//FPS #timer interval in ms
# initial ball movement speeds
ball_dx0 = 4
ball_dy0 = 4
paddle_v = 6 #paddle movement speed

# time_variable
t = 0 #set initial time
draw_ = True #draw on / off
y_l = 0 #initial left paddle position
y_r = 0 #initial right paddle position
ball_x = 0 #initial ball coordinates
ball_y = 0
ball_dx = ball_dx0*np.random.choice([-1,1])
ball_dy = ball_dy0*np.random.choice([-1,1])
p_l_up, p_r_up, p_l_down, p_r_down = 0, 0, 0, 0 #initial paddle movements


# Score Screen
pen = turtle.Turtle()
# set animation speed
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))


# Paddle L
paddle_l = turtle.Turtle()
#update speed
paddle_l.speed(0)
paddle_l.shape("square")
paddle_l.color("white")
# default pixel size 20 by 20
paddle_l.shapesize(stretch_wid=5, stretch_len=1)
paddle_l.penup()
paddle_l.goto(-350,y_l)


# Paddle R
paddle_r = turtle.Turtle()
#update speed
paddle_r.speed(0)
paddle_r.shape("square")
paddle_r.color("white")
# default pixel size 20 by 20
paddle_r.shapesize(stretch_wid=5, stretch_len=1)
paddle_r.penup()
paddle_r.goto(350,y_l)


# Ball
ball = turtle.Turtle()
#update speed
ball.speed(0)
ball.shape("square")
ball.color("white")
# default pixel size 20 by 20
ball.penup()
ball.goto(0,0)
#ball changes by n pixels each update
#ball.dx = 0.2
#ball.dy = 0.2



# allow keyboard presses to control movement

def p_l_up_press():
    global p_l_up
    p_l_up = 1
def p_l_down_press():
    global p_l_down
    p_l_down = 1
def p_l_up_release():
    global p_l_up
    p_l_up = 0
def p_l_down_release():
    global p_l_down
    p_l_down = 0
def p_r_up_press():
    global p_r_up
    p_r_up = 1
def p_r_down_press():
    global p_r_down
    p_r_down = 1
def p_r_up_release():
    global p_r_up
    p_r_up = 0
def p_r_down_release():
    global p_r_down
    p_r_down = 0

window.onkeypress(p_l_up_press, "w")
window.onkeypress(p_l_down_press, "s")
window.onkeyrelease(p_l_up_release, "w")
window.onkeyrelease(p_l_down_release, "s")
window.onkeypress(p_r_up_press, "Up")
window.onkeypress(p_r_down_press, "Down")
window.onkeyrelease(p_r_up_release, "Up")
window.onkeyrelease(p_r_down_release, "Down")




# Keyboard Binding to execute paddle movements
window.listen()



# Define playing sound 
def play_hit():
    # set block = False to run asynchronously
    # prevents pause in game on playing sound
    playsound('tennis_ball_hit.wav', block=False)
    

# Define ball movements
    
def movement():
    
    global ball_x, ball_y, ball_dx, ball_dy, score_l, score_r, t, p_l_down, p_l_up, y_l, p_r_down, p_r_up, y_r, paddle_v
    
    #increment time 
    t += timer_val
    
    # apply left paddle movement
    y_l += paddle_v*(p_l_up-p_l_down)
    if y_l > 260:
        y_l = 260
    if y_l < -260:
        y_l = -260
    # apply right paddle movement
    y_r += paddle_v*(p_r_up-p_r_down)
    if y_r > 260:
        y_r = 260
    if y_r < -260:
        y_r = -260
    
    # apply ball movement
    ball_x = ball_x + ball_dx
    ball_y = ball_y + ball_dy
    
    # check boundary conditions
    if ball_y > 290:
        ball_y = 290
        #reflect y velocity
        ball_dy *= -1
    if ball_y < -290:
        ball_y = -290
        ball_dy *= -1
    
    # check points scored
    if ball_x > 390:
        ball_x = 0
        ball_y = np.random.randint(-150,150)
        score_l += 1
        # reset ball veloities
        ball_dx = -ball_dx0
        ball_dy = ball_dy0*np.random.choice([-1,1])
    if ball_x < -390:
        ball_x = 0
        ball_y = np.random.randint(-150,150)
        score_r += 1
        # reset ball velocities
        ball_dx = ball_dx0
        ball_dy = ball_dy0*np.random.choice([-1,1])
    
    # check paddle collisions
    if ball_x > 340 and ball_x < 360:
        if ball_y < y_r + 40 and ball_y > y_r - 40:
            if ball_dx >0:
                #reflect and speed up ball
                ball_dx *= -1.1
                ball_dy *= 1.1
                play_hit()
    if ball_x < -340 and ball_x > -360:
        if ball_y < y_l + 40 and ball_y > y_l -40:
            if ball_dx < 0:
                #reflect and speed up ball
                ball_dx *= -1.1
                ball_dy *= 1.1
                play_hit()
    
    # recall the function after timer_val
    window.ontimer(movement, timer_val)
    
    
#drawing function
def draw(ball_x, ball_y, score_l, score_r, y_l, y_r):
    global v, draw_
    
    #if drawing is off
    if draw_ == False:
        return
    #else redraw ball object and scores
    ball.setx(ball_x)
    ball.sety(ball_y)
    paddle_l.sety(y_l)
    paddle_r.sety(y_r)
    pen.clear()
    pen.write("Player A: {}  Player B: {}".format(score_l, score_r), align="center", font=("Courier", 24, "normal"))
    #draw_ = False #turn drawing off until next time interval



    
# perform ball and paddle position updates every frame (timer_val intervals)
window.ontimer(movement, timer_val)
    
 
#Main game loop
while True:

    #drawing component
    draw(ball_x, ball_y, score_l, score_r, y_l, y_r)

    # update the window screen once on every loop
    window.update()

