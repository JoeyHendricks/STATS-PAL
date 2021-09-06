import pandas as pd
import string
import random
import json


class CreateFictitiousScenario:

    def __init__(self, increase=0, decrease=0):

        self.transaction_specifications = {

            "TR-001": {"start": 0.010, "end": 0.060, "throughput": 8000},
            "TR-002": {"start": 0.050, "end": 0.100, "throughput": 1500},
            "TR-003": {"start": 0.600, "end": 0.800, "throughput": 1200},
            "TR-004": {"start": 0.300, "end": 1.400, "throughput": 1600},
            "TR-005": {"start": 0.100, "end": 0.200, "throughput": 1000},
            "TR-006": {"start": 2.000, "end": 8.000, "throughput": 1200},
            "TR-007": {"start": 1.500, "end": 3.000, "throughput": 1000},
            "TR-008": {"start": 0.100, "end": 0.500, "throughput": 4000},
            "TR-009": {"start": 0.010, "end": 0.100, "throughput": 2500},
            "TR-010": {"start": 0.800, "end": 1.000, "throughput": 1000},
        }

        self.baseline_test_id = self._generate_random_string()
        self.benchmark_test_id = self._generate_random_string()
        self.baseline_x, self.baseline_y = self._create_fictitious_population()
        self.benchmark_x, self.benchmark_y = self._create_fictitious_population()

        if increase != 0 or decrease != 0:
            self.benchmark_y = self._increase_or_decrease_population(self.benchmark_y, increase, decrease)

    @staticmethod
    def _generate_random_string():
        """
        will generate a random identifier
        :return:
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

    def _create_fictitious_population(self):
        """


        """
        y = []
        x = []
        for transaction in self.transaction_specifications:
            for _ in range(0, self.transaction_specifications[transaction]["throughput"]):
                measurement = random.uniform(
                    self.transaction_specifications[transaction]["start"],
                    self.transaction_specifications[transaction]["end"],
                )
                y.append(measurement)
        for offset in range(0, len(y)):
            x.append(offset)

        return x, y

    @staticmethod
    def _increase_or_decrease_population(population, increase=0, decrease=0):
        """

        :param increase:
        :param decrease:
        :return:
        """
        changed_population = []
        for measurement in population:
            if increase > 0:
                measurement += measurement / 100 * increase

            elif decrease > 0:
                measurement -= measurement / 100 * decrease
            changed_population.append(measurement)

        return changed_population


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


