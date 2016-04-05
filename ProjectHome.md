PyBreakout - a Breakout clone written in Python using the Pygame libraries



I created this little game using Python 2.4.3, Pygame 1.7.1, and finally created the .exe distribution using py2exe 0.6.

This is my second project that I have done with the awesome Pygame Libraries and I plan to continue this project based on user feedback, so let me know what needs to be tweaked.

What is the current version?

The current version, which this document describes, is pybreakout 0.3 released on 2006/10/19 .


What's the goal of the game?


  * You are a paddle that can move left and right, you launch the ball from your paddle by pressing the LEFT mouse button.
  * The goal of the game is simple, just keep the ball from falling into the abyss beneath you and hit all of the destructible blocks on the level to advance and gain points.
  * You have 3 lives when you start the game.
  * During the level your ball will increase in speed every 15 seconds, until it reaches a pretty quick max speed.
  * You will be awarded a new life if you acquire 500 pts, and another at 1500 pts.




How do I control the game?


  * Press ESC to End game
  * Right or Middle click the mouse - Reset the ball ( Looses 1 life )
  * Left click the mouse- Launch the ball off the paddle
  * Move Mouse left within the Pygame window- Move the paddle left
  * Move Mouse right within the Pygame window - Move the paddle right




How to launch PyBreakout ( only tested on WinXP, sorry )

Windows XP/2000


  1. Download the pybreakout-0.3-win.zip.
> 2. Unzip this pybreakout-

&lt;currentVersion&gt;

-win.zip to a suitable location, your Desktop or where ever you want.
> 3. Double-click on pybreakout.exe within the newly unzipped directory and start playing!



**Nix / Mac**


  1. Download the pybreakout-0.3-src.zip
> 2. Unzip this pybreakout-

&lt;currentVersion&gt;

-src.zip to a suitable location.
> 3. Assuming that you have Python 2.4 and Pygame installed correctly, simply type "python pybreakout.py" at the command prompt in the src/ directory and it should work.
> 4. View and critique the source code and drop me a line on how sweet it is...





Checkout the latest Source Code from Google Code's Subversion Repository


  1. Get TortoiseSVN or Eclipse with the Subclipse plugin and the PyDev plugin or a suitable Subversion client...
> 2. Follow the directions on the Source Tab of the Pybreakout page





Game Notes


Version 0.3 Notes
I have added several cool features in this release but probably the most exciting is:
POWERUPS! I have successfully implemented both a Slowball powerup as well as a Triball powerup.

Here are all the changes in this version:


  * Created a Triball Bonus which splits your main ball into 2 additional balls. You can get this powerup several times and have some real fun with many balls.
  * Created a Slowball Bonus which slows all balls on the board down to the slowest speed. Very helpful on higher levels.
  * These bonuses occur randomly when destroying bricks
  * Many improvements to the Mouse Control, and capture of the cursor when the game is primary focused.
  * Added ESC key to end game at any time (because you can no longer hit the "X")
  * The paddle now has five zones of redirection for more control over where you will redirect the balls.
  * Each successful level begins at a higher speed until you have reset to level 0
  * Now even GREY BRICKS are destructible once they have been hit 4 times. This was needed to avoid some infinite ball loops in the levels.
  * I have used the --bundle flag in py2exe so that it has a much more organized distribution
  * I spent some time refactoring and improving the codebase during this period especially when I had to account for several balls instead of only one ball on the board.




Version 0.2 Notes

I have added several features to this release including:


  * Mouse Control of paddle Left and Right
  * Mouse Control - Left Click (strictly pygame's button1) to launch the ball
  * Mouse Control - Right Click or Middle Click (strictly pygame's button2 or button3) to use next life
  * Improved ball redirection based on where it hits the paddle, if the ball hits the left 10px of the paddle it is redirected up and left, middle 20 px it is reflected, right 10 px it is always reflected up and right. This improves directional control of ball.
  * Sound Effects - for bouncing off gameboard walls, destroying blocks, bouncing off paddle, bouncing off indestructible blocks, and when you get extra lives
  * Reset speed to 1 ( rather slow ) when you advance to next level instead of leaving it at whatever speed you passed the previous level at.



Thanks to Peter Nosgoth for trying the game out and giving me some pointers on how to improve it on the Pygame page


Version 0.1 Notes

Version 0.1 is available as src only.

After some gentle poking and prodding from my boy Chryso on this here forum, I decided that Pygame was cool enough and easy enough so that I would pound out PyBreakout in about a weeks time... even being out of town all week

This project is much more ambitious and more fun than Avoidgame so I am going to keep it up and tweak it until it is pretty sweet. But this current version should be playable.

Check it out, and let me know what you think!