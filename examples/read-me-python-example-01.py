# coding=utf-8
from heuristics.kolmogorov_smirnov_and_wasserstein import StatisticalDistance
from heuristics.misc.measurements import Measurements

from data import file_location_hendricks_raw_data_set_001  # <-- My primary example data set.
from data.wranglers import ConvertCsvResultsIntoDictionary
"""

"""
# As an example I provided a way to quickly convert a csv file into a Python dictionary.
data_set = ConvertCsvResultsIntoDictionary(file_location_hendricks_raw_data_set_001).data

# Feed your raw data to the measurements object to calculate the relevant statistics.
baseline_measurements = Measurements(data=data_set["RID-5"]["response_times"])
benchmark_measurements = Measurements(data=data_set["RID-4"]["response_times"])

# Setup and run the distance test against the given data.
stats_distance_test = StatisticalDistance(
    baseline_ecdf=baseline_measurements.ecdf,
    benchmark_ecdf=benchmark_measurements.ecdf,

    # The heuristics boundaries that I use myself.
    heuristics_boundaries={
        "letter_ranks": [

            {"wasserstein_boundary": 0.020, "kolmogorov_smirnov_boundary": 0.060, "rank": "S"},
            {"wasserstein_boundary": 0.030, "kolmogorov_smirnov_boundary": 0.070, "rank": "A"},
            {"wasserstein_boundary": 0.040, "kolmogorov_smirnov_boundary": 0.080, "rank": "B"},
            {"wasserstein_boundary": 0.050, "kolmogorov_smirnov_boundary": 0.090, "rank": "C"},
            {"wasserstein_boundary": 0.075, "kolmogorov_smirnov_boundary": 0.100, "rank": "D"},
            {"wasserstein_boundary": 0.100, "kolmogorov_smirnov_boundary": 0.125, "rank": "E"},
            {"wasserstein_boundary": 0.125, "kolmogorov_smirnov_boundary": 0.150, "rank": "F"},
        ],
        "score_boundaries": {
            "wasserstein_lowest_boundary": 0.030,
            "kolmogorov_smirnov_lowest_boundary": 0.060,
            "matrix_size": 100,
            "boundary_increment": 0.001
        }
    }
)

# Below printed information can be used to control a CI/CD pipeline.
print(stats_distance_test.kolmogorov_smirnov_distance)  # >> 0.080
print(stats_distance_test.wasserstein_distance)         # >> 0.107
print(stats_distance_test.score)                        # >> 23.21
print(stats_distance_test.letter_rank)                  # >> F
