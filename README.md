# Snake

This is a PyGame project of Snake.
This Project was made by Auwliya Popal / Lemon1 (although I did follow a few youtube tutorials)

Information about the code:
The entire window is 800 px, every block is 40 x 40 px making a 20 x 20 block grid.
The snakes head is [0], the first part of the neck is [1] and so on. This is important to understand the math in some parts of the code. 
The directions are shown like (1,0) on the x and y axis (0 is the top left corner).

To run the game both the snake-project, the graphics folder and the Font folder need to be in the same folder.
The code uses Vector2 to simulate a grid, where the snake consists of blocks in the grid. It does not look like a block because I am using .blit to transport graphics onto the snake blocks

The game can be played with both the arrow keys and WASD controls.
When you crash into yourself or hit a border the game is over. As of right now the game closes itself once you're game over, but I might add a game-over screen or start menu.

There are apples and lemons, when you eat an apple you grow 1 block and get 1 point. When you eat a lemon you grow 2 blocks and gain 2 points.
Lemons have a 33% of showing up, apples 66%

There are comments in the code explaining other uses and info.

Note: It's playable, I might add updates in the future.
