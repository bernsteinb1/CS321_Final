# Human Playable Pong
pong.py contains a human playable pong game. By default, the left paddle is played by our trained AI, and the right paddle is a human player.

To play the game run:
- `python3 pong.py`

Controls:
- Left paddle player
  - w: move up
  - s: move down
- Right paddle player
  - up arrow: move up
  - down arrow: move down

If you would like to customize how the game runs (paddle speed, ball speed, paddle size, etc.), all these variables can be adjusted via the constant variables (upper case) at the top of the file. Changing any of these variables may affect how the AI performs and further training may be required after these are modified. **Notably**, there is an AI_PLAYER variable. If this variable is True, the left paddle will be played by an AI agent trained by our neural network via neuroevolution. The AI that is played against can be set in the main function by changing the relative path to the desired pickle file. 

# AI Pong
We train Pong AIs by running a series of simulated trials where the ball starts in a random configuration immediately
after the AI would have hit it. The ball is then deflected off the right side at a random angle and rewards are assigned
by a paddle's proximity to where the ball hit on the left side.

ai_pong.py trains our neural network to play pong. Graphics have been turned off for this version to train the AI faster.
This is a greedy program; it uses all CPU cores and will max out each of them for the duration of the runtime. On an
M1 Pro Macbook Pro 2021, this code takes several hours to run completion. After each generation, champion.pickle and last_gen.pickle
are overwritten without consideration of whether there is already data in these files to allow for early termination. These files store the neural networks
that performed best overall (champion.pickle) and best in the newest generation (last_gen.pickle).

To train the AI, run:
- `python3 ai_pong.py`

The same variables that customize the game above can be modified to change how this version of the game runs as well. Notably, there are more variables that control the training of the neural network (NUM_AGENTS, GENERATIONS, SELECT_NUM, RANDOM_NETWORKS_PER_GEN). These variables control parameters used when evolving neural networks. Additionally, the AI_PLAYER variable has been removed because the AI_PLAYER is always used to train the neural network. Other variables, like the mutation rate and intensity can be found in nn.py
