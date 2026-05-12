Welcome to Funtime foxy's survivial run!!

Description:

This has been a slightly revised version of what was originally planned as the original plan was a little too complex given my current coding skills.

Featuring the character Funtime foxy, this is about simply survivial in the game while a silly little enemy comes towards the player,
the goal is to just hit them to make them go away, but if they collide with the player, the player will lose a heart. The player has 3 hearts,
and once those are up, the sprite dies and the game is over. 

The game runs infinitely in a way of just seeing how many enemies the user can kill off before they're meet with their demise.

Features:
Features the player sprite, which takes the inputs of w, a , s , d to move, and the left click of the mouth to attack. When the player isnt moving,
a little idle animation plays, and when they move or attack or die, another type of animation plays.

The player is brought to main menu screen where that is where the code starts and once the player moves to the far right of the screen, thats when the game
begins!! 
Enemies will start spawning and honing in on the player while the player can move around the screen freely and hit them to fight back.

If the player presses the r key, they are respawned, restarting the game all over again. But should they press the escape keep, the game ends all together,
exiting out of the game and closing it. This is to help with the fact the game goes into full screen so the user isnt able to press the x on the corner of the canvas.


Challenges
A challenge was figuring out how to transition between images for the background and start the game once the player moves to the right side of the screen.
A lot of the sprites for the game had to be hidden and not be allowed to call till the game "started" and functions for the enemies, health bar, death, reset
were only called once that happened.

Another challenge was just the amount of def and classes, each sprite function required a lot of things that ended up making each class line long
and if there were errors made it difficult to spot them as easy if the code was shorter. 
Something that helped though was creating different text files for 
