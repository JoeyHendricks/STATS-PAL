from deterministic_algorithms.students_t_test import TTest
from utilities.generator import CreateFictitiousScenario
from data import real_world_raw_performance_test_data
import matplotlib.pyplot as plt
import numpy as np
import unittest


HUMAN_OBSERVER = False


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


class TestAgainstRandomData(unittest.TestCase):

    def test_hypothesis_test_under_continuously_increasing_benchmark(self) -> None:
        """
        Will verify the hypothesis test with a constantly decreasing slower benchmark run.
        Expected result is that every increment will comeback as false.
        """
        for increment in range(4, 100):
            scenario = CreateFictitiousScenario()
            scenario.benchmark_percentage_increased = {"start": 2, "end": increment}
            hypothesis = TTest(
                baseline_measurements=scenario.baseline_measurements,
                benchmark_measurements=scenario.benchmark_measurements
            )
            if HUMAN_OBSERVER is True:
                show_scatter_plot(
                    baseline_x_axis=scenario.x_axis,
                    baseline_y_axis=scenario.baseline_measurements,
                    benchmark_x_axis=scenario.x_axis,
                    benchmark_y_axis=scenario.benchmark_measurements
                )
            self.assertFalse(hypothesis.results)

    def test_hypothesis_test_under_continuously_decreasing_benchmark(self) -> None:
        """
        Will verify the hypothesis test with a constantly decreasing faster benchmark run.
        Expected result is that every increment will comeback as false.
        """
        for increment in range(4, 100):
            scenario = CreateFictitiousScenario()
            scenario.benchmark_percentage_decreased = {"start": 2, "end": increment}
            hypothesis = TTest(
                baseline_measurements=scenario.baseline_measurements,
                benchmark_measurements=scenario.benchmark_measurements
            )
            if HUMAN_OBSERVER is True:
                show_scatter_plot(
                    baseline_x_axis=scenario.x_axis,
                    baseline_y_axis=scenario.baseline_measurements,
                    benchmark_x_axis=scenario.x_axis,
                    benchmark_y_axis=scenario.benchmark_measurements
                )
            self.assertFalse(hypothesis.results)

    def test_hypothesis_test_with_a_constant_benchmark(self) -> None:
        """
        will test the hypothesis test with a benchmark
        that has acceptable levels of change.
        """
        change = [{"start": 0, "end": 1}, {"start": 0, "end": 2}]

        for increment in change:
            scenario = CreateFictitiousScenario()
            scenario.benchmark_percentage_increased = increment
            hypothesis = TTest(
                baseline_measurements=scenario.baseline_measurements,
                benchmark_measurements=scenario.benchmark_measurements
            )
            if HUMAN_OBSERVER is True:
                show_scatter_plot(
                    baseline_x_axis=scenario.x_axis,
                    baseline_y_axis=scenario.baseline_measurements,
                    benchmark_x_axis=scenario.x_axis,
                    benchmark_y_axis=scenario.benchmark_measurements
                )
            self.assertTrue(hypothesis.results)


class TestAgainstRealWordData(unittest.TestCase):

    def test_hypothesis_test_benchmark_is_slower_than_baseline(self) -> None:
        """

        :return:
        """
        scenario = {
            "baseline": real_world_raw_performance_test_data["RID-1"],
            "benchmark": real_world_raw_performance_test_data["RID-2"]
        }
        hypothesis = TTest(
            baseline_measurements=scenario["baseline"]["response_times"],
            benchmark_measurements=scenario["benchmark"]["response_times"]
        )
        if HUMAN_OBSERVER is True:
            show_scatter_plot(
                baseline_x_axis=scenario["baseline"]["timestamps"],
                baseline_y_axis=scenario["baseline"]["response_times"],
                benchmark_x_axis=scenario["benchmark"]["timestamps"],
                benchmark_y_axis=scenario["benchmark"]["response_times"]
            )
        self.assertFalse(hypothesis.results)

    def test_hypothesis_test_benchmark_is_faster_than_baseline(self) -> None:
        """

        :return:
        """
        scenario = {
            "baseline": real_world_raw_performance_test_data["RID-2"],
            "benchmark": real_world_raw_performance_test_data["RID-3"]
        }
        hypothesis = TTest(
            baseline_measurements=scenario["baseline"]["response_times"],
            benchmark_measurements=scenario["benchmark"]["response_times"]
        )
        if HUMAN_OBSERVER is True:
            show_scatter_plot(
                baseline_x_axis=scenario["baseline"]["timestamps"],
                baseline_y_axis=scenario["baseline"]["response_times"],
                benchmark_x_axis=scenario["benchmark"]["timestamps"],
                benchmark_y_axis=scenario["benchmark"]["response_times"]
            )
        self.assertFalse(hypothesis.results)

    def test_hypothesis_test_benchmark_is_not_different_from_baseline(self) -> None:
        """

        :return:
        """
        scenario = {
            "baseline": real_world_raw_performance_test_data["RID-3"],
            "benchmark": real_world_raw_performance_test_data["RID-4"]
        }
        hypothesis = TTest(
            baseline_measurements=scenario["baseline"]["response_times"],
            benchmark_measurements=scenario["benchmark"]["response_times"]
        )
        if HUMAN_OBSERVER is True:
            show_scatter_plot(
                baseline_x_axis=scenario["baseline"]["timestamps"],
                baseline_y_axis=scenario["baseline"]["response_times"],
                benchmark_x_axis=scenario["benchmark"]["timestamps"],
                benchmark_y_axis=scenario["benchmark"]["response_times"]
            )
        self.assertTrue(hypothesis.results)
