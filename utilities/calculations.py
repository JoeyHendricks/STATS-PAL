import numpy as np
from sklearn import preprocessing


def calculate_percentile(array: list, percentile: int) -> float:
    """
    Used to calculate the percentile over the given array.
    :return: a float number of the requested percentile
    """
    return float(np.percentile(array, percentile))


def normalize_distribution(raw: list) -> list:
    """
    Will normalize a given distribution,
    :return:
    """
    maximum = max(raw)
    norm = [np.divide(i, maximum) for i in raw]
    return norm
