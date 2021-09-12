from heuristic_comparisons.wasserstein_distance_testing import StatisticalDistanceTest
from utilities.data import CreateFictitiousScenario, generate_delta_array
from utilities.visuals import LineGraph, Animation
from data import response_times_prod, response_times_dummy
import random

SEEDS = [random.randint(152100, 1000001521654651) for _ in range(0, 1000)]


class SimulateFictitiousScenario:
    """

    """
    SEED = 65981

    def __init__(self, benchmark_scenario_id, baseline_scenario_id):

        self.benchmark_scenario_id = benchmark_scenario_id
        self.baseline_scenario_id = baseline_scenario_id

        self.image_export_folder = "C:\\temp\\change"
        self._computed_statistics = []

    def _create_scenario(self, percentage_of_data_set, delta) -> object:
        """

        :param percentage_of_data_set:
        :param delta: The amount
        :return:
        """
        random.seed(self.SEED)
        return CreateFictitiousScenario(
            percentage=percentage_of_data_set,
            delta=delta,
            baseline_scenario_id=self.baseline_scenario_id,
            benchmark_scenario_id=self.benchmark_scenario_id
        )

    def _execute_statistical_distance_test(self, percentage_of_data_set, delta) -> object:
        """

        :param percentage_of_data_set:
        :param delta:
        :return:
        """
        scenario = self._create_scenario(
            percentage_of_data_set=percentage_of_data_set,
            delta=delta
        )
        return StatisticalDistanceTest(
            population_a=scenario.baseline_y,
            population_b=scenario.benchmark_y
        )

    def _generate_line_graph(self, statistical_distance_test: object, delta):
        """

        :return:
        """
        graph = LineGraph(
            baseline=statistical_distance_test.sample_a,
            benchmark=statistical_distance_test.sample_b,
            wasserstein_distance=statistical_distance_test.wasserstein_distance,
            kolmogorov_smirnov_distance=statistical_distance_test.kolmogorov_smirnov_distance,
            rank=statistical_distance_test.rank,
            change=delta
        )
        return graph

    def _simulate_scenario(self, percentage_of_data_set, delta, c_id, save_image=False, show_image=False) -> None:
        """

        :param percentage_of_data_set:
        :param delta:
        :param c_id:
        :param save_image:
        :param show_image:
        :return:
        """
        statistical_distance_test = self._execute_statistical_distance_test(
            percentage_of_data_set=percentage_of_data_set,
            delta=delta
        )
        statistics = {
                "percentage_of_data_set": percentage_of_data_set,
                "delta": delta,
                "kolmogorov_smirnov_distance": statistical_distance_test.kolmogorov_smirnov_distance,
                "kolmogorov_smirnov_probability": statistical_distance_test.kolmogorov_smirnov_probability,
                "wasserstein_distance": statistical_distance_test.wasserstein_distance,
                "score": statistical_distance_test.score,
                "rank": statistical_distance_test.rank,
                "sample_size": statistical_distance_test.sample_size,
            }
        self._computed_statistics.append(statistics)
        print(statistics)  # <-- Log to the terminal

        graph = self._generate_line_graph(statistical_distance_test, delta)
        if save_image:
            graph.save_frame(self.image_export_folder, filename=f"{delta}_{c_id}__")

        elif show_image:
            graph.show()

        else:
            del graph

    def consistently_increase_and_decrease_benchmark(self, percentage_of_data_set, save_image, show_image, repeats=0):
        """

        :return:
        """
        delta_array = []
        delta = 0
        while delta <= 99:
            delta_array.append(round(delta, 3))
            delta = delta + 1

        for random_amount_of_increase in delta_array:
            repeats = 1 if repeats == 0 else repeats
            for repeat_id in range(0, repeats):
                self._simulate_scenario(
                    percentage_of_data_set=percentage_of_data_set,
                    delta=random_amount_of_increase,
                    c_id=repeat_id,
                    save_image=save_image,
                    show_image=show_image
                )


def verify_against_real_world_data_prod():
    print("real world data")

    sample_order = [
        {"data": ["RID-1", "RID-2"]},
        {"data": ["RID-2", "RID-3"]},
        {"data": ["RID-3", "RID-4"]},
        {"data": ["RID-4", "RID-5"]},
        {"data": ["RID-5", "RID-6"]},
        {"data": ["RID-1", "RID-6"]},
        {"data": ["RID-1", "RID-1"]},
    ]

    for samples in sample_order:
        print("----------------------------")
        print(samples["data"])
        distance_test = StatisticalDistanceTest(
            population_a=response_times_prod[samples["data"][0]]["response_times"],
            population_b=response_times_prod[samples["data"][1]]["response_times"]
        )
        print(
            f"ks-d {distance_test._ks_d_value} -- ws {distance_test._ws_d_value} -- Rank: {distance_test.rank} -- Score: {distance_test.score}")

        print("----------------------------")


def verify_against_real_world_data_dummy():
    print("real world data")

    sample_order = [
        {"data": ["RID-0", "RID-1"]},
        {"data": ["RID-1", "RID-2"]},
        {"data": ["RID-2", "RID-3"]},
        {"data": ["RID-3", "RID-4"]},
    ]

    for samples in sample_order:
        print("----------------------------")
        print(samples["data"])
        distance_test = StatisticalDistanceTest(
            population_a=response_times_dummy[samples["data"][0]]["response_times"],
            population_b=response_times_dummy[samples["data"][1]]["response_times"]
        )
        print(
            f"-- ks-d {distance_test._ks_d_value} -- ws {distance_test._ws_d_value} -- Rank: {distance_test.rank} -- Score: {distance_test.score}")
        print("----------------------------")


scenario = SimulateFictitiousScenario(
    baseline_scenario_id="RID-3",
    benchmark_scenario_id="RID-4"
)
scenario.consistently_increase_and_decrease_benchmark(
    percentage_of_data_set=100,
    save_image=False,
    show_image=False,
    repeats=0
)
