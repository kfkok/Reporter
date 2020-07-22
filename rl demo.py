import os
from reporter_tool.reporter import Reporter
import random

"""
A sample use case to record intrinsic reward, external reward, and unit activation for an reinforcement learning agent
"""

models = ["model A", "model B", "model C"]
repeats = 3
episodes = 10
time_steps_per_episode = 100

# Setup reports for variables of interest
Reporter.setup("int_reward", "time step", type=Reporter.Type.PLOT)
Reporter.setup("ext_reward", "time step", type=Reporter.Type.PLOT)
Reporter.setup("activation_count", "unit", type=Reporter.Type.COUNT)

for model in models:
    for repeat in range(repeats):
        # Create the result directory for this model
        Reporter.create_results_directory(os.path.join('Results', model, 'repeat_' + str(repeat) + '\\'))
        episode_reward = []

        for episode in range(episodes):
            total_rewards = 0
            
            for t in range(time_steps_per_episode):
                # Generate some random data for each report
                int_reward = random.random()
                ext_reward = random.random() - 0.3
                activated_unit = random.randint(0, 10)

                # Append these data for each report, this is the data recording/collecting step
                Reporter.append("int_reward", int_reward)
                Reporter.append("ext_reward", ext_reward)
                Reporter.append("activation_count", activated_unit)

                total_rewards += ext_reward

            # save the report figure for the episode
            # the first argument is the file name, typically set as episode N
            # for subsequent arguments, passing a single string report name (eg:"int_reward") will render a single plot for the report
            # passing a list such as [["int_reward", "ext_reward"], "time step", "rewards"] will render multiple plot
            # on the same graph. In the list, "time step" and "rewards" corresponds to x label and y label respectively
            Reporter.save_figure("episode " + str(episode), "int_reward", "ext_reward",
                                 [["int_reward", "ext_reward"], "time step", "rewards"],
                                 "activation_count")
            
            episode_reward.append(total_rewards)
            
            # clear the reports of interest, else they will accumulate
            Reporter.clear("int_reward", "ext_reward", "activation_count")

        # dump the episode reward list as pickle file, used for plot comparison later on
        Reporter.dump_variable("episode_reward", episode_reward)
