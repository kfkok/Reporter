import numpy as np

from reporter_tool.reporter import Reporter
import random

# Set the directory
Reporter.create_results_directory('Results')

# Setup a report to collect external reward data
Reporter.setup("ext_reward", "time step", type=Reporter.Type.PLOT)

# Collect some external rewards
Reporter.append("ext_reward", random.random())
Reporter.append("ext_reward", random.random())
Reporter.append("ext_reward", random.random())
Reporter.append("ext_reward", random.random())
Reporter.append("ext_reward", random.random())

# Plot the external rewards graph
Reporter.save_figure("ext_reward.png", "ext_reward")

# Setup a report to collect intrinsic reward data
Reporter.setup("int_reward", "time step", type=Reporter.Type.PLOT)

# Collect some external rewards
Reporter.append("int_reward", random.random())
Reporter.append("int_reward", random.random())
Reporter.append("int_reward", random.random())
Reporter.append("int_reward", random.random())
Reporter.append("int_reward", random.random())

# Plot the external rewards and intrinsic rewards on separate graph of same figure
Reporter.save_figure("rewards.png", "ext_reward", "int_reward")

# Plot the external rewards and intrinsic rewards on same graph
Reporter.save_figure("multiplots.png", [["ext_reward", "int_reward"], "time step", "rewards"])

method_1_results = np.array(
                    [[0.3, 0.22, 0.6, 0.8, 0.62],
                    [0.59, 0.3, 0.5, 0.3, 0.12],
                    [0.34, 0.6, 0.77, 0.12, 0.82]])

method_2_results = method_1_results + np.random.random((3, 5)) - 0.11

all_method_results = {"method_1": method_1_results, "method_2": method_2_results}

Reporter.save_plot_comparison(file="comparison.png", plots=all_method_results, title="Comparison", xlabel="x", ylabel="y")