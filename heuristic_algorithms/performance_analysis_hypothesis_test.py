import numpy as np
from math import log2


class DivergenceTest:
    """
    A percentile hypothesis test to find the difference in the behaviour of two populations.
    This hypothesis test is originally designed to pick up changes in measurement patterns.

    For this to work properly this test expects a large baseline and benchmark population.
    This is why this test works great for finding spotting difference in large performance test
    results sets in an automated way.

    Please share feedback and let me know if you encounter any type 1 or type 2 errors using this test.
    """
    # The change matrix

    # The percentile curve distribution
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

    LETTER_GRADES = [

        {"threshold": 2.50, "letter": "A"},
        {"threshold": 3.00, "letter": "B"},
        {"threshold": 4.00, "letter": "C"},
        {"threshold": 6.00, "letter": "D"},
        {"threshold": 8.00, "letter": "E"},
        {"threshold": 10.0, "letter": "F"},

    ]

    def __init__(self, group_a: list, group_b: list) -> None:
        """
        Will construct the class and calculate a list of percentiles for both group A and B.
        The list of percentiles used range from 5th to 95th.

        :param group_a: An list of floats of the A population (baseline).
        :param group_b: An list of floats of the B population (benchmark).
        """
        self.group_a = self.bin_into_percentiles_ranges(group_a)
        self.group_b = self.bin_into_percentiles_ranges(group_b)
        self.c_value, self.absolute_change = self._estimate_c_value()
        self.grade = self._letter_grade_comparison()

    def bin_into_percentiles_ranges(self, data):
        """

        :return:
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
        :return: a float number of the requested percentile
        """
        return float(np.percentile(array, percentile))

    @staticmethod
    def _calculate_kl_divergence(p, q):
        """

        :param p:
        :param q:
        :return:
        """
        return sum(p[i] * log2(p[i] / q[i]) for i in range(len(p)))

    def _estimate_c_value(self) -> tuple:
        """
        Will find out what the difference in percentage is between each percentile.
        It will than feed that percentage through a matrix to find out
        how much positive or negative change exists.

        After that the array of scores gets computed into a score taking the
        standard deviation in account. This is done to verify if the change is
        across all of the percentiles or just within certain areas.

        :return: A float which represent the probability value
        """
        divergence_per_percentile_range = []
        for A, B in zip(self.group_a, self.group_b):
            divergence_per_percentile_range.append(
                abs(self._calculate_kl_divergence(A, B))
            )
        c = sum(divergence_per_percentile_range) + np.std(divergence_per_percentile_range)
        return c, divergence_per_percentile_range

    def _letter_grade_comparison(self):
        """

        :return:
        """
        for grade in self.LETTER_GRADES:
            if self.c_value < grade["threshold"]:
                return grade["letter"]
            else:
                continue
        return "F"



print("real world data")
from data import response_times_prod

sample_order = [
    {"data": ["RID-1", "RID-2"]},
    {"data": ["RID-2", "RID-3"]},
    {"data": ["RID-3", "RID-4"]},
    {"data": ["RID-4", "RID-5"]},
    {"data": ["RID-5", "RID-6"]},
    {"data": ["RID-1", "RID-6"]},
]

for samples in sample_order:
    print("----------------------------")
    print(samples["data"])
    print(
        DivergenceTest(
            group_a=response_times_prod[samples["data"][0]]["response_times"],
            group_b=response_times_prod[samples["data"][1]]["response_times"]
        ).grade
    )
    print(
        DivergenceTest(
            group_a=response_times_prod[samples["data"][0]]["response_times"],
            group_b=response_times_prod[samples["data"][1]]["response_times"]
        ).c_value
    )

    print("----------------------------")
