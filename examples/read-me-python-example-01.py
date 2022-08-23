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
baseline_measurements = Measurements(data=data_set["RID-1"]["response_times"])
benchmark_measurements = Measurements(data=data_set["RID-2"]["response_times"])


# Run the distance test against the given data.
stats_distance_test = StatisticalDistance(
    baseline_ecdf=baseline_measurements.ecdf,
    benchmark_ecdf=benchmark_measurements.ecdf
)

# Below printed information can be used to control a CI/CD pipeline.
print(stats_distance_test.kolmogorov_smirnov_distance)  # >> 0.080
print(stats_distance_test.wasserstein_distance)         # >> 0.107
print(stats_distance_test.score)                        # >> 23.21
print(stats_distance_test.letter_rank)                  # >> F
