from DQN import DQNAgent 
from game import SoccerGame as env
import torch
import numpy as np
import random
from itertools import count

BATCH_SIZE = 128
DIVERSIFY_MEMORY = 0.25
MEMORY_CAPACITY = 8500

GAMMA = 0.75
LEARNING_RATE = 0.05

EPSILON = 0

torch.manual_seed(10)
random.seed(10)
np.random.seed(10)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

env = env()
n_actions = env.n_action_space
n_observations = env.n_observation_space

# Creating 2 agents
agent_1 = DQNAgent(LEARNING_RATE, GAMMA, EPSILON, MEMORY_CAPACITY, BATCH_SIZE, n_observations, n_actions, device=device, num_actions = n_actions)
agent_2 = DQNAgent(LEARNING_RATE, GAMMA, EPSILON, MEMORY_CAPACITY, BATCH_SIZE, n_observations, n_actions, device=device, num_actions = n_actions)

# agent_1.policy_network.load_state_dict(torch.load('best_agent_1'))
# agent_2.policy_network.load_state_dict(torch.load('best_agent_2'))

agent_1.policy_network.load_state_dict(torch.load('recent_agent_1'))
agent_2.policy_network.load_state_dict(torch.load('recent_agent_2'))


done = False

state = env.reset(display=True)
state = state.float().to(device).view(1, n_observations)

for j in count():
    action_1 = agent_1.policy_network(state).max(-1)[1].view(1, 1)
    action_2 = agent_2.policy_network(state).max(-1)[1].view(1, 1)

    next_state, r1, r2, done = env.step(action_1, action_2)

    if next_state is not None:
        next_state = next_state.float().to(device).view(1, n_observations)

    if done:
        break

    state = next_state
