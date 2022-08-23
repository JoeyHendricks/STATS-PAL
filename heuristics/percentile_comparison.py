# coding=utf-8
import numpy as np

# Silence Divided by zero warnings
np.seterr(divide='ignore')


class PercentileComparison:
    """

    -ToDo Create a percentage difference method.
    """

    GRID = {
        "positive_threshold": [20, 30, 50, 75, 90],
        "positive_punishment": [0.2, 0.4, 0.6, 0.8, 1],
        "negative_threshold": [-10, -15, -20, -25, -30],
        "negative_punishment": [0.2, 0.4, 0.6, 0.8, 1]
    }

    def __init__(self, benchmark_sample: list, baseline_sample: list) -> None:
        """
        Will set up th class and find the max edge of the score from which the distance
        will be calculated by determining the length of the baseline sample.
        :param benchmark_sample: A benchmark percentile distribution following
        an exponential distribution.
        :param baseline_sample: A baseline percentile distribution following
        an exponential distribution.
        """
        self.BENCHMARK_SAMPLE = benchmark_sample
        self.BASELINE_SAMPLE = baseline_sample
        self._score = len(baseline_sample)

    @property
    def score(self) -> float:
        """
        A score from 0 to 100 that represents the amount of change
        between two percentile distributions.
        :return: The classic distance score a a float
        """
        return self._calculate_percentile_distance_score()

    def _push_value_through_positive_change_matrix(self, value: float) -> None:
        """
        Will iterate a value trough the positive change grid and will
        punish the score when a threshold is broken.
        :param value: The percentage difference between the benchmark and the baseline.
        """
        for punishment, threshold in zip(self.GRID["positive_punishment"], self.GRID["positive_threshold"]):
            if value > threshold:
                self._score -= punishment
            else:
                continue

    def _push_value_through_negative_change_matrix(self, value: float) -> None:
        """
        Will iterate a value trough the negative change grid and will
        punish the score when a threshold is broken.
        :param value: The percentage difference between the benchmark and the baseline.
        """
        for punishment, threshold in zip(self.GRID["negative_punishment"], self.GRID["negative_threshold"]):
            if value < threshold:
                self._score -= punishment
            else:
                continue

    def _iterate_through_percentiles_and_calculate_difference(self) -> None:
        """
        Will go through each percentile measurement and calculate the percentage
        difference between them which it will push through its respectable
        change matrix.
        """
        for baseline_value, benchmark_value in zip(self.BASELINE_SAMPLE, self.BENCHMARK_SAMPLE):

            # Calculate percentage change
            change = round(calculate_percentage_change(old=baseline_value, new=benchmark_value), 2)

            # Score the amount of distance
            if change > 0:
                self._push_value_through_positive_change_matrix(value=change)

            elif change < 0:
                self._push_value_through_negative_change_matrix(value=change)

            else:
                continue

    def _calculate_percentile_distance_score(self) -> float:
        """
        Will calculate the distance score by looking at how many
        measurements exhausted its threshold.
        :return: The distance score
        """
        self._iterate_through_percentiles_and_calculate_difference()
        return abs(round(float(self._score) / float(len(self.BASELINE_SAMPLE)) * 100, 2))