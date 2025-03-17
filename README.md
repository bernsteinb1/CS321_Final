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
  - Example output of ai_pong.py when trained. This is not automatically populated when trained, but was created deliberately. The results seen here were cut off after 37 generations because progress had stopped.
- champion.pickle
  - Contains the best (highest scoring) overall AI player trained from running ai_pong.py.
- last_gen.pickle
  - Contains the best AI player from the most recent generation of agents trained from running ai_pong.py.
- champion.pickle and last_gen.pickle can be used within pong.py to set the enemy AI player
