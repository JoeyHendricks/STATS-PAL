from scipy.stats import ks_2samp
import pandas as pd
import numpy as np


class DistanceTest:
    """
    This class is an algorithm that uses the kolmogorov smirnov statistics
    to define how much distance there is between a baseline and a benchmark
    test execution.

    To interpret how much distance is to much for us we use an heuristic
    to make sense of our statistics to make an best effort estimation
    if we tolerate a change or not.

    This is done by letter ranking the kolmogorov smirnov distance statistic
    from the S to F (using the Japanese ranking system), alternatively a score
    from 0 to 100 can also be used or the distance value itself can also be used
    to interpret the results and make a quick decision whether to accept
    the change or refuse it.

    Using this approach to rapidly perform an baseline versus benchmark analysis
    we can fit this method into a CI/CD pipeline to be able to do a accurate
    performance analysis in an automated fashion.

    Keep in mind that this approach leans toward being a heuristic method because
    of the unpredictable nature of performance test results it is difficult
    to create a model that will fit a very wide array of test results.

    The models used in this class can there for be consider as a general guideline
    which can be adjusted to fit your own need.
    """

    # The letter ranks that interpret the KS distance statistic.
    LETTER_RANKS = [

        {"boundary": 0.020, "letter": "S"},
        {"boundary": 0.040, "letter": "A"},
        {"boundary": 0.060, "letter": "B"},
        {"boundary": 0.080, "letter": "C"},
        {"boundary": 0.100, "letter": "D"},
        {"boundary": 0.120, "letter": "E"},
        {"boundary": 0.140, "letter": "F"},

    ]

    def __init__(self, population_a: list, population_b: list, filter_outliers=True) -> None:
        """
        Will construct the class and calculate all the required statistics.
        After all of the computation have been completed the following information can then
        be extracted from this class:

        :param population_a: An list of floats of the A population (baseline).
        :param population_b: An list of floats of the B population (benchmark).
        """
        self.filter_outliers = filter_outliers
        self.sample_size = min([len(population_a), len(population_b)])
        self.sample_a = self._calculate_empirical_cumulative_distribution_function(population_a)
        self.sample_b = self._calculate_empirical_cumulative_distribution_function(population_b)
        self.d_value, self.p_value, self.score = self._calculate_kolmogorov_smirnov_statistics()
        self.rank = self._letter_rank_kolmogorov_smirnov_distance_statistic()

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
        raw_sample = np.random.choice(population, self.sample_size)
        sample = pd.DataFrame(
            {
                'measure': np.sort(raw_sample),
                'probability': np.arange(len(raw_sample)) / float(len(raw_sample)),
            }
        )
        if self.filter_outliers is True:
            # Removing irrelevant low and high outliers
            sample = sample[~(sample['probability'] <= 0.05)]
            sample = sample[~(sample['probability'] >= 0.95)]
        return sample

    def _calculate_kolmogorov_smirnov_statistics(self) -> tuple:
        """
        Will use the kolmogorov smirnov statistical test to calculate the
        distance between two ECDF distributions.

        :return: Will return three metrics a the absolute distance between
        our distributions as "distance", It will return the probability value
        from the KS-Test and it will output a score based on the distance to
        represent the change in the form of simple score.
        """
        distance, probability = ks_2samp(
            self.sample_a["measure"].values,
            self.sample_b["measure"].values
        )
        score = 100 - (distance * 100)
        return distance, probability, score

    def _letter_rank_kolmogorov_smirnov_distance_statistic(self) -> str:
        """
        An heuristic that will estimate a rank of what the amount of change is
        between our distributions. This rank is based on the Japanese letter
        ranking system the letters can be interpreted the following way:

        S =
        A =
        B =
        C =
        D =
        E =
        F =

        :return: The letter rank in the form as string ranging from S to F
        """
        for grade in self.LETTER_RANKS:
            if self.d_value < grade["boundary"]:
                return grade["letter"]
            else:
                continue
        return "F"
