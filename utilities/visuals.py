import matplotlib.pyplot as plt
import numpy as np


def show_scatter_plot(baseline_x_axis: list, baseline_y_axis: list,
                      benchmark_x_axis: list, benchmark_y_axis: list,
                      rank, distance, delta) -> None:
    """
    Shows the scatter plot containing the baseline and benchmark
    to verify the runs results.
    """

    # benchmark
    plt.figure(figsize=(10.0, 6.0))  # in inches!
    ax1 = plt.subplot(1, 2, 2)
    x = np.array(benchmark_x_axis)
    y = np.array(benchmark_y_axis)
    ax1.scatter(x, y, s=6, color='orange')

    # baseline
    ax2 = plt.subplot(1, 2, 1, sharey=ax1)
    x = np.array(baseline_x_axis)
    y = np.array(baseline_y_axis)
    ax2.scatter(x, y, s=6, color='blue')
    plt.figtext(
        0.5,
        0.01,
        f"Estimated rank: {rank} - % change introduced: {delta} - Calculated KS Distance: {round(distance, 4)}",
        ha="center",
        fontsize=15
    )
    plt.savefig(f'C:\\temp\\change\\frame_{delta}.png', dpi=100)
    plt.clf()
