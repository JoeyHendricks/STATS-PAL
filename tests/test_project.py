from heuristics.kolmogorov_smirnov_and_wasserstein import StatisticalDistanceTest
from data import location_hendricks_set_001
from data.wranglers import ConvertCsvResultsIntoDictionary
from QuickPotato import performance_test as pt
from QuickPotato.statistical.visualizations import BarChart, FlameGraph
import unittest


SHOW_FLAME_GRAPH = False
SHOW_BAR_GRAPH = False


class TestHeuristic(unittest.TestCase):

    def setUp(self) -> None:
        """
        Will structure the raw data object used in the tests.
        """
        self.raw_data = ConvertCsvResultsIntoDictionary(location_hendricks_set_001).data

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

    def test_performance_of_heuristic(self) -> None:
        """
        A simple code performance test which allows me to access complex
        code performance visualizations and test if my heuristic follows
        basic performance requirements.
        :return:
        """
        pt.test_case_name = "performance-test-heuristic"

        def profiler_starting_point() -> None:
            """
            Complex classes can confuse QuickPotato and make it hard to find a starting point
            from where QuickPotato can start unwrapping your code. By encapsulating the code
            we want to test in a simple function QuickPotato can make sense of the data better.

            This function acts as wrapper or starting point for QuickPotato.
            """
            StatisticalDistanceTest(self.raw_data["RID-1"]["response_times"], self.raw_data["RID-2"]["response_times"])

        pt.measure_method_performance(
            method=profiler_starting_point,
            arguments=[],
            iteration=10,
            pacing=0
        )

        if SHOW_BAR_GRAPH:
            BarChart(pt.test_case_name, test_ids=[pt.current_test_id, pt.previous_test_id]).export("C:\\temp\\")

        if SHOW_FLAME_GRAPH:
            FlameGraph(pt.test_case_name, test_id=pt.current_test_id).export("C:\\temp\\")

        pt.max_and_min_boundary_for_average = {"max": 0.020, "min": 0.005}

        # verify if my heuristic meets my basic performance requirements.
        self.assertTrue(pt.verify_benchmark_against_set_boundaries())

