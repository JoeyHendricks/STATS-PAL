# coding=utf-8
from heuristics.misc.helpers import normalize_array, calculate_ecdf

import numpy as np
import pandas as pd


class Measurements:

    def __init__(self, data: list):
        """
        Will load in the object and map the object arguments to attributes.
        These attributes ares used to identify the data.

        :param data: the raw data.
        """
        super(Measurements, self).__init__()

        # Arguments
        self._provided_measurements = data

    @property
    def raw(self) -> list:
        """
        This property represent the collected data in its raw format.
        It is used by this object itself to calculate other metrics and information.
        The object will automatically cache the data inside this object.

        :return: A tuple containing all the raw data.
        """
        return self._provided_measurements

    @raw.setter
    def raw(self, value: list) -> None:
        """
        For transactional object collection the raw data needs to be appended a lot.
        :param value: additional measurements that need to be added to the object
        """
        self._provided_measurements += value

    @property
    def normalized(self) -> tuple:
        """
        Will normalize a given raw distribution to its maximum.
        When normalizing it wil exclude all measurement below the 95th percentile.
        This is done because of the increased amount of swing that can exist within -
        the higher part of the percentile spectrum.
        :return:
        """
        if "_normalized_" not in self.__dict__.keys():
            self.__dict__["_normalized_"] = normalize_array(self.raw)
        return self.__dict__["_normalized_"]

    @property
    def ecdf(self) -> pd.DataFrame:
        """
        The ECDF (empirical cumulative distribution function)
        Will calculate the eCDF to find the empirical distribution of our population.
        This function will then create a dataframe which will contain the measure
        and its probability.

        Further more this function also gives the option to filter out the outliers
        on the extreme ends of our new distribution.
        More info about empirical cumulative distribution functions can be found here:
        https://en.wikipedia.org/wiki/Empirical_distribution_function

        :return: The empirical cumulative distribution function (outliers filtered or not filtered)
        """
        if "_ecdf_" not in self.__dict__.keys():
            self.__dict__["_ecdf_"] = calculate_ecdf(normalized_sample=self.normalized)
            # sample[~(sample['probability'] >= 0.95)]
        return self.__dict__["_ecdf_"]

    @property
    def average(self) -> float:
        """
        The average metric calculated over all of the measurements.
        :return: a float that represents the average of the sample
        """
        if "_average_" not in self.__dict__.keys():
            self.__dict__["_average_"] = round(
                float(
                    np.average(
                        self.raw  # All measurements
                    )
                ),
                2
            )
        return self.__dict__["_average_"]

    @property
    def outliers(self) -> pd.DataFrame:
        """
        Will calculate the ECDF (empirical cumulative distribution function) to find the
        empirical distribution of our population.
        It will  filter out all the measurement that are below a probability of 95%.
        Effectively isolating the outliers from the rest of the population for a
        separate analysis.
        :return:A dataframe with outliers
        """
        if "_outliers_" not in self.__dict__.keys():
            percentile = np.percentile(self.raw, 95)
            self.__dict__["_outliers_"] = [value for value in self.raw if value >= percentile]
        return self.__dict__["_outliers_"]

    @property
    def max(self) -> float:
        """
        Will find out the minimum outlier
        from all of the collected measurements (raw data).
        :return: A float that is the maximum number.
        """
        if "_max_" not in self.__dict__.keys():
            self.__dict__["_max_"] = float(max(self.raw))
        return self.__dict__["_max_"]

    @property
    def min(self) -> float:
        """
        Will find out the maximum outlier
        from all of the collected measurements (raw data).
        :return: A float that is the maximum number.
        """
        if "_min_" not in self.__dict__.keys():
            self.__dict__["_min_"] = float(min(self.raw))
        return self.__dict__["_min_"]

    @property
    def standard_deviation(self) -> float:
        """
        Will calculate the standard deviation over
        the collected measurements. (raw data)
        :return: A float which is the standard deviation.
        """
        if "_standard_deviation_" not in self.__dict__.keys():
            self.__dict__["_standard_deviation_"] = float(np.std(self.raw))
        return self.__dict__["_standard_deviation_"]

    @property
    def median(self) -> float:
        """
        Will calculate the median over
        the collected measurements. (raw data)
        :return: A float which is the standard deviation.
        """
        if "_median_" not in self.__dict__.keys():
            self.__dict__["_median_"] = float(np.median(self.raw))
        return self.__dict__["_median_"]

    @property
    def percentiles(self) -> list:
        """
        Will calculate a pre-defined set of percentiles from the raw data.
        :return: Will return the percentile measurement as a tuple.
        """
        if "_percentiles_" not in self.__dict__.keys():
            self.__dict__["_percentiles_"] = []
            for percentile in range(1, 100):
                self.__dict__["_percentiles_"].append(
                    float(np.percentile(np.array(self.raw), percentile))
                )
        return self.__dict__["_percentiles_"]

    @property
    def count(self) -> int:
        """
        Will count how many measurements there
        are loaded into this object.
        In the performance engineering context this
        count is considered the throughput of a performance test.

        :return: Will return an integer representing the count.
        """
        if "_count_" not in self.__dict__.keys():
            self.__dict__["_count_"] = len(self.raw)
        return self.__dict__["_count_"]

    @property
    def sum(self) -> float:
        """
        This total amount of all of the measurement combined.
        :return: returns an integer representing the total sum
        of all measurements.
        """
        if "_sum_" not in self.__dict__.keys():
            self.__dict__["_sum_"] = sum(self.raw)
        return self.__dict__["_sum_"]
