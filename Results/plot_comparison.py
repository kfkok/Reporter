import os
import pickle
import numpy as np
from reporter_tool.reporter import Reporter

"""
Plots a mean with standard deviation graph for both rewards and cummulative rewards for each model for comparison.

This script will loop through each model directory and its repeat directories to collect all files named episode_reward.pkl 
These files are dumped by the Reporter for each repeat after running demo.py
Tt contains all the episode rewards for that repeat
"""

model_rewards = {}
cummulative_model_rewards = {}

for model in os.listdir():
    if not os.path.isdir(model):
        continue

    model_rewards[model] = []
    cummulative_model_rewards[model] = []

    for repeat in os.listdir(model):
        for episode_file in os.listdir(os.path.join(model, repeat)):
            if episode_file == "episode_reward.pkl":
                with open(os.path.join(model, repeat, episode_file), 'rb') as handle:
                    episode_reward = pickle.load(handle)
                    # print(episode_reward)
                    model_rewards[model].append(episode_reward)

    cummulative_model_rewards[model] = np.array(model_rewards[model]).cumsum(axis=1)

Reporter.save_plot_comparison("comparison.png", model_rewards, "rewards", "episodes", "rewards")
Reporter.save_plot_comparison("cumulative comparison.png", cummulative_model_rewards, "cumulative rewards", "episodes", "rewards")













