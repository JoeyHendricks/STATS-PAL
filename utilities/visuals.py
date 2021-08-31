import matplotlib.pyplot as plt
import numpy as np


def show_scatter_plot(baseline_x_axis: list, baseline_y_axis: list,
                      benchmark_x_axis: list, benchmark_y_axis: list) -> None:
    """
    Shows the scatter plot containing the baseline and benchmark
    to verify the runs results.
    """
    x = np.array(baseline_x_axis)
    y = np.array(baseline_y_axis)
    plt.scatter(x, y)

    x = np.array(benchmark_x_axis)
    y = np.array(benchmark_y_axis)
    plt.scatter(x, y)

    plt.show()
