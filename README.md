# CS321_Final
A repository containing code for an AI agent to play Flappy Bird and Pong. 

# Dependencies:
- numpy
- pygame

# How to run code:
- To play against our pre-trained AI, run the command:
  - `python3 pong/pong.py`
- To train pong (which will override the pretrained model) or play flappy_bird, run:
  - `python3 flappy_bird/ai_flappy_bird.py`
  - `python3 pong/ai_pong.py`
  - Generally: `python3 <name of file>`

# Miscellaneous files:
- results.txt
  - Example output of ai_pong.py when trained. This is not automatically populated when trained, but was created deliberately. The results seen here were cut off after 37 generations because progress had stopped. It's difficult to represent exactly what score means, but, broadly speaking, it is a measurement of how often the neural network is able to hit the ball with the center of its paddle. A perfect score for 1,000 trials is, therefore, 1,000 as it means the network always hits the ball with the perfect center of the paddle. The further away a paddle is the lower its score will be. Because of this, it is more important to focus on the improvement trends of scores rather than the values themselves.
- champion.pickle
  - Contains the best (highest scoring) overall AI player trained from running ai_pong.py.
- last_gen.pickle
  - Contains the best AI player from the most recent generation of agents trained from running ai_pong.py.
- champion.pickle and last_gen.pickle can be used within pong.py to set the enemy AI player
