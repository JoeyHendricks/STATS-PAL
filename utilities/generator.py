import pandas as pd
import string
import random
import json

random.seed(1541561651354842310231651651321321654)  # <-- Used to make test runs consistent
# 1541561651354842310231651651321321654

class CreateFictitiousScenario:

    def __init__(self):

        self.fictitious_measurement_ranges = {"start": 50, "end": 100}

        self.baseline_sample_size = 1000
        self.baseline_percentage_increased = {"start": 0, "end": 0}
        self.baseline_percentage_decreased = {"start": 0, "end": 0}
        self.baseline_test_id = self._generate_random_string()
        self._baseline_measurements = None

        self.benchmark_sample_size = 1000
        self.benchmark_test_id = self._generate_random_string()
        self.benchmark_percentage_increased = {"start": 0, "end": 0}
        self.benchmark_percentage_decreased = {"start": 0, "end": 0}
        self._benchmark_measurements = None
        self.x_axis = None

    @staticmethod
    def _generate_random_string():
        """
        will generate a random identifier
        :return:
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

    def _create_fictitious_sample(self, sample_size: int, increase: dict, decrease: dict):
        """
        Will create a fictitious sample on which the PercentileHypothesisTest can be tested.

        :param sample_size: The increase in sample size.
        :param increase: the increase in percentage to the measurement.
        :param decrease: the decrease in percentage to the measurement.
        :return: The generated sample size.
        """
        sample = []
        self.x_axis = []
        for offset in range(0, sample_size):
            fictitious_measurement = random.randint(
                self.fictitious_measurement_ranges["start"],
                self.fictitious_measurement_ranges["end"]
            )
            if increase["start"] > 0:
                fictitious_measurement += fictitious_measurement / 100 * random.randint(
                    increase["start"],
                    increase["end"]
                )

            elif decrease["start"] > 0:
                fictitious_measurement -= fictitious_measurement / 100 * random.randint(
                    decrease["start"],
                    decrease["end"]
                )

            self.x_axis.append(offset)
            sample.append(fictitious_measurement)

        return sample

    @property
    def baseline_measurements(self):
        """

        :return:
        """
        if self._baseline_measurements is None:
            self._baseline_measurements = self._create_fictitious_sample(
                sample_size=self.baseline_sample_size,
                increase=self.baseline_percentage_increased,
                decrease=self.baseline_percentage_decreased
            )
        return self._baseline_measurements

    @baseline_measurements.setter
    def baseline_measurements(self, value):
        self._baseline_measurements = value

    @property
    def benchmark_measurements(self):
        """

        :return:
        """
        if self._benchmark_measurements is None:
            self._benchmark_measurements = self._create_fictitious_sample(
                sample_size=self.benchmark_sample_size,
                increase=self.benchmark_percentage_increased,
                decrease=self.benchmark_percentage_decreased
            )
        return self._benchmark_measurements

    @benchmark_measurements.setter
    def benchmark_measurements(self, value):
        self._benchmark_measurements = value


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
