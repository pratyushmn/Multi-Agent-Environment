from DQN import DQNAgent 
from game import SoccerGame as env
import torch
import numpy as np
import random
from itertools import count
import time

BATCH_SIZE = 128
DIVERSIFY_MEMORY = 0.25
MEMORY_CAPACITY = 8500

GAMMA = 0.75
LEARNING_RATE = 0.05

EPSILON = 0.9

# Setting up GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# Setting up random seeds
torch.manual_seed(10)
random.seed(10)
np.random.seed(10)

# Setting up environment
env = env()
n_actions = env.n_action_space
n_observations = env.n_observation_space

# Creating 2 agents
agent_1 = DQNAgent(LEARNING_RATE, GAMMA, EPSILON, MEMORY_CAPACITY, BATCH_SIZE, n_observations, n_actions, device=device, num_actions = n_actions)
agent_2 = DQNAgent(LEARNING_RATE, GAMMA, EPSILON, MEMORY_CAPACITY, BATCH_SIZE, n_observations, n_actions, device=device, num_actions = n_actions)

max_reward_1 = 0
max_reward_2 = 0

for i in count():
    print("Episode {} started.".format(i + 1))
    total_reward_1 = 0
    total_reward_2 = 0
    done = False

    state = env.reset()
    state = state.float().to(device).view(1, n_observations)

    for j in count():
        action_1 = agent_1.select_action(state, j)
        action_2 = agent_2.select_action(state, j)

        next_state, r1, r2, done = env.step(action_1, action_2)

        if next_state is not None:
            next_state = next_state.float().to(device).view(1, n_observations)

        total_reward_1 += r1
        total_reward_2 += r2

        agent_1.mem.push(state, action_1, next_state, r1.to(device).view(1,1))
        agent_2.mem.push(state, action_2, next_state, r2.to(device).view(1,1))

        state = next_state

        if j%2 == 0:
            agent_1.optimize_model()
            agent_2.optimize_model()

        if j % 10000 == 0:
            print("Episode: {}, Step: {}, R1: {}, R2: {}, A1: {}, A2: {}".format(i+1, j, total_reward_1, total_reward_2, action_1, action_2))

        if done:
            break

    agent_1.target_network.load_state_dict(agent_1.policy_network.state_dict())
    agent_2.target_network.load_state_dict(agent_2.policy_network.state_dict())

    total_reward_1 /= j
    total_reward_2 /= j

    if total_reward_1 > max_reward_1:
        print("Best Agent 1 reward: {}".format(total_reward_1))
        torch.save(agent_1.policy_network.state_dict(), "best_agent_1")
        max_reward_1 = total_reward_1

    if total_reward_2 > max_reward_2:
        print("Best Agent 2 reward: {}".format(total_reward_2))
        torch.save(agent_2.policy_network.state_dict(), "best_agent_2")
        max_reward_2 = total_reward_2

    torch.save(agent_1.policy_network.state_dict(), "recent_agent_1")
    torch.save(agent_2.policy_network.state_dict(), "recent_agent_2")
    
    






