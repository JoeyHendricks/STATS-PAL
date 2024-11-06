import pandas as pd
import numpy as np
import math


np.seterr(divide='ignore', invalid='ignore')


def calculate_percentage_change(old: float, new: float) -> float:
    """
    Will calculate the percentage change.
    :param old: The old measurement.
    :param new: the new measurement.
    :return: The percentage change as an absolute and a float
    """
    try:
        change = float(((new - old) / old) * 100)
        return 0.00 if math.isnan(change) or math.isinf(change) else change

    except ZeroDivisionError:
        return 0.00


def normalize_array(data: list, percentile: float) -> np.array:
    """
    Will normalize a given raw distribution to its maximum.
    param data: A list of raw measurements that need to be normalized.
    param percentile: the percentile cut-off point of the data everything below this point
    will be excluded from normalisation
    :return: An normalized list of data.
    """
    percentile = np.percentile(data, percentile)
    data = [value for value in data if value <= percentile]
    return np.array(data)


def calculate_ecdf(normalized_sample: tuple) -> pd.DataFrame:
    """
    Will calculate the eCDF to find the empirical distribution of our population.
    This function will then create a dataframe which will contain the measure
    and its probability.
    Furthermore, this function also gives the option to filter out the outliers
    on the extreme ends of our new distribution.
    More info about empirical cumulative distribution functions can be found here:
    https://en.wikipedia.org/wiki/Empirical_distribution_function
    :param normalized_sample: A normalized list of measurements
    :return: a data frame containing the ECDF
    """
    return pd.DataFrame(
        {
            'measure': np.sort(normalized_sample),
            'probability': np.arange(len(normalized_sample)) / float(len(normalized_sample)),
        }
    ).fillna(0.00)


def validate_thresholds_on_given_value(change: float, thresholds: dict) -> bool:
    """
    Will check the boundary of a change value by validating if the value -
    breaches the max or min boundary.
    :param change: The change value
    :param thresholds: The threshold key value pair containing max and min values.
    :return:
    """
    if thresholds["max"] is not None and change > thresholds["max"] or \
            thresholds["min"] is not None and change < thresholds["min"]:
        return False

    else:
        return True


def validate_letter_rank_boundary(boundary_letter_rank: str, current_letter_rank: str) -> bool:
    """
    Check if a boundary of a letter rank based on the pre-defined boundary matrix.
    By matching the letter rank to a number determining if a letter rank is above or below -
    another letter rank,
    The boundary matrix:
         - "S": 7,
         - "A": 6,
         - "B": 5,
         - "C": 4,
         - "D": 3,
         - "E": 2,
         - "F": 1
    :param boundary_letter_rank: The boundary letter rank.
    :param current_letter_rank: The calculated letter rank.
    :return: Either True or False if the letter rank is greater than the threshold -
    the test is passed, so it will output True otherwise the test is failed, and it will -
    output false.
    """
    # Determine rank as a number using the matrix
    letter_rank_matrix = {
        "S": 7,
        "A": 6,
        "B": 5,
        "C": 4,
        "D": 3,
        "E": 2,
        "F": 1
    }
    boundary_rank = letter_rank_matrix[boundary_letter_rank]
    active_rank = letter_rank_matrix[current_letter_rank[0]]

    # See if rank falls under or above the set boundary
    if active_rank >= boundary_rank or boundary_rank is None:
        return True
    else:
        return False
