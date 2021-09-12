import pandas as pd
import random
import json


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


class CreateFictitiousScenario:

    def __init__(self, data_set_location, percentage=0, delta=0, baseline_id="RID-3", benchmark_id="RID-4"):
        """

        :param percentage:
        :param delta:
        :param baseline_id:
        :param benchmark_id:
        """
        scenarios = ConvertCsvResultsIntoJson(data_set_location).data

        self.baseline_x = scenarios[baseline_id]["timestamps"]
        self.baseline_y = scenarios[baseline_id]["response_times"]
        self.benchmark_y = scenarios[benchmark_id]["response_times"]
        self.benchmark_x = scenarios[benchmark_id]["timestamps"]

        self.baseline_test_id = baseline_id
        self.benchmark_test_id = benchmark_id

        self.benchmark_y = self.randomly_decrease_or_increase_part_of_the_population(
            population=self.benchmark_y,
            percentage=percentage,
            delta=delta,
        )

    @staticmethod
    def randomly_decrease_or_increase_part_of_the_population(population, percentage=0, delta=0):
        """

        :param delta:
        :param population:
        :param percentage:
        :return:
        """
        for _ in range(0, int(len(population) / 100 * percentage)):
            rand_index = abs(random.randint(0, len(population) - 1))
            change = float(population[rand_index] / 100 * delta)
            current = population[rand_index]
            new = current + change
            population[rand_index] = new

        return population


def generate_delta_array():
    """

    :return:
    """
    array = []
    delta = 0
    while delta <= 99:
        array.append(round(delta, 3))
        delta = delta + 1
    return array
