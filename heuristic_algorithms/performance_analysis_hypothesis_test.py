import numpy as np
from math import log2


class DivergenceTest:
    """
    A equivalence test to determine how much regression there
    is between sample A and B.

    To determine how much regression is to much this class uses boundaries
    defined around the Kullback–Leibler divergence. To asses if the change
    between 2 samples is within the acceptable ranges of normalcy.

    The core idea behind this algorithm is to find how much regression
    there is between two sample not to define if that is good or bad.
    Yet this test is equipped with some general boundaries and guidelines
    that will hopefully be useful for most use-cases.

    As this entire is algorithm an heuristic it is key that if the standard
    are insufficient for your use-case that you define your own that work
    better in your context.
    """
    # Raw data will be structured into a exponential curve.
    DISTRIBUTION = [

        [5, 6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
        [26, 27, 28, 29, 30],
        [31, 32, 33, 34, 35],
        [36, 37, 38, 39, 40],
        [41, 42, 43, 44, 45],
        [46, 47, 48, 49, 50],
        [51, 52, 53, 54, 55],
        [56, 57, 58, 59, 60],
        [61, 62, 63, 64, 65],
        [66, 67, 68, 69, 70],
        [71, 72, 73, 74, 75],
        [76, 77, 78, 79, 80],
        [81, 82, 83, 84, 85],
        [86, 87, 88, 89, 90],
        [91, 92, 93, 94, 95],

    ]
    # The letter grades and there literal critical values (Allows up to 30% regression).
    LETTER_RANKS = [

        {"boundary": 2.50, "letter": "S"},  # < ± 1% regression
        {"boundary": 6.00, "letter": "A"},  # ± 1 to 5% regression
        {"boundary": 8.00, "letter": "B"},  # ± 5 to 8% regression
        {"boundary": 15.0, "letter": "C"},  # ± 8 to 10% regression
        {"boundary": 20.0, "letter": "D"},  # ± 10 to 17% regression
        {"boundary": 25.0, "letter": "E"},  # ± 17 to 25% regression
        {"boundary": 30.0, "letter": "F"},  # > ± 25% regression

    ]
    # Used to score the c-value from 0 to 100 (Values smaller then 0.100 are considered insignificant.)
    SCORING_MATRIX = [

        {"boundary": 0.100, "punishment": 0.00210437},
        {"boundary": 0.125, "punishment": 0.00217105},
        {"boundary": 0.150, "punishment": 0.00787242},
        {"boundary": 0.175, "punishment": 0.00791472},
        {"boundary": 0.200, "punishment": 0.00814541},
        {"boundary": 0.225, "punishment": 0.00884361},
        {"boundary": 0.250, "punishment": 0.00907313},
        {"boundary": 0.275, "punishment": 0.01296521},
        {"boundary": 0.300, "punishment": 0.01383224},
        {"boundary": 0.325, "punishment": 0.01443168},
        {"boundary": 0.350, "punishment": 0.01624729},
        {"boundary": 0.375, "punishment": 0.01760769},
        {"boundary": 0.400, "punishment": 0.01886994},
        {"boundary": 0.425, "punishment": 0.02218302},
        {"boundary": 0.450, "punishment": 0.02376578},
        {"boundary": 0.475, "punishment": 0.02734606},
        {"boundary": 0.500, "punishment": 0.03823586},
        {"boundary": 0.525, "punishment": 0.03894435},
        {"boundary": 0.550, "punishment": 0.04147971},
        {"boundary": 0.575, "punishment": 0.04562214},
        {"boundary": 0.600, "punishment": 0.04700291},
        {"boundary": 0.625, "punishment": 0.04833569},
        {"boundary": 0.650, "punishment": 0.06287215},
        {"boundary": 0.675, "punishment": 0.06680662},
        {"boundary": 0.700, "punishment": 0.07658837},
        {"boundary": 0.725, "punishment": 0.08191112},
        {"boundary": 0.750, "punishment": 0.08290606},
        {"boundary": 0.775, "punishment": 0.15592140},

    ]

    def __init__(self, group_a: list, group_b: list) -> None:
        """
        Will construct the class and calculate all the required statistics.

        :param group_a: An list of floats of the A population (baseline).
        :param group_b: An list of floats of the B population (benchmark).
        """
        self.group_a = self.bin_into_percentiles_ranges(group_a)
        self.group_b = self.bin_into_percentiles_ranges(group_b)
        self.c_value, self.absolute_change = self._estimate_c_value()
        self.grade = self._letter_rank_c_value()
        self.score = self._score_c_value_from_0_to_100()

    def bin_into_percentiles_ranges(self, data: list) -> list:
        """
        Will calculate the required percentile range for each slice of data.
        :return: An array containing the calculated percentiles.
        """
        percentile_ranges = []
        for belt in self.DISTRIBUTION:
            group = []
            for percentile in belt:
                group.append(self._calculate_percentile(data, percentile))
            percentile_ranges.append(group)

        return percentile_ranges

    @staticmethod
    def _calculate_percentile(array: list, percentile: int) -> float:
        """
        Used to calculate the percentile over the given array.
        :return: the requested percentile as a float
        """
        return float(np.percentile(array, percentile))

    @staticmethod
    def _calculate_kl_divergence(p: list, q: list) -> float:
        """
        the Kullback–Leibler divergence is used to represent a measure of
        distance between a percentile range from A to B.
        More info about the equation can be found here:

        https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence

        :param p: The true distribution (Baseline)
        :param q: Is the approximate distribution Q (Benchmark)
        :return: The estimated distance from P to Q
        :except: ValueError or ZeroDivisionError: When a negative number is inside the
        log function or a zero value, a forced output of 100 will be given to represent
        the large change.
        """
        try:
            return sum(p[i] * log2(p[i] / q[i]) for i in range(len(p)))

        except (ValueError, ZeroDivisionError):
            # Possible negative number inside log function or a zero value -
            # this is only possible at extreme differences on the negative axis.
            return 100

    def _estimate_c_value(self) -> tuple:
        """
        Will estimate the change value from A to B using the
        Kullback–Leibler divergence.

        This value can be considered as the absolute distance between
        2 probability distributions representing 2 raw data sets.
        This value can then be interpret in a number of way like
        the following features this class supports:

        - Letter rank the c-value from S to F.
        - Score the c-value from 0 - 100.

        :return: A float which represent the change from A to B
        and a list of change per percentile range
        """
        divergence_per_percentile_range = []
        for A, B in zip(self.group_a, self.group_b):
            divergence_per_percentile_range.append(
                abs(self._calculate_kl_divergence(A, B))
            )
        c = sum(divergence_per_percentile_range) + np.std(divergence_per_percentile_range)
        return c, divergence_per_percentile_range

    def _letter_rank_c_value(self) -> str:
        """
        Will give the letter grade to the C value score.
        Below a rough estimate how much regression in
        percentage each letter grade represents:

        Do keep in mind that these values are based
        on randomly generated test data on one seed.
        These values are a rough estimate and you
        very well could need to tweak these to your context
        to get a better estimate.

        :return: The letter rank in the form as string ranging from S to F
        """
        for grade in self.LETTER_RANKS:
            if self.c_value < grade["boundary"]:
                return grade["letter"]
            else:
                continue
        return "F"

    def _score_c_value_from_0_to_100(self) -> float:
        """
        Will use a change matrix to score every
        Kullback–Leibler divergence statistics
        grading it from 0 to 1.

        :return: returns a float representing the
        change in a logical score.
        """
        scored_ranges = []
        for change in self.absolute_change:
            score = 1
            for row in self.SCORING_MATRIX:
                if change > row["boundary"]:
                    score -= row["punishment"]
                else:
                    continue
            scored_ranges.append(score)
        return round(sum(scored_ranges) / len(scored_ranges) * 100, 2)

