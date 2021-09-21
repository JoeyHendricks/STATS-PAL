from heuristics.kolmogorov_smirnov_and_wasserstein import StatisticalDistanceTest
from data import file_location_hendricks_raw_data_set_001  # <-- My primary example data set.
from data.wranglers import ConvertCsvResultsIntoDictionary
import unittest


class TestHeuristic(unittest.TestCase):

    def setUp(self) -> None:
        """
        Will structure the raw data object used in the tests.
        """
        self.raw_data = ConvertCsvResultsIntoDictionary(file_location_hendricks_raw_data_set_001).data

    def test_metrics_if_the_correct_rank_can_be_estimated(self) -> None:
        """
        Verifying if it is possible to find the correct rank and distance metrics for one of my dummy runs.
        Be aware that distance metrics can move a bit but they will generally stay within
        the same categories.
        """
        # Run the distance test against the given data.
        stats_distance_test = StatisticalDistanceTest(
            population_a=self.raw_data["RID-1"]["response_times"],
            population_b=self.raw_data["RID-2"]["response_times"]
        )

        # Testing if correct values have been calculated
        self.assertEqual(stats_distance_test.kolmogorov_smirnov_distance, 0.108)
        self.assertEqual(stats_distance_test.wasserstein_distance, 0.11)
        self.assertEqual(stats_distance_test.score, 85.57)
        self.assertEqual(stats_distance_test.rank, "C")
