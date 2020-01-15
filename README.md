# Pong
A simple pong game

Written in Python utilizing the Turtle module. 

Based off simple tutorial by Based on tutorial by @TokyoEdTech

 Script modified in the following (major) ways.
 1. Improved performance by splitting object position calculation and object drawing into two seperate processes.
    The object positions are calculated every 'timer_val' interval (default 30FPS). The draw function is constantly 
    invoked, but only performs an action if the objects locations have changed (again at 30FPS).
 2. Improved keyboard inputs. Original script moved paddles only on keyboard presses. This leads to a behavior where
    the paddle moves initially, pauses, then moves continuously. Additionally multiple keys being pressed are not
    detected - ie moving one paddle prevents the other moving. This has been addressesd by setting movement variables 
    on key presses and releases. The value of the movement variables is checked each loop ('timer_val' interval) and
    the y-coordinate is adjusted accordingly.
 3. Minor gameplay changes. Starting velocity of ball is randomized (up-left, up-right, down-left, down-right). Ball
    moves slightly faster each time it is hit by a paddle. After scoring ball is served back at the winner of the point
    and its initial y location lies within (-150, 150) pixels of centre.
