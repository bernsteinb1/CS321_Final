# Human Playable Flappy Bird
flappy_bird.py contains a (very basic) human playable flappy bird game. Final score is sent to terminal. 

To play the game, run:
- `python3 flappy_bird.py`

Controls:
- space bar: flap
- q: quit the game

If you would like to customize how the game runs (fall speed, pipe size, pipe speed, etc.), all these variables can be adjusted via the constant variables (upper case) at the top of the file.

# AI Flappy Bird
ai_flappy_bird.py implements an AI agent to play the game. 

To watch the AI play the game, run:
- `python3 ai_flappy_bird.py`

The same variables that customize the game above can be modified to change how this version of the game runs as well. Notably, there is a NUM_AGENTS variable that controls the number of AI agents that play the game at once. 1000 seems to be a reasonable amount from our usage/testing.