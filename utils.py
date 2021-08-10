import string
import random

random.seed(12345678910)  # <-- Used to make test runs consistent
# 121515


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
