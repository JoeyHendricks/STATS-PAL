from heuristic_algorithms.performance_analysis_hypothesis_test import DivergenceTest
from utilities.helpers import CreateFictitiousScenario
from data import response_times_prod
import random

SEEDS = [random.randint(152100, 1000001521654651) for _ in range(0, 1000)]
"""
scores = []
for seed in SEEDS:
    random.seed(152100)  # <-- Used to make test runs consistent
    scenario = CreateFictitiousScenario(increase=1)
    c_value = DivergenceTest(
        group_a=scenario.baseline_y,
        group_b=scenario.benchmark_y
    ).c_value
    print(c_value)
    exit()
"""


def consistently_increase_or_decrease_benchmark(seed=2205):
    """

    :return:
    """
    for delta in range(0, 31):
        random.seed(seed)
        scenario_increased = CreateFictitiousScenario(increase=delta)
        scenario_decreased = CreateFictitiousScenario(decrease=delta)
        d_test_increased = DivergenceTest(
            group_a=scenario_increased.baseline_y,
            group_b=scenario_increased.benchmark_y
        )
        d_test_decreased = DivergenceTest(
            group_a=scenario_decreased.baseline_y,
            group_b=scenario_decreased.benchmark_y
        )

        c_value__increased = d_test_increased.c_value
        c_value__decreased = d_test_decreased.c_value
        letter_grade__increased = d_test_increased.grade
        letter_grade__decreased = d_test_decreased.grade
        absolute_change__increased = d_test_increased.absolute_change
        absolute_change__decreased = d_test_decreased.absolute_change

        print(f"{delta} -- {d_test_increased.score}")

        #print(f"{delta}; {c_value__increased}; {letter_grade__increased}; {absolute_change__increased}")
        #print(f"{delta}; {c_value__decreased}; {letter_grade__decreased}; {absolute_change__decreased}")


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
        print(
            DivergenceTest(
                group_a=response_times_prod[samples["data"][0]]["response_times"],
                group_b=response_times_prod[samples["data"][1]]["response_times"]
            ).score
        )

        print("----------------------------")


verify_against_real_world_data()

