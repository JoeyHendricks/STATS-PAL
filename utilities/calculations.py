import numpy as np


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
    return [float(i)/sum(raw) for i in raw]
