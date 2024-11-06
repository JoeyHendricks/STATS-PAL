from heuristics.kolmogorov_smirnov_and_wasserstein import StatisticalDistance
from data.wranglers import CreateFictitiousScenario, ConvertCsvResultsIntoDictionary
from data.visuals import LineGraph, ScatterPlot
import random


class SimulateScenario:
    """
    Creates a simulated scenario based on real scenario from my
    test data.
    """
    SEED = 65981

    def __init__(self, data_set_location, heuristics_boundaries, benchmark_id=None, baseline_id=None):
        """
        Will construct the simulation object and provide a few attributes
        which can be changed.

        :param benchmark_id: The RID that needs the benchmark
        :param baseline_id:  The RID that need to be baseline
        :param data_set_location:  The data set that is used as a starting point.
        """
        self.benchmark_scenario_id = benchmark_id
        self.baseline_scenario_id = baseline_id
        self.heuristics_boundaries = heuristics_boundaries

        self.data_set_location = data_set_location
        self.image_export_folder = "C:\\temp\\change"
        self._computed_statistics = []

    def _create_scenario(self, percent_of_data_set, delta, positive) -> CreateFictitiousScenario:
        """
        Will create a scenario based on the scenario information.
        :param percent_of_data_set: The amount in percentage of the
        data set that needs to be changed.
        :param delta: The amount of change.
        :param positive: True when the change the delta needs to increase on false delta will be used
        to decrease response time.
        :return: The scenario.
        """
        random.seed(self.SEED)
        return CreateFictitiousScenario(
            percentage=percent_of_data_set,
            delta=delta,
            positive=positive,
            baseline_id=self.baseline_scenario_id,
            benchmark_id=self.benchmark_scenario_id,
            data_set_location=self.data_set_location
        )

    def _run_distance_test_on_fictitious_scenario(self, scenario: CreateFictitiousScenario) -> StatisticalDistance:
        """
        Will compare the scenario using the distance test and returning the metrics.
        :param scenario: the simulated scenario containing all of the data
        :return: All of the statistics that have been computed.
        """
        return StatisticalDistance(
            baseline_ecdf=scenario.baseline_y,
            benchmark_ecdf=scenario.benchmark_y,
            heuristics_boundaries=self.heuristics_boundaries
        )

    @staticmethod
    def _generate_line_graph(distance_test: StatisticalDistance, delta):
        """
        Will generate a graph object which can be used to verify the results.
        :return: The plotly graph object/
        """
        return LineGraph(
            baseline=distance_test.sample_a,
            benchmark=distance_test.sample_b,
            wasserstein_distance=distance_test.wasserstein_distance,
            kolmogorov_smirnov_distance=distance_test.kolmogorov_smirnov_distance,
            rank=distance_test.letter_rank,
            score=distance_test.score,
            change=delta
        )

    @staticmethod
    def _generate_scatter_plot(scenario: object, statistical_distance_test: StatisticalDistance, delta: int):
        """
        Will generate a graph object which can be used to verify the results.
        :return: The plotly graph object.
        """
        return ScatterPlot(
            scenario=scenario,
            rank=statistical_distance_test.letter_rank,
            score=statistical_distance_test.score,
            change=delta
        )

    def _simulate_scenario(
            self,
            percent_of_data_set,
            delta,
            c_id,
            positive,
            image_type="line",
            save_image=False,
            show_image=False) -> None:
        """
        Will run a simulation.
        :param percent_of_data_set: The amount in percentage of the
        data set that needs to be changed.
        :param delta: The amount of change.
        :param c_id: an unique id that can be added to the file name
        to make sure that each file name is unique. (Normally only used when repeating testing)
        :param save_image: If you want to save the image.
        :param show_image: If you want to view the image in your browser
        :param positive: True when the change the delta needs to increase on false delta will be used
        to decrease response time.
        """
        scenario = self._create_scenario(
            percent_of_data_set=percent_of_data_set,
            delta=delta,
            positive=positive
        )
        statistical_distance_test = self._run_distance_test_on_fictitious_scenario(scenario)
        statistics = {
            "percentage_of_data_set": percent_of_data_set,
            "delta": delta,
            "kolmogorov_smirnov_distance": statistical_distance_test.kolmogorov_smirnov_distance,
            "kolmogorov_smirnov_probability": statistical_distance_test.kolmogorov_smirnov_probability,
            "wasserstein_distance": statistical_distance_test.wasserstein_distance,
            "score": statistical_distance_test.score,
            "rank": statistical_distance_test.letter_rank,
            "sample_size": len(scenario.baseline_y),
        }
        self._computed_statistics.append(statistics)
        print(statistics)  # <-- Log to the terminal

        ecdf_line_graph = self._generate_line_graph(statistical_distance_test, delta)
        raw_scatter_plot = self._generate_scatter_plot(scenario, statistical_distance_test, delta)

        if save_image and image_type == "line":
            ecdf_line_graph.save_frame(self.image_export_folder, filename=f"{delta}")

        elif save_image and image_type == "scatter":
            raw_scatter_plot.save_frame(self.image_export_folder, filename=f"{delta}")

        elif show_image and image_type == "line":
            ecdf_line_graph.show()

        elif show_image and image_type == "scatter":
            raw_scatter_plot.show()

        else:
            del ecdf_line_graph

    def run_consistently_changing_benchmark_fictitious_scenario(
            self,
            percent_of_data,
            save_image,
            positive,
            show_image,
            image_type="line",
            repeats=0) -> None:
        """
        A simulation where the benchmark is consistently randomly increased.
        This will generate an ever changing benchmark that can help us find the correct critical values.

        :param image_type:
        :param percent_of_data: The amount in percentage of the
        data set that needs to be changed.
        :param save_image: If you want to save the image
        :param show_image: If you want to view the image in your browser
        :param repeats: Amount of repeats per simulation. (each simulation randomly spreads
        the change over the data set. more repeats will give you more perspectives on how your data sets changes.)
        :param positive: True when the change the delta needs to increase on false delta will be used
        to decrease response time
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
                    percent_of_data_set=percent_of_data,
                    delta=random_amount_of_increase,
                    c_id=repeat_id,
                    save_image=save_image,
                    show_image=show_image,
                    image_type=image_type,
                    positive=positive
                )

    def run_original_scenario(self, order_of_comparison: list) -> None:
        """

        :return:
        """
        for simulation in order_of_comparison:
            instructions = simulation["instructions"]
            raw_data = ConvertCsvResultsIntoDictionary(self.data_set_location).data
            baseline_response_times = raw_data[instructions[0]]["response_times"]
            benchmark_response_times = raw_data[instructions[1]]["response_times"]

            statistical_distance_test = StatisticalDistance(
                baseline_ecdf=baseline_response_times,
                benchmark_ecdf=benchmark_response_times,
                heuristics_boundaries=self.heuristics_boundaries
            )
            statistics = {
                "baseline-runid": instructions[0],
                "benchmark-runid": instructions[1],
                "kolmogorov_smirnov_distance": statistical_distance_test.kolmogorov_smirnov_distance,
                "kolmogorov_smirnov_probability": statistical_distance_test.kolmogorov_smirnov_probability,
                "wasserstein_distance": statistical_distance_test.wasserstein_distance,
                "score": statistical_distance_test.score,
                "rank": statistical_distance_test.letter_rank,
                "sample_size": len(benchmark_response_times),
            }
            self._computed_statistics.append(statistics)
            print(statistics)  # <-- Log to the terminal
            ecdf_line_graph = self._generate_line_graph(statistical_distance_test, 0)
            """
            raw_scatter_plot = self._generate_scatter_plot(self._create_scenario(
                100, 0, True
            ), statistical_distance_test, 0)
            """
            ecdf_line_graph.show()
