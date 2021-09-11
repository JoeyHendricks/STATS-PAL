from heuristic_comparisons.wasserstein_distance_testing import StatisticalDistanceTest
from utilities.data import CreateFictitiousScenario, generate_delta_array
from utilities.visuals import LineGraph, Animation
from data import response_times_prod, response_times_dummy
import random

SEEDS = [random.randint(152100, 1000001521654651) for _ in range(0, 1000)]


def consistently_increase_and_decrease_benchmark(seed=65981):
    """

    :return:
    """
    scores = []
    percentage_increase = []
    for delta in generate_delta_array():
        #for foo in range(0, 10):
        random.seed(seed)
        scenario = CreateFictitiousScenario(percentage=100, delta=delta)
        distance_test = StatisticalDistanceTest(
            population_a=scenario.baseline_y,
            population_b=scenario.benchmark_y
        )
        scores.append(distance_test.wasserstein_d_value)
        percentage_increase.append(delta)
        print(f"{delta} -- ks-d {distance_test.ks_d_value} -- ws {distance_test.wasserstein_d_value} -- Rank: {distance_test.rank}")
        LineGraph(
            baseline=distance_test.sample_a,
            benchmark=distance_test.sample_b,
            wasserstein_distance=distance_test.wasserstein_d_value,
            kolmogorov_smirnov_distance=distance_test.ks_d_value,
            rank=distance_test.rank,
            change=delta
        ).save_frame(
            folder="C:\\temp\\change", filename=f"{delta}_"
        )

    Animation.render_frames_in_target_directory_to_gif(
        target_folder="C:\\temp\\change",
        export_folder="C:\\temp"
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
        print(f"{distance_test.wasserstein_d_value} - rank {distance_test.rank}")

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
        x = StatisticalDistanceTest(
            population_a=response_times_dummy[samples["data"][0]]["response_times"],
            population_b=response_times_dummy[samples["data"][1]]["response_times"]
        )
        rank = x.rank
        distance = x.d_value
        print(f"rank: {rank} - distance: {distance}")
        print("----------------------------")




#verify_against_real_world_data_prod()
print("++++++++++++expon+++++++++++++++")
consistently_increase_and_decrease_benchmark()
