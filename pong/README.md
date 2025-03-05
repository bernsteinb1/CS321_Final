# Human Playable Pong
pong.py contains a human playable pong game. 

To play the game run:
- `python3 pong.py`

Controls:
- Left paddle player
  - w: move up
  - s: move down
- Right paddle player
  - up arrow: move up
  - down arrow: move down

If you would like to customize how the game runs (paddle speed, ball speed, paddle size, etc.), all these variables can be adjusted via the constant variables (upper case) at the top of the file. **Notably**, there is a AI_PLAYER variable. If this variable is True, the right paddle will be played by an "optimal" AI agent.

# AI Pong
ai_pong.py implements an AI agent to play the game as the left paddle against the "optimal" AI agent mentioned above.

To watch the AI learn and play the game, run:
- `python3 ai_pong.py`

The same variables that customize the game above can be modified to change how this version of the game runs as well. Notably, there are more variables that control the training of the neural network (NUM_AGENTS, GENERATIONS, SELECT_NUM, RANDOM_NETWORKS_PER_GEN). Additionally, the AI_PLAYER variable has been removed because the AI_PLAYER is always used to train the neural network.
