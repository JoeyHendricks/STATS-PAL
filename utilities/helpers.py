import pandas as pd
import numpy as np
import string
import random
import json

random.seed(513513251)  # <-- Used to make test runs consistent
# 1541561651354842310231651651321321654


def calculate_percentile(array: list, percentile: int) -> float:
    """
    Used to calculate the percentile over the given array.
    :return: a float number of the requested percentile
    """
    return float(np.percentile(array, percentile))


def normalize_distribution(raw):
    """

    :return:
    """
    return [float(i)/sum(raw) for i in raw]


class CreateFictitiousScenario:

    def __init__(self, increase=0, decrease=0):

        self.transaction_specifications = {

            "TR-001": {"start": 0.010, "end": 0.060, "throughput": 800},
            "TR-002": {"start": 0.050, "end": 0.100, "throughput": 1500},
            "TR-003": {"start": 0.600, "end": 0.800, "throughput": 1000},
            "TR-004": {"start": 0.300, "end": 1.400, "throughput": 1600},
            "TR-005": {"start": 0.100, "end": 0.200, "throughput": 1000},
            "TR-006": {"start": 2.000, "end": 8.000, "throughput": 1200},
            "TR-007": {"start": 1.500, "end": 3.000, "throughput": 800},
            "TR-008": {"start": 0.100, "end": 0.500, "throughput": 900},
            "TR-009": {"start": 0.010, "end": 0.100, "throughput": 750},
            "TR-010": {"start": 0.800, "end": 1.000, "throughput": 1000},
        }

        self.baseline_test_id = self._generate_random_string()
        self.benchmark_test_id = self._generate_random_string()

        self.baseline_x, self.baseline_y = self._create_fictitious_sample()
        self.benchmark_x, self.benchmark_y = self._create_fictitious_sample(increase=increase, decrease=decrease)

    @staticmethod
    def _generate_random_string():
        """
        will generate a random identifier
        :return:
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

    def _create_fictitious_sample(self, increase=0, decrease=0):
        """

        :param increase:
        :param decrease:
        """
        y = []
        x = []
        for transaction in self.transaction_specifications:
            for _ in range(0, self.transaction_specifications[transaction]["throughput"]):
                measurement = random.uniform(
                    self.transaction_specifications[transaction]["start"],
                    self.transaction_specifications[transaction]["end"],
                )
                if increase > 0:
                    measurement += measurement / 100 * increase

                elif decrease > 0:
                    measurement -= measurement / 100 * decrease

                y.append(measurement)
        for offset in range(0, len(y)):
            x.append(offset)

        return x, y


class ConvertCsvResultsIntoJson:

    def __init__(self, path: str) -> None:
        """
        When constructed will start the conversion process.
        :param path: The path to the file
        """
        self.file = pd.read_csv(path, chunksize=10000, delimiter=";")
        self.data = {}
        self.convert_csv_to_json()

    @property
    def json(self):
        """
        will convert the python dictionary to true json
        :return:
        """
        return json.dumps(self.data)

    def convert_csv_to_json(self) -> None:
        """
        Will read the csv file in chunks and convert it to json.
        """
        for chunk in self.file:
            self.add_chunk_to_json(chunk)

    def add_chunk_to_json(self, chunk) -> None:
        """
        Will transfer the lines of the chunk into the json data set.
        Keep in mind that the json structure will be kept in the
        correct order.
        That way it is possible to still connect the Y axis to the X axis
        and see which action was executed.
        :param chunk: A part of the csv (10k rows)
        """
        for line in chunk.values.tolist():

            response_time = float(line[0].replace(",", "."))
            runid = line[1]
            timestamp = line[2]
            action = line[3]

            if runid not in self.data:
                self.data[runid] = {
                    "response_times": [response_time],
                    "timestamps": [timestamp],
                    "actions": [action]
                }

            else:
                self.data[runid]["response_times"].append(response_time)
                self.data[runid]["timestamps"].append(timestamp)
                self.data[runid]["actions"].append(action)
"""
from heuristic_algorithms.performance_analysis_hypothesis_test import DivergenceTest

seeds = []
for _ in range(0, 10000):
    seeds.append(random.randint(152100, 1000001521654651))

scores = []
for seed in seeds:
    random.seed(seed)  # <-- Used to make test runs consistent
    scenario = CreateFictitiousScenario(increase=0)
    c_value = DivergenceTest(
        group_a=scenario.baseline_y,
        group_b=scenario.benchmark_y
    ).c_value
    with open('scores.txt', 'a') as f:
        f.write(f"{str(c_value)}\n")
"""

