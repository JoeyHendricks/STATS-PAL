from heuristic_comparisons.distance_testing import DistanceTest
from heuristic_comparisons.divergence_testing import DivergenceTest
from utilities.data import CreateFictitiousScenario
from data import response_times_acc
import random

SEEDS = [random.randint(152100, 1000001521654651) for _ in range(0, 1000)]


def consistently_increase_and_decrease_benchmark(seed=21021995):
    """

    :return:
    """
    for delta in range(0, 150):
        random.seed(seed)
        scenario_increased = CreateFictitiousScenario(increase=delta)
        scenario_decreased = CreateFictitiousScenario(decrease=delta)
        d_test_increased = DistanceTest(
            population_a=scenario_increased.baseline_y,
            population_b=scenario_increased.benchmark_y
        )
        d_test_decreased = DistanceTest(
            population_a=scenario_decreased.baseline_y,
            population_b=scenario_decreased.benchmark_y
        )

        rank = d_test_increased.rank
        score = d_test_increased.score
        distance = d_test_increased.d_value
        print(f"rank: {rank} - score: {score} - distance: {distance} - delta: {delta}")


def verify_against_real_world_data():
    print("real world data")

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
        x = DistanceTest(
            population_a=response_times_acc[samples["data"][0]]["response_times"],
            population_b=response_times_acc[samples["data"][1]]["response_times"]
        )
        rank = x.rank
        score = x.score
        distance = x.d_value
        print(f"rank: {rank} - score: {score} - distance: {distance}")
        print("----------------------------")




#consistently_increase_and_decrease_benchmark()
verify_against_real_world_data()

"""
A
B
C
D
E
F
"""