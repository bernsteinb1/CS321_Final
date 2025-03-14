# Human Playable Pong
pong.py contains a human playable pong game. By default, the left paddle played by our trained AI, and the right paddle is a human player.

To play the game run:
- `python3 pong.py`

Controls:
- Left paddle player
  - w: move up
  - s: move down
- Right paddle player
  - up arrow: move up
  - down arrow: move down

If you would like to customize how the game runs (paddle speed, ball speed, paddle size, etc.), all these variables can be adjusted via the constant variables (upper case) at the top of the file. **Notably**, there is a AI_PLAYER variable. If this variable is True, the right paddle will be played by an AI agent trained by our neural network via neuroevolution. The AI that is played against can be set in the main function. 

# AI Pong
ai_pong.py trains our neural network to play pong. Graphics have been turned off for this version to train the AI faster.

To train the AI, run:
- `python3 ai_pong.py`

Controls:
- space bar: toggle graphics on/off

The same variables that customize the game above can be modified to change how this version of the game runs as well. Notably, there are more variables that control the training of the neural network (NUM_AGENTS, GENERATIONS, SELECT_NUM, RANDOM_NETWORKS_PER_GEN). Additionally, the AI_PLAYER variable has been removed because the AI_PLAYER is always used to train the neural network.
