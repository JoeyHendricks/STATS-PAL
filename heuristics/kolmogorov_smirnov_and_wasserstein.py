from scipy.stats import wasserstein_distance, ks_2samp
import pandas as pd
import numpy as np


class StatisticalDistanceTest:
    """
    This class is an algorithm that uses the kolmogorov smirnov statistics
    to define how much distance there is between a baseline and a benchmark
    test execution.

    To interpret how much distance is to much for us we use an heuristic
    to make sense of our statistics to make an best effort estimation
    if we tolerate a change or not.

    This is done by letter ranking the kolmogorov smirnov and Wasserstein
    distance statistic from the S to F (using the Japanese ranking system),
    alternatively a score from 0 to 100 can also be used or the distance
    value itself can also be used to interpret the results and make a quick
    decision whether to accept the change or refuse it.

    Using this approach to rapidly perform an baseline versus benchmark analysis
    we can fit this method into a CI/CD pipeline to be able to do a accurate
    performance analysis in an automated fashion.

    Keep in mind that this approach leans toward being a heuristic method because
    of the unpredictable nature of performance test results it is difficult
    to create a model that will fit a very wide array of test results.

    The models used in this class can there for be consider as a general guideline
    which can be adjusted to fit your own need.
    """

    # The letter rank that interprets the wasserstein & kolmogorov smirnov distance.
    LETTER_RANKS = [

        {"wasserstein_boundary": 0.030, "kolmogorov_smirnov_boundary": 0.080, "rank": "S"},
        {"wasserstein_boundary": 0.060, "kolmogorov_smirnov_boundary": 0.150, "rank": "A"},
        {"wasserstein_boundary": 0.100, "kolmogorov_smirnov_boundary": 0.180, "rank": "B"},
        {"wasserstein_boundary": 0.125, "kolmogorov_smirnov_boundary": 0.220, "rank": "C"},
        {"wasserstein_boundary": 0.150, "kolmogorov_smirnov_boundary": 0.260, "rank": "D"},
        {"wasserstein_boundary": 0.200, "kolmogorov_smirnov_boundary": 0.300, "rank": "E"},
        {"wasserstein_boundary": 0.250, "kolmogorov_smirnov_boundary": 0.340, "rank": "F"},

    ]

    # The matrix used to score the d-value from 0 to 100.
    SCORING_MATRIX = [

        {"wasserstein_boundary": 0.030, "kolmogorov_smirnov_boundary": 0.080, "punishment": 0.00210437},
        {"wasserstein_boundary": 0.035, "kolmogorov_smirnov_boundary": 0.085, "punishment": 0.00217105},
        {"wasserstein_boundary": 0.040, "kolmogorov_smirnov_boundary": 0.090, "punishment": 0.00787242},
        {"wasserstein_boundary": 0.045, "kolmogorov_smirnov_boundary": 0.095, "punishment": 0.00791472},
        {"wasserstein_boundary": 0.050, "kolmogorov_smirnov_boundary": 0.100, "punishment": 0.00814541},
        {"wasserstein_boundary": 0.055, "kolmogorov_smirnov_boundary": 0.105, "punishment": 0.00884361},
        {"wasserstein_boundary": 0.060, "kolmogorov_smirnov_boundary": 0.110, "punishment": 0.00907313},
        {"wasserstein_boundary": 0.065, "kolmogorov_smirnov_boundary": 0.115, "punishment": 0.01296521},
        {"wasserstein_boundary": 0.070, "kolmogorov_smirnov_boundary": 0.120, "punishment": 0.01383224},
        {"wasserstein_boundary": 0.075, "kolmogorov_smirnov_boundary": 0.125, "punishment": 0.01443168},
        {"wasserstein_boundary": 0.080, "kolmogorov_smirnov_boundary": 0.130, "punishment": 0.01624729},
        {"wasserstein_boundary": 0.085, "kolmogorov_smirnov_boundary": 0.135, "punishment": 0.01760769},
        {"wasserstein_boundary": 0.090, "kolmogorov_smirnov_boundary": 0.140, "punishment": 0.01886994},
        {"wasserstein_boundary": 0.095, "kolmogorov_smirnov_boundary": 0.145, "punishment": 0.02218302},
        {"wasserstein_boundary": 0.100, "kolmogorov_smirnov_boundary": 0.150, "punishment": 0.02376578},
        {"wasserstein_boundary": 0.105, "kolmogorov_smirnov_boundary": 0.155, "punishment": 0.02734606},
        {"wasserstein_boundary": 0.110, "kolmogorov_smirnov_boundary": 0.160, "punishment": 0.03823586},
        {"wasserstein_boundary": 0.115, "kolmogorov_smirnov_boundary": 0.165, "punishment": 0.03894435},
        {"wasserstein_boundary": 0.120, "kolmogorov_smirnov_boundary": 0.170, "punishment": 0.04147971},
        {"wasserstein_boundary": 0.125, "kolmogorov_smirnov_boundary": 0.175, "punishment": 0.04562214},
        {"wasserstein_boundary": 0.130, "kolmogorov_smirnov_boundary": 0.180, "punishment": 0.04700291},
        {"wasserstein_boundary": 0.135, "kolmogorov_smirnov_boundary": 0.185, "punishment": 0.04833569},
        {"wasserstein_boundary": 0.140, "kolmogorov_smirnov_boundary": 0.190, "punishment": 0.06287215},
        {"wasserstein_boundary": 0.145, "kolmogorov_smirnov_boundary": 0.195, "punishment": 0.06680662},
        {"wasserstein_boundary": 0.150, "kolmogorov_smirnov_boundary": 0.200, "punishment": 0.07658837},
        {"wasserstein_boundary": 0.155, "kolmogorov_smirnov_boundary": 0.205, "punishment": 0.08191112},
        {"wasserstein_boundary": 0.160, "kolmogorov_smirnov_boundary": 0.210, "punishment": 0.08290606},
        {"wasserstein_boundary": 0.165, "kolmogorov_smirnov_boundary": 0.215, "punishment": 0.15592140},

    ]

    def __init__(self, population_a: list, population_b: list) -> None:
        """
        Will construct the class and calculate all the required statistics.
        After all of the computation have been completed the following information can then
        be extracted from this class:

        :param population_a: An list of floats of the A population (baseline).
        :param population_b: An list of floats of the B population (benchmark).
        """
        self.sample_size = min([len(population_a), len(population_b)])
        self.sample_a = self._calculate_empirical_cumulative_distribution_function(population_a)
        self.sample_b = self._calculate_empirical_cumulative_distribution_function(population_b)
        self._ws_d_value = self._calculate_wasserstein_distance_statistics()
        self._ks_d_value, self._ks_p_value = self._calculate_kolmogorov_smirnov_distance_statistics()
        self.rank = self._letter_rank_distance_statistics()
        self.score = self._score_distance_statistics()

    @property
    def wasserstein_distance(self) -> float:
        """
        Gives the computed value of distance from sample a versus sample b.
        This value represent how much effort there is required to move the
        distribution of sample a toward b.

        More information about this metric can be found here:

        https://en.wikipedia.org/wiki/Wasserstein_metric

        :return: The wasserstein distance as rounded float
        until the third decimal.
        """
        return self._ws_d_value

    @property
    def kolmogorov_smirnov_distance(self) -> float:
        """
        Computes the absolute distance between 2 distribution representing
        the maximum distance between sample A and B.

        More information about this metric can be found here:

        https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test

        :return: The kolmogorov smirnov distance as rounded float
        until the third decimal.
        """
        return self._ks_d_value

    @property
    def kolmogorov_smirnov_probability(self) -> float:
        """
        Not used in any of the calculation in this heuristic but it might be helpful
        for engineers that also want to perform a official KS-test on their data
        to verify if the change is statistically relevant.

        More info on probability value's:

        https://en.wikipedia.org/wiki/P-value

        :return: The kolmogorov smirnov probability value
        """
        return self._ks_p_value

    @staticmethod
    def normalize_raw_data(raw_data: object) -> list:
        """
        Will normalize a given raw distribution to its maximum.
        :return:
        """
        return (np.array(raw_data) - np.array(raw_data).mean()) / np.array(raw_data).std()

    def _calculate_empirical_cumulative_distribution_function(self, population: list) -> object:
        """
        Will calculate the eCDF to find the empirical distribution of our population.
        It will randomly build a sample based on the smallest population size from there
        this function will then create a dataframe which will contain the measure
        and its probability.

        Further more this function also gives the option to filter out the outliers
        on the extreme ends of our new distribution.
        More info about empirical cumulative distribution functions can be found here:

        https://en.wikipedia.org/wiki/Empirical_distribution_function

        :param population: The provided measurements from one collected population.
        :return: The empirical cumulative distribution function (outliers filtered or not filtered)
        """
        normalized_sample = self.normalize_raw_data(population)
        sample = pd.DataFrame(
            {
                'measure': np.sort(normalized_sample),
                'probability': np.arange(len(normalized_sample)) / float(len(normalized_sample)),
            }
        )
        sample = sample[~(sample['probability'] >= 0.96)]
        return sample

    def _calculate_wasserstein_distance_statistics(self) -> float:
        """
        Computes the Wasserstein distance or Kantorovich–Rubinstein metric also known
        as the Earth mover's distance. This metric represents how much effort is needed
        to move the benchmark distribution towards the baseline.

        :return: Will return the Wasserstein metric as a float from a normalized distribution.
        """
        wasserstein = wasserstein_distance(
            self.sample_a["measure"].values,
            self.sample_b["measure"].values
        )
        return round(wasserstein, 3)

    def _calculate_kolmogorov_smirnov_distance_statistics(self) -> tuple:
        """
        Will use the kolmogorov smirnov statistical test to calculate the
        distance between two ECDF distributions. The KS test measures how
        significant the change is between the 2 largest points.

        :return: Gives back the KS-test D-value & the P-Value
        """
        kolmogorov_smirnov_distance, kolmogorov_smirnov_probability = ks_2samp(
            self.sample_a["measure"].values,
            self.sample_b["measure"].values
        )
        return round(kolmogorov_smirnov_distance, 3), kolmogorov_smirnov_probability

    def _score_distance_statistics(self) -> float:
        """
        An heuristic that will estimate a score between 0 - 100 using the
        Wasserstein distance and the kolmogorov smirnov distance.
        It determines the distance by using defined boundaries to lower the score
        if they are breached.

        Allowing for an more accurate threshold that can
        be used to decide if the change acceptable or not.

        :return: A score from 0 - 100 which can be interpret by a engineer.
        """
        ks_score = 1
        ws_score = 1
        for boundary in self.SCORING_MATRIX:
            if self._ws_d_value >= boundary["wasserstein_boundary"]:
                ws_score -= boundary["punishment"]

            if self._ks_d_value >= boundary["kolmogorov_smirnov_boundary"]:
                ks_score -= boundary["punishment"]
        return round(float(ks_score + ws_score) / 2 * 100, 2)

    def _letter_rank_distance_statistics(self) -> str:
        """
        An heuristic that will estimate a rank of what the amount of change is
        between our distributions. This rank is based on the Japanese letter
        ranking system the letters can be interpreted the following way:


        |  Rank |        Severity       |             Action              |
        |-------|-----------------------|---------------------------------|
        |   S   | Almost None           | Automated release to production |
        |   A   | Very low              | Automated release to production |
        |   B   | Low                   | Pending impact analysis needed  |
        |   C   | Medium                | Halt create minor defect        |
        |   D   | High                  | Halt create medium defect       |
        |   E   | Very High             | Halt create major defect        |
        |   F   | Significant change    | Halt create Priority defect     |
        |-------|-----------------------|---------------------------------|

        Depending on your situation it is fine to also automatically release
        to production when a B rank is produced as the impact is low.
        If you choose to do that I would recommend to also create a defect
        to document the automated release with an low performance risk.

        :return: The letter rank in the form as string ranging from S to F
        """
        for grade in self.LETTER_RANKS:
            ks_critical_grade = grade["kolmogorov_smirnov_boundary"]
            wasserstein_critical_grade = grade["wasserstein_boundary"]
            if self._ws_d_value < wasserstein_critical_grade and self._ks_d_value < ks_critical_grade:
                return grade["rank"]
            else:
                continue
        return "F"
