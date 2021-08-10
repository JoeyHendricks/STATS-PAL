from regression import PercentileHypothesisTest
from utils import CreateFictitiousScenario
import matplotlib.pyplot as plt
import numpy as np
import unittest


HUMAN_OBSERVER = True


class TestPercentileHypothesisTest(unittest.TestCase):

    @staticmethod
    def _show_scatter_plot(scenario) -> None:
        """
        Shows the scatter plot containing the baseline and benchmark
        to verify the runs results.
        :param scenario: the run that needs to be visualized
        """
        x = np.array(scenario.x_axis)
        y = np.array(scenario.baseline_measurements)
        plt.scatter(x, y)

        x = np.array(scenario.x_axis)
        y = np.array(scenario.benchmark_measurements)
        plt.scatter(x, y)

        plt.show()

    def test_hypothesis_test_under_continuously_increasing_benchmark(self) -> None:
        """
        Will verify the hypothesis test with a constantly decreasing slower benchmark run.
        Expected result is that every increment will comeback as false.
        """
        for increment in range(4, 100):
            scenario = CreateFictitiousScenario()
            scenario.benchmark_percentage_increased = {"start": 2, "end": increment}

            hypothesis = PercentileHypothesisTest(
                group_a=scenario.baseline_measurements,
                group_b=scenario.benchmark_measurements
            )
            self.assertFalse(hypothesis.test())
            if HUMAN_OBSERVER is True:
                self._show_scatter_plot(scenario)

    def test_hypothesis_test_under_continuously_decreasing_benchmark(self) -> None:
        """
        Will verify the hypothesis test with a constantly decreasing faster benchmark run.
        Expected result is that every increment will comeback as false.
        """
        for increment in range(4, 100):
            scenario = CreateFictitiousScenario()
            scenario.benchmark_percentage_decreased = {"start": 2, "end": increment}

            hypothesis = PercentileHypothesisTest(
                group_a=scenario.baseline_measurements,
                group_b=scenario.benchmark_measurements
            )
            results = hypothesis.test()
            self.assertFalse(results)
            print(results)
            if HUMAN_OBSERVER is True:
                self._show_scatter_plot(scenario)

    def test_hypothesis_test_with_a_constant_benchmark(self) -> None:
        """
        will test the hypothesis test with a benchmark
        that has acceptable levels of change.
        """
        change = [{"start": 0, "end": 1}, {"start": 0, "end": 2}]

        for increment in change:
            scenario = CreateFictitiousScenario()
            scenario.benchmark_percentage_increased = increment

            hypothesis = PercentileHypothesisTest(
                group_a=scenario.baseline_measurements,
                group_b=scenario.benchmark_measurements
            )
            self.assertTrue(hypothesis.test())
            if HUMAN_OBSERVER is True:
                self._show_scatter_plot(scenario)






